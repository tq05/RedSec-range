#!/usr/bin/env bash
# Build a single container image that can run ANY module's targets, without
# pulling per-target images from a registry. Used by scripts/docker_run_all.py
# (the registry-free, Kubernetes-free way to run every challenge in containers).
#
# Run from the repo root. Requires Docker + a reachable PyPI (directly or via a
# proxy). Honors HTTPS_PROXY if set.
set -euo pipefail

IMAGE="${IMAGE:-redsec/base:local}"
CTX="$(mktemp -d)"
trap 'rm -rf "$CTX"' EXIT

# Stage the repo into the build context.
cp -a "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" "$CTX/redsec-range"

# Apply the repository's Docker exclusions to the nested build context as well.
# This keeps local virtualenvs, credentials, state, and generated challenge files
# out of the shared runner image.
awk 'NF && $1 !~ /^#/ { print "redsec-range/" $0 }' .dockerignore > "$CTX/.dockerignore"

cat > "$CTX/Dockerfile" <<'EOF'
FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
ARG PXY=
COPY redsec-range/deploy/constraints.txt /tmp/constraints.txt
RUN pip install --no-cache-dir ${PXY:+--proxy $PXY} -c /tmp/constraints.txt \
    --trusted-host pypi.org --trusted-host files.pythonhosted.org \
    fastapi "uvicorn[standard]" httpx pydantic pyyaml
COPY redsec-range /app
ENV PYTHONPATH=/app
WORKDIR /app
EOF

echo ">> building ${IMAGE}"
docker build --network=host --build-arg PXY="${HTTPS_PROXY:-}" -t "$IMAGE" "$CTX"
echo ">> done: ${IMAGE}"
