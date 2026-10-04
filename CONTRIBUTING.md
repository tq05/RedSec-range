# Contributing

Contributions are very welcome — new modules, completing scaffolds, better
verifiers, additional attack vectors, docs, and fixes.

## Dev setup

```bash
pip install -e ".[dev]"
pip install kubernetes-validate      # for offline manifest validation
redsec doctor                        # sanity-check all modules load
pytest -q                            # unit + integration
```

## Adding or completing a module

See [docs/authoring-modules.md](docs/authoring-modules.md). The nine scaffold
modules already have a complete design (`module.yaml` + `lesson.md`); "completing"
one means implementing its targets, verifiers, and `solution/solve.py`, then setting
`status: complete`. Modules **03** and **07** are the reference implementations.

A module is not mergeable as `complete` until:

```bash
redsec selftest <id>     # must go fail -> pass
pytest -q                # integration test picks it up automatically
```

## Standards

- **Keep targets faithful.** A vuln should teach the real failure mode; the
  deterministic mock model is there to keep it reproducible, not to fake the bug.
- **Prefer oracle verifiers** (prove the side effect) over flag-only for
  action-style vulns. Make oracle needles per-vector so `selftest`'s fail-before
  guard stays meaningful.
- **Containment by default.** New targets are non-root and egress-denied unless
  there's a documented reason (`privileged`/`egress` must be explicit in the
  manifest).
- **Map it.** Fill in `mappings` (AI-300 / OWASP LLM / OWASP MCP / ATLAS) honestly;
  mark uncertain ATLAS IDs as indicative.
- **Lessons are part of the product.** Include theory, a walkthrough, and defenses.
- Python: standard library + the existing deps; keep targets small and readable
  (they're teaching material). Run `pytest` and `redsec doctor` before a PR.

## Scope / safety

By contributing you agree the content is for education and defense. Do not add
payloads designed to attack real third-party systems, real malware, or anything that
only functions outside the isolated lab. See [SECURITY.md](SECURITY.md).

## License

Contributions are accepted under the project's Apache-2.0 license.
