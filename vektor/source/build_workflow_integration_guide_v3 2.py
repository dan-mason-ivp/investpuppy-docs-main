"""
Vektor Workflow Integration Guide — vk5 build script.
Dark-theme ReportLab PDF matching the suite visual standard exactly.
Cover: VEKTOR wordmark centred + InvestPuppy maker mark bottom-left.
Header: VEKTOR logo left + document title/page right + rule.
Footer: InvestPuppy 32mm bottom-left + investpuppy.com right.
"""
import os as _os
_SCRIPT_DIR  = _os.path.dirname(_os.path.abspath(__file__))
_REPO_ROOT   = _os.path.dirname(_os.path.dirname(_SCRIPT_DIR))
_LOGOS       = _os.path.join(_REPO_ROOT, '_shared', 'logos')
_SCREENSHOTS = _os.path.join(_SCRIPT_DIR, 'screenshots')

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
    PageBreak, NextPageTemplate,
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.utils import ImageReader
import os

BG        = colors.HexColor('#0A0A0F')
PLATINUM  = colors.HexColor('#E8E8EC')
GOLD      = colors.HexColor('#C8A96E')
OFF_WHITE = colors.HexColor('#E8E2D9')
WARM_GREY = colors.HexColor('#9A9086')
RULE_MAJ  = colors.HexColor('#5A5A60')
RULE_MIN  = colors.HexColor('#2A2828')
CARD_BG   = colors.HexColor('#111116')
NOTE_BG   = colors.HexColor('#16161A')
CARD_EDGE = colors.HexColor('#242428')

W, H         = A4
ML = MR      = 22*mm
MT1          = 16*mm
MT2          = 46*mm
MB           = 20*mm
LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png')
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')
IP_H_RATIO   = 2.337
DATE         = 'May 2026'
REF          = 'IP-WIG-260501-1.0'
SUB          = 'Workflow Integration Guide'
OUT          = '/home/claude/investpuppy/vektor/output/pdf/vk5-workflow-integration-guide.pdf'
COL_W        = W - ML - MR


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    try:
        img = ImageReader(LOGO); iw, ih = img.getSize()
        lw = min(W * 0.72, 340); lh = lw * ih / iw
        lx = (W - lw) / 2;       ly = H * 0.56
        canvas.drawImage(LOGO, lx, ly - lh, lw, lh, mask='auto', preserveAspectRatio=True)
        ry = ly - lh - 8
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8)
        canvas.line(ML, ry, W - MR, ry)
        canvas.setFont('Helvetica-Bold', 7); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2, ry - 13, 'WORKFLOW INTEGRATION GUIDE')
        canvas.setFont('Helvetica-Bold', 26); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2, ry - 46, 'Workflow')
        canvas.drawCentredString(W/2, ry - 76, 'Integration Guide')
        canvas.setFont('Helvetica', 10); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2, ry - 104,
            'What it replaces, what it augments, and what stays exactly as it is.')
    except Exception as e:
        print(f'Cover VEKTOR error: {e}')
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4)
    canvas.line(ML, 36*mm, W - MR, 36*mm)
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(WARM_GREY)
    canvas.drawCentredString(W/2, 28*mm,
        'For DPMs and portfolio managers evaluating Vektor alongside existing infrastructure')
    canvas.setFont('Helvetica', 7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W/2, 19*mm, REF)
    canvas.drawCentredString(W/2, 11*mm, DATE)
    try:
        ip_w = 38*mm; ip_h = ip_w / IP_H_RATIO
        canvas.drawImage(IP_H, ML, 9*mm, ip_w, ip_h, mask='auto', preserveAspectRatio=True)
    except Exception as e:
        print(f'Cover IP error: {e}')
    canvas.restoreState()


