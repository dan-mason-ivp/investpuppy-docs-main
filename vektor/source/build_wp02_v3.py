"""WP-02: Per-Instrument Signal Optimisation & XGBoost Validation — vk5 build."""
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

OUT      = '/home/claude/investpuppy/vektor/output/pdf/vk5-wp02-signal-optimisation.pdf'
SUBTITLE = 'Per-Instrument Signal Optimisation'
REF      = 'IP-WP-SIG-260501-1.0'
SC_DIR   = _os.path.join(_SCRIPT_DIR, 'screenshots') + '/'

def sc(fname, caption):
    """Screenshot card with caption."""
    path = SC_DIR + fname
    items = []
    try:
        ir = ImageReader(path); iw, ih = ir.getSize()
        w = COL_W; h = w * ih / iw
        items.append(p('PLATFORM INTERFACE', make_styles()['tag']))
        items.append(Image(path, width=w, height=h))
        items.append(sp(4))
        items.append(p(caption, make_styles()['body_grey']))
    except Exception as e:
        print(f'Screenshot {fname}: {e}')
    return items

draw_cover = make_cover_fn(
    ['Per-Instrument Signal', 'Optimisation &', 'XGBoost Validation'],
    ['How Vektor selects the optimal technical indicator for every individual holding',
     '\u2014 and why one-size-fits-all signal strategies leave alpha on the table.'],
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
        'One-size-fits-all signal selection is where most systematic portfolios leave alpha on the table. '
        'This paper describes exactly how Vektor recovers it \u2014 per instrument, not on average. '
        'Standard quantitative portfolio strategies apply a single technical indicator across all holdings \u2014 '
        'a compromise that optimises for the average at the expense of the individual. This paper describes '
        'Vektor\u2019s per-instrument signal optimisation methodology: a full grid search across six technical '
        'indicators for each holding, Sharpe-ranked parameter selection, and a two-stage XGBoost validation '
        'layer that filters live signals before execution. The result is a portfolio where every position is '
        'driven by the indicator that actually worked for that specific instrument \u2014 not the one that '
        'performed best on average across the universe.',
        s['body']),
    sp(10),
    key_takeaways_box([
        'A single technical indicator applied across a universe is a known source of lost alpha. Per-instrument selection recovers it.',
        'Grid search across six indicators with full parameter optimisation produces the highest-Sharpe configuration for each individual stock.',
        'XGBoost validation adds a second layer of signal verification, filtering out low-confidence signals before they reach execution.',
        'The winning indicator, its optimised parameters, and its backtest Sharpe ratio are stored in the strategy record \u2014 fully transparent and auditable.',
    ], s),
    sp(10),
    p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {REF}  \u00b7  Copyright 2026 InvestPuppy', s['wp_ref']),
    PageBreak(), sp(0),
]

# ── SECTION 1 ─────────────────────────────────────────────────────────────────
story += [
    p('1. THE PROBLEM WITH UNIVERSAL SIGNALS', s['wp_section']), hrm(),
    p('Why a single indicator applied across a portfolio is a structural source of lost alpha.', s['body_grey']),
    p('Technical indicators are designed to detect specific price behaviours \u2014 momentum, mean reversion, '
      'volatility breakouts, overbought/oversold conditions. Different instruments exhibit different dominant '
      'price behaviours at different points in time. A financial services stock in Singapore may trend strongly '
      'and respond well to a simple moving average crossover. A smaller industrial stock in the same universe '
      'may exhibit high volatility and respond better to a Bollinger Band breakout signal. Applying the same '
      'indicator to both instruments does not produce the best outcome for either \u2014 it produces a mediocre '
      'outcome for both.', s['body']),
    p('This is not a theoretical concern. In a ten-stock portfolio, if three holdings are generating signals '
      'from a sub-optimal indicator, the portfolio\u2019s systematic edge is materially reduced. Across a '
      'larger mandate, the effect compounds. The solution is not a better universal indicator \u2014 it is '
      'per-instrument selection.', s['body']),
    NoteBox(COL_W,
        'The six indicators evaluated by Vektor \u2014 SMA, EMA, MACD, Bollinger Bands, RSI, and Stochastic '
        'Oscillator \u2014 were selected to cover the primary categories of price behaviour: trend-following, '
        'momentum, volatility, and mean reversion. Together they represent the full spectrum of systematic '
        'signal types available to a discretionary portfolio manager.',
        s['body']),
    sp(10),
]

