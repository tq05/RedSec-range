"""`redsec` command-line interface."""
from __future__ import annotations

import json
import os
import signal
import time
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from . import state
from .config import state_dir
from .deploy.local import local_range, start_range
from .loader import ModuleError, find, load_all
from .models import Module
from .range_catalog import load_catalog
from . import ranges as range_lifecycle
from .verify.base import CheckContext
from .verify.runner import run_challenge

app = typer.Typer(
    add_completion=False,
    help="RedSec Range -- a guided, self-verifying AI & MCP security training range.",
    no_args_is_help=True,
)
console = Console()
err = Console(stderr=True)
ranges_app = typer.Typer(
    add_completion=False,
    help="Enable and operate the built-in course and external maintained ranges.",
    no_args_is_help=True,
)
app.add_typer(ranges_app, name="ranges")

DIFF_COLOR = {
    "intro": "green", "beginner": "green", "intermediate": "yellow",
    "advanced": "red", "expert": "bright_red",
}
STATUS_ICON = {"complete": "[green]●[/]", "scaffold": "[yellow]◐[/]", "draft": "[dim]○[/]"}


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _running_file(module: Module) -> Path:
    return state_dir() / f"running-{module.id}.json"


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


def _running_endpoints(module: Module) -> tuple[dict[str, str], Optional[str]]:
    f = _running_file(module)
    if not f.is_file():
        raise typer.BadParameter(
            f"module {module.id} is not running locally. Start it with "
            f"`redsec dev {module.id}` (or deploy to k8s and use --endpoint)."
        )
    data = json.loads(f.read_text())
    return data["endpoints"], data.get("drop_url")


def _ctx(module: Module, submitted_flag: str | None = None,
         artifact: str | None = None) -> CheckContext:
    endpoints, drop = _running_endpoints(module)
    return CheckContext(endpoints=endpoints, drop_url=drop,
                        submitted_flag=submitted_flag, artifact=artifact)


def _challenge(module: Module, cid: str):
    for c in module.challenges:
        if c.id == cid:
            return c
    raise typer.BadParameter(f"module {module.id} has no challenge {cid!r}")


# --------------------------------------------------------------------------- #
# discovery
# --------------------------------------------------------------------------- #
@ranges_app.command("list")
def list_ranges() -> None:
    """List built-in, external, and placeholder ranges."""
    catalog = load_catalog()
    rows = {row["id"]: row for row in range_lifecycle.status_rows(catalog)}
    table = Table(title="RedSec range catalog", header_style="bold cyan")
    table.add_column("ID")
    table.add_column("Range")
    table.add_column("Maintainer")
    table.add_column("Enabled", justify="center")
    table.add_column("Status")
    table.add_column("Revision", style="dim")
    for definition in catalog.ranges.values():
        row = rows[definition.id]
        enabled = "[green]yes[/]" if row["enabled"] else "[dim]no[/]"
        revision = (row["revision"] or "-")[:12]
        table.add_row(
            definition.id, definition.title, definition.maintainer,
            enabled, row["status"], revision,
        )
    console.print(table)
    console.print("[dim]The OffSec entry is reserved and cannot be enabled until a supported lab is published.[/]")


@ranges_app.command("enable")
def enable_ranges(
    range_ids: Optional[list[str]] = typer.Argument(None, help="range IDs or aliases"),
    all_ranges: bool = typer.Option(False, "--all", help="enable every available range"),
) -> None:
    """Add ranges to the enabled profile. Run `redsec ranges up` to start them."""
    definitions = range_lifecycle.selected_ranges(range_ids, select_all=all_ranges)
    if not range_ids and not all_ranges:
        raise typer.BadParameter("provide range IDs or --all")
    enabled = range_lifecycle.set_enabled([item.id for item in definitions], enable=True)
    console.print(f"enabled: [cyan]{' '.join(enabled)}[/]")
    console.print("start them with `redsec ranges up`")


@ranges_app.command("disable")
def disable_ranges(range_ids: list[str] = typer.Argument(..., help="range IDs or aliases")) -> None:
    """Stop ranges and remove them from the enabled profile."""
    definitions = range_lifecycle.resolve_many(range_ids)
    range_lifecycle.down_many(definitions)
    enabled = range_lifecycle.set_enabled([item.id for item in definitions], enable=False)
    console.print(f"enabled: [cyan]{' '.join(enabled) or '(none)'}[/]")


