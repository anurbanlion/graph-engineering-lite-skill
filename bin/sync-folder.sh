#!/usr/bin/env sh

# Stop immediately on errors and reject unset variables.
set -eu

# Resolve the Node.js implementation from this file's location.
SCRIPT_DIRECTORY=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
NODE_SCRIPT="$SCRIPT_DIRECTORY/sync-folder.mjs"

exec node "$NODE_SCRIPT" "$@"
