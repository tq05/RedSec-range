# Deploy the range on Fly.io

This path creates one private Fly Machine, runs the Docker-backed RedSec Range
inside it, and lets a person or an AI harness control it. The deployment declares
no Fly services or public ports. Access goes through Fly SSH or a local `fly proxy`
tunnel.

Fly.io is a paid external service. You need a Fly account with billing enabled,
`flyctl`, and either an interactive login or a scoped `FLY_API_TOKEN`. Current
usage and stopped-Machine root filesystems can incur charges; destroy the app when
you finish. See [Fly pricing](https://fly.io/docs/about/pricing/).

Fly trial Machines without a payment method are automatically stopped after five
minutes. A focused module can finish its first build in that window, but the full
external catalog generally cannot. Add billing before using Fly for a complete
multi-range session; Codespaces remains the default hosted path.

The default Machine is `shared-cpu-2x` with 4 GB RAM, which fits a normal personal
Fly organization's per-Machine limits. Use `--modules` or `--ranges` to keep a
session focused. Running every external range together may require a larger
Machine; change `deploy/fly/fly.toml` when your organization allows one.

## Start and stop

```bash
# One-time setup
brew install flyctl                 # or use Fly's installer
fly auth login

# From the repository root
./deploy/fly/up.sh --ttl 60
./deploy/fly/status.sh
./deploy/fly/down.sh
```

`up.sh` generates a unique app name and saves it in `.redsec/fly.json`. Every
other helper reads that file, so app names do not need to be copied between
commands. Set `FLY_APP` or pass `--app NAME` when you need a fixed name. Useful
options include:

```bash
./deploy/fly/up.sh --region lhr --ttl 90
./deploy/fly/up.sh --modules "01 07"       # smaller range for a focused session
./deploy/fly/up.sh --ranges "builtin dvaa mcpgoat"  # several maintained ranges
./deploy/fly/up.sh --json                  # machine-readable completion record
```

For CI or an AI harness, set `FLY_API_TOKEN` instead of using `fly auth login`.
The script checks authentication, creates the app, stages any supported model
keys, deploys, and waits until all selected targets pass their health checks. A
failed first deployment removes the new app rather than leaving an unknown
resource behind.

## Use SSH directly

Open an interactive command centre:

```bash
./deploy/fly/ssh.sh

# Inside the Machine
range status
range solve 07
range verify 07
range shell 07 vuln-mcp
```

`ssh.sh` accepts normal `fly ssh console` options. The generated app has no public
service; Fly's SSH transport reaches it over Fly's private network.

## Drive it from Claude, Codex, or another harness

`exec.sh` is the non-interactive interface. It preserves the remote command's exit
status and is suitable for tool calls and CI:

```bash
./deploy/fly/exec.sh range status
./deploy/fly/exec.sh range solve 04
./deploy/fly/exec.sh redsec ranges status
./deploy/fly/exec.sh redsec ranges challenges mcpgoat
./deploy/fly/exec.sh 'range solve 07 resource-traversal'
./deploy/fly/status.sh --json
```

The root [`AGENTS.md`](../AGENTS.md) gives repository-aware agents the full setup,
test, and cleanup contract. A typical prompt is: “Deploy this repository to Fly,
test modules 04 and 07, report the results, then destroy the app.” Provisioning is
still an explicit action because it creates billable infrastructure.

Use only this `deploy/fly` workflow. A root-level `fly.toml` produced by
`fly launch` declares a public web service and is incompatible with the private
range lifecycle and Docker-in-Docker build context.

## Use a model as the assessor

The Machine includes the `assess` agent. `model.sh` runs it next to the targets so
all challenge traffic stays within the private Machine:

```bash
# Export before up.sh; it becomes a Fly secret.
export OPENAI_API_KEY=...
./deploy/fly/up.sh
./deploy/fly/model.sh 07 --provider openai --model gpt-5

# Or xAI
export XAI_API_KEY=...
./deploy/fly/up.sh
./deploy/fly/model.sh 04 --provider grok --model grok-4
```

Supported assessor providers are `openai`, `grok`, and `custom`. For a custom
OpenAI-compatible endpoint, set `REDSEC_LLM_API_KEY` before deployment and pass
the endpoint explicitly:

```bash
./deploy/fly/model.sh 05 --provider custom \
  --base-url https://gateway.example/v1 --model my-model
```

API keys passed with `--api-key` become command-line arguments. Prefer the Fly
secret path above. `up.sh` automatically stages `OPENAI_API_KEY`, `XAI_API_KEY`,
and `REDSEC_LLM_API_KEY` when they exist in the local environment.

The vulnerable targets use the deterministic mock model by default. To test the
targets themselves with a real OpenAI-compatible model, set these values on the
Fly app and restart the target containers:

```bash
APP=$(python3 -c 'import json; print(json.load(open(".redsec/fly.json"))["app"])')
fly secrets set --app "$APP" \
  REDSEC_LLM_BACKEND=openai \
  REDSEC_LLM_BASE_URL=https://api.openai.com/v1 \
  REDSEC_LLM_MODEL=gpt-5 \
  REDSEC_LLM_API_KEY="$OPENAI_API_KEY"
./deploy/fly/exec.sh 'range down-all && scripts/sandbox-up.sh'
```

The controller passes only the four `REDSEC_LLM_*` variables into target
containers. The assessor key variables are separate, so exporting an API key does
not silently change deterministic target behavior.

## Open a target in a browser or local tool

The challenge containers publish their ports on the Machine's private interface,
which lets [`fly proxy`](https://fly.io/docs/flyctl/proxy/) tunnel one port to
localhost:

```bash
./deploy/fly/proxy.sh 07            # module 07 primary target: localhost:9070
./deploy/fly/proxy.sh 9071 19071    # secondary target: localhost:19071
```

Run separate proxy processes when you need several ports. The primary module map
is:

| Module | Port | Module | Port |
|---|---:|---|---:|
| 01 | 9010 | 02 | 9020 |
| 03 | 9030 | 04 | 9040 |
| 05 | 9050 | 06 | 9060 |
| 07 | 9070 | 08 | 9080 |
| 09 | 9090 | 11 | 9110 |

Secondary ports are `9071`, `9091`, and `9112`. `range status` is the source of
truth for the live target map.

External ports can be tunneled numerically in the same way, for example
`deploy/fly/proxy.sh 7332` for MCPGoat or `deploy/fly/proxy.sh 9000` for DVAA.
See [external ranges](external-ranges.md) for the complete catalog and port map.

## Lifecycle and storage

`--ttl MINUTES` makes PID 1 exit after the deadline. The Fly restart policy leaves
the Machine stopped. It does not delete the app. `persist_rootfs = "restart"`
keeps the inner Docker state across Machine restarts, but a new deployment replaces
it. Run `down.sh` to destroy the app and remove the stopped root filesystem charge.

```bash
./deploy/fly/down.sh
./deploy/fly/down.sh --app redsec-range-...
```

No Fly Volume is created. The range is disposable, and redeploying may rebuild its
inner images and reset progress.

## How startup is verified

The outer image installs the Python package and dependencies at build time. At
boot, `entrypoint.sh` starts the enabled profile through `redsec ranges up`.
Startup fails if Docker, dependency installation, an image build, or a target
health check fails. Only then does it create `/run/redsec-ready`; `up.sh` waits
for that marker and a successful `redsec ranges status`.

Useful diagnostics:

```bash
./deploy/fly/status.sh
APP=$(python3 -c 'import json; print(json.load(open(".redsec/fly.json"))["app"])')
fly logs --app "$APP"
./deploy/fly/ssh.sh -C 'tail -100 /var/log/dockerd.log'
```

The local CI job builds and boots the Fly image with Docker-in-Docker and solves a
module without using Fly credentials. A live deployment still depends on Fly
account permissions, regional capacity, and remote-builder availability.

See also [the interactive sandbox](interactive-sandbox.md),
[the LLM assessor](llm-assessor.md), and [Kubernetes deployment](kubernetes.md).
