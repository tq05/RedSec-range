#!/usr/bin/env bash
# Build (and optionally push) all container images for the range.
# Run from the repo root. Requires Docker.
#
#   REGISTRY=ghcr.io/you TAG=dev ./scripts/build_images.sh
#   PUSH=1 REGISTRY=ghcr.io/you ./scripts/build_images.sh
#
# Image names follow the chart convention: m<ID>-<target>  (+ the shared 'drop').
set -euo pipefail

REGISTRY="${REGISTRY:-ghcr.io/redsec-range}"
TAG="${TAG:-latest}"
PUSH="${PUSH:-0}"

# On a normal machine no flags are needed. Behind an egress proxy (e.g. a
# corporate network or this project's dev sandbox), export HTTPS_PROXY and the
# build will route pip/network through it via BuildKit's host network.
PROXY="${HTTPS_PROXY:-}"
EXTRA=()
if [ -n "$PROXY" ]; then
  EXTRA=(--network=host
         --build-arg "http_proxy=$PROXY"  --build-arg "https_proxy=$PROXY"
         --build-arg "HTTP_PROXY=$PROXY"  --build-arg "HTTPS_PROXY=$PROXY")
fi

build() {  # <dockerfile> <image-name>
  echo ">> building ${REGISTRY}/$2:${TAG}"
  docker build "${EXTRA[@]}" -f "$1" -t "${REGISTRY}/$2:${TAG}" .
  [ "$PUSH" = "1" ] && docker push "${REGISTRY}/$2:${TAG}" || true
}

# shared sink (repo-root context, for the shared constraints file)
docker build "${EXTRA[@]}" -f redsec/services/drop/Dockerfile -t "${REGISTRY}/drop:${TAG}" .
[ "$PUSH" = "1" ] && docker push "${REGISTRY}/drop:${TAG}" || true

build modules/01-intro/targets/guide/Dockerfile                    m01-guide
build modules/02-recon/targets/saas/Dockerfile                     m02-saas
build modules/03-attacking-agents/targets/assistant/Dockerfile     m03-assistant
build modules/04-multi-agent-a2a/targets/agents/Dockerfile         m04-agents
build modules/05-rag-pipelines/targets/rag/Dockerfile              m05-rag
build modules/06-embeddings/targets/embeddings/Dockerfile          m06-embeddings
build modules/07-mcp-tool-surfaces/targets/vuln-mcp/Dockerfile     m07-vuln-mcp
build modules/07-mcp-tool-surfaces/targets/host/Dockerfile         m07-host
build modules/08-supply-chain/targets/registry/Dockerfile          m08-registry
build modules/09-infra-deployment/targets/appserver/Dockerfile     m09-appserver
build modules/09-infra-deployment/targets/metadata/Dockerfile      m09-metadata
build modules/11-capstone/targets/assistant/Dockerfile             m11-assistant
build modules/11-capstone/targets/vault/Dockerfile                 m11-vault
# (Module 10 is artifact-scored and has no container targets.)

echo "done. images tagged ${REGISTRY}/*:${TAG}"
