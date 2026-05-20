"""
Outstanding Panel Recommendations Register
Internal document — dark-branded, structured as a work register.
Captures all deferred items from Stages 1–4 panel reviews.
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
RED_DIM   = colors.HexColor('#8B3A3A')
AMBER_DIM = colors.HexColor('#7A6020')
GREEN_DIM = colors.HexColor('#2A5A3A')
BLUE_DIM  = colors.HexColor('#1E3A5A')
PURP_DIM  = colors.HexColor('#3A1E5A')
RED_TXT   = colors.HexColor('#C87070')
AMBER_TXT = colors.HexColor('#C8A050')
GREEN_TXT = colors.HexColor('#70C890')
BLUE_TXT  = colors.HexColor('#70A8D0')
PURP_TXT  = colors.HexColor('#A870D0')

W, H = A4
ML = MR = 22*mm
MT1 = 16*mm; MT2 = 46*mm; MB = 20*mm
COL_W = W - ML - MR
LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png')
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')
IP_H_RATIO = 2.337
DATE = 'May 2026'
SUB = 'Outstanding Recommendations Register'
FOOTER = f'Vektor by InvestPuppy  \u00b7  INTERNAL USE ONLY  \u00b7  {DATE}'


def S():
    s = {}
    s['tag'] = ParagraphStyle('tag', fontName='Helvetica', fontSize=7,
        textColor=WARM_GREY, leading=11, spaceAfter=4, letterSpacing=4)
    s['section_title'] = ParagraphStyle('stit', fontName='Helvetica-Bold',
        fontSize=15, textColor=PLATINUM, leading=21, spaceAfter=5)
    s['section_sub'] = ParagraphStyle('ssub', fontName='Helvetica-Oblique',
        fontSize=10, textColor=WARM_GREY, leading=16, spaceAfter=10)
    s['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5,
        textColor=OFF_WHITE, leading=17, spaceAfter=8, alignment=TA_JUSTIFY)
    s['body_grey'] = ParagraphStyle('bgrey', fontName='Helvetica', fontSize=9.5,
        textColor=WARM_GREY, leading=17, spaceAfter=6, alignment=TA_JUSTIFY)
    s['cat_head'] = ParagraphStyle('chead', fontName='Helvetica-Bold', fontSize=8,
        textColor=GOLD, leading=12, letterSpacing=2, spaceAfter=6, spaceBefore=14)
    s['item_id'] = ParagraphStyle('iid', fontName='Helvetica-Bold', fontSize=8.5,
        textColor=GOLD, leading=12)
    s['item_title'] = ParagraphStyle('ititl', fontName='Helvetica-Bold', fontSize=9.5,
        textColor=PLATINUM, leading=14)
    s['item_body'] = ParagraphStyle('ibody', fontName='Helvetica', fontSize=8.5,
        textColor=OFF_WHITE, leading=13, alignment=TA_JUSTIFY)
    s['item_grey'] = ParagraphStyle('igrey', fontName='Helvetica', fontSize=8.5,
        textColor=WARM_GREY, leading=13, alignment=TA_JUSTIFY)
    s['item_trigger'] = ParagraphStyle('itrig', fontName='Helvetica-Bold', fontSize=8,
        textColor=WARM_GREY, leading=12)
    s['tbl_hdr'] = ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=7.5,
        textColor=PLATINUM, leading=11)
    s['tbl_body'] = ParagraphStyle('tb', fontName='Helvetica', fontSize=8.5,
        textColor=OFF_WHITE, leading=12, alignment=TA_JUSTIFY)
    s['tbl_id'] = ParagraphStyle('tid', fontName='Helvetica-Bold', fontSize=8.5,
        textColor=GOLD, leading=12)
    s['tbl_grey'] = ParagraphStyle('tg', fontName='Helvetica', fontSize=8,
        textColor=WARM_GREY, leading=12)
    s['status_p'] = ParagraphStyle('sp', fontName='Helvetica-Bold', fontSize=7.5,
        textColor=RED_TXT, leading=11, alignment=TA_CENTER)
    s['status_a'] = ParagraphStyle('sa', fontName='Helvetica-Bold', fontSize=7.5,
        textColor=AMBER_TXT, leading=11, alignment=TA_CENTER)
    s['status_g'] = ParagraphStyle('sg', fontName='Helvetica-Bold', fontSize=7.5,
        textColor=GREEN_TXT, leading=11, alignment=TA_CENTER)
    s['status_b'] = ParagraphStyle('sb', fontName='Helvetica-Bold', fontSize=7.5,
        textColor=BLUE_TXT, leading=11, alignment=TA_CENTER)
    s['status_u'] = ParagraphStyle('su', fontName='Helvetica-Bold', fontSize=7.5,
        textColor=PURP_TXT, leading=11, alignment=TA_CENTER)
    s['wp_ref'] = ParagraphStyle('wpr', fontName='Helvetica', fontSize=7.5,
        textColor=colors.HexColor('#555550'), alignment=TA_CENTER, leading=11)
    return s


class HRule(Flowable):
    def __init__(self, w, c=RULE_MIN, t=0.5, sa=4, sb=4):
        Flowable.__init__(self)
        self.rw = w; self.c = c; self.t = t; self._sa = sa; self._sb = sb
        self.height = sa + t + sb
    def wrap(self, aw, ah): return self.rw, self.height
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        self.canv.line(0, self._sb + self.t/2, self.rw, self._sb + self.t/2)


class NoteBox(Flowable):
    def __init__(self, w, text, style, bg=NOTE_BG, bar=RULE_MAJ, ph=14, pv=12, bw=4):
        Flowable.__init__(self)
        self._w = w; self.bg = bg; self.bar = bar; self.ph = ph; self.pv = pv; self.bw = bw
        self._p = Paragraph(text, style); self._iw = w - bw - ph * 2
    def wrap(self, aw, ah):
        _, h = self._p.wrap(self._iw, ah); self.height = h + self.pv * 2; return self._w, self.height
    def draw(self):
        c = self.canv; c.saveState()
        c.setFillColor(self.bg); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0, 0, self._w, self.height, 3, fill=1, stroke=1)
        c.setFillColor(self.bar); c.roundRect(0, 0, self.bw, self.height, 2, fill=1, stroke=0)
        self._p.wrap(self._iw, self.height); self._p.drawOn(c, self.bw + self.ph, self.pv)
        c.restoreState()


def status_pill(text, style):
    """Render a coloured status label."""
    return Paragraph(text, style)


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0, 0, W, H, fill=1, stroke=0)
    from reportlab.lib.utils import ImageReader
    import os
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), LOGO)
    if not os.path.exists(logo_path):
        logo_path = '/home/claude/vk2-work/VEKTOR-transparent-v3.png'
    try:
        img = ImageReader(logo_path); iw, ih = img.getSize()
        lw = min(W * 0.62, 320); lh = lw * ih / iw; lx = (W - lw) / 2; ly = H * 0.52
        canvas.drawImage(logo_path, lx, ly - lh, lw, lh, mask='auto', preserveAspectRatio=True)
        ry = ly - lh - 14
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8)
        canvas.line(ML, ry, W - MR, ry)
        canvas.setFont('Helvetica', 7); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2, ry - 14, 'INTERNAL REFERENCE')
        canvas.setFont('Helvetica-Bold', 22); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2, ry - 44, 'Outstanding Panel')
        canvas.drawCentredString(W/2, ry - 70, 'Recommendations Register')
        canvas.setFont('Helvetica-Oblique', 10); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2, ry - 94,
            'Deferred items from Stages 1\u20134 panel reviews \u2014 to be addressed as a separate exercise.')
    except Exception as e:
        print(e)
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4)
    canvas.line(ML, 36*mm, W - MR, 36*mm)
    canvas.setFont('Helvetica-Bold', 7.5); canvas.setFillColor(GOLD)
    canvas.drawCentredString(W/2, 28*mm, 'INTERNAL USE ONLY \u2014 NOT FOR DISTRIBUTION')
    canvas.setFont('Helvetica', 7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W/2, 16*mm, DATE)
    canvas.restoreState()


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0, 0, W, H, fill=1, stroke=0)
    import os
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), LOGO)
    if not os.path.exists(logo_path):
        logo_path = '/home/claude/vk2-work/VEKTOR-transparent-v3.png'
    from reportlab.lib.utils import ImageReader
    hy = H - MT2 + 14
    try:
        img = ImageReader(logo_path); iw, ih = img.getSize()
        lh = 22; lw = lh * iw / ih
        canvas.drawImage(logo_path, ML, hy, lw, lh, mask='auto', preserveAspectRatio=True)
    except: pass
    canvas.setFont('Helvetica', 7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawRightString(W - MR, H - MT2 + 18, f'{SUB}  \u00b7  {doc.page-1:02d}')
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.4)
    canvas.line(ML, H - MT2 + 8, W - MR, H - MT2 + 8)
    canvas.setLineWidth(0.3); canvas.line(ML, MB - 2, W - MR, MB - 2)
    ip_w=32*mm; ip_h=ip_w/IP_H_RATIO
    try:
        canvas.drawImage(IP_H,ML,1.0*mm,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawRightString(W-MR,1.0*mm+ip_h/2-2.5,f'investpuppy.com  \u00b7  {DATE}')
    canvas.restoreState()


def p(text, s, st='body'): return Paragraph(text, s[st])
def sp(n=8): return Spacer(1, n)
def hrm(): return HRule(COL_W, RULE_MAJ, 1.0, 3, 5)
def hrn(): return HRule(COL_W, RULE_MIN, 0.3, 3, 3)
def hrgold(): return HRule(COL_W, GOLD, 0.8, 4, 6)


def item_row(item_id, title, detail, trigger, docs, s, status='PLATFORM'):
    """Build a single recommendation item card."""
    if status == 'PLATFORM':
        status_style = s['status_p']
        row_bg = colors.HexColor('#120A0A')
        edge = RED_DIM
    elif status == 'DOCUMENT':
        status_style = s['status_a']
        row_bg = colors.HexColor('#100E08')
        edge = AMBER_DIM
    elif status == 'PRODUCT':
        status_style = s['status_b']
        row_bg = colors.HexColor('#08101A')
        edge = BLUE_DIM
    elif status == 'UK ENTRY':
        status_style = s['status_u']
        row_bg = colors.HexColor('#0E0814')
        edge = PURP_DIM
    else:
        status_style = s['status_g']
        row_bg = colors.HexColor('#080E0A')
        edge = GREEN_DIM

    inner_rows = [
        [Paragraph(item_id, s['item_id']),
         Paragraph(title, s['item_title']),
         Paragraph(status, status_style)],
        [Paragraph('', s['item_body']),
         Paragraph(detail, s['item_body']),
         Paragraph('', s['item_body'])],
    ]
    if trigger:
        inner_rows.append([
            Paragraph('', s['item_body']),
            Paragraph(f'<b>Trigger:</b> {trigger}', s['item_grey']),
            Paragraph('', s['item_body']),
        ])
    if docs:
        inner_rows.append([
            Paragraph('', s['item_body']),
            Paragraph(f'<b>Affected:</b> {docs}', s['item_grey']),
            Paragraph('', s['item_body']),
        ])

    cw = [16*mm, COL_W - 16*mm - 26*mm, 26*mm]
    t = Table(inner_rows, colWidths=cw, splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), row_bg),
        ('BOX', (0, 0), (-1, -1), 0.5, edge),
        ('LINEABOVE', (0, 1), (-1, 1), 0, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('SPAN', (0, 1), (0, -1)),
    ]))
    return t


def build():
    out = '/home/claude/investpuppy/vektor/output/pdf/vk5-outstanding-recommendations.pdf'
    s = S()
    f_cover = Frame(0, 0, W, H, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='cover')
    f_body = Frame(ML, MB, COL_W, H - MT2 - MB, id='body')
    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=ML, rightMargin=MR,
        topMargin=MT1, bottomMargin=MB,
        title='Vektor Outstanding Panel Recommendations Register',
        author='InvestPuppy')
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[f_cover], onPage=draw_cover),
        PageTemplate(id='Body', frames=[f_body], onPage=draw_page),
    ])

    story = []
    story.append(sp(1))
    story.append(NextPageTemplate('Body'))
    story.append(PageBreak())

    # ── PREAMBLE ──────────────────────────────────────────────────────────────
    story.append(p('PURPOSE OF THIS DOCUMENT', s, 'tag'))
    story.append(NoteBox(COL_W,
        'This register captures every panel recommendation from Stages 1\u20134 that was explicitly deferred '
        'rather than implemented. Items fall into two categories: those blocked by platform changes that must '
        'occur before any document work is possible, and minor document/suite polish items noted for the next '
        'update cycle. No item here reflects a gap in what has been distributed \u2014 all Tier 1 and Tier 2 '
        'items from Stage 4 have been implemented. This register is the complete audit trail of what remains.',
        s['body_grey']))
    story.append(sp(10))

    # Status legend
    legend_rows = [[
        Paragraph('\u25a0  PLATFORM', ParagraphStyle('lp', fontName='Helvetica-Bold',
            fontSize=7.5, textColor=RED_TXT, leading=11)),
        Paragraph('\u25a0  DOCUMENT', ParagraphStyle('la', fontName='Helvetica-Bold',
            fontSize=7.5, textColor=AMBER_TXT, leading=11)),
        Paragraph('\u25a0  STRATEGIC', ParagraphStyle('lg', fontName='Helvetica-Bold',
            fontSize=7.5, textColor=GREEN_TXT, leading=11)),
        Paragraph('\u25a0  PRODUCT', ParagraphStyle('lb', fontName='Helvetica-Bold',
            fontSize=7.5, textColor=BLUE_TXT, leading=11)),
        Paragraph('\u25a0  UK ENTRY', ParagraphStyle('lu', fontName='Helvetica-Bold',
            fontSize=7.5, textColor=PURP_TXT, leading=11)),
        Paragraph('Requires platform or app changes before document work', s['item_grey']),
        Paragraph('Document-only change, no platform dependency', s['item_grey']),
        Paragraph('Product / brand direction decision required', s['item_grey']),
        Paragraph('New capability or document needed; product development input', s['item_grey']),
        Paragraph('Required before UK market distribution', s['item_grey']),
    ]]
    leg_t = Table(legend_rows, colWidths=[22*mm, 22*mm, 22*mm, 20*mm, 20*mm,
                                          (COL_W-106*mm)/5, (COL_W-106*mm)/5,
                                          (COL_W-106*mm)/5, (COL_W-106*mm)/5,
                                          (COL_W-106*mm)/5])
    leg_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
        ('BOX', (0, 0), (-1, -1), 0.4, CARD_EDGE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEAFTER', (0, 0), (0, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (1, 0), (1, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (2, 0), (2, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (3, 0), (3, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (4, 0), (4, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (5, 0), (5, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (6, 0), (6, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (7, 0), (7, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (8, 0), (8, -1), 0.3, RULE_MIN),
    ]))
    story.append(leg_t)
    story.append(sp(14))

    # ── SECTION 1: PLATFORM CHANGES ───────────────────────────────────────────
    story.append(p('SECTION 1 \u2014 PLATFORM CHANGES REQUIRED', s, 'tag'))
    story.append(hrm())
    story.append(p('Items blocked by platform or application changes.', s, 'section_sub'))
    story.append(p(
        'The following four issues are visible in the platform UI screenshots embedded in the brochure. '
        'None can be resolved through document editing alone \u2014 the platform must be updated first, '
        'then all affected screenshots retaken, then the brochure rebuilt. All four can be addressed '
        'in a single screenshot retake session once the platform changes are made.',
        s, 'body_grey'))
    story.append(sp(8))

    items_platform = [
        ('P-01',
         'Admin portal still branded as \u201cInvestPuppy Admin Portal\u201d',
         'The admin portal header displays \u201cInvestPuppy Admin Portal\u201d across all authenticated screens. '
         'Every brochure screenshot showing the logged-in interface carries this label, creating a brand '
         'inconsistency between the document suite (which uses Vektor throughout) and the platform itself. '
         'All eight portal screenshots are affected.',
         'Platform UI rebrand: change portal header to \u201cVektor\u201d or \u201cVektor by InvestPuppy\u201d',
         'Brochure screenshots: sc04 through sc11 (8 of 11 screenshots)',
         'PLATFORM'),

        ('P-02',
         'Tan Chow Pin credentials visible in all logged-in screenshots',
         'The name \u201cTan Chow Pin\u201d appears in the top-right user profile area of all authenticated '
         'portal screenshots. This is a real or test-account name that should not appear in distributed '
         'materials. All screenshots showing the authenticated portal header are affected.',
         'Retake all portal screenshots under a neutral/anonymised test account '
         '(e.g. \u201cTest Account\u201d or a role-based label)',
         'All authenticated brochure screenshots: sc04 through sc11',
         'PLATFORM'),

        ('P-03',
         'NaN% displayed in strategy view screenshot',
         'Screenshot sc04_strategy.png (the SGP Equity Strategy admin view) shows one or more metric '
         'fields displaying \u201cNaN%\u201d \u2014 a rendering error where a percentage calculation '
         'produced a non-numeric result. This is visible in the distributed brochure and undermines '
         'confidence in the platform\u2019s calculation reliability at a critical first-impression moment.',
         'Investigate and fix the NaN% calculation bug in the strategy view; retake sc04',
         'vektor-brochure.pdf (Step 05, strategy admin screenshot)',
         'PLATFORM'),

        ('P-04',
         'KYC PENDING status shown alongside KYC ACTIVE in client management',
         'Screenshot sc05_clients.png (the customer management view) shows clients with both KYC ACTIVE '
         'and KYC PENDING status. While mixed status is operationally accurate for a test environment, '
         'the PENDING entries alongside ACTIVE entries in the same screenshot creates an inconsistent '
         'impression for a reader evaluating platform maturity. '
         'A clean screenshot showing only fully onboarded clients would be more appropriate for '
         'marketing materials.',
         'Retake sc05 showing a client list with consistent KYC ACTIVE status across all entries',
         'vektor-brochure.pdf (Step 06, customer management screenshot)',
         'PLATFORM'),
    ]

    for args in items_platform:
        story.append(item_row(*args[:5], s=s, status=args[5] if len(args)>5 else 'PLATFORM'))
        story.append(sp(6))

    story.append(sp(6))
    story.append(NoteBox(COL_W,
        '<b>Downstream work once P-01 through P-04 are resolved:</b> retake all 11 brochure screenshots '
        'in a single session, update the screenshots/ folder in INTERNAL \u2014 Do Not Distribute / BUILD-SCRIPTS, '
        'run build_brochure.py, and repackage the ZIP. The build script requires no changes \u2014 it reads from the '
        'screenshots/ folder by filename.',
        s['body_grey']))

    story.append(PageBreak())
    story.append(Spacer(1, 0))

    # ── SECTION 2: DOCUMENT SUITE ─────────────────────────────────────────────
    story.append(p('SECTION 2 \u2014 DOCUMENT SUITE', s, 'tag'))
    story.append(hrm())
    story.append(p('Minor document changes noted for the next update cycle.', s, 'section_sub'))
    story.append(sp(4))

    items_doc = [
        ('D-01',
         'Brand build specification: \u201c[NEW]\u201d label on FMP build step will become stale',
         'Section 07 of the Brand & Build Specification lists build_founding_mandate.py with a [NEW] '
         'annotation in the build order. This label was added to highlight the FMP as a new addition '
         'to the suite. As time passes the label becomes misleading \u2014 the FMP is no longer new.',
         'Next update cycle: remove the [NEW] annotation from step 6 in Section 07 build order',
         'vektor-brand-build-specification.pdf + .docx',
         'DOCUMENT'),

        ('D-02',
         'WP-03 PDF: three platform screenshots carry the P-01 through P-04 issues',
         'WP-03 (Capital Allocation Precision) embeds three screenshots from the allocation workflow: '
         'the full allocation breakdown, the portfolio positions view, and the order confirmation. '
         'All three will carry the \u201cInvestPuppy Admin Portal\u201d label and Tan Chow Pin credentials '
         'once P-01 and P-02 are fixed. WP-03 requires a screenshot retake and PDF rebuild concurrent '
         'with the brochure work.',
         'After platform changes (P-01, P-02): retake WP-03 screenshots and rebuild wp03-capital-allocation.pdf',
         'wp03-capital-allocation.pdf (pages 3\u20135)',
         'DOCUMENT'),

        ('D-03',
         'WP-07 technical architecture diagram: reflects dev environment, not production',
         'The architecture diagram in WP-07 accurately reflects the current AWS deployment but is '
         'explicitly a dev environment. Once the platform is promoted to production (a defined trigger '
         'in the risk roadmap), the diagram will need updating to reflect the production architecture, '
         'including any observability, RBAC, and monitoring components added at that stage.',
         'After production environment promotion: update architecture diagram and rebuild WP-07',
         'wp07-technical-architecture.pdf (Section 3 architecture diagram)',
         'DOCUMENT'),

        ('D-04',
         'Brand Story PDF \u2014 no build script, predates brand declaration, no footer mark',
         'The Brand Story document (vektor-brand-story.pdf) was built externally and has no Python '
         'build script in the suite. It is carried as a static file across vk2 and vk3 without updates. '
         'It predates the \u201cThe InvestPuppy Question\u201d brand declaration developed in vk3, '
         'does not carry the InvestPuppy footer mark, and may contain copy that is out of step with '
         'the brand position now established in Why Vektor. It is the only external commercial document '
         'without a build script and the only one without the vk3 footer standard.',
         'Create a build_brand_story.py script; align copy with the brand declaration; apply footer mark. '
         'Treat as vk4 first-pass item.',
         'vektor-brand-story.pdf (all pages)',
         'DOCUMENT'),
    ]

    for args in items_doc:
        story.append(item_row(*args[:5], s=s, status=args[5] if len(args)>5 else 'PLATFORM'))
        story.append(sp(6))

    story.append(sp(8))

    # ── SECTION 3: STRATEGIC ──────────────────────────────────────────────────
    story.append(p('SECTION 3 \u2014 STRATEGIC & PRODUCT', s, 'tag'))
    story.append(hrm())
    story.append(p(
        'Items that require a product or brand direction decision before any document work is appropriate.',
        s, 'section_sub'))
    story.append(sp(4))

    items_strategic = [
        ('S-01',
         'InvestPuppy website: replace mailto contact with a waitlist capture form',
         'The current InvestPuppy placeholder website uses a mailto: link as its primary CTA. Every '
         'document in the suite directs prospects to investpuppy.com. A prospect who follows that link '
         'and finds a mailto: CTA rather than a form loses context and creates friction at the critical '
         'conversion moment. Replacing the mailto: with a waitlist or enquiry form was flagged by all '
         'five experts as the highest-priority, lowest-effort improvement to the overall distribution '
         'infrastructure. It does not require any document changes \u2014 only a website update.',
         'Product decision: choose waitlist platform (e.g. Mailchimp, Typeform, custom); '
         'implement before any Founding Mandate outreach begins',
         'investpuppy.com (no document changes required)',
         'STRATEGIC'),

        ('S-02',
         'Brand identity tension: InvestPuppy name vs institutional positioning',
         'The panel identified a tension between the InvestPuppy brand name \u2014 which reads as '
         'approachable, consumer-facing fintech \u2014 and the institutional target audience of the '
         'Vektor product. The current positioning resolves this deliberately: InvestPuppy is the '
         'maker\u2019s mark, Vektor leads. The Brand Story\u2019s Founder\u2019s Note addresses the '
         'question directly. However, this is a strategic question that remains open \u2014 the panel '
         'noted it as an unresolved tension rather than a settled decision. No document changes are '
         'appropriate until a position is taken.',
         'Strategic decision: confirm or revise the InvestPuppy / Vektor brand hierarchy before '
         'any institutional distribution at scale',
         'Affects all documents at the brand level if the decision changes',
         'STRATEGIC'),
    ]

    for args in items_strategic:
        story.append(item_row(*args[:5], s=s, status=args[5] if len(args)>5 else 'STRATEGIC'))
        story.append(sp(6))

    story.append(PageBreak())
    story.append(Spacer(1, 0))

    # ── SECTION 4: PRODUCT & FEATURE SUGGESTIONS ──────────────────────────────
    story.append(p('SECTION 4 \u2014 PRODUCT & FEATURE SUGGESTIONS', s, 'tag'))
    story.append(hrm())
    story.append(p('Panel suggestions requiring new platform capabilities or new documents.', s, 'section_sub'))
    story.append(p(
        'These items were raised by the five-expert panel across Stages 1\u20134 as gaps in the '
        'platform\u2019s described capability. They are distinct from the document-level fixes above: '
        'each one requires either building a new platform capability or creating a new document to '
        'address a question the suite does not currently answer. They are captured here as product '
        'development inputs rather than document corrections.',
        s, 'body_grey'))
    story.append(sp(8))

    items_product = [
        ('PR-01',
         'Portfolio lifecycle and ongoing portfolio management \u2014 rebalancing, drift triggers, corporate actions',
         'The document suite describes portfolio construction in depth but is entirely silent on what '
         'happens after initial allocation. There is no description of drift monitoring, rebalancing '
         'triggers, threshold-based rebalancing, or corporate action handling. The Workflow Integration '
         'Guide has no row for \u201cMonitor and rebalance an existing portfolio.\u201d The impression '
         'created \u2014 whether accurate or not \u2014 is of a platform that builds a portfolio and '
         'then leaves the DPM to manage it manually thereafter. For a DPM evaluating a portfolio '
         'management platform, ongoing lifecycle management is as important as initial construction. '
         'A platform that addresses only construction is, in the panel\u2019s framing, a research '
         'tool rather than a DPM operating platform.',
         'Build rebalancing and drift monitoring capabilities; update Workflow Integration Guide '
         'and brochure to reflect the complete lifecycle. Alternatively, scope explicitly as a '
         'near-term roadmap item with a defined trigger condition.',
         'Platform Brochure, Workflow Integration Guide, WP-09 risk roadmap table',
         'PRODUCT'),

        ('PR-02',
         'Multi-mandate isolation \u2014 how client mandates are separated in multi-family and multi-client contexts',
         'The suite describes the three-role workflow for a single mandate in detail. It does not '
         'describe how multiple simultaneous client mandates are isolated from each other \u2014 how '
         'cross-contamination of data or strategy parameters is prevented, how conflicting client '
         'instructions are handled, or whether a PM can accidentally apply strategy A\u2019s parameters '
         'to client B\u2019s mandate. For a multi-family office managing twelve families, or a DPM '
         'running multiple client portfolios, this is a primary operational and compliance requirement. '
         'The panel noted it is completely absent from all commercial documents, the research series, '
         'and the workflow integration guide.',
         'Document the current multi-mandate isolation architecture explicitly. If physical separation '
         'does not yet exist, state the current logical isolation approach and the migration path.',
         'Platform Brochure, WP-06 (Audit & Compliance), WP-07 (Technical Architecture)',
         'PRODUCT'),

        ('PR-03',
         'No evidence layer \u2014 quantitative performance claims with no backtested or simulation evidence',
         'The suite makes specific quantitative claims \u2014 99.94% capital allocation efficiency, '
         'per-instrument Sharpe improvement over universal signals, efficient frontier optimisation '
         'selecting the max-Sharpe allocation. None of these claims are supported by backtested data, '
         'simulation outputs, or worked examples with actual numbers. The intellectual methodology '
         'is presented thoroughly. The empirical case is entirely absent. WP-10 teaches readers how '
         'to evaluate a systematic strategy\u2019s performance but provides no strategy performance '
         'data to evaluate. For an institutional investor making a Founding Mandate commitment, '
         'the absence of any performance evidence is a structural gap that the suite does not address.',
         'Add at minimum one worked backtest or simulation output with appropriate caveats to '
         'WP-01 or WP-10. Even a hypothetical example with fully disclosed assumptions gives a '
         'prospect something concrete to evaluate.',
         'WP-01 (Portfolio Construction), WP-10 (Evaluating Performance)',
         'PRODUCT'),

        ('PR-04',
         'Role permissions matrix \u2014 what each role can initiate, approve, and execute today',
         'The suite describes the three-role model (Stock Analyst, Portfolio Manager, Operations) '
         'at a structural level across multiple documents. It does not specify what each role can '
         'and cannot do in the current platform. What prevents a PM from approving their own '
         'strategy in the current implementation? Can the same individual hold two roles? What does '
         'the Analyst see that the PM does not? For any institutional client with compliance '
         'obligations, the operational implementation of the role model \u2014 not just its '
         'structural description \u2014 is due diligence material. The panel rated this as Critical '
         'in the WP-07 review and Important at the suite level.',
         'Document the current permissions in a role matrix table. Acknowledge the maker/checker '
         'limitation (PM can currently assign directly) explicitly in WP-06 and the brochure, '
         'not only in WP-07.',
         'WP-06 (Audit & Compliance), WP-07 (Technical Architecture), Platform Brochure',
         'PRODUCT'),

        ('PR-05',
         'Competitive positioning \u2014 suite positions against Bloomberg PORT, not against Excel',
         'The Why Vektor document identifies three inadequate alternatives: Excel-based allocation, '
         'institutional quant platforms (Bloomberg PORT, FactSet), and retail robo-tools. The '
         'institutional platforms are named as the comparison point for price and complexity. '
         'But Bloomberg PORT and FactSet are not the actual competitive consideration for most of '
         'the target audience \u2014 boutique DPMs and family offices cannot afford them and are '
         'not evaluating them. The actual alternative most prospects are weighing is Excel, a '
         'customised in-house model, or no systematic tool at all. Positioning against an '
         'out-of-reach platform makes the comparison feel aspirational rather than practical. '
         'Positioning against Excel \u2014 the real status quo \u2014 is more commercially resonant '
         'and easier to win.',
         'Rewrite the competitive section of Why Vektor to make Excel the primary comparison '
         'point. Keep Bloomberg PORT as a reference for price benchmarking only.',
         'Why Vektor (commercial), Deck 1 (60-Minute Meeting)',
         'PRODUCT'),

        ('PR-06',
         'Implementation and onboarding process \u2014 the \u201cwe\u2019ve been burned before\u201d objection is unaddressed',
         'Every sophisticated family office and DPM principal has a story about a vendor that '
         'over-promised and under-delivered on implementation. The document suite builds '
         'intellectual confidence thoroughly but does not address operational confidence: what '
         'does onboarding look like, what is the implementation timeline, what support is '
         'available during setup, and what happens if something goes wrong post-launch? '
         'The Founding Mandate programme is presumably the answer to this \u2014 early partners '
         'get direct founding-team access and a more hands-on onboarding. But since the '
         'Founding Mandate programme has not been fully defined in any document, this '
         'reassurance is not currently available to a prospect reading the suite.',
         'Define the onboarding and implementation process as part of the Founding Mandate '
         'Programme document. At minimum add an FAQ answer: Q13. What does implementation '
         'look like and what support is available?',
         'Founding Mandate Programme (IP-FMP-260501-1.0), FAQ',
         'PRODUCT'),

        ('PR-07',
         'Day-in-the-life operational narrative \u2014 what Monday morning looks like on a Vektor desk',
         'The suite excels at describing what Vektor is and how it works architecturally. It does '
         'not describe what it is like to operate Vektor as a daily working tool. No document '
         'answers the question a DPM will ask in their head throughout the reading process: '
         '\u201cWhat does my day actually change?\u201d The Workflow Integration Guide comes closest '
         'with its Replaces/Augments/Unchanged table but stops at the task level. A short '
         'narrative \u2014 one or two pages \u2014 describing a typical strategy build cycle from '
         'the PM\u2019s perspective, and the ongoing weekly rhythm of monitoring and review, '
         'would translate the architecture into operational reality more effectively than any '
         'technical document currently in the suite.',
         'Add a \u201cA Day on a Vektor Desk\u201d section to the Workflow Integration Guide, '
         'or as a standalone one-pager for use at Stage 3 of the sales journey.',
         'Workflow Integration Guide, or new standalone document',
         'PRODUCT'),

        ('PR-08',
         'Founder biography and voice absent from all commercial documents',
         'No founder biography, founder note, or personal voice appears anywhere across the '
         'commercial or research documents. Both the original Singapore panel and the UK panel '
         'flagged this explicitly: at pre-revenue stage, founder credibility is a primary trust '
         'signal. The intellectual rigour of the suite builds confidence in the methodology '
         'but provides no signal about the people behind it. The Founding Mandate Programme '
         'and Why Vektor are the natural homes \u2014 not a full biography, but a paragraph of '
         'personal voice that makes the founder visible and gives a prospect someone to trust '
         'before they have met anyone from the team.',
         'Add a brief founder note (4\u20136 sentences, first person) to Why Vektor and the '
         'Founding Mandate Programme. Not a CV \u2014 a voice.',
         'Why Vektor (page 2), Founding Mandate Programme (introduction)',
         'PRODUCT'),
    ]

    for args in items_product:
        story.append(item_row(*args[:5], s=s, status=args[5] if len(args)>5 else 'PRODUCT'))
        story.append(sp(6))

    story.append(sp(8))

    # ── SECTION 5: UK MARKET ENTRY ────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Spacer(1, 0))
    story.append(p('SECTION 5 \u2014 UK MARKET ENTRY', s, 'tag'))
    story.append(hrm())
    story.append(p('Items required before distribution to UK prospects or FCA-regulated firms.', s, 'section_sub'))
    story.append(p(
        'The UK panel convened for the vk3 review identified a specific set of items that must be '
        'addressed before the document suite is distributed to any UK-based prospect or FCA-regulated '
        'firm. These items do not affect Singapore distribution and are not defects in the existing '
        'suite \u2014 they are jurisdiction-specific additions required for the UK market context. '
        'UK-01 is a distribution blocker. UK-02 through UK-04 are significant but not immediate blockers.',
        s, 'body_grey'))
    story.append(sp(8))

    items_uk = [
        ('UK-01',
         'FCA regulatory context entirely absent from commercial documents \u2014 UK distribution blocker',
         'The complete commercial document suite \u2014 brochure, FAQ, Why Vektor, Founding Mandate, '
         'Workflow Integration Guide \u2014 contains no reference to the FCA, Consumer Duty, or any '
         'UK regulatory framework. UK wealth managers and DPMs operate under FCA obligations and will '
         'immediately notice the omission. The panel rated this as a unanimous blocker: no UK prospect '
         'distribution should occur until at minimum a FAQ question on UK regulatory considerations '
         'is added. A short UK regulatory annex to the Workflow Integration Guide is the fuller solution.',
         'IMMEDIATE: Add FAQ Q14 addressing UK regulatory context (FCA standing, Consumer Duty, '
         'applicable permissions). Consider a short UK regulatory annex to Workflow Integration Guide.',
         'FAQ (new Q14), Workflow Integration Guide (new UK annex)',
         'UK ENTRY'),

        ('UK-02',
         'Yahoo Finance as default data source creates FCA compliance friction',
         'Yahoo Finance is the default data source stated in the commercial documents and FAQ. '
         'For FCA-regulated UK firms, Yahoo Finance as an institutional data source will generate '
         'immediate compliance questions \u2014 data quality obligations, audit trail requirements, '
         'and vendor risk assessments all apply. The suite notes that institutional feeds are '
         'configurable but this appears only in the technical white papers at low prominence. '
         'A clear, commercially-facing statement of the institutional data feed pathway '
         '(Bloomberg, Refinitiv, ICE) with an onboarding route needs to appear in the brochure '
         'and FAQ before UK DPMs review these materials.',
         'Add explicit institutional data feed pathway to Platform Brochure (data section) and '
         'FAQ Q6. Reframe Yahoo Finance as the development/demonstration default, not the '
         'production default for regulated clients.',
         'Platform Brochure (data source section), FAQ Q6 (What data does Vektor use?)',
         'UK ENTRY'),

        ('UK-03',
         'UK competitive landscape absent \u2014 Bipsync, Objectway, Iress, Figaro by Dorsum unmentioned',
         'The competitive landscape in Why Vektor names Bloomberg PORT and FactSet as the institutional '
         'alternatives. A UK prospect \u2014 particularly one in the DPM or wealth management space '
         '\u2014 will be aware of UK-specific competitors that are entirely absent from the document: '
         'Bipsync (portfolio management and research), Objectway (wealth management platform), '
         'Iress (widely used across UK wealth and DPM), and Figaro by Dorsum (systematic portfolio '
         'construction). The absence signals either unfamiliarity with the UK market or a competitive '
         'landscape written for a different geography. A targeted UK competitive section addressing '
         'these vendors is required for credible UK positioning.',
         'Add a UK-specific competitive landscape paragraph to Why Vektor addressing Bipsync, '
         'Objectway, Iress, and Figaro. Position Vektor\u2019s differentiation in each case.',
         'Why Vektor (competitive landscape section, page 3)',
         'UK ENTRY'),

        ('UK-04',
         'No UK data residency or deployment pathway documented',
         'The suite describes AWS ap-southeast-1 (Singapore) as the current deployment region '
         'and notes the architecture is region-agnostic. FAQ Q8 addresses Singapore data residency. '
         'No equivalent statement exists for UK data residency requirements. UK firms with FCA '
         'obligations around data location, GDPR/UK GDPR compliance, and cloud vendor risk will '
         'require a clear statement of the UK deployment pathway \u2014 specifically AWS eu-west-2 '
         '(London) deployment, UK GDPR applicability, and the migration process from the current '
         'Singapore instance. Without this, a UK firm\u2019s compliance team will block evaluation '
         'before it reaches the investment or operations team.',
         'Add FAQ Q addressing UK data residency and deployment. Update WP-07 architecture '
         'section with a note on UK/EU regional deployment pathway.',
         'FAQ (new question on UK data residency), WP-07 Technical Architecture',
         'UK ENTRY'),
    ]

    for args in items_uk:
        story.append(item_row(*args[:5], s=s, status=args[5] if len(args)>5 else 'UK ENTRY'))
        story.append(sp(6))

    story.append(sp(8))

    # ── SUMMARY TABLE ─────────────────────────────────────────────────────────
    story.append(p('REGISTER SUMMARY', s, 'tag'))
    story.append(hrm())
    story.append(sp(4))

    all_items = [
        ('P-01', 'Admin portal branded as \u201cInvestPuppy Admin Portal\u201d',
         'Platform rebrand', 'PLATFORM', 'Before any further screenshot distribution'),
        ('P-02', 'Tan Chow Pin credentials in all portal screenshots',
         'Anonymise test account', 'PLATFORM', 'Before any further screenshot distribution'),
        ('P-03', 'NaN% in strategy view screenshot',
         'Fix calculation bug + retake', 'PLATFORM', 'Before Founding Mandate partner distribution'),
        ('P-04', 'KYC PENDING/ACTIVE inconsistency in client screenshots',
         'Retake with clean data', 'PLATFORM', 'Before Founding Mandate partner distribution'),
        ('D-01', 'Brand spec [NEW] label on FMP build step',
         'Remove annotation', 'DOCUMENT', 'Next update cycle (low urgency)'),
        ('D-02', 'WP-03 screenshots carry P-01/P-02 issues',
         'Retake + rebuild', 'DOCUMENT', 'Concurrent with brochure screenshot retake'),
        ('D-03', 'WP-07 architecture diagram: dev environment, not production',
         'Update at production promotion', 'DOCUMENT', 'After production environment promotion'),
        ('D-04', 'Brand Story PDF \u2014 no build script, no footer mark, predates brand declaration',
         'Create build script; align copy; apply footer', 'DOCUMENT', 'vk4 first-pass item'),
        ('S-01', 'investpuppy.com: mailto vs waitlist form',
         'Implement form capture', 'STRATEGIC', 'Before Founding Mandate outreach begins'),
        ('S-02', 'InvestPuppy / Vektor brand hierarchy tension',
         'Strategic decision required', 'STRATEGIC', 'Before institutional distribution at scale'),
        ('PR-01', 'Portfolio lifecycle: rebalancing, drift triggers, corporate actions absent',
         'Build capability or scope roadmap', 'PRODUCT', 'Before DPM desk distribution'),
        ('PR-02', 'Multi-mandate isolation not documented',
         'Document architecture + isolation approach', 'PRODUCT', 'Before MFO / multi-client distribution'),
        ('PR-03', 'No evidence layer \u2014 zero backtested or simulation data',
         'Add worked backtest with caveats', 'PRODUCT', 'Before institutional DD distribution'),
        ('PR-04', 'Role permissions matrix missing',
         'Document what each role can do today', 'PRODUCT', 'Before any compliance review'),
        ('PR-05', 'Competitive positioning targets Bloomberg PORT, not Excel',
         'Rewrite Why Vektor comp section', 'PRODUCT', 'Before next commercial document update'),
        ('PR-06', 'Onboarding process and implementation risk unaddressed',
         'Define in FMP doc + FAQ Q13', 'PRODUCT', 'Before Founding Mandate partner outreach'),
        ('PR-07', 'No day-in-the-life operational narrative',
         'Add to Workflow Integration Guide', 'PRODUCT', 'Before Stage 3 sales meetings'),
        ('PR-08', 'Founder biography and voice absent from all commercial documents',
         'Add founder note to Why Vektor + FMP', 'PRODUCT', 'Before Founding Mandate outreach'),
        ('UK-01', 'FCA regulatory context absent \u2014 UK distribution blocker',
         'Add FAQ Q14 + UK regulatory annex', 'UK ENTRY', 'BEFORE any UK distribution'),
        ('UK-02', 'Yahoo Finance creates FCA compliance friction for UK firms',
         'Add institutional feed pathway to Brochure + FAQ', 'UK ENTRY', 'Before UK DPM distribution'),
        ('UK-03', 'UK competitive landscape absent \u2014 Bipsync, Objectway, Iress, Figaro',
         'Add UK competitive paragraph to Why Vektor', 'UK ENTRY', 'Before UK distribution of Why Vektor'),
        ('UK-04', 'No UK data residency or deployment pathway documented',
         'Add FAQ question + WP-07 note', 'UK ENTRY', 'Before UK firm compliance review'),
    ]

    status_styles = {
        'PLATFORM': s['status_p'], 'DOCUMENT': s['status_a'],
        'STRATEGIC': s['status_g'], 'PRODUCT': s['status_b'],
        'UK ENTRY': s['status_u'],
    }

    hrow = [Paragraph(h, s['tbl_hdr']) for h in ['ID', 'ITEM', 'ACTION', 'STATUS', 'WHEN']]
    rows = [hrow]
    for item_id, item, action, status, when in all_items:
        rows.append([
            Paragraph(item_id, s['tbl_id']),
            Paragraph(item, s['tbl_body']),
            Paragraph(action, s['tbl_body']),
            Paragraph(status, status_styles[status]),
            Paragraph(when, s['tbl_grey']),
        ])

    cw = [12*mm, 56*mm, 34*mm, 22*mm, COL_W - 124*mm]
    t = Table(rows, colWidths=cw, repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [CARD_BG, colors.HexColor('#0F0F14')]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, RULE_MIN),
        ('BOX', (0, 0), (-1, -1), 0.4, CARD_EDGE),
        ('LINEAFTER', (0, 0), (0, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (1, 0), (1, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (2, 0), (2, -1), 0.3, RULE_MIN),
        ('LINEAFTER', (3, 0), (3, -1), 0.3, RULE_MIN),
        # Row tints by category
        ('BACKGROUND', (0, 1),  (-1, 4),  colors.HexColor('#120A0A')),  # P-01 to P-04
        ('BACKGROUND', (0, 5),  (-1, 8),  colors.HexColor('#100E08')),  # D-01 to D-04
        ('BACKGROUND', (0, 9),  (-1, 10), colors.HexColor('#080E0A')),  # S-01 to S-02
        ('BACKGROUND', (0, 11), (-1, 18), colors.HexColor('#08101A')),  # PR-01 to PR-08
        ('BACKGROUND', (0, 19), (-1, 22), colors.HexColor('#0E0814')),  # UK-01 to UK-04
    ]))
    story.append(t)
    story.append(sp(12))
    story.append(hrgold())
    story.append(sp(6))
    story.append(p(
        '22 open items: 4 PLATFORM (blocked by app changes), 4 DOCUMENT (next cycle), '
        '2 STRATEGIC (awaiting direction), 8 PRODUCT (new capabilities or documents required), '
        '4 UK ENTRY (required before UK market distribution \u2014 UK-01 is a distribution blocker). '
        'All vk3 Tier 1 and Tier 2 items have been implemented. '
        'This register is the complete outstanding work log.',
        s, 'body_grey'))
    story.append(sp(8))
    story.append(p(
        f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  Internal use only  \u00b7  {DATE}',
        s, 'wp_ref'))

    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    r = subprocess.run(['pdfinfo', out], capture_output=True, text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l or 'File' in l:
            print(l)


if __name__ == '__main__':
    build()
