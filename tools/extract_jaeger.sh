#!/usr/bin/env bash
# Regenerate the Jaeger thesis extracts from the full thesis.
# The full thesis and the PDF crop are local-only and gitignored.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
THESIS="${THESIS:-$ROOT/HAJ_Thesis_2018.pdf}"
OUT="$ROOT/docs/extracts"

if [[ ! -f "$THESIS" ]]; then
  echo "error: thesis not found: $THESIS" >&2
  echo "Set THESIS=/path/to/HAJ_Thesis_2018.pdf and retry." >&2
  echo "See docs/reference/MANIFEST.md REF-01 for how to obtain it." >&2
  exit 1
fi

for cmd in gs pdfunite pdftotext; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "error: missing command: $cmd" >&2
    exit 1
  fi
done

mkdir -p "$OUT"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# 27-page crop: PDF pp.84–94 (Ch.3) + 199–214 (Ch.7)
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite \
  -dFirstPage=84 -dLastPage=94 \
  -sOutputFile="$TMP/ch3.pdf" "$THESIS"
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite \
  -dFirstPage=199 -dLastPage=214 \
  -sOutputFile="$TMP/ch7.pdf" "$THESIS"
pdfunite "$TMP/ch3.pdf" "$TMP/ch7.pdf" \
  "$OUT/Jaeger2018_filament-sensor-model_extract.pdf"

# Text extracts used by agents
pdftotext -layout -f 84 -l 94 "$THESIS" \
  "$OUT/Jaeger2018_filament-sensor-model_Ch3_extract.txt"
pdftotext -layout -f 199 -l 214 "$THESIS" \
  "$OUT/Jaeger2018_bespoke-sensor_Ch7_extract.txt"

echo "regenerated:"
ls -lh "$OUT"/*.pdf "$OUT"/*.txt