def _hdr(canvas, doc):
    hy = H - MT2 + 14
    try:
        img = ImageReader(LOGO); iw, ih = img.getSize()
        lh = 22; lw = lh * iw / ih
        canvas.drawImage(LOGO, ML, hy, lw, lh, mask='auto', preserveAspectRatio=True)
    except Exception:
        pass
    canvas.setFont('Helvetica', 7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawRightString(W - MR, H - MT2 + 18, f'{SUB}  \u00b7  {doc.page - 1:02d}')
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.4)
    canvas.line(ML, H - MT2 + 8, W - MR, H - MT2 + 8)


def _ftr(canvas):
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.3)
    canvas.line(ML, MB - 2, W - MR, MB - 2)
    try:
        ip_w = 32*mm; ip_h = ip_w / IP_H_RATIO
        canvas.drawImage(IP_H, ML, 1.0*mm, ip_w, ip_h, mask='auto', preserveAspectRatio=True)
    except Exception as e:
        print(f'Footer IP error: {e}')
    canvas.setFont('Helvetica', 6.5); canvas.setFillColor(colors.HexColor('#444440'))
    fy = 1.0*mm + (32*mm / IP_H_RATIO) / 2 - 2.5
    canvas.drawRightString(W - MR, fy, f'investpuppy.com  \u00b7  {DATE}')


def draw_first(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0, 0, W, H, fill=1, stroke=0)
    _ftr(canvas)
    canvas.restoreState()


def draw_later(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0, 0, W, H, fill=1, stroke=0)
    _hdr(canvas, doc); _ftr(canvas)
    canvas.restoreState()


class HRule(Flowable):
    def __init__(self, w, c=RULE_MIN, t=0.5, sa=5, sb=5):
        Flowable.__init__(self)
        self.rw=w; self.c=c; self.t=t; self._sa=sa; self._sb=sb
        self.height=sa+t+sb
    def wrap(self, aw, ah): return self.rw, self.height
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        self.canv.line(0, self._sb+self.t/2, self.rw, self._sb+self.t/2)


class NoteBox(Flowable):
    """Gold-left-bar callout block for high-importance passages."""
    def __init__(self, w, text, style):
        Flowable.__init__(self)
        self._w = w; self._p = Paragraph(text, style)
        self._ph = 16; self._pv = 14; self._bw = 4
        self._iw = w - self._bw - self._ph * 2
    def wrap(self, aw, ah):
        _, h = self._p.wrap(self._iw, ah)
        self.height = h + self._pv * 2
        return self._w, self.height
    def draw(self):
        c = self.canv; c.saveState()
        c.setFillColor(NOTE_BG); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0, 0, self._w, self.height, 3, fill=1, stroke=1)
        c.setFillColor(GOLD)
        c.roundRect(0, 0, self._bw, self.height, 2, fill=1, stroke=0)
        self._p.wrap(self._iw, self.height)
        self._p.drawOn(c, self._bw + self._ph, self._pv)
        c.restoreState()


def sp(h=6): return Spacer(1, h)


def S():
    s = {}
    s['tag']        = ParagraphStyle('tag', fontName='Helvetica', fontSize=7,
                        textColor=WARM_GREY, leading=11, letterSpacing=4)
    s['num']        = ParagraphStyle('num', fontName='Helvetica-Bold', fontSize=7,
                        textColor=GOLD, leading=10, letterSpacing=2)
    s['section_h']  = ParagraphStyle('sh', fontName='Helvetica-Bold', fontSize=14,
                        textColor=PLATINUM, leading=20, spaceAfter=2)
    s['section_sh'] = ParagraphStyle('ssh', fontName='Helvetica-Oblique', fontSize=9,
                        textColor=WARM_GREY, leading=14, spaceAfter=10)
    s['subhead']    = ParagraphStyle('sub', fontName='Helvetica-Bold', fontSize=9.5,
                        textColor=GOLD, leading=14, spaceAfter=4, spaceBefore=12)
    s['body']       = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5,
                        textColor=OFF_WHITE, leading=16, spaceAfter=8, alignment=TA_JUSTIFY)
    s['body_grey']  = ParagraphStyle('bg', fontName='Helvetica-Oblique', fontSize=9,
                        textColor=WARM_GREY, leading=15, spaceAfter=6)
    s['tbl_hdr']    = ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=8,
                        textColor=PLATINUM, leading=12)
    s['tbl_role']   = ParagraphStyle('tr', fontName='Helvetica-Bold', fontSize=8.5,
                        textColor=GOLD, leading=13)
    s['tbl_body']   = ParagraphStyle('tb', fontName='Helvetica', fontSize=8.5,
                        textColor=OFF_WHITE, leading=13, alignment=TA_JUSTIFY)
    s['wp_ref']     = ParagraphStyle('wr', fontName='Helvetica', fontSize=7.5,
                        textColor=colors.HexColor('#555550'),
                        alignment=TA_CENTER, leading=11)
    return s


