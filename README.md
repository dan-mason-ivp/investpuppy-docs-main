# InvestPuppy — Master Repository
## Version 1.0 · May 2026

This is the single repository for all InvestPuppy content: the Vektor commercial document suite, the InvestPuppy: Unvarnished thought leadership series, and the investpuppy.com website.

---

## Repository structure

```
investpuppy/
│
├── README.md                    ← You are here. Master project state.
├── OUTSTANDING.md               ← Live outstanding items register
├── PANELS.md                    ← All panel rosters
├── PARKED.md                    ← Parked recommendations (P1–P5)
├── setup.sh                     ← Run once per session before building
├── deploy.sh                    ← Propagate outputs → website/assets/docs/
│
├── _shared/                     ← Single copy of all shared assets
│   ├── fonts/                   ← Poppins family (8 cuts)
│   ├── logos/                   ← IP logos + Vektor logos
│   ├── stamp/                   ← stamp_graphic.png
│   └── cover-photos/            ← Unvarnished cover photos (unv01–10)
│
├── vektor/                      ← Suite A — Vektor commercial documents
│   ├── source/                  ← Build scripts (wp_builder_v3.py + 26 scripts)
│   │   └── screenshots/         ← Chart PNGs (sc01–sc11) for white papers
│   ├── word/                    ← Canonical Word source files (19 .docx)
│   ├── output/
│   │   ├── pdf/                 ← Built PDFs (23 files)
│   │   └── pptx/                ← Built presentation decks (5 files)
│   └── internal/                ← Internal PDFs (brand spec, voice guide, etc.)
│
├── unvarnished/                 ← Suite B — InvestPuppy: Unvarnished series
│   ├── source/                  ← unvarnished_builder.py + build_unv01–10.py
│   └── output/                  ← Built PDFs (10 files, 43pp total)
│
└── website/                     ← investpuppy.com
    ├── pages/                   ← HTML files + css/ + js/
    ├── netlify.toml
    └── assets/
        ├── images/              ← Logos + cover photos (synced by deploy.sh)
        └── docs/
            ├── public/          ← Unvarnished PDFs + commercial docs (renamed from ungated/)
            └── qualified/       ← Research papers (renamed from gated/)
```

---

## Company overview

**Company:** InvestPuppy (investpuppy.com · contact@investpuppy.com)
**Product:** Vektor — systematic listed equity portfolio management platform
**Stage:** Pre-revenue prototype. IBKR simulation mode. Not yet live-trading.
**Primary market:** Singapore (SGX). Architecture region-agnostic.
**Target:** Boutique DPMs, independent RIAs, family offices, emerging market asset managers

**Governing principle:** Honest by design.
**Brand tagline:** Serious when it matters.

---

## Two document suites

### Suite A — Vektor (vk5) · CURRENT CANONICAL
Product documentation for the Vektor platform.

| Property | Value |
|---|---|
| Version | vk5 |
| Naming | vk5-[document-name].pdf / .docx / .pptx |
| Brand | VEKTOR BY INVESTPUPPY (v3 logo) |
| Accent | GOLD #C8A96E |
| Typography | Helvetica throughout |
| Status | Complete. Distribution-ready for Singapore. |
| Contents | 23 PDFs · 19 Word docs · 5 PPTX decks |

**vk4 is superseded.** Do not distribute or mix with vk5.

#### Vektor document inventory

**Ungated (client-facing, no registration):**
- vk5-at-a-glance.pdf
- vk5-brochure.pdf
- vk5-what-vektor-is-not.pdf
- vk5-why-not-incumbents.pdf

**Gated (post-registration):**
- vk5-why-vektor.pdf
- vk5-brand-story.pdf
- vk5-workflow-integration-guide.pdf
- vk5-founding-mandate-programme.pdf
- vk5-first-90-days.pdf
- vk5-mutual-nda.pdf
- vk5-wp00 through vk5-wp10 (research series)
- vk5-faq.pdf
- vk5-dd-navigation-guide.pdf

**Presentations (on request):**
- vk5-deck1-sixty-minute-meeting.pptx
- vk5-deck2-technical-deep-dive.pptx
- vk5-deck3-institutional-partner.pptx
- vk5-deck4-lightning-deck.pptx
- vk5-deck5-due-diligence.pptx

**Internal only (not for distribution):**
- vk5-brand-voice-guide.pdf
- vk5-brand-build-specification.pdf
- vk5-internal-document-journey.pdf
- vk5-outstanding-recommendations.pdf
- vk5-website-specification.pdf

### Suite B — InvestPuppy: Unvarnished (IP-UNV) · COMPLETE AND LOCKED
Thought leadership series on financial software implementation failure.

| Property | Value |
|---|---|
| Naming | ip-unv-XX-[title].pdf |
| Brand | InvestPuppy mark ONLY. No Vektor branding. |
| Accent | GREEN #85D155 |
| Typography | Poppins throughout (8 cuts) |
| Status | UNV-01 through UNV-10 built, panel-reviewed, content LOCKED |
| Total | 43 pages across 10 papers |

