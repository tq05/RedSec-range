# RedSec Range on a single Fly.io Machine (Docker-in-Docker).
#
# A Fly Machine is a Firecracker micro-VM. We run an inner dockerd inside it and
# bring the whole range up with the repo's own scripts/sandbox-up.sh — the same
# bootstrap used in the Claude cloud sandbox, which is also a Firecracker microVM.
# The range is a Docker Compose-style stack (not kind/k8s), so the Firecracker
# nested-kubelet limit documented in docs/kubernetes.md does NOT apply here.
#
# Build context is the REPO ROOT (so the whole range is copied in). deploy/fly/up.sh
# runs the deploy from the repo root with the right --config/--dockerfile flags.

FROM docker:27-dind

# Tooling the bootstrap + controller need. docker:dind is Alpine-based and already
# provides a correctly-plumbed inner dockerd; we add python for the `redsec`
# controller and the range/grok/assess CLIs. Module *target* images are built at
# runtime by scripts/build_base_image.sh (FROM python:3.12-slim) on the inner daemon.
RUN apk add --no-cache \
      bash \
      python3 \
      py3-pip \
      git \
      curl \
      tar \
      coreutils \
      procps

WORKDIR /opt/redsec-range
COPY . /opt/redsec-range

RUN python3 -m pip install --break-system-packages --no-cache-dir . \
    && chmod +x deploy/fly/*.sh scripts/*.sh

ENTRYPOINT ["/opt/redsec-range/deploy/fly/entrypoint.sh"]
