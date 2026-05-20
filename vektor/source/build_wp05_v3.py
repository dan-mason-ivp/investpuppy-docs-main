"""WP-05: Multi-Currency Portfolio Infrastructure — vk5 build."""
import os as _os
_SCRIPT_DIR  = _os.path.dirname(_os.path.abspath(__file__))
_REPO_ROOT   = _os.path.dirname(_os.path.dirname(_SCRIPT_DIR))
_LOGOS       = _os.path.join(_REPO_ROOT, '_shared', 'logos')
_SCREENSHOTS = _os.path.join(_SCRIPT_DIR, 'screenshots')

import sys, os
sys.path.insert(0, '/home/claude')
from wp_builder_v3 import *
from reportlab.platypus import PageBreak, NextPageTemplate, Image
from reportlab.lib.utils import ImageReader

OUT      = '/home/claude/investpuppy/vektor/output/pdf/vk5-wp05-multi-currency.pdf'
SUBTITLE = 'Multi-Currency Infrastructure'
REF      = 'IP-WP-FX-260501-1.0'
SC_DIR   = _os.path.join(_SCRIPT_DIR, 'screenshots') + '/'

def sc(fname, caption):
    s = make_styles()
    items = []
    try:
        ir = ImageReader(SC_DIR + fname); iw, ih = ir.getSize()
        w = COL_W; h = w * ih / iw
        items.append(p('PLATFORM INTERFACE', s['tag']))
        items.append(Image(SC_DIR + fname, width=w, height=h))
        items.append(sp(4))
        items.append(p(caption, s['body_grey']))
    except Exception as e:
        print(f'Screenshot {fname}: {e}')
    return items

draw_cover = make_cover_fn(
    ['Multi-Currency', 'Portfolio', 'Infrastructure'],
    ['How Vektor handles daily FX rate collection, currency-adjusted portfolio valuation,',
     'and cross-border mandate management \u2014 for any currency pair.'],
    'For professional and institutional investors', REF)
draw_page = make_page_fn(SUBTITLE)
doc, f_cov, f_fst, f_lat = make_doc(OUT, SUBTITLE)
doc.addPageTemplates([
    PageTemplate(id='Cover', frames=[f_cov], onPage=draw_cover),
    PageTemplate(id='First', frames=[f_fst], onPage=draw_page),
    PageTemplate(id='Later', frames=[f_lat], onPage=draw_page),
])

s = make_styles()
story = [sp(1), NextPageTemplate('Later'), PageBreak()]

# ── ABSTRACT ──────────────────────────────────────────────────────────────────
story += [
    p('ABSTRACT', s['tag']),
    NoteBox(COL_W,
        'Multi-currency is treated as a configuration option in most portfolio platforms. '
        'In Vektor, it is a first-class design requirement, built in from the first prototype. '
        'Wealth teams managing clients across multiple currencies face a persistent infrastructure problem: '
        'portfolio valuations, performance calculations, and allocation decisions that span currency '
        'boundaries require daily FX rate data, consistent currency conversion logic, and a portfolio '
        'architecture that treats multi-currency mandates as a first-class use case rather than an '
        'afterthought. This paper describes Vektor\u2019s multi-currency infrastructure: daily FX collection, '
        'currency-adjusted valuation, and the platform\u2019s support for mandates spanning any combination '
        'of listed equity markets and base currencies.',
        s['body']),
    sp(10),
    key_takeaways_box([
        'Daily FX rate collection at 8 AM SGT ensures all portfolio valuations use current exchange rates \u2014 not rates from the previous week or quarter.',
        'Currency conversion is applied at the position level \u2014 enabling accurate per-instrument P&L attribution across currency boundaries.',
        'Any base currency can be configured per client \u2014 the same strategy can be run for an SGD client and a USD client simultaneously.',
        'FX rate history supports backwards-looking performance analysis in any reporting currency.',
    ], s),
    sp(10),
    p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {REF}  \u00b7  Copyright 2026 InvestPuppy', s['wp_ref']),
    PageBreak(), sp(0),
]

# ── SECTION 1 ─────────────────────────────────────────────────────────────────
story += [
    p('1. THE MULTI-CURRENCY PROBLEM IN WEALTH MANAGEMENT', s['wp_section']), hrm(),
    p('Why currency handling is not a peripheral feature \u2014 it is a core infrastructure requirement.', s['body_grey']),
    p('A boutique family office managing clients across Singapore, the UK, and the US faces a currency '
      'challenge on every portfolio decision. An allocation to Singapore equities for a USD-base client '
      'requires real-time SGD/USD conversion for accurate position valuation. A performance report for a '
      'GBP-base client holding a mixed SGX/LSE portfolio requires daily FX rates applied at the position '
      'level for each trading day in the reporting period. A rebalancing decision requires knowing the '
      'current FX-adjusted weight of each position \u2014 not the weight at the time of original allocation, '
      'which may have drifted materially with currency movements.', s['body']),
    p('None of these requirements are exotic. They are the daily operational reality of multi-currency '
      'wealth management.', s['body']),
    NoteBox(COL_W,
        'The alternative \u2014 converting currencies manually using bank rates or periodic batch processes '
        '\u2014 introduces latency, inconsistency, and the risk of valuation errors that compound over time. '
        'A platform that treats multi-currency as a first-class feature eliminates this risk entirely.',
        s['body']),
    sp(10),
]

