#!/usr/bin/env sh

set -eu

usage() {
  echo "Usage: ./sync-folder.sh /absolute/path/to/destination-project path/to/folder" >&2
}

fail() {
  echo "sync-folder: $1" >&2
  exit 1
}

if [ "$#" -ne 2 ]; then
  usage
  exit 2
fi

DESTINATION_PROJECT=$1
RELATIVE_FOLDER=$2

case "$DESTINATION_PROJECT" in
  /*) ;;
  *) fail "the destination project path must be absolute" ;;
esac

case "$RELATIVE_FOLDER" in
  "") fail "the folder path must not be empty" ;;
  /*) fail "the folder path must be relative" ;;
esac

OLD_IFS=$IFS
IFS='/\\'
for segment in $RELATIVE_FOLDER; do
  if [ "$segment" = ".." ]; then
    IFS=$OLD_IFS
    fail "the folder path must not contain '..' segments"
  fi
done
IFS=$OLD_IFS

SCRIPT_DIRECTORY=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE_PROJECT=$SCRIPT_DIRECTORY
NODE_SCRIPT="$SCRIPT_DIRECTORY/sync-folder.mjs"

command -v git >/dev/null 2>&1 || fail "git is not installed or is not available in PATH"
command -v node >/dev/null 2>&1 || fail "Node.js is not installed or is not available in PATH"

[ -f "$NODE_SCRIPT" ] || fail "Node.js script not found: $NODE_SCRIPT"
[ -d "$SOURCE_PROJECT/.git" ] || fail "the current project is not a Git repository: $SOURCE_PROJECT"

printf '%s\n' "Pulling the current project..."
if ! git -C "$SOURCE_PROJECT" pull; then
  fail "git pull failed; the destination was not modified"
fi

printf '%s\n' "Synchronizing $RELATIVE_FOLDER..."
node "$NODE_SCRIPT" "$SOURCE_PROJECT" "$DESTINATION_PROJECT" "$RELATIVE_FOLDER"
