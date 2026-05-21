"""
WP-01: Quantitative Portfolio Construction for Single-Country Equity Markets
Rebuilt from existing PDF content. Corrections applied:
  - Series label: VEKTOR RESEARCH SERIES · 2026 (was INVESTPUPPY)
  - Key Takeaway 3: two-step description of 10,000 configs + MPT
  - Footer: Vektor Research Series (was InvestPuppy Research Series)
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
    PageBreak, NextPageTemplate, Image,
)
from reportlab.platypus.flowables import Flowable

# ── Brand ──────────────────────────────────────────────────────────────────────
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

W, H   = A4
ML = MR = 22*mm
MT1    = 16*mm
MT2    = 46*mm
MB     = 20*mm
COL_W  = W - ML - MR

LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png')
CHART_PATH = _os.path.join(_SCREENSHOTS, 'sc02_frontier.png')
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')
IP_H_RATIO = 2.337
DOC_DATE   = 'May 2026'
DOC_REF    = 'IP-WP-QPC-260430-1.2'
DOC_TITLE  = 'Quantitative Portfolio Construction'
DOC_SERIES = 'VEKTOR RESEARCH SERIES · 2026'
FOOTER_STR = f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  Vektor Research Series 2026  \u00b7  {DOC_DATE}'


# ── Styles ─────────────────────────────────────────────────────────────────────
def S():
    s = {}
    s['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=24, textColor=PLATINUM,
        alignment=TA_CENTER, leading=30)
    s['cover_distil'] = ParagraphStyle('cover_distil',
        fontName='Helvetica-Oblique', fontSize=11, textColor=WARM_GREY,
        alignment=TA_CENTER, leading=19)
    s['abstract_tag'] = ParagraphStyle('abstract_tag',
        fontName='Helvetica', fontSize=7, textColor=WARM_GREY,
        leading=11, spaceAfter=6, letterSpacing=4)
    s['kt_item'] = ParagraphStyle('kt_item',
        fontName='Helvetica', fontSize=9.5, textColor=OFF_WHITE,
        leading=17, spaceAfter=8, alignment=TA_JUSTIFY)
    s['wp_ref'] = ParagraphStyle('wp_ref',
        fontName='Helvetica', fontSize=7.5,
        textColor=colors.HexColor('#555550'),
        leading=11, alignment=TA_LEFT)
    s['section_title'] = ParagraphStyle('section_title',
        fontName='Helvetica-Bold', fontSize=16, textColor=PLATINUM,
        leading=22, spaceAfter=5, spaceBefore=4)
    s['section_lead'] = ParagraphStyle('section_lead',
        fontName='Helvetica-Oblique', fontSize=10, textColor=WARM_GREY,
        leading=16, spaceAfter=10, alignment=TA_JUSTIFY)
    s['sub_head'] = ParagraphStyle('sub_head',
        fontName='Helvetica-Bold', fontSize=11, textColor=GOLD,
        leading=16, spaceAfter=5, spaceBefore=12)
    s['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=9.5, textColor=OFF_WHITE,
        leading=17, spaceAfter=10, alignment=TA_JUSTIFY)
    s['body_grey'] = ParagraphStyle('body_grey',
        fontName='Helvetica', fontSize=9.5, textColor=WARM_GREY,
        leading=17, spaceAfter=10, alignment=TA_JUSTIFY)
    s['caption'] = ParagraphStyle('caption',
        fontName='Helvetica-Oblique', fontSize=8, textColor=WARM_GREY,
        alignment=TA_CENTER, leading=12)
    s['pi_label'] = ParagraphStyle('pi_label',
        fontName='Helvetica', fontSize=7, textColor=WARM_GREY,
        leading=10, letterSpacing=2)
    s['footer'] = ParagraphStyle('footer',
        fontName='Helvetica', fontSize=6.5,
        textColor=colors.HexColor('#444440'),
        leading=10, alignment=TA_CENTER)
    s['xref'] = ParagraphStyle('xref',
        fontName='Helvetica', fontSize=8.5, textColor=WARM_GREY,
        leading=14, alignment=TA_CENTER)
    return s


# ── Flowables ──────────────────────────────────────────────────────────────────
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
    def __init__(self, w, text, style, bg=NOTE_BG, bar=RULE_MAJ, ph=15, pv=13, bw=4):
        Flowable.__init__(self)
        self._w=w; self.bg=bg; self.bar=bar; self.ph=ph; self.pv=pv; self.bw=bw
        self._p = Paragraph(text, style)
        self._iw = w - bw - ph*2
    def wrap(self, aw, ah):
        _, h = self._p.wrap(self._iw, ah)
        self.height = h + self.pv*2
        return self._w, self.height
    def draw(self):
        c=self.canv; c.saveState()
        c.setFillColor(self.bg); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0, 0, self._w, self.height, 3, fill=1, stroke=1)
        c.setFillColor(self.bar); c.roundRect(0,0,self.bw,self.height,2,fill=1,stroke=0)
        self._p.wrap(self._iw, self.height)
        self._p.drawOn(c, self.bw+self.ph, self.pv)
        c.restoreState()


class PlatformInterfaceCard(Flowable):
    """Screenshot card matching original style."""
    def __init__(self, w, img_path, caption_text, S):
        Flowable.__init__(self)
        self._w = w; self._img = img_path
        self._cap = Paragraph(caption_text, S['caption'])
        self._label = Paragraph('PLATFORM INTERFACE', S['pi_label'])
        self._S = S
        self._pad = 10
    def wrap(self, aw, ah):
        from reportlab.lib.utils import ImageReader
        img = ImageReader(self._img)
        iw, ih = img.getSize()
        inner_w = self._w - self._pad*2
        scale = inner_w / iw
        self._ih_scaled = ih * scale
        self._iw_scaled = inner_w
        _, lh = self._label.wrap(inner_w, ah)
        _, ch = self._cap.wrap(inner_w, ah)
        self.height = (self._pad + lh + 6 + self._ih_scaled +
                       6 + ch + self._pad)
        return self._w, self.height
    def draw(self):
        c=self.canv; c.saveState()
        c.setFillColor(CARD_BG); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0, 0, self._w, self.height, 3, fill=1, stroke=1)
        # Label
        y = self.height - self._pad
        inner_w = self._w - self._pad*2
        _, lh = self._label.wrap(inner_w, self.height)
        y -= lh
        self._label.drawOn(c, self._pad, y)
        y -= 6
        # Image
        y -= self._ih_scaled
        c.drawImage(self._img, self._pad, y, self._iw_scaled, self._ih_scaled,
                    preserveAspectRatio=True)
        y -= 6
        # Caption
        _, ch = self._cap.wrap(inner_w, self.height)
        y -= ch
        self._cap.drawOn(c, self._pad, y)
        c.restoreState()


# ── Page templates ─────────────────────────────────────────────────────────────
def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    from reportlab.lib.utils import ImageReader
    try:
        img = ImageReader(LOGO); iw,ih = img.getSize()
        lw=min(W*0.62,320); lh=lw*ih/iw; lx=(W-lw)/2; ly=H*0.52
        canvas.drawImage(LOGO, lx, ly-lh, lw, lh, mask='auto', preserveAspectRatio=True)
        ry = ly-lh-14
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8)
        canvas.line(ML, ry, W-MR, ry)
        canvas.setFont('Helvetica', 7); canvas.setFillColor(WARM_GREY)
        # CORRECTED: VEKTOR RESEARCH SERIES not INVESTPUPPY
        canvas.drawCentredString(W/2, ry-14, DOC_SERIES)
        # Document title
        canvas.setFont('Helvetica-Bold', 22); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2, ry-48, 'Quantitative Portfolio')
        canvas.drawCentredString(W/2, ry-74, 'Construction')
        canvas.setFont('Helvetica-Bold', 16); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2, ry-98, 'for Single-Country Equity Markets')
        # Distillation
        canvas.setFont('Helvetica-Oblique', 9.5); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2, ry-122,
            'A replicable five-stage framework \u2014 universe screening,')
        canvas.drawCentredString(W/2, ry-136,
            '10,000 portfolio configurations, and benchmark validation.')
    except Exception as e: print(f'Logo: {e}')
    # Bottom section
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4)
    canvas.line(ML, 36*mm, W-MR, 36*mm)
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(WARM_GREY)
    canvas.drawCentredString(W/2, 28*mm, 'For professional and institutional investors only')
    canvas.setFont('Helvetica', 7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W/2, 22*mm,
        f'Vektor Research Series  \u00b7  {DOC_REF}  \u00b7  Copyright 2026')
    canvas.drawCentredString(W/2, 16*mm, DOC_DATE)
    canvas.restoreState()


def draw_first(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    _footer(canvas)
    canvas.restoreState()


def draw_later(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    _header(canvas, doc)
    _footer(canvas)
    canvas.restoreState()


def _header(canvas, doc):
    from reportlab.lib.utils import ImageReader
    hy = H - MT2 + 14
    try:
        img = ImageReader(LOGO); iw,ih = img.getSize()
        lh=22; lw=lh*iw/ih
        canvas.drawImage(LOGO, ML, hy, lw, lh, mask='auto', preserveAspectRatio=True)
    except:
        canvas.setFont('Helvetica-Bold', 9); canvas.setFillColor(PLATINUM)
        canvas.drawString(ML, hy+4, 'VEKTOR')
    canvas.setFont('Helvetica', 7)
    canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawRightString(W-MR, H-MT2+18,
        f'{DOC_TITLE}  \u00b7  {doc.page-1:02d}')
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.4)
    canvas.line(ML, H-MT2+8, W-MR, H-MT2+8)


def _footer(canvas):
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.3)
    canvas.line(ML, MB-2, W-MR, MB-2)
    ip_w=32*mm; ip_h=ip_w/IP_H_RATIO
    try:
        canvas.drawImage(IP_H,ML,1.0*mm,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawRightString(W-MR,1.0*mm+ip_h/2-2.5,f'investpuppy.com  ·  {DOC_DATE}')
# ── Helpers ────────────────────────────────────────────────────────────────────
def para(text, s, st='body'): return Paragraph(text, s[st])
def sp(n=8): return Spacer(1, n)
def hrm(): return HRule(COL_W, RULE_MAJ, 1.0, 4, 6)

def section(num_title, lead, s):
    out = []
    out.append(hrm())
    out.append(para(num_title, s, 'section_title'))
    out.append(para(lead, s, 'section_lead'))
    return out


# ── Build ──────────────────────────────────────────────────────────────────────
def build():
    out = '/home/claude/investpuppy/vektor/output/pdf/vk5-wp01-quantitative-portfolio-construction.pdf'
    s = S()

    f_cover = Frame(0,0,W,H,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='cover')
    f_first = Frame(ML, MB, COL_W, H-MT1-MB, id='first')
    f_later = Frame(ML, MB, COL_W, H-MT2-MB, id='later')

    doc = BaseDocTemplate(out, pagesize=A4,
        leftMargin=ML, rightMargin=MR, topMargin=MT1, bottomMargin=MB,
        title='Quantitative Portfolio Construction \u2014 Vektor by InvestPuppy',
        author='InvestPuppy')
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[f_cover], onPage=draw_cover),
        PageTemplate(id='First', frames=[f_first], onPage=draw_first),
        PageTemplate(id='Later', frames=[f_later], onPage=draw_later),
    ])

    story = []

    # ── COVER ──────────────────────────────────────────────────────────────────
    story.append(Spacer(1,1))
    story.append(NextPageTemplate('First'))
    story.append(PageBreak())

    # ── ABSTRACT PAGE ──────────────────────────────────────────────────────────
    story.append(para('ABSTRACT', s, 'abstract_tag'))
    story.append(NoteBox(COL_W,
        'This paper describes the methodology the Vektor platform uses \u2014 not the approach '
        'we are building toward, but the framework running today. It presents a replicable, '
        'quantitative framework for constructing equity portfolios in domestic markets '
        'characterised by a bounded investable universe, concentrated sector exposure, and structural '
        'liquidity constraints. Drawing on a worked implementation across SGX-listed equities, we demonstrate how '
        'disciplined universe screening, 10,000 portfolio configurations mapping the efficient frontier, and '
        'index-relative tracking error minimisation can be combined into a coherent, scalable investment process. '
        'The principles generalise across any single-country equity market where a national benchmark index exists.',
        s['body']))

    story.append(sp(16))
    story.append(para('KEY TAKEAWAYS', s, 'abstract_tag'))
    story.append(HRule(COL_W, RULE_MIN, 0.3, 4, 6))

    kts = [
        'A five-stage, benchmark-aware workflow can produce diversified domestic equity portfolios even in '
        'small, concentrated markets.',
        'Liquidity and dividend-continuity screens reduce implementation risk without turning the process into '
        'a pure yield strategy.',
        # CORRECTED KEY TAKEAWAY 3
        '10,000 portfolio configurations generate the empirical efficient frontier; Modern Portfolio Theory '
        'identifies the maximum Sharpe portfolio from within it \u2014 providing a transparent, reproducible '
        'audit trail from universe to final holdings.',
    ]
    for kt in kts:
        story.append(para(f'\u2014 {kt}', s, 'kt_item'))

    story.append(sp(14))
    story.append(para(
        f'Reference: {DOC_REF}  \u00b7  Copyright 2026 InvestPuppy  \u00b7  investpuppy.com',
        s, 'wp_ref'))

    story.append(NextPageTemplate('Later'))
    story.append(PageBreak())

    # ── SECTION 1 ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0))
    for item in section(
        '1. INTRODUCTION',
        'Why domestic quant mandates are harder than they look: a small universe, sector concentration, '
        'and liquidity constraints force discipline in screening and portfolio construction.',
        s):
        story.append(item)

    story.append(para(
        'This paper describes a five-stage framework: universe definition, liquidity and quality filtering, '
        'disciplined universe screening, 10,000 portfolio configurations mapping the efficient frontier, '
        'and index-relative tracking error minimisation against the domestic benchmark. We use SGX-listed '
        'equities as the primary illustrative dataset, with the Straits Times Index (STI) as the reference benchmark.',
        s))

    story.append(NoteBox(COL_W,
        'From an implementation perspective, the framework aligns with a standard client-portfolio workflow: a '
        'research function defines the investable universe; a portfolio management function approves the '
        'strategy and generates target allocations; and an operations function ensures funding is available. '
        'This structure supports an auditable mapping from analytical inputs to investable outputs \u2014 the '
        'same structure embodied in the Vektor platform.',
        s['body']))

    # ── SECTION 2 ──────────────────────────────────────────────────────────────
    for item in section(
        '2. UNIVERSE DEFINITION AND SECTOR MAPPING',
        'Define the investable set first: exclude non-ordinary listings, map sectors consistently, and make '
        'explicit which parts of the market you are structurally choosing to own \u2014 or not own.',
        s):
        story.append(item)

    story.append(para(
        'Universe definition is not merely administrative. The choice of sectors establishes the '
        'strategy\u2019s factor exposures from the outset. A strategy that excludes REITs, for example, will '
        'exhibit materially different yield and duration characteristics than one that includes them.',
        s))

    story.append(NoteBox(COL_W,
        'SGX implementation: the starting point is the set of listed ordinary equities \u2014 several hundred '
        'names. Prior to applying investability constraints, constituents are mapped into broad sector groupings '
        '(financials, real estate, industrials) so that sector exposures can be monitored explicitly throughout '
        'the optimisation process.',
        s['body_grey']))

    # ── SECTION 3 ──────────────────────────────────────────────────────────────
    for item in section(
        '3. LIQUIDITY AND QUALITY FILTERING',
        'Screens should reduce implementation risk: calibrate liquidity to strategy size and use dividend '
        'continuity as a practical proxy for business quality.',
        s):
        story.append(item)

    story.append(para(
        'The quality filter applies dividend continuity as a proxy for business stability, retaining only '
        'companies that have paid dividends in at least two of the preceding three fiscal years. This is not a '
        'yield-maximisation screen \u2014 it is a quality screen. Companies with consistent dividend histories '
        'tend to exhibit lower earnings volatility and more disciplined capital allocation. Liquidity thresholds '
        'should be stated explicitly and calibrated to mandate size.',
        s))

    story.append(para(
        'A minimum average daily volume screen (e.g., >100,000 shares/day) reduces implementation shortfall '
        'and mitigates the risk of selecting statistically attractive but illiquid securities.',
        s))

    # ── SECTION 4 ──────────────────────────────────────────────────────────────
    for item in section(
        '4. PORTFOLIO CONFIGURATION AND EFFICIENT FRONTIER ANALYSIS',
        'Generate 10,000 portfolio configurations to map the feasible set and make the '
        'risk-return trade-off explicit for your market.',
        s):
        story.append(item)

    story.append(para(
        'Each simulated portfolio is evaluated on three dimensions: annualised return (trailing 3 years), '
        'annualised volatility, and Sharpe ratio. The resulting scatter plot \u2014 the empirical efficient '
        'frontier \u2014 reveals the risk-return trade-off surface available within this universe. This surface '
        'is market-specific: the shape of the SGX frontier differs materially from the KOSPI or ASX frontier '
        'due to differences in sector concentration, correlation structure, and individual stock volatility profiles.',
        s))

    # Add target optimization formula screenshot showing the mathematical basis
    SC12 = _os.path.join(_SCREENSHOTS, 'sc12_target_optimization.png')
    if _os.path.exists(SC12):
        story.append(sp(4))
        story.append(PlatformInterfaceCard(COL_W, SC12,
            'Target optimisation logic \u2014 the algorithm runs 10,000 simulations to find the optimal '
            'portfolio subset. Mathematical formula for weight calculation, portfolio returns, active returns, '
            'tracking error, and information ratio are fully documented and reproducible.',
            s))
        story.append(sp(8))

    story.append(sp(6))
    story.append(PlatformInterfaceCard(COL_W, CHART_PATH,
        'Efficient frontier \u2014 SGX equity mandate. Each point is one simulated portfolio. '
        'Red\u00a0=\u00a0high Sharpe, blue\u00a0=\u00a0low Sharpe. Star marks the max-Sharpe selection.',
        s))
    story.append(sp(8))

    story.append(NoteBox(COL_W,
        'With sufficient sampling the empirical frontier stabilises. 10,000 constrained portfolio configurations '
        'are typically adequate to characterise the feasible risk-return region. Modern Portfolio Theory then '
        'identifies the maximum Sharpe portfolio from within the mapped space. The frontier plot, with the '
        'selected portfolio highlighted, serves as a reproducible artefact for model governance and review.',
        s['body_grey']))

    story.append(PageBreak())

    # ── SECTION 5 ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0))
    for item in section(
        '5. EFFICIENT FRONTIER OPTIMISATION AND STOCK SELECTION',
        'Select on risk-adjusted merit, then validate against the benchmark: combine frontier selection with '
        'sector coverage and explicit tracking-error limits.',
        s):
        story.append(item)

    story.append(para(
        'The final stock selection is validated against the benchmark on two criteria: sector coverage (at '
        'least one stock from each of the three primary sectors) and tracking error (annualised tracking error '
        'against the STI below 8%). Two diagnostics assess genuine diversification: an allocation-weight view '
        'makes concentration transparent, and a correlation matrix confirms that selected holdings are not '
        'near-substitutes co-moving through market cycles.',
        s))

    # ── SECTION 6 ──────────────────────────────────────────────────────────────
    for item in section(
        '6. GENERALISABILITY AND IMPLEMENTATION',
        'Port the framework by tuning the inputs: set market-appropriate liquidity bars, choose the correct '
        'national benchmark, and add diversification constraints when indices are highly concentrated.',
        s):
        story.append(item)

    story.append(para(
        'Data infrastructure requirements are modest: three years of daily OHLCV price data, dividend history, '
        'and daily trading volume \u2014 all available from standard financial data providers for most listed '
        'markets globally.',
        s))

    story.append(para('6.1 Operationalisation \u2014 Platform Workflow', s, 'sub_head'))
    story.append(para(
        'In a production setting, the five-stage method is organised into two phases: (a) strategy '
        'construction and validation and (b) client onboarding and allocation. A manager review gate prior to '
        'client assignment establishes an approval record for strategy metadata, holdings, weights, and '
        'benchmark-validation results.',
        s))

    story.append(NoteBox(COL_W,
        'Operational completeness requires (i) a funding step with an auditable record and (ii) a defined '
        'market-data refresh policy comprising daily OHLCV history with routine updates, supplemented by '
        'exchange-rate series for multi-currency mandates.',
        s['body_grey']))

    # ── SECTION 7 ──────────────────────────────────────────────────────────────
    for item in section(
        '7. CONCLUSION',
        'In domestic markets, robustness comes from explicit constraints, transparent optimisation, and '
        'benchmark-aware validation.',
        s):
        story.append(item)

    story.append(para(
        'Systematic portfolio construction in domestic equity markets is not merely a scaled-down version of '
        'global quant strategies. The constraints of a bounded universe, concentrated sectors, and liquidity '
        'limitations demand purpose-built frameworks. The five-stage process described here provides a rigorous, '
        'replicable foundation for any single-country equity mandate. The SGX implementation demonstrates that '
        'meaningful diversification and strong risk-adjusted returns are achievable even within a relatively '
        'small domestic universe.',
        s))

    story.append(sp(12))
    story.append(HRule(COL_W, GOLD, 0.8))
    story.append(sp(8))

    story.append(para(
        'This paper describes the methodology underpinning the Vektor platform. To see the framework applied '
        'live to your mandate \u2014 any listed equity market, any currency, any benchmark \u2014 enquire '
        'about the Proof Partners programme at investpuppy.com. For the commercial case, see the companion '
        'document: Why Vektor.',
        s, 'xref'))

    story.append(sp(12))
    ref_style = ParagraphStyle('ref_bottom', fontName='Helvetica', fontSize=7.5,
        textColor=colors.HexColor('#555550'), leading=11, alignment=TA_CENTER)
    story.append(Paragraph(
        f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {DOC_REF}  \u00b7  Copyright 2026 InvestPuppy',
        ref_style))

    # ── BUILD ──────────────────────────────────────────────────────────────────
    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    r = subprocess.run(['pdfinfo', out], capture_output=True, text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l or 'File size' in l: print(l)

if __name__ == '__main__':
    build()
