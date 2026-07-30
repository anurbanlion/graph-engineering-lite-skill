#!/usr/bin/env sh

# Stop immediately on errors and reject unset variables.
set -eu

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
# Change only these two values when the folders to synchronize change.
# SOURCE_PATH may be relative to this repository or absolute.
# DESTINATION_PATH must be the complete destination folder path.
SOURCE_PATH="graph-engineering"
DESTINATION_PATH="/absolute/path/to/destination-project/graph-engineering"

# Report a clear error and terminate with a non-zero exit code.
fail() {
  printf '%s\n' "sync: $1" >&2
  exit 1
}

# This wrapper is configured in the file and does not accept CLI arguments.
if [ "$#" -ne 0 ]; then
  fail "this script does not accept arguments; edit SOURCE_PATH and DESTINATION_PATH at the top of sync.sh"
fi

# Resolve the repository and the Node.js implementation from this file's location.
SCRIPT_DIRECTORY=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
NODE_SCRIPT="$SCRIPT_DIRECTORY/sync.mjs"

# Resolve a relative source path from the current repository.
case "$SOURCE_PATH" in
  /*) RESOLVED_SOURCE_PATH=$SOURCE_PATH ;;
  *) RESOLVED_SOURCE_PATH="$SCRIPT_DIRECTORY/$SOURCE_PATH" ;;
esac

# Require an absolute destination path so the target is always explicit.
case "$DESTINATION_PATH" in
  /*) RESOLVED_DESTINATION_PATH=$DESTINATION_PATH ;;
  *) fail "DESTINATION_PATH must be absolute: $DESTINATION_PATH" ;;
esac

# Validate tools and local files before updating or copying anything.
command -v git >/dev/null 2>&1 || fail "git is not installed or is not available in PATH"
command -v node >/dev/null 2>&1 || fail "Node.js is not installed or is not available in PATH"
[ -f "$NODE_SCRIPT" ] || fail "Node.js script not found: $NODE_SCRIPT"
[ -d "$SCRIPT_DIRECTORY/.git" ] || fail "the current directory is not a Git repository: $SCRIPT_DIRECTORY"

# Update the current repository. Synchronization only runs when git pull succeeds.
printf '%s\n' "Pulling the current repository..."
if ! git -C "$SCRIPT_DIRECTORY" pull; then
  fail "git pull failed; the destination was not modified"
fi

# Synchronize the configured source folder into the configured destination folder.
printf '%s\n' "Synchronizing folder..."
node "$NODE_SCRIPT" "$RESOLVED_SOURCE_PATH" "$RESOLVED_DESTINATION_PATH"
