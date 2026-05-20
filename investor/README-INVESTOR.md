# InvestPuppy — Investor Pack

## Scope
This directory contains all materials for InvestPuppy's seed round fundraising.
It is entirely separate from the Vektor commercial suite (vektor/) and the
Unvarnished thought leadership series (unvarnished/). No content from this
directory should appear in client-facing Vektor materials without deliberate
cross-referencing decisions recorded here.

The only shared assets used are _shared/logos/ and _shared/fonts/.

---

## Round summary

| Field | Value |
|---|---|
| Round | Seed |
| Raise target | S$1M–S$2M |
| Use of funds | Engineering build-out · Sales & BD headcount · Operational runway (18–24 months) |
| Stage | Pre-revenue prototype. IBKR simulation mode. Not yet live-trading. |
| Team | 2 co-founders — fintech / financial software backgrounds |
| Revenue model | Under development (see V5 in main OUTSTANDING.md) |
| Primary market | Singapore (SGX). Architecture region-agnostic. |

---

## Pack contents

| File | Format | Status |
|---|---|---|
| ip-investor-onepager.pdf | PDF | Draft |
| ip-investor-deck.pptx | PPTX | Not started |
| ip-investor-memo.pdf | PDF | Not started |
| ip-investor-model.xlsx | Excel | Not started |

---

## Design system

Investor materials use a distinct design from both Vektor and Unvarnished:

| Property | Value |
|---|---|
| Background | White (#FFFFFF) — print-friendly |
| Primary accent | InvestPuppy green (#85D155) |
| Secondary | Dark charcoal (#1A1A1A) |
| Typography | Poppins (from _shared/fonts/) |
| Logo | IPHorizontalClear.png (dark version on light backgrounds) |

Rationale: Investor documents are printed and shared in formal settings.
Light-background treatment is appropriate. Green accent maintains InvestPuppy
brand without conflating with Vektor (gold) or Unvarnished (green on dark).

---

## Outstanding / decisions needed

| # | Item | Priority |
|---|---|---|
| I1 | Revenue model — finalise subscription/AUM/hybrid structure | HIGH (blocks financial model) |
| I2 | Founder names and bios — [FOUNDER A] / [FOUNDER B] placeholders in use | HIGH |
| I3 | CEO / CTO designation — confirm before finalising deck | HIGH |
| I4 | Valuation / cap table structure | MEDIUM |
| I5 | Target investor profiles — angels, family offices, institutional seed? | MEDIUM |

---

## Build instructions

```bash
bash setup.sh  # once per session (installs Poppins fonts)
python3 investor/source/build_onepager.py
```

Output lands in investor/output/pdf/.

---

*InvestPuppy · investpuppy.com · contact@investpuppy.com*
