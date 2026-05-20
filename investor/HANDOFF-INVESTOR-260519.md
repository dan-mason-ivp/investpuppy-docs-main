# InvestPuppy — Investor Pack Handoff
## Session: May 19 2026
## Status: Complete — distribution-ready subject to noted open items

---

## PACK VERSION SUMMARY

| Document | File | Version | Status |
|---|---|---|---|
| Covering Note | ip-investor-covering-note.pdf | v2.2 | Distribution-ready |
| Investor Overview | ip-investor-onepager.pdf | v3.0 (rebuild) | Distribution-ready |
| NDA Deck | ip-investor-deck-nda.pptx | v2.3 | Distribution-ready |
| Investor Memo | ip-investor-memo.pdf | v2.4 | Distribution-ready |
| Financial Model | ip-investor-model.xlsx | v1.3 | Distribution-ready (see open items) |
| Share Structure Briefing | ip-share-structure-briefing.pdf | v1.0 | Internal only |
| Founder Context | ip-founder-context.pdf | v1.0 | Pre-NDA distribution |

---

## BUILD SCRIPTS (all in /home/claude/)

| Script | Document | Notes |
|---|---|---|
| build_covering_note.py | Covering note | Full rebuild |
| build_memo.py | Investor memo | 987 lines |
| build_onepager_v2.py | One-pager | v2 rebuild — single page |
| build_model_update.py | Financial model | Run after build_model.py |
| build_share_brief.py | Share structure briefing | Internal only |
| build_founder_context.py | Founder Context | Pre-NDA document |

---

## KEY DECISIONS THIS SESSION

### Raise Parameters (FINAL)
- Raise target: **US$2.5M** (was US$2M–US$2.5M range — floor raised, range dropped)
- Pre-money: **US$9M–US$10M** (unchanged)
- Structure: Quiet raise · 3–5 investors · boutique wealth practitioners or fintech-experienced angels
- Full-time commitment: both founders on close

### Team Compensation
- Founding team compensated at **market rate** (not below-market)
- Market rate (base case): CEO US$280K · CTO US$240K · 3 collaborators US$150K–US$180K = **US$1,030K/yr total**
- Framework visible in Assumptions tab of financial model
- Actual draw cells (yellow, base case = market rate) — founders to confirm
- Philosophy: founders' alignment through equity, not personal financial compromise

### Financial Profile (updated for market-rate team costs)
| | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| Total ARR | US$77K | US$167K | US$878K | US$1,493K | US$2,520K |
| EBITDA | (US$1,104K) | (US$1,132K) | (US$618K) | (US$299K) | **US$366K** |
| EBITDA margin | n/m | n/m | n/m | n/m | **15%** |

- EBITDA breakeven: **Year 5** (base case) — Year 3 (bull case)
- Runway at US$2.5M raise: **~28–29 months** to Series A milestone

### Tenzor Pricing (updated for institutional credibility)
- Standard (up to US$500M AUM): **US$300K/yr**
- Growth (US$500M–US$2B AUM): **US$480K/yr**
- Institutional (US$2B+ AUM): **US$720K/yr**
- TAM: Tenzor direct **~US$10M–US$13M ARR** · combined **~US$25M–US$28M ARR** (3 markets, 10% penetration)

### Exit Philosophy (panel-agreed, locked)
*"InvestPuppy is building what the incumbents should have built and chose not to. At revenue maturity, that creates a natural acquisition landscape. InvestPuppy is not building toward those outcomes. It is building away from the platforms that created the problem it is solving."*

### Deck Structure (final)
1. Title · 2. Problem · 3. Platform · 4. Team · 5. Delivery Models · 6. Revenue Model · 7. Tenzor (NDA) · 8. Market · 9. Financial Projections · 10. Go-to-Market · 11. The Raise · 12. Appendix

---

## LOCKED TERMINOLOGY (COMPLETE SET — session additions marked *)

