# Deploy to Fly.io — an ephemeral cloud range

Stand up the **whole** RedSec Range on a throwaway cloud VM, use it for an hour,
and destroy it — with remote access built in and **no VPC ingress rules and no
per-box VPN install**. Good for "I just want to mess around and run the
challenges" without touching your laptop's Docker or any cloud console.

> ⚠️ The targets are deliberately vulnerable (see [SECURITY.md](../SECURITY.md)).
> This setup is isolated by design: access is over Fly's private WireGuard only,
> nothing is published to the internet.

## TL;DR

```bash
# one-time
brew install flyctl && fly auth login     # or https://fly.io/docs/flyctl/install/

# from the repo root
export XAI_API_KEY=xai-...                 # optional: real Grok for targets + harness
./deploy/fly/up.sh                         # build + deploy one Machine

fly ssh console --app redsec-range-lab     # your command centre
#   range status
#   range solve 05               # run a reference exploit, verifier-scored
#   assess 05 --provider grok --model grok-4

./deploy/fly/down.sh                        # throw it all away
```

## What this is

One Fly **Machine** (a Firecracker micro-VM) runs an inner `dockerd` and brings
the range up with the repo's own [`scripts/sandbox-up.sh`](../scripts/sandbox-up.sh)
— the exact bootstrap used in the interactive sandbox
([docs/interactive-sandbox.md](interactive-sandbox.md)). You get the same
`range` / `grok` / `assess` command centre, in the cloud, reachable from anywhere
you can run `fly`.

Files live in [`deploy/fly/`](../deploy/fly):

| file | purpose |
|------|---------|
| `Dockerfile` | `docker:dind` + python; copies the repo in; runs `sandbox-up.sh` at boot |
| `entrypoint.sh` | PID 1: bring the range up, hold the Machine, optional self-destruct |
| `fly.toml` | one Machine, `lhr`, **no public ports**, `MAX_RUNTIME_MIN` knob |
| `up.sh` / `down.sh` | one command to deploy, one to destroy |

## Why Fly works here (kind doesn't, Docker does)

A Fly Machine is a Firecracker micro-VM — the **same substrate** as the Claude
cloud sandbox, where this range already runs. The range is a Docker stack, not
Kubernetes, so the Firecracker nested-kubelet limit that blocks `kind`
([docs/kubernetes.md](kubernetes.md)) does **not** apply. Running `dockerd`
inside the Machine (Docker-in-Docker) is the standard Fly pattern for this.

## Access model — no ingress, no VPN install

`fly.toml` declares **no `[[services]]`**, so the Machine has no public address.
You reach it two ways, both over Fly's built-in WireGuard:

- **`fly ssh console --app <app>`** — a shell on the Machine. Drive the range from
  here (this is the intended workflow; targets are on `127.0.0.1:90xx` inside the
  Machine, and the assessor's `http_request` tool is scoped to them).
- **`fly proxy 9010:9010 --app <app>`** — forward a challenge's web port to your
  laptop to poke it in a browser. Forward several at once:
  `fly proxy 9010:9010 9070:9070 9112:9112 --app <app>`.

Nothing inbound is ever opened, so there are no security-group / ingress rules to
edit, and there is no Tailscale (or similar) to install per box.

## Module ports

`range status` prints the live map. The range uses `127.0.0.1:9010–9112` for
module targets and `92xx` for the exfil/oracle sinks, e.g.:

```
01 guide 9010 · 02 saas 9020 · 03 assistant 9030 · 04 agents 9040 · 05 rag 9050
06 embeddings 9060 · 07 vuln-mcp 9070 / host 9071 · 08 registry 9080
09 appserver 9090 / metadata 9091 · 11 assistant 9110 / vault 9112
```

## Using your LLM harness against the deployed range

The range ships two OpenAI-compatible harnesses; `sandbox-up.sh` puts both on
PATH inside the Machine (details in [docs/llm-assessor.md](llm-assessor.md)):

- **`assess`** (`scripts/agent_solver.py`) — the autonomous range assessor: the
  model gets the objective, live target URLs, a lab-scoped `http_request` tool and
  `submit_flag`; the verifier scores each step.
- **`grok`** (`scripts/grok_cli.py`) — a general Grok chat/agent CLI.

From inside the Machine (`fly ssh console`):

```bash
# Grok (needs the XAI_API_KEY secret; up.sh sets it if it was in your env)
assess 07 --provider grok --model grok-4
grok "what MCP tool-poisoning vectors does module 07 expose?"

# OpenAI instead
OPENAI_API_KEY=sk-... assess 05 --provider openai --model gpt-4.1

# Any OpenAI-compatible endpoint (local model, gateway, your own harness)
assess 05 --provider custom --base-url http://host:8000/v1 --model m --api-key x
```

Bring your **own** harness by pointing it at the same contract: an
OpenAI-compatible chat endpoint plus the two tools, scored by `run_challenge`.
`scripts/agent_solver.py` (~150 lines) is the reference to fork.

To make the **targets** think with a real model instead of the deterministic mock,
set the backend (the mock is the default, which is what keeps challenges
reproducible):

```bash
REDSEC_LLM_BACKEND=openai REDSEC_LLM_BASE_URL=https://api.x.ai/v1 \
  REDSEC_LLM_MODEL=grok-4 REDSEC_LLM_API_KEY="$XAI_API_KEY" range reset
```

## Cost & lifecycle

A `shared-cpu-4x` / 8 GB Machine is cheap for hour-long use, and you only pay
while it exists. Three ways to make it ephemeral:

- `./deploy/fly/down.sh` when you're done (destroys app + Machine + volume);
- set `MAX_RUNTIME_MIN = "60"` in `fly.toml` so the Machine halts itself;
- `fly machine stop` / `start` to pause without rebuilding.

## How this was verified

On the identical Firecracker substrate (the Claude cloud sandbox), before this
was committed:

- `pip install -e .`, `redsec doctor` (11/11), `redsec selftest` (**43/43**
  fail→pass);
- `scripts/sandbox-up.sh` brought **19 containers** up across the module networks;
- `range solve` ran reference exploits that the verifier scored **PASS**,
  including side-effect oracle (exfil-sink) modules;
- the `assess` harness drove the live range end-to-end (tool loop + verifier).

The Docker-in-Docker image was separately confirmed to build, boot its inner
`dockerd`, and run a module stack on a private network with published ports. The
only step not exercisable without a Fly account is Fly's own Machine privilege for
the inner daemon; `docker:dind` on a Fly Machine is the standard way to run it.

## Troubleshooting

- **`429 Too Many Requests` during first boot** — Docker Hub anonymous pull limit
  while building the base image, not a bug. Re-run `range reset` / re-deploy; or
  `fly ssh console` and authenticate the inner daemon (`docker login`) to raise the
  limit.
- **Inner `dockerd` won't start** — the Machine needs the privilege to run DinD. If
  a Fly change ever blocks it, the fallback is one native Fly Machine per challenge
  (no DinD); open an issue and we'll add that variant.
- **`fly ssh console` can't connect** — the Machine may still be building images on
  first boot; wait a minute, or check `fly logs --app <app>`.
- **`XAI_API_KEY` not picked up** — set it as a secret:
  `fly secrets set XAI_API_KEY=... --app <app>` (then `range reset`).

See also: [docs/interactive-sandbox.md](interactive-sandbox.md),
[docs/llm-assessor.md](llm-assessor.md), [docs/kubernetes.md](kubernetes.md).
