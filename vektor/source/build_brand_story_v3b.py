"""
Vektor Brand Story — vk3b rebuild. Restructured on panel recommendation:
  - New Section 01: The Two Marks — confident dual-identity opening (Expert G draft)
  - Section 02: Why Vektor (was 01)
  - Section 03: The InvestPuppy Mark — The maker's brand (was 06, now early, no apology)
  - Section 04: The Vektor Mark — The logo that is a mathematical statement (was 02)
  - Section 05: The Colour System (was 03)
  - Section 06: The Brand in Practice — covers both marks (was 05)
  - "The Parent Brand / tension" section retired entirely
  - Cover subtitle updated to reference both marks
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
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
    PageBreak, NextPageTemplate, Image as RLImage,
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
DARK_WARM = colors.HexColor('#0D0C0A')
IP_GREEN  = colors.HexColor('#5DBE4A')

W, H = A4
ML = MR = 22*mm
MT1 = 16*mm; MT2 = 46*mm; MB = 20*mm
COL_W = W - ML - MR

LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png')
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')
IP_V         = '/home/claude/vk2-work/IPVerticalClear.png'
IP_H_INV     = '/home/claude/vk2-work/IPHorizontalInvClear.png'
IP_V_INV     = '/home/claude/vk2-work/IPVerticalInvClear.png'
IP_H_RATIO   = 2.337
IP_V_RATIO   = 1.427
DATE         = 'May 2026'
SUB          = 'Brand Story'
DOC_AUDIENCE = 'Brand and naming documentation \u2014 internal and partner use'


def mk(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9.5, textColor=OFF_WHITE,
             leading=17, spaceAfter=8)
    d.update(kw)
    return ParagraphStyle(name, **d)

S_tag   = mk('tag',  fontSize=7, textColor=WARM_GREY, leading=11, letterSpacing=4, spaceAfter=4)
S_sec   = mk('sec',  fontName='Helvetica-Bold', fontSize=16, textColor=PLATINUM, leading=22, spaceAfter=5)
S_sub   = mk('sub',  fontName='Helvetica-Oblique', fontSize=11, textColor=WARM_GREY, leading=17, spaceAfter=10)
S_body  = mk('body', alignment=TA_JUSTIFY)
S_grey  = mk('grey', textColor=WARM_GREY, alignment=TA_JUSTIFY)
S_note  = mk('note', fontName='Helvetica-Oblique', textColor=WARM_GREY, alignment=TA_JUSTIFY)
S_subh  = mk('subh', fontName='Helvetica-Bold', fontSize=8, textColor=WARM_GREY,
              leading=12, letterSpacing=3, spaceAfter=5, spaceBefore=12)
S_pull  = mk('pull', fontName='Helvetica-Oblique', fontSize=11, textColor=PLATINUM,
              leading=18, alignment=TA_CENTER)
S_close = mk('close', fontName='Helvetica-Bold', fontSize=11, textColor=PLATINUM,
              leading=17, alignment=TA_CENTER, spaceAfter=0)
S_th    = mk('th', fontName='Helvetica-Bold', fontSize=7.5, textColor=PLATINUM, leading=11)
S_tb    = mk('tb', fontSize=8.5, textColor=OFF_WHITE, leading=13, alignment=TA_JUSTIFY)
S_tg    = mk('tg', fontSize=8.5, textColor=WARM_GREY, leading=13, alignment=TA_JUSTIFY)
S_tgold = mk('tgold', fontSize=8.5, textColor=GOLD, leading=13)
S_num   = mk('num', fontName='Helvetica-Bold', fontSize=28, textColor=GOLD,
              leading=32, alignment=TA_CENTER)
S_decl  = mk('decl', fontSize=9.5, textColor=OFF_WHITE, leading=17, spaceAfter=10,
              alignment=TA_JUSTIFY)
S_swim = mk('swim', fontName='Helvetica-Oblique', fontSize=10, textColor=colors.HexColor('#9A9086'), leading=16, alignment=TA_CENTER, spaceBefore=8, spaceAfter=0)
S_decl_swim = mk('dswim', fontName='Helvetica-BoldOblique', fontSize=13, textColor=OFF_WHITE, leading=18, alignment=TA_CENTER, spaceBefore=0, spaceAfter=0)
S_decl_close = mk('declc', fontName='Helvetica-BoldOblique', fontSize=10,
                   textColor=PLATINUM, leading=16, alignment=TA_JUSTIFY)
S_ref   = mk('ref', fontSize=7.5, textColor=colors.HexColor('#555550'),
              leading=11, alignment=TA_CENTER)
S_asset_label = mk('albl', fontName='Helvetica-Bold', fontSize=8, textColor=GOLD,
                    leading=12, spaceAfter=2)
S_asset_desc  = mk('adsc', fontSize=8, textColor=WARM_GREY, leading=12, spaceAfter=6)
S_deploy_hdr  = mk('dhdr', fontName='Helvetica-Bold', fontSize=8, textColor=PLATINUM,
                    leading=12, spaceAfter=2)
S_deploy_body = mk('dbod', fontSize=8, textColor=OFF_WHITE, leading=13, spaceAfter=4)
S_contents_n  = mk('cn', fontName='Helvetica-Bold', fontSize=9, textColor=GOLD, leading=14)
S_contents_t  = mk('ct', fontSize=9, textColor=OFF_WHITE, leading=14)
S_contents_p  = mk('cp', fontSize=9, textColor=WARM_GREY, leading=14, alignment=TA_RIGHT)


class HRule(Flowable):
    def __init__(self, w, c=RULE_MIN, t=0.5, sa=4, sb=4):
        Flowable.__init__(self)
        self.rw=w; self.c=c; self.t=t; self._sa=sa; self._sb=sb
        self.height = sa + t + sb
    def wrap(self, aw, ah): return self.rw, self.height
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        self.canv.line(0, self._sb+self.t/2, self.rw, self._sb+self.t/2)


class NoteBox(Flowable):
    def __init__(self, w, text, style, bg=NOTE_BG, bar=RULE_MAJ, ph=15, pv=13, bw=4):
        Flowable.__init__(self)
        self._w=w; self.bg=bg; self.bar=bar; self.ph=ph; self.pv=pv; self.bw=bw
        self._p=Paragraph(text, style); self._iw=w-bw-ph*2
    def wrap(self, aw, ah):
        _, h = self._p.wrap(self._iw, ah)
        self.height = h + self.pv*2; return self._w, self.height
    def draw(self):
        c = self.canv; c.saveState()
        c.setFillColor(self.bg); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0, 0, self._w, self.height, 3, fill=1, stroke=1)
        c.setFillColor(self.bar); c.roundRect(0, 0, self.bw, self.height, 2, fill=1, stroke=0)
        self._p.wrap(self._iw, self.height); self._p.drawOn(c, self.bw+self.ph, self.pv)
        c.restoreState()


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0, 0, W, H, fill=1, stroke=0)
    from reportlab.lib.utils import ImageReader
    # Vektor logo — large, centred
    try:
        img = ImageReader(LOGO); iw, ih = img.getSize()
        lw = min(W*0.62, 320); lh = lw*ih/iw
        lx = (W-lw)/2; ly = H*0.55
        canvas.drawImage(LOGO, lx, ly-lh, lw, lh, mask='auto', preserveAspectRatio=True)
        ry = ly - lh - 10
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8)
        canvas.line(ML, ry, W-MR, ry)
        canvas.setFont('Helvetica-Bold', 7); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2, ry-14, 'THE BRAND STORY')
        canvas.setFont('Helvetica-Bold', 22); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2, ry-42, 'Two Marks. One Purpose.')
        canvas.setFont('Helvetica-Oblique', 10); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2, ry-66,
            'The visual identities of Vektor and InvestPuppy \u2014 every element documented.')
        canvas.drawCentredString(W/2, ry-82,
            'Nothing is decorative.')
    except Exception as e: print(e)
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4)
    canvas.line(ML, 36*mm, W-MR, 36*mm)
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(WARM_GREY)
    canvas.drawCentredString(W/2, 28*mm, DOC_AUDIENCE)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W/2, 16*mm, DATE)
    # IP mark — cover standard 38mm bottom-left
    try:
        ip_w = 38*mm; ip_h = ip_w / IP_H_RATIO
        canvas.drawImage(IP_H, ML, 9*mm, ip_w, ip_h, mask='auto', preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.restoreState()


def _hdr(canvas, doc):
    from reportlab.lib.utils import ImageReader
    hy = H - MT2 + 14
    try:
        img = ImageReader(LOGO); iw, ih = img.getSize()
        lh = 22; lw = lh*iw/ih
        canvas.drawImage(LOGO, ML, hy, lw, lh, mask='auto', preserveAspectRatio=True)
    except: pass
    canvas.setFont('Helvetica', 7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawRightString(W-MR, H-MT2+18, f'{SUB}  \u00b7  {doc.page-1:02d}')
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.4)
    canvas.line(ML, H-MT2+8, W-MR, H-MT2+8)


def _ftr(canvas):
    from reportlab.lib.utils import ImageReader
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.3)
    canvas.line(ML, MB-2, W-MR, MB-2)
    ip_w = 32*mm; ip_h = ip_w / IP_H_RATIO
    try:
        canvas.drawImage(IP_H, ML, 1.0*mm, ip_w, ip_h, mask='auto', preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.setFont('Helvetica', 6.5); canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawRightString(W-MR, 1.0*mm + ip_h/2 - 2.5, f'investpuppy.com  \u00b7  {DATE}')


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


def p(text, style): return Paragraph(text, style)
def sp(n=8): return Spacer(1, n)
def hrm(): return HRule(COL_W, RULE_MAJ, 1.0, 3, 6)
def hrn(): return HRule(COL_W, RULE_MIN, 0.3, 3, 3)
def hrgold(): return HRule(COL_W, GOLD, 0.8, 4, 6)


def section_opener(number, title, subtitle, story):
    story.append(p(number, S_num))
    story.append(sp(4))
    story.append(p(title, S_sec))
    story.append(hrm())
    story.append(p(subtitle, S_sub))


def build():
    out = '/home/claude/investpuppy/vektor/output/pdf/vk5-brand-story.pdf'
    f_cov = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0, id='cover')
    f_fst = Frame(ML, MB, COL_W, H-MT1-MB, id='first')
    f_lat = Frame(ML, MB, COL_W, H-MT2-MB, id='later')
    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=ML, rightMargin=MR,
        topMargin=MT1, bottomMargin=MB,
        title='Vektor Brand Story', author='InvestPuppy')
    doc.addPageTemplates([
        PageTemplate(id='Cover',  frames=[f_cov], onPage=draw_cover),
        PageTemplate(id='First',  frames=[f_fst], onPage=draw_first),
        PageTemplate(id='Later',  frames=[f_lat], onPage=draw_later),
    ])

    story = []
    story.append(sp(1))
    story.append(NextPageTemplate('First'))
    story.append(PageBreak())

    # ── CONTENTS ─────────────────────────────────────────────────────────────
    story.append(p('CONTENTS', S_tag))
    story.append(hrm())
    story.append(sp(4))
    contents = [
        ('01', 'The Two Marks',        'One company, two identities, one purpose',          '2'),
        ('02', 'Why Vektor',           'A word that earns its place',                       '3'),
        ('03', 'The InvestPuppy Mark', 'The maker\u2019s brand',                            '4'),
        ('04', 'The Vektor Mark',      'A logo that is a mathematical statement',           '6'),
        ('05', 'The Colour System',    'Three colours, each earning its place',             '7'),
        ('06', 'The Brand in Practice','What both marks do in a room',                      '8'),
    ]
    for num, title, sub, pg in contents:
        row = [p(num, S_contents_n), p(f'{title} \u2014 {sub}', S_contents_t),
               p(pg, S_contents_p)]
        t = Table([row], colWidths=[10*mm, COL_W-22*mm, 12*mm])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('LINEBELOW', (0,0), (-1,-1), 0.3, RULE_MIN),
        ]))
        story.append(t)

    story.append(NextPageTemplate('Later'))
    story.append(PageBreak())
    story.append(sp(0))

    # ── SECTION 01: THE TWO MARKS ─────────────────────────────────────────────
    section_opener('01', 'The Two Marks', 'One company, two identities, one purpose.', story)

    # Origin narrative — new opening before the declaration
    story.append(p(
        'This did not start with a brand strategy. It started with a conviction.',
        S_sub))
    story.append(sp(8))
    for origin_para in [
        'The people who built Vektor spent decades inside the system they are now trying to improve. '
        'Decades of working with tools that were either too expensive, too generic, or too opaque for the '
        'mandates they were managing. Decades of watching institutional-grade capability remain '
        'inaccessible to independent teams who needed it most.',
        'The frustration was not theoretical. It was professional. And eventually it became a question '
        'that would not go away: there must be a better way. Not a better version of what existed. '
        'A genuinely different approach \u2014 one built by practitioners for practitioners, '
        'without the cost, the complexity, or the credibility performance that had made '
        'the existing tools what they were.',
        'Vektor is that approach. InvestPuppy is the company that decided to build it. '
        'The two marks are not a brand architecture exercise. They are the honest representation '
        'of what this actually is: a serious platform, built by people who are not serious about '
        'sounding like everyone else.',
    ]:
        story.append(p(origin_para, S_body))
        story.append(sp(4))
    story.append(sp(8))

    # Expert G's opening declaration
    story.append(HRule(COL_W, RULE_MAJ, 1.0, 2, 6))
    story.append(p(
        'Vektor by InvestPuppy. Two names. Two marks. One purpose.', S_pull))
    story.append(HRule(COL_W, RULE_MAJ, 1.0, 6, 10))

    story.append(p(
        'Vektor is the platform: systematic, precise, built from the mathematics of magnitude '
        'and direction. InvestPuppy is the company: confident, irreverent, more interested in '
        'the quality of its work than the hyperbole of its messaging.', S_body))
    story.append(p(
        'Neither mark explains the other. Each is complete on its own terms. Together they '
        'make a statement about the kind of firm this is: serious about portfolios, not serious '
        'about itself. Every element of both marks was chosen with the same precision as the '
        'platform they represent. Nothing is decorative.', S_body))
    story.append(sp(6))

    # Side by side mark descriptions
    two_marks = [[
        p('VEKTOR', S_th),
        p('INVESTPUPPY', S_th),
    ],[
        p('The product. Systematic portfolio management platform for listed equities.',
          S_tb),
        p('The company. The people who built it and the conviction they built it with.',
          S_tb),
    ],[
        p('Geometric wordmark. Custom asymmetric V. Gold arrowhead. Termina Bold. '
          'Dark ground. Institutional register.', S_tg),
        p('Illustrated mark. Dog outline. Stock chart arrow. Split wordmark: '
          'Invest in platinum, Puppy in green. Approachable register.', S_tg),
    ],[
        p('Leads every commercial document and platform interface.', S_tb),
        p('Appears as the maker\u2019s attribution on all Vektor materials.', S_tb),
    ]]
    tm = Table(two_marks, colWidths=[COL_W/2, COL_W/2])
    tm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD_BG, colors.HexColor('#0F0F14')]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('LINEAFTER', (0,0), (0,-1), 0.3, RULE_MIN),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, RULE_MIN),
        ('BOX', (0,0), (-1,-1), 0.4, CARD_EDGE),
    ]))
    story.append(tm)
    story.append(sp(10))
    story.append(p(
        'The brand architecture is strict: Vektor leads every application. InvestPuppy appears '
        'beneath it as a maker\u2019s mark \u2014 authoritative, declarative, contextualising '
        'without competing. BY INVESTPUPPY at one-quarter the cap height of VEKTOR is not a '
        'sub-brand treatment. It is a stamp.', S_body))

    story.append(sp(12))
    story.append(HRule(COL_W,RULE_MAJ,0.5,4,4))
    story.append(sp(8))
    story.append(p('Serious when it matters.', S_decl_swim))
    story.append(sp(12))
    story.append(PageBreak()); story.append(sp(0))

    # ── SECTION 02: WHY VEKTOR ───────────────────────────────────────────────
    section_opener('02', 'Why Vektor', 'A word that earns its place.', story)
    story.append(p(
        'The name was not chosen for memorability alone \u2014 though it achieves that. '
        'It was chosen because it encodes the platform\u2019s core proposition in a single word.',
        S_body))

    story.append(p('THE MATHEMATICAL ORIGIN', S_subh))
    story.append(p(
        'In mathematics, a vector is a quantity defined by two inseparable properties: '
        'magnitude and direction. It is not enough to know how much force is applied \u2014 '
        'you must know where it is going. A vector without direction is just a number. A vector '
        'without magnitude is just a guess. Together, they define a precise, actionable quantity. '
        'A well-constructed portfolio strategy requires exactly the same two things: capital '
        'weight and signal direction. Vektor encodes both into its name.', S_body))

    story.append(p('THE DELIBERATE SPELLING', S_subh))
    story.append(p(
        'We chose Vektor with a K, not Vector with a C. This is not affectation \u2014 it is a '
        'considered brand decision with three specific consequences: distinctiveness in a crowded '
        'fintech namespace, trademark clearance from the many Vector-named entities already '
        'registered globally, and a signal \u2014 subtle but present \u2014 that this product was '
        'built with precision and intention rather than assembled from defaults. The K is a small '
        'difference that carries a clear message: we do not do things the default way.', S_body))

    story.append(p('THE NAMING SHORTLIST', S_subh))
    naming = [
        ('WealthAdvisor',
         'Generic to the point of invisibility. Describes a human role, not a technology '
         'platform. Almost certainly trademarked multiple times over.'),
        ('InvestLens\u202f/\u202fInvestScope',
         'Both carry the InvestPuppy prefix, partially defeating brand separation. Both imply '
         'observation rather than action \u2014 neither implies the decisiveness that systematic '
         'execution requires.'),
        ('Axiom',
         'Strong mathematical authority, but already present in financial services in multiple '
         'contexts. The rigour is right; the availability is not.'),
        ('Lattice',
         'Intellectually precise but collision risk with an established HR SaaS platform of the '
         'same name made it problematic in enterprise sales contexts.'),
        ('Arc\u202f/\u202fVantage\u202f/\u202fFoundry',
         'Each has merit but none encode both magnitude and direction simultaneously the way '
         'Vektor does. Arc is too common. Vantage implies perspective without action. '
         'Foundry implies creation but not direction.'),
    ]
    hrow = [p('Name', S_th), p('Why set aside', S_th)]
    rows = [hrow] + [[p(n, S_tgold), p(r, S_tg)] for n, r in naming]
    nt = Table(rows, colWidths=[38*mm, COL_W-38*mm], repeatRows=1, splitByRow=1)
    nt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD_BG, colors.HexColor('#0F0F14')]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, RULE_MIN),
        ('BOX', (0,0), (-1,-1), 0.4, CARD_EDGE),
        ('LINEAFTER', (0,0), (0,-1), 0.3, RULE_MIN),
    ]))
    story.append(nt)

    story.append(PageBreak()); story.append(sp(0))

    # ── SECTION 03: THE INVESTPUPPY MARK ─────────────────────────────────────
    section_opener('03', 'The InvestPuppy Mark', 'The maker\u2019s brand.', story)

    story.append(p(
        'InvestPuppy is an unconventional name for a company building institutional-grade '
        'financial infrastructure. It was chosen deliberately. The name is a filter: if it '
        'makes you curious, you are probably our kind of client. If it makes you '
        'uncomfortable, other, more traditional vendors are available.', S_body))
    story.append(p(
        'We are serious about portfolios. We are not serious about ourselves. '
        'That is the distinction the mark is built on.', S_decl_close))
    story.append(sp(10))
    story.append(HRule(COL_W,RULE_MAJ,0.5,4,4))
    story.append(sp(8))
    story.append(p('Serious when it matters.', S_decl_swim))
    story.append(sp(8))

    # Panel endorsement — confident framing
    story.append(NoteBox(COL_W,
        'A panel of UK institutional practitioners \u2014 including a senior discretionary '
        'portfolio manager (\u00a3400M book, 32 mandates), a McKinsey senior manager in '
        'fintech, a former investment banking MD with eleven fintech investments, a financial '
        'services copywriter, and an institutional fintech editor \u2014 reviewed the brand '
        'positioning. Their conclusion was unanimous: <b>the name is an asset, not a '
        'liability \u2014 when owned with conviction.</b> Memorability is a commercial '
        'mechanism. Polarisation is segmentation working correctly. The name is recalled '
        'when generic names are not.', S_grey))
    story.append(sp(10))

    story.append(p('THE ILLUSTRATION', S_subh))
    story.append(p(
        'The mark centres on a simplified dog face \u2014 rendered in single continuous '
        'outline strokes, clean geometry, no fill. It reads immediately as confident without '
        'being cartoonish. The construction discipline matches the Vektor wordmark: both marks '
        'are built from lines, not fills. Both are flat by specification.', S_body))
    story.append(p(
        'Overlaid across the illustration is a stock performance chart: a V-shaped recovery '
        'to an upward trajectory, terminating in an arrowhead. This is the same directional '
        'signal as the Vektor arrowhead \u2014 not a coincidence, a system. The arrow carries '
        'a luminous spark at the arrowhead: the moment the signal fires. On dark backgrounds '
        'this renders as a visible glow. It is the one moment of energy in an otherwise '
        'controlled illustration.', S_body))

    story.append(p('THE WORDMARK SPLIT', S_subh))
    story.append(p(
        '\u2018Invest\u2019 is rendered in platinum or near-white \u2014 the institutional '
        'context, the function, the serious half. \u2018Puppy\u2019 is rendered in the brand '
        'green \u2014 the differentiating half, the signal that this is not what you expected. '
        'The split encodes the brand\u2019s duality in a single word: both serious and '
        'irreverent simultaneously, the colour making it legible at a glance.', S_body))

    story.append(p('THE FOUR VARIANTS', S_subh))
    variants = [
        ('Horizontal \u2014 Dark (IPHorizontalClear)',
         'Dog left, wordmark right. \u2018Invest\u2019 in near-white, \u2018Puppy\u2019 in '
         'green. Transparent background. Use on dark-background PDF footers and headers.'),
        ('Vertical \u2014 Dark (IPVerticalClear)',
         'Dog above, wordmark below. Transparent background. Use on dark-background cover '
         'pages where the mark has a standalone presence.'),
        ('Horizontal \u2014 Light (IPHorizontalInvClear)',
         '\u2018Invest\u2019 in solid black, \u2018Puppy\u2019 in green. Transparent '
         'background. Use on white-background Word documents and light PPTX slides.'),
        ('Vertical \u2014 Light (IPVerticalInvClear)',
         '\u2018Invest\u2019 in solid black. Transparent background. Use on '
         'white-background cover pages and title slides.'),
    ]
    vt_rows = [[p('VARIANT', S_th), p('USE CONTEXT', S_th)]]
    for vname, vdesc in variants:
        vt_rows.append([p(vname, S_tgold), p(vdesc, S_tb)])
    vt2 = Table(vt_rows, colWidths=[52*mm, COL_W-52*mm], repeatRows=1)
    vt2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD_BG, colors.HexColor('#0F0F14')]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 7), ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, RULE_MIN),
        ('BOX', (0,0), (-1,-1), 0.4, CARD_EDGE),
        ('LINEAFTER', (0,0), (0,-1), 0.3, RULE_MIN),
    ]))
    story.append(vt2); story.append(sp(10))

    story.append(p('DEPLOYMENT RULES', S_subh))
    deploy_rules = [
        ('Commercial document covers',
         'Horizontal dark variant. 38mm wide. Bottom-left, above the compliance line. '
         'Applies to: Brochure, At a Glance, Why Vektor, FAQ, Founding Mandate Programme.'),
        ('Interior PDF footers (all dark-background documents)',
         'Horizontal dark variant. 32mm wide. Left-aligned below the footer rule. '
         'Right-aligned companion: investpuppy.com \u00b7 date.'),
        ('White-background Word documents',
         'Horizontal light variant. \u2018Invest\u2019 in black ensures legibility.'),
        ('PPTX title slides',
         'Vertical light variant. Content slides: horizontal light variant in footer only.'),
        ('White paper covers (WP-00 through WP-10)',
         'Footer only \u2014 no cover mark. Technical documents for committed readers.'),
    ]
    for rt, rb in deploy_rules:
        story.append(p(rt, S_deploy_hdr))
        story.append(p(rb, S_body))

    story.append(PageBreak()); story.append(sp(0))

    # ── SECTION 04: THE VEKTOR MARK ───────────────────────────────────────────
    section_opener('04', 'The Vektor Mark',
                   'A logo that is also a mathematical statement.', story)
    story.append(p(
        'The Vektor wordmark is not a logo with a concept attached \u2014 it is a concept '
        'expressed as a logo. Every geometric decision maps directly to something the platform '
        'does. A designer reading the brief and a portfolio manager reading the mark should '
        'arrive at the same understanding.', S_body))

    story.append(p('THE V \u2014 ASYMMETRIC BY DESIGN', S_subh))
    story.append(p(
        'The two strokes of the V are not equal. The left arm is visibly heavier \u2014 a thick, '
        'structural stroke representing the weight of capital deployed. It is the magnitude '
        'component of the portfolio equation: how much is committed, and with what conviction. '
        'The right arm is lighter and longer, extending past cap height before terminating in '
        'the arrowhead. It represents the signal, the trajectory, the algorithmic direction '
        'that determines where capital moves.', S_body))
    v_rows = [[
        p('Heavy left stroke', S_th), p('Lighter right stroke', S_th),
    ],[
        p('Capital magnitude. The weight of capital deployed \u2014 how much is committed, '
          'and with what conviction.', S_tb),
        p('Signal direction. The trajectory that determines where capital moves \u2014 the '
          'algorithmic instruction that drives the position.', S_tb),
    ]]
    vt = Table(v_rows, colWidths=[COL_W/2, COL_W/2])
    vt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('LINEAFTER', (0,0), (0,-1), 0.3, RULE_MIN),
        ('BOX', (0,0), (-1,-1), 0.4, CARD_EDGE),
        ('LINEBELOW', (0,0), (-1,0), 0.3, RULE_MIN),
    ]))
    story.append(vt); story.append(sp(8))
    story.append(p(
        'Asymmetry in a letterform is unusual enough to register subconsciously. A '
        'quantitatively literate reader sees the vector duality immediately. A reader without '
        'that background feels authority without being able to name the source. The mark works '
        'for both audiences simultaneously.', S_body))

    story.append(p('THE ARROWHEAD \u2014 NOTATION, NOT DECORATION', S_subh))
    story.append(p(
        'In vector mathematics, a quantity is denoted by placing a right-arrow above the '
        'variable name. The arrowhead integrated into Vektor\u2019s right stroke is that '
        'notation, realised as a structural element of the letterform itself \u2014 not placed '
        'above the letter as a diacritic, but growing from the stroke as its natural terminus. '
        'One continuous object. One continuous intention.', S_body))
    arrow_rows = [[
        p('Open, not filled', S_th), p('Integrated, not placed', S_th), p('Gold, not platinum', S_th),
    ],[
        p('A filled triangle reads as a decorative chevron. An open arrowhead reads as '
          'notation \u2014 precise, technical, a different register.', S_tb),
        p('The arrowhead is the natural terminus of the V\u2019s right stroke. It grows from '
          'it \u2014 one continuous object, one continuous intention.', S_tb),
        p('Gold applied everywhere is decoration. Gold applied once \u2014 to the directional '
          'element only \u2014 is meaning.', S_tb),
    ]]
    at = Table(arrow_rows, colWidths=[COL_W/3]*3)
    at.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEAFTER', (0,0), (1,-1), 0.3, RULE_MIN),
        ('BOX', (0,0), (-1,-1), 0.4, CARD_EDGE),
        ('LINEBELOW', (0,0), (-1,0), 0.3, RULE_MIN),
    ]))
    story.append(at); story.append(sp(8))

    story.append(p('THE TYPEFACE \u2014 GEOMETRIC WITHOUT COMPROMISE', S_subh))
    story.append(p(
        'The EKTOR letters are specified in Termina Bold \u2014 a pure geometric sans-serif '
        'with flat-cut stroke terminals, uniform stroke weight, and no humanist '
        'characteristics. Termina was chosen because its construction language matches the '
        "V\u2019s architecture precisely: both are built from geometry, not calligraphic "
        'tradition. The result is a wordmark where the custom-drawn V and the typeset EKTOR '
        'feel as though they came from the same hand.', S_body))
    story.append(p(
        "The K in EKTOR carries an additional function: its diagonal strokes, drawn at the "
        "same angular sharpness as the arrowhead geometry in the V, create a quiet internal "
        "rhythm across the wordmark \u2014 a detail that rewards close reading without "
        "announcing itself.", S_body))

    story.append(PageBreak()); story.append(sp(0))

    # ── SECTION 05: THE COLOUR SYSTEM ────────────────────────────────────────
    section_opener('05', 'The Colour System', 'Three colours. Each one earns its place.', story)
    story.append(p(
        'The palette was not assembled \u2014 it was specified. Each colour has a defined role '
        'and a defined rule governing where and how it appears.', S_body))
    colour_rows = [[
        p('NEAR-BLACK', S_th), p('PLATINUM', S_th), p('AMBER GOLD', S_th),
    ],[
        p('#0A0A0F', S_tgold), p('#E8E8EC', S_tgold), p('#C8A96E', S_tgold),
    ],[
        p('Primary background. Canonical dark ground.', S_tb),
        p('Primary mark colour. All letterforms.', S_tb),
        p('Accent. Arrowhead strokes only.', S_tb),
    ]]
    ct = Table(colour_rows, colWidths=[COL_W/3]*3)
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('LINEAFTER', (0,0), (1,-1), 0.3, RULE_MIN),
        ('BOX', (0,0), (-1,-1), 0.4, CARD_EDGE),
        ('LINEBELOW', (0,0), (-1,0), 0.3, RULE_MIN),
        ('LINEBELOW', (0,1), (-1,1), 0.3, RULE_MIN),
    ]))
    story.append(ct); story.append(sp(8))
    story.append(NoteBox(COL_W,
        '<b>Colour discipline note:</b> The single-application rule for gold applies '
        'specifically to the primary mark \u2014 the wordmark itself. In document and '
        'communications applications, gold functions as a structural accent to signal '
        'directional elements: the Founder\u2019s Note bar, hex references, and the closing '
        'page rule. This mirrors the arrowhead\u2019s function in the mark \u2014 gold '
        'appears where something specific is being signalled, and nowhere else.', S_grey))
    story.append(sp(10))
    story.append(p('THE COLOUR RULES', S_subh))
    for rule_title, rule_body in [
        ('Gold appears once in the primary mark.',
         'In the canonical dark-ground wordmark, the gold accent is applied to the arrowhead '
         'strokes only. Not to the V. Not to EKTOR. Not to the sub-brand. The moment gold '
         'appears on more than one element, it loses its function as a signal and becomes decoration.'),
        ('The dark ground is canonical.',
         'Near-black is the primary application. The light-ground version exists for print and '
         'document contexts but is always secondary. Vektor presents itself in darkness because '
         'that is where precision instruments live: trading terminals, portfolio dashboards, '
         'technical interfaces.'),
        ('No gradients. No dimensional effects. No shadows.',
         'The mark is flat by specification, not convention. Gradients imply softness. Vektor '
         'implies structural rigour. A flat mark reproduced consistently across every application '
         'is more powerful than a rendered mark that varies by medium.'),
    ]:
        story.append(p(rule_title, S_deploy_hdr))
        story.append(p(rule_body, S_body))

    story.append(PageBreak()); story.append(sp(0))

    # ── SECTION 06: THE BRAND IN PRACTICE ────────────────────────────────────
    section_opener('06', 'The Brand in Practice', 'What both marks do in a room.', story)
    story.append(p(
        'A brand is not what it says about itself. It is what it makes a reader feel in the '
        'first three seconds before any claim has been evaluated. These are the specific '
        'responses the Vektor and InvestPuppy marks are designed to produce at each stage '
        'of a professional engagement.', S_body))

    for title, body in [
        ('When the document lands on a desk',
         'The cover \u2014 dark ground, Vektor mark prominent, gold arrowhead, InvestPuppy '
         'mark bottom-left as maker\u2019s attribution \u2014 produces one instinctive '
         'response: this is not a consumer product. Both marks are present from the first '
         'second. The relationship between them is legible before a word has been read.'),
        ('When the Vektor mark is examined closely',
         'The asymmetric V rewards attention. A quantitatively literate reader sees the '
         'vector notation immediately. A reader without that background feels the precision '
         'without naming it. The mark does different work for different audiences '
         'simultaneously, and correctly for both.'),
        ('When InvestPuppy is noticed for the first time',
         'The prospect who notices the maker\u2019s mark and pauses is the target audience. '
         'The name produces a moment of curiosity. That moment is the beginning of the '
         'commercial relationship. Platforms that produce no reaction are forgotten in '
         'twenty minutes. Vektor by InvestPuppy is recalled when it matters.'),
        ('When the name is mentioned in conversation',
         'Vektor is pronounceable in every major language, short enough to anchor in memory '
         'after one hearing, and correctly spelt after one reading. InvestPuppy is recalled '
         'in referral conversations precisely because it is unexpected. \u201cHave you met '
         'the InvestPuppy team?\u201d is a better sentence than any name chosen to sound '
         'institutional.'),
        ('When it appears in a due diligence document',
         '\u2018Platform: Vektor\u2019 on a vendor questionnaire reads as a system name, not '
         'a company name. It has the right register for compliance documentation without '
         'requiring explanation. By InvestPuppy, when it appears, reads as a '
         'manufacturer\u2019s designation rather than a consumer brand.'),
    ]:
        story.append(p(title, S_deploy_hdr))
        story.append(p(body, S_body))

    story.append(sp(10))
    story.append(hrgold())
    story.append(sp(6))
    story.append(p(
        'The K distinguishes the mark in a crowded namespace and signals intentionality. '
        'The asymmetric V encodes the magnitude-direction duality into the letterform. '
        'The gold arrowhead is the vector notation symbol realised as a single geometric '
        'stroke. The InvestPuppy mark signals that the people behind the platform are more '
        'interested in the quality of their work than the hyperbole of their messaging. '
        'Both marks are complete on their own terms. Together they say something neither '
        'could say alone: that serious work and serious character are not in tension '
        '\u2014 that one is the evidence of the other.', S_grey))
    story.append(sp(10))
    story.append(HRule(COL_W, RULE_MAJ, 1.0, 2, 6))
    story.append(p('Every element earns its place. Nothing is decorative.', S_close))
    story.append(HRule(COL_W, RULE_MAJ, 1.0, 6, 2))
    story.append(sp(10))
    story.append(p(
        f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  '
        f'{DOC_AUDIENCE}  \u00b7  {DATE}', S_ref))
    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    r = subprocess.run(['pdfinfo', out], capture_output=True, text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l or 'File' in l:
            print(l)


if __name__ == '__main__':
    build()
