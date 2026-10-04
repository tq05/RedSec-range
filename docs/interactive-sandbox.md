# Interactive sandbox — solve the challenges live, without Kubernetes

This is the way to run and solve the whole range **interactively inside a
Docker-capable sandbox** (including this project's own cloud sandbox), when a real
Kubernetes cluster isn't available.

## Why not kind/k3s here?

kind and k3s both start a Kubernetes control plane fine, but on some hosts the
**kubelet can't launch pods**: `runc create … can't get final child's PID from pipe:
EOF`. This happens on locked-down VMs / Firecracker microVMs (cgroup-v1 + a kernel
whose nested-container setup the sandbox restricts). Plain Docker containers — and
even `containerd`'s own `ctr run` — work on the same host; only the kubelet
pod-sandbox path fails. It is an environment limit, not a project bug, and a normal
laptop/server/CI runs kind fine (see [kubernetes.md](kubernetes.md)).

So here we run each module's targets as **long-lived Docker containers** on a
per-module network, with container-name DNS standing in for Kubernetes Service
names — the same wiring, one layer down.

## One-time (or after a sandbox reset)

```bash
./scripts/sandbox-up.sh        # ensures dockerd + base image + brings the range up
```

Idempotent: if the sandbox went idle and was reclaimed, just run it again to
restore everything from cold.

## The `range` controller

```bash
range status                 # what's running, with URLs
range up 07                  # start one module (or: range up-all)
range solve 07               # run the reference exploit live, then verify (resets state first)
range solve 07 rug-pull      # just one challenge
range verify 07              # re-run verifiers only (no exploit)
range shell 07 vuln-mcp      # interactive shell INSIDE a target container
range logs 07 host           # tail a target's logs
range reset 07               # reset a module's sink + planted state
range down 07                # stop one module (or: range down-all)
```

Each target is published on `127.0.0.1:<port>` (see `range status`), so you can
also just `curl` them directly and submit flags with the normal CLI:

```bash
# recover a flag by hand, then submit it
curl -s http://127.0.0.1:9070/ -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"resources/read","params":{"uri":"file://../secret/resource.flag"}}'
redsec submit 07 resource-traversal 'REDSEC{...}'

# oracle challenges: exploit, then verify against the live sink
redsec verify 07 tool-poisoning
```

Follow any module's walkthrough with `redsec lesson <id>` — every curl in it works
against the running containers (use the port from `range status`).

## Production images instead of the base image

By default every target runs from one small `redsec/base:local` image (fast, no
registry). To run the **actual per-module production images** (the ones a real
Kubernetes deploy would use):

```bash
REGISTRY=ghcr.io/redsec-range ./scripts/build_images.sh   # build all 14 images
range down-all
range up-all --real                                        # use m<ID>-<target> images
```

## How interactive it is

- The containers **persist across turns/messages** as long as the sandbox is alive
  (they use `--restart unless-stopped`).
- You drive it like a terminal: ask for any `range …`, `curl …`, or `redsec …`
  command and read the output; iterate on payloads; watch the sink.
- `range shell <mod> <target>` drops you *inside* a target container to inspect the
  vulnerable app from the inside.

## Relationship to the other run paths

| Path | Where | Command |
|------|-------|---------|
| Local processes | anywhere with Python | `redsec dev/up <id>` |
| **Persistent Docker range (this doc)** | any Docker sandbox | `./scripts/sandbox-up.sh` + `range …` |
| Ephemeral container check | any Docker host | `python scripts/docker_run_all.py [--real]` |
| Kubernetes | real cluster / kind on a normal host | `./scripts/kind-up.sh` |

All four use the identical modules, verifiers, and reference exploits, so a
challenge solved in one is solved in all.