**Series strapline (interior only):** field notes from decades of bad projects.
**Brand tagline:** Serious when it matters.

#### Series inventory

| Ref | Title | Pages | Status |
|---|---|---|---|
| UNV-01 | Why financial software implementations fail | 4 | LOCKED |
| UNV-02 | Nobody owns it | 4 | LOCKED |
| UNV-03 | Complexity as cover: The consultant layer | 5 | LOCKED |
| UNV-04 | Plan last — discovery before configuration | 4 | LOCKED |
| UNV-05 | The change request trap | 4 | LOCKED |
| UNV-06 | The invisible stakeholders | 4 | LOCKED |
| UNV-07 | A hammer is a tool, not a methodology | 5 | LOCKED |
| UNV-08 | Life after live | 4 | LOCKED |
| UNV-09 | The U in UAT — kind of important... | 4 | LOCKED |
| UNV-10 | 9 Women Cannot Make a Baby in 1 Month | 5 | LOCKED — cover photo placeholder pending |

**UNV-05 cover photo provenance:** flagged by 3 panelists as possibly AI/stock. Dan to confirm.

---

## Critical terminology (Vektor)

| Never say | Always say |
|---|---|
| Monte Carlo | 10,000 portfolio configurations |
| 99.9% | 99.94% |
| permanently preferential | preferential commercial terms locked for the duration |
| simulations per strategy | portfolio configurations per strategy |

---

## Design systems

### Vektor design system
- **Accent:** GOLD #C8A96E
- **Background:** #0A0A0F
- **Typography:** Helvetica throughout
- **Builder:** `vektor/source/wp_builder_v3.py`

### Unvarnished design system
- **Accent:** GREEN #85D155
- **Dark:** #0A0A0A
- **Typography:** Poppins throughout (8 cuts — see `_shared/fonts/`)
- **Page:** A4 (595.27 × 841.89pt)
- **Cover split:** 58% photo / 42% dark band
- **Margins:** L/R 52pt, Bottom 44pt
- **Builder:** `unvarnished/source/unvarnished_builder.py`
- All design decisions LOCKED. Do not modify the builder without recording the change here.

---

## Website

**Platform:** Netlify (Pro recommended for password protection pre-launch)
**Spec:** IP-WEB-SPEC-260510-3.0 — Webflow rebuild is the long-term plan; current static site can deploy now.

**Pages:**
- `/` — Home (Unvarnished band + Founding Mandate CTA)
- `/platform` — The Platform
- `/why-vektor` — Why Vektor
- `/what-we-are-not` — What We Are Not
- `/unvarnished` — All 10 papers, ungated
- `/founding-mandate` — Founding Mandate enquiry form
- `/story` — The Story (brand/founder)
- `/research` — Gated research registration
- `/documents` — Document library

**Navigation (5 items):** Platform · Why Vektor · What We Are Not · Unvarnished · Founding Mandate

---

## How to start a new Claude session

Upload the entire `investpuppy/` folder as a zip. Claude reads this README first to orient. Then navigate to the relevant directory for the work required.

Paste this prompt:

> "I am continuing work on the InvestPuppy document suite. Please read README.md carefully — it is the master project state document. Once you have read it along with OUTSTANDING.md, confirm what you understand and ask what I would like to work on."

If building PDFs, run `setup.sh` first in the Claude session.

---

## Workflow for common tasks

### Rebuild an Unvarnished paper
```bash
bash setup.sh  # once per session
cd /path/to/investpuppy
python3 unvarnished/source/build_unv07.py
bash deploy.sh  # sync to website
```

### Rebuild a Vektor document
```bash
bash setup.sh  # once per session
cd /path/to/investpuppy
python3 vektor/source/build_wp01_v3.py
bash deploy.sh  # sync to website
```

### Update the website only
Edit files in `website/pages/`, then redeploy to Netlify (drag updated folder).

### After any document update
```bash
bash deploy.sh
```
Then redeploy `website/` to Netlify.

---

## Go-to-market status

**Commercial priority #1:** First Founding Mandate client conversation. Vektor suite is ready.

**UK distribution:** BLOCKED pending UK-01 FCA regulatory content. Do not distribute Vektor suite in UK without this.

**Singapore:** Distribution-ready.

---

## Panels

See PANELS.md for full rosters.

**Original panels (stood down):** Meridian, Arclight, Nova, Forge — 20 members total. Available to reconvene.

**New panel (active):** 20 members convened May 2026. Available for further tasking.

---

## Version history

| Version | Date | Notes |
|---|---|---|
| 1.0 | May 2026 | Unified repository created. Migrated from 5 separate packages: vk5-package-may2026.zip, unvarnished-repository-v1.zip, investpuppy-handoff-may2026.zip, investpuppy-site-may2026.zip, vk4-document-suite-may2026.zip (archived). |

---

*InvestPuppy · investpuppy.com · contact@investpuppy.com*
