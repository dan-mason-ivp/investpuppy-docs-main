"""
WP-07 Technical Architecture — Full branded rebuild
Follows brand-build-specification.pdf exactly.
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
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, NextPageTemplate,
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
import os

# ── Brand constants (from brand-build-specification.pdf) ──────────────────────
BG         = colors.HexColor('#0A0A0F')
PLATINUM   = colors.HexColor('#E8E8EC')
GOLD       = colors.HexColor('#C8A96E')
OFF_WHITE  = colors.HexColor('#E8E2D9')
WARM_GREY  = colors.HexColor('#9A9086')
RULE_MAJ   = colors.HexColor('#5A5A60')   # section dividers — NOT gold
RULE_MIN   = colors.HexColor('#2A2828')   # minor rules
CARD_BG    = colors.HexColor('#111116')
NOTE_BG    = colors.HexColor('#16161A')
CARD_EDGE  = colors.HexColor('#242428')

# ── Page constants ─────────────────────────────────────────────────────────────
W, H       = A4
MARGIN_L   = 22*mm
MARGIN_R   = 22*mm
MARGIN_T1  = 16*mm   # cover/first pages
MARGIN_T2  = 46*mm   # later pages WITH persistent header — MUST be 46mm
MARGIN_B   = 20*mm
COL_W      = W - MARGIN_L - MARGIN_R

LOGO_PATH  = '/home/claude/vk2-work/VEKTOR-transparent-v3.png'
DOC_DATE   = 'May 2026'
DOC_REF    = 'IP-WP-ARCH-260501-1.0'
DOC_SUBTITLE = 'Production Infrastructure: Technical Architecture'
DOC_AUDIENCE = 'For technical due diligence teams, CTOs, and institutional partners'


# ── Styles ────────────────────────────────────────────────────────────────────
def build_styles():
    S = {}

    # Cover
    S['cover_label'] = ParagraphStyle('cover_label',
        fontName='Helvetica', fontSize=7, textColor=WARM_GREY,
        alignment=TA_CENTER, leading=11, spaceAfter=6, letterSpacing=4)

    S['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=24, textColor=PLATINUM,
        alignment=TA_CENTER, leading=30, spaceAfter=0)

    S['cover_distil'] = ParagraphStyle('cover_distil',
        fontName='Helvetica-Oblique', fontSize=11, textColor=WARM_GREY,
        alignment=TA_CENTER, leading=19, spaceAfter=0)

    # Section headings
    S['section_tag'] = ParagraphStyle('section_tag',
        fontName='Helvetica', fontSize=7, textColor=WARM_GREY,
        leading=11, spaceAfter=4, letterSpacing=4)

    S['section_title'] = ParagraphStyle('section_title',
        fontName='Helvetica-Bold', fontSize=18, textColor=PLATINUM,
        leading=24, spaceAfter=6, spaceBefore=0)

    S['section_sub'] = ParagraphStyle('section_sub',
        fontName='Helvetica-Oblique', fontSize=11, textColor=WARM_GREY,
        leading=17, spaceAfter=10)

    S['sub_head'] = ParagraphStyle('sub_head',
        fontName='Helvetica-Bold', fontSize=8.5, textColor=WARM_GREY,
        leading=13, spaceAfter=5, spaceBefore=16, letterSpacing=2)

    # Body text
    S['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=9.5, textColor=OFF_WHITE,
        leading=17, spaceAfter=10, alignment=TA_JUSTIFY)

    S['body_grey'] = ParagraphStyle('body_grey',
        fontName='Helvetica', fontSize=9.5, textColor=WARM_GREY,
        leading=17, spaceAfter=10, alignment=TA_JUSTIFY)

    # White paper specific
    S['wp_section'] = ParagraphStyle('wp_section',
        fontName='Helvetica-Bold', fontSize=14, textColor=PLATINUM,
        leading=20, spaceAfter=6, spaceBefore=8)

    S['wp_subsection'] = ParagraphStyle('wp_subsection',
        fontName='Helvetica-Bold', fontSize=11, textColor=GOLD,
        leading=16, spaceAfter=5, spaceBefore=12)

    S['wp_lead'] = ParagraphStyle('wp_lead',
        fontName='Helvetica-Oblique', fontSize=10, textColor=WARM_GREY,
        leading=16, spaceAfter=10, alignment=TA_JUSTIFY)

    # Abstract / KT
    S['abstract_tag'] = ParagraphStyle('abstract_tag',
        fontName='Helvetica', fontSize=7, textColor=WARM_GREY,
        leading=11, spaceAfter=6, letterSpacing=4)

    S['kt_item'] = ParagraphStyle('kt_item',
        fontName='Helvetica', fontSize=9.5, textColor=OFF_WHITE,
        leading=17, spaceAfter=8, leftIndent=0, alignment=TA_JUSTIFY)

    # Table styles
    S['tbl_hdr'] = ParagraphStyle('tbl_hdr',
        fontName='Helvetica-Bold', fontSize=7.5, textColor=PLATINUM,
        leading=11)

    S['tbl_label'] = ParagraphStyle('tbl_label',
        fontName='Helvetica-Bold', fontSize=8.5, textColor=OFF_WHITE,
        leading=13)

    S['tbl_body'] = ParagraphStyle('tbl_body',
        fontName='Helvetica', fontSize=8.5, textColor=OFF_WHITE,
        leading=13, alignment=TA_JUSTIFY)

    S['tbl_body_sm'] = ParagraphStyle('tbl_body_sm',
        fontName='Helvetica', fontSize=8, textColor=WARM_GREY,
        leading=12, alignment=TA_JUSTIFY)

    S['tbl_group'] = ParagraphStyle('tbl_group',
        fontName='Helvetica-Bold', fontSize=7.5, textColor=GOLD,
        leading=11, spaceAfter=4, letterSpacing=2)

    # Footer / refs
    S['footer'] = ParagraphStyle('footer',
        fontName='Helvetica', fontSize=6.5, textColor=colors.HexColor('#444440'),
        leading=10, alignment=TA_CENTER)

    S['wp_ref'] = ParagraphStyle('wp_ref',
        fontName='Helvetica', fontSize=7.5, textColor=colors.HexColor('#555550'),
        leading=11, alignment=TA_CENTER)

    S['xref'] = ParagraphStyle('xref',
        fontName='Helvetica', fontSize=8.5, textColor=WARM_GREY,
        leading=14, alignment=TA_CENTER)

    return S


# ── Flowables ─────────────────────────────────────────────────────────────────
class HRule(Flowable):
    def __init__(self, width, color=RULE_MIN, thickness=0.5,
                 spaceAbove=5, spaceBelow=5):
        Flowable.__init__(self)
        self.rule_width = width
        self.color = color
        self.thickness = thickness
        self._spaceAbove = spaceAbove
        self._spaceBelow = spaceBelow
        self.height = spaceAbove + thickness + spaceBelow

    def wrap(self, w, h):
        return self.rule_width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        y = self._spaceBelow + self.thickness / 2
        self.canv.line(0, y, self.rule_width, y)
        self.canv.restoreState()


class NoteBox(Flowable):
    """Editorial aside with left platinum bar — matches brand spec."""
    def __init__(self, width, text, style,
                 bg=NOTE_BG, bar_color=RULE_MAJ,
                 pad_h=15, pad_v=13, bar=4):
        Flowable.__init__(self)
        self.bw = width
        self.text = text
        self.style = style
        self.bg = bg
        self.bar_color = bar_color
        self.pad_h = pad_h
        self.pad_v = pad_v
        self.bar = bar
        inner_w = width - bar - pad_h * 2
        self._para = Paragraph(text, style)
        self._inner_w = inner_w

    def wrap(self, avail_w, avail_h):
        _, th = self._para.wrap(self._inner_w, avail_h)
        self.height = th + self.pad_v * 2
        return self.bw, self.height

    def draw(self):
        c = self.canv
        c.saveState()
        # background with rounded corners
        c.setFillColor(self.bg)
        c.setStrokeColor(CARD_EDGE)
        c.setLineWidth(0.4)
        c.roundRect(0, 0, self.bw, self.height, 3, fill=1, stroke=1)
        # left bar
        c.setFillColor(self.bar_color)
        c.setStrokeColor(self.bar_color)
        c.roundRect(0, 0, self.bar, self.height, 2, fill=1, stroke=0)
        # text
        x = self.bar + self.pad_h
        y = self.pad_v
        self._para.wrap(self._inner_w, self.height)
        self._para.drawOn(c, x, y)
        c.restoreStore = None
        c.restoreState()


def SvcTable(width, rows, col_widths, S):
    """Service inventory table — dark themed. Returns a splittable Table."""
    header = [
        Paragraph('SERVICE', S['tbl_hdr']),
        Paragraph('ROLE IN VEKTOR', S['tbl_hdr']),
        Paragraph('DESIGN RATIONALE', S['tbl_hdr']),
    ]
    data = [header] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [CARD_BG, colors.HexColor('#0F0F14')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, RULE_MIN),
        ('BOX', (0, 0), (-1, -1), 0.4, CARD_EDGE),
        ('LINEAFTER', (0, 0), (0, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (1, 0), (1, -1), 0.3, RULE_MIN),
    ]))
    return t


def FlowTable(width, headers, rows, col_widths, S):
    """Generic dark table. Returns a splittable Table."""
    hrow = [Paragraph(h, S['tbl_hdr']) for h in headers]
    data = [hrow] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [CARD_BG, colors.HexColor('#0F0F14')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, RULE_MIN),
        ('BOX', (0, 0), (-1, -1), 0.4, CARD_EDGE),
        ('LINEAFTER', (0, 0), (0, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (1, 0), (1, -1), 0.3, RULE_MIN),
    ]))
    return t


# ── Page templates ─────────────────────────────────────────────────────────────
def draw_cover(canvas, doc):
    canvas.saveState()
    # Full bleed dark background
    canvas.setFillColor(BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)

    from reportlab.lib.utils import ImageReader
    try:
        img = ImageReader(LOGO_PATH)
        iw, ih = img.getSize()
        lw = min(W * 0.62, 320)
        lh = lw * ih / iw
        lx = (W - lw) / 2
        # ly = bottom of logo (brand spec: ly = H × 0.52)
        ly = H * 0.52
        canvas.drawImage(LOGO_PATH, lx, ly - lh, lw, lh,
                         mask='auto', preserveAspectRatio=True)

        # Gold rule just below logo
        rule_y = ly - lh - 14
        canvas.setStrokeColor(GOLD)
        canvas.setLineWidth(0.8)
        canvas.line(MARGIN_L, rule_y, W - MARGIN_R, rule_y)

        # Series label below rule
        canvas.setFont('Helvetica', 7)
        canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W / 2, rule_y - 14, 'VEKTOR RESEARCH SERIES · 2026')

        # Title below series label (Helvetica-Bold 24pt PLATINUM)
        title_y = rule_y - 44
        canvas.setFont('Helvetica-Bold', 24)
        canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W / 2, title_y, 'The Vektor Technical')
        canvas.drawCentredString(W / 2, title_y - 30, 'Architecture')

        # Distillation line (Helvetica-Oblique 11pt WARM_GREY)
        canvas.setFont('Helvetica-Oblique', 10)
        canvas.setFillColor(WARM_GREY)
        distil1 = 'AWS services, architectural decisions, and design principles\u2014'
        distil2 = 'documented as a record of choices made, not a list of technologies used.'
        canvas.drawCentredString(W / 2, title_y - 58, distil1)
        canvas.drawCentredString(W / 2, title_y - 72, distil2)

    except Exception as e:
        print(f"Logo error: {e}")
        canvas.setFont('Helvetica-Bold', 24)
        canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W / 2, H / 2, 'VEKTOR')

    # Bottom section — RULE_MAJ separator at y=36mm
    canvas.setStrokeColor(RULE_MAJ)
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN_L, 36*mm, W - MARGIN_R, 36*mm)

    # Audience at 28mm
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(WARM_GREY)
    canvas.drawCentredString(W / 2, 28*mm, DOC_AUDIENCE)

    # Reference at 22mm
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W / 2, 22*mm,
        f'Vektor Research Series  ·  {DOC_REF}  ·  Copyright 2026')

    # Date at 16mm
    canvas.drawCentredString(W / 2, 16*mm, DOC_DATE)

    canvas.restoreState()


def draw_first(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    _draw_footer(canvas, doc)
    canvas.restoreState()


def draw_later(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    _draw_persistent_header(canvas, doc)
    _draw_footer(canvas, doc)
    canvas.restoreState()


def _draw_persistent_header(canvas, doc):
    """Brand spec: Logo h=22pt left, subtitle+page right, separator below."""
    from reportlab.lib.utils import ImageReader
    header_y = H - MARGIN_T2 + 14

    # Logo — height 22pt, width scales from PNG aspect ratio
    try:
        img = ImageReader(LOGO_PATH)
        iw, ih = img.getSize()
        lh = 22
        lw = lh * iw / ih
        canvas.drawImage(LOGO_PATH, MARGIN_L, header_y,
                         lw, lh, mask='auto', preserveAspectRatio=True)
    except Exception:
        canvas.setFont('Helvetica-Bold', 9)
        canvas.setFillColor(PLATINUM)
        canvas.drawString(MARGIN_L, header_y + 4, 'VEKTOR')

    # Page subtitle + number right-aligned — brand spec: Helvetica 7pt #555550
    page_num = doc.page - 1   # cover is page 1, abstract is page 2 = "01"
    subtitle_str = f'{DOC_SUBTITLE}  ·  {page_num:02d}'
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawRightString(W - MARGIN_R, H - MARGIN_T2 + 18, subtitle_str)

    # Separator rule — 0.4pt RULE_MIN at y=H-MARGIN_T2+8
    canvas.setStrokeColor(RULE_MIN)
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN_L, H - MARGIN_T2 + 8, W - MARGIN_R, H - MARGIN_T2 + 8)


def _draw_footer(canvas, doc):
    """Brand spec: 0.3pt RULE_MIN at y=MARGIN_B-2, text centred at MARGIN_B-11."""
    canvas.setStrokeColor(RULE_MIN)
    canvas.setLineWidth(0.3)
    canvas.line(MARGIN_L, MARGIN_B - 2, W - MARGIN_R, MARGIN_B - 2)

    footer_text = f'Vektor by InvestPuppy  ·  investpuppy.com  ·  {DOC_SUBTITLE}  ·  {DOC_DATE}'
    canvas.setFont('Helvetica', 6.5)
    canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawCentredString(W / 2, MARGIN_B - 11, footer_text)


# ── Content helpers ────────────────────────────────────────────────────────────
def section(num_label, title, subtitle, S):
    """Section header block."""
    items = []
    items.append(Paragraph(num_label, S['section_tag']))
    items.append(Paragraph(title, S['section_title']))
    if subtitle:
        items.append(Paragraph(subtitle, S['section_sub']))
    items.append(HRule(COL_W, color=RULE_MAJ, thickness=1.0, spaceAbove=2, spaceBelow=8))
    return items


def p(text, S, style='body'):
    return Paragraph(text, S[style])


def sp(n=8):
    return Spacer(1, n)


def hrule_major():
    return HRule(COL_W, color=RULE_MAJ, thickness=1.0, spaceAbove=6, spaceBelow=6)


def hrule_minor():
    return HRule(COL_W, color=RULE_MIN, thickness=0.3, spaceAbove=4, spaceBelow=3)


# ── Main build ────────────────────────────────────────────────────────────────
def build():
    out = '/home/claude/investpuppy/vektor/output/pdf/vk5-wp07-technical-architecture.pdf'
    S = build_styles()

    # Three frames
    frame_cover = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')

    frame_first = Frame(MARGIN_L, MARGIN_B, COL_W,
                        H - MARGIN_T1 - MARGIN_B, id='first')

    frame_later = Frame(MARGIN_L, MARGIN_B, COL_W,
                        H - MARGIN_T2 - MARGIN_B, id='later')

    tpl_cover = PageTemplate(id='Cover',  frames=[frame_cover], onPage=draw_cover)
    tpl_first = PageTemplate(id='First',  frames=[frame_first], onPage=draw_first)
    tpl_later = PageTemplate(id='Later',  frames=[frame_later], onPage=draw_later)

    doc = BaseDocTemplate(
        out, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T1, bottomMargin=MARGIN_B,
        title='WP-07 The Vektor Technical Architecture',
        author='InvestPuppy',
    )
    doc.addPageTemplates([tpl_cover, tpl_first, tpl_later])

    story = []

    # ── COVER ─────────────────────────────────────────────────────────────────
    # Page 1 auto-uses first template (Cover). All content drawn on canvas.
    # A tiny spacer registers the page, then we switch to First for page 2.
    story.append(Spacer(1, 1))
    story.append(NextPageTemplate('First'))
    story.append(PageBreak())

    # ── ABSTRACT PAGE (first template — no persistent header) ─────────────────
    story.append(Spacer(1, 0))

    story.append(p('ABSTRACT', S, 'abstract_tag'))
    story.append(NoteBox(COL_W,
        'Most vendor technical documentation is a list of services used. '
        'This paper is a record of decisions made \u2014 including the reasoning behind each one '
        'and what it would take to change them. '
        'This paper documents the Vektor production infrastructure through that lens: the architectural '
        'decisions made at the design stage, the reasoning behind each, and the properties those '
        'decisions produce\u2014modularity, scalability, and the ability to integrate with existing '
        'institutional infrastructure. The platform is currently deployed in Singapore (ap-southeast-1) '
        'for the initial SGX implementation. The architecture is region-agnostic by design: any AWS '
        'region can be configured as the deployment target without architectural change. Where '
        'capabilities are on the roadmap rather than live today, this paper says so directly.',
        S['body']))

    story.append(sp(16))
    story.append(p('KEY TAKEAWAYS', S, 'abstract_tag'))
    story.append(hrule_minor())
    story.append(sp(6))

    kts = [
        'Vektor runs on AWS using a microservices architecture. The current deployment is in ap-southeast-1 (Singapore). '
        'The architecture is region-agnostic \u2014 any AWS region can be configured as the deployment target. A client '
        'with UK or Hong Kong data residency requirements deploys to a different region; AWS data residency guarantees follow.',
        'SageMaker serves two distinct roles: JupyterLab research environment for universe screening, and a managed XGBoost '
        'inference endpoint for signal validation. These are separate concerns, treated separately.',
        'SQS decouples order generation from execution. A connectivity issue with IBKR does not cascade into the application layer.',
        'EventBridge + Step Functions provide observable, retryable workflow orchestration \u2014 producing an implicit audit trail '
        'for every automated operation.',
        'Cognito with Azure EntraID integration enables SSO for institutional firms running Microsoft 365 \u2014 designed in '
        'from the first prototype.',
        'The two-account AWS strategy (shared CI/CD + workload) means deploying to a new region is a CI/CD pipeline '
        'configuration, not an architecture change. CodePipeline in the shared account builds Docker images, pushes to ECR, '
        'and deploys cross-account to the workload account \u2014 making the region-agnostic claim concrete rather than aspirational.',
        'All infrastructure is defined in AWS CloudFormation. Every resource is version-controlled, reproducible, and auditable\u2014'
        'no manual console configuration exists in the production path.',
        'ECS services run on Fargate Spot capacity, delivering approximately 70% reduction in compute costs '
        'versus on-demand pricing. Compute is one component of total infrastructure cost; the saving is '
        'meaningful at scale and reflects deliberate infrastructure cost management.',
    ]
    for kt in kts:
        story.append(p(f'\u2014 {kt}', S, 'kt_item'))
        story.append(sp(2))

    story.append(sp(10))
    story.append(p(f'Reference: {DOC_REF}  \u00b7  Copyright 2026 InvestPuppy  \u00b7  investpuppy.com',
                   S, 'wp_ref'))

    story.append(NextPageTemplate('Later'))
    story.append(PageBreak())

    # ── SECTION 1 ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0))

    for item in section('1.', 'PLATFORM OVERVIEW',
        'What Vektor is built on, and why the infrastructure choices reflect the same design principles as the platform itself.',
        S):
        story.append(item)

    story.append(p(
        'Vektor is deployed on Amazon Web Services using a microservices architecture. The platform is currently '
        'running in ap-southeast-1 (Singapore), chosen as the deployment base for the initial SGX implementation '
        'and for alignment with the MAS regulatory context of the founding client base.',
        S))

    story.append(sp(6))
    story.append(NoteBox(COL_W,
        '<b>Region-agnostic by design.</b> Singapore (ap-southeast-1) is the current deployment region\u2014a '
        'configuration choice, not a structural dependency. A client with UK data residency requirements deploys '
        'to eu-west-2; Hong Kong to ap-east-1; US to us-east-1 or us-west-2. AWS data residency guarantees follow '
        'the region. The two-account CI/CD architecture means deploying to a new region is a pipeline configuration, '
        'not an architecture change.',
        S['body']))

    story.append(sp(10))
    story.append(p(
        'Three design principles were established before the first line of code was written. '
        '<b>Modularity:</b> every capability is an independently deployable service. '
        '<b>Scalability by default:</b> the infrastructure scales horizontally without architectural changes. '
        '<b>Governance before growth:</b> authentication, encryption, deployment pipeline separation, and operational '
        'visibility were designed in from the start.',
        S))

    story.append(sp(6))
    story.append(NoteBox(COL_W,
        '<b>Current deployment status.</b> The architecture described in this document is designed for institutional '
        'production. The current deployment is at prototype stage, running in ap-southeast-1 with IBKR connected '
        'to a simulation account. Section\u00a09 describes which specific capabilities are live today and which '
        'are on the near-term roadmap. The infrastructure designed today supports all described capabilities \u2014 '
        'implementing the roadmap items is configuration and integration work, not architectural change.',
        S['body']))

    story.append(PageBreak())

    # ── SECTION 2 ─────────────────────────────────────────────────────────────
    for item in section('2.', 'ARCHITECTURE DIAGRAM',
        'The complete Vektor AWS stack\u2014nine layers, colour-coded by user role. Read in conjunction with the decision log in Section 5.',
        S):
        story.append(item)

    # Architecture diagram as a dark layered table
    arch_body = ParagraphStyle('arch_body',
        fontName='Helvetica', fontSize=8, textColor=OFF_WHITE, leading=12)
    arch_label = ParagraphStyle('arch_label',
        fontName='Helvetica-Bold', fontSize=7.5, textColor=GOLD, leading=11)
    arch_sm = ParagraphStyle('arch_sm',
        fontName='Helvetica', fontSize=7.5, textColor=WARM_GREY, leading=11)

    layers = [
        ('USERS',
         'Stock Analyst  ·  Portfolio Manager  ·  Operations'),
        ('FRONTEND',
         'React Admin Portal (all three roles)  ·  AWS Amplify hosting + CI/CD'),
        ('API',
         'AWS API Gateway  ·  Single entry point  ·  Auth enforced  ·  Rate limiting on roadmap  ·  All ECS services exposed'),
        ('COMPUTE',
         'ECS Microservices (Python / Flask)  ·  ECS Service Connect: sub-100ms inter-service calls\n'
         'Fargate Spot: ~70% compute cost reduction  ·  Portfolio svc  ·  Allocation svc  ·  Data svc\n'
         'SageMaker: JupyterLab Research  +  XGBoost Endpoint'),
        ('MESSAGING',
         'SQS: Market order queue  ·  EventBridge: Scheduled triggers\n'
         'Step Functions: Workflow orchestration  ·  SNS + Lambda router: Operational notifications'),
        ('DATA',
         'RDS PostgreSQL  ·  Schema separation: market_data / portfolio_data / customer_data\n'
         'Equity prices + FX rates  ·  S3: Model artefacts + Backup'),
        ('EXECUTION',
         'EC2 t3.large: IBKR Gateway + SQS consumer  ·  IBKR API (Simulation \u2192 Live)\n'
         'EC2 t3.medium: Bastion host'),
        ('AUTH & SECURITY',
         'Cognito + Azure EntraID SSO  ·  KMS: Encryption at rest  ·  CloudWatch: Logging'),
        ('INFRASTRUCTURE',
         'AWS ap-southeast-1 (Singapore)  ·  Region-agnostic by design  ·  All infra in AWS CloudFormation\n'
         'Two-account strategy: CodePipeline + ECR (Shared CI/CD) \u2192 Workload  ·  Dev/prod by stack naming convention'),
    ]

    lbl_w = 28*mm
    content_w = COL_W - lbl_w

    for layer_name, content in layers:
        row_data = [[
            Paragraph(layer_name, arch_label),
            Paragraph(content.replace('\n', '<br/>'), arch_sm),
        ]]
        t = Table(row_data, colWidths=[lbl_w, content_w])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor('#1A1A20')),
            ('BACKGROUND', (1,0), (1,0), CARD_BG),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 7),
            ('RIGHTPADDING', (0,0), (-1,-1), 7),
            ('LINEBELOW', (0,0), (-1,-1), 0.3, RULE_MIN),
            ('LINEAFTER', (0,0), (0,-1), 0.3, RULE_MIN),
            ('BOX', (0,0), (-1,-1), 0.4, CARD_EDGE),
        ]))
        story.append(t)

    story.append(sp(8))
    story.append(p(
        'Current deployment: ap-southeast-1 (Singapore). Every layer is configurable to any AWS region '
        'without architectural changes. Dashed line indicates the SQS-mediated asynchronous path from '
        'ECS to the IBKR Gateway.',
        S, 'body_grey'))

    story.append(PageBreak())

    # ── SECTION 3 ─────────────────────────────────────────────────────────────
    for item in section('3.', 'AWS SERVICE INVENTORY',
        'Every AWS service in production use, its role, and design rationale.', S):
        story.append(item)

    cw3 = [32*mm, 44*mm, COL_W - 76*mm]

    def srow(label, role, rationale):
        return [p(label, S, 'tbl_label'), p(role, S, 'tbl_body'), p(rationale, S, 'tbl_body')]

    story.append(p('COMPUTE', S, 'tbl_group'))
    compute_rows = [
        srow('ECS (Fargate)',
             'All application microservices',
             'Container-native deployment\u2014each microservice is independently deployable and scalable. '
             'Fargate eliminates EC2 cluster management. '
             '<b>ECS Service Connect</b> handles inter-service communication via a local proxy that eliminates '
             'DNS lookup latency, providing consistent sub-100ms service-to-service calls. '
             '<b>Fargate Spot</b> is used for 80\u2013100% of ECS workloads, delivering approximately 70% '
             'reduction in compute costs versus on-demand pricing.'),
        srow('EC2 t3.medium', 'Bastion host',
             'Secure SSH access point for infrastructure administration. Isolated from the application layer.'),
        srow('EC2 t3.large', 'IBKR Gateway (SQS consumer)',
             'Interactive Brokers requires a persistent gateway process\u2014EC2 provides the stable, '
             'long-running process the IBKR API requires. Currently connected to IBKR simulation account.'),
        srow('SageMaker',
             'Two roles: (1)\u00a0JupyterLab research environment; (2)\u00a0XGBoost model training, versioning, managed inference endpoint',
             'Separating research from production inference is a governance decision. The notebook environment '
             'cannot directly affect production signals\u2014model promotion requires an explicit deployment step.'),
    ]
    story.append(SvcTable(COL_W, compute_rows, cw3, S))
    story.append(sp(10))

    story.append(p('DATA', S, 'tbl_group'))
    data_rows = [
        srow('RDS PostgreSQL',
             'Primary application DB + market data (equity prices, FX rates)',
             'Single relational database\u2014deliberate simplicity at prototype stage. ACID compliance '
             'important for allocation records forming the audit trail. '
             '<b>Schema separation:</b> three schemas\u2014market_data, portfolio_data, customer_data\u2014'
             'within a single RDS instance provide logical isolation today and a clear migration path to '
             'separate databases when scale requires it.'),
        srow('S3', 'Model artefacts + backup',
             'SageMaker model artefacts stored in S3 enable model versioning and rollback. Also serves as backup target for RDS snapshots.'),
    ]
    story.append(SvcTable(COL_W, data_rows, cw3, S))
    story.append(sp(10))

    story.append(PageBreak())

    story.append(p('INTEGRATION & MESSAGING', S, 'tbl_group'))
    integ_rows = [
        srow('API Gateway',
             'All ECS microservices exposed. Currently serves Admin Portal only.',
             'Single entry point enforces authentication and logging consistently. '
             '<b>Rate limiting and WAF protection are on the near-term roadmap\u2014not yet enforced.</b> '
             'External integrations (PMS, custodian) connect through the same gateway when added.'),
        srow('SQS', 'Market order queue between ECS and IBKR Gateway',
             'Decouples order generation from execution. If IBKR is temporarily unavailable, orders queue '
             'rather than fail. Order record exists in SQS before execution: a pre-execution audit trail.'),
        srow('EventBridge', 'Scheduled triggers (price download, market orders)',
             'Triggers Step Functions rather than Lambda directly\u2014provides observable, retryable '
             'workflow orchestration with per-step logging.'),
        srow('Step Functions', 'Workflow orchestration for scheduled operations',
             'Per-step logging, retry logic, visual workflow state. Each step is individually observable '
             'and retryable\u2014contributes to the audit trail.'),
        srow('SNS + Lambda router',
             'Notification fan-out architecture',
             'Services publish events to SNS without knowledge of notification targets. A Lambda-based '
             'router delivers to Slack today. The architecture supports future multi-platform delivery '
             '(email, Teams, webhooks) without changes to publishing services \u2014 notification '
             'channel decisions are operational, not architectural.'),
        srow('Slack', 'Current notification delivery target',
             'Receives operational notifications via SNS/Lambda router (orders, daily price download). '
             'CloudWatch alerting will supplement this as the platform moves toward production.'),
    ]
    story.append(SvcTable(COL_W, integ_rows, cw3, S))
    story.append(sp(10))

    story.append(p('AUTH, SECURITY & FRONTEND', S, 'tbl_group'))
    auth_rows = [
        srow('Cognito', 'User + client authentication, Azure EntraID federation',
             'Institutional firms using Microsoft 365 authenticate via existing SSO. Designed in from first '
             'prototype\u2014not retrofitted when required.'),
        srow('KMS', 'Primary encryption at rest',
             'AWS KMS for RDS and S3. All connections HTTPS/TLS. No unencrypted paths.'),
        srow('CloudWatch', 'Logging for all services',
             'Aggregates logs from ECS, API Gateway, Step Functions. Alerting and dashboards on near-term roadmap.'),
        srow('Amplify', 'React Admin Portal hosting + CI/CD',
             'Connects to CI/CD pipeline. Handles frontend deployment automatically on merge to main.'),
    ]
    story.append(SvcTable(COL_W, auth_rows, cw3, S))

    story.append(PageBreak())

    # ── SECTION 4 ─────────────────────────────────────────────────────────────
    for item in section('4.', 'ARCHITECTURE \u2014 DATA FLOWS',
        'How data moves through the platform\u2014from market data ingestion through portfolio construction to order execution.',
        S):
        story.append(item)

    story.append(p('FLOW\u00a01 \u2014 DAILY MARKET DATA PIPELINE (AUTOMATED)', S, 'wp_subsection'))
    story.append(sp(4))

    cw4a = [24*mm, 36*mm, COL_W - 60*mm]
    f1_rows = [
        [p('08:00 SGT', S, 'tbl_label'), p('EventBridge', S, 'tbl_body'),
         p('Scheduled trigger fires\u2014daily price download workflow', S, 'tbl_body')],
        [p('08:00 SGT', S, 'tbl_label'), p('Step Functions', S, 'tbl_body'),
         p('Workflow initiates\u2014per-step logging begins', S, 'tbl_body')],
        [p('08:01 SGT', S, 'tbl_label'), p('ECS data svc', S, 'tbl_body'),
         p('Equity prices fetched for all configured instruments', S, 'tbl_body')],
        [p('08:02 SGT', S, 'tbl_label'), p('ECS data svc', S, 'tbl_body'),
         p('FX rates fetched for all configured currency pairs', S, 'tbl_body')],
        [p('08:03 SGT', S, 'tbl_label'), p('RDS PostgreSQL', S, 'tbl_body'),
         p('Price and FX records written\u20143 years daily history maintained', S, 'tbl_body')],
        [p('08:04 SGT', S, 'tbl_label'), p('SNS \u2192 Lambda \u2192 Slack', S, 'tbl_body'),
         p('Event published to SNS; Lambda router delivers to Slack: daily price download complete', S, 'tbl_body')],
    ]
    story.append(FlowTable(COL_W, ['TIME', 'SERVICE', 'ACTION'], f1_rows, cw4a, S))

    story.append(sp(12))
    story.append(p('FLOW\u00a02 \u2014 RESEARCH TO STRATEGY TO FUNDED POSITIONS', S, 'wp_subsection'))
    story.append(sp(4))

    cw4b = [28*mm, 40*mm, COL_W - 68*mm]
    f2_rows = [
        [p('Research', S, 'tbl_label'),
         p('SageMaker JupyterLab', S, 'tbl_body'),
         p('Analyst: universe screening (500+\u2009\u2192\u2009target). '
           '<b>Portfolio optimisation:</b> 10,000 portfolio configurations generated to map the efficient frontier; '
           'Modern Portfolio Theory (PyPortfolioOpt) identifies the maximum Sharpe ratio portfolio from the mapped space. '
           '<b>Technical indicator backtesting and selection</b> across six indicator types (SMA, EMA, RSI, '
           'MACD, Bollinger Bands, Stochastic Oscillator)\u2014system backtests each indicator per instrument '
           'and selects the best performer. XGBoost validation via SageMaker endpoint.',
           S, 'tbl_body')],
        [p('Strategy record', S, 'tbl_label'),
         p('ECS \u2192 RDS', S, 'tbl_body'),
         p('Outputs written to DB: instruments, weights, indicators, Sharpe ratios. Status: pending PM approval.',
           S, 'tbl_body')],
        [p('Strategy approval', S, 'tbl_label'),
         p('Admin Portal \u2192 API GW \u2192 ECS \u2192 RDS', S, 'tbl_body'),
         p('PM reviews complete strategy. Approval writes audit record: PM identity + timestamp + strategy ID. '
           '<b>Maker/checker approval workflow with RBAC enforcement is planned for the next prototype iteration. '
           'Current implementation allows the PM to assign strategies directly.</b>',
           S, 'tbl_body')],
        [p('Client onboarding', S, 'tbl_label'),
         p('Admin Portal \u2192 API GW \u2192 ECS \u2192 RDS', S, 'tbl_body'),
         p('PM creates client profile, assigns approved strategy, sets mandate capital. Separate action from strategy approval.',
           S, 'tbl_body')],
        [p('Allocation', S, 'tbl_label'),
         p('ECS \u2192 RDS \u2192 ECS \u2192 RDS', S, 'tbl_body'),
         p('Allocation service fetches live prices, applies lot rounding, calculates position set. PM confirms. Audit record written.',
           S, 'tbl_body')],
        [p('Cash funding', S, 'tbl_label'),
         p('Admin Portal \u2192 API GW \u2192 ECS \u2192 RDS', S, 'tbl_body'),
         p('Operations records wire: currency, amount, reference. Cash account activated. Audit record written.',
           S, 'tbl_body')],
        [p('Order execution', S, 'tbl_label'),
         p('ECS \u2192 SQS \u2192 EC2 \u2192 IBKR API', S, 'tbl_body'),
         p('Trade instructions queued in SQS. IBKR Gateway polls and submits. Currently: simulation account. '
           'SNS publishes completion event; Lambda router delivers Slack notification.',
           S, 'tbl_body')],
    ]
    story.append(FlowTable(COL_W, ['STAGE', 'SERVICES', 'DETAIL'], f2_rows, cw4b, S))

    # Visual evidence — Step Functions workflow and Slack notification
    story.append(sp(10))
    from reportlab.platypus import Image as RLImage
    from reportlab.lib.utils import ImageReader

    for sc_file, caption in [
        ('sc15_order_workflow.png',
         'AWS Step Functions order workflow \u2014 the complete pipeline from GetActiveStrategies through '
         'MLValidation to GenerateOrders, with explicit state handling for NoStrategies, NoPortfolios, '
         'MLBlocked, LowConfidence, SignalApproved, and SkipPosition outcomes.'),
        ('sc16_slack_signals.png',
         'InvestPuppy Trading Bot in the #trading-signals Slack channel \u2014 live signal summary showing '
         'Approved, ML Blocked, and Low Confidence signals per portfolio. '
         'The notification is generated automatically by the SNS\u2192Lambda router after each execution cycle.'),
    ]:
        sc_path = _os.path.join(_SCREENSHOTS, sc_file)
        try:
            ir = ImageReader(sc_path); iw, ih = ir.getSize()
            w = COL_W; h = w * ih / iw
            story.append(p('PLATFORM EVIDENCE', S, 'tbl_label'))
            story.append(RLImage(sc_path, width=w, height=h))
            story.append(sp(4))
            story.append(p(caption, S, 'body_grey'))
            story.append(sp(8))
        except Exception as e:
            print(f'Screenshot {sc_file}: {e}')

    story.append(PageBreak())

    # ── SECTION 5 ─────────────────────────────────────────────────────────────
    for item in section('5.', 'THE DECISION LOG',
        'Architectural decisions made at the design stage. Read in conjunction with the architecture diagram in Section\u00a02.',
        S):
        story.append(item)

    cw5 = [44*mm, 38*mm, COL_W - 82*mm]

    def drow(decision, alt, reason):
        return [p(decision, S, 'tbl_label'), p(alt, S, 'tbl_body'), p(reason, S, 'tbl_body')]

    dec_rows = [
        drow('ECS for all microservices', 'Single EC2 monolith',
             'Each service updates, scales, and restarts independently. A bug in the allocation service does not require redeploying the data service.'),
        drow('ECS Service Connect\nfor inter-service comms', 'Standard DNS service discovery',
             'Local proxy eliminates DNS lookup latency, providing consistent sub-100ms service-to-service calls '
             'without requiring a separate service mesh infrastructure component.'),
        drow('Fargate Spot for ECS compute', 'Fargate on-demand',
             '80\u2013100% Fargate Spot capacity delivers approximately 70% reduction in compute costs versus '
             'on-demand pricing. Compute cost is one component of total infrastructure cost; the saving is '
             'meaningful at scale without requiring architectural changes.'),
        drow('SQS between ECS and IBKR Gateway', 'Direct API call from ECS to IBKR',
             'Direct calls create a hard dependency\u2014if IBKR is unreachable, the flow fails. SQS decouples generation from '
             'execution. Order record exists in SQS before execution: a pre-execution audit trail.'),
        drow('EventBridge + Step Functions', 'Cron-triggered Lambda',
             'Step Functions provides per-step logging, retry logic, visual workflow state. A Lambda cron produces one log entry; '
             'Step Functions produces a complete workflow audit trail.'),
        drow('SageMaker endpoint for XGBoost', 'Model embedded in ECS microservice',
             'Managed endpoint allows model versioning and rollback independently of the application deployment. '
             'Model governance requires these concerns to be separated.'),
        drow('Cognito + Azure EntraID', 'Application-layer username/password',
             'Institutional firms expect SSO. Designed in from first prototype\u2014not added when an enterprise client required it.'),
        drow('Two-account AWS strategy\n(Shared CI/CD + Workload)', 'Single AWS account',
             'Separates deployment pipeline from application environment. CodePipeline in the shared account builds Docker images, '
             'pushes to ECR, and deploys cross-account to the workload account\u2014this is the mechanism that makes the '
             'region-agnostic claim concrete. Current prototype uses a single workload account with environment separation by '
             'naming convention (dev/prod stacks). For production clients, separate workload accounts per environment or per client '
             'can be provisioned; the pipeline targets a different account ID with no architectural change required.'),
        drow('AWS CloudFormation\nfor all infrastructure', 'Manual console configuration',
             'All infrastructure defined as code. Every resource is version-controlled, reproducible, and auditable. '
             'No manual console configuration exists in the production path. Directly supports the "deploying to a new region '
             'is a pipeline configuration" claim\u2014the CloudFormation stacks are the artefacts the pipeline deploys.'),
        drow('Singapore (ap-southeast-1)\nas primary region', 'US East or multi-region from day one',
             'Data residency aligned with initial SGX market and MAS regulatory context. '
             'Architecture is region-agnostic\u2014any region configurable without code change.'),
        drow('Single RDS with\nschema separation', 'Separate time-series DB for market data',
             'Deliberate simplicity at prototype stage. Three schemas\u2014market_data, portfolio_data, customer_data\u2014'
             'provide logical isolation within a single RDS instance. '
             'Logical schema separation organises data and enforces query boundaries; it is not equivalent to '
             'physical database separation for compliance-grade data isolation. Physical separation into distinct '
             'database instances is the defined migration path for production-scale multi-client deployments. '
             'A deferral with a defined trigger condition, not an oversight.'),
        drow('API Gateway as\nsingle entry point', 'Direct ECS service calls',
             'Authentication and logging enforced consistently today. Rate limiting and WAF protection on the near-term roadmap. '
             'External integrations connect through the same gateway\u2014no additional exposure surface created.'),
    ]
    story.append(FlowTable(COL_W, ['DECISION MADE', 'ALTERNATIVE CONSIDERED', 'REASON'], dec_rows, cw5, S))

    story.append(PageBreak())

    # ── SECTION 6 ─────────────────────────────────────────────────────────────
    for item in section('6.', 'MODULARITY AND INTEGRATION CAPABILITY',
        "How Vektor\u2019s architecture enables integration with existing institutional infrastructure\u2014as a complement, not a replacement.",
        S):
        story.append(item)

    story.append(p(
        'Each service is independently accessible via API Gateway. A client with an existing PMS does not need to '
        'replace it. Vektor operates as the quantitative construction and signal layer, passing outputs to existing '
        'execution and reconciliation infrastructure.',
        S))

    integrations = [
        ('Allocation table output',
         'Produces a complete position set\u2014symbol, target quantity, target value, assigned indicator\u2014as a '
         'database record retrievable via REST API. A PMS integration receives trade instructions in JSON. No file transfer.'),
        ('Market data access',
         'Equity price history and FX rates accessible via API Gateway. A client can call these endpoints directly, or '
         'substitute their own market data feed\u2014the allocation engine accepts prices as input parameters.'),
        ('Authentication federation',
         'Cognito + Azure EntraID means Microsoft 365 users authenticate via existing SSO. No separate credential management required.'),
        ('Audit log access',
         'Every action logged as a timestamped record in RDS, accessible via API. A compliance team can query the complete '
         'decision chain for any position without accessing the Admin Portal.'),
    ]
    for title, body in integrations:
        story.append(p(title, S, 'wp_subsection'))
        story.append(p(body, S))

    story.append(NoteBox(COL_W,
        '<b>Current status:</b> API Gateway serves the Admin Portal only\u2014no external integration is yet live. '
        'The API layer is production-ready for external integration. Connecting to a specific PMS or custodian is a '
        'scoped integration project, typically two to four weeks for a standard REST integration.',
        S['body']))

    story.append(PageBreak())

    # ── SECTION 7 ─────────────────────────────────────────────────────────────
    for item in section('7.', 'SECURITY AND DATA RESIDENCY',
        'Encryption, access control, and data localisation.', S):
        story.append(item)

    security = [
        ('Encryption at rest',
         'AWS KMS for RDS and S3. All client data, market data, allocation records, and model artefacts are encrypted at rest.'),
        ('Encryption in transit',
         'All connections HTTPS/TLS. API Gateway enforces HTTPS for all endpoints. No unencrypted data paths.'),
        ('Authentication and access control',
         'Cognito with Azure EntraID federation. Infrastructure-level RBAC planned for next prototype\u2014'
         'three-role model currently enforced at application layer.'),
        ('Data residency',
         'Current deployment: ap-southeast-1 (Singapore). Data does not leave the configured region. Clients with '
         'UK (eu-west-2), Hong Kong (ap-east-1), or US residency requirements deploy to the appropriate region\u2014'
         'data residency guarantees follow. Full commitments available to Proof Partners.'),
        ('Network isolation',
         'Services run within a VPC. Bastion host is the only SSH access point. API Gateway is the only '
         'public-facing application entry point. Full VPC architecture available on request.'),
    ]
    for title, body in security:
        story.append(p(title, S, 'wp_subsection'))
        story.append(p(body, S))

    story.append(PageBreak())

    # ── SECTION 8 ─────────────────────────────────────────────────────────────
    for item in section('8.', 'SCALABILITY',
        'Scaling was a design requirement, not a roadmap item.', S):
        story.append(item)

    scaling = [
        ('New regions without architecture changes',
         'The two-account CI/CD strategy\u2014CodePipeline building in the shared account and deploying '
         'cross-account via CloudFormation\u2014means deploying Vektor to a new AWS region for a client in London, '
         'Dubai, or Hong Kong is a pipeline configuration. The shared account targets a different workload account '
         'and region; the CloudFormation stacks are the deployable artefacts.'),
        ('Horizontal scaling via ECS',
         'Each microservice scales horizontally. Adding mandates does not require architectural changes. Services '
         'scale independently. ECS Service Connect handles inter-service communication\u2014sub-100ms calls '
         'regardless of instance count.'),
        ('New markets without engine changes',
         'Exchange, benchmark, currency, and lot sizes are RDS configuration parameters. Adding a new listed '
         'equity market is a configuration change, not a code deployment.'),
        ('New clients in minutes',
         'Client onboarding is a database operation. The Cognito user pool scales to accommodate new users '
         'without infrastructure changes.'),
        ('SageMaker endpoint scaling',
         'The XGBoost inference endpoint scales independently of the application layer during strategy creation '
         'when signal validation calls are most frequent.'),
        ('Cost scaling discipline',
         'Fargate Spot capacity means compute costs scale proportionally rather than linearly\u2014the ~70% '
         'cost reduction versus on-demand is maintained as workloads grow.'),
    ]
    for title, body in scaling:
        story.append(p(title, S, 'wp_subsection'))
        story.append(p(body, S))

    story.append(PageBreak())

    # ── SECTION 9 ─────────────────────────────────────────────────────────────
    for item in section('9.', 'WHAT IS NOT YET IN SCOPE',
        'Honest current state\u2014and defined roadmap conditions.', S):
        story.append(item)

    not_in_scope = [
        ('Live trade execution',
         'IBKR Gateway currently connected to simulation account. Full order flow operational in simulation mode. '
         'Live execution on near-term roadmap.'),
        ('Infrastructure-level RBAC',
         'Three-role model enforced at application layer. Infrastructure-level RBAC (IAM roles aligned to '
         'three-role model) planned for next prototype iteration.'),
        ('Maker/checker approval workflow',
         'Strategy assignment currently allows the PM to act directly. Maker/checker workflow with RBAC '
         'enforcement\u2014requiring a separate checker to approve before a strategy is activated\u2014is planned '
         'for the next prototype iteration.'),
        ('API Gateway rate limiting and WAF',
         'Authentication and logging are enforced at API Gateway today. Rate limiting and WAF protection are '
         'on the near-term roadmap.'),
        ('Production observability',
         'CloudWatch logging is in place. Alerting and dashboards not yet implemented. SNS/Lambda routing to '
         'Slack provides operational visibility for key events. Full CloudWatch alerting on near-term roadmap.'),
        ('Production environment promotion',
         'Current workload runs in the dev environment (stack naming convention). Two-account CI/CD architecture '
         'is in place and operational. The workload will be promoted to a separate production AWS account before '
         'the first Proof Partner is onboarded\u2014a defined trigger condition, not an open-ended roadmap item.'),
        ('External API integrations',
         'All ECS microservices exposed via API Gateway and production-ready for external integration. No external '
         'PMS or custodian integration currently live. Integration with a specific external system is a scoped '
         'project, not an architectural change.'),
    ]
    for title, body in not_in_scope:
        story.append(p(title, S, 'wp_subsection'))
        story.append(p(body, S))

    story.append(sp(8))
    story.append(NoteBox(COL_W,
        'These are sequencing decisions, not architectural gaps. The infrastructure designed today supports all '
        'of these capabilities. Implementing them is configuration and integration work, not architectural change.',
        S['body']))

    story.append(PageBreak())

    # ── SECTION 10 ────────────────────────────────────────────────────────────
    for item in section('10.', 'CONCLUSION',
        'The architecture is not a collection of services\u2014it is a set of decisions, made in a specific sequence, for specific reasons.',
        S):
        story.append(item)

    story.append(p(
        'Singapore is the current deployment region\u2014a starting point, not a constraint. Any AWS region can '
        'be configured as the deployment target for a client with different data residency or regulatory requirements. '
        'The two-account CI/CD architecture\u2014CodePipeline, ECR, and CloudFormation stacks in a shared account '
        'deploying cross-account to the workload\u2014makes this a pipeline configuration, not a rebuild.',
        S))

    story.append(p(
        'The infrastructure choices documented here\u2014ECS with Service Connect and Fargate Spot, CloudFormation-defined '
        'stacks, SNS-decoupled notifications, schema-separated RDS\u2014reflect the same design principle applied '
        'consistently: build for production credibility from the first prototype, sequence implementations deliberately, '
        'and document what is live versus what is on the roadmap.',
        S))

    story.append(p(
        'Full technical documentation is available to Proof Partners as part of the due diligence process.',
        S))

    story.append(sp(16))
    story.append(HRule(COL_W, color=GOLD, thickness=0.8))
    story.append(sp(8))

    story.append(p(
        'For compliance and audit trail architecture, see WP-06. '
        'For AI and ML governance, see WP-08. '
        'For the platform overview, see the Platform Brochure. '
        'All documents at investpuppy.com.',
        S, 'xref'))

    story.append(sp(16))
    story.append(p(
        f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {DOC_REF}  \u00b7  Copyright 2026 InvestPuppy',
        S, 'wp_ref'))

    # ── BUILD ─────────────────────────────────────────────────────────────────
    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    result = subprocess.run(['pdfinfo', out], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'Pages' in line or 'File size' in line:
            print(line)


if __name__ == '__main__':
    build()