@ranges_app.command("up")
def ranges_up(
    range_ids: Optional[list[str]] = typer.Argument(None, help="range IDs or aliases"),
    all_ranges: bool = typer.Option(False, "--all", help="start every available range"),
    allow_egress: bool = typer.Option(
        False, help="allow external ranges to reach the internet at runtime"
    ),
    rebuild: bool = typer.Option(False, help="rebuild external images"),
) -> None:
    """Start explicit ranges, or all ranges in the enabled profile."""
    definitions = range_lifecycle.selected_ranges(range_ids, select_all=all_ranges)
    for result in range_lifecycle.up_many(
        definitions, allow_egress=allow_egress, rebuild=rebuild
    ):
        console.print(f"[green]up[/] {result['id']}")
        for name, url in result.get("endpoints", {}).items():
            console.print(f"  {name}: {url}")


@ranges_app.command("down")
def ranges_down(
    range_ids: Optional[list[str]] = typer.Argument(None, help="range IDs or aliases"),
    all_ranges: bool = typer.Option(False, "--all", help="stop every available range"),
) -> None:
    """Stop explicit ranges, or all ranges in the enabled profile."""
    definitions = range_lifecycle.selected_ranges(range_ids, select_all=all_ranges)
    range_lifecycle.down_many(definitions)
    console.print("stopped: " + " ".join(item.id for item in definitions))


@ranges_app.command("status")
def ranges_status(json_output: bool = typer.Option(False, "--json")) -> None:
    """Show enabled state, runtime status, revisions, and endpoints."""
    rows = range_lifecycle.status_rows()
    if json_output:
        print(json.dumps(rows, indent=2))
        return
    table = Table(title="RedSec ranges", header_style="bold cyan")
    table.add_column("ID")
    table.add_column("Enabled", justify="center")
    table.add_column("Status")
    table.add_column("Revision", style="dim")
    table.add_column("Endpoints")
    for row in rows:
        endpoints = "\n".join(f"{name}: {url}" for name, url in row["endpoints"].items())
        table.add_row(
            row["id"], "yes" if row["enabled"] else "no", row["status"],
            (row["revision"] or "-")[:12], endpoints or "-",
        )
    console.print(table)
    unhealthy = [
        row["id"] for row in rows
        if row["enabled"] and row["availability"] == "available"
        and row["status"] != "running"
    ]
    if unhealthy:
        raise typer.Exit(1)


@ranges_app.command("update")
def ranges_update(range_ids: list[str] = typer.Argument(..., help="external range IDs")) -> None:
    """Fetch, build, and if necessary restart external ranges individually."""
    for definition in range_lifecycle.resolve_many(range_ids):
        old, new, restarted = range_lifecycle.update_one(definition)
        action = "rebuilt and restarted" if restarted else "rebuilt"
        console.print(f"{definition.id}: {old[:12]} -> {new[:12]} ({action})")


@ranges_app.command(
    "exec", context_settings={"allow_extra_args": True, "ignore_unknown_options": True}
)
def ranges_exec(
    ctx: typer.Context,
    range_id: str = typer.Argument(...),
) -> None:
    """Run a command in an external range container."""
    definition = range_lifecycle.resolve_many([range_id])[0]
    command = list(ctx.args)
    if not command:
        raise typer.BadParameter("provide a command after the range ID")
    raise typer.Exit(range_lifecycle.container_exec(definition, command))


@ranges_app.command("shell")
def ranges_shell(range_id: str) -> None:
    """Open an interactive shell in an external range container."""
    definition = range_lifecycle.resolve_many([range_id])[0]
    raise typer.Exit(range_lifecycle.container_exec(definition, ["sh"], interactive=True))


@ranges_app.command("entrypoints")
def ranges_entrypoints(range_id: str) -> None:
    """List named stdio servers supplied by an external range adapter."""
    definition = range_lifecycle.resolve_many([range_id])[0]
    if not definition.runtime.entrypoints:
        console.print(f"{definition.id} has no named stdio entrypoints")
        return
    table = Table(title=f"{definition.id} stdio entrypoints", header_style="bold cyan")
    table.add_column("Name")
    table.add_column("Command", style="dim")
    for name, command in definition.runtime.entrypoints.items():
        table.add_row(name, " ".join(command))
    console.print(table)


