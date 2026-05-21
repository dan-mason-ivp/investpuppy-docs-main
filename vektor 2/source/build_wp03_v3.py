"""
WP-03: Capital Allocation Precision — corrected rebuild.
Corrections applied:
  - 99.9% → 99.94% throughout (all 6 body instances)
  - SGD 999 → SGD 999.40, SGD 1 residual → SGD 0.60
  - Section 5 heading: "How 99.9% efficiency" → "How 99.94% efficiency"
  - Cover distillation: 99.9% → 99.94%
  - Footer: "InvestPuppy Research Series 2026" → "VEKTOR RESEARCH SERIES · 2026"
"""
import os as _os
_SCRIPT_DIR  = _os.path.dirname(_os.path.abspath(__file__))
_REPO_ROOT   = _os.path.dirname(_os.path.dirname(_SCRIPT_DIR))
_LOGOS       = _os.path.join(_REPO_ROOT, '_shared', 'logos')
_SCREENSHOTS = _os.path.join(_SCRIPT_DIR, 'screenshots')

import sys; sys.path.insert(0, '/home/claude')
from wp_builder_v3 import *
from reportlab.platypus import PageBreak, NextPageTemplate

OUT = '/home/claude/investpuppy/vektor/output/pdf/vk5-wp03-capital-allocation.pdf'
SUBTITLE = 'Capital Allocation Precision'
REF = 'IP-WP-CAP-260501-1.0'
SC = _os.path.join(_SCREENSHOTS, 'sc06_allocation.png')


