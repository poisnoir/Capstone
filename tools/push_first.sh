#!/usr/bin/env bash
# First-push guard: refuse to push if a private file or student ID is tracked,
# or if a tracked file is over 20 MB.
set -euo pipefail

BRANCH="${BRANCH:-main}"

python3 tools/check_publish.py --public || {
  echo "Refusing to push: private details are still tracked." >&2
  exit 1
}

big="$(git ls-files -z | xargs -0 du -k | awk '$1 > 20480 {print $0}')"
if [[ -n "$big" ]]; then
  echo "Refusing to push: tracked files over 20 MB:" >&2
  echo "$big" >&2
  exit 1
fi

git push -u origin "$BRANCH"