def wf_table(rows_data, s):
    cw = [COL_W*0.30, COL_W*0.14, COL_W*0.56]
    hdr = [Paragraph('DPM TASK TODAY', s['tbl_hdr']),
           Paragraph("VEKTOR'S ROLE",  s['tbl_hdr']),
           Paragraph('WHAT CHANGES',   s['tbl_hdr'])]
    rows = [hdr] + [
        [Paragraph(t, s['tbl_body']), Paragraph(r, s['tbl_role']), Paragraph(d, s['tbl_body'])]
        for t, r, d in rows_data
    ]
    tbl = Table(rows, colWidths=cw)
    tbl.setStyle(TableStyle([
        ('BACKGROUND',     (0,0),(-1,0),  CARD_BG),
        ('ROWBACKGROUNDS', (0,1),(-1,-1), [NOTE_BG, CARD_BG]),
        ('TOPPADDING',     (0,0),(-1,-1), 7),
        ('BOTTOMPADDING',  (0,0),(-1,-1), 7),
        ('LEFTPADDING',    (0,0),(-1,-1), 9),
        ('RIGHTPADDING',   (0,0),(-1,-1), 9),
        ('LINEBELOW',      (0,0),(-1,-2), 0.3, RULE_MIN),
        ('BOX',            (0,0),(-1,-1), 0.4, CARD_EDGE),
        ('VALIGN',         (0,0),(-1,-1), 'TOP'),
    ]))
    return tbl


def p(t, st): return Paragraph(t, st)
def hrm(s=None): return HRule(COL_W, RULE_MAJ, 1.0, 4, 6)


doc = BaseDocTemplate(OUT, pagesize=A4,
    leftMargin=ML, rightMargin=MR, topMargin=MT1, bottomMargin=MB,
    title='Vektor Workflow Integration Guide', author='InvestPuppy')
doc.addPageTemplates([
    PageTemplate(id='Cover', frames=[Frame(0,0,W,H,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='cover')], onPage=draw_cover),
    PageTemplate(id='First', frames=[Frame(ML,MB,COL_W,H-MT1-MB,id='first')], onPage=draw_first),
    PageTemplate(id='Later', frames=[Frame(ML,MB,COL_W,H-MT2-MB,id='later')], onPage=draw_later),
])

s = S()
story = []

# Cover — entirely drawn by draw_cover(), just need one blank page
story.append(NextPageTemplate('First'))
story.append(PageBreak())

# Section 1
story.append(NextPageTemplate('Later'))
story.append(p('THE STARTING POINT', s['tag']))
story.append(HRule(COL_W, RULE_MAJ, 1.0, 2, 10))
story.append(p('This document addresses the question that every DPM asks but rarely states '
    'directly: \u2018What does this mean for the way I work today?\u2019 It maps '
    'the typical DPM workflow against the Vektor platform \u2014 task by task \u2014 '
    'and states honestly what Vektor replaces, augments, and leaves unchanged.', s['body']))
