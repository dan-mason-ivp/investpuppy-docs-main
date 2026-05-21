"""WP-06: Audit Trail & Compliance Architecture — vk5 build."""
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

OUT      = '/home/claude/investpuppy/vektor/output/pdf/vk5-wp06-audit-compliance.pdf'
SUBTITLE = 'Audit Trail & Compliance Architecture'
REF      = 'IP-WP-AUD-260501-1.0'
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
    ['Audit Trail &', 'Compliance', 'Architecture'],
    ["How Vektor's three-role accountability structure, complete action logging,",
     'and transparent methodology support institutional compliance requirements.'],
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

# ── ABSTRACT — already has strong InvestPuppy voice ────────────────────────────
story += [
    p('ABSTRACT', s['tag']),
    NoteBox(COL_W,
        'Systematic portfolio management platforms are frequently described as black boxes by institutional '
        'compliance reviewers \u2014 algorithms that make decisions without producing the documentation that '
        'compliance frameworks require. Vektor is designed specifically to invert this. This paper describes '
        'the platform\u2019s three-role accountability architecture, its complete action logging across every '
        'stage of the investment workflow, and the compliance-ready audit trail that is produced automatically '
        'as a by-product of normal platform operation \u2014 not as a separately maintained compliance process.',
        s['body']),
    sp(10),
    key_takeaways_box([
        'Three distinct user roles \u2014 Stock Analyst, Portfolio Manager, Operations \u2014 with defined scopes and separate approval gates at each stage.',
        'Every action across strategy creation, client onboarding, allocation, cash funding, and trade preparation is logged with timestamp and user identity.',
        'No position can be established without explicit portfolio manager approval of the complete strategy \u2014 instruments, weights, indicators, and Sharpe ratios.',
        'The methodology is transparent by design: every signal, every weight, and every backtest result is visible and explainable before execution.',
        'Cash movements carry a full audit trail \u2014 currency, amount, date, reference \u2014 ready for compliance review at any point.',
    ], s),
    sp(10),
    p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {REF}  \u00b7  Copyright 2026 InvestPuppy', s['wp_ref']),
    sp(8),
    p('Regulatory standing: Vektor is a portfolio construction and management platform. Regulatory '
      'status, applicable jurisdiction, and permissions relevant to specific use cases are not '
      'disclosed in this document. Full details are available to Proof Partners as part '
      'of the due diligence process.', s['body_grey']),
    PageBreak(), sp(0),
]

# ── SECTION 1 ─────────────────────────────────────────────────────────────────
story += [
    p('1. THE COMPLIANCE PROBLEM WITH SYSTEMATIC PLATFORMS', s['wp_section']), hrm(),
    p('Why most systematic portfolio platforms fail institutional compliance review.', s['body_grey']),
    p('A systematic platform that produces a portfolio allocation without a complete record of how that '
      'allocation was generated creates a compliance gap. Compliance reviewers require evidence that '
      'investment decisions were made within defined parameters, that approval gates were observed, that '
      'client mandates were applied correctly, and that the full chain of events from research to execution '
      'is documented and retrievable. Most systematic platforms produce a result \u2014 the allocation '
      '\u2014 without the documentation chain that compliance frameworks require.', s['body']),
    p('Vektor is designed so that the compliance documentation is a natural output of normal platform '
      'operation. Every action required to create and execute a strategy produces a log entry. The audit '
      'trail is not maintained separately \u2014 it is the platform\u2019s operational record.', s['body']),
]

# ── SECTION 2 ─────────────────────────────────────────────────────────────────
story += [
    p('2. THE THREE-ROLE ARCHITECTURE', s['wp_section']), hrm(),
    p('How accountability is separated across Stock Analyst, Portfolio Manager, and Operations \u2014 and why each boundary matters.', s['body_grey']),
    p('<b>Stock Analyst</b>', s['wp_sub']),
    p('The Stock Analyst role is responsible for research and strategy construction: screening the investable '
      'universe, running portfolio optimisation, selecting per-instrument signals, and producing a fully '
      'specified strategy. The Analyst cannot approve a strategy for client assignment \u2014 this requires '
      'a separate Portfolio Manager review. The separation ensures that the person who builds the strategy '
      'is not the same person who commits client capital to it.', s['body']),
    p('Scope: universe screening, portfolio optimisation, signal selection, strategy specification.', s['body_grey']),
    p('<b>Portfolio Manager</b>', s['wp_sub']),
    p('The Portfolio Manager role is responsible for strategy review and approval, client onboarding, and '
      'allocation execution. The PM reviews the complete strategy \u2014 instruments, weights, indicators, '
      'backtest Sharpe ratios \u2014 before approving it for client assignment. Once approved, the PM creates '
      'the client profile, links the strategy, and initiates the allocation calculation. The PM cannot fund '
      'the cash account \u2014 this requires Operations.', s['body']),
    p('Scope: strategy approval, client creation, portfolio setup, allocation execution.', s['body_grey']),
    p('<b>Operations</b>', s['wp_sub']),
    p('The Operations role is responsible for cash account management \u2014 recording deposits, verifying '
      'funding, and maintaining the cash movement audit trail. Operations cannot create strategies or approve '
      'allocations. The separation ensures that the person controlling cash movements is independent of the '
      'investment decision chain.', s['body']),
    p('Scope: cash account creation, deposit recording, audit trail maintenance.', s['body_grey']),
    PageBreak(), sp(0),
]

