# Authoring a module

A module is self-contained and declarative. To add one you write three things —
a manifest, a target, a verifier — and ship a reference exploit so CI can prove it
works. No framework or infrastructure code needs changing.

```
modules/NN-slug/
├── module.yaml          # metadata, targets, challenges, verify, hints
├── lesson.md            # the guided lesson
├── targets/<name>/      # vulnerable app(s): app.py + Dockerfile
├── verify/checks.py     # optional custom Check classes
└── solution/solve.py    # reference exploit: solve(endpoints, drop_url) -> {"flags": {...}}
```

Copy module **03** (single HTTP app, builtin checks) or **07** (multi-target, MCP,
custom oracle checks) as your starting point.

## 1. `module.yaml`

```yaml
id: "12"
slug: my-attack
title: My Attack
status: scaffold          # -> complete once solvable; selftest only runs complete modules
difficulty: intermediate  # intro|beginner|intermediate|advanced|expert
summary: One paragraph.
prerequisites: ["03"]
tags: [example]
mappings:                 # traceability — keep these honest
  ai300_module: 12
  owasp_llm: [LLM01]
  owasp_mcp: []
  mitre_atlas: [AML.T0051]

targets:
  - name: app              # DNS-safe
    kind: http             # http | mcp | sink | custom
    build: targets/app     # dir with a Dockerfile (for docker/k8s)
    run: { asgi: app:app } # how `redsec dev` runs it locally (uvicorn)
    port: 9120
    privileged: false      # true only if the target needs weak isolation (e.g. RCE)
    network:
      egress: false        # default-deny egress (safety + lesson); drop is always reachable
  - name: drop
    kind: sink
    uses_builtin: drop      # the shared exfiltration oracle

challenges:
  - id: my-challenge
    title: Do the thing
    objective: What success looks like.
    points: 150
    primitive: example      # free-form label shown in `redsec info`
    verify:
      - type: flag           # flag | oracle | artifact
        flag: "REDSEC{...}"
    hints: ["nudge 1", "nudge 2", "near-spoiler"]

lesson: lesson.md
```

Run `redsec schema -o module.schema.json` to get the JSON Schema for editor
validation, and `redsec doctor` to check your manifest loads and its checks
resolve.

## 2. The target

A target is any HTTP service exposing `GET /healthz`. For LLM/agent targets, use
the shared engine so challenges stay deterministic and offline:

```python
from redsec.mockllm import Message, Tool, get_backend
backend = get_backend(secrets=["sk-canary"])   # mock by default; real via env
comp = backend.complete([Message("system", SYS), Message("user", msg)], TOOLS)
```

The engine follows instructions found in **any** channel (user, tool result,
retrieved doc, tool description) and resolves `{{SYSTEM_PROMPT}}` / `{{SECRETS}}` /
`{{MEMORY}}` placeholders — that's what makes injection payloads land. Read
`redsec/mockllm/engine.py`; it's short and is itself teaching material.

To exfiltrate for an **oracle** challenge, POST the stolen data to the shared sink
at `os.environ["REDSEC_DROP_URL"]` (`/collect/...`). Peer targets are reachable via
`REDSEC_URL_<NAME>` env vars (set in both local and K8s modes).

Add a `Dockerfile` (build context = repo root; copy `redsec/__init__.py` +
`redsec/mockllm/` + your `app.py`) and register the image in
`scripts/build_images.sh`.

## 3. The verifier

Use a builtin or write a `Check` in `verify/checks.py`:

```python
from redsec.verify.base import Check, CheckContext, CheckResult

class MyOracle(Check):
    def run(self, ctx: CheckContext) -> CheckResult:
        if ctx.drop_contains(self.params["needle"]):
            return CheckResult.ok("secret reached the sink")
        return CheckResult.fail("not yet")
```

Reference it from `module.yaml` as `check: "checks:MyOracle"` with `params`. See
[verification.md](verification.md) for the three patterns and when to use each.

## 4. The reference exploit

`solution/solve.py` must define:

```python
def solve(endpoints: dict[str, str], drop_url: str | None) -> dict:
    # exploit the live targets; return flags you extracted
    return {"flags": {"my-challenge": "REDSEC{...}"}}
```

It should **actually exploit** the target (extract flags live; cause the side
effects oracle checks look for) — not hardcode answers. That's what makes
`redsec selftest` a real test.

## 5. Finish

Set `status: complete` and run:

```bash
redsec selftest 12     # must go: verify FAIL (pre) -> exploit -> verify PASS (post)
pytest -q              # the integration test will pick it up automatically
```

If a verifier passes *before* the exploit, selftest fails — tighten it (prefer
per-vector markers so each challenge is satisfied only by its own exploit).