@ranges_app.command("launch")
def ranges_launch(range_id: str, entrypoint: str) -> None:
    """Attach stdin/stdout to a named MCP server inside an external range."""
    definition = range_lifecycle.resolve_many([range_id])[0]
    command = definition.runtime.entrypoints.get(entrypoint)
    if not command:
        raise typer.BadParameter(
            f"unknown entrypoint {entrypoint!r}; run `redsec ranges entrypoints {definition.id}`"
        )
    raise typer.Exit(range_lifecycle.container_exec(definition, command))


@app.command("list")
def list_modules() -> None:
    """List all modules in the curriculum."""
    t = Table(title="RedSec Range -- Curriculum", header_style="bold cyan")
    t.add_column("ID"); t.add_column("Module"); t.add_column("Diff")
    t.add_column("St", justify="center"); t.add_column("Chal", justify="right")
    t.add_column("Pts", justify="right"); t.add_column("Maps", style="dim")
    for _, m in load_all():
        diff = f"[{DIFF_COLOR.get(m.difficulty.value, 'white')}]{m.difficulty.value}[/]"
        maps = " ".join(m.mappings.owasp_llm + m.mappings.owasp_mcp) or "-"
        t.add_row(m.id, m.title, diff, STATUS_ICON.get(m.status, "?"),
                  str(len(m.challenges)), str(m.points), maps)
    console.print(t)
    console.print("  [green]●[/] complete   [yellow]◐[/] scaffold   [dim]○[/] draft")


@app.command()
def info(module: str) -> None:
    """Show details and challenges for a module."""
    mdir, m = find(module)
    body = [f"[bold]{m.title}[/]  ([cyan]{m.id}[/])", "", m.summary, ""]
    body.append(f"Difficulty: {m.difficulty.value}   Status: {m.status}   "
                f"~{m.estimated_minutes} min   {m.points} pts")
    maps = m.mappings
    if maps.ai300_module:
        body.append(f"AI-300 module: {maps.ai300_module}")
    if maps.owasp_llm:
        body.append(f"OWASP LLM: {', '.join(maps.owasp_llm)}")
    if maps.owasp_mcp:
        body.append(f"OWASP MCP: {', '.join(maps.owasp_mcp)}")
    if maps.mitre_atlas:
        body.append(f"MITRE ATLAS: {', '.join(maps.mitre_atlas)}")
    console.print(Panel("\n".join(body), border_style="cyan"))

    t = Table(header_style="bold")
    t.add_column("Challenge"); t.add_column("Title"); t.add_column("Pts", justify="right")
    t.add_column("Primitive", style="dim"); t.add_column("Solved", justify="center")
    for c in m.challenges:
        solved = "[green]✓[/]" if state.is_solved(m.id, c.id) else ""
        t.add_row(c.id, c.title, str(c.points), c.primitive or "", solved)
    if m.challenges:
        console.print(t)
    console.print(f"\nLesson: [dim]{mdir / m.lesson}[/]  "
                  f"(view with `redsec lesson {m.id}`)")


@app.command()
def lesson(module: str) -> None:
    """Render a module's guided lesson."""
    mdir, m = find(module)
    path = mdir / m.lesson
    if not path.is_file():
        err.print(f"[red]lesson not found: {path}[/]")
        raise typer.Exit(1)
    console.print(Markdown(path.read_text()))


# --------------------------------------------------------------------------- #
# local development
# --------------------------------------------------------------------------- #
@app.command()
def dev(module: str) -> None:
    """Run a module's targets locally (no Docker/K8s). Ctrl-C to stop."""
    mdir, m = find(module)
    if not m.targets:
        err.print(f"[yellow]module {m.id} defines no targets (scaffold).[/]")
        raise typer.Exit(1)
    console.print(f"Starting [bold]{m.title}[/] locally ...")
    with local_range(m, mdir) as rng:
        _running_file(m).write_text(json.dumps(
            {"endpoints": rng.endpoints, "drop_url": rng.drop_url}, indent=2))
        t = Table(title=f"{m.title} -- running", header_style="bold green")
        t.add_column("Target"); t.add_column("URL")
        for name, url in rng.endpoints.items():
            t.add_row(name, url)
        console.print(t)
        console.print("\nIn another shell: "
                      f"`redsec lesson {m.id}` · `redsec hint {m.id} <chal>` · "
                      f"`redsec verify {m.id}`\n[dim]Ctrl-C to stop.[/]")
        try:
            signal.pause()
        except (KeyboardInterrupt, AttributeError):
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
        finally:
            _running_file(m).unlink(missing_ok=True)
    console.print("stopped.")