# ── SECTION 2 ─────────────────────────────────────────────────────────────────
story += [
    p('2. DAILY FX RATE COLLECTION', s['wp_section']), hrm(),
    p('How Vektor collects and stores exchange rates \u2014 automatically, every market day.', s['body_grey']),
    p('Vektor collects daily foreign exchange rates from Yahoo Finance at 8 AM SGT every market day \u2014 '
      'the same time as the daily OHLCV price data refresh. Rates are stored with full history, enabling '
      'backwards-looking FX-adjusted performance calculations across any time period. The collection covers '
      'all FX pairs required by configured mandates. New currency pairs are added to the collection schedule '
      'automatically when a new mandate with a different base currency is configured.', s['body']),
]
for item in sc('sc09_instruments.png',
    'Instruments master \u2014 securities listed with exchange, currency, sector, and market cap. '
    'Multi-currency mandates configure the base currency per client; the platform handles conversion automatically.'):
    story.append(item)
story.append(sp(10))
story.append(PageBreak())
story.append(sp(0))

# ── SECTION 3 ─────────────────────────────────────────────────────────────────
story += [
    p('3. CURRENCY-ADJUSTED PORTFOLIO VALUATION', s['wp_section']), hrm(),
    p('How FX rates are applied at the position level to produce accurate cross-currency valuations.', s['body_grey']),
    p('Portfolio valuation in the client\u2019s base currency requires applying the relevant FX rate to each '
      'position denominated in a foreign currency. Vektor applies currency conversion at the position level '
      '\u2014 not at the portfolio aggregate level \u2014 ensuring that each holding\u2019s contribution to '
      'portfolio value is accurately stated in the reporting currency.', s['body']),
    p('This distinction matters for performance attribution: a position that gained 5% in local currency '
      'terms but lost 3% due to currency movement contributed only 2% to portfolio return in the base '
      'currency. Aggregate-level conversion masks this \u2014 position-level conversion reveals it.', s['body']),
]

# ── SECTION 4 ─────────────────────────────────────────────────────────────────
story += [
    p('4. PER-CLIENT BASE CURRENCY CONFIGURATION', s['wp_section']), hrm(),
    p('How the same strategy serves clients with different base currencies simultaneously.', s['body_grey']),
    p('Each client in Vektor has a configured base currency. The same investment strategy \u2014 for example, '
      'the SGP Equity Strategy holding SGX-listed securities in SGD \u2014 can simultaneously serve an SGD '
      'client and a USD client. For the SGD client, all valuations are in SGD. For the USD client, the same '
      'holdings are valued in USD using the daily SGD/USD rate. Capital allocation for the USD client is '
      'calculated in USD and converted to SGD at the time of position sizing. No manual conversion is '
      'required at any stage.', s['body']),
]
for item in sc('sc05_clients.png',
    'Customer management \u2014 clients configured with individual base currencies. The same strategy can be '
    'assigned to multiple clients with different currencies; valuation and reporting are handled per client automatically.'):
    story.append(item)
story.append(sp(10))
story.append(PageBreak())
story.append(sp(0))

# ── SECTION 5 ─────────────────────────────────────────────────────────────────
story += [
    p('5. GENERALISING BEYOND SGD/USD', s['wp_section']), hrm(),
    p('How the multi-currency infrastructure scales to any market and any currency pair.', s['body_grey']),
    p('The multi-currency infrastructure described in this paper is not specific to SGD/USD. Any listed equity '
      'market can be configured \u2014 London-listed industrials in GBP, US equities in USD, European equities '
      'in EUR \u2014 and any base currency can be set per client. The FX collection schedule expands '
      'automatically as new currency pairs are required. The position-level conversion logic applies '
      'identically regardless of the currency pair. The platform is currency-agnostic by design, consistent '
      'with its market-agnostic architecture.', s['body']),
]

# ── SECTION 6 — CONCLUSION ────────────────────────────────────────────────────
story += [
    p('6. CONCLUSION', s['wp_section']), hrm(),
    p('Multi-currency support is not a feature to be added later. It is a requirement that must be designed '
      'in from the start.', s['body_grey']),
    p('Vektor\u2019s daily FX collection, position-level currency conversion, and per-client base currency '
      'configuration provide the infrastructure that wealth teams managing cross-currency mandates require '
      '\u2014 without the manual processes, batch conversions, and valuation inconsistencies that characterise '
      'currency handling in spreadsheet-based workflows.', s['body']),
    NoteBox(COL_W,
        'Any currency pair. Any exchange. The configuration changes. The rigour does not.',
        s['pull'], bg=CARD_BG, bar=GOLD),
]
closing_row(
    'This paper describes Steps 10\u201311 of the Vektor workflow. For the full platform overview, see the '
    'Platform Brochure. For portfolio construction methodology, see WP-01. All documents at investpuppy.com.',
    REF, s, story)

doc.build(story)
sz = os.path.getsize(OUT)
print(f'Built: {OUT}')
print(f'Size:  {sz:,} bytes ({sz//1024}KB)')
