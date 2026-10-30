#!/usr/bin/env bash
# Sync the pinned contract into the arm repo, or verify the local snapshot.
#
#   sync-contract.sh latest      # download the rolling contract-latest release
#   sync-contract.sh 1.0.0       # download contract-v1.0.0
#   sync-contract.sh --check     # verify capstone/contract/ against the local json
#
# Requires: curl, unzip, python3. Token: CONTRACT_READ_TOKEN (or GH_TOKEN).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"          # <arm-repo>/capstone
DEST="$ROOT/contract"
META="$ROOT/contract-release.json"
REPO="${CONTRACT_REPO:-poisnoir/Capstone}"
MODE="${1:-latest}"

verify_tree() {
  # $1 = extracted contract dir, $2 = release json, $3 = "check" or "sync"
  python3 - "$1" "$2" "$3" <<'PY'
import hashlib, json, sys
from pathlib import Path

src = Path(sys.argv[1])
meta = Path(sys.argv[2])
mode = sys.argv[3]
data = json.loads(meta.read_text())
files = data.get("files", {})
errors = []
if not files:
    errors.append("release json has no files")

seen = set()
for rel, expected in sorted(files.items()):
    p = src / rel
    if not p.is_file():
        errors.append(f"missing: {rel}")
        continue
    actual = hashlib.sha256(p.read_bytes()).hexdigest()
    if actual != expected:
        errors.append(f"hash mismatch: {rel}")
    seen.add(rel)

for p in sorted(src.rglob("*")):
    if p.is_file():
        rel = p.relative_to(src).as_posix()
        if rel not in seen:
            errors.append(f"unexpected: {rel}")

if errors:
    print(f"contract verification failed ({mode}):", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)

print(f"contract {data.get('version')} verified: {len(files)} files")
PY
}

if [[ "$MODE" == "--check" ]]; then
  if [[ ! -d "$DEST" || ! -f "$META" ]]; then
    echo "error: $DEST or $META missing; run a sync first" >&2
    exit 1
  fi
  verify_tree "$DEST" "$META" check
  exit 0
fi

TOKEN="${CONTRACT_READ_TOKEN:-${GH_TOKEN:-}}"
if [[ -z "$TOKEN" ]]; then
  echo "error: CONTRACT_READ_TOKEN (or GH_TOKEN) is not set" >&2
  echo "Create a fine-grained PAT with Contents: Read on $REPO." >&2
  exit 1
fi

if [[ "$MODE" == "latest" ]]; then
  TAG="contract-latest"
  ZIP="contract-latest.zip"
  JSON="contract-latest.json"
else
  TAG="contract-v$MODE"
  ZIP="$TAG.zip"
  JSON="$TAG.json"
fi
BASE="https://github.com/$REPO/releases/download/$TAG"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
echo "downloading $TAG"
curl -fsSL -H "Authorization: Bearer $TOKEN" -o "$TMP/$ZIP" "$BASE/$ZIP"
curl -fsSL -H "Authorization: Bearer $TOKEN" -o "$TMP/$JSON" "$BASE/$JSON"

mkdir -p "$TMP/extract"
unzip -q "$TMP/$ZIP" -d "$TMP/extract"
verify_tree "$TMP/extract" "$TMP/$JSON" sync

rm -rf "$DEST"
mkdir -p "$DEST"
cp -a "$TMP/extract/." "$DEST/"
cp "$TMP/$JSON" "$META"

python3 - "$META" "$ROOT/CONTRACT_VERSION" <<'PY'
import json, sys
from datetime import datetime, timezone
from pathlib import Path
data = json.loads(Path(sys.argv[1]).read_text())
Path(sys.argv[2]).write_text(
    f"version: {data.get('version')}\n"
    f"tag: {data.get('tag')}\n"
    f"commit: {data.get('commit')}\n"
    f"synced: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n"
)
PY

echo "synced contract $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$META")"
