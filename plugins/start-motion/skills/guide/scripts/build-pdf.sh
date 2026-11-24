#!/usr/bin/env bash
# Prints the guide's index.html to a Letter PDF with headless Chrome, using the page's own print styles.
#   bash build-pdf.sh <folder holding index.html> "<Output name>.pdf"
# The web page and the PDF come from the same file, so they always match. Rebuild the PDF whenever the page changes.
# Fonts: the page loads its fonts from Google Fonts. Where that is blocked (Claude's cloud workspace), install the
# font files locally first (npm i @fontsource/sora @fontsource/ibm-plex-sans, or copy the .ttf files into ~/.fonts and run fc-cache).
set -euo pipefail
DIR="$(cd "${1:?folder holding index.html}" && pwd)"; OUT="${2:-Guide.pdf}"
CHROME=""
for c in google-chrome chromium chromium-browser "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; do
  if command -v "$c" >/dev/null 2>&1 || [ -x "$c" ]; then CHROME="$c"; break; fi
done
[ -n "$CHROME" ] || { echo "Chrome not found"; exit 1; }
"$CHROME" --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer --virtual-time-budget=8000 \
  --print-to-pdf="$DIR/$OUT" "file://$DIR/index.html" >/dev/null 2>&1
ls -la "$DIR/$OUT"
