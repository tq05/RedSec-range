# Security & responsible use

RedSec Range is **deliberately vulnerable software for education**. Please read this
before deploying it.

## This repository contains real vulnerabilities on purpose

Every target ships genuine, working flaws — prompt injection, indirect injection,
SSRF, path traversal, command-injection RCE, insecure deserialization, credential
exfiltration, and more. They exist so defenders can learn to find and fix them.

## Rules for running it

- **Isolate it.** Run only on a throwaway/lab cluster or local machine you control.
  The Kubernetes chart default-denies egress precisely so targets can't phone home;
  do not weaken that on a shared network.
- **Never expose a target to the internet or an untrusted network.** Targets are
  ClusterIP-only by default. Do not put one behind a public LoadBalancer/Ingress.
  Docker paths publish ports on `127.0.0.1`. Binding elsewhere
  (`REDSEC_BIND_HOST=all` or another address) is refused unless you also set
  `REDSEC_ALLOW_PUBLIC_BIND=1`, and is always refused inside a Codespace.
- **Never point a target at production** data, credentials, models, or services.
- **Use the canaries, not real secrets.** All planted flags/tokens are fake.
- The RCE target (`07/vuln-mcp`) executes a shell. It is marked `privileged`
  (a deliberately weak application), which forbids egress. Its container still runs
  as uid 10001 with all capabilities dropped and is contained by NetworkPolicy. Keep
  it in an isolated namespace and never on a node you care about.
- External catalog ranges are third-party deliberately vulnerable code. RedSec pins
  their default Git revisions, builds them locally, binds ports to loopback, and
  gives each an internal Docker network. Review upstream changes before running
  `redsec ranges update`; use `--allow-egress` only on a disposable host when an
  exercise explicitly needs internet content.

## Intended use

Learning, training, CTF-style exercises, tool evaluation, and building/validating
defenses for AI and MCP systems. Only test systems you own or are explicitly
authorized to test. You are responsible for complying with applicable law and the
terms of any service you interact with.

## Reporting a vulnerability *in the framework itself*

The targets are *supposed* to be exploitable. If you find a flaw in the
**framework** (the CLI, verifier, deploy tooling, chart, or sink) that could harm a
user running the range as intended — for example a container escape path not gated
by `privileged`, a verifier bypass, or the sink/CLI being exploitable from a target
— please report it privately to the maintainers rather than opening a public issue,
and give us reasonable time to fix it. (Set a security contact / advisory policy for
your fork before publishing.)

### Security maintainers

| Maintainer | GitHub |
| --- | --- |
| rolfh9 | [@rolfh9](https://github.com/rolfh9) |

## A note on the mock model

The included model is a deterministic stand-in that reproduces LLM failure modes for
reproducibility. It is not a real model and has no safety relevance of its own; the
vulnerabilities taught live in the *applications*, which is the point.

## Integrity & isolation model (read before relying on results)

- **The verifier is a teaching oracle, not a tamper-proof judge.** Side-effect
  (oracle) challenges confirm an exploit by watching the shared `drop` sink. Each
  range start generates a random range token that only the sink and the targets
  receive. Targets send it with their sink posts, and oracle checks count only those
  trusted events, so posting a marker to the sink directly no longer passes. Anyone
  who controls the host can still read the token: from target process environments in
  local mode, `docker inspect` on the Docker paths, or the `drop-token` Secret on
  Kubernetes. RCE challenges (module 08) read it legitimately from inside the target.
  For graded/benchmark use, treat `redsec selftest` (which runs the *reference
  exploit* end-to-end) as the source of truth.
- **Isolation depends on the run path.** The Kubernetes path puts each module in a
  default-deny namespace (egress enforced with a policy CNI; DNS is allowed only to
  the cluster resolver) with no service-account token mounted. The Docker paths run
  RedSec containers with all capabilities dropped, `no-new-privileges`, and a PID
  limit; third-party range containers get `no-new-privileges` and a PID limit.
  **Bare local-process mode (`redsec dev/up`) has no isolation** — and
  modules 07 (shell RCE), 08 (unsafe deserialization) and 09 (SSRF, which can reach a
  real cloud metadata endpoint on a cloud VM) are genuinely dangerous there, so
  `redsec dev/up` refuses them unless you pass `--unsafe-local`. Run those modules
  via the Docker range (`range up`) or Kubernetes, on a throwaway host, never on a
  machine or network you care about. Local targets receive only basic host variables
  (`PATH`, `HOME`, locale, …) and `REDSEC_*` settings, not the rest of your shell
  environment. Cloud, GitHub, Fly, and other credentials there are not handed to
  them. The one exception is `REDSEC_LLM_API_KEY`, which you set deliberately for a
  real-model backend. Process isolation is still absent.
- External catalog adapters currently use Docker isolation on the same host. They do
  not inherit the built-in Helm NetworkPolicy and are not deployed into the built-in
  Kubernetes namespaces. Each target joins only an internal network; a read-only
  gateway forwards its declared host ports. The target receives a routed bridge only
  when the operator explicitly enables egress.
