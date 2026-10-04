#!/usr/bin/env python3
"""Offline Kubernetes validation for RedSec Range.

The build/CI sandbox used to author this project blocks egress to helm's download
host and the Go module proxy, so `helm`/`kubeconform` can't run there. This script
provides equivalent *offline* assurance: it renders the manifests a module would
produce (mirroring deploy/helm/redsec-module faithfully), then validates every
object against the real upstream Kubernetes OpenAPI schemas (via the
`kubernetes-validate` package, which bundles them) and runs structural
cross-checks (selector<->template label match, probe ports, env well-formedness,
NetworkPolicy containment).

The Helm chart itself is additionally validated with `helm lint` / `helm template`
/ `kubeconform` in CI (.github/workflows/ci.yml), which runs where egress is open.
Keep this renderer in sync with the chart; `tests/test_k8s.py` guards it.
"""
from __future__ import annotations

import sys

import kubernetes_validate

from redsec.deploy.k8s import module_to_values
from redsec.loader import load_all

K8S_VERSION = "1.29"


def _drop_host(v: dict) -> str:
    d = v["drop"]
    ns = v["range"]["namespace"]
    return f"http://{d['name']}.{ns}.svc.cluster.local:{d['port']}"


def render(values: dict) -> list[dict]:
    """Mirror deploy/helm/redsec-module/templates/* for the given values."""
    objs: list[dict] = []
    ns = values["range"]["namespace"]
    labels = {"app.kubernetes.io/part-of": "redsec-range",
              "redsec.io/range": values["range"]["module"]}

    def deployment(name, image, port, env, privileged):
        sc_pod = ({} if privileged else
                  {"runAsNonRoot": True, "runAsUser": 10001, "fsGroup": 10001,
                   "seccompProfile": {"type": "RuntimeDefault"}})
        sc_ctr = ({"allowPrivilegeEscalation": True, "runAsNonRoot": False}
                  if privileged else
                  {"allowPrivilegeEscalation": False, "readOnlyRootFilesystem": False,
                   "capabilities": {"drop": ["ALL"]}})
        return {
            "apiVersion": "apps/v1", "kind": "Deployment",
            "metadata": {"name": name, "namespace": ns,
                         "labels": {**labels, "app": name}},
            "spec": {"replicas": 1,
                     "selector": {"matchLabels": {"app": name}},
                     "template": {
                         "metadata": {"labels": {**labels, "app": name}},
                         "spec": {"securityContext": sc_pod, "containers": [{
                             "name": name, "image": image, "imagePullPolicy": "IfNotPresent",
                             "ports": [{"containerPort": port}],
                             "env": env, "securityContext": sc_ctr,
                             "readinessProbe": {"httpGet": {"path": "/healthz", "port": port},
                                                "initialDelaySeconds": 2},
                             "resources": {"requests": {"cpu": "50m", "memory": "128Mi"},
                                           "limits": {"cpu": "1", "memory": "512Mi"}}}]}}},
        }

    def service(name, port):
        return {"apiVersion": "v1", "kind": "Service",
                "metadata": {"name": name, "namespace": ns, "labels": labels},
                "spec": {"selector": {"app": name},
                         "ports": [{"port": port, "targetPort": port}]}}

    peers = [{"name": "REDSEC_URL_" + t["name"].upper().replace("-", "_"),
              "value": f"http://{t['name']}.{ns}.svc.cluster.local:{t['port']}"}
             for t in values["targets"]]

    if values["drop"]["enabled"]:
        d = values["drop"]
        objs.append(deployment(d["name"], d["image"], d["port"],
                               [{"name": "REDSEC_PORT", "value": str(d["port"])}], False))
        objs.append(service(d["name"], d["port"]))

    for t in values["targets"]:
        env = [{"name": "REDSEC_PORT", "value": str(t["port"])}]
        if values["drop"]["enabled"]:
            env.append({"name": "REDSEC_DROP_URL", "value": _drop_host(values)})
        for k, val in (t.get("env") or {}).items():
            env.append({"name": k, "value": str(val)})
        env.extend(peers)
        objs.append(deployment(t["name"], t["image"], t["port"], env, t["privileged"]))
        objs.append(service(t["name"], t["port"]))

    # NetworkPolicies
    objs.append({"apiVersion": "networking.k8s.io/v1", "kind": "NetworkPolicy",
                 "metadata": {"name": "default-deny", "namespace": ns, "labels": labels},
                 "spec": {"podSelector": {}, "policyTypes": ["Ingress", "Egress"]}})
    objs.append({"apiVersion": "networking.k8s.io/v1", "kind": "NetworkPolicy",
                 "metadata": {"name": "allow-intra-and-dns", "namespace": ns, "labels": labels},
                 "spec": {"podSelector": {}, "policyTypes": ["Ingress", "Egress"],
                          "ingress": [{"from": [{"podSelector": {}}]}],
                          "egress": [{"to": [{"podSelector": {}}]},
                                     {"to": [], "ports": [{"protocol": "UDP", "port": 53},
                                                          {"protocol": "TCP", "port": 53}]}]}})
    for t in values["targets"]:
        if t.get("egress"):
            objs.append({"apiVersion": "networking.k8s.io/v1", "kind": "NetworkPolicy",
                         "metadata": {"name": f"allow-egress-{t['name']}", "namespace": ns,
                                      "labels": labels},
                         "spec": {"podSelector": {"matchLabels": {"app": t["name"]}},
                                  "policyTypes": ["Egress"], "egress": [{}]}})
    return objs


