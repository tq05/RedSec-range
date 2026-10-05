#!/usr/bin/env bash
# One-time dependency setup for GitHub Codespaces and compatible dev containers.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "== RedSec Codespaces: install Python environment =="
python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -q -e .
.venv/bin/redsec doctor

mkdir -p .redsec
echo "Dependencies ready. The post-start hook will now start the Docker range."
