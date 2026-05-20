"""WP-04: Technical Indicator Selection: Grid Search Methodology — vk5 build."""
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

OUT      = '/home/claude/investpuppy/vektor/output/pdf/vk5-wp04-indicator-selection.pdf'
SUBTITLE = 'Technical Indicator Selection'
REF      = 'IP-WP-TIS-260501-1.0'
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
    ['Technical Indicator', 'Selection:', 'Grid Search Methodology'],
    ["A practitioner's guide to systematic parameter optimisation across six technical indicators",
     '\u2014 and how Sharpe-ranked selection produces consistent, instrument-specific trading signals.'],
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
        'Default indicator parameters \u2014 SMA 50/200, RSI 14 \u2014 were calibrated for the average instrument '
        'in average conditions. We do not use them. This paper explains why, and exactly what we use instead. '
        'Technical indicators are commonly applied with default or rule-of-thumb parameters \u2014 a practice '
        'that ignores the significant variation in optimal configurations across different instruments and market '
        'regimes. This paper presents the grid search methodology used by Vektor to identify the optimal '
        'indicator and parameter set for each individual holding: how the search space is defined, how '
        'performance is evaluated, how the winning configuration is selected, and how the process generalises '
        'across any listed equity market.',
        s['body']),
    sp(10),
    key_takeaways_box([
        'Default indicator parameters (e.g., SMA 50/200) are designed for the average \u2014 not for any specific instrument.',
        'A full grid search across the parameter space of six indicators identifies the configuration with the highest historical risk-adjusted return for each stock.',
        'Annualised Sharpe ratio is the primary selection criterion \u2014 it penalises high-volatility signals and rewards consistent, risk-adjusted performance.',
        'Three years of daily price data provides sufficient history for stable Sharpe estimation while remaining relevant to current market conditions.',
    ], s),
    sp(10),
    p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {REF}  \u00b7  Copyright 2026 InvestPuppy', s['wp_ref']),
    PageBreak(), sp(0),
]

# ── SECTION 1 ─────────────────────────────────────────────────────────────────
story += [
    p('1. WHY DEFAULT PARAMETERS FAIL', s['wp_section']), hrm(),
    p('The problem with applying industry-standard indicator parameters to individual instruments.', s['body_grey']),
    p('The SMA 50/200 crossover \u2014 the so-called golden cross \u2014 is the most widely referenced technical '
      'signal in institutional and retail portfolio management. It is applied identically to every instrument '
      'in countless systematic strategies. The assumption embedded in this practice is that the same look-back '
      'period is equally relevant to a large-cap financial stock, a small-cap industrial, and a real estate '
      'trust in the same market. This assumption is demonstrably false.', s['body']),
    p('Different instruments have different natural cycle lengths, different liquidity profiles, different '
      'volatility regimes, and different sensitivities to market-wide factors. An instrument that trends '
      'strongly over 30-day periods will not be well served by a 200-day slow average. An instrument with '
      'high intraday volatility may generate more false signals from an RSI configured for slower-moving '
      'stocks. The solution is not to find a better universal parameter \u2014 it is to abandon the premise '
      'of universality.', s['body']),
]

# ── SECTION 2 — PARAMETER TABLE ───────────────────────────────────────────────
story += [
    p('2. DEFINING THE SEARCH SPACE', s['wp_section']), hrm(),
    p('How the parameter ranges for each indicator are specified and bounded.', s['body_grey']),
    p('For each of the six indicators, Vektor defines a bounded parameter space calibrated to the typical '
      'behaviour of listed equities with at least three years of price history. The ranges are set to cover '
      'the full spectrum of plausible configurations while excluding economically unreasonable extremes.',
      s['body']),
    sp(8),
]
# Parameter table
hdr = [p('INDICATOR', s['tbl_hdr']), p('PARAMETER', s['tbl_hdr']),
       p('RANGE', s['tbl_hdr']),     p('STEP', s['tbl_hdr'])]
rows_data = [
    ('SMA',  'Short period',     '10\u201330 days', '1'),
    ('SMA',  'Long period',      '40\u201380 days', '1'),
    ('EMA',  'Short period',     '10\u201330 days', '1'),
    ('EMA',  'Long period',      '40\u201380 days', '1'),
    ('MACD', 'Short EMA',        '5\u201320',        '1'),
    ('MACD', 'Long EMA',         '20\u201350',       '1'),
    ('MACD', 'Signal period',    '5\u201315',        '1'),
    ('BB',   'SMA period',       '10\u201330 days', '1'),
    ('BB',   'Std deviations',   '1\u20133',         '0.5'),
    ('RSI',  'Period',           '10\u201320 days', '1'),
    ('RSI',  'Upper threshold',  '60\u201380',       '5'),
    ('RSI',  'Lower threshold',  '20\u201340',       '5'),
    ('SO',   'Period',           '10\u201320 days', '1'),
    ('SO',   '%D smoothing',     '2\u20135',         '1'),
]
tbl_rows = [hdr]
for ind, param, rng, step in rows_data:
    tbl_rows.append([p(ind, s['tbl_gold']), p(param, s['tbl_body']),
                     p(rng, s['tbl_body']),  p(step, s['tbl_body'])])
