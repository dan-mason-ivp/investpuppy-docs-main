"""
Vektor Platform Brochure — vk3 rebuild.
vk2 baseline (simulations fix already applied) + brand integration:
  - Cover: IP horizontal mark 38mm bottom-left
  - Footer: IP horizontal mark 32mm standard across all 14 pages
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
    PageBreak, NextPageTemplate, Image as RLImage,
)
from reportlab.platypus.flowables import Flowable

BG=colors.HexColor('#0A0A0F'); PLATINUM=colors.HexColor('#E8E8EC')
GOLD=colors.HexColor('#C8A96E'); OFF_WHITE=colors.HexColor('#E8E2D9')
WARM_GREY=colors.HexColor('#9A9086'); RULE_MAJ=colors.HexColor('#5A5A60')
RULE_MIN=colors.HexColor('#2A2828'); CARD_BG=colors.HexColor('#111116')
NOTE_BG=colors.HexColor('#16161A'); CARD_EDGE=colors.HexColor('#242428')

W,H=A4; ML=MR=22*mm; MT1=16*mm; MT2=46*mm; MB=20*mm; COL_W=W-ML-MR
LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png'); DATE='May 2026'
SUB='Platform Overview'
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')
IP_H_RATIO=2.337

SC={1:_os.path.join(_SCREENSHOTS, 'sc01_research_env.png'), 2:_os.path.join(_SCREENSHOTS, 'sc02_frontier.png'),
    3:_os.path.join(_SCREENSHOTS, 'sc03_correlation.png'), 4:_os.path.join(_SCREENSHOTS, 'sc04_strategy.png'),
    5:_os.path.join(_SCREENSHOTS, 'sc05_clients.png'), 6:_os.path.join(_SCREENSHOTS, 'sc06_allocation.png'),
    7:_os.path.join(_SCREENSHOTS, 'sc07_portfolio.png'), 8:_os.path.join(_SCREENSHOTS, 'sc08_cash.png'),
    9:_os.path.join(_SCREENSHOTS, 'sc09_instruments.png'),10:_os.path.join(_SCREENSHOTS, 'sc10_prices.png'),
   11:_os.path.join(_SCREENSHOTS, 'sc11_fx.png'),
   12:_os.path.join(_SCREENSHOTS, 'sc12_target_optimization.png'),
   13:_os.path.join(_SCREENSHOTS, 'sc13_xgboost_setup.png'),
   14:_os.path.join(_SCREENSHOTS, 'sc14_xgboost_test.png'),
   15:_os.path.join(_SCREENSHOTS, 'sc15_order_workflow.png'),
   16:_os.path.join(_SCREENSHOTS, 'sc16_slack_signals.png'),
   17:_os.path.join(_SCREENSHOTS, 'sc17_order_list.png'),
   18:_os.path.join(_SCREENSHOTS, 'sc18_order_detail.png')}

def mk(name,**kw):
    d=dict(fontName='Helvetica',fontSize=9.5,textColor=OFF_WHITE,leading=17,spaceAfter=8)
    d.update(kw); return ParagraphStyle(name,**d)

S_tag=mk('tag',fontSize=7,textColor=WARM_GREY,leading=11,letterSpacing=4,spaceAfter=4)
S_sec=mk('sec',fontName='Helvetica-Bold',fontSize=14,textColor=PLATINUM,leading=20,spaceAfter=5)
S_sub=mk('sub',fontName='Helvetica-Oblique',fontSize=10,textColor=WARM_GREY,leading=16,spaceAfter=8)
S_body=mk('body',alignment=TA_JUSTIFY)
S_grey=mk('grey',textColor=WARM_GREY,alignment=TA_JUSTIFY)
S_role=mk('role',fontName='Helvetica-Bold',fontSize=9.5,textColor=GOLD,leading=14,spaceAfter=2)
S_note=mk('note',fontName='Helvetica-Oblique',textColor=WARM_GREY,alignment=TA_JUSTIFY)
S_mn=mk('mn',fontName='Helvetica-Bold',fontSize=18,textColor=GOLD,leading=22,alignment=TA_CENTER)
S_ml=mk('ml',fontSize=7.5,textColor=WARM_GREY,leading=10,alignment=TA_CENTER,spaceAfter=0)
S_mc=mk('mc',fontSize=7.5,textColor=OFF_WHITE,leading=11,alignment=TA_CENTER)
S_cap=mk('cap',fontName='Helvetica-Oblique',fontSize=8,textColor=WARM_GREY,leading=12,alignment=TA_CENTER)
S_pi=mk('pi',fontSize=7,textColor=WARM_GREY,leading=10,letterSpacing=2)
S_step=mk('step',fontName='Helvetica-Bold',fontSize=11,textColor=GOLD,leading=15,spaceAfter=3)
S_hdr=mk('hdr',fontName='Helvetica-Bold',fontSize=14,textColor=PLATINUM,leading=20,spaceAfter=5)
S_sub2=mk('sub2',fontName='Helvetica-Oblique',textColor=WARM_GREY,alignment=TA_JUSTIFY)
S_bl=mk('bl',fontSize=9.5,textColor=OFF_WHITE,leading=16,spaceAfter=3)
S_ref=mk('ref',fontSize=7.5,textColor=colors.HexColor('#555550'),leading=11,alignment=TA_CENTER)
S_status_hdr=mk('stH',fontName='Helvetica-Bold',fontSize=8,textColor=PLATINUM,leading=11)
S_status_body=mk('stB',fontSize=8,textColor=OFF_WHITE,leading=12,alignment=TA_JUSTIFY)
S_live=mk('liv',fontName='Helvetica-Bold',fontSize=8,textColor=GOLD,leading=11)
S_next=mk('nxt',fontSize=8,textColor=WARM_GREY,leading=12)
S_scale=mk('scl',fontSize=8,textColor=OFF_WHITE,leading=12)
S_xref=mk('xref',fontSize=8.5,textColor=WARM_GREY,leading=14,alignment=TA_CENTER)


class HRule(Flowable):
    def __init__(self,w,c=RULE_MIN,t=0.5,sa=4,sb=4):
        Flowable.__init__(self); self.rw=w; self.c=c; self.t=t; self._sa=sa; self._sb=sb; self.height=sa+t+sb
    def wrap(self,aw,ah): return self.rw,self.height
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        self.canv.line(0,self._sb+self.t/2,self.rw,self._sb+self.t/2)


class NoteBox(Flowable):
    def __init__(self,w,text,style,bg=NOTE_BG,bar=RULE_MAJ,ph=14,pv=12,bw=4):
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


class ScreenshotCard(Flowable):
    def __init__(self,w,img_path,caption,label='PLATFORM INTERFACE'):
        Flowable.__init__(self); self._w=w; self._img=img_path; self._cap=caption; self._lbl=label
        self._pad=10; self._lbl_h=16
    def wrap(self,aw,ah):
        from reportlab.lib.utils import ImageReader
        img=ImageReader(self._img); iw,ih=img.getSize()
        inner_w=self._w-self._pad*2
        scale=min(inner_w/iw,(ah*0.6)/ih)
        self._ih=ih*scale; self._iw=iw*scale
        cap_p=Paragraph(self._cap,S_cap)
        _,ch=cap_p.wrap(inner_w,ah); self._cap_h=ch; self._cap_p=cap_p
        self.height=self._pad+self._lbl_h+self._ih+6+ch+self._pad
        return self._w,self.height
    def draw(self):
        c=self.canv; c.saveState()
        c.setFillColor(CARD_BG); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0,0,self._w,self.height,3,fill=1,stroke=1)
        c.setFont('Helvetica',7); c.setFillColor(WARM_GREY)
        c.drawString(self._pad,self.height-self._pad-8,self._lbl)
        img_x=self._pad+(self._w-self._pad*2-self._iw)/2
        img_y=self.height-self._pad-self._lbl_h-self._ih
        c.drawImage(self._img,img_x,img_y,self._iw,self._ih,preserveAspectRatio=True)
        self._cap_p.wrap(self._w-self._pad*2,100)
        self._cap_p.drawOn(c,self._pad,self._pad)
        c.restoreState()


def draw_cover(canvas,doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    from reportlab.lib.utils import ImageReader
    try:
        img=ImageReader(LOGO); iw,ih=img.getSize()
        lw=min(W*0.80,380); lh=lw*ih/iw; lx=(W-lw)/2; ly=H*0.55
        canvas.drawImage(LOGO,lx,ly-lh,lw,lh,mask='auto',preserveAspectRatio=True)
        ry=ly-lh-8
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8); canvas.line(0,ry,W,ry)
        canvas.setFont('Helvetica-Bold',7); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2,ry-14,'PLATFORM OVERVIEW  \u00b7  2026')
        canvas.setFont('Helvetica-Bold',28); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2,ry-52,'One Platform.')
        canvas.drawCentredString(W/2,ry-84,'Any Market.')
        canvas.drawCentredString(W/2,ry-116,'Every Step.')
        canvas.setFont('Helvetica',10); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2,ry-140,
            'The complete eleven-step workflow \u2014 from stock screening to funded, trade-ready positions.')
        canvas.drawCentredString(W/2,ry-154,'Systematic, auditable, data-driven.')
    except Exception as e: print(e)
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4); canvas.line(ML,36*mm,W-MR,36*mm)
    canvas.setFont('Helvetica',7.5); canvas.setFillColor(WARM_GREY)
    canvas.drawCentredString(W/2,28*mm,'For professional and institutional investors only')
    canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W/2,16*mm,DATE)
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
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.3); canvas.line(ML,MB-2,W-MR,MB-2)
    try:
        ip_w=32*mm; ip_h=ip_w/IP_H_RATIO
        canvas.drawImage(IP_H,ML,1.0*mm,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawRightString(W-MR,1.0*mm+(32*mm/IP_H_RATIO)/2-2.5,f'investpuppy.com  \u00b7  {DATE}')


def draw_first(canvas,doc):
    canvas.saveState(); canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0); _ftr(canvas); canvas.restoreState()


def draw_later(canvas,doc):
    canvas.saveState(); canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0); _hdr(canvas,doc); _ftr(canvas); canvas.restoreState()


def p(text,style): return Paragraph(text,style)
def sp(n=8): return Spacer(1,n)
def hrm(): return HRule(COL_W,RULE_MAJ,1.0,3,5)
def hrn(): return HRule(COL_W,RULE_MIN,0.3,3,3)
def sc(n,cap,lbl='PLATFORM INTERFACE'): return ScreenshotCard(COL_W,SC[n],cap,lbl)


def build():
    out='/home/claude/investpuppy/vektor/output/pdf/vk5-brochure.pdf'
    f_cov=Frame(0,0,W,H,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='cover')
    f_fst=Frame(ML,MB,COL_W,H-MT1-MB,id='first')
    f_lat=Frame(ML,MB,COL_W,H-MT2-MB,id='later')
    doc=BaseDocTemplate(out,pagesize=A4,leftMargin=ML,rightMargin=MR,topMargin=MT1,bottomMargin=MB,
        title='Vektor Platform Brochure',author='InvestPuppy')
    doc.addPageTemplates([
        PageTemplate(id='Cover',frames=[f_cov],onPage=draw_cover),
        PageTemplate(id='First',frames=[f_fst],onPage=draw_first),
        PageTemplate(id='Later',frames=[f_lat],onPage=draw_later),
    ])
    story=[]
    story.append(Spacer(1,1)); story.append(NextPageTemplate('First')); story.append(PageBreak())

    # ── THE PLATFORM ──────────────────────────────────────────────────────────
    story.append(p('THE PLATFORM',S_tag)); story.append(hrm())
    story.append(p('Rigour at every step.',S_sec))
    story.append(p('The eleven steps documented here are not aspirational. They describe what the platform does today \u2014 on your data, at live prices, for any listed equity market you configure.',S_body))
    story.append(p('Vektor coordinates three roles \u2014 Stock Analyst, Portfolio Manager, and Operations \u2014 through a single admin portal. Each has a defined scope. Every action is logged.',S_body))
    story.append(p('Stock Analyst',S_role)); story.append(p('Screens the universe, runs optimisation, selects per-instrument signals.',S_grey))
    story.append(p('Portfolio Manager',S_role)); story.append(p('Reviews strategy, onboards clients, allocates capital.',S_grey))
    story.append(p('Operations',S_role)); story.append(p('Funds accounts, maintains the full audit trail.',S_grey))
    story.append(sp(6))
    story.append(NoteBox(COL_W,
        'Result: a quantitatively constructed, genuinely diversified, compliance-ready portfolio \u2014 from '
        'first client meeting to funded positions \u2014 in a fraction of the time.',S_note))
    story.append(sp(8))

    # CORRECTED metrics panel
    mw=COL_W/4
    metrics=[
        ('10,000','portfolio configurations\nper strategy',
         'Efficient frontier mapped\nacross 10,000 portfolio\nconfigurations.\nMPT selects max-Sharpe.'),
        ('99.94%','capital\nallocation\nefficiency','Of target allocation deployed.'),
        ('6','signals per\ninstrument','Indicators evaluated per\nstock, 3 years of data.'),
        ('3 yrs','daily data,\nrefreshed\ndaily','Current signals, not stale history.'),
    ]
    mt=Table([[p(m[0],S_mn) for m in metrics],[p(m[1],S_ml) for m in metrics],[p(m[2],S_mc) for m in metrics]],colWidths=[mw]*4)
    mt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),CARD_BG),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,0),7),('BOTTOMPADDING',(0,0),(-1,0),2),
        ('TOPPADDING',(0,1),(-1,1),2),('BOTTOMPADDING',(0,1),(-1,1),2),
        ('TOPPADDING',(0,2),(-1,2),4),('BOTTOMPADDING',(0,2),(-1,2),7),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('LINEAFTER',(0,0),(2,-1),0.3,RULE_MIN),('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
    ]))
    story.append(mt); story.append(sp(8))
    story.append(p('The example throughout this document uses a Singapore equity mandate (SGX, SGD). The platform is market-agnostic and is configured and validated on SGX (Singapore), LSE (UK), and US equities. Any listed equity market is a configuration. Run all your mandates \u2014 across any market and currency \u2014 on a single platform. Configure your exchange, benchmark, currency, and lot sizes \u2014 and the engine does the rest.',S_grey))

    story.append(NextPageTemplate('Later')); story.append(PageBreak())
    story.append(Spacer(1,0))

    # ── STEPS 01-03 ───────────────────────────────────────────────────────────
    story.append(p('STEPS 01\u201303  \u00b7  STOCK ANALYST',S_tag)); story.append(hrm())
    story.append(p('Strategy Research & Construction',S_hdr))
    story.append(p('STEP 01',S_step))
    story.append(p('Screen the Universe',S_sec))
    story.append(p(
        "Vektor\u2019s research workbench screens any listed equity universe by sector, daily liquidity, and "
        "dividend continuity \u2014 turning thousands of candidates into a clean, implementation-ready set. "
        "Singapore example: ~700 SGX-listed stocks filtered by sector (financials, real estate, industrials), "
        "average daily volume >100K, and dividend continuity.",S_body))
    story.append(sc(1,'Research environment \u2014 instrument selection notebook. Market parameters configured for SGX: sectors, liquidity filters, benchmark index, and risk-free rate.','RESEARCH ENVIRONMENT'))
    story.append(sp(8))
    story.append(p('STEP 02',S_step))
    story.append(p('Optimise the Portfolio',S_sec))
    # CORRECTED: accurate two-step description
    story.append(p(
        'The system generates 10,000 portfolio configurations to map the efficient frontier, then applies '
        'Modern Portfolio Theory to identify the max-Sharpe allocation \u2014 the combination of stocks and '
        'weights that maximises risk-adjusted return.',S_body))
    story.append(sc(12,'Target optimisation logic \u2014 10,000 simulations find the optimal portfolio subset. '
        'Mathematical formula for weight calculation, tracking error, and information ratio. Industry standard used by major index fund providers.'))

    story.append(PageBreak()); story.append(Spacer(1,0))
    story.append(sc(2,'Efficient frontier \u2014 10,000 portfolio configurations mapped across risk-return space. Red\u00a0=\u00a0high Sharpe, blue\u00a0=\u00a0low Sharpe. Red star\u00a0=\u00a0max-Sharpe selection via Modern Portfolio Theory.'))
    story.append(sp(8))
    story.append(p('STEP 03',S_step))
    story.append(p('Validate Diversification',S_sec))
    story.append(p('A correlation heatmap confirms the portfolio is genuinely diversified \u2014 not just spread across names that move in lockstep. Strategy weights are then locked in.',S_body))

    story.append(PageBreak()); story.append(Spacer(1,0))
    story.append(sc(3,'Correlation heatmap (top) \u2014 diagonal yellows only confirm genuine diversification. Allocation weights pie chart (bottom) \u2014 max-Sharpe portfolio weights by instrument.'))

    story.append(PageBreak()); story.append(Spacer(1,0))

    # ── STEP 04 ───────────────────────────────────────────────────────────────
    story.append(p('STEP 04  \u00b7  AUTOMATED',S_tag)); story.append(hrm())
    story.append(p('Per-Stock Signal Selection',S_hdr))
    story.append(p(
        "One-size-fits-all trading signals leave alpha on the table. Vektor gives every holding its own "
        "optimised edge \u2014 the technical indicator configuration that actually worked for that specific "
        "instrument over three years of price history.",S_body))
    story.append(p('The six indicators evaluated:',S_body))
    for ind in ['SMA \u2014 Simple Moving Average crossover','EMA \u2014 Exponential Moving Average crossover',
                'MACD \u2014 EMA convergence / divergence momentum','BB \u2014 Bollinger Bands volatility breakout',
                'RSI \u2014 Relative Strength Index overbought/oversold','SO \u2014 Stochastic Oscillator closing price vs range']:
        story.append(p(f'\u2014 {ind}',S_bl))
    story.append(sp(6))
    story.append(p('An XGBoost layer validates every live signal before execution. Two layers of rigour, zero guesswork.',S_body))
    story.append(p("Each instrument's winning indicator, its optimised parameters, and its backtest Sharpe ratio are saved to the strategy record and visible to the portfolio manager before sign-off.",S_body))
    story.append(sc(13,'XGBoost ML validation \u2014 11 features trained at SageMaker, same features sent at inference. Signal output: WEAK_BUY, WEAK_SELL, or HOLD with probability score and confidence classification.'))

    story.append(PageBreak()); story.append(Spacer(1,0))

    # ── STEPS 05-06 ───────────────────────────────────────────────────────────
    story.append(p('STEPS 05\u201306  \u00b7  PORTFOLIO MANAGER',S_tag)); story.append(hrm())
    story.append(p('Strategy Review & Client Onboarding',S_hdr))
    story.append(p('Full transparency before a single order is placed. The portfolio manager reviews instruments, weights, indicators, and backtest Sharpe ratios \u2014 before the strategy is approved. No black boxes. No surprises at execution.',S_body))
    story.append(sc(4,'SGP Equity Strategy \u2014 admin portal. Ten instruments with allocation weights, assigned technical indicators (BB, MACD, SMA, EMA, RSI), optimisation status and selection date. All ten validated and ready for client assignment.'))
    story.append(sp(6))
    story.append(p('Client onboarding \u2014 two steps:',S_body))
    story.append(p('\u2014 Create Client \u2014 name, type (individual / institutional), risk profile, base currency.',S_bl))
    story.append(p('\u2014 Create Portfolio \u2014 link client, assign strategy, set investment capital.',S_bl))
    story.append(sp(4))
    story.append(sc(5,'Customer management \u2014 clients listed with type, currency, risk profile, KYC status, and account status. Individual or institutional. Any currency.'))

    story.append(PageBreak()); story.append(Spacer(1,0))

    # ── STEPS 07-08 ───────────────────────────────────────────────────────────
    story.append(p('STEPS 07\u201308  \u00b7  PORTFOLIO MANAGER',S_tag)); story.append(hrm())
    story.append(p('Asset Allocation at Live Prices',S_hdr))
    story.append(p('Weights in a spreadsheet are just numbers. Vektor turns them into actual positions \u2014 at real prices, rounded to the correct lot size for the target exchange.',S_body))
    for item in ['Live market prices fetched at execution time',
                 'Percentage weights converted to share quantities automatically',
                 'SGX board lot sizes applied (multiples of 100 shares \u2014 configurable per market)',
                 'Configurable cash buffer reserved for fees and slippage']:
        story.append(p(f'\u2014 {item}',S_bl))
    story.append(sp(6))
    # CORRECTED: 99.94% in caption
    story.append(sc(6,'Asset allocation \u2014 SGD 500,000 mandate. SGD 474,712 allocated across seven active positions at live prices. Cash reserve: SGD 25,288 (5%). Efficiency: 99.94%.'))
    story.append(sp(6))
    story.append(p('The trade-ready position set:',S_body))
    story.append(p('Every instrument. Every quantity. Every signal. Every price. '
                   'Reviewed and approved. Nothing moves until this is complete. '
                   'The eleven steps end here.',S_sub))

    story.append(PageBreak()); story.append(Spacer(1,0))
    story.append(sc(7,'Portfolio positions \u2014 target quantities and values vs actual holdings. All positions pending execution. Target value SGD 474,712. Indicator assigned to each position visible.'))

    story.append(PageBreak()); story.append(Spacer(1,0))

    # ── STEPS 09-11 ───────────────────────────────────────────────────────────
    story.append(p('STEPS 09\u201311  \u00b7  OPERATIONS & ADMIN',S_tag)); story.append(hrm())
    story.append(p('Cash Funding, Market Data & Audit',S_hdr))
    story.append(p('Clean data in. Clean audit trail out.',S_sub))
    story.append(p("Operations records the client's wire transfer \u2014 currency, amount, reference \u2014 and the cash account is live immediately. Every deposit is logged with a full audit trail, ready for compliance review.",S_body))
    story.append(sc(8,'Cash movements \u2014 SGD 500,000 deposit recorded 30/04/2026. Date, type, amount, and wire reference logged. Immediately available for allocation.'))
    story.append(sp(8))
    story.append(p('Global market data \u2014 always current:',S_body))
    for item in ['Instrument master \u2014 symbol, company, exchange, currency, sector, market cap',
                 '3 years daily OHLCV \u2014 auto-refreshed every morning at 8\u00a0AM SGT',
                 'FX rates updated daily \u2014 any currency pair',
                 'All actions logged \u2014 strategy, allocation, cash movements']:
        story.append(p(f'\u2014 {item}',S_bl))
    story.append(sp(6))
    story.append(sc(9,'Instruments master \u2014 ten SGX-listed securities with symbol, company name, type, exchange, sector, and market cap. Full securities database.'))

    story.append(PageBreak()); story.append(Spacer(1,0))
    story.append(sc(10,'Price history detail \u2014 5CF (OKP Holdings Limited). Daily OHLCV data auto-refreshed at 8\u00a0AM SGT. Three years of history for signal backtests.'))

    story.append(PageBreak()); story.append(Spacer(1,0))
    story.append(p('MULTI-CURRENCY SUPPORT  \u00b7  STEP 11',S_tag))
    story.append(HRule(COL_W,RULE_MIN,0.3,2,6))
    story.append(p('Daily FX rate collection supports multi-currency mandates and cross-border portfolio valuation. Any currency pair, updated every morning.',S_body))
    story.append(sc(11,'SGD/USD exchange rate history \u2014 60 days. Daily open, high, low, close, and change. Auto-collected at 8\u00a0AM SGT from Yahoo Finance. Any FX pair supported.'))
    story.append(sp(10))

    # Platform Status table
    story.append(p('PLATFORM STATUS',S_tag)); story.append(hrm())
    story.append(p("What's Live. What's Next.",S_hdr))
    st_rows=[
        [p('LIVE TODAY',S_status_hdr),p('COMING NEXT',S_status_hdr),p('BUILT TO SCALE',S_scale)],
        [p('Strategy creation & optimisation',S_live),p('Live client execution via IBKR \u2014 real-money order submission',S_next),p('Automated rebalancing',S_scale)],
        [p('XGBoost signal validation',S_live),p('Real-time position updates post-fill',S_next),p('External PMS integration',S_scale)],
        [p('ML model training & deployment',S_live),p('Live P\u0026L & performance dashboards',S_next),p('SAA & model portfolios',S_scale)],
        [p('Three-state signal approval',S_live),p('Walk-forward strategy validation',S_next),p('',S_scale)],
        [p('Client onboarding & portfolio setup',S_live),p('Infrastructure RBAC / maker-checker',S_next),p('',S_scale)],
        [p('Asset allocation at live prices',S_live),p('',S_next),p('',S_scale)],
        [p('IBKR integration \u2014 connectivity validated',S_live),p('',S_next),p('',S_scale)],
        [p('SGX, LSE, and US equities configured and validated \u2014 any listed market is a configuration',S_live),p('',S_next),p('',S_scale)],
        [p('Cash funding & full audit trail',S_live),p('',S_next),p('',S_scale)],
        [p('Order preparation, queuing & Slack notification',S_live),p('',S_next),p('',S_scale)],
    ]
    st=Table(st_rows,colWidths=[COL_W/3]*3)
    st.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD_BG,colors.HexColor('#0F0F14')]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
        ('LINEAFTER',(0,0),(1,-1),0.3,RULE_MIN),
    ]))
    story.append(st)
    story.append(sp(8))
    story.append(sc(16,'InvestPuppy Trading Bot in the #trading-signals Slack channel \u2014 live signal summary: '
        'Approved, ML Blocked, and Low Confidence signals per portfolio, delivered automatically after each execution cycle.'))
    story.append(sp(4))
    story.append(sc(15,'AWS Step Functions order workflow \u2014 the complete automated pipeline from GetActiveStrategies '
        'through MLValidation to GenerateOrders. Observable, retryable, fully audited at every step.'))
    st.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD_BG,colors.HexColor('#0F0F14')]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
        ('LINEAFTER',(0,0),(1,-1),0.3,RULE_MIN),
    ]))
    story.append(st)
    story.append(sp(12)); story.append(HRule(COL_W,GOLD,0.8,4,6)); story.append(sp(6))
    # Proof of concept block — standalone section before xrefs
    story.append(sp(10))
    story.append(HRule(COL_W,GOLD,0.8,0,8))
    story.append(p('SHOW US A MANDATE.', mk('poc_h',fontName='Helvetica-Bold',
        fontSize=13,textColor=PLATINUM,leading=18,alignment=TA_CENTER,spaceAfter=4)))
    story.append(p('WE’LL SHOW YOU THE PLATFORM.', mk('poc_h2',fontName='Helvetica-Bold',
        fontSize=13,textColor=GOLD,leading=18,alignment=TA_CENTER,spaceAfter=8)))
    story.append(p('Pick any listed equity market, any currency, any benchmark. '
        'We will run the full Vektor workflow against it and show you the output: '
        'the efficient frontier, the correlation matrix, the max-Sharpe allocation, '
        'and the per-instrument signal selection. No slides. No promises. '
        'Just the platform, working on your data.',
        mk('poc_b',fontSize=9.5,textColor=OFF_WHITE,leading=16,
           alignment=TA_CENTER,spaceAfter=6)))
    story.append(p('Become a Proof Partner at investpuppy.com/proof-partners',
        mk('poc_cta',fontName='Helvetica-Bold',fontSize=9,textColor=GOLD,
           leading=14,alignment=TA_CENTER,spaceAfter=4)))
    story.append(HRule(COL_W,GOLD,0.8,4,10))
    story.append(sp(6))
    story.append(p('For methodology: Vektor Research Series (WP-01 through WP-10)  \u00b7  For Proof Partners programme details: vk5-proof-partners.pdf (IP-PPR-260515-1.0)  \u00b7  investpuppy.com',S_xref))
    story.append(sp(6))
    story.append(p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  Copyright 2026 InvestPuppy',S_ref))

    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    r=subprocess.run(['pdfinfo',out],capture_output=True,text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l or 'File' in l: print(l)

if __name__=='__main__': build()
