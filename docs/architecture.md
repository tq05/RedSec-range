# Architecture

## Pieces

- **`redsec` CLI** (`redsec/cli.py`) — discovers modules, renders lessons, runs
  targets locally (`dev`) or on Kubernetes (`deploy`/`render`), and drives play
  (`hint`/`submit`/`verify`/`score`) and CI (`doctor`/`selftest`).
- **Module model & loader** (`redsec/models.py`, `loader.py`) — parses and
  validates `module.yaml` into typed objects; dynamically loads module verifiers.
- **Verification framework** (`redsec/verify/`) — `Check`/`CheckContext`/`CheckResult`,
  a runner, and builtins. Three patterns: flag, oracle, artifact.
- **Mock LLM** (`redsec/mockllm/`) — a deterministic, deliberately-vulnerable model
  so LLM challenges are reproducible and offline. Pluggable to a real
  OpenAI-compatible endpoint via env.
- **Shared sink** (`redsec/services/drop/`) — an attacker-collection stand-in that
  records exfiltrated data for oracle verifiers.
- **Deploy backends** (`redsec/deploy/`) — `local.py` (processes via uvicorn) and
  `k8s.py` (derive Helm values from a module, invoke helm).
- **Helm chart** (`deploy/helm/redsec-module/`) — templates one module into an
  isolated namespace with default-deny networking.
- **Modules** (`modules/NN-slug/`) — the content: manifest, lesson, targets,
  verifier, reference solution.

## Request flow (a challenge)

```
learner ──HTTP──► vulnerable target(s) ──(tricked)──► drop sink
   │                                                     ▲
   └── redsec verify ──► Check.run(ctx) ─── reads ───────┘  (oracle)
   └── redsec submit ──► FlagCheck                          (flag)
```

`CheckContext` abstracts *where* targets live, so the same verifier works whether
the module runs as local processes or Kubernetes Services. Locally, the deploy
layer assigns ports and injects `REDSEC_DROP_URL` + `REDSEC_URL_<PEER>`; on
Kubernetes the Helm chart injects the equivalent service DNS.

## Why a mock model

Real LLMs are non-deterministic and increasingly guardrailed — bad for a
reproducible course and impossible for CI to assert on. The mock
(`mockllm/engine.py`) reproduces the *failure modes* faithfully (it trusts all
context channels equally, leaks its system prompt, and acts on injected tool
directives) while being a pure function of its inputs. The vulnerabilities taught
are properties of the **application** (how it assembles context and wires tools),
not of the mock, so they transfer to a real model — set `REDSEC_LLM_BACKEND=openai`
and `REDSEC_LLM_BASE_URL` to try it.

## Isolation model

Deliberately vulnerable targets are contained by:

- **NetworkPolicy** — default-deny, re-allowing only intra-namespace traffic and
  DNS. Targets can reach each other and the sink, but not the internet or other
  ranges. A target may opt into egress with `network.egress: true`.
- **Namespace per range** — `redsec-<module>[-<instance>]`.
- **No real secrets** — only planted canaries.
- **`privileged` is explicit** — a target only gets weak isolation (e.g. for the
  RCE challenge) when its manifest says so.

Containment is both a safety control and a lesson (Module 09 is about blast
radius). See [kubernetes.md](kubernetes.md).

## Extensibility

The module format is the API. The CLI/Helm/verifier never hard-code a module;
adding content is `module.yaml` + target + verifier (+ reference solution). See
[authoring-modules.md](authoring-modules.md).