@app.command()
def up(module: str) -> None:
    """Start a module's targets in the BACKGROUND (for walkthroughs/automation).

    Unlike `dev` (which blocks), this returns immediately so you can run
    `redsec verify`/`submit` in the same shell. Stop it with `redsec down`.
    """
    mdir, m = find(module)
    if not m.targets:
        err.print(f"[yellow]module {m.id} defines no targets.[/]")
        raise typer.Exit(1)
    if _running_file(m).is_file():
        console.print(f"module {m.id} already running (use `redsec down {m.id}` first).")
        raise typer.Exit(1)
    rng = start_range(m, mdir, detached=True)
    _running_file(m).write_text(json.dumps(
        {"endpoints": rng.endpoints, "drop_url": rng.drop_url, "pids": rng.pids},
        indent=2))
    t = Table(title=f"{m.title} -- running (background)", header_style="bold green")
    t.add_column("Target"); t.add_column("URL")
    for name, url in rng.endpoints.items():
        t.add_row(name, url)
    console.print(t)
    console.print(f"[dim]verify with `redsec verify {m.id}` · stop with `redsec down {m.id}`[/]")


@app.command()
def down(module: str) -> None:
    """Stop a background range started with `redsec up`."""
    _, m = find(module)
    f = _running_file(m)
    if not f.is_file():
        console.print(f"module {m.id} is not running.")
        return
    data = json.loads(f.read_text())
    pids = data.get("pids", [])

    def _signal_all(sig: int) -> None:
        for pid in pids:
            try:  # detached procs are their own session/group leaders
                os.killpg(os.getpgid(pid), sig)
            except (ProcessLookupError, PermissionError):
                pass
            try:
                os.kill(pid, sig)
            except (ProcessLookupError, PermissionError):
                pass

    _signal_all(signal.SIGTERM)
    time.sleep(1.0)
    alive = [p for p in pids if _pid_alive(p)]
    if alive:
        _signal_all(signal.SIGKILL)
    f.unlink(missing_ok=True)
    console.print(f"stopped range for module {m.id} ({len(pids)} process(es)).")


# --------------------------------------------------------------------------- #
# kubernetes
# --------------------------------------------------------------------------- #
@app.command()
def render(module: str, registry: str = "ghcr.io/redsec-range",
           tag: str = "latest", instance: Optional[str] = None) -> None:
    """Render Kubernetes manifests for a module (helm template) to stdout."""
    from .deploy import k8s

    _, m = find(module)
    try:
        print(k8s.render(m, registry, tag, instance))
    except RuntimeError as e:
        err.print(f"[red]{e}[/]"); raise typer.Exit(1)


@app.command()
def deploy(module: str, registry: str = "ghcr.io/redsec-range",
           tag: str = "latest", instance: Optional[str] = None) -> None:
    """Deploy a module to the current Kubernetes context (helm upgrade --install)."""
    from .deploy import k8s

    _, m = find(module)
    try:
        console.print(k8s.deploy(m, registry, tag, instance))
    except RuntimeError as e:
        err.print(f"[red]{e}[/]"); raise typer.Exit(1)


@app.command()
def destroy(module: str, instance: Optional[str] = None) -> None:
    """Uninstall a module's Kubernetes release."""
    from .deploy import k8s

    _, m = find(module)
    try:
        console.print(k8s.destroy(m, instance))
    except RuntimeError as e:
        err.print(f"[red]{e}[/]"); raise typer.Exit(1)


