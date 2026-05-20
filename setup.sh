#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# setup.sh — Prepare a new Claude session for building
# Run once at the start of any session that will build PDFs.
# ─────────────────────────────────────────────────────────────────────────────

set -e
REPO="$(cd "$(dirname "$0")" && pwd)"

echo "InvestPuppy build setup — $(date '+%Y-%m-%d %H:%M')"
echo ""

# ── Python dependencies ───────────────────────────────────────────────────────
echo "Installing Python dependencies..."
pip install reportlab pillow numpy pypdf --break-system-packages -q
echo "  ✓ reportlab pillow numpy pypdf"

# ── Install Poppins fonts to system path (for Unvarnished builder) ─────────────
echo "Installing Poppins fonts..."
FONT_SRC="$REPO/_shared/fonts"
FONT_DEST="/usr/share/fonts/truetype/google-fonts"
mkdir -p "$FONT_DEST"
cp "$FONT_SRC"/Poppins-*.ttf "$FONT_DEST/"
fc-cache -f -q 2>/dev/null || true
echo "  ✓ Poppins installed to $FONT_DEST"

# ── Create output directories ─────────────────────────────────────────────────
echo "Creating output directories..."
mkdir -p "$REPO/unvarnished/output"
mkdir -p "$REPO/vektor/output/pdf"
mkdir -p "$REPO/vektor/output/pptx"
echo "  ✓ Output directories ready"

echo ""
echo "Setup complete. You can now run any build script."
echo ""
echo "Examples:"
echo "  python3 unvarnished/source/build_unv01.py"
echo "  python3 vektor/source/build_wp01_v3.py"
echo "  bash deploy.sh"