story.append(sp(12))
story.append(p('1', s['num'])); story.append(sp(2))
story.append(p('THE WORKFLOW MAP', s['section_h']))
story.append(p('What the typical DPM does today \u2014 and where Vektor sits in that workflow.', s['section_sh']))
story.append(wf_table([
    ('Screen a universe of 500+ stocks manually or via Bloomberg screens', 'Replaces',
     'Vektor runs the screening systematically against configured liquidity, sector, and dividend criteria. Output: a ranked, filtered universe ready for portfolio optimisation.'),
    ('Select portfolio instruments based on research and intuition', 'Augments',
     'The screened universe is the input \u2014 the analyst reviews it and selects the final instruments. Vektor accelerates the screening; the selection remains human.'),
    ('Build a portfolio allocation using Excel or a Bloomberg model', 'Replaces',
     '10,000 portfolio configurations map the efficient frontier; Modern Portfolio Theory identifies the max-Sharpe allocation. Output: a complete weight set with efficient frontier chart and correlation matrix.'),
    ('Select technical indicators and set parameters manually', 'Replaces',
     'Grid search across six indicators per instrument, optimised for Sharpe ratio over a three-year window. XGBoost validated per instrument.'),
    ('Review and approve the portfolio strategy', 'Unchanged',
     'The portfolio manager reviews the complete strategy \u2014 all instruments, weights, indicators, and Sharpe ratios \u2014 and approves. This step is structurally required. It is not faster or slower; it is better-informed.'),
    ('Convert portfolio weights to share quantities', 'Replaces',
     'Allocation calculation at live prices, with lot-size rounding and cash buffer. Output: exact share quantities per instrument.'),
    ('Submit orders to the broker', 'Replaces (when live)',
     'Orders submitted via SQS queue to IBKR Gateway. Currently in simulation mode \u2014 live execution before first Founding Mandate client onboards.'),
    ('Record cash movements and reconcile', 'Augments',
     'Cash funding recorded in the platform with currency, amount, and reference. Reconciliation against custody records remains with Operations.'),
    ('Produce audit trail and compliance documentation', 'Replaces',
     'Every action logged with timestamp and user identity as a by-product of normal platform operation. No separate documentation required.'),
    ('Report to clients on portfolio performance', 'Not yet in scope',
     'Client reporting is on the product roadmap. Performance data available via API and Admin Portal. Formatted client reports are a Founding Mandate roadmap item.'),
], s))
story.append(sp(12))

# Section 2
story.append(p('2', s['num'])); story.append(sp(2))
story.append(p('VEKTOR ALONGSIDE BLOOMBERG', s['section_h']))
story.append(p('The most common existing infrastructure question \u2014 how does Vektor relate to a Bloomberg terminal workflow?', s['section_sh']))
story.append(p(
    'Bloomberg is not one product. It is three distinct products, each with a different relationship to Vektor: '
    'the Bloomberg Terminal, Bloomberg PORT, and Bloomberg data feeds. '
    'Understanding the distinction determines which Vektor entry motion applies.',
    s['body']))

story.append(p('BLOOMBERG TERMINAL \u2014 STAYS', s['subhead']))
story.append(p(
    'The Bloomberg Terminal ($31,980/seat/year in 2026; approximately S$43,000+ SGD) provides price discovery, '
    'news, IB Chat messaging, fixed income coverage, and corporate action monitoring. '
    'Vektor does not compete with the Terminal and does not replace it. '
    'Terminal clients keep their Terminal. All of the above continues unchanged.',
    s['body']))

story.append(p('BLOOMBERG PORT \u2014 DIRECT REPLACEMENT', s['subhead']))
story.append(p(
    'Bloomberg PORT is the portfolio construction and analytics module \u2014 a separate subscription '
    'layered on top of the Terminal, typically adding S$8,000\u2013S$25,000 per seat per year. '
    'PORT is what Vektor replaces, specifically, for listed equity portfolio construction. '
    'A client who cancels PORT and buys Vektor: pays less, retains the Terminal for everything it does well, '
    'and gains systematic construction capability that PORT does not provide in the same accessible form. '
    'The ROI is immediate and calculable.',
    s['body']))

