# RedSec Range agent instructions

Read `CLAUDE.md` for architecture, module status, and project conventions. This
file defines the cloud workflows for repository-aware harnesses such as Codex and
Claude Code.

## Default GitHub Codespaces workflow

Codespaces is the default hosted environment. Its devcontainer installs the Python
package and starts the private Docker range automatically. Wait for
`.redsec/codespaces-ready`, then use the repository's command surface directly:

```bash
range status
redsec lesson 01
range solve 07
range shell 07 vuln-mcp
```

Do not provision Fly.io from a Codespace unless the user explicitly requests Fly.
Keep all forwarded challenge ports private; these targets are deliberately
vulnerable. Use `assess MODULE --provider ... --model ...` for an autonomous model
assessment. Read model keys from environment variables or Codespaces secrets and
never print or commit them.

For external SSH, the user can run `gh codespace ssh -R tq05/RedSec-range` after
authenticating the GitHub CLI. An external harness can run
`./scripts/codespaces-connect.sh range status` (or another command) over the same
authenticated SSH path. A repository connection alone does not create a tunnel or
move tool execution into the Codespace. Full details: `docs/codespaces.md`.

## Fly.io range workflow

Fly provisioning creates billable external infrastructure. Run it when the user
explicitly asks to deploy, test on Fly, or create a cloud range. The user must have
installed `flyctl` and authenticated with `fly auth login`, or provided a scoped
`FLY_API_TOKEN`.

From the repository root:

```bash
./deploy/fly/up.sh --json
./deploy/fly/status.sh --json
./deploy/fly/exec.sh range status
./deploy/fly/exec.sh range solve 07
./deploy/fly/down.sh --json
```

`up.sh` creates a unique private app and waits for target readiness. Deployment
state is stored in ignored `.redsec/fly.json`; all helpers use that app by default.
Use `--modules "01 07"` for a focused session and `--ttl MINUTES` as a compute
deadline.

Use `deploy/fly/ssh.sh` when the user wants an interactive shell. Use
`deploy/fly/exec.sh` for non-interactive harness commands. Use
`deploy/fly/model.sh MODULE ...` to run the bundled OpenAI-compatible assessor
inside the Machine. Model credentials must be supplied through environment
variables before `up.sh`; never print or commit them.

The range has no public services. Use `deploy/fly/proxy.sh MODULE_OR_PORT` only
when a local browser or HTTP client needs a target. Keep the proxy bound to its
default loopback address.

Always report the app name, readiness, commands run, verifier results, and whether
cleanup succeeded. Destroy the app after a throwaway test when the user requested
cleanup or did not request a persistent session. If the user wants the session
left running, report `deploy/fly/down.sh` and note that Fly charges can continue.

Full details: `docs/deploy-fly.md`.
