"""
Vektor Founding Mandate Programme — standalone document
Full brand treatment matching the suite.
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

# ── Brand constants ────────────────────────────────────────────────────────────
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

W, H      = A4
ML = MR   = 22*mm
MT1       = 16*mm
MT2       = 46*mm
MB        = 20*mm
COL_W     = W - ML - MR

LOGO_PATH = '/home/claude/vk2-work/VEKTOR-transparent-v3.png'
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')
IP_H_RATIO = 2.337
DOC_DATE  = 'May 2026'
DOC_REF   = 'IP-FMP-260501-1.0'
DOC_SUB   = 'Founding Mandate Programme'


# ── Styles ─────────────────────────────────────────────────────────────────────
def styles():
    S = {}
    S['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=28, textColor=PLATINUM,
        alignment=TA_CENTER, leading=34, spaceAfter=0)
    S['cover_sub'] = ParagraphStyle('cover_sub',
        fontName='Helvetica-Oblique', fontSize=12, textColor=WARM_GREY,
        alignment=TA_CENTER, leading=18)
    S['section_tag'] = ParagraphStyle('section_tag',
        fontName='Helvetica', fontSize=7, textColor=WARM_GREY,
        leading=11, spaceAfter=4, letterSpacing=4)
    S['section_title'] = ParagraphStyle('section_title',
        fontName='Helvetica-Bold', fontSize=18, textColor=PLATINUM,
        leading=24, spaceAfter=6)
    S['section_sub'] = ParagraphStyle('section_sub',
        fontName='Helvetica-Oblique', fontSize=11, textColor=WARM_GREY,
        leading=17, spaceAfter=10)
    S['wp_subsection'] = ParagraphStyle('wp_subsection',
        fontName='Helvetica-Bold', fontSize=11, textColor=GOLD,
        leading=16, spaceAfter=5, spaceBefore=12)
    S['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=9.5, textColor=OFF_WHITE,
        leading=17, spaceAfter=10, alignment=TA_JUSTIFY)
    S['body_grey'] = ParagraphStyle('body_grey',
        fontName='Helvetica', fontSize=9.5, textColor=WARM_GREY,
        leading=17, spaceAfter=8, alignment=TA_JUSTIFY)
    S['abstract_tag'] = ParagraphStyle('abstract_tag',
        fontName='Helvetica', fontSize=7, textColor=WARM_GREY,
        leading=11, spaceAfter=6, letterSpacing=4)
    S['kt_item'] = ParagraphStyle('kt_item',
        fontName='Helvetica', fontSize=9.5, textColor=OFF_WHITE,
        leading=17, spaceAfter=8, alignment=TA_JUSTIFY)
    S['tbl_hdr'] = ParagraphStyle('tbl_hdr',
        fontName='Helvetica-Bold', fontSize=7.5, textColor=PLATINUM, leading=11)
    S['tbl_label'] = ParagraphStyle('tbl_label',
        fontName='Helvetica-Bold', fontSize=8.5, textColor=OFF_WHITE, leading=13)
    S['tbl_body'] = ParagraphStyle('tbl_body',
        fontName='Helvetica', fontSize=8.5, textColor=OFF_WHITE,
        leading=13, alignment=TA_JUSTIFY)
    S['tbl_gold'] = ParagraphStyle('tbl_gold',
        fontName='Helvetica-Bold', fontSize=8.5, textColor=GOLD, leading=13)
    S['footer'] = ParagraphStyle('footer',
        fontName='Helvetica', fontSize=6.5,
        textColor=colors.HexColor('#444440'),
        leading=10, alignment=TA_CENTER)
    S['wp_ref'] = ParagraphStyle('wp_ref',
        fontName='Helvetica', fontSize=7.5,
        textColor=colors.HexColor('#555550'),
        leading=11, alignment=TA_CENTER)
    S['xref'] = ParagraphStyle('xref',
        fontName='Helvetica', fontSize=8.5, textColor=WARM_GREY,
        leading=14, alignment=TA_CENTER)
    S['large_gold'] = ParagraphStyle('large_gold',
        fontName='Helvetica-Bold', fontSize=32, textColor=GOLD,
        alignment=TA_CENTER, leading=36)
    S['large_label'] = ParagraphStyle('large_label',
        fontName='Helvetica', fontSize=9, textColor=WARM_GREY,
        alignment=TA_CENTER, leading=13, letterSpacing=1)
    return S


# ── Flowables ──────────────────────────────────────────────────────────────────
class HRule(Flowable):
    def __init__(self, w, color=RULE_MIN, thickness=0.5, sa=5, sb=5):
        Flowable.__init__(self)
        self.rw = w; self.color = color; self.thickness = thickness
        self._sa = sa; self._sb = sb
        self.height = sa + thickness + sb
    def wrap(self, aw, ah): return self.rw, self.height
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        y = self._sb + self.thickness / 2
        self.canv.line(0, y, self.rw, y)


class NoteBox(Flowable):
    def __init__(self, width, text, style, bg=NOTE_BG, bar=RULE_MAJ,
                 ph=15, pv=13, bw=4):
        Flowable.__init__(self)
        self.bw_ = width; self.text = text; self.style = style
        self.bg = bg; self.bar = bar; self.ph = ph; self.pv = pv; self.bw = bw
        self._para = Paragraph(text, style)
        self._iw = width - bw - ph * 2
    def wrap(self, aw, ah):
        _, th = self._para.wrap(self._iw, ah)
        self.height = th + self.pv * 2
        return self.bw_, self.height
    def draw(self):
        c = self.canv; c.saveState()
        c.setFillColor(self.bg); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0, 0, self.bw_, self.height, 3, fill=1, stroke=1)
        c.setFillColor(self.bar); c.setStrokeColor(self.bar)
        c.roundRect(0, 0, self.bw, self.height, 2, fill=1, stroke=0)
        self._para.wrap(self._iw, self.height)
        self._para.drawOn(c, self.bw + self.ph, self.pv)
        c.restoreState()


class GoldBox(Flowable):
    """Full-width gold-bordered box for the CTA."""
    def __init__(self, width, children_flowables):
        Flowable.__init__(self)
        self.bw_ = width
        self.children = children_flowables
        self._pad = 18
    def wrap(self, aw, ah):
        inner = self.bw_ - self._pad * 2
        total_h = self._pad
        for f in self.children:
            _, fh = f.wrap(inner, ah)
            total_h += fh + 6
        total_h += self._pad
        self.height = total_h
        return self.bw_, self.height
    def draw(self):
        c = self.canv; c.saveState()
        c.setFillColor(colors.HexColor('#0D0C0A'))
        c.setStrokeColor(GOLD); c.setLineWidth(1.2)
        c.roundRect(0, 0, self.bw_, self.height, 4, fill=1, stroke=1)
        c.setStrokeColor(GOLD); c.setLineWidth(3)
        c.line(0, self.height - 1.5, self.bw_, self.height - 1.5)
        c.line(0, 1.5, self.bw_, 1.5)
        x = self._pad
        y = self.height - self._pad
        inner = self.bw_ - self._pad * 2
        for f in self.children:
            w, h = f.wrap(inner, self.height)
            y -= h
            f.drawOn(c, x, y)
            y -= 6
        c.restoreState()


# ── Page templates ─────────────────────────────────────────────────────────────
def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0, 0, W, H, fill=1, stroke=0)
    from reportlab.lib.utils import ImageReader
    try:
        img = ImageReader(LOGO_PATH)
        iw, ih = img.getSize()
        lw = min(W * 0.62, 320); lh = lw * ih / iw
        lx = (W - lw) / 2; ly = H * 0.52
        canvas.drawImage(LOGO_PATH, lx, ly - lh, lw, lh,
                         mask='auto', preserveAspectRatio=True)
        rule_y = ly - lh - 14
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8)
        canvas.line(ML, rule_y, W - MR, rule_y)
        canvas.setFont('Helvetica', 7); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2, rule_y - 14, 'VEKTOR BY INVESTPUPPY')
        # Document title
        canvas.setFont('Helvetica-Bold', 26); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2, rule_y - 48, 'Founding Mandate')
        canvas.drawCentredString(W/2, rule_y - 78, 'Programme')
        # Distillation
        canvas.setFont('Helvetica-Oblique', 10); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2, rule_y - 104,
            'A structured early-access partnership for institutional wealth management firms.')
    except Exception as e:
        print(f"Logo: {e}")
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4)
    canvas.line(ML, 36*mm, W - MR, 36*mm)
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(WARM_GREY)
    canvas.drawCentredString(W/2, 28*mm,
        'For prospective Founding Mandate partners only \u2014 strictly confidential')
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W/2, 22*mm,
        f'InvestPuppy  \u00b7  {DOC_REF}  \u00b7  Copyright 2026')
    canvas.drawCentredString(W/2, 16*mm, DOC_DATE)
    try:
        ip_w=38*mm; ip_h=ip_w/IP_H_RATIO
        canvas.drawImage(IP_H,ML,9*mm,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.restoreState()


def draw_first(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0, 0, W, H, fill=1, stroke=0)
    _footer(canvas)
    canvas.restoreState()


def draw_later(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0, 0, W, H, fill=1, stroke=0)
    _header(canvas, doc)
    _footer(canvas)
    canvas.restoreState()


def _header(canvas, doc):
    from reportlab.lib.utils import ImageReader
    hy = H - MT2 + 14
    try:
        img = ImageReader(LOGO_PATH)
        iw, ih = img.getSize()
        lh = 22; lw = lh * iw / ih
        canvas.drawImage(LOGO_PATH, ML, hy, lw, lh,
                         mask='auto', preserveAspectRatio=True)
    except:
        canvas.setFont('Helvetica-Bold', 9); canvas.setFillColor(PLATINUM)
        canvas.drawString(ML, hy + 4, 'VEKTOR')
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawRightString(W - MR, H - MT2 + 18,
        f'{DOC_SUB}  \u00b7  {doc.page - 1:02d}')
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.4)
    canvas.line(ML, H - MT2 + 8, W - MR, H - MT2 + 8)


def _footer(canvas):
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.3)
    canvas.line(ML, MB - 2, W - MR, MB - 2)
    canvas.setFont('Helvetica', 6.5)
    canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawCentredString(W/2, MB - 11,
        f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  {DOC_SUB}  \u00b7  {DOC_DATE}')


# ── Helpers ────────────────────────────────────────────────────────────────────
def sec(tag, title, sub, S):
    out = []
    out.append(Paragraph(tag, S['section_tag']))
    out.append(Paragraph(title, S['section_title']))
    if sub: out.append(Paragraph(sub, S['section_sub']))
    out.append(HRule(COL_W, RULE_MAJ, 1.0, 2, 8))
    return out

def p(text, S, st='body'): return Paragraph(text, S[st])
def sp(n=8): return Spacer(1, n)
def hr_maj(): return HRule(COL_W, RULE_MAJ, 1.0, 6, 6)
def hr_min(): return HRule(COL_W, RULE_MIN, 0.3, 4, 3)


def dark_table(headers, rows, col_widths, S):
    hrow = [Paragraph(h, S['tbl_hdr']) for h in headers]
    data = [hrow] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [CARD_BG, colors.HexColor('#0F0F14')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, RULE_MIN),
        ('BOX', (0, 0), (-1, -1), 0.4, CARD_EDGE),
        ('LINEAFTER', (0, 0), (0, -1), 0.3, RULE_MIN),
    ]))
    return t


# ── Build ──────────────────────────────────────────────────────────────────────
def build():
    out = '/home/claude/investpuppy/vektor/output/pdf/vk5-founding-mandate-programme.pdf'
    S = styles()

    f_cover = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                    topPadding=0, bottomPadding=0, id='cover')
    f_first = Frame(ML, MB, COL_W, H - MT1 - MB, id='first')
    f_later = Frame(ML, MB, COL_W, H - MT2 - MB, id='later')

    doc = BaseDocTemplate(out, pagesize=A4,
        leftMargin=ML, rightMargin=MR, topMargin=MT1, bottomMargin=MB,
        title='Vektor Founding Mandate Programme',
        author='InvestPuppy')
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[f_cover], onPage=draw_cover),
        PageTemplate(id='First', frames=[f_first], onPage=draw_first),
        PageTemplate(id='Later', frames=[f_later], onPage=draw_later),
    ])

    story = []

    # ── COVER ──────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1))
    story.append(NextPageTemplate('First'))
    story.append(PageBreak())

    # ── PAGE 2: PROGRAMME OVERVIEW ─────────────────────────────────────────────
    # Proof-of-concept opening — before programme description
    story.append(p('Show us a mandate. We’ll show you the platform.',
        S,'wp_subsection'))
    story.append(p('Pick any listed equity market, any currency, any benchmark. '
        'We will run the full Vektor workflow against it and show you the output: '
        'the efficient frontier, the correlation matrix, the max-Sharpe allocation, '
        'and the per-instrument signal selection. No slides. No promises. '
        'Just the platform, working on your data.',
        S))
    story.append(p('This is the Founding Mandate proposition: engage with the platform '
        'on your terms, using your data, before any commercial commitment is made.',
        S))
    story.append(Spacer(1,8))
    story.append(p(
        'We built what we wished existed. '
        'Now we want to build it further with the people it was built for.',
        S, 'wp_subsection'))
    story.append(Spacer(1,10))
    story.append(p('WHAT IS THE FOUNDING MANDATE PROGRAMME', S, 'abstract_tag'))
    story.append(NoteBox(COL_W,
        'The Founding Mandate Programme is a structured early-access partnership between Vektor and a small number of '
        'institutional wealth management firms. Founding Mandate partners are not beta testers. They are the firms '
        'alongside whom Vektor is being built into a production-grade platform \u2014 with direct access to the '
        'founding team, influence over the product roadmap, and commercial terms that reflect the value of that '
        'commitment. The programme has a defined number of slots. Once full, it closes.',
        S['body']))

    story.append(sp(14))
    story.append(p('WHY FOUNDING STAGE IS AN ADVANTAGE', S, 'abstract_tag'))
    story.append(hr_min())
    story.append(sp(6))

    advantages = [
        ('You shape the platform, not inherit it.',
         'Every production platform reflects the requirements of the clients who were there at the start. '
         'Founding Mandate partners define the workflows, approval structures, reporting formats, and integration '
         'priorities that the platform is built around. Partners who arrive later inherit those decisions.'),
        ('Commercial terms reflect your risk, not the market rate.',
         'Founding Mandate partners are committing before live production. The commercial terms reflect that '
         'commitment \u2014 not the pricing a platform commands once it has an established track record. '
         'Founding Mandate partners receive a 12-month founding rate of S$18,000/year — 25% below the standard entry tier — '
         'followed by permanent preferential pricing at one tier below their AUM tier. '
         'A partner whose AUM grows from S$75M to S$400M will pay the Growth tier rate, not the '
         'Institutional rate \u2014 permanently, for the duration of the relationship. '
         'The benefit scales with the partner\u2019s success. It does not expire.'),
        ('Direct access to the people building it.',
         'At founding stage, your team has direct access to the founding team \u2014 not a sales representative or '
         'a support ticket queue. Questions about methodology, architecture, and roadmap are answered by the people '
         'who wrote the code and the papers.'),
        ('Your mandate becomes the live track record.',
         'The first Founding Mandate produces the platform\u2019s live performance history. That track record '
         'belongs to both parties. A platform with a founding partner\u2019s mandates in live production is a '
         'fundamentally different proposition from a platform seeking its first client.'),
    ]
    for title, body in advantages:
        story.append(p(title, S, 'wp_subsection'))
        story.append(p(body, S))

    story.append(NextPageTemplate('Later'))
    story.append(PageBreak())

    # ── PAGE 3: WHAT THE PARTNER GETS ──────────────────────────────────────────
    for item in sec('1.', 'WHAT THE PARTNER RECEIVES',
        'Specific benefits of Founding Mandate status \u2014 commercial, operational, and strategic.', S):
        story.append(item)

    story.append(NoteBox(COL_W,
        'These are not standard vendor benefits. They reflect a specific reality: you are committing before '
        'the platform has a live track record. What follows is exactly what we are committing in return. '
        'The commercial terms are structured in two stages: a 12-month founding rate at S$18,000/year, '
        'then permanent preferential pricing at one tier below your AUM tier. '
        'The benefit is real, permanent, and scales with your growth.',
        S['body']))
    story.append(sp(10))

    benefits = [
        ('Preferential commercial terms \u2014 structured and permanent',
         'Founding Mandate pricing operates in two stages. Stage one: a 12-month founding rate of '
         'S$18,000/year \u2014 the founding rate, regardless of AUM. Stage two: from year four onwards, '
         'permanent preferential pricing at one tier below the partner\u2019s current AUM tier, '
         'with Entry tier (S$24,000/year) as the permanent floor. '
         'A Founding Mandate partner whose AUM grows to S$400M pays the Growth tier rate (S$48,000/year), '
         'not the Institutional rate (S$108,000/year) \u2014 permanently. '
         'The distinction between Founding Mandate partners and subsequent clients does not close. '
         'It reflects the commitment made at a specific moment in the platform\u2019s development.'),
        ('Direct roadmap influence',
         'Founding Mandate partners participate in structured quarterly roadmap sessions with the founding team. '
         'Partner requirements are tracked explicitly. Where a requirement applies across the platform, it is '
         'prioritised accordingly. Where it is specific to the founding partner\u2019s workflow, it is addressed '
         'as part of the mandate \u2014 this is what founding means.'),
        ('Priority onboarding and dedicated implementation support',
         'Founding Mandate partners receive dedicated implementation support from the founding team through '
         'the full onboarding process \u2014 platform configuration, data integration, workflow mapping, and '
         'user training. Implementation timelines are agreed at mandate signing and treated as commitments, '
         'not estimates.'),
        ('Full technical and compliance documentation',
         'The complete Vektor research series, architecture documentation, AI governance framework, risk '
         'disclosure, and compliance architecture are available in full to Founding Mandate partners as part '
         'of due diligence. Legal documentation, including data processing agreements and service level '
         'commitments, is provided before onboarding commences.'),
        ('Early access to new capabilities',
         'New platform capabilities \u2014 additional markets, enhanced reporting, expanded integration '
         'options, walk-forward validation \u2014 are available to Founding Mandate partners before general '
         'release. Partners have the option to participate in capability development or to receive new '
         'features as they are released.'),
        ('Recognition as a Founding Mandate partner',
         'Where a Founding Mandate partner chooses to be identified publicly, Vektor will acknowledge their '
         'founding status in appropriate contexts. Partners who prefer not to be identified publicly are not '
         'required to be. Founding Mandate partners who choose public recognition become part of the '
         'platform\u2019s story from the first chapter.'),
    ]
    for title, body in benefits:
        story.append(p(title, S, 'wp_subsection'))
        story.append(p(body, S))

    story.append(PageBreak())

    # ── PAGE 4: WHAT THE PARTNER COMMITS TO ────────────────────────────────────
    for item in sec('2.', 'WHAT THE PARTNER COMMITS TO',
        'The obligations of Founding Mandate status \u2014 stated directly.', S):
        story.append(item)

    story.append(NoteBox(COL_W,
        'The Founding Mandate is a genuine partnership, not a one-sided commercial arrangement. '
        'The partner\u2019s obligations are the reason the commercial terms are preferential. '
        'A founding partner who does not engage actively is not serving their own interests or the platform\u2019s. '
        'The following commitments are standard across all Founding Mandate arrangements.',
        S['body']))
    story.append(sp(10))

    obligations = [
        ('Minimum mandate commitment',
         'A Founding Mandate requires a minimum active mandate on the platform \u2014 specific AUM threshold '
         'agreed at signing, reflecting the partner\u2019s operational context. The mandate must be actively '
         'managed through the platform, not a dormant arrangement. The minimum commitment is the basis on '
         'which the commercial terms are structured.'),
        ('Active platform use through the founding period',
         'The founding period runs from onboarding through to the first production milestone \u2014 defined '
         'at mandate signing, typically twelve months. During this period, the partner commits to active '
         'platform use: running strategies, processing allocations, and using the audit trail as part of '
         'normal operational workflow rather than in parallel with existing systems.'),
        ('Structured feedback participation',
         'Founding Mandate partners participate in quarterly structured reviews with the founding team. '
         'These sessions cover platform performance, workflow friction, capability gaps, and roadmap priorities. '
         'Feedback does not need to be positive \u2014 it needs to be specific. The reviews are the primary '
         'mechanism by which partner requirements reach the development roadmap.'),
        ('Reference arrangement \u2014 subject to agreement',
         'Founding Mandate partners are asked \u2014 not required \u2014 to serve as a reference for prospective '
         'clients at an appropriate stage of the platform\u2019s development. The nature, timing, and '
         'scope of any reference arrangement is agreed separately and at the partner\u2019s discretion. '
         'Partners who prefer not to participate in reference arrangements retain full Founding Mandate '
         'benefits without exception.'),
    ]
    for title, body in obligations:
        story.append(p(title, S, 'wp_subsection'))
        story.append(p(body, S))

    story.append(PageBreak())

    # ── PAGE 5: PROGRAMME MECHANICS ────────────────────────────────────────────
    for item in sec('3.', 'PROGRAMME MECHANICS',
        'Slots, selection, timeline, and what happens after the founding period.', S):
        story.append(item)

    # Slots metric display
    slot_data = [
        [
            Paragraph('3', S['large_gold']),
            Paragraph('12', S['large_gold']),
            Paragraph('Defined', S['large_gold']),
        ],
        [
            Paragraph('total founding\nmandate slots', S['large_label']),
            Paragraph('month founding\nrate period', S['large_label']),
            Paragraph('production milestone\nbefore general release', S['large_label']),
        ],
    ]
    slot_t = Table(slot_data, colWidths=[COL_W/3]*3)
    slot_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LINEAFTER', (0,0), (1,-1), 0.3, RULE_MIN),
        ('BOX', (0,0), (-1,-1), 0.4, CARD_EDGE),
    ]))
    story.append(slot_t)
    story.append(sp(12))

    # Pricing outcomes table
    story.append(p('PRICING STRUCTURE', S, 'wp_subsection'))
    story.append(p(
        'Founding Mandate pricing operates in two stages. The founding rate of S$18,000/year applies '
        'for the first 12 months \u2014 25% below the standard entry tier, in recognition of the '
        'partner\u2019s commitment at the earliest stage of the platform\u2019s commercial history. '
        'From year two, the permanent preferential rate applies: one tier below the partner\u2019s '
        'current AUM tier, with Entry tier as the permanent floor.',
        S))
    story.append(sp(4))
    story.append(NoteBox(COL_W,
        'Vektor pricing is published openly and held consistently. It is not inflated to create '
        'negotiating room. Structured commercial flexibility exists for two defined reasons: '
        'multi-year subscription commitments, and reference partnerships where both parties '
        'receive something of genuine value. Outside those structures, the published rate applies. '
        'We set prices we can defend \u2014 and we defend them. '
        'This pricing policy applies consistently across all clients. '
        'That is what honest by design means in practice.',
        S['body']))

    price_hdr_style = ParagraphStyle('pfh', fontName='Helvetica-Bold', fontSize=8,
                                     textColor=OFF_WHITE, leading=12, alignment=1)
    price_cell_style = ParagraphStyle('pfc', fontName='Helvetica', fontSize=8,
                                      textColor=OFF_WHITE, leading=12)
    price_gold_style = ParagraphStyle('pfg', fontName='Helvetica-Bold', fontSize=8,
                                      textColor=GOLD, leading=12, alignment=1)
    price_grey_style = ParagraphStyle('pfgr', fontName='Helvetica', fontSize=8,
                                      textColor=WARM_GREY, leading=12)

    pricing_data = [
        [Paragraph('Client AUM', price_hdr_style),
         Paragraph('Standard tier', price_hdr_style),
         Paragraph('FM rate (from yr 2)', price_hdr_style),
         Paragraph('Annual saving', price_hdr_style)],
        [Paragraph('Stays \u2264S$75M',   price_cell_style),
         Paragraph('Entry  S$24,000',     price_grey_style),
         Paragraph('Entry  S$24,000',     price_gold_style),
         Paragraph('Floor (yr 2+)',       price_grey_style)],
        [Paragraph('Grows to S$150M',     price_cell_style),
         Paragraph('Growth  S$48,000',    price_grey_style),
         Paragraph('Entry  S$24,000',     price_gold_style),
         Paragraph('S$24,000 (50%)',      price_gold_style)],
        [Paragraph('Grows to S$400M',     price_cell_style),
         Paragraph('Institutional  S$108,000', price_grey_style),
         Paragraph('Growth  S$48,000',    price_gold_style),
         Paragraph('S$60,000 (56%)',      price_gold_style)],
        [Paragraph('Grows to S$1B+',      price_cell_style),
         Paragraph('Enterprise  S$168,000+', price_grey_style),
         Paragraph('Institutional  S$108,000', price_gold_style),
         Paragraph('S$60,000+ (36%+)',    price_gold_style)],
    ]
    cws = [COL_W*0.27, COL_W*0.24, COL_W*0.26, COL_W*0.23]
    price_tbl = Table(pricing_data, colWidths=cws)
    price_tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  CARD_BG),
        ('BACKGROUND',    (0,1), (-1,-1), NOTE_BG),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [NOTE_BG, CARD_BG]),
        ('GRID',          (0,0), (-1,-1), 0.3, RULE_MIN),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(price_tbl)
    story.append(sp(12))
    story.append(p(
        'The programme has a maximum of three Founding Mandate slots. Slot allocation follows '
        'the due diligence process \u2014 NDA signed, technical and compliance review completed, commercial '
        'terms agreed. Slots are not reserved on the basis of intent or preliminary interest. Once the '
        'programme reaches capacity, it closes to new partners. Subsequent clients join on standard '
        'commercial terms.',
        S))

    story.append(p('SELECTION CRITERIA', S, 'wp_subsection'))
    story.append(p(
        'Founding Mandate partners are selected on the basis of: operational fit (the platform addresses '
        'a real workflow requirement, not a theoretical one), institutional credibility (the partner operates '
        'at a scale and standard consistent with the platform\u2019s target positioning), and genuine '
        'partnership intent (the partner is willing to engage actively, not just subscribe). '
        'Geographic and market diversity across the founding cohort is a consideration \u2014 '
        'founding partners operating in different markets strengthen the platform\u2019s '
        'multi-market validation.',
        S))

    story.append(p('THE FOUNDING PERIOD', S, 'wp_subsection'))
    story.append(p(
        'The founding period is twelve months from onboarding completion. '
        'During this period, the partner\u2019s rate is fixed at S$18,000/year \u2014 '
        'the founding rate, 25% below the standard entry tier. '
        'The founding period milestone is defined at signing: typically, the first '
        'live mandate running in production with full audit trail, allocation, and order execution '
        'operational.',
        S))

    story.append(p('AFTER THE FOUNDING PERIOD', S, 'wp_subsection'))
    story.append(p(
        'From year two, pricing transitions to the permanent preferential structure: '
        'one tier below the partner\u2019s current AUM tier, with Entry tier (S$24,000/year) '
        'as the permanent floor. The transition is handled as a renewal conversation \u2014 '
        'InvestPuppy reviews the partner\u2019s current AUM together and sets the ongoing rate. '
        'A partner whose AUM remains below S$75M moves to Entry tier (S$24,000). '
        'A partner whose AUM has grown to S$150M moves to Entry tier (not Growth). '
        'A partner whose AUM has grown to S$400M moves to Growth tier (not Institutional). '
        'Roadmap participation, early access to new capabilities, and direct founding team engagement '
        'continue for the life of the relationship.',
        S))

    story.append(PageBreak())

    # ── PAGE 6: THE PATH TO PRODUCTION + CTA ───────────────────────────────────
    for item in sec('4.', 'THE PATH TO PRODUCTION',
        'Where the platform is today and the defined conditions for production promotion.', S):
        story.append(item)

    story.append(p(
        'The Vektor platform is live in prototype on AWS ap-southeast-1. The core workflow is operational: '
        'universe screening, portfolio optimisation, technical indicator selection, capital allocation, '
        'client onboarding, cash funding, and order preparation are all functional. IBKR is connected '
        'in simulation mode. The platform has not yet executed a live trade.',
        S))
    story.append(sp(4))

    # What's live / roadmap table
    status_rows = [
        [Paragraph('\u2713  Strategy creation and optimisation', S['tbl_body']),
         Paragraph('Live', S['tbl_gold'])],
        [Paragraph('\u2713  Client onboarding and portfolio setup', S['tbl_body']),
         Paragraph('Live', S['tbl_gold'])],
        [Paragraph('\u2713  Capital allocation at live prices', S['tbl_body']),
         Paragraph('Live', S['tbl_gold'])],
        [Paragraph('\u2713  Cash funding and audit trail', S['tbl_body']),
         Paragraph('Live', S['tbl_gold'])],
        [Paragraph('\u2713  Order preparation and SQS queuing', S['tbl_body']),
         Paragraph('Live', S['tbl_gold'])],
        [Paragraph('\u2713  Multi-currency FX infrastructure', S['tbl_body']),
         Paragraph('Live', S['tbl_gold'])],
        [Paragraph('\u25cb  Live trade execution (IBKR simulation \u2192 live)', S['tbl_body']),
         Paragraph('Roadmap', S['tbl_body'])],
        [Paragraph('\u25cb  Infrastructure RBAC and maker/checker workflow', S['tbl_body']),
         Paragraph('Roadmap', S['tbl_body'])],
        [Paragraph('\u25cb  API Gateway rate limiting and WAF', S['tbl_body']),
         Paragraph('Roadmap', S['tbl_body'])],
        [Paragraph('\u25cb  Walk-forward strategy validation', S['tbl_body']),
         Paragraph('Roadmap', S['tbl_body'])],
        [Paragraph('\u25cb  External PMS/custodian integration', S['tbl_body']),
         Paragraph('Roadmap', S['tbl_body'])],
    ]
    story.append(dark_table(['CAPABILITY', 'STATUS'], status_rows,
        [COL_W - 28*mm, 28*mm], S))
    story.append(sp(8))

    story.append(NoteBox(COL_W,
        '<b>Production promotion condition.</b> The platform will be promoted from prototype to the production '
        'AWS account before the first Founding Mandate client is onboarded into live trading. This is a '
        'defined trigger condition, not an open-ended roadmap item. The infrastructure to support this '
        'promotion is already in place \u2014 the two-account CI/CD architecture makes promotion a pipeline '
        'configuration, not an architectural change.',
        S['body']))

    story.append(sp(14))

    # CTA Box
    cta_children = [
        Paragraph('HOW TO PROCEED', ParagraphStyle('cta_tag',
            fontName='Helvetica', fontSize=7, textColor=GOLD,
            letterSpacing=3, alignment=TA_CENTER, spaceAfter=8)),
        Paragraph('Three steps from this document to a Founding Mandate.',
            ParagraphStyle('cta_sub', fontName='Helvetica-Oblique',
                fontSize=10, textColor=WARM_GREY, alignment=TA_CENTER,
                leading=15, spaceAfter=12)),
        Paragraph(
            '<b>Step 1 \u2014 NDA.</b> Execute the mutual non-disclosure agreement '
            '(vektor-mutual-nda.pdf). This is the prerequisite for sharing specific commercial terms '
            'and detailed technical documentation.',
            ParagraphStyle('cta_body', fontName='Helvetica', fontSize=9,
                textColor=OFF_WHITE, leading=15, alignment=TA_JUSTIFY,
                spaceAfter=8)),
        Paragraph(
            '<b>Step 2 \u2014 Due diligence.</b> Work through the Vektor research series using the '
            'DD Navigation Guide. The full technical architecture (WP-07), compliance framework (WP-06), '
            'AI governance (WP-08), and risk disclosure (WP-09) are available in full.',
            ParagraphStyle('cta_body2', fontName='Helvetica', fontSize=9,
                textColor=OFF_WHITE, leading=15, alignment=TA_JUSTIFY,
                spaceAfter=8)),
        Paragraph(
            '<b>Step 3 \u2014 Commercial discussion.</b> Once due diligence is complete, the '
            'founding team will present specific commercial terms for your context. '
            'Contact: contact@investpuppy.com',
            ParagraphStyle('cta_body3', fontName='Helvetica', fontSize=9,
                textColor=OFF_WHITE, leading=15, alignment=TA_JUSTIFY,
                spaceAfter=0)),
    ]
    story.append(GoldBox(COL_W, cta_children))

    story.append(sp(14))
    story.append(HRule(COL_W, GOLD, 0.8))
    story.append(sp(8))
    story.append(p(
        'For the full Vektor research series, platform brochure, and compliance documentation: '
        'investpuppy.com  \u00b7  contact@investpuppy.com',
        S, 'xref'))
    story.append(sp(10))
    story.append(p(
        f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {DOC_REF}  \u00b7  Copyright 2026 InvestPuppy',
        S, 'wp_ref'))

    # ── BUILD ──────────────────────────────────────────────────────────────────
    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    r = subprocess.run(['pdfinfo', out], capture_output=True, text=True)
    for line in r.stdout.split('\n'):
        if 'Pages' in line or 'File size' in line:
            print(line)

if __name__ == '__main__':
    build()
