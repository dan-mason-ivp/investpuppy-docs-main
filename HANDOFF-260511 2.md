# InvestPuppy / Vektor — Session Handoff
**Date:** 11 May 2026  
**Session scope:** Full investor pack rebuild, vk5 suite update, website build, super panel review series  
**Repository:** investpuppy-suite-may2026.zip (67MB)  
**Transcripts:** /mnt/transcripts/ (3 files, this session and prior)

---

## REPOSITORY STATE

### Investor Pack — 4 documents, distribution-ready
| File | Status |
|---|---|
| `ip-investor-onepager.pdf` | Built, QA passed |
| `ip-investor-deck.pptx` | Built, QA passed |
| `ip-investor-memo.pdf` | Built, QA passed |
| `ip-investor-model.xlsx` | Built, QA passed |

### vk5 Suite — 23 PDFs, all built
All 23 documents rebuilt this session. Build scripts at `/investpuppy/vektor/source/build_*_v3.py` and `build_deck.js`.

### Website — 11 pages
`index.html` · `platform.html` · `why-vektor.html` · `what-we-are-not.html` · `unvarnished.html` · `founding-mandate.html` · `research.html` · `documents.html` · `story.html` · `thank-you.html` · `pricing.html`

### Screenshots — 19 files
At `/investpuppy/vektor/source/screenshots/sc01_*.png` through `sc19_*.png`.  
All admin portal screens carry Vektor branding and `demo@investpuppy.com` credentials.

---

## DECISIONS LOCKED THIS SESSION

### Pricing model
- **Structure:** AUM-tiered annual subscription
- **Entry** ≤S$75M: S$24,000/yr
- **Growth** S$75M–S$250M: S$48,000/yr
- **Institutional** S$250M–S$750M: S$108,000/yr
- **Enterprise** S$750M+: S$168,000+/yr
- **Founding Mandate:** S$18,000/yr for 12 months, then permanently 1 tier below AUM tier (floor: Entry at S$24,000/yr)
- **Slots:** 3 (not 3–5)

### Pricing philosophy statement (locked in FAQ, FM doc, memo)
> "Vektor pricing is published openly and held consistently. It is not inflated to create negotiating room. Structured commercial flexibility exists for two defined reasons: multi-year subscription commitments, and reference partnerships where both parties receive something of genuine value. Outside those structures, the published rate applies. This pricing policy applies consistently across all clients. We set prices we can defend — and we defend them. That is what honest by design means in practice."

### Bloomberg pricing (verified 2026)
- Terminal: ~$31,980 USD / S$43,000+ SGD per seat per year
- PORT: additional S$8,000–S$25,000 per seat per year
- Data feeds (B-PIPE): separate enterprise product
- Three distinct competitive positions: capability provision / PORT replacement / development termination

### Platform language (locked throughout suite)
- NEVER: "simulation mode" / "not live-trading capable" / "Monte Carlo" / "permanently preferential" / "99.9%"
- ALWAYS: "has not yet executed in a live account" / "10,000 portfolio configurations" / "99.94%" / "preferential commercial terms locked for the duration"

### Singapore family office count
- 2,000+ single family offices (MAS, 2024) — source note required on all uses

### Website
- Public pricing teaser: "From S$24,000/year — below the cost of a single Bloomberg Terminal seat"
- Full pricing page: `/pricing.html` — public, no gate
- Team page: **REMOVED** — not ready for publication. Reinstate when founder biographies are finalised.

---

## OUTSTANDING — FOUNDER ACTIONS REQUIRED

### COMMERCIAL CRITICAL (before first investor conversation)
- [ ] **Founder names** — both still `[FOUNDER A]` and `[FOUNDER B]` throughout all 28 documents
- [ ] **Regulatory pathway** — MAS licensing status. Documents reference "a defined question with a defined answer." The answer must be prepared as a verbal response. Panel flagged this across 3 review rounds.
- [ ] **Valuation anchor** — range not yet decided. Must exist before the first investor meeting.
- [ ] **Unvarnished release strategy** — investor pack says "already in circulation." If not released, change to "ready for distribution" or execute the release. This is the most commercially urgent decision outstanding.
- [ ] **CTO biography** — `vk5-first-90-days.pdf` and team card both reference `[FOUNDER B — NAME]`

### IMPLEMENTATION / ONBOARDING PRICING — OPEN QUESTION
Panel discussion conducted this session. Question: should implementation, configuration, and go-live support be included in the annual subscription or charged separately?

**Panel position (not yet resolved):**
- Founding Mandate clients: include fully, no separate charge. Non-negotiable given First 90 Days document.
- Entry/Growth tiers: panel favours inclusion with defined standard scope.
- Institutional/Enterprise: panel split. Consensus toward "standard package included, enhanced services separately quoted at signing."
- Key tension: First 90 Days document commits to "CEO and CTO in your office week one." If implementation is separately charged, this commitment changes character.
- Investor view (Marcus Chen): keep ARR clean — professional services revenue muddies SaaS valuation multiples.
- **Action required:** Founder decision on scope of standard onboarding before first standard-tier client conversation. Update pricing page, FAQ Q12, and First 90 Days document once decided.

---

## OUTSTANDING — DOCUMENT FIXES (next rebuild only)

| Document | Issue | Action |
|---|---|---|
| `vk5-why-not-incumbents.pdf` | Bloomberg Terminal still cited at "~$24,000/yr" — pre-session figure | Update to ~$31,980 USD / S$43,000+ SGD at next rebuild |
| `vk5-wp10-evaluating-performance.pdf` | "operational in simulation mode" language | Update to "has not yet executed in a live account" at next rebuild |
| `vk5-what-vektor-is-not.pdf` | Platform status language updated in HTML but **PDF not rebuilt** | Rebuild from `build_what_vektor_is_not_v3.py` |