# --------------------------------------------------------------------------- #
# play: hints, submit, verify
# --------------------------------------------------------------------------- #
@app.command()
def hint(module: str, challenge: str, n: int = typer.Option(0, help="hint index")) -> None:
    """Reveal a hint for a challenge (progressive)."""
    _, m = find(module)
    c = _challenge(m, challenge)
    if not c.hints:
        console.print("[dim]no hints for this challenge.[/]"); return
    idx = max(0, min(n, len(c.hints) - 1))
    console.print(Panel(c.hints[idx], title=f"hint {idx + 1}/{len(c.hints)}",
                        border_style="yellow"))
    if idx < len(c.hints) - 1:
        console.print(f"[dim]next: `redsec hint {m.id} {challenge} --n {idx + 1}`[/]")


def _run_and_report(m: Module, mdir: Path, ctx: CheckContext, challenge) -> bool:
    outcome = run_challenge(mdir, challenge, ctx)
    for o in outcome.outcomes:
        tag = "[green]PASS[/]" if o.result.passed else "[red]FAIL[/]"
        console.print(f"  {tag} [{o.step.type}] {o.result.message}")
    if outcome.passed:
        state.mark_solved(m.id, challenge.id, challenge.points)
        console.print(f"[bold green]✓ solved {challenge.id} "
                      f"(+{challenge.points} pts)[/]")
    return outcome.passed


@app.command()
def submit(module: str, challenge: str, flag: str) -> None:
    """Submit a flag for a flag-based challenge."""
    mdir, m = find(module)
    c = _challenge(m, challenge)
    # Flag checks work offline; oracle checks need a running range.
    needs_range = any(s.type != "flag" for s in c.verify)
    ctx = (_ctx(m, submitted_flag=flag) if needs_range
           else CheckContext(endpoints={}, submitted_flag=flag))
    _run_and_report(m, mdir, ctx, c)


@app.command()
def verify(module: str, challenge: Optional[str] = typer.Argument(None),
           flag: Optional[str] = typer.Option(None),
           artifact_file: Optional[Path] = typer.Option(None)) -> None:
    """Run verifiers for a challenge (or all challenges) of a running module."""
    mdir, m = find(module)
    art = artifact_file.read_text() if artifact_file else None
    # Artifact-only modules have no running targets; flag/artifact checks don't
    # need endpoints. Only resolve a running range when the module has targets.
    if m.targets:
        ctx = _ctx(m, submitted_flag=flag, artifact=art)
    else:
        ctx = CheckContext(endpoints={}, submitted_flag=flag, artifact=art)
    challenges = [_challenge(m, challenge)] if challenge else m.challenges
    any_pass = False
    for c in challenges:
        console.print(f"[bold]{c.id}[/] -- {c.title}")
        # Flag challenges are recorded when you `submit`; a later `verify` sweep has
        # no flag to recheck, so honor the solved state instead of showing a scary
        # FAIL. Oracle/artifact challenges still run live the first time.
        if state.is_solved(m.id, c.id) and not flag and not art:
            console.print("  [green]PASS[/] already solved")
            any_pass = True
            continue
        if _run_and_report(m, mdir, ctx, c):
            any_pass = True
    raise typer.Exit(0 if any_pass or not challenges else 1)


@app.command()
def score() -> None:
    """Show your progress across the range."""
    t = Table(title="Progress", header_style="bold cyan")
    t.add_column("Module"); t.add_column("Solved", justify="right")
    t.add_column("Points", justify="right")
    grand = 0
    for _, m in load_all():
        solved = sum(1 for c in m.challenges if state.is_solved(m.id, c.id))
        pts = sum(c.points for c in m.challenges if state.is_solved(m.id, c.id))
        grand += pts
        if m.challenges:
            t.add_row(f"{m.id} {m.title}", f"{solved}/{len(m.challenges)}", str(pts))
    console.print(t)
    console.print(f"[bold]Total: {grand} pts[/]")


@app.command()
def reset(module: str) -> None:
    """Reset local progress for a module."""
    _, m = find(module)
    state.reset_module(m.id)
    console.print(f"reset progress for module {m.id}.")