| Term | Rule |
|---|---|
| "10,000 portfolio configurations" | Never "Monte Carlo" or "simulations per strategy" |
| "99.94% capital allocation efficiency" | * BOTH number AND descriptor locked. Never "uptime", "availability" or "commitment" |
| "preferential commercial terms locked for the duration" | Never "permanently preferential" |
| "Proof Partners" (boutique) / "Alloy Partners" (institutional) | Never "Founding Mandate Programme" or "early adopters" |
| "has not yet executed in a live account" | Never "simulation mode" |
| "Vektor : Boutique · Vektor : House · Vektor : Wrapped" | Spaces around colon |
| "THE NATURAL PROGRESSION" | Framing for Tenzor — not "WHY TWO PRODUCTS" |
| "Tenzor development begins post first Vektor Proof Partners go-live" | Go-live not signed/contracted |
| "building away from the platforms that created the problem" | Exit philosophy — never "trade sale is the primary exit" |
| "InvestPuppy compensates its founding team at market rate" | * Compensation philosophy — never below-market framing |

---

## MARKET GEOGRAPHY (confirmed complete set)

1. **Singapore** — primary, distribution-ready now (2,000+ SFOs, MAS 2024)
2. **Switzerland** — near-term, FinIA compliance, OpenWealth established
3. **UK** — FCA regulatory opinion underway (escalation clause if UK Proof Partner)
4. **Rest of Europe** — Luxembourg, Germany, Liechtenstein, Channel Islands (Jersey, Guernsey), Crown Dependencies — medium-term pipeline
5. **SE Asia broadly** — EAM/MFO growth, Wrapped channel multiplier
6. **DIFC / UAE** — first qualifying conversation active

Addressable market: ~US$15M ARR (SG, CH, UK only — 3 markets, 10% penetration). Conservative baseline, not ceiling.

---

## INVESTOR PANEL FINAL VERDICT

Panel of 10 (investment management, VC, strategic, former founder):

| Member | Role | Would invest? |
|---|---|---|
| James Whitfield-Cross | UK DPM, angel | Yes |
| Soo-Jin Park | Singapore SFO | Yes |
| Benedikt Gruber | Zurich MFO | Yes |
| Amara Osei-Bonsu | Singapore boutique DPM | Yes |
| Charlotte Beaumont | UK IWM | Yes |
| Rajan Mehta | Singapore SFO, seed investor | Yes |
| Marcus Webb | Singapore fintech VC | Conditional |
| Eliza Thornton | London B2B fintech VC | Yes |
| Dr. Heinrich Maurer | Swiss private bank venture | Yes |
| Nadia Volkov | Former founder, angel | Yes |

**9–1. Marcus conditional on fund lifecycle / Year 5 breakeven path.**

---

## OPEN ITEMS (must address before distribution)

### CRITICAL — pre-distribution
- [ ] **Actual salary draws** — populate yellow cells in Assumptions tab (currently set to market rate as placeholder)
- [ ] **Revenue assumptions rework** — Year 1 US$77K reconciliation with actual PP slot/tier mix once conversations begin
- [ ] **Numbers review** — full financial model review once actual costs confirmed

### HIGH — pre-distribution or at NDA stage
- [ ] **UK incorporation prerequisites** — employment contract review (both founders), UK solicitor for EIS/advance assurance, UK personal tax call (CEO), Singapore OpCo incorporation, IP assignment
- [ ] **CEO@ and CTO@ email routing** — set up forwarding addresses before materials go out
- [ ] EIS advance assurance filing — UK counsel

### MEDIUM — post-first conversation
- [ ] PPTX voice review
- [ ] WP-09 regime risk section
- [ ] PR-08 founder biography
- [ ] UNV-10 cover photo commission
- [ ] UNV-05 cover photo provenance confirmation
- [ ] Webflow rebuild (A6)

---

## RENDERING NOTE
Slide 7 (Tenzor) header band renders dark in LibreOffice. Correct in PowerPoint. Not a distribution issue.

---

## CONTACTS (investor-facing)
- General enquiries: contact@investpuppy.com
- Investor / CEO communications: CEO@investpuppy.com
- Technical / CTO communications: CTO@investpuppy.com
- Website: investpuppy.com · investpuppy.com/unvarnished

---

*Handoff prepared: May 19 2026 · InvestPuppy · Confidential*
