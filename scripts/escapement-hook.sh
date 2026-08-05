#!/usr/bin/env sh
set -eu

EVENT="${1:?hook event required}"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "$ROOT" ]; then
  ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
fi

PYTHON="${ESCAPEMENT_PYTHON:-}"
if [ -z "$PYTHON" ]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
  elif command -v python >/dev/null 2>&1; then
    PYTHON="python"
  else
    echo "Escapement requires Python 3.10+." >&2
    exit 127
  fi
fi

exec "$PYTHON" "$ROOT/scripts/agent_runtime.py" "$EVENT"
