#!/usr/bin/env bash
# Start or restore the range whenever a Codespace starts.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p .redsec
rm -f .redsec/codespaces-ready

modules=()
if [ -n "${REDSEC_MODULES:-}" ]; then
  [[ "$REDSEC_MODULES" =~ ^[0-9][0-9]([[:space:]]+[0-9][0-9])*$ ]] || {
    echo "REDSEC_MODULES must contain space-separated two-digit module IDs" >&2
    exit 2
  }
  read -r -a modules <<<"$REDSEC_MODULES"
fi

ranges=()
if [ -n "${REDSEC_RANGES:-}" ]; then
  [[ "$REDSEC_RANGES" =~ ^[a-z0-9][a-z0-9-]*([[:space:]]+[a-z0-9][a-z0-9-]*)*$ ]] || {
    echo "REDSEC_RANGES must contain space-separated range IDs" >&2
    exit 2
  }
  read -r -a ranges <<<"$REDSEC_RANGES"
  .venv/bin/redsec ranges enable "${ranges[@]}"
fi

echo "== RedSec Codespaces: start enabled ranges${REDSEC_RANGES:+ ($REDSEC_RANGES)} =="
.venv/bin/redsec ranges up
.venv/bin/redsec ranges status
touch .redsec/codespaces-ready

cat <<'EOF'

RedSec Range is ready.
  range status                 # live targets and ports
  redsec lesson 01             # course material
  range solve 01               # reference exploit + verifier
  redsec ranges list           # built-in, external, and placeholder ranges
  redsec ranges enable --all   # opt in to every available range
  redsec ranges up             # start the enabled profile
  assess 07 --provider openai --model <model>

Challenge ports are private to your GitHub account. Open the PORTS tab to browse.
EOF