**Platform bugs (cannot fix in documents):**
- P-03: NaN% in strategy view (sc04) — platform fix required before brochure broadcast distribution
- P-04: KYC PENDING in customer management (sc05) — demo data fix required

---

## OUTSTANDING — WEBSITE (next build)

| Item | Status |
|---|---|
| Team page | Removed. Reinstate when founder biographies ready. |
| Founder names on founding-mandate.html | Still `[CEO]` and `[CTO]` placeholders |
| Privacy policy page | Referenced in footer privacy note but page does not exist |
| Form backend | All forms use `netlify` attribute — configure Netlify form handling on deploy |

---

## SUPER PANEL — OPEN TOPICS

The super panel (28 members, Meridian/Arclight/Nova/Forge + May 2026 cohort) was convened this session across multiple rounds. Outstanding topics not yet concluded:

1. **Implementation/onboarding pricing** — panel discussion complete, founder decision pending (see above)
2. **Unvarnished release strategy** — Tom Aldridge recommendation: lead with UNV-09 or UNV-07 for reach. Full release vs phased vs individual still unresolved.
3. **UNV-05 cover photo** — provenance to confirm (3 panelists flagged AI/stock risk)
4. **PARKED items** — P1 brand story doc, P2 "Before week one" synthesis, P3 UNV-09 closing page, P4 bidirectional cross-referencing, P5 temporal brand management brief

---

## BUILD SCRIPTS — QUICK REFERENCE

```bash
# Investor pack
cd /home/claude/investpuppy
python3 investor/source/build_onepager.py
node investor/source/build_deck.js
python3 investor/source/build_memo.py
python3 investor/source/build_model.py

# vk5 suite (all 23 docs)
cd /home/claude/investpuppy/vektor/source
python3 build_brochure_v3.py
python3 build_why_vektor_v3.py
python3 build_what_vektor_is_not_v3.py
python3 build_why_not_incumbents_v3.py   # needs Bloomberg price fix
python3 build_workflow_integration_guide_v3.py
python3 build_faq_v3.py
python3 build_founding_mandate_v3.py
python3 build_dd_nav_v3.py
python3 build_first_90_days_v3.py
python3 build_at_a_glance_v3.py
python3 build_mutual_nda_v3.py
python3 build_wp00_v3.py through build_wp10_v3.py

# Package full suite
cd /home/claude && zip -r /mnt/user-data/outputs/investpuppy-suite-may2026.zip investpuppy/ \
  --exclude "investpuppy/**/__pycache__/*" \
  --exclude "investpuppy/**/*.pyc" \
  --exclude "investpuppy/**/node_modules/*"
```

---

## DESIGN SYSTEM — DO NOT CHANGE

| Element | Value |
|---|---|
| Vektor accent | Gold `#C8A96E` |
| Vektor font | Helvetica |
| Vektor background | Dark `#0A0F0A` |
| InvestPuppy accent | Green `#85D155` |
| InvestPuppy font | Poppins |
| Unvarnished brand | InvestPuppy only — NO Vektor mark anywhere |
| Website font | Inter (current) |
| Website background | `#0A0A0A` |

---

## BRAND VOICE — CRITICAL RULES

- NEVER "Monte Carlo" → "10,000 portfolio configurations"
- NEVER "99.9%" → "99.94%"
- NEVER "permanently preferential" → "preferential commercial terms locked for the duration"
- NEVER "simulations per strategy" → "portfolio configurations per strategy"
- NEVER "not live-trading capable" → "has not yet executed in a live account"
- NEVER "$25K+ Bloomberg" → "~$31,980/yr USD / S$43,000+ SGD per seat (2026 verified)"
- Bloomberg Terminal ≠ Bloomberg PORT ≠ Bloomberg data feeds — three separate products, different competitive positions
- InvestPuppy name is NOT changing
- Governing principle: "Honest by design"
- Brand philosophy: See it clearly → Own it completely → Ask what it gives you

---

## PANEL ROSTER

**Original panels (stood down, available to reconvene):** Meridian, Arclight, Nova, Forge — 20 members total.

**May 2026 fresh-eyes panel (active):** Patrick Seah, Charlotte Beaumont, Nadia Petrov, Marcus Tan, Geoffrey Holt, Samantha Reyes, Andrew Fong, Kavita Sharma, Sophie Laurent, Victor Huang, Daniel Osei + 9 others. Full roster in `PANEL-ROSTERS.md`.

**Investor review panel (used this session):** Rachel Tan, James Whitfield, Priya Menon, Marcus Chen, Sophia Hartley, Tan Wei Lin, David Okafor, Nadia Petrov, Robert Lim.

**Super panel (convened this session):** All 28 members from both cohorts. Delphi process used: individual anonymous responses → anonymised summary → group discussion.

**LOCKED POLICY:** All panel feedback delivered as plain text in chat. No interactive artifacts, React components, or external pages for panel reviews.

---

## COMMERCIAL PRIORITY ORDER

1. **First Founding Mandate client conversation** — suite ready. Must begin.
2. **Founder names decision** — required before any named distribution.
3. **Unvarnished release decision** — required before investor pack references can be accurate.
4. **Regulatory pathway answer** — required before first investor meeting.
5. **Valuation anchor** — required before first investor meeting.
6. **Implementation pricing decision** — required before first standard-tier client conversation.
7. **UK-01 FCA regulatory content** — UK distribution blocker. WP-07 depth required.

---

*Handoff prepared 11 May 2026. Next session: pick up at implementation/onboarding pricing decision and any subsequent build requirements.*
