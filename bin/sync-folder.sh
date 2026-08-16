#!/usr/bin/env sh

# Stop immediately on errors and reject unset variables.
set -eu

# Resolve the Node.js implementation from this file's location.
SCRIPT_DIRECTORY=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPOSITORY_DIRECTORY=$(CDPATH= cd -- "$SCRIPT_DIRECTORY/.." && pwd)
NODE_SCRIPT="$SCRIPT_DIRECTORY/sync-folder.mjs"
NODE_BINARY="$REPOSITORY_DIRECTORY/desktop-wsl-apply-patch/scripts/node"

exec "$NODE_BINARY" "$NODE_SCRIPT" "$@"
