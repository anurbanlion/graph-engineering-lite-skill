#!/usr/bin/env sh

# Stop immediately on errors and reject unset variables.
set -eu

# Print the public wrapper usage expected by callers.
usage() {
  echo "Usage: ./sync-folder.sh /absolute/path/to/destination-project path/to/folder" >&2
}

# Report a clear error message and terminate with a non-zero exit code.
fail() {
  echo "sync-folder: $1" >&2
  exit 1
}

# Step 1: validate the number of arguments before doing any work.
if [ "$#" -ne 2 ]; then
  usage
  exit 2
fi

DESTINATION_PROJECT=$1
RELATIVE_FOLDER=$2

# Step 2: require an absolute destination-project path.
case "$DESTINATION_PROJECT" in
  /*) ;;
  *) fail "the destination project path must be absolute" ;;
esac

# Step 3: require a non-empty relative folder path.
case "$RELATIVE_FOLDER" in
  "") fail "the folder path must not be empty" ;;
  /*) fail "the folder path must be relative" ;;
esac

# Step 4: reject traversal segments so the folder cannot escape either project.
OLD_IFS=$IFS
IFS='/\\'
for segment in $RELATIVE_FOLDER; do
  if [ "$segment" = ".." ]; then
    IFS=$OLD_IFS
    fail "the folder path must not contain '..' segments"
  fi
done
IFS=$OLD_IFS

# Step 5: resolve the current repository from the wrapper location and locate
# the Node.js implementation next to it.
SCRIPT_DIRECTORY=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE_PROJECT=$SCRIPT_DIRECTORY
NODE_SCRIPT="$SCRIPT_DIRECTORY/sync-folder.mjs"

# Step 6: verify the required executables and local files before pulling.
command -v git >/dev/null 2>&1 || fail "git is not installed or is not available in PATH"
command -v node >/dev/null 2>&1 || fail "Node.js is not installed or is not available in PATH"

[ -f "$NODE_SCRIPT" ] || fail "Node.js script not found: $NODE_SCRIPT"
[ -d "$SOURCE_PROJECT/.git" ] || fail "the current project is not a Git repository: $SOURCE_PROJECT"

# Step 7: update the current project. The destination is not touched unless
# this command finishes successfully.
printf '%s\n' "Pulling the current project..."
if ! git -C "$SOURCE_PROJECT" pull; then
  fail "git pull failed; the destination was not modified"
fi

# Step 8: delegate validation, replacement, directory creation, and copying to
# the Node.js script only after git pull succeeds.
printf '%s\n' "Synchronizing $RELATIVE_FOLDER..."
node "$NODE_SCRIPT" "$SOURCE_PROJECT" "$DESTINATION_PROJECT" "$RELATIVE_FOLDER"
