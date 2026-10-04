# Verification — "did the exploit actually work?"

The whole point of the range is that success is *checked*, not claimed. Each
challenge declares one or more `verify` steps; the runner instantiates each as a
`Check` and runs it against the deployed targets. A challenge passes only if every
step passes.

## The three patterns

### 1. Flag
The exploit reveals a canary string the learner submits. Good for *read*-style
vulns where the attacker directly sees a secret (traversal, prompt leakage,
enumeration).

```yaml
verify:
  - type: flag
    flag: "REDSEC{...}"        # or: flag_sha256: "<hex>"
```

`redsec submit <mod> <chal> REDSEC{...}` checks it (works offline).

### 2. Oracle (side-effect)
The verifier observes a *consequence* of the exploit and decides success itself —
no submission needed. This is the strongest pattern for *action*-style vulns
(exfiltration, excessive agency, confused deputy): it proves the secret actually
left the application, or a privileged action actually happened.

```yaml
verify:
  - type: oracle
    check: "builtins:DropContains"
    params: { needle: "sk-canary" }
```

The shared **drop** sink records anything a tricked target POSTs to it; `ctx.drop_contains(needle)`
checks it. `redsec verify <mod> <chal>` runs oracle checks against a running range.

Design oracle needles to be **per-vector** (a unique marker each exploit adds), so
a challenge is satisfied *only* by its own exploit — this keeps `selftest`'s
fail-before guard meaningful.

### 3. Artifact (scored)
The learner submits a produced artifact (an extracted system prompt, an inverted
embedding, a threat model) and the verifier scores it (match / similarity /
required-elements).

```yaml
verify:
  - type: artifact
    check: "checks:ArtifactCovers"
    params: { all_of: [model, prompt, secret], any_of: [llm01, mcp], min_matches: 1 }
```

`redsec verify <mod> <chal> --artifact-file model.md` passes the file contents as
`ctx.artifact`.

## The `Check` interface

```python
class Check:
    def __init__(self, **params): self.params = params
    def run(self, ctx: CheckContext) -> CheckResult: ...
```

`CheckContext` gives you, independent of where targets run (local or K8s):

| field | meaning |
|-------|---------|
| `ctx.base("name")` | base URL of a target |
| `ctx.client()` | an `httpx.Client` |
| `ctx.drop_url`, `ctx.drop_events()`, `ctx.drop_contains(s)` | the sink |
| `ctx.submitted_flag` | the learner's flag (flag checks) |
| `ctx.artifact` | learner-supplied artifact (artifact checks) |
| `ctx.params` | step params from `module.yaml` |

`CheckResult.ok(msg, **evidence)` / `CheckResult.fail(msg, **evidence)`.

Builtins (`builtins:Name`): `FlagCheck`, `DropContains`, `HttpContains`. Anything
module-specific lives in `verify/checks.py` and is referenced as `checks:Name`.

## The correctness guarantee

`redsec selftest <mod>` (and CI) runs, for every complete module:

1. **verify FAIL** — before the exploit, no challenge may pass (catches trivially
   true verifiers).
2. **run `solution/solve.py`** — the reference exploit.
3. **verify PASS** — after the exploit, every challenge must pass.

A module that doesn't flip fail → pass is not shippable.
