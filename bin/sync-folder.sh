#!/usr/bin/env sh

# Stop immediately on errors and reject unset variables.
set -eu

# Resolve the Python implementation from this file's location.
SCRIPT_DIRECTORY=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_SCRIPT="$SCRIPT_DIRECTORY/sync_folder.py"

exec python3 "$PYTHON_SCRIPT" "$@"