# ── SECTION 3 ─────────────────────────────────────────────────────────────────
story += [
    p('3. WHAT IS LOGGED AND WHEN', s['wp_section']), hrm(),
    p('A complete record of every action across the eleven-step workflow.', s['body_grey']),
    p('<b>Strategy creation:</b> Analyst ID, strategy name, universe specification, screening parameters, '
      'optimisation result, per-instrument signal assignments, backtest Sharpe ratios. Timestamp.', s['body']),
    p('<b>Strategy approval:</b> PM ID, strategy ID, approval status, review timestamp. No position can be '
      'assigned to a client before this record exists.', s['body']),
    p('<b>Client creation:</b> PM ID, client name, type, risk profile, base currency, KYC status. Timestamp.', s['body']),
    p('<b>Portfolio creation:</b> PM ID, portfolio ID, client linkage, assigned strategy, configured capital. Timestamp.', s['body']),
    p('<b>Allocation calculation:</b> PM ID, portfolio ID, live prices fetched, weight-to-share calculations, '
      'lot size rounding applied, cash buffer reserved, efficiency percentage. Timestamp.', s['body']),
    p('<b>Cash deposit:</b> Operations ID, portfolio ID, currency, amount, wire reference, resulting cash balance. Timestamp.', s['body']),
    p('<b>Market data refresh:</b> Instrument count updated, price history extended, FX rates updated. '
      'Timestamp. Automatic \u2014 no manual action required.', s['body']),
    sp(10),
]
for item in sc('sc04_strategy.png',
    'Strategy review \u2014 full instrument list with weights, indicators, optimisation status, and creation date. '
    'Portfolio Manager approves this view before any client assignment proceeds.'):
    story.append(item)
story.append(sp(8))
for item in sc('sc08_cash.png',
    'Cash movements audit trail \u2014 SGD 500,000 deposit recorded with date, type, amount, and reference. '
    'Every cash movement is logged and retrievable.'):
    story.append(item)
story.append(sp(8))
for item in sc('sc18_order_detail.png',
    'Order lifecycle timeline \u2014 CREATED and QUEUED states with timestamps. '
    'Every order is traceable from generation through execution, with sub-second precision.'):
    story.append(item)
story.append(sp(10))
story.append(PageBreak())
story.append(sp(0))

# ── SECTION 4 ─────────────────────────────────────────────────────────────────
story += [
    p('4. TRANSPARENCY AS A COMPLIANCE PROPERTY', s['wp_section']), hrm(),
    p('Why a transparent methodology is a compliance asset \u2014 not just a design choice.', s['body_grey']),
    p('A compliance reviewer examining a position in a Vektor portfolio can trace the complete decision chain: '
      'which analyst created the strategy and when, which universe screening parameters were applied, which '
      'optimisation run produced the weights, which indicator was assigned to the position and why, which '
      'portfolio manager approved the strategy and when, how the share quantity was calculated, and what cash '
      'was available at the time of allocation. No step in this chain is invisible or requires reconstruction '
      'from memory.', s['body']),
    p('This transparency is not retrofitted compliance documentation \u2014 it is the natural output of a '
      'platform designed so that the documentation cannot be absent. If a portfolio manager cannot explain '
      'why a position was included, the system has failed. Vektor is built so that failure cannot happen '
      'silently.', s['body']),
]

# ── SECTION 5 ─────────────────────────────────────────────────────────────────
story += [
    p('5. WHAT IS NOT YET IN SCOPE', s['wp_section']), hrm(),
    p('Honesty about the current compliance scope \u2014 and what is on the roadmap.', s['body_grey']),
    p('The current platform covers the pre-trade compliance workflow: strategy creation, approval, allocation, '
      'and cash management. Post-trade compliance \u2014 real-time position monitoring, automated breach '
      'detection, regulatory reporting \u2014 is on the near-term roadmap alongside direct trade execution. '
      'The current platform produces a trade-ready position set with a complete pre-trade audit trail; the '
      'post-trade audit trail will be completed as execution capability is added.', s['body']),
    NoteBox(COL_W,
        'The absence of post-trade automation does not diminish the value of the pre-trade audit trail '
        '\u2014 it is complete for the workflow that is currently live. Sophistication without candour is '
        'not a sales argument. This is the platform as it exists today, and what it is becoming.',
        s['body']),
    sp(6),
    sp(10),
]

# ── SECTION 6 — CONCLUSION ────────────────────────────────────────────────────
story += [
    p('6. CONCLUSION', s['wp_section']), hrm(),
    p('Compliance documentation should be a by-product of correct platform operation \u2014 not a separately maintained process.', s['body_grey']),
    p('Vektor\u2019s three-role accountability architecture and complete action logging produce an '
      'institutional-grade audit trail as a natural consequence of using the platform correctly. No '
      'additional compliance workflow is required. Every investment decision is documented, every approval '
      'is recorded, every cash movement is logged, and the complete chain from research to trade-ready '
      'position is retrievable at any point.', s['body']),
    NoteBox(COL_W,
        'A compliance reviewer who reads this paper should finish it knowing exactly what Vektor produces '
        'at every stage of the workflow \u2014 and exactly what they would find in an audit. '
        'That is the point.',
        s['pull'], bg=CARD_BG, bar=GOLD),
]
closing_row(
    'This paper describes the compliance and audit architecture embedded across all eleven steps of the '
    'Vektor workflow. For the full platform overview, see the Platform Brochure. For portfolio construction '
    'methodology, see WP-01. All documents available at investpuppy.com.',
    REF, s, story)

doc.build(story)
sz = os.path.getsize(OUT)
print(f'Built: {OUT}')
print(f'Size:  {sz:,} bytes ({sz//1024}KB)')