def build():
    draw_cover = make_cover_fn(
        ['Capital Allocation', 'Precision', 'From Weights to Positions'],
        # CORRECTED: 99.94%
        ['How Vektor translates percentage weights into actual share quantities at live prices',
         '\u2014 and why 99.94% capital allocation efficiency is achievable and measurable.'],
        'For professional and institutional investors', REF)
    draw_page = make_page_fn(SUBTITLE)

    doc, f_cov, f_fst, f_lat = make_doc(OUT, SUBTITLE)
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[f_cov], onPage=draw_cover),
        PageTemplate(id='Later', frames=[f_lat], onPage=draw_page),
    ])
    s = make_styles()
    story = [sp(1), NextPageTemplate('Later'), PageBreak()]

    # ── ABSTRACT + KEY TAKEAWAYS ──────────────────────────────────────────────
    story += [
        p('ABSTRACT', s['tag']),
        NoteBox(COL_W,
            "99.94% capital allocation efficiency is not an estimate. "
            "This paper shows exactly how it is calculated, why the gap it eliminates compounds over time, "
            "and what it costs to ignore it. "
            "Translating portfolio weights into executable share quantities is a problem every discretionary "
            "portfolio manager faces \u2014 and most solve it imprecisely. The gap between a target percentage "
            "weight and the actual capital deployed is not a rounding error to be ignored. It is measurable, "
            "recurring, and compounding drag on portfolio performance. This paper describes Vektor\u2019s "
            "weight-to-position translation engine: how live market prices are fetched, how lot size rounding is "
            "applied, how a configurable cash buffer is reserved, and how 99.94% capital allocation efficiency is "
            "achieved and verified on every strategy execution.", s['body']),
        sp(10),
        key_takeaways_box([
            'The gap between a target percentage weight and actual deployed capital is measurable drag \u2014 typically 0.5\u20133% for manually calculated allocations.',
            'Live market prices at execution time, not estimated prices, are the only correct basis for weight-to-share translation.',
            'Exchange lot size constraints require explicit rounding logic \u2014 ignoring them produces unexecutable orders.',
            'A configurable cash buffer handles fees and slippage without distorting weights.',
            # CORRECTED
            'Vektor achieves 99.94% capital allocation efficiency \u2014 verified on every execution.',
        ], s),
        sp(10),
        p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {REF}  \u00b7  Copyright 2026 InvestPuppy', s['wp_ref']),
        PageBreak(), sp(0),
    ]

    # ── SECTION 1 ────────────────────────────────────────────────────────────
    story += [
        p('1. THE WEIGHT-TO-POSITION PROBLEM', s['wp_section']), hrm(),
        p('Why percentage weights and actual share positions are not the same thing \u2014 and why the difference matters.', s['body_grey']),
        p('A portfolio optimisation algorithm produces percentage weights: 36.1% to instrument A, 26.5% to instrument B, '
          'and so on. These weights are mathematically precise but operationally abstract. To deploy capital, a portfolio '
          'manager must convert them into actual share quantities \u2014 a process that introduces three sources of '
          'imprecision: price uncertainty (the price at weight calculation differs from the price at execution), lot size '
          'constraints (exchanges require purchases in minimum lot sizes), and fee and slippage reserves (some capital '
          'must be withheld to cover transaction costs). Each source of imprecision reduces the correspondence between '
          'target allocation and actual deployed capital.', s['body']),
        NoteBox(COL_W,
            'In a SGD 500,000 mandate with ten holdings, a 1% allocation gap represents SGD 5,000 of uninvested capital '
            'per execution cycle. Across a year of quarterly rebalancing, the compounding effect of consistently '
            'underdeployed capital is a measurable drag on performance \u2014 one that systematic precision eliminates.',
            s['body']),
        sp(10),
    ]

    # ── SECTION 2 ────────────────────────────────────────────────────────────
    story += [
        p('2. LIVE PRICE FETCHING', s['wp_section']), hrm(),
        p('Why execution-time prices are the only correct basis for weight-to-position translation.', s['body_grey']),
        p('The most common source of allocation imprecision is using stale prices. A weight calculated at market close on '
          'Tuesday and executed at market open on Wednesday will produce a different share quantity at the same '
          'allocation percentage \u2014 because the price has changed. Using the price at weight calculation time rather '
          'than execution time systematically underallocates or overallocates depending on whether prices have risen or '
          'fallen overnight. Vektor fetches live market prices at the moment of allocation calculation \u2014 not the '
          'prices used during optimisation, and not the previous close. The allocation engine makes a real-time call to '
          'the instrument service immediately before calculating share quantities, ensuring that the translation uses the '
          'price at which the orders will actually be executed.', s['body']),
    ]

    # ── SECTION 3 ────────────────────────────────────────────────────────────
    story += [
        p('3. LOT SIZE ROUNDING', s['wp_section']), hrm(),
        p('How exchange microstructure constraints are handled without distorting weights.', s['body_grey']),
        p('Most exchanges require securities to be purchased in minimum lot sizes. On SGX, the standard board lot is 100 '
          'shares. A weight-to-position calculation that produces 214,350 shares must be rounded to 214,300 or 214,400 '
          '\u2014 and the choice of rounding direction affects both the deployed capital and the cash reserve. Vektor '
          'applies floor rounding \u2014 always rounding down to the nearest lot \u2014 to ensure the allocated capital '
          'never exceeds the available capital. The residual from rounding joins the cash buffer.', s['body']),
        p('Lot sizes are configurable per market. SGX uses 100-share board lots. Other exchanges have different '
          'conventions \u2014 some use 1-share lots, others use fixed capital minimums. Vektor\u2019s allocation engine '
          'applies the correct lot size rule for each configured exchange without manual intervention.', s['body']),
        sp(6),
    ]

    # ── SCREENSHOT CARD ───────────────────────────────────────────────────────
    class ScreenshotCard(Flowable):
        def __init__(self, w, img_path, caption, label='PLATFORM INTERFACE'):
            Flowable.__init__(self); self._w=w; self._img=img_path
            self._cap=caption; self._lbl=label; self._pad=10; self._lbl_h=16
        def wrap(self, aw, ah):
            from reportlab.lib.utils import ImageReader
            img=ImageReader(self._img); iw,ih=img.getSize()
            inner_w=self._w-self._pad*2
            scale=min(inner_w/iw, (ah*0.55)/ih)
            self._ih=ih*scale; self._iw=iw*scale
            cap_p=Paragraph(self._cap, s['body_grey'])
            _, ch=cap_p.wrap(inner_w, ah); self._cap_h=ch; self._cap_p=cap_p
            self.height=self._pad+self._lbl_h+self._ih+6+ch+self._pad
            return self._w, self.height
        def draw(self):
            c=self.canv; c.saveState()
            c.setFillColor(CARD_BG); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
            c.roundRect(0,0,self._w,self.height,3,fill=1,stroke=1)
            c.setFont('Helvetica',7); c.setFillColor(WARM_GREY)
            c.drawString(self._pad, self.height-self._pad-8, self._lbl)
            img_x=self._pad+(self._w-self._pad*2-self._iw)/2
            img_y=self.height-self._pad-self._lbl_h-self._ih
            c.drawImage(self._img, img_x, img_y, self._iw, self._ih, preserveAspectRatio=True)
            self._cap_p.wrap(self._w-self._pad*2, 100)
            self._cap_p.drawOn(c, self._pad, self._pad)
            c.restoreState()

    story.append(ScreenshotCard(COL_W, SC,
        'Asset allocation breakdown \u2014 SGD 500,000 mandate. SGD 474,712 allocated across seven active '
        'positions at live prices. Cash reserve: SGD 25,288 (5% buffer). Total efficiency: 99.94%.'))
    story.append(sp(10))

    # ── SECTION 4 ────────────────────────────────────────────────────────────
    story += [
        p('4. THE CASH BUFFER', s['wp_section']), hrm(),
        p('How fees and slippage are reserved without distorting portfolio weights.', s['body_grey']),
        p('A configurable percentage of the total mandate capital is set aside before allocation calculations begin. '
          'In the example above, a 5% cash reserve (SGD 25,000) is withheld from a SGD 500,000 mandate, leaving '
          'SGD 475,000 as available capital. The allocation engine then applies weights to the available capital '
          'rather than the total mandate \u2014 ensuring that fee and slippage costs do not force partial liquidation '
          'of positions after execution. The buffer percentage is configurable per mandate and per strategy.', s['body']),
        PageBreak(), sp(0),
    ]

    # ── SECTION 5 ────────────────────────────────────────────────────────────
    # CORRECTED: section heading and all 99.9% instances
    story += [
        p('5. MEASURING ALLOCATION EFFICIENCY', s['wp_section']), hrm(),
        # CORRECTED heading
        p('How 99.94% efficiency is calculated and what it means in practice.', s['body_grey']),
        p('Capital allocation efficiency is defined as: total allocated capital divided by total available capital '
          '(after cash buffer). In the SGD 500,000 example: available capital SGD 475,000, allocated capital '
          'SGD 474,712, efficiency 99.94%. The residual SGD 288 represents the aggregate effect of lot size '
          'rounding across all seven active positions \u2014 the irreducible minimum of integer lot sizing, '
          'reduced to its theoretical floor by the allocation engine.', s['body']),
        # CORRECTED: 99.9% → 99.94%, SGD 999 → SGD 999.40, SGD 1 → SGD 0.60
        NoteBox(COL_W,
            '99.94% efficiency means that for every SGD 1,000 of available capital, SGD 999.40 is productively '
            'deployed in the portfolio. The SGD 0.60 residual from lot rounding sits in cash. For a manually '
            'calculated allocation, the equivalent figure is typically SGD 980\u2013995 \u2014 a difference that '
            'compounds materially across a multi-year investment horizon.', s['body']),
        sp(10),
    ]

    # ── SECTION 6 ────────────────────────────────────────────────────────────
    # CORRECTED: "99.9% capital allocation efficiency" → "99.94%"
    story += [
        p('6. CONCLUSION', s['wp_section']), hrm(),
        p('Precision in weight-to-position translation is not an operational detail. It is a source of systematic performance drag that can be eliminated.', s['body_grey']),
        p('By fetching live prices at execution time, applying exchange-specific lot size rounding, reserving a '
          'configurable cash buffer, and measuring efficiency on every execution, Vektor eliminates the allocation '
          'gap that affects manually calculated portfolios. The result \u2014 99.94% capital allocation efficiency '
          '\u2014 is not aspirational. It is verified on every strategy, for every client, in every configured market.',
          s['body']),
    ]

    closing_row(
        'This paper describes Steps 07\u201308 of the Vektor eleven-step workflow. For the full portfolio construction '
        'methodology, see WP-01. For per-instrument signal selection, see WP-02. All documents available at investpuppy.com.',
        REF, s, story)

    doc.build(story)
    print(f'Built: {OUT}')
    import subprocess
    r = subprocess.run(['pdfinfo', OUT], capture_output=True, text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l: print(l)

if __name__ == '__main__': build()
