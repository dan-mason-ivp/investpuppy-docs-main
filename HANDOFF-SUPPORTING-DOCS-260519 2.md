# InvestPuppy — Supporting Documents Handoff
## Session: May 19 2026
## Scope: Non-investor-pack documents from this and immediately prior sessions

---

## CONTENTS

### 1. Brand & Product Architecture
| File | Description | Status |
|---|---|---|
| ip-brand-product-roadmap.pdf | Brand Tier Framework, admin portal specs, product architecture | Current |
| build_roadmap.py | Build script for brand/product roadmap PDF | Current |
| build_roadmap_base.py | Base builder for roadmap | Current |

**Covers:** Brand Tier Framework (Tier 1 dark / Tier 2 brand-inflected / Tier 3 clean functional), admin portal login and dashboard specifications (dark ground, metric card treatment), "One Size Fits None." brand line, button style open decision (Option A gold border vs Option B filled gold — not yet resolved).

---

### 2. Tenzor Brand Documents
| File | Description | Status |
|---|---|---|
| tenzor-brand-260518.zip | Tenzor brand comparison + handoff | May 18 2026 |
| tenzor-brand-comparison.jsx | React component — Tenzor vs Vektor brand comparison | May 18 2026 |
| HANDOFF-TENZOR-BRAND-260518.md | Tenzor brand session handoff | May 18 2026 |

**Covers:** Tenzor brand direction (institutional-grade, distinct from Vektor : Boutique), naming logic (tensor generalises vector across multiple dimensions), brand relationship between Vektor and Tenzor platforms.

**Note:** Tenzor is not publicly disclosed. These documents are NDA-stage only.

---

### 3. Website Pricing Documents
| File | Description | Status |
|---|---|---|
| prices.js | Single source of truth for all pricing — USD primary | Current |
| pricing.html | Updated pricing page for investpuppy.com | Current |
| website-pricing-update-260518.zip | Full website pricing update package | May 18 2026 |

**Covers:** USD as single default and binding currency. Non-USD prices are illustrative with "approx." prefix. prices.js is the canonical source — never edit for currency changes. Staging URL: https://staging-investpuppy.netlify.app

**Critical rule:** prices.js is the single source of truth. All pricing changes must flow from this file. Never hardcode prices elsewhere.

---

### 4. Previous Investor Pack (May 18 — superseded)
| File | Description | Status |
|---|---|---|
| investpuppy-investor-260518.zip | Full investor pack v1 (May 18 2026) | Superseded |
| ip-investor-deck.pptx | Original pre-NDA investor deck (pre-rebuild) | Superseded |
| HANDOFF-INVESTOR-260518.md | May 18 investor pack session handoff | Historical |

**Note:** These are the May 18 versions, before the full pack rebuild in today's session. Retained for reference. All distribution should use the May 19 versions in investpuppy-investor-pack-260519.zip.

---

## OPEN ITEMS FROM SUPPORTING DOCUMENTS

### Brand & Admin Portal
- [ ] Button style decision: Option A (gold border) vs Option B (filled gold) — not yet resolved
- [ ] A5 production rebuild of Vektor suite docs (v2, 32 docs) still outstanding
- [ ] Webflow rebuild (A6) still outstanding

### Website
- [ ] Webflow rebuild pending (current site is HTML, staging only)
- [ ] Currency selector validated but Webflow migration not yet done

### Unvarnished Series
- [ ] UNV-10 cover photo — commission outstanding
- [ ] UNV-05 cover photo — provenance confirmation needed
- [ ] Release strategy not yet decided: individual vs full set, phased vs simultaneous
- [ ] Tom Aldridge recommends leading with UNV-09 or UNV-07 for reach

### Parked Items (from earlier sessions)
- P1: Brand story document (5-gap brief exists)
- P2: "Before week one" synthesis/action doc
- P3: UNV-09 closing page
- P4: Bidirectional Vektor ↔ Unvarnished cross-referencing
- P5: Temporal brand management brief

---

*Handoff prepared: May 19 2026 · InvestPuppy · Confidential*
