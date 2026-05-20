#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# deploy.sh — Propagate built outputs into website/assets/docs/
# Run from the investpuppy/ repo root after any build.
# ─────────────────────────────────────────────────────────────────────────────

set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
UNGATED="$REPO/website/assets/docs/ungated"
GATED="$REPO/website/assets/docs/gated"

echo "InvestPuppy deploy — $(date '+%Y-%m-%d %H:%M')"
echo ""

# ── Unvarnished → ungated ─────────────────────────────────────────────────────
echo "Copying Unvarnished papers → ungated..."
cp "$REPO/unvarnished/output/"ip-unv-*.pdf "$UNGATED/"

# ── Vektor commercial docs → ungated ─────────────────────────────────────────
echo "Copying Vektor commercial docs → ungated..."
for f in \
  vk5-at-a-glance.pdf \
  vk5-brochure.pdf \
  vk5-what-vektor-is-not.pdf \
  vk5-why-not-incumbents.pdf; do
  if [ -f "$REPO/vektor/output/pdf/$f" ]; then
    cp "$REPO/vektor/output/pdf/$f" "$UNGATED/"
  else
    echo "  WARNING: $f not found in vektor/output/pdf/"
  fi
done

# ── Vektor research series → gated ────────────────────────────────────────────
echo "Copying Vektor research series → gated..."
for f in \
  vk5-wp00-research-series-index.pdf \
  vk5-wp01-quantitative-portfolio-construction.pdf \
  vk5-wp02-signal-optimisation.pdf \
  vk5-wp03-capital-allocation.pdf \
  vk5-wp04-indicator-selection.pdf \
  vk5-wp05-multi-currency.pdf \
  vk5-wp06-audit-compliance.pdf \
  vk5-wp07-technical-architecture.pdf \
  vk5-wp08-ai-ml-philosophy.pdf \
  vk5-wp09-risk-disclosure.pdf \
  vk5-wp10-evaluating-performance.pdf \
  vk5-why-vektor.pdf \
  vk5-dd-navigation-guide.pdf; do
  if [ -f "$REPO/vektor/output/pdf/$f" ]; then
    cp "$REPO/vektor/output/pdf/$f" "$GATED/"
  else
    echo "  WARNING: $f not found in vektor/output/pdf/"
  fi
done

# ── Sync cover photos to website/assets/images/covers/ ───────────────────────
echo "Syncing cover photos..."
for f in "$REPO/_shared/cover-photos/"unv*.jpg; do
  fname=$(basename "$f")
  # Strip the _cover_photo suffix for website naming
  dest="${fname/_cover_photo/}"
  # website expects unv01_cover.jpg format
  dest="${dest/unv0/unv0}"; dest="${dest/.jpg/_cover.jpg}"
  dest="${dest/unv09_cover_photo/unv09_cover}"
  cp "$f" "$REPO/website/assets/images/covers/$(basename $f | sed 's/_cover_photo/_cover/')"
done

# ── Sync logos ────────────────────────────────────────────────────────────────
echo "Syncing logos..."
cp "$REPO/_shared/logos/ip_logo_dark_bg.png"  "$REPO/website/assets/images/"
cp "$REPO/_shared/logos/ip_logo_light_bg.png" "$REPO/website/assets/images/"
cp "$REPO/_shared/logos/ip_logo_vertical.png" "$REPO/website/assets/images/"

echo ""
echo "Done."
echo "  ungated: $(ls "$UNGATED"/*.pdf 2>/dev/null | wc -l) PDFs"
echo "  gated:   $(ls "$GATED"/*.pdf 2>/dev/null | wc -l) PDFs"
