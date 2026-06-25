#!/usr/bin/env bash
set -euo pipefail

# Generate the polarization figures from the moment formula:
# Var(X) = E[X^2] - [E(X)]^2.
# Requires Python + matplotlib and the local generator script.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$ROOT_DIR/scripts/render_polarization_variance.py"
DST_DIR="$ROOT_DIR/polarization"

export MPLCONFIGDIR="${MPLCONFIGDIR:-/private/tmp/spence-signal-mpl-cache}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/private/tmp/spence-signal-xdg-cache}"
mkdir -p "$MPLCONFIGDIR" "$XDG_CACHE_HOME"
mkdir -p "$DST_DIR"

python3 "$SCRIPT" --output-dir "$DST_DIR"

echo "generated figures in $DST_DIR"