story.append(p('BLOOMBERG DATA FEEDS \u2014 DEVELOPMENT TERMINATION', s['subhead']))
story.append(p(
    'Bloomberg data feeds (B-PIPE and equivalent) are enterprise data agreements used by quantitative teams '
    'consuming market data programmatically for in-house systematic development. '
    'Firms running Bloomberg data feeds to build what Vektor already is are engaged in a build-or-buy '
    'decision. Vektor terminates that decision in favour of buy \u2014 immediately, at lower cost, '
    'and with better systematic construction capability than most in-house builds achieve.',
    s['body']))

story.append(p('WHAT VEKTOR DOES INSTEAD OF BLOOMBERG (ALL CONFIGURATIONS)', s['subhead']))
story.append(p('Universe screening (replacing Bloomberg screen-based filtering). Portfolio optimisation (replacing BOPT or Excel-based optimisation). Technical indicator selection and optimisation. Allocation calculation (replacing Excel-based weight-to-quantity conversion).', s['body']))

story.append(p('DATA SOURCE', s['subhead']))
story.append(p(
    'Vektor uses Yahoo Finance for historical price data as standard. '
    'A DPM requiring Bloomberg-quality data can substitute a Bloomberg data feed as the market data source \u2014 '
    'this is a configuration change, not an architectural change, and is available as a Founding Mandate option. '
    'Note: this is a data feed substitution only. It does not require or imply a Bloomberg Terminal subscription.',
    s['body']))
story.append(HRule(COL_W, RULE_MAJ, 1.0, 4, 6))

# Section 3
story.append(p('3', s['num'])); story.append(sp(2))
story.append(p('VEKTOR ALONGSIDE AN EXISTING PMS', s['section_h']))
story.append(p('For DPMs with an existing Portfolio Management System \u2014 how Vektor connects as the quantitative construction layer.', s['section_sh']))
story.append(p('Vektor is designed to operate as a complement to an existing PMS. The platform produces a trade-ready allocation table \u2014 instruments, target quantities, target values \u2014 via REST API. An existing PMS integration receives this table and processes it through the existing order management and reconciliation workflow.', s['body']))
story.append(p('WHAT THE API DELIVERS', s['subhead']))
story.append(p('A JSON response containing: instrument identifier (ticker + exchange), target quantity (lot-rounded), target value (at calculation price), portfolio weight, and assigned technical indicator. Complete information to raise orders in any order management system.', s['body']))
story.append(p('INTEGRATION EFFORT', s['subhead']))
story.append(p('A standard REST API integration between Vektor\u2019s allocation endpoint and an existing PMS typically takes two to four weeks for a developer familiar with the target PMS. Vektor provides API documentation and integration support as part of Founding Mandate onboarding.', s['body']))
story.append(p('WHAT THE PMS CONTINUES TO HANDLE', s['subhead']))
story.append(p('Order management workflow. Client account reconciliation. Custody interface. Compliance pre-trade screening. Client reporting. All of this continues through the existing PMS \u2014 Vektor is upstream.', s['body']))
story.append(HRule(COL_W, RULE_MAJ, 1.0, 4, 6))
story.append(PageBreak())