# ── SECTION 2 ─────────────────────────────────────────────────────────────────
story += [
    p('2. THE SIX INDICATORS', s['wp_section']), hrm(),
    p('What each indicator measures, how it is parameterised, and what price behaviour it is designed to detect.', s['body_grey']),
    p('<b>Simple Moving Average (SMA)</b>', s['wp_sub']),
    p('Crossover of a short-term and long-term moving average. Generates a buy signal when the short average '
      'crosses above the long, and a sell signal on the reverse. Best suited to instruments with persistent '
      'trending behaviour. Optimised parameters: Short period 10\u201330 days \u00b7 Long period 40\u201380 days.', s['body']),
    p('<b>Exponential Moving Average (EMA)</b>', s['wp_sub']),
    p('Identical structure to SMA but applies exponentially greater weight to recent prices, making it more '
      'responsive to current market conditions. Better suited to instruments with trend reversals or regime '
      'changes. Optimised parameters: Short period 10\u201330 days \u00b7 Long period 40\u201380 days.', s['body']),
    p('<b>MACD</b>', s['wp_sub']),
    p('Momentum indicator using the convergence and divergence of two EMAs. Generates signals when the MACD '
      'line crosses its signal line. Effective for instruments with cyclical momentum patterns. Optimised '
      'parameters: Short EMA 5\u201320 \u00b7 Long EMA 20\u201350 \u00b7 Signal 5\u201315.', s['body']),
    p('<b>Bollinger Bands (BB)</b>', s['wp_sub']),
    p('Volatility-based bands set at standard deviations around a moving average. Generates signals when price '
      'breaks out of or returns to the bands. Suited to instruments with periodic volatility expansions. '
      'Optimised parameters: SMA period 10\u201330 \u00b7 Standard deviations 1\u20133.', s['body']),
    p('<b>Relative Strength Index (RSI)</b>', s['wp_sub']),
    p('Momentum oscillator measuring the speed and magnitude of price movements. Generates signals at '
      'overbought and oversold thresholds. Suited to instruments with clear mean-reverting tendencies. '
      'Optimised parameters: Period 10\u201320 \u00b7 Upper threshold 60\u201380 \u00b7 Lower threshold 20\u201340.', s['body']),
    p('<b>Stochastic Oscillator (SO)</b>', s['wp_sub']),
    p('Compares the closing price to the price range over a look-back period. Generates signals at extremes '
      'of the range. Similar in intent to RSI but with different sensitivity characteristics. Optimised '
      'parameters: Period 10\u201320 \u00b7 %D smoothing 2\u20135.', s['body']),
    PageBreak(), sp(0),
]

# ── SECTION 3 ─────────────────────────────────────────────────────────────────
story += [
    p('3. THE GRID SEARCH METHODOLOGY', s['wp_section']), hrm(),
    p('How Vektor searches the full parameter space for each indicator and each instrument.', s['body_grey']),
    p('For each instrument in the portfolio and each of the six indicators, Vektor executes a full grid search '
      'across the indicator\u2019s parameter space. The grid search tests every combination of parameter values '
      'within the defined ranges. Each combination is backtested against three years of daily price data and '
      'the annualised Sharpe ratio is calculated. The Sharpe ratio is selected because it simultaneously '
      'captures both the return and the risk of the signal\u2019s performance.', s['body']),
    p('<b>Step 1</b> \u2014 Define parameter grid: the full range of valid parameter combinations is enumerated for each indicator.', s['bullet']),
    p('<b>Step 2</b> \u2014 Backtest each configuration: applied to three years of daily OHLCV price data, generating buy/sell signals and performance statistics.', s['bullet']),
    p('<b>Step 3</b> \u2014 Calculate annualised Sharpe ratio for each configuration.', s['bullet']),
    p('<b>Step 4</b> \u2014 Select highest-Sharpe configuration as the winner for that instrument.', s['bullet']),
    p('<b>Step 5</b> \u2014 Repeat for all six indicators; the indicator with the highest Sharpe across all six is assigned.', s['bullet']),
    p('<b>Step 6</b> \u2014 Save to strategy record: indicator name, optimised parameters, and backtest Sharpe ratio \u2014 fully visible to the portfolio manager before any trade approval.', s['bullet']),
    sp(10),
]
for item in sc('sc04_strategy.png',
    'SGP Equity Strategy \u2014 admin portal. Each instrument shows its assigned indicator (BB, MACD, SMA, EMA) '
    'alongside its allocation weight and optimisation status.'):
    story.append(item)