# --------------------------------------------------------------------------- #
# authoring / CI
# --------------------------------------------------------------------------- #
@app.command()
def doctor() -> None:
    """Validate every module loads, resolves its checks, and (if complete) ships a solution."""
    ok = True
    for mdir, m in load_all():
        problems: list[str] = []
        for c in m.challenges:
            for s in c.verify:
                if s.check:
                    try:
                        from .loader import load_check
                        load_check(mdir, s.check)
                    except Exception as e:
                        problems.append(f"{c.id}: check {s.check} -> {e}")
        if m.status == "complete":
            if not (mdir / "solution").is_dir():
                problems.append("status=complete but no solution/ directory")
            if not any((mdir / "solution").glob("solve.py")) if (mdir / "solution").is_dir() else False:
                problems.append("status=complete but no solution/solve.py")
        icon = "[green]OK[/]" if not problems else "[red]!![/]"
        console.print(f"{icon} {m.id} {m.title}")
        for p in problems:
            console.print(f"     [red]- {p}[/]"); ok = False
    raise typer.Exit(0 if ok else 1)


@app.command()
def selftest(module: Optional[str] = typer.Argument(None),
             keep: bool = typer.Option(False, help="leave the range running on failure")) -> None:
    """Prove a module is solvable: start it, verify FAIL, run the reference
    solution, verify PASS. This is the correctness guarantee run in CI."""
    import importlib.util

    mods = [find(module)] if module else [
        (d, m) for d, m in load_all() if m.status == "complete"
    ]
    if not mods:
        err.print("[yellow]no complete modules to self-test.[/]"); raise typer.Exit(0)

    failures = 0
    for mdir, m in mods:
        console.rule(f"selftest: {m.id} {m.title}")
        solve_py = mdir / "solution" / "solve.py"
        if not solve_py.is_file():
            err.print(f"[red]{m.id}: missing solution/solve.py[/]"); failures += 1
            continue
        spec = importlib.util.spec_from_file_location(f"solve_{m.id}", solve_py)
        assert spec and spec.loader
        solmod = importlib.util.module_from_spec(spec)
        try:
            with local_range(m, mdir) as rng:
                import sys as _sys
                _sys.path.insert(0, str(mdir))
                spec.loader.exec_module(solmod)
                # reset sink if present
                if rng.drop_url:
                    import httpx
                    httpx.post(f"{rng.drop_url}/reset", timeout=5)

                def mkctx(flag=None, artifact=None):
                    return CheckContext(endpoints=rng.endpoints,
                                        drop_url=rng.drop_url, submitted_flag=flag,
                                        artifact=artifact)

                # 1) FAIL before exploitation (guards against trivial verifiers).
                pre_ok = []
                for c in m.challenges:
                    oc = run_challenge(mdir, c, mkctx())
                    pre_ok.append((c.id, oc.passed))
                leaked_pre = [cid for cid, p in pre_ok if p]
                if leaked_pre:
                    err.print(f"[red]{m.id}: verifier passed BEFORE exploit for "
                              f"{leaked_pre} -- verifier too weak.[/]")
                    failures += 1

                # 2) Run the reference exploit.
                result = solmod.solve(rng.endpoints, rng.drop_url) or {}
                flags = result.get("flags", {})
                artifacts = result.get("artifacts", {})

                # 3) PASS after exploitation.
                for c in m.challenges:
                    oc = run_challenge(mdir, c, mkctx(flag=flags.get(c.id),
                                                      artifact=artifacts.get(c.id)))
                    tag = "[green]PASS[/]" if oc.passed else "[red]FAIL[/]"
                    console.print(f"  {tag} {c.id} -- {c.title}")
                    if not oc.passed:
                        failures += 1
                        for o in oc.outcomes:
                            if not o.result.passed:
                                console.print(f"        [red]{o.result.message}[/]")
        except Exception as e:
            err.print(f"[red]{m.id}: selftest error: {e}[/]")
            failures += 1

    if failures:
        err.print(f"\n[bold red]{failures} selftest failure(s).[/]")
        raise typer.Exit(1)
    console.print("\n[bold green]all selftests passed.[/]")


@app.command()
def schema(out: Optional[Path] = typer.Option(None, help="write to file")) -> None:
    """Emit the JSON Schema for module.yaml (for editor validation)."""
    s = json.dumps(Module.model_json_schema(), indent=2)
    if out:
        out.write_text(s); console.print(f"wrote {out}")
    else:
        print(s)


def main() -> None:  # console-script entrypoint
    try:
        app()
    except (ModuleError, range_lifecycle.RangeLifecycleError) as e:
        err.print(f"[red]{e}[/]")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