# Section 4
story.append(p('4', s['num'])); story.append(sp(2))
story.append(p('THE DPM WITHOUT A PMS', s['section_h']))
story.append(p('For boutique DPMs and family offices managing portfolios in Excel \u2014 what the transition looks like.', s['section_sh']))
story.append(p('Many boutique DPMs and independent family offices manage client portfolios in Excel, with Bloomberg or Yahoo Finance as the data source and manual order entry at the broker. This is the workflow Vektor is most directly designed to upgrade.', s['body']))
story.append(p('WHAT VEKTOR REPLACES IN THIS WORKFLOW', s['subhead']))
story.append(p('The universe screening spreadsheet. The optimisation model. The indicator selection process. The weight-to-quantity calculation. The order list preparation. The audit trail \u2014 if one exists at all.', s['body']))
story.append(p('THE HONEST TRANSITION REALITY', s['subhead']))
story.append(NoteBox(COL_W,
    'Moving from an Excel-based workflow to a systematic platform takes time and '
    'requires a period of parallel running. The portfolio manager\u2019s judgement '
    'does not become redundant \u2014 it becomes better-supported. The Founding '
    'Mandate structure is designed to support this transition: Vektor is configured '
    'around the specific instruments, markets, and client profiles of the founding '
    'firm, not the other way around.',
    ParagraphStyle('note_body', fontName='Helvetica', fontSize=9.5,
        textColor=OFF_WHITE, leading=16)))
story.append(sp(8))
story.append(p('WHAT THE DPM GAINS', s['subhead']))
story.append(p('A systematic, replicable process that produces the same quality of output regardless of time pressure or individual analyst capacity. An audit trail that documents every decision. The ability to manage more client mandates with the same team.', s['body']))
story.append(HRule(COL_W, RULE_MAJ, 1.0, 4, 6))

# Section 5
story.append(p('5', s['num'])); story.append(sp(2))
story.append(p('WHAT VEKTOR DOES NOT REPLACE', s['section_h']))
story.append(p('Important to state clearly.', s['section_sh']))
story.append(p('The portfolio manager\u2019s judgement', s['subhead']))
story.append(p('Vektor produces a systematically optimised strategy recommendation. The portfolio manager reviews it, challenges it, and approves or modifies it. The PM\u2019s understanding of the client, market context, and risk environment is the final filter the platform is designed to support \u2014 not replace.', s['body']))
story.append(p('Client relationships', s['subhead']))
story.append(p('Vektor manages portfolios. It does not manage clients. The relationship between the DPM and the client \u2014 suitability assessment, regular reviews, reporting, communication \u2014 remains entirely with the portfolio manager.', s['body']))
story.append(p('Regulatory compliance', s['subhead']))
story.append(p('Vektor provides the audit trail that supports compliance. Regulatory obligations \u2014 licensing, suitability, reporting \u2014 remain with the operating firm. Vektor is a tool in a regulated firm\u2019s hands, not a substitute for that firm\u2019s regulatory standing.', s['body']))
story.append(p('Fixed income, alternatives, and structured products', s['subhead']))
story.append(p('Vektor is a listed equity platform. A multi-asset DPM continues to use existing tools for non-equity asset classes. Vektor handles the listed equity sleeve.', s['body']))
story.append(sp(16))
story.append(HRule(COL_W, RULE_MAJ, 1.0, 4, 6))
story.append(p('For the technical integration architecture, see WP-07. For the platform workflow in detail, see the Platform Brochure. For risk and limitation disclosure, see WP-09. All documents at investpuppy.com.', s['body_grey']))
story.append(sp(14))
story.append(HRule(COL_W, GOLD, 0.5, 4, 8))
story.append(p('Show us a mandate. We\u2019ll show you the platform.',
    ParagraphStyle('cta', fontName='Helvetica-BoldOblique', fontSize=11,
        textColor=PLATINUM, leading=17, alignment=TA_CENTER)))
story.append(sp(6))
story.append(p('Pick any listed equity market, any currency, any benchmark. '
    'We will run the full Vektor workflow on your data and show you the output. '
    'No slides. No promises.',
    ParagraphStyle('cta_sub', fontName='Helvetica-Oblique', fontSize=9.5,
        textColor=WARM_GREY, leading=15, alignment=TA_CENTER)))
story.append(sp(10))
story.append(p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {REF}  \u00b7  Copyright 2026 InvestPuppy', s['wp_ref']))

doc.build(story)
sz = os.path.getsize(OUT)
print(f'Built: {OUT}')
print(f'Pages: {doc.page}')
print(f'Size:  {sz:,} bytes ({sz//1024}KB)')