story.append(sp(10))
story.append(PageBreak())
story.append(sp(0))

# ── SECTION 4 ─────────────────────────────────────────────────────────────────
story += [
    p('4. XGBOOST SIGNAL VALIDATION', s['wp_section']), hrm(),
    p('Why a second validation layer is necessary \u2014 and how XGBoost provides it.', s['body_grey']),
    p('The grid search selects the optimal historical configuration for each instrument. But a signal that '
      'performed well in backtest is not guaranteed to be valid at the moment of execution. Market regimes '
      'change. A historically strong MACD signal may be generated during a period of low liquidity, unusual '
      'volatility, or data quality issues. The XGBoost layer addresses this by providing real-time validation '
      'of every live signal before it reaches the execution layer.', s['body']),
    p('XGBoost (Extreme Gradient Boosting) is a machine learning classification model trained on historical '
      'signal outcomes \u2014 specifically, whether a signal generated by the selected indicator in similar '
      'market conditions historically produced a positive outcome. The model outputs a confidence score for '
      'each live signal. Signals below the confidence threshold are filtered out before execution, preventing '
      'the system from acting on historically weak signals even if the indicator technically generated them.', s['body']),
    NoteBox(COL_W,
        'Two layers of rigour: the grid search optimises the signal for the instrument\u2019s historical '
        'behaviour. XGBoost validates the signal against current market conditions. Neither layer alone is '
        'sufficient \u2014 together they provide the systematic edge that neither a single indicator nor a '
        'pure ML model would achieve independently.',
        s['body']),
    sp(10),
]

# ── SECTION 5 ─────────────────────────────────────────────────────────────────
story += [
    p('5. TRANSPARENCY AND AUDITABILITY', s['wp_section']), hrm(),
    p('Every signal selection decision is recorded, visible, and explainable.', s['body_grey']),
    p('A portfolio manager using Vektor can examine, for every holding in every strategy: which indicator was '
      'selected and why, what parameters were optimised, what backtest Sharpe ratio justified the selection, '
      'and whether the XGBoost layer validated the most recent live signal. Nothing is a black box. If a '
      'position cannot be explained, the system has failed \u2014 and Vektor is built so that failure cannot '
      'happen silently.', s['body']),
]

# ── SECTION 6 — CONCLUSION ────────────────────────────────────────────────────
story += [
    p('6. CONCLUSION', s['wp_section']), hrm(),
    p('Per-instrument signal optimisation is not a marginal improvement over universal signal strategies \u2014 '
      'it is a structural change in how systematic signals are applied.', s['body_grey']),
    p('By searching the full parameter space for each of six indicators across every instrument, and validating '
      'every live signal through an XGBoost layer, Vektor ensures that each position in the portfolio is driven '
      'by the signal that actually works for that specific instrument \u2014 not the signal that works on average. '
      'In a ten-stock portfolio, the difference between an optimised per-instrument signal and a universal '
      'signal is the difference between a systematic edge and a systematic compromise.', s['body']),
    NoteBox(COL_W,
        'Each position in the portfolio is driven by the indicator that actually works for that instrument '
        '\u2014 not the one that performs best on average. That is the systematic edge per-instrument '
        'optimisation produces: not a marginal improvement, but a structural change in how every signal '
        'in the portfolio is selected.',
        s['pull'], bg=CARD_BG, bar=GOLD),
]
closing_row(
    'This paper describes Step 04 of the Vektor eleven-step workflow. For the full portfolio construction '
    'methodology, see WP-01: Quantitative Portfolio Construction. For the commercial case, see Why Vektor. '
    'All documents available at investpuppy.com.',
    REF, s, story)

doc.build(story)
sz = os.path.getsize(OUT)
print(f'Built: {OUT}')
print(f'Size:  {sz:,} bytes ({sz//1024}KB)')