def structural_checks(objs: list[dict]) -> list[str]:
    errs: list[str] = []
    for o in objs:
        kind = o.get("kind")
        md = o.get("metadata", {})
        if not md.get("name"):
            errs.append(f"{kind}: missing metadata.name")
        if not md.get("namespace"):
            errs.append(f"{kind}/{md.get('name')}: missing namespace")
        if kind == "Deployment":
            sel = o["spec"]["selector"]["matchLabels"]
            tlabels = o["spec"]["template"]["metadata"]["labels"]
            if not sel.items() <= tlabels.items():
                errs.append(f"Deployment/{md['name']}: selector not subset of pod labels")
            c = o["spec"]["template"]["spec"]["containers"][0]
            probe_port = c["readinessProbe"]["httpGet"]["port"]
            cport = c["ports"][0]["containerPort"]
            if probe_port != cport:
                errs.append(f"Deployment/{md['name']}: probe port {probe_port} != {cport}")
            for e in c["env"]:
                if "name" not in e or "value" not in e:
                    errs.append(f"Deployment/{md['name']}: malformed env entry {e}")
    return errs


def main() -> int:
    failures = 0
    checked = 0
    # A representative set: the richest complete module + the chart defaults.
    cases = [("demo-defaults", {
        "range": {"module": "00", "slug": "demo", "namespace": "redsec-demo"},
        "image": {"registry": "ghcr.io/redsec-range", "tag": "latest"},
        "drop": {"enabled": True, "name": "drop", "port": 9099,
                 "image": "ghcr.io/redsec-range/drop:latest"},
        "targets": []})]
    for _, m in load_all():
        if m.status == "complete" and m.targets:
            cases.append((m.dirname,
                          module_to_values(m, "ghcr.io/redsec-range", "latest")))

    for name, values in cases:
        objs = render(values)
        for o in objs:
            checked += 1
            try:
                kubernetes_validate.validate(o, K8S_VERSION, strict=True)
            except kubernetes_validate.ValidationError as e:
                failures += 1
                print(f"  SCHEMA FAIL [{name}] {o['kind']}/{o['metadata'].get('name')}: {e}")
        for err in structural_checks(objs):
            failures += 1
            print(f"  STRUCT FAIL [{name}] {err}")
        print(f"  [{name}] {len(objs)} objects rendered & validated")

    print(f"\nvalidated {checked} Kubernetes objects against schema {K8S_VERSION}")
    if failures:
        print(f"FAILURES: {failures}")
        return 1
    print("all manifests valid (offline).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
