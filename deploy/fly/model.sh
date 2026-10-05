#!/usr/bin/env bash
# Run the bundled autonomous model assessor inside the private Fly Machine.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
[ "$#" -gt 0 ] || {
  echo "usage: deploy/fly/model.sh MODULE [CHALLENGE] [assess options]" >&2
  echo "example: deploy/fly/model.sh 07 --provider openai --model gpt-5" >&2
  exit 2
}
exec "$HERE/exec.sh" assess "$@"
