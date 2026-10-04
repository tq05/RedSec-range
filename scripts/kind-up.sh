#!/usr/bin/env bash
# Turnkey kind bring-up for the whole range (one cluster, all modules).
#
#   ./scripts/kind-up.sh                 # create cluster, build+load images, deploy all modules
#   MODULES="03 07" ./scripts/kind-up.sh # only these modules
#   CLUSTER=redsec KIND_IMAGE=kindest/node:v1.34.0 ./scripts/kind-up.sh
#
# Requires: docker, kind, kubectl, helm. On a normal machine this "just works".
# A policy-enforcing CNI (Calico/Cilium) is optional; without it the range runs
# but the default-deny NetworkPolicies are advisory (see docs/kubernetes.md).
set -euo pipefail

CLUSTER="${CLUSTER:-redsec}"
REGISTRY="${REGISTRY:-ghcr.io/redsec-range}"
TAG="${TAG:-latest}"
MODULES="${MODULES:-01 02 03 04 05 06 07 08 09 11}"   # 10 is artifact-only, no pods
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "== 1/4 create kind cluster '${CLUSTER}' =="
if ! kind get clusters 2>/dev/null | grep -qx "$CLUSTER"; then
  kind create cluster --name "$CLUSTER" ${KIND_IMAGE:+--image "$KIND_IMAGE"}
fi
kubectl cluster-info --context "kind-${CLUSTER}" >/dev/null

echo "== 2/4 build images =="
REGISTRY="$REGISTRY" TAG="$TAG" "$ROOT/scripts/build_images.sh"

echo "== 3/4 load images into the kind node (no registry push needed) =="
imgs=$(docker images "${REGISTRY}/*:${TAG}" --format '{{.Repository}}:{{.Tag}}')
for img in $imgs; do
  echo "   loading $img"
  kind load docker-image "$img" --name "$CLUSTER"
done

echo "== 4/4 deploy modules: ${MODULES} =="
for m in $MODULES; do
  echo "   -> module $m"
  redsec deploy "$m" --registry "$REGISTRY" --tag "$TAG"
done

echo
echo "done. Inspect with:  kubectl get pods -A | grep redsec"
echo "Run challenges on-cluster with:  ./scripts/kind-run-all.sh"
echo "Tear down with:  kind delete cluster --name ${CLUSTER}"
