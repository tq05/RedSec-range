#!/usr/bin/env bash
# Throw it all away. Destroys the app + its Machine — nothing lingers, nothing bills.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
APP="${FLY_APP:-$(grep -E '^app ' "$HERE/fly.toml" | sed -E 's/app *= *"(.*)"/\1/')}"
echo ">> destroying app $APP"
fly apps destroy "$APP" -y
echo ">> gone."
