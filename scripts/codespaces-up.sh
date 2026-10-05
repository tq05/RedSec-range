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

echo "== RedSec Codespaces: start range${REDSEC_MODULES:+ ($REDSEC_MODULES)} =="
bash scripts/sandbox-up.sh "${modules[@]}"
touch .redsec/codespaces-ready

cat <<'EOF'

RedSec Range is ready.
  range status                 # live targets and ports
  redsec lesson 01             # course material
  range solve 01               # reference exploit + verifier
  assess 07 --provider openai --model <model>

Challenge ports are private to your GitHub account. Open the PORTS tab to browse.
EOF
