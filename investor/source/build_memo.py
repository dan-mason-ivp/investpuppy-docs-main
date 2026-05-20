"""
ip-investor-memo.pdf
InvestPuppy investor memo — ~10 pages
Build: python3 memo/source/build_memo.py
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, PageBreak, HRFlowable,
                                 KeepTogether)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY

OUT = '/home/claude/ip-investor-memo.pdf'

GREEN = colors.HexColor('#85D155')
DARK  = colors.HexColor('#0A0A0A')
BODY  = colors.HexColor('#1A1A1A')
GREY  = colors.HexColor('#888888')
WHITE = colors.white
GOLD  = colors.HexColor('#C8A96E')
LIGHT = colors.HexColor('#F4F4F4')
SECT  = colors.HexColor('#F0F7EA')

FONT_PATH = '/usr/share/fonts/truetype/google-fonts/'
for name in ['Poppins-Light','Poppins-Regular','Poppins-Medium','Poppins-Bold',
             'Poppins-Italic','Poppins-BoldItalic','Poppins-LightItalic']:
    pdfmetrics.registerFont(TTFont(name, f'{FONT_PATH}{name}.ttf'))

W, H = A4
ML = 52
MR = 52
MT = 72
MB = 54

# ── Styles ─────────────────────────────────────────────────────────────────────
def _styles():
    s = {}
    base = dict(fontName='Poppins-Light', fontSize=10, leading=16,
                textColor=BODY, spaceAfter=8)

    s['body']      = ParagraphStyle('body', **base, alignment=TA_JUSTIFY)
    s['body_left'] = ParagraphStyle('body_left', **base, alignment=TA_LEFT)
    s['h1']        = ParagraphStyle('h1', fontName='Poppins-Bold', fontSize=18,
                                    textColor=DARK, leading=24, spaceAfter=6, spaceBefore=16)
    s['h2']        = ParagraphStyle('h2', fontName='Poppins-Bold', fontSize=12,
                                    textColor=DARK, leading=18, spaceAfter=4, spaceBefore=14)
    s['h3']        = ParagraphStyle('h3', fontName='Poppins-Bold', fontSize=10.5,
                                    textColor=GREEN, leading=16, spaceAfter=4, spaceBefore=10)
    s['label']     = ParagraphStyle('label', fontName='Poppins-Bold', fontSize=8,
                                    textColor=GREEN, leading=12, spaceAfter=2, spaceBefore=8)
    s['small']     = ParagraphStyle('small', fontName='Poppins-Light', fontSize=8.5,
                                    textColor=GREY, leading=13, spaceAfter=4)
    s['bold_body'] = ParagraphStyle('bold_body', fontName='Poppins-Bold', fontSize=10,
                                    textColor=DARK, leading=15, spaceAfter=6)
    s['quote']     = ParagraphStyle('quote', fontName='Poppins-BoldItalic', fontSize=11,
                                    textColor=GREEN, leading=18, spaceAfter=8,
                                    leftIndent=16, rightIndent=16, alignment=TA_CENTER)
    s['cover_title'] = ParagraphStyle('cover_title', fontName='Poppins-Bold', fontSize=26,
                                      textColor=WHITE, leading=34, spaceAfter=8,
                                      alignment=TA_LEFT)
    s['cover_sub']   = ParagraphStyle('cover_sub', fontName='Poppins-Light', fontSize=12,
                                      textColor=WHITE, leading=18, spaceAfter=6)
    s['cover_meta']  = ParagraphStyle('cover_meta', fontName='Poppins-Regular', fontSize=9,
                                      textColor=GREY, leading=14, spaceAfter=4)
    s['toc']         = ParagraphStyle('toc', fontName='Poppins-Regular', fontSize=9.5,
                                      textColor=BODY, leading=16, spaceAfter=2)
    s['bullet']      = ParagraphStyle('bullet', fontName='Poppins-Light', fontSize=10,
                                      textColor=BODY, leading=15, spaceAfter=4,
                                      leftIndent=14, bulletIndent=0)
    s['note']        = ParagraphStyle('note', fontName='Poppins-Regular', fontSize=9,
                                      textColor=BODY, leading=14, spaceAfter=4,
                                      leftIndent=10, backColor=SECT,
                                      borderPadding=(6,8,6,8))
    return s

ST = _styles()

def B(text): return f'<font name="Poppins-Bold">{text}</font>'
def I(text): return f'<font name="Poppins-Italic">{text}</font>'
def G(text): return f'<font color="#85D155">{text}</font>'
def SM(text): return f'<font size="8" color="#888888">{text}</font>'


def hr(color=GREEN, thickness=1.5, spb=6, spa=10):
    return HRFlowable(width='100%', thickness=thickness, color=color,
                      spaceAfter=spa, spaceBefore=spb)

def bullet_item(text, st=None):
    if st is None:
        st = ST['bullet']
    return Paragraph(f'<bullet>&bull;</bullet> {text}', st)

def section_header(title, sub=None):
    items = [hr(color=DARK, thickness=0.5, spb=14, spa=2),
             Paragraph(title, ST['h2'])]
    if sub:
        items.append(Paragraph(sub, ST['small']))
    items.append(hr(color=GREEN, thickness=1, spb=0, spa=8))
    return items

def note_box(text):
    return Paragraph(text, ST['note'])


def kv_table(rows, col_widths=None):
    """Two-column key-value table."""
    if col_widths is None:
        col_widths = [120, W - ML - MR - 120]
    data = []
    for k, v in rows:
        data.append([Paragraph(B(k), ST['body_left']),
                     Paragraph(v, ST['body_left'])])
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Poppins-Light'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('VALIGN',   (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [WHITE, LIGHT]),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ]))
    return t


def pricing_table():
    headers = ['Tier', 'AUM', 'USD/year', 'Note']
    rows = [
        [B('Proof Partners'), 'Any',          G('US$13,500'),  'Year 1 rate · preferential terms locked for the duration'],
        ['Entry',             '≤US$55M',      'US$18,000',     ''],
        ['Growth',            '≤US$185M',     'US$36,000',     ''],
        ['Institutional',     '≤US$550M',     'US$105,000',    ''],
        ['Enterprise',        'US$550M+',     'US$175,000+',   'Pricing on request'],
        [I('Bloomberg Terminal'), I('—'),     I('~US$32,000'), I('Reference only — market data, not portfolio management')],
    ]
    data = [[Paragraph(h, ST['label']) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), ST['body_left']) for c in r])

    cw = [120, 70, 80, W - ML - MR - 280]
    t = Table(data, colWidths=cw)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  DARK),
        ('FONTNAME',      (0,0), (-1,0),  'Poppins-Bold'),
        ('FONTSIZE',      (0,0), (-1,0),  8),
        ('TEXTCOLOR',     (0,0), (-1,0),  WHITE),
        ('ROWBACKGROUNDS',(0,1), (-1,-2), [WHITE, LIGHT]),
        ('BACKGROUND',    (0,-1),(-1,-1), LIGHT),
        ('FONTNAME',      (0,-1),(-1,-1), 'Poppins-LightItalic'),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('GRID',          (0,0), (-1,-1), 0.25, colors.HexColor('#DDDDDD')),
    ]))
    return t


def revenue_table():
    headers = ['', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
    rows_data = [
        ('Boutique ARR',    '$77K',  '$167K', '$398K',   '$763K',   '$1,310K'),
        ('House ARR',       '—',     '—',     '$250K',   '$500K',   '$750K'),
        ('Wrapped revenue', '—',     '—',     '$230K',   '$230K',   '$460K'),
        (B('Total ARR'),    B('$77K'), B('$167K'), B('$878K'), B('$1,493K'), B('$2,520K')),
        ('EBITDA',          '($1,104K)','($1,132K)','($618K)', '($299K)', '$366K'),
        ('EBITDA margin',   'n/m',   'n/m',   'n/m',    'n/m',   '15%'),
    ]
    data = [[Paragraph(h, ST['label']) for h in headers]]
    for row in rows_data:
        data.append([Paragraph(str(c), ST['body_left']) for c in row])

    cw_total = W - ML - MR
    cw = [120] + [(cw_total - 120) / 5] * 5
    t = Table(data, colWidths=cw)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),  (-1,0),  DARK),
        ('TEXTCOLOR',     (0,0),  (-1,0),  WHITE),
        ('FONTNAME',      (0,0),  (-1,0),  'Poppins-Bold'),
        ('FONTSIZE',      (0,0),  (-1,-1), 9),
        ('ROWBACKGROUNDS',(0,1),  (-1,-2), [WHITE, LIGHT]),
        ('BACKGROUND',    (0,4),  (-1,4),  SECT),
        ('BACKGROUND',    (0,-2), (-1,-1), LIGHT),
        ('TOPPADDING',    (0,0),  (-1,-1), 5),
        ('BOTTOMPADDING', (0,0),  (-1,-1), 5),
        ('LEFTPADDING',   (0,0),  (-1,-1), 6),
        ('RIGHTPADDING',  (0,0),  (-1,-1), 6),
        ('VALIGN',        (0,0),  (-1,-1), 'MIDDLE'),
        ('ALIGN',         (1,0),  (-1,-1), 'RIGHT'),
        ('GRID',          (0,0),  (-1,-1), 0.25, colors.HexColor('#DDDDDD')),
    ]))
    return t


# ── Page templates ─────────────────────────────────────────────────────────────
class MemoTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename,
                         pagesize=A4,
                         leftMargin=ML,
                         rightMargin=MR,
                         topMargin=MT,
                         bottomMargin=MB,
                         **kw)
        self.page_num = 0

    def handle_pageBegin(self):
        super().handle_pageBegin()

    def afterPage(self):
        pass


def _header_footer(canvas, doc):
    """Called on every page."""
    canvas.saveState()
    pn = canvas.getPageNumber()

    # Header band (skip cover page = page 1)
    if pn > 1:
        canvas.setFillColor(DARK)
        canvas.rect(0, H - 38, W, 38, fill=1, stroke=0)
        canvas.setFont('Poppins-Bold', 10)
        canvas.setFillColor(WHITE)
        canvas.drawString(ML, H - 22, 'Invest')
        iw = canvas.stringWidth('Invest', 'Poppins-Bold', 10)
        canvas.setFillColor(GREEN)
        canvas.drawString(ML + iw, H - 22, 'Puppy')
        canvas.setFont('Poppins-Regular', 8)
        canvas.setFillColor(GREY)
        canvas.drawString(ML, H - 33, 'Investor Memo · Confidential · May 2026')
        canvas.setFillColor(WHITE)
        canvas.drawRightString(W - MR, H - 22, 'Vektor — Systematic Portfolio Management')
        canvas.setFillColor(GREY)
        canvas.drawRightString(W - MR, H - 33, f'investpuppy.com')
        canvas.setStrokeColor(GREEN)
        canvas.setLineWidth(1.5)
        canvas.line(0, H - 38, W, H - 38)

    # Footer
    canvas.setStrokeColor(colors.HexColor('#DDDDDD'))
    canvas.setLineWidth(0.5)
    canvas.line(ML, MB + 16, W - MR, MB + 16)
    canvas.setFont('Poppins-Light', 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(ML, MB + 4,
                      'InvestPuppy Pte Ltd · investpuppy.com · contact@investpuppy.com · Internal only')
    canvas.drawRightString(W - MR, MB + 4, str(pn))
    canvas.restoreState()


# ── Cover page (built manually) ────────────────────────────────────────────────
def _cover_page(c):
    # Full dark background
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Green accent bar on left
    c.setFillColor(GREEN)
    c.rect(0, 0, 6, H, fill=1, stroke=0)

    # Logo
    c.setFont('Poppins-Bold', 18)
    c.setFillColor(WHITE)
    c.drawString(ML, H - 60, 'Invest')
    iw = c.stringWidth('Invest', 'Poppins-Bold', 18)
    c.setFillColor(GREEN)
    c.drawString(ML + iw, H - 60, 'Puppy')
    c.setFont('Poppins-Regular', 9)
    c.setFillColor(GREY)
    c.drawString(ML, H - 76, 'investpuppy.com')

    # Green rule
    c.setStrokeColor(GREEN)
    c.setLineWidth(1)
    c.line(ML, H - 88, W - MR, H - 88)

    # Title block
    c.setFont('Poppins-Bold', 28)
    c.setFillColor(WHITE)
    c.drawString(ML, H - 140, 'Investor Memo')
    c.setFont('Poppins-Light', 14)
    c.setFillColor(colors.HexColor('#AAAAAA'))
    c.drawString(ML, H - 162, 'Vektor — Systematic Listed Equity')
    c.drawString(ML, H - 180, 'Portfolio Management')

    # Tagline
    c.setFont('Poppins-BoldItalic', 12)
    c.setFillColor(GREEN)
    c.drawString(ML, H - 212, '"Honest by design."')

    # Divider
    c.setStrokeColor(colors.HexColor('#333333'))
    c.setLineWidth(0.5)
    c.line(ML, H - 232, W - MR, H - 232)

    # Meta block
    meta = [
        ('Document',   'IP-INV-MEMO-260517-1.1'),
        ('Date',       'May 2026'),
        ('Status',     'Confidential — internal and NDA counterparties only'),
        ('Company',    'InvestPuppy Pte Ltd'),
        ('Website',    'investpuppy.com'),
        ('Contact',    'contact@investpuppy.com'),
    ]
    y = H - 258
    for label, val in meta:
        c.setFont('Poppins-Bold', 9)
        c.setFillColor(GREY)
        c.drawString(ML, y, label + ':')
        c.setFont('Poppins-Regular', 9)
        c.setFillColor(WHITE)
        c.drawString(ML + 80, y, val)
        y -= 16

    # Contents preview
    y = H - 430
    c.setStrokeColor(colors.HexColor('#333333'))
    c.setLineWidth(0.5)
    c.line(ML, y + 8, W - MR, y + 8)
    c.setFont('Poppins-Bold', 9)
    c.setFillColor(GREEN)
    c.drawString(ML, y - 4, 'Contents')
    sections = [
        '1.  Executive Summary',
        '2.  Team',
        '3.  The Problem',
        '4.  The Platform — Vektor',
        '5.  Business Model',
        '6.  Go-to-Market',
        '7.  Market',
        '8.  Financial Projections',
        '9.  The Raise',
        '10. Appendix — Delivery Models',
    ]
    y -= 20
    for s in sections:
        c.setFont('Poppins-Regular', 9)
        c.setFillColor(WHITE)
        c.drawString(ML + 8, y, s)
        y -= 14

    # Footer
    c.setFont('Poppins-Light', 7.5)
    c.setFillColor(GREY)
    c.drawString(ML, MB,
                 'Confidential · Not for distribution · InvestPuppy Pte Ltd · May 2026')
    c.drawRightString(W - MR, MB, '1')


# ── Story builder ──────────────────────────────────────────────────────────────
def build_story():
    story = []

    def H2(t, sub=None):
        for item in section_header(t, sub):
            story.append(item)

    def H3(t): story.append(Paragraph(t, ST['h3']))
    def P(t):  story.append(Paragraph(t, ST['body']))
    def PL(t): story.append(Paragraph(t, ST['body_left']))
    def SP(n=8): story.append(Spacer(1, n))
    def BUL(t): story.append(bullet_item(t))
    def NOTE(t): story.append(note_box(t))
    def LBL(t): story.append(Paragraph(t.upper(), ST['label']))

    # ── 1. Executive Summary ───────────────────────────────────────────────────
    H2('1.  Executive Summary')

    P(f'{B("InvestPuppy")} is building {B("Vektor")} — a systematic listed equity portfolio management '
      f'platform for boutique discretionary portfolio managers, independent wealth managers, '
      f'and family offices. One product. Three delivery models. '
      f'{B("Honest by design.")}')

    NOTE(f'Vektor is one platform available through three delivery models: '
         f'direct subscription for boutique practitioners ({B("Vektor : Boutique")}), '
         f'direct institutional subscription ({B("Vektor : House")}), '
         f'and licensing through custodian banks for their EAM client base ({B("Vektor : Wrapped")}). '
         f'Methodology, signal generation, and audit trail are identical in every deployment.')

    SP()
    rows = [
        ('Raise',           'US$2.5M'),
        ('Pre-money',       'US$9M – US$10M'),
        ('Stage',           'Pre-revenue · building toward first Proof Partner'),
        ('Primary market',  'Singapore · 2,000+ single family offices (MAS, 2024)'),
        ('Revenue model',   'AUM-tiered SaaS + institutional licence + per-mandate fee'),
        ('Year 5 ARR',      'US$2.52M (base) · US$1.25M (bear) · US$4.25M (bull)'),
        ('EBITDA positive', 'Year 3 · base case'),
        ('Team',            'CEO + CTO (co-equal, decade together) + 3 pre-launch collaborators'),
    ]
    story.append(kv_table(rows))
    SP(12)

    # ── 2. Team ───────────────────────────────────────────────────────────────
    story.append(PageBreak())
    H2('2.  Team',
       'Five people. Decades of institutional experience. One conviction.')

    NOTE(f'Full founder biographies are disclosed under NDA. '
         f'The founding partnership predates InvestPuppy by approximately a decade, '
         f'established through shared work in institutional financial technology.')

    SP(8)
    H3('CEO')
    P(f'Co-equal founder. Spent the better part of three decades inside the institutional '
      f'portfolio management technology that boutique practitioners cannot access — '
      f'spanning the product\'s full commercial lifecycle from vendor through solution '
      f'architect and programme and engagement management for Global Tier 1 bank deployments. '
      f'The Unvarnished series documents the failure modes this platform was specifically '
      f'designed to avoid. Full biography disclosed under NDA.')

    SP(8)
    H3('CTO')
    P(f'Co-equal founder. Two decades of institutional financial technology architecture — '
      f'cloud-native core banking infrastructure deployed by major financial institutions '
      f'and end-to-end architecture of digital challenger bank launches. '
      f'Architect of the Vektor platform. Built to institutional compliance standards '
      f'from first principles — data residency, audit trail, API integration security '
      f'— not retrofitted to meet them. '
      f'The platform was built to operate within custodian-connected financial infrastructure, not alongside it. '
      f'{I(chr(34) + "I could not have done it without him. He could not have done it without me." + chr(34))} — CEO '
      f'Full biography disclosed under NDA.')

    SP(8)
    H3('Pre-launch team (three collaborators)')
    P('Three senior professionals with decades of shared institutional experience in '
      'wealth management, technology implementation, and compliance. '
      'All bound by NDA and the same founding conviction: '
      + I('"there has to be a better way."'))

    SP(8)
    P(f'The five-person team was built before the raise. '
      f'This is not a team assembled to chase funding — '
      f'it is a team that has been doing the work.')

    # ── 3. The Problem ────────────────────────────────────────────────────────
    story.append(PageBreak())
    H2('3.  The Problem',
       'Why boutique practitioners need a better tool — and why nobody has built one')

    P(f'{B("The Bloomberg Terminal costs approximately US$32,000 per seat per year.")} '
      f'It was built for sell-side research and market data distribution. '
      f'It is not a portfolio management tool. Boutique discretionary managers and family offices '
      f'have been using it as one — expensively, incompletely, and without audit trail — '
      f'because there was nothing else.')

    SP(6)
    P(f'The alternative is manual: spreadsheets, ad hoc rebalancing tools, and fragmented systems '
      f'that make systematic portfolio construction time-consuming and error-prone. '
      f'Compliance and audit requirements grow while tools do not.')

    SP(6)
    P('The incumbent platforms — Bloomberg, Advent, Iress — are scaled for large institutions. '
      'Their pricing, implementation requirements, and architecture assumptions exclude the boutique practitioner. '
      'This is not an oversight. It is a rational commercial decision by vendors serving large clients.')

    SP(8)
    H3('Three specific failure modes')
    failure_modes = [
        (f'{B("Signal application is manual.")} '
         'Translating a systematic view into portfolio actions requires human judgment at every step. '
         'This is not risk management. It is friction.'),
        (f'{B("Rebalancing is not systematic.")} '
         'Without a platform that can generate 10,000 portfolio configurations per strategy, '
         'portfolio construction defaults to heuristic approximation.'),
        (f'{B("Audit trail is incomplete.")} '
         'MAS and regulatory requirements assume documented rationale for every decision. '
         'Manual workflows cannot produce this reliably.'),
    ]
    for f in failure_modes:
        BUL(f)

    SP(8)
    NOTE(f'{B("The Unvarnished series")} — 10 published papers on why financial software '
         f'implementations fail — addresses this directly. '
         f'These are the field notes from the rooms where the same projects failed '
         f'for the third time. Available at investpuppy.com/unvarnished.')

    # ── 3. The Platform ────────────────────────────────────────────────────────
    story.append(PageBreak())
    H2('4.  The Platform — Vektor',
       'Systematic listed equity portfolio management')

    P(f'Vektor is a systematic portfolio management platform. '
      f'It generates {B("10,000 portfolio configurations per strategy")}, '
      f'applies signals systematically, produces a complete audit trail, and integrates with '
      f'custodian infrastructure. It is not a reporting tool layered on top of manual execution. '
      f'It is the execution layer.')

    SP(8)
    H3('Core capabilities — identical across all three delivery models')
    caps = [
        f'{B("10,000 portfolio configurations per strategy")} — systematic signal application at institutional quality.',
        f'{B("Full audit trail")} — every rebalance, every override, every decision. Transparent to regulators and clients.',
        f'{B("Multi-custodian mandate management")} — independent sub-accounts sharing a common strategy.',
        f'{B("Order routing")} — automated (IBKR) or manual (any custodian, EAM records fill).',
        f'{B("99.94% capital allocation efficiency.")}', 
        f'{B("RBAC and maker/checker workflow")} — institutional-grade access controls.',
    ]
    for cap in caps:
        BUL(cap)

    SP(8)
    H3('Platform status')
    status = [
        'Systematic signal generation and portfolio construction: live.',
        f'IBKR integration in place. {B("Has not yet executed in a live account.")}',
        'Audit trail and reporting: complete.',
        'Multi-custodian mandate management: in build.',
        'Proof Partners programme: open for first commercial conversations.',
    ]
    for s in status:
        BUL(s)

    SP(6)
    # PARK: 3-month live execution timeline is a provisional planning assumption.
    # Confirm with founding team before NDA version distribution.
    NOTE(f'{B("Live execution target [provisional]:")} '
         f'First live account execution is targeted within three months of first Proof Partner onboarding. '
         f'This timeline is a planning assumption and will be confirmed once the Proof Partner programme is active.')

    SP(8)
    NOTE(f'{B("Delivery model ≠ product quality.")} '
         f'The platform is identical in Vektor : Boutique, Vektor : House, and Vektor : Wrapped. '
         f'The delivery model describes how it reaches the client, not what they receive.')

    SP(4)
    NOTE(f'{B("Data governance:")} Every deployment model operates under a defined data processing agreement. '
         f'Vektor : Boutique — InvestPuppy holds client portfolio data under DPA, MAS TRM framework referenced. '
         f'Vektor : House — standard cloud or hybrid deployment; no client identity data in cloud on hybrid. '
         f'Vektor : Wrapped — InvestPuppy holds no EAM client PII by structural design. '
         f'Full data residency and privacy architecture: {I("ip-data-residency-privacy.pdf")} — available on request.')

    # PARK: The founding team is considering introducing the "Rolex analogy" as a framing
    # device for this section — "there are thousands of fake Rolex watches; aficionados
    # still want the real thing." Decision parked. Revisit before NDA version distribution.
    # The paragraph below carries the sentiment and evidence without the analogy for now.
    SP(10)
    H3('Why methodology matters — and why it cannot be quickly replicated')
    P('There will be platforms that look like Vektor. Some already exist in adjacent form. '
      'The practitioners who know this market — who have lived through the implementations '
      'that did not work and have the audit trail gaps to prove it — will be able to tell '
      'the difference. The methodology behind Vektor is documented across eleven technical '
      'white papers. The signal generation architecture was built by someone who has operated '
      'systematic portfolios at institutional scale. The custodian credentials are '
      'production-grade and live. The failure modes this platform was designed to avoid '
      'are published under our own name. These things take years to build. They cannot be '
      'assembled quickly by someone who has identified a market gap. The market for portfolio '
      'management software has never lacked for vendors. It has lacked for vendors who '
      'understand the difference between what they built and what practitioners actually need.')

    # ── 4. Business Model ─────────────────────────────────────────────────────
    story.append(PageBreak())
    H2('5.  Business Model',
       'Three revenue streams — one product')

    H3('Vektor : Boutique — AUM-tiered annual subscription')
    P('Direct subscription to boutique DPMs, independent RIAs, and family offices. '
      'Pricing is published openly and held consistently. '
      'Early-commitment Proof Partners receive a preferential Year 1 rate, '
      'followed by a permanently locked discount from standard pricing for the duration of the relationship.')

    SP(8)
    story.append(pricing_table())
    SP(4)
    PL(SM('All prices USD. Non-USD currencies available on request. '
          'Proof Partners: preferential commercial terms locked for the duration — '
          'permanently discounted from standard tier pricing, agreed at signing.'))

    SP(12)
    H3('Vektor : House — Alloy Partners programme')
    P(f'Institutional subscription for DPM desks at regional banks, MFOs, and large independent managers. '
      f'The {B("Alloy Partners")} programme is {B("staged and gated")} — '
      f'InvestPuppy screens and selects partners. Both parties are assessing fit.')

    SP(4)
    alloy_stages = [
        (f'{B("Stage 1")} — open now', 'Initial conversation and NDA. Low resource. Parallel to boutique activity.'),
        (f'{B("Stage 2")} — gated',    'Proof of concept on the partner\'s own data + integration architecture scoping. '
                                        'Capacity-gated: maximum one Alloy Partner at Stage 2 at any time. '
                                        'Begins once first Proof Partner is active.'),
        (f'{B("Stage 3")} — commercial', 'Commercial negotiation and partnership terms. Follows Stage 2.'),
    ]
    for stage, desc in alloy_stages:
        story.append(Paragraph(f'{stage}: {desc}', ST['bullet']))
        SP(4)

    NOTE(f'{B("Too small to fail.")} One Stage 2 partner at a time. '
         f'Honest capacity management. No overselling. '
         f'Implementations that fail do not fail cheaply — we have documented that in ten papers. '
         f'We will not be the subject of an eleventh.')

    SP(12)
    H3('Vektor : Wrapped — custodian bank licensing')
    P('InvestPuppy licenses Vektor to custodian banks and wealth platforms '
      'for distribution to their EAM client base. '
      'The bank is the commercial counterpart. EAMs are end users — '
      'their capability is identical to Boutique and House clients.')

    SP(4)
    BUL(f'{B("Platform licence fee")} per partner per year.')
    BUL(f'{B("Per-mandate fee")} for each EAM mandate managed on the platform.')
    SP(6)
    NOTE(f'{B("The CEO credential:")} The CEO holds production-grade OpenWealth API credentials '
         f'across Tier 1 custodian institutions in EMEA and APAC, established over years of direct '
         f'institutional relationship work. This is not a planned integration — it is a live '
         f'credential that enables InvestPuppy to initiate the Wrapped channel conversation at '
         f'the infrastructure level before most competitors can get a meeting with the right counterpart. '
         f'It is the primary reason the Wrapped revenue stream is modelled as near-term rather than speculative. '
         f'Specific institutions and credentials are disclosed under NDA.')


    # ── 5a. Institutional Product Roadmap (NDA) ───────────────────────────────
    story.append(PageBreak())
    H2('5a.  Institutional Product Roadmap',
       'NDA confidential — not for external distribution')

    NOTE(f'{B("NDA STAGE ONLY.")} This section describes a product in development that is not '
         f'yet publicly disclosed. It is included because it materially extends '
         f'InvestPuppy\'s addressable market and changes the investment case. '
         f'Do not share beyond this NDA relationship.')

    SP(8)
    H3('The natural progression')
    P(f'Vektor proves the methodology at boutique scale. '
      f'Tenzor deploys it at institutional scale. '
      f'The platform architecture was designed from the outset to reach both.')

    SP(6)
    P(f'{B("Tenzor")} is the full institutional portfolio management platform — '
      f'the same systematic methodology as Vektor, extended to serve DPM desks at '
      f'regional banks, large MFOs, and institutional asset managers who require '
      f'order workflow, performance attribution, core corporate actions, and '
      f'multi-asset capability alongside systematic portfolio construction.')

    SP(8)
    H3('The sequencing')
    P(f'Tenzor development begins post first Vektor Proof Partners go-live, funded at Series A. '
      f'The founding team is focused on Vektor\'s commercial launch. '
      f'This is not two products in parallel — it is one company building in the right order. '
      f'Boutique practitioners need simplicity and access. '
      f'Institutional operators need full-stack capability and compliance depth. '
      f'Different buyers, different commercial structures, different products — '
      f'built on the same codebase by a team that has operated both sides of this market for decades.')

    SP(8)
    H3('Addressable market — combined')
    tenzor_rows = [
        ('Vektor TAM',                    '~US$15M ARR · three markets · 10% penetration'),
        ('Tenzor TAM (direct)',           '~US$10M–US$13M ARR · three markets · 10% penetration'),
        ('Tenzor TAM (incl. Wrapped)',    '~US$22M–US$26M ARR at conservative assumptions'),
        (f'{B("Combined (non-overlapping)")}', f'{B("~US$25M–US$28M ARR · three markets · 10% penetration")}'),
    ]
    story.append(kv_table(tenzor_rows))

    SP(8)
    H3('The conversion pathway')
    P(f'Vektor : House clients who grow their AUM or add asset classes are '
      f'Tenzor\'s first clients. A conversion from a proven relationship — '
      f'not a cold sale. The institutional sales cycle is already running through '
      f'the Alloy Partners programme. Tenzor extends the commercial outcome of '
      f'that relationship, not a new sales motion.')

    SP(8)
    H3('Institutional market context')
    P(f'The institutional portfolio management market that Tenzor enters is served at tier 1 scale '
      f'by platforms including {B("Temenos TripleA Plus")} (US$150,000–US$400,000+ per deployment, '
      f'dominant in European private banking and wealth management) and {B("Avaloq")} '
      f'(US$500,000–US$2M+ implementation, dominant in Swiss private banking). '
      f'Neither offers systematic portfolio management at mid-market institutional pricing. '
      f'Tenzor enters below the pricing floor of both — with a methodology already '
      f'proven at boutique scale through Vektor clients.')

    NOTE(f'{B("Tenzor status:")} Architecture defined. '
         f'Development milestone-gated to first Vektor Proof Partners go-live. '
         f'Series A funded. Product name and brand are working direction, not yet public. '
         f'The naming logic: a tensor generalises a vector across multiple simultaneous dimensions. '
         f'Vektor → Tenzor is the same product philosophy at institutional scale.')

    # ── 6. Go-to-Market ───────────────────────────────────────────────────────
    story.append(PageBreak())
    H2('6.  Go-to-Market',
       'Proof Partners first, then institutional and Wrapped in parallel')

    H3('Immediate priority — Proof Partners')
    P(f'The {B("Proof Partners")} programme is the boutique go-to-market. '
      f'Three Proof Partner slots available at the US$13,500 founding rate. '
      f'Suite is distribution-ready. First conversations beginning now.')

    SP(6)
    pp_benefits = [
        f'{B("Year 1 rate:")} US$13,500 (firms below US$55M AUM) or 35% below standard tier (firms above US$55M AUM).',
        f'{B("Preferential terms locked for the duration")} — permanently discounted from standard tier pricing at each renewal, agreed at signing.',
        f'{B("Founding team access")} — CEO and CTO present in first implementation weeks.',
        f'{B("Named as a Proof Partner")} — first-mover recognition.',
    ]
    for b in pp_benefits:
        BUL(b)

    SP(10)
    H3('Institutional — Alloy Partners')
    P('Institutional sales cycles run 12–18 months minimum. '
      'Active engagement must begin before the product is fully built. '
      'Stage 1 conversations (NDA + initial call) are open now in parallel with boutique activity.')

    SP(10)
    H3('Distribution')
    dist = [
        f'{B("Singapore:")} Primary market. 2,000+ single family offices (MAS, 2024). Distribution-ready.',
        f'{B("Switzerland:")} Near-term expansion. FinIA compliance. OpenWealth infrastructure established with Tier 1 custodians.',
        f'{B("UK:")} FCA regulatory opinion planned within 12 months. '
        f'Distribution begins post-clearance. '
        f'Timeline will be escalated if required for a UK-based Proof Partner.',
    ]
    for d in dist:
        BUL(d)

    # ── 6. Market ─────────────────────────────────────────────────────────────
    story.append(PageBreak())
    H2('7.  Market',
       'Boutique practitioners are systematically underserved')

    P('The addressable market is not enterprise wealth management. '
      'It is the boutique end — DPMs managing US$20M–US$500M, '
      'independent RIAs, single family offices and MFOs, '
      'and EAMs operating through custodian banks. '
      'These practitioners have institutional-quality investment processes '
      'but consumer-grade tooling.')

    SP(8)
    market_facts = [
        f'Singapore: {B("2,000+ single family offices")} (MAS, 2024) plus boutique DPMs and IWMs — primary market, distribution-ready.',
        f'Switzerland: established EAM and IAM market with {B("strong OpenWealth infrastructure adoption")}. '
        f'FinIA (Financial Institutions Act) compliance framework active since 2023, creating '
        f'structured compliance requirements that Vektor\'s audit trail and systematic workflow '
        f'directly address. CEO credential operational across Swiss Tier 1 custodians. '
        f'Near-term expansion — first commercial conversations underway.',
        f'UK: growing boutique DPM segment post-MiFID II unbundling. '
        f'FCA regulatory opinion planned within 12 months — distribution begins post-clearance. '
        f'Timeline will be escalated if required for a UK-based Proof Partner. '
        f'UK practitioners may engage in pre-distribution conversations in the interim.',
        f'SE Asia broadly: emerging market asset manager growth and increasing compliance requirements. '
        f'A successful Wrapped channel through major Asian custodians would extend Vektor\'s reach '
        f'to EAM markets across the region — downstream impact that scales with custodian adoption '
        f'rather than direct sales effort.',
        f'Rest of Europe: {B("Luxembourg, Germany, Liechtenstein, the Channel Islands (Jersey, Guernsey) and Crown Dependencies")} '
        f'represent natural expansion from the '
        f'Switzerland and UK base. Shared MiFID II regulatory framework and growing boutique DPM '
        f'and independent wealth management population. The Channel Islands and Crown Dependencies '
        f'are English-speaking, common law jurisdictions with FCA-adjacent regulatory culture and '
        f'substantial independent wealth management communities — a natural early-stage '
        f'UK-adjacent market without a separate FCA authorisation pathway. '
        f'OpenWealth infrastructure at Swiss Tier 1 custodians provides cross-border connectivity '
        f'into Luxembourg and German markets. Medium-term pipeline — expansion follows '
        f'Swiss and UK commercial proof.',
        f'DIFC / UAE: high concentration of family offices and private wealth management. '
        f'European private bank presence in the DIFC creates a natural bridge from the '
        f'OpenWealth European institutional network. On first qualifying conversation.',
    ]
    for m in market_facts:
        BUL(m)

    SP(8)
    NOTE(f'{B("Addressable market — indicative sizing:")} '
         f'Singapore alone — 2,000+ SFOs plus the boutique DPM and IWM population — '
         f'represents an annual addressable subscription market of approximately '
         f'{B("US$5M–US$8M at 10% penetration")} across pricing tiers. '
         f'Adding Switzerland and UK at conservative entry-level penetration brings '
         f'the three-market primary addressable to approximately {B("US$15M ARR.")} '
         f'This figure is based on Singapore, Switzerland, and UK only — '
         f'it does not include Rest of Europe, the Channel Islands, SE Asia broadly, '
         f'or DIFC / UAE, each of which represents additional addressable opportunity '
         f'that has not been sized in this document. The US$15M is a '
         f'conservative three-market baseline, not a ceiling. '
         f'The Wrapped channel is a separate and multiplicative layer: each bank partner '
         f'brings a portfolio of EAM mandates generating subscription revenue that would '
         f'otherwise require individual direct client relationships.')

    SP(8)
    NOTE(f'InvestPuppy does not position Vektor against Bloomberg. '
         f'{B("Bloomberg Terminal, Bloomberg PORT, and Bloomberg data feeds are three separate products with three distinct competitive positions.")} '
         f'Vektor competes for the systematic portfolio management workflow — '
         f'a gap the Terminal does not fill and PORT prices out of the boutique segment.')

    SP(10)
    H3('Competitive landscape')
    P('The direct competitive set for systematic portfolio management at boutique scale is thin. '
      'This is part of the opportunity.')

    SP(4)
    comp_items = [
        f'{B("Iress / XPLAN")} — strong in UK and Australia, primarily execution and reporting, '
        f'not systematic signal-to-portfolio construction. Priced for mid-size firms upward.',
        f'{B("Advent Geneva / SS&C")} — institutional portfolio accounting. Expensive, complex '
        f'implementation, built for fund administrators not boutique DPMs. '
        f'Entry-level pricing starts above US$100,000/year.',
        f'{B("Enfusion")} — cloud-native PMS, strongest at hedge fund scale. Growing in '
        f'wealth management but primarily institutional. Pricing is AUM-linked and typically '
        f'exceeds US$150,000/year for the target Vektor client profile.',
        f'{B("Bloomberg PORT")} — portfolio analytics add-on to Terminal. '
        f'Adds US$6,000–US$25,000 on top of the US$32,000 Terminal cost. '
        f'Analytics only — not systematic execution or audit trail.',
        f'{B("Locally-built SGX tools")} — a small number of Singapore-specific portfolio '
        f'tools targeting SGX-listed equities exist in the market. None offer systematic '
        f'multi-mandate construction, full audit trail, or custodian-agnostic architecture.',
        f'{B("Spreadsheet + manual workflow")} — the de facto standard for boutique practitioners. '
        f'No audit trail. Not systematic. Compliance risk increasing. This is the largest addressable segment.',
    ]
    for item in comp_items:
        BUL(item)

    SP(8)
    NOTE(f'{B("Vektor\'s position:")} Below the pricing floor of institutional PMS platforms. '
         f'Above the capability ceiling of spreadsheet workflows. '
         f'Purpose-built for the boutique practitioner segment that incumbents '
         f'have rationally chosen not to serve.')

    # ── 7. Financial Projections ──────────────────────────────────────────────
    story.append(PageBreak())
    H2('8.  Financial Projections',
       'Base case — three-stream revenue model (USD)')

    P(f'Revenue begins with Proof Partners and first Entry clients in Year 1. '
      f'Boutique scale drives Years 2–3. '
      f'First House commercial client targets Year 3. '
      f'First Wrapped partner targets Year 3. '
      f'Base case reaches EBITDA positive in Year 5. '
      f'Full financial model available in {I("ip-investor-model.xlsx")} — three scenarios.')

    SP(8)
    story.append(revenue_table())
    SP(6)
    NOTE(f'{B("Year 1 revenue note:")} Year 1 Boutique ARR of US$77K reflects three Proof Partner '
         f'slots (US$40,500 at Tier A rate) plus first Entry-tier clients acquired through '
         f'direct distribution in parallel with the Proof Partner programme. '
         f'The Proof Partner programme is the commercial foundation, not the ceiling.')
    SP(4)
    PL(SM('Base case shown. Bear case: first House Year 4, first Wrapped Year 5, slower boutique ramp. '
          'Bull case: first House Year 3, two Wrapped partners Year 4. '
          'Costs scale at +10% p.a. Year 1→2, +15% Year 2→3, +20% thereafter. '
          'See ip-investor-model.xlsx for full assumptions.'))

    SP(10)
    H3('Use of proceeds')
    proceeds = [
        (f'{B("Five-person team")} (salaries + benefits)',  'US$420K/yr · Year 1 base'),
        (f'{B("Infrastructure")} (AWS, tooling)',            'US$36K/yr'),
        (f'{B("Legal + compliance")} (SG, CH, UK)',          'US$60K · primarily Year 1'),
        (f'{B("Sales + marketing")}',                        'US$30K/yr · growing with traction'),
        (f'{B("Runway")}',                                   '18–24 months to Series A milestone'),
        (f'{B("Tenzor")}',                                     'Design phase and architecture documentation funded from seed. Full development at Series A.'),
    ]
    story.append(kv_table(proceeds, col_widths=[200, W - ML - MR - 200]))

    # ── 9. The Raise ─────────────────────────────────────────────────────────
    story.append(PageBreak())
    H2('9.  The Raise')

    raise_data = [
        ('Target',           'US$2.5M'),
        ('Pre-money',        'US$9M – US$10M (two-product platform strategy, founding team institutional credentials, combined Vektor and Tenzor addressable market of US$25M–US$28M ARR)'),
        ('Structure',        'Quiet raise · 3–5 investors · boutique wealth practitioners or fintech-experienced angels with wealth management backgrounds'),
        ('Compatibility',    'Stealth-compatible · founders currently employed · both commit full-time on close'),
        ('Use of proceeds',  '5-person team · institutional sales runway · legal infrastructure · product build'),
        ('Runway',           '18–24 months to Series A milestone'),
        ('Milestones',       'First Vektor Proof Partners go-live → first Alloy Partners Stage 2 active → Tenzor design phase complete → first Wrapped channel pilot conversation — Series A milestone'),
    ]
    story.append(kv_table(raise_data))

    SP(8)
    NOTE(f'{B("UK structure and EIS:")} A UK holding company is being incorporated to enable '
         f'EIS-qualifying investment for UK-based angels. HMRC advance assurance is being sought. '
         f'UK investors should confirm EIS eligibility with their advisors. '
         f'Singapore government co-investment — Startup SG Equity and MAS FSTI grants — '
         f'are being pursued in parallel through the Singapore operating entity as supplementary '
         f'non-dilutive channels.')

    SP(8)
    NOTE(f'{B("Team compensation:")} '
         f'InvestPuppy compensates its founding team at market rate. '
         f'The founders\' alignment with investor outcomes is through equity '
         f'\u2014 not through personal financial risk underwritten by below-market '
         f'compensation. We do not ask the team to subsidise the raise. '
         f'We ask investors to fund the actual cost of building this platform with the '
         f'people capable of building it. The raise is sized accordingly. '
         f'Market-rate costs and the full salary framework are visible in the '
         f'financial model Assumptions tab.')

    SP(12)
    H3('The ideal investor')
    P('The ideal investor for this round is a boutique wealth practitioner — '
      'whether managing a family office, a discretionary portfolio management firm, '
      'an independent wealth management practice, or a multi-family office — '
      'who faces the tool gap Vektor is built to close. Such an investor brings '
      'more than capital: a credible, operationally experienced voice within the target '
      'market with a direct stake in the platform\'s success.')

    P('The ideal investor may also be a fintech-experienced angel with wealth management '
      'background; a former executive of an institutional portfolio management platform '
      'who combines capital with direct knowledge of the competitive landscape; or a '
      'custodian bank corporate venture arm evaluating both financial investment and '
      'Wrapped channel partnership — where investment and commercial interest are '
      'structurally aligned. InvestPuppy is not simply seeking capital. '
      'It is seeking investors who are, in the fullest sense, constituents of the '
      'market it serves or the institutional ecosystem it is entering.')

    SP(4)
    NOTE(f'{B("Ring-fencing:")} Investment terms and subscription pricing are entirely separate '
         f'and neither confers benefit on the other. A family office that invests in InvestPuppy '
         f'and subscribes to Vektor does so on the same commercial terms as any other client. '
         f'The alignment is operational and reputational — not financial.')

    SP(12)
    NOTE(f'{B("What the raise buys:")} Time. '
         f'The boutique channel can begin generating revenue within 6 months of Proof Partner signing. '
         f'The institutional channel (House + Wrapped) requires 12–18 months of active relationship '
         f'development before commercial terms are possible. '
         f'The raise funds that cycle without compromising the pace of boutique traction.')

    SP(10)
    NOTE(f'{B("On exit:")} '
         f'InvestPuppy is building what the incumbents should have built and chose not to. '
         f'At revenue maturity, that creates a natural acquisition landscape — '
         f'custodian banks seeking to own the Wrapped channel relationship directly, '
         f'and institutional fintech consolidators seeking boutique and mid-market access. '
         f'InvestPuppy is not building toward those outcomes. '
         f'It is building away from the platforms that created the problem it is solving. '
         f'The investors\' return follows from that — from commercial success, '
         f'not from a plan to be acquired.')

    SP(12)
    story.append(Paragraph('"Honest by design."', ST['quote']))

    # ── 10. Appendix ─────────────────────────────────────────────────────────
    story.append(PageBreak())
    H2('10.  Appendix — Delivery Models Reference')

    P('Three delivery models. One product. Methodology, signal generation, and audit trail '
      'identical in every deployment. The model name describes how Vektor is delivered '
      'and at what scale — not three different products.')

    SP(8)
    models = [
        ('Vektor : Boutique',
         'Direct · boutique scale',
         'Direct subscription. AUM-tiered annual fee. '
         'InvestPuppy manages infrastructure. Client holds their own data. '
         'DPA with every client. MAS TRM framework referenced.'),
        ('Vektor : House',
         'Direct · institutional scale',
         'Direct subscription. Alloy Partners programme. Staged and gated. '
         'Standard cloud (InvestPuppy-managed) or hybrid deployment (identity vault on client infrastructure). '
         'InvestPuppy screens and selects partners.'),
        ('Vektor : Wrapped',
         'Intermediated · custodian banks',
         'Licensed to custodian banks and wealth platforms for their EAM client base. '
         'Platform fee + per-mandate fee. InvestPuppy holds no EAM client PII — '
         'structural separation by design. '
         'Bank is the commercial counterpart.'),
    ]

    for name, tagline, desc in models:
        story.append(Paragraph(name, ST['h3']))
        story.append(Paragraph(I(tagline), ST['small']))
        P(desc)
        SP(6)

    SP(8)
    story.append(Paragraph(
        'Full delivery models reference: ip-three-delivery-models-v2.pdf (public distribution)',
        ST['small']
    ))

    return story


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)

    # Build the cover page separately
    from reportlab.pdfgen import canvas as pdfcanvas2
    import tempfile
    cover_path = os.path.join(os.path.dirname(OUT), '_cover_tmp.pdf')
    body_path  = os.path.join(os.path.dirname(OUT), '_body_tmp.pdf')

    # Cover
    c = pdfcanvas2.Canvas(cover_path, pagesize=A4)
    _cover_page(c)
    c.save()

    # Body
    doc = MemoTemplate(body_path)
    story = build_story()
    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)

    # Merge
    from pypdf import PdfWriter, PdfReader
    writer = PdfWriter()
    for path in [cover_path, body_path]:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(OUT, 'wb') as f:
        writer.write(f)

    # Cleanup
    os.remove(cover_path)
    os.remove(body_path)
    print(f'Saved: {OUT}')

if __name__ == '__main__':
    main()
