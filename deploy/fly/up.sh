#!/usr/bin/env bash
# Deploy the RedSec Range to a Fly.io Machine. Run from anywhere in the repo.
# Build context is the repo root so the whole range is included in the image.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
cd "$ROOT"

APP="${FLY_APP:-$(grep -E '^app ' "$HERE/fly.toml" | sed -E 's/app *= *"(.*)"/\1/')}"

command -v fly >/dev/null || { echo "Install flyctl first: https://fly.io/docs/flyctl/install/" >&2; exit 1; }

# Create the app once (idempotent).
if ! fly apps list 2>/dev/null | awk '{print $1}' | grep -qx "$APP"; then
  echo ">> creating app $APP"
  fly apps create "$APP"
fi

# Optional: give the targets a real LLM (otherwise the deterministic mock is used).
# Set XAI_API_KEY in your shell before running to push it as a Fly secret, so the
# `assess`/`grok` harness and REDSEC_LLM_BACKEND=openai can use Grok from the Machine.
if [ -n "${XAI_API_KEY:-}" ]; then
  echo ">> setting XAI_API_KEY secret"
  fly secrets set XAI_API_KEY="$XAI_API_KEY" --app "$APP" >/dev/null
fi

echo ">> deploying (remote build; first boot builds images, give it a few minutes)"
fly deploy --app "$APP" \
  --config "$HERE/fly.toml" \
  --dockerfile "$HERE/Dockerfile" \
  --ha=false --remote-only

cat <<EOF

====================================================================
 RedSec Range deploying to app: $APP

 Shell in (your command centre):
     fly ssh console --app $APP
   then:  range status
          range solve <mod> [chal]      # run a reference exploit, verifier-scored
          assess <mod> --provider grok --model grok-4   # your harness vs the range

 Open a challenge in your browser (forward a module port):
     fly proxy 9010:9010 --app $APP     # then http://localhost:9010

 Throw it all away:
     $HERE/down.sh        (or: fly apps destroy $APP -y)
====================================================================
EOF