cw = [20*mm, 50*mm, 45*mm, COL_W-119*mm]
tbl = Table(tbl_rows, colWidths=cw)
tbl.setStyle(TableStyle([
    ('BACKGROUND',     (0,0), (-1,0),  CARD_BG),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [NOTE_BG, CARD_BG]),
    ('TOPPADDING',     (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING',    (0,0), (-1,-1), 9), ('RIGHTPADDING',  (0,0), (-1,-1), 9),
    ('LINEBELOW',      (0,0), (-1,-2), 0.3, RULE_MIN),
    ('BOX',            (0,0), (-1,-1), 0.4, CARD_EDGE),
    ('VALIGN',         (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(tbl)
story.append(sp(10))
story.append(PageBreak())
story.append(sp(0))

# ── SECTION 3 ─────────────────────────────────────────────────────────────────
story += [
    p('3. SHARPE RATIO AS SELECTION CRITERION', s['wp_section']), hrm(),
    p('Why Sharpe ratio is the correct objective function \u2014 and what it captures that raw return does not.', s['body_grey']),
    p('Maximising raw return from a technical indicator backtest produces configurations that generate large '
      'gains but with commensurately large drawdowns \u2014 high-volatility signals that may perform well in '
      'trending markets but catastrophically in ranging ones. Minimising volatility alone produces overly '
      'conservative signals that generate few trades and limited performance. The Sharpe ratio balances both: '
      'it selects the configuration that produces the most return per unit of risk, consistently.', s['body']),
    p('For each configuration tested, the annualised Sharpe ratio is calculated as: (annualised signal return '
      '\u2212 risk-free rate) / annualised standard deviation of signal returns. The risk-free rate used is '
      'the current national benchmark rate for the relevant market (e.g., Singapore 3-month T-bill rate for '
      'SGX mandates).', s['body']),
]

# ── SECTION 4 ─────────────────────────────────────────────────────────────────
story += [
    p('4. THREE YEARS OF DAILY DATA', s['wp_section']), hrm(),
    p('Why the three-year look-back window is the correct balance between stability and relevance.', s['body_grey']),
    p('A shorter look-back period (e.g., one year) produces Sharpe estimates that are sensitive to recent '
      'market conditions \u2014 potentially selecting a configuration that performed well in a recent bull run '
      'but has no long-term validity. A longer look-back (e.g., ten years) incorporates market regimes that '
      'are no longer relevant to current conditions. Three years of daily data provides approximately 750 '
      'trading days \u2014 sufficient for statistically stable Sharpe estimation while remaining anchored to '
      'conditions that are reasonably representative of the current market.', s['body']),
]
for item in sc('sc10_prices.png',
    'Price history detail \u2014 daily OHLCV data auto-refreshed every morning at 8 AM SGT. '
    'Three years of history used for all signal backtests and grid searches.'):
    story.append(item)
story.append(sp(10))
story.append(PageBreak())
story.append(sp(0))

# ── SECTION 5 ─────────────────────────────────────────────────────────────────
story += [
    p('5. OVERFITTING AND OUT-OF-SAMPLE VALIDITY', s['wp_section']), hrm(),
    p('The most important question about any grid search: how do you know the optimised parameters work out of sample?', s['body_grey']),
    p('This is the correct question and it deserves a direct answer. A grid search that selects parameters '
      'purely on in-sample Sharpe ratio risks overfitting \u2014 selecting a configuration that performed '
      'well on historical data but degenerates on unseen data. Three design decisions explicitly address '
      'this risk.', s['body']),
    p('<b>Parameter range bounding.</b> The search space is bounded by economically motivated ranges, not by '
      'whatever produces the highest in-sample Sharpe. This reduces effective degrees of freedom and limits '
      'overfitting scope.', s['body']),
    p('<b>Sharpe ratio as objective, not raw return.</b> Maximising raw return on a backtest reliably produces '
      'overfitting. Sharpe ratio penalises volatility, selecting more stable, regime-robust configurations '
      'over those that fitted a specific trending period.', s['body']),
    p('<b>Daily re-optimisation against rolling data.</b> The grid search re-runs against the most recent '
      'three years of data whenever a strategy is created or reviewed. This provides a continuous implicit '
      'out-of-sample test.', s['body']),
    NoteBox(COL_W,
        'Candour note: these design decisions reduce overfitting risk materially but do not eliminate it. '
        'No in-sample optimisation can guarantee out-of-sample performance. The XGBoost validation layer '
        '(WP-02) provides an additional real-time filter at the point of execution. The roadmap includes '
        'formal walk-forward validation as live track record develops.',
        s['body']),
    sp(10),
]

# ── SECTION 6 — CONCLUSION ────────────────────────────────────────────────────
story += [
    p('6. CONCLUSION', s['wp_section']), hrm(),
    p('Systematic parameter optimisation is not more complex than applying default parameters \u2014 it is simply more precise.', s['body_grey']),
    p('The grid search methodology ensures every instrument carries a trading signal calibrated to its own '
      'price behaviour \u2014 reproducible, transparent, and optimised for risk-adjusted performance. The '
      'overfitting risks inherent in parameter optimisation are addressed through bounded search spaces, '
      'Sharpe-based selection, and daily re-optimisation against rolling data.', s['body']),
]
closing_row(
    'This paper provides the technical detail behind Step 04 of the Vektor workflow. For XGBoost signal '
    'validation, see WP-02: Per-Instrument Signal Optimisation. For portfolio construction, see WP-01. '
    'All documents at investpuppy.com.',
    REF, s, story)

doc.build(story)
sz = os.path.getsize(OUT)
print(f'Built: {OUT}')
print(f'Size:  {sz:,} bytes ({sz//1024}KB)')
