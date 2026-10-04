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
- **Never point a target at production** data, credentials, models, or services.
- **Use the canaries, not real secrets.** All planted flags/tokens are fake.
- The RCE target (`07/vuln-mcp`) executes a shell. It is marked `privileged` and is
  contained by NetworkPolicy; keep it in an isolated namespace and never on a node
  you care about.

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

## A note on the mock model

The included model is a deterministic stand-in that reproduces LLM failure modes for
reproducibility. It is not a real model and has no safety relevance of its own; the
vulnerabilities taught live in the *applications*, which is the point.
