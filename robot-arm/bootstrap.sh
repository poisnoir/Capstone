#!/usr/bin/env bash
# Clone the arm repo into robot-arm/vendor/arm (gitignored) for integration.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ARM_REPO_URL="${ARM_REPO_URL:-}"
DEST="$ROOT/robot-arm/vendor/arm"

if [[ -z "$ARM_REPO_URL" ]]; then
  echo "error: set ARM_REPO_URL to the arm repo (SSH or HTTPS URL)." >&2
  echo "Example: ARM_REPO_URL=git@github.com:poisnoir/Capstone-arm.git ./robot-arm/bootstrap.sh" >&2
  exit 1
fi

mkdir -p "$ROOT/robot-arm/vendor"
if [[ -d "$DEST/.git" ]]; then
  echo "updating $DEST"
  git -C "$DEST" pull --ff-only
else
  echo "cloning $ARM_REPO_URL -> $DEST"
  git clone "$ARM_REPO_URL" "$DEST"
fi

echo "done. The arm repo is gitignored; do not commit it."
