# Running on Kubernetes

You have three ways to run the range, in increasing order of realism:

| Path | Needs | What it proves |
|------|-------|----------------|
| `redsec dev` / `redsec up` | Python only | fastest; targets as local processes |
| `scripts/docker_run_all.py` | Docker | every built-in container challenge in **real containers** with service-name DNS |
| **kind** (this doc) | Docker + kind + kubectl + helm | the full Kubernetes deploy, isolation policies and all |

All three use the same modules, verifiers and reference exploits.

## Quickstart with kind (one command)

```bash
./scripts/kind-up.sh          # create cluster, build images, load them, deploy every module
./scripts/kind-run-all.sh     # port-forward + exploit + verify each module on the cluster
kind delete cluster --name redsec
```

`kind-up.sh` creates a cluster, builds all images, `kind load`s them into the node
(so **no registry push is needed**), and `redsec deploy`s every module. Set
`MODULES="03 07"` to limit it. `kind-run-all.sh` runs the same fail→pass
verification used everywhere else, but against the live cluster.

> **Heads-up on nested environments.** kind runs Kubernetes inside a Docker
> container, which itself needs to start pod sandboxes (nested containers). Some
> locked-down/CI/VM hosts (cgroup v1, or a very new kernel with an old runc) can't
> do that — `kubeadm init` fails with `runc create … can't get final child's PID
> from pipe: EOF`. If you hit that, use `scripts/docker_run_all.py` (single-level
> Docker, no nesting) — it runs **all 40 container-backed challenges** and is the
> fallback this project's own dev sandbox uses. A normal laptop/server runs kind
> fine.

## Prerequisites (manual path)

- A cluster (kind, minikube, k3d, or real). For the NetworkPolicies to be
  *enforced* you need a **policy-enforcing CNI** (Calico, Cilium, …); kind's default
  CNI does not enforce them, so there containment is advisory.
- `kubectl`, `helm` (v3). A registry is **optional** with kind (`kind load`); needed
  for a remote cluster.

## Build & (optionally) push images

```bash
# normal machine:
REGISTRY=ghcr.io/you TAG=latest ./scripts/build_images.sh          # local build
REGISTRY=ghcr.io/you TAG=latest PUSH=1 ./scripts/build_images.sh   # build + push
```

Builds all 14 images: `drop` plus `m<ID>-<target>` for every module with pods
(module 10 is artifact-only, no image). Behind an egress proxy, export
`HTTPS_PROXY` and the script routes the build through it automatically.

## Deploy (manual, per module)

```bash
redsec render 07 --registry ghcr.io/you          # inspect manifests first
redsec deploy 07 --registry ghcr.io/you          # helm upgrade --install --wait
# multiple isolated copies (e.g. per student):
redsec deploy 07 --registry ghcr.io/you --instance alice   # -> namespace redsec-07-alice
```

`redsec deploy` derives Helm values from the module's `module.yaml` and runs
`helm upgrade --install` into `redsec-<id>[-<instance>]`.

## Reach a target

Vulnerable targets are **ClusterIP only** — never exposed by default. Use
port-forward (works through the API server, unaffected by NetworkPolicy):

```bash
kubectl -n redsec-07 port-forward svc/vuln-mcp 9070:9070 &
kubectl -n redsec-07 port-forward svc/host 9071:9071 &
```

Then exploit/verify against `localhost`, or let `scripts/kind-run-all.sh` do the
port-forward + `solution/solve.py` + verify loop for you.

## Containment (the safety control)

The chart applies, in every range namespace:

- `default-deny` — denies all ingress and egress.
- `allow-intra-and-dns` — re-allows pod↔pod traffic *within the namespace* and DNS
  only. Targets can reach each other and the `drop` sink; they **cannot** reach the
  internet or other namespaces.
- `allow-egress-<target>` — added only for targets that set `network.egress: true`.

Combined with non-root pods (including `privileged` targets), resource
limits, and canary-only secrets, this keeps deliberately vulnerable apps contained.

> If you expose a target via an Ingress/LoadBalancer, you take on the risk — allow
> ingress from the ingress-controller namespace explicitly and never put a range on
> a public address.

## Teardown

```bash
redsec destroy 07                 # helm uninstall
kubectl delete namespace redsec-07
```

## Validation

- `helm lint deploy/helm/redsec-module` and `redsec render <id>` (helm template)
  render every module; all 62 rendered objects pass `kubeconform -strict`.
- `python scripts/validate_manifests.py` validates the rendered objects against the
  upstream Kubernetes schemas offline (no helm needed).
- `python scripts/docker_run_all.py --real` runs all 40 container-backed challenges
  through the **actual production images** (what kind loads) end-to-end.
- CI runs the lint + kubeconform + the container run on every push.
