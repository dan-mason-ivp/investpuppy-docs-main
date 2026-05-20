"""
Why Vektor — vk3 rebuild.
vk2 baseline + InvestPuppy brand integration:
  - "A Note on the Name" replaced with "The InvestPuppy Question" brand declaration (Expert G draft)
  - "simulations" corrected to "portfolio configurations" in metrics panel
  - Footer: IP horizontal mark (32mm, dark variant) replaces centred text
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

BG=colors.HexColor('#0A0A0F'); PLATINUM=colors.HexColor('#E8E8EC')
GOLD=colors.HexColor('#C8A96E'); OFF_WHITE=colors.HexColor('#E8E2D9')
WARM_GREY=colors.HexColor('#9A9086'); RULE_MAJ=colors.HexColor('#5A5A60')
RULE_MIN=colors.HexColor('#2A2828'); CARD_BG=colors.HexColor('#111116')
NOTE_BG=colors.HexColor('#16161A'); CARD_EDGE=colors.HexColor('#242428')
DARK_WARM=colors.HexColor('#0D0C0A')

W,H=A4; ML=MR=22*mm; MT1=16*mm; MT2=46*mm; MB=20*mm; COL_W=W-ML-MR
LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png'); DATE='May 2026'; SUB='Why Vektor'
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')
IP_H_RATIO=2.337

def mkstyle(name,**kw):
    defaults=dict(fontName='Helvetica',fontSize=9.5,textColor=OFF_WHITE,leading=17,spaceAfter=8)
    defaults.update(kw); return ParagraphStyle(name,**defaults)

S_tag=mkstyle('tag',fontSize=7,textColor=WARM_GREY,leading=11,letterSpacing=4,spaceAfter=4)
S_sec=mkstyle('sec',fontName='Helvetica-Bold',fontSize=16,textColor=PLATINUM,leading=22,spaceAfter=5)
S_sub=mkstyle('sub',fontName='Helvetica-Oblique',fontSize=11,textColor=WARM_GREY,leading=17,spaceAfter=10)
S_body=mkstyle('body',alignment=TA_JUSTIFY)
S_grey=mkstyle('grey',textColor=WARM_GREY,alignment=TA_JUSTIFY)
S_note=mkstyle('note',fontName='Helvetica-Oblique',textColor=WARM_GREY,leading=17,alignment=TA_JUSTIFY)
S_subh=mkstyle('subh',fontName='Helvetica-Bold',fontSize=11,textColor=GOLD,leading=16,spaceAfter=5,spaceBefore=12)
S_rnum=mkstyle('rnum',fontName='Helvetica-Bold',fontSize=20,textColor=colors.HexColor('#1A1A20'),leading=24)
S_rtit=mkstyle('rtit',fontName='Helvetica-Bold',fontSize=11,textColor=PLATINUM,leading=16,spaceAfter=5)
S_mn=mkstyle('mn',fontName='Helvetica-Bold',fontSize=20,textColor=GOLD,leading=24,alignment=TA_CENTER)
S_ml=mkstyle('ml',fontSize=7.5,textColor=WARM_GREY,leading=10,alignment=TA_CENTER,spaceAfter=0)
S_mc=mkstyle('mc',fontSize=8,textColor=OFF_WHITE,leading=12,alignment=TA_CENTER)
S_pull=mkstyle('pull',fontName='Helvetica-Oblique',fontSize=11,textColor=PLATINUM,leading=18,alignment=TA_CENTER)
S_xref=mkstyle('xref',fontSize=8.5,textColor=WARM_GREY,leading=14,alignment=TA_CENTER)
S_ref=mkstyle('ref',fontSize=7.5,textColor=colors.HexColor('#555550'),leading=11,alignment=TA_CENTER)
S_fmp_tt=mkstyle('ftt',fontName='Helvetica-Bold',fontSize=13,textColor=GOLD,leading=18,spaceAfter=8)
S_fmp_b=mkstyle('fb',fontSize=9.5,textColor=OFF_WHITE,leading=17,spaceAfter=10,alignment=TA_JUSTIFY)
S_fmp_tl=mkstyle('ftl',fontName='Helvetica-Bold',fontSize=9,textColor=GOLD,leading=13,spaceAfter=2)
S_fmp_bd=mkstyle('fbd',fontSize=8.5,textColor=OFF_WHITE,leading=13)
S_cta_h=mkstyle('cth',fontName='Helvetica-Bold',fontSize=14,textColor=PLATINUM,leading=20,alignment=TA_CENTER,spaceAfter=8)
S_cta_b=mkstyle('ctb',fontName='Helvetica-Oblique',fontSize=9.5,textColor=WARM_GREY,leading=16,alignment=TA_CENTER,spaceAfter=10)
S_cta_g=mkstyle('ctg',fontName='Helvetica-Bold',fontSize=10,textColor=GOLD,leading=15,alignment=TA_CENTER,spaceAfter=4)
S_cta_s=mkstyle('cts',fontSize=8.5,textColor=WARM_GREY,leading=13,alignment=TA_CENTER)
S_swim=mkstyle('swim',fontName='Helvetica-Oblique',fontSize=10,textColor=WARM_GREY,leading=16,alignment=TA_CENTER,spaceBefore=6,spaceAfter=0)
S_decl_swim=mkstyle('dswim',fontName='Helvetica-BoldOblique',fontSize=13,textColor=OFF_WHITE,leading=18,alignment=TA_CENTER,spaceBefore=0,spaceAfter=0)
S_decl=mkstyle('decl',fontSize=9.5,textColor=OFF_WHITE,leading=17,spaceAfter=10,alignment=TA_JUSTIFY)
S_decl_close=mkstyle('decl_close',fontName='Helvetica-BoldOblique',fontSize=10,textColor=PLATINUM,leading=16,spaceAfter=0,alignment=TA_JUSTIFY)
S_hl=mkstyle('hl',fontName='Helvetica-Bold',fontSize=16,textColor=PLATINUM,leading=22,spaceAfter=6,alignment=TA_JUSTIFY)


class HRule(Flowable):
    def __init__(self,w,c=RULE_MIN,t=0.5,sa=4,sb=4):
        Flowable.__init__(self); self.rw=w; self.c=c; self.t=t; self._sa=sa; self._sb=sb; self.height=sa+t+sb
    def wrap(self,aw,ah): return self.rw,self.height
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        self.canv.line(0,self._sb+self.t/2,self.rw,self._sb+self.t/2)


class NoteBox(Flowable):
    def __init__(self,w,text,style,bg=NOTE_BG,bar=RULE_MAJ,ph=15,pv=13,bw=4):
        Flowable.__init__(self); self._w=w; self.bg=bg; self.bar=bar; self.ph=ph; self.pv=pv; self.bw=bw
        self._p=Paragraph(text,style); self._iw=w-bw-ph*2
    def wrap(self,aw,ah):
        _,h=self._p.wrap(self._iw,ah); self.height=h+self.pv*2; return self._w,self.height
    def draw(self):
        c=self.canv; c.saveState()
        c.setFillColor(self.bg); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0,0,self._w,self.height,3,fill=1,stroke=1)
        c.setFillColor(self.bar); c.roundRect(0,0,self.bw,self.height,2,fill=1,stroke=0)
        self._p.wrap(self._iw,self.height); self._p.drawOn(c,self.bw+self.ph,self.pv)
        c.restoreState()


class CardBox(Flowable):
    def __init__(self,w,children,bg=DARK_WARM,border=GOLD,bw=1.0,gold_top=True,pad=14):
        Flowable.__init__(self); self._w=w; self._ch=children; self.bg=bg
        self.border=border; self.bw=bw; self.gold_top=gold_top; self._pad=pad
    def wrap(self,aw,ah):
        inner=self._w-self._pad*2; h=self._pad
        for c in self._ch:
            _,ch=c.wrap(inner,ah); h+=ch+2
        self.height=h+self._pad; return self._w,self.height
    def draw(self):
        c=self.canv; c.saveState()
        c.setFillColor(self.bg); c.setStrokeColor(self.border); c.setLineWidth(self.bw)
        c.roundRect(0,0,self._w,self.height,4,fill=1,stroke=1)
        if self.gold_top:
            c.setFillColor(GOLD); c.setLineWidth(3)
            c.line(0,self.height-1.5,self._w,self.height-1.5)
        x=self._pad; y=self.height-self._pad; inner=self._w-self._pad*2
        for ch in self._ch:
            _,h=ch.wrap(inner,self.height); y-=h; ch.drawOn(c,x,y); y-=2
        c.restoreState()


def draw_cover(canvas,doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    from reportlab.lib.utils import ImageReader
    try:
        img=ImageReader(LOGO); iw,ih=img.getSize()
        lw=min(W*0.62,320); lh=lw*ih/iw; lx=(W-lw)/2; ly=H*0.52
        canvas.drawImage(LOGO,lx,ly-lh,lw,lh,mask='auto',preserveAspectRatio=True)
        ry=ly-lh-14
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8); canvas.line(ML,ry,W-MR,ry)
        canvas.setFont('Helvetica',7); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2,ry-14,'THE CASE FOR VEKTOR')
        canvas.setFont('Helvetica-Bold',22); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2,ry-42,'Why Vektor?')
        canvas.setFont('Helvetica-Oblique',10); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2,ry-62,'The commercial argument for institutional-grade quantitative infrastructure,')
        canvas.drawCentredString(W/2,ry-76,'without the institutional overhead.')
    except Exception as e: print(e)
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4); canvas.line(ML,36*mm,W-MR,36*mm)
    canvas.setFont('Helvetica',7.5); canvas.setFillColor(WARM_GREY)
    canvas.drawCentredString(W/2,28*mm,'For professional and institutional investors only')
    canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W/2,16*mm,DATE)
    # IP horizontal mark — bottom-left, maker's attribution
    try:
        ip_w=38*mm; ip_h=ip_w/IP_H_RATIO
        canvas.drawImage(IP_H,ML,9*mm,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.restoreState()


def _hdr(canvas,doc):
    from reportlab.lib.utils import ImageReader
    hy=H-MT2+14
    try:
        img=ImageReader(LOGO); iw,ih=img.getSize(); lh=22; lw=lh*iw/ih
        canvas.drawImage(LOGO,ML,hy,lw,lh,mask='auto',preserveAspectRatio=True)
    except: pass
    canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawRightString(W-MR,H-MT2+18,f'{SUB}  \u00b7  {doc.page-1:02d}')
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.4); canvas.line(ML,H-MT2+8,W-MR,H-MT2+8)


def _ftr(canvas):
    from reportlab.lib.utils import ImageReader
    ip_w=32*mm; ip_h=ip_w/IP_H_RATIO; ip_x=ML; ip_y=1.0*mm
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.3)
    canvas.line(ML,MB-2,W-MR,MB-2)
    try:
        canvas.drawImage(IP_H,ip_x,ip_y,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawRightString(W-MR,ip_y+ip_h/2-2.5,f'investpuppy.com  \u00b7  {DATE}')


def draw_first(canvas,doc):
    canvas.saveState(); canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0); _ftr(canvas); canvas.restoreState()


def draw_later(canvas,doc):
    canvas.saveState(); canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0); _hdr(canvas,doc); _ftr(canvas); canvas.restoreState()


def p(text,style): return Paragraph(text,style)
def sp(n=8): return Spacer(1,n)
def hrm(): return HRule(COL_W,RULE_MAJ,1.0,3,6)
def hrn(): return HRule(COL_W,RULE_MIN,0.3,3,3)


def build():
    out='/home/claude/investpuppy/vektor/output/pdf/vk5-why-vektor.pdf'
    f_cov=Frame(0,0,W,H,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='cover')
    f_fst=Frame(ML,MB,COL_W,H-MT1-MB,id='first')
    f_lat=Frame(ML,MB,COL_W,H-MT2-MB,id='later')
    doc=BaseDocTemplate(out,pagesize=A4,leftMargin=ML,rightMargin=MR,topMargin=MT1,bottomMargin=MB)
    doc.addPageTemplates([
        PageTemplate(id='Cover',frames=[f_cov],onPage=draw_cover),
        PageTemplate(id='First',frames=[f_fst],onPage=draw_first),
        PageTemplate(id='Later',frames=[f_lat],onPage=draw_later),
    ])
    story=[]
    story.append(Spacer(1,1))
    story.append(NextPageTemplate('First'))
    story.append(PageBreak())

    story.append(p('THE INVESTPUPPY QUESTION',S_tag))
    story.append(hrm())
    # Origin sentence before the main declaration
    story.append(p(
        'The name is a signal. Not just about personality \u2014 about origin.',
        mkstyle('ip_origin_tag', fontName='Helvetica-Oblique', fontSize=9,
          textColor=WARM_GREY, leading=13, spaceAfter=6)))
    story.append(p(
        'InvestPuppy was built by practitioners who spent decades inside the traditional system \u2014 '
        'who saw, from the inside, how institutional messaging was being used to substitute '
        'for the substance of the work. The name is a deliberate rejection of that.',
        mkstyle('ip_origin_b', fontSize=9.5, textColor=OFF_WHITE, leading=15, spaceAfter=10)))
    decl_children=[
        p('InvestPuppy is a deliberate signal: that we are more interested '
          'in the quality of our work than the hyperbole of our messaging. '
          'The name is a filter. '
          'If it makes you curious, you are probably our kind of client. If it makes you uncomfortable, '
          'the platforms that look more like institutions probably suit you better.',S_decl),
        p('We are serious about portfolios. We are not serious about ourselves. '
          'That is the distinction we are built on.',S_decl_close),
    ]
    story.append(CardBox(COL_W,decl_children,bg=NOTE_BG,border=RULE_MAJ,bw=0.6,gold_top=False,pad=16))
    story.append(sp(14))
    story.append(HRule(COL_W,RULE_MAJ,0.5,4,4))
    story.append(sp(8))
    story.append(p('Serious when it matters.',S_decl_swim))
    story.append(sp(14))
    story.append(p('THE CASE FOR VEKTOR',S_tag)); story.append(hrm())
    story.append(p('Giving wealth teams the quantitative infrastructure that institutional asset managers take for granted.',S_hl))
    story.append(p(
        'The tools that generate genuine alpha \u2014 quantitative portfolio construction, systematic signal '
        'selection, rigorous backtesting \u2014 have historically required institutional infrastructure, '
        'institutional headcount, and institutional budgets. Vektor resolves that tension completely. '
        'Without the cost, the complexity, or the minimum AUM that have always made it inaccessible.',S_body))

    story.append(NextPageTemplate('Later')); story.append(PageBreak())
    story.append(Spacer(1,0))
    story.append(p('01 \u00b7 THE PROBLEM WITH THE ALTERNATIVES',S_tag)); story.append(hrm())
    story.append(p('The status quo is broken in three distinct ways.',S_sub))
    for title,body in [
        ('Spreadsheet-based allocation',
         'Most wealth teams still build portfolios in Excel. Weights are set by intuition, signals are applied '
         'inconsistently, and diversification is assumed rather than verified. The result is portfolios that feel '
         'constructed but are not \u2014 they carry hidden correlations, unquantified risk, and no systematic edge.'),
        ('Institutional quant platforms',
         'Bloomberg PORT, FactSet, and their peers offer genuine quantitative rigour \u2014 but at a price point, '
         'complexity level, and minimum AUM threshold that places them firmly out of reach for independent wealth '
         'teams, boutique family offices, and emerging market managers. Bloomberg PORT adds S$8,000\u2013S$25,000 '
         'per seat per year on top of a terminal subscription already costing S$43,000+ per seat. '
         'For equity-focused boutique managers, Vektor directly replaces the PORT subscription \u2014 '
         'the Terminal stays, the PORT cancellation funds Vektor, and systematic construction capability improves.'),
        ('Robo-advisory and algorithmic retail tools',
         'The consumer fintech wave produced automated portfolio tools built for retail investors \u2014 standardised '
         'risk profiles, limited instrument universes, no transparency into the underlying methodology, and no '
         'capacity for bespoke, multi-currency, multi-mandate complexity.'),
    ]:
        story.append(p(title,S_subh)); story.append(p(body,S_body))

    story.append(hrm()); story.append(p('02 \u00b7 WHAT VEKTOR DOES DIFFERENTLY',S_tag)); story.append(sp(4))
    story.append(p('Institutional rigour. Without the institutional overhead.',
        mkstyle('hl2',fontName='Helvetica-Bold',fontSize=13,textColor=PLATINUM,leading=18,spaceAfter=6)))
    story.append(p(
        'Vektor is built on a single premise: that the quantitative methods used by the world\u2019s '
        'best-capitalised investment teams are not inherently complex to deploy \u2014 they have simply '
        'never been packaged for the teams who need them most.',S_body))

    # METRICS PANEL — CORRECTED
    mw=COL_W/4
    metrics=[
        ('10,000','portfolio configurations\nper strategy',
         'Efficient frontier mapped\nacross 10,000 portfolio\nconfigurations.\nMPT selects max-Sharpe.'),
        ('99.94%','capital\nallocation\nefficiency',
         'Of target allocation actually\ndeployed. The gap between\nweight and position is drag.\nVektor eliminates it.'),
        ('6','signals per\ninstrument',
         'Technical indicators\nevaluated per instrument\nacross three years of price\nhistory.'),
        ('3 yrs','daily data,\nrefreshed\ndaily',
         'Of price data updated every\nday. Signal selection reflects\ncurrent market behaviour.'),
    ]
    mt=Table([[p(m[0],S_mn) for m in metrics],[p(m[1],S_ml) for m in metrics],[p(m[2],S_mc) for m in metrics]],colWidths=[mw]*4)
    mt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),CARD_BG),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,0),8),('BOTTOMPADDING',(0,0),(-1,0),2),
        ('TOPPADDING',(0,1),(-1,1),2),('BOTTOMPADDING',(0,1),(-1,1),2),
        ('TOPPADDING',(0,2),(-1,2),4),('BOTTOMPADDING',(0,2),(-1,2),8),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('LINEAFTER',(0,0),(2,-1),0.3,RULE_MIN),('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
    ]))
    story.append(mt); story.append(sp(8))
    story.append(p('These are not aspirational metrics. They describe what Vektor produces on every strategy, for every client, across every configured mandate and market \u2014 concurrently.',S_body))

    story.append(PageBreak()); story.append(Spacer(1,0))
    story.append(p('THE FIVE REASONS',S_tag)); story.append(hrm())
    story.append(p('Five reasons sophisticated teams choose Vektor.',S_sub))
    for num,title,body in [
        ('01','Every holding gets its own optimised signal.',
         'Vektor runs a full grid search across six indicators \u2014 SMA, EMA, MACD, Bollinger Bands, RSI, and Stochastic Oscillator \u2014 against three years of each instrument\u2019s price history, selects the highest Sharpe configuration, and validates every live signal through an XGBoost classification layer. Each position is driven by the signal that actually worked for that specific instrument \u2014 not the signal that worked on average.'),
        ('02','Diversification is verified, not assumed.',
         '10,000 portfolio configurations map the efficient frontier; Modern Portfolio Theory selects the max-Sharpe allocation \u2014 weights determined by evidence, not intuition. A full correlation matrix confirms genuine diversification before every strategy is locked.'),
        ('03','Full transparency before a single order is placed.',
         'Every strategy review surfaces the complete picture before approval: instruments, weights, the specific indicator assigned to each holding, and the backtest Sharpe ratio. The compliance-ready audit trail captures every action across all three user roles \u2014 accountability built into the architecture, not bolted on afterwards.'),
        ('04','Capital is deployed with precision, not approximation.',
         'Vektor translates percentage weights into actual share quantities at live market prices, rounded to exchange-specific lot sizes, with a configurable cash buffer \u2014 achieving 99.94% capital allocation efficiency.'),
        ('05','Any market. Any currency. Any number of mandates.',
         'Configure the exchange, benchmark, base currency, and lot sizes \u2014 the engine runs identically across Singapore equities, London-listed industrials, or any listed equity market globally. Different clients run on different mandates concurrently: separate universes, separate benchmarks, separate currencies, independent of each other. FX rates update daily. New mandates onboard in minutes.'),
    ]:
        story.append(p(num,S_rnum)); story.append(p(title,S_rtit)); story.append(p(body,S_body)); story.append(hrn())

    story.append(PageBreak()); story.append(Spacer(1,0))
    story.append(CardBox(COL_W,[
        p('Show us a mandate. We’ll show you the platform.',
          mkstyle('poc_pull',fontName='Helvetica-Bold',fontSize=11,
             textColor=PLATINUM,leading=16,alignment=TA_CENTER,spaceAfter=4)),
        p('Pick any listed equity market, any currency, any benchmark. '
          'We will run the full Vektor workflow on your data and show you the output. '
          'No slides. No promises.',
          mkstyle('poc_sub',fontSize=9,textColor=WARM_GREY,leading=14,
             alignment=TA_CENTER,spaceAfter=0)),
    ],bg=colors.HexColor('#0D0C0A'),border=GOLD,bw=0.6))
    story.append(sp(10))
    story.append(p('THE HONEST ANSWER',S_tag)); story.append(hrm())
    story.append(p('What Vektor is not.',S_sec))
    story.append(p('Sophistication without candour is not a sales argument \u2014 it is a liability.',S_sub))
    for title,body in [
        ('Not yet a fully automated trading system.',
         'Direct trade execution, real-time position updates, live P&L dashboards, and automated rebalancing are on the near-term roadmap. Live today: complete portfolio construction, strategy review, client onboarding, asset allocation, and cash funding \u2014 everything to a trade-ready position set.'),
        ('Not a black box.',
         'Every signal, weight, backtest result, and action is visible, logged, and reviewable. If a portfolio manager cannot explain why a position was included, the system has failed \u2014 and Vektor is built so that failure cannot happen silently.'),
        ('Not for every mandate.',
         'Built for listed equity markets. Fixed income, alternatives, and derivatives are outside the current scope. Vektor does one thing \u2014 systematic listed equity portfolio management \u2014 and does it with rigour the generalist platforms cannot match.'),
        ('Data handling and security.',
         'Vektor is built with institutional data handling standards. Full details of the platform\u2019s security architecture, data residency, and access controls are available on request.'),
        ('Regulatory standing.',
         'Vektor is a portfolio construction and management platform. Regulatory status, jurisdiction, and applicable permissions are not disclosed in this document \u2014 full details are available to prospective partners on request as part of the Founding Mandate due diligence process.'),
    ]:
        story.append(p(title,S_subh)); story.append(p(body,S_body))
    story.append(sp(12)); story.append(p('THE ANSWER IN ONE SENTENCE',S_tag)); story.append(hrm()); story.append(sp(6))
    story.append(HRule(COL_W,RULE_MAJ,1.0,2,6))
    story.append(p('\u201cVektor gives wealth teams the quantitative infrastructure that institutional asset managers take for granted \u2014 without the cost, complexity, or minimum AUM that have always made it inaccessible.\u201d',S_pull))
    story.append(HRule(COL_W,RULE_MAJ,1.0,6,2))

    story.append(PageBreak()); story.append(Spacer(1,0))
    story.append(p('FOUNDING MANDATE PROGRAMME',S_tag)); story.append(hrm()); story.append(sp(4))

    fmp_ch=[
        p('Founding Mandate Programme',S_fmp_tt),
        p('Vektor is currently onboarding a small number of Founding Mandate partners \u2014 wealth teams managing listed equity mandates who will help shape Vektor\u2019s development in exchange for preferential commercial terms, direct access to the founding team, and formal input into the product roadmap. Three slots. Availability will close once the cohort is complete.',S_fmp_b),
        HRule(COL_W-30,RULE_MIN,0.3,2,4),
    ]
    terms=[('Slots available','Three founding partners \u2014 specific, scarce, selected. Once full, the programme closes.'),
           ('Roadmap influence','Formal input into product direction \u2014 quarterly structured reviews with the founding team.'),
           ('Commercial terms','12-month founding rate of S$18,000/year, then permanently one tier below your AUM tier.'),
           ('Recognition','Referenced as a Founding Partner in future materials, with consent.'),
           ('Access','Direct line to the founding team throughout onboarding and beyond.'),
           ('Close date','Applications close once the cohort is complete.')]
    left,right=terms[:3],terms[3:]
    trows=[]
    for i in range(3):
        trows.append([p(left[i][0],S_fmp_tl),p(right[i][0],S_fmp_tl)])
        trows.append([p(left[i][1],S_fmp_bd),p(right[i][1],S_fmp_bd)])
        trows.append([Spacer(1,6),Spacer(1,6)])
    tt=Table(trows,colWidths=[(COL_W-32)/2]*2)
    tt.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MIN),('LEFTPADDING',(1,0),(1,-1),8)]))
    fmp_ch.append(tt)
    story.append(CardBox(COL_W,fmp_ch)); story.append(sp(14))

    story.append(p('WHAT HAPPENS NEXT',S_tag)); story.append(hrm()); story.append(sp(4))
    try:
        from reportlab.platypus import Image as RLImage
        from reportlab.lib.utils import ImageReader
        img=ImageReader(LOGO); iw,ih=img.getSize(); lw=min(180,COL_W*0.48); lh=lw*ih/iw
        logo_img=RLImage(LOGO,width=lw,height=lh); logo_img.hAlign='CENTER'
        cta_children=[
            p("Show us a mandate. We'll show you the platform.",S_cta_h),
            p('Any listed equity market. Any currency. Any benchmark.',S_cta_b),
            p('We will run the full Vektor workflow on your data and show you the output. '
              'The efficient frontier. The correlation matrix. The max-Sharpe allocation. '
              'Per-instrument signals. No slides. No promises.',S_cta_b),
            Spacer(1,6),logo_img,Spacer(1,8),
            p('Enquire about Founding Mandate availability at investpuppy.com',S_cta_g),
            p('investpuppy.com  \u00b7  For professional and institutional enquiries',S_cta_s),
        ]
    except:
        cta_children=[
            p("Show us a mandate. We'll show you the platform.",S_cta_h),
            p('Pick any listed equity market, any currency, any benchmark.',S_cta_b),
            p('Enquire about Founding Mandate availability at investpuppy.com',S_cta_g),
            p('investpuppy.com  \u00b7  For professional and institutional enquiries',S_cta_s),
        ]
    story.append(CardBox(COL_W,cta_children,bg=colors.HexColor('#0D0C0A'),border=RULE_MAJ,bw=0.6,gold_top=False))

    story.append(PageBreak()); story.append(Spacer(1,0))
    story.append(HRule(COL_W,GOLD,0.8,4,8)); story.append(sp(6))
    story.append(p(
        'For the technical methodology underpinning this platform, see the companion white paper: '
        'Quantitative Portfolio Construction for Single-Country Equity Markets. '
        'For the complete Founding Mandate Programme specification \u2014 commercial structure, partner '
        'obligations, programme mechanics, and path to production \u2014 see the Founding Mandate Programme '
        'document (IP-FMP-260501-1.0). All documents available at investpuppy.com.',S_xref))
    story.append(sp(8))
    story.append(p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  Copyright 2026 InvestPuppy',S_ref))

    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    r=subprocess.run(['pdfinfo',out],capture_output=True,text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l or 'File' in l: print(l)

if __name__=='__main__': build()
