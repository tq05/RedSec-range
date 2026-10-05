#!/usr/bin/env bash
# Connect an authenticated local/hosted harness to this repository's Codespace.
# With arguments, run one remote command. Without arguments, open an SSH shell.
set -euo pipefail

command -v gh >/dev/null 2>&1 || {
  echo "GitHub CLI (gh) is required" >&2
  exit 1
}

REPOSITORY="${REDSEC_REPOSITORY:-tq05/RedSec-range}"
CODESPACE="${REDSEC_CODESPACE:-}"

if [ -z "$CODESPACE" ]; then
  CODESPACE="$(gh codespace list -R "$REPOSITORY" \
    --json name,lastUsedAt \
    --jq 'sort_by(.lastUsedAt) | reverse | .[0].name // empty')"
fi

if [ -z "$CODESPACE" ]; then
  echo "No Codespace found for $REPOSITORY." >&2
  echo "Create one at https://codespaces.new/$REPOSITORY?quickstart=1" >&2
  exit 1
fi

if [ "$#" -eq 0 ]; then
  exec gh codespace ssh -c "$CODESPACE"
fi

exec gh codespace ssh -c "$CODESPACE" -- "$@"
