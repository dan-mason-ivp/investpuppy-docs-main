"""
Vektor At a Glance — vk3 rebuild.
vk2 baseline + InvestPuppy brand integration:
  - IP horizontal mark (dark variant) bottom-right of page 1 above footer rule
  - IP vertical mark (dark variant) centred on back page as brand moment
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
CARD_EDGE = colors.HexColor('#242428')
DARK_WARM = colors.HexColor('#0D0C0A')

W, H = A4
ML = MR = 16*mm
MB = 14*mm; MT = 12*mm
COL_W = W - ML - MR
LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png')
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')   # dark-bg horizontal mark
IP_V     = '/home/claude/vk2-work/IPVerticalClear.png'     # dark-bg vertical mark
IP_H_RATIO = 2.337   # width/height
IP_V_RATIO = 1.427   # width/height
DATE = 'May 2026'
FOOTER = f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  {DATE}'

def S():
    s = {}
    s['tag'] = ParagraphStyle('tag', fontName='Helvetica', fontSize=7,
        textColor=WARM_GREY, leading=10, letterSpacing=3, alignment=TA_CENTER)
    s['headline'] = ParagraphStyle('headline', fontName='Helvetica-Bold', fontSize=16,
        textColor=PLATINUM, leading=22, alignment=TA_CENTER, spaceAfter=3)
    s['subline'] = ParagraphStyle('subline', fontName='Helvetica', fontSize=10,
        textColor=WARM_GREY, leading=15, alignment=TA_CENTER, spaceAfter=8)
    s['col_hdr'] = ParagraphStyle('col_hdr', fontName='Helvetica-Bold', fontSize=7.5,
        textColor=GOLD, leading=10, letterSpacing=1)
    s['col_body'] = ParagraphStyle('col_body', fontName='Helvetica', fontSize=8.5,
        textColor=OFF_WHITE, leading=13, alignment=TA_JUSTIFY)
    s['metric_num'] = ParagraphStyle('metric_num', fontName='Helvetica-Bold', fontSize=20,
        textColor=GOLD, leading=24, alignment=TA_CENTER)
    s['metric_label'] = ParagraphStyle('metric_label', fontName='Helvetica', fontSize=7.5,
        textColor=WARM_GREY, leading=10, alignment=TA_CENTER)
    s['metric_ctx'] = ParagraphStyle('metric_ctx', fontName='Helvetica', fontSize=7.5,
        textColor=OFF_WHITE, leading=11, alignment=TA_CENTER)
    s['reason_num'] = ParagraphStyle('reason_num', fontName='Helvetica-Bold', fontSize=14,
        textColor=GOLD, leading=18, alignment=TA_CENTER)
    s['reason_title'] = ParagraphStyle('reason_title', fontName='Helvetica-Bold', fontSize=9,
        textColor=PLATINUM, leading=13)
    s['reason_body'] = ParagraphStyle('reason_body', fontName='Helvetica', fontSize=8.5,
        textColor=WARM_GREY, leading=13)
    s['fmp_title'] = ParagraphStyle('fmp_title', fontName='Helvetica-Bold', fontSize=11,
        textColor=GOLD, leading=15)
    s['fmp_body'] = ParagraphStyle('fmp_body', fontName='Helvetica', fontSize=8.5,
        textColor=OFF_WHITE, leading=13, alignment=TA_JUSTIFY)
    s['scope_note'] = ParagraphStyle('scope_note', fontName='Helvetica-Oblique',
        fontSize=8, textColor=colors.HexColor('#9A9086'), leading=12,
        spaceAfter=0)
    s['fmp_cta'] = ParagraphStyle('fmp_cta', fontName='Helvetica-Bold', fontSize=9,
        textColor=GOLD, leading=13, alignment=TA_RIGHT)
    s['footer'] = ParagraphStyle('footer', fontName='Helvetica', fontSize=6.5,
        textColor=colors.HexColor('#444440'), alignment=TA_CENTER, leading=10)
    s['back_text'] = ParagraphStyle('back_text', fontName='Helvetica', fontSize=8,
        textColor=WARM_GREY, alignment=TA_CENTER, leading=13)
    return s


class HRule(Flowable):
    def __init__(self, w, c=RULE_MIN, t=0.4, sa=3, sb=3):
        Flowable.__init__(self)
        self.rw=w; self.c=c; self.t=t; self._sa=sa; self._sb=sb
        self.height=sa+t+sb
    def wrap(self, aw, ah): return self.rw, self.height
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        self.canv.line(0, self._sb+self.t/2, self.rw, self._sb+self.t/2)


def draw_p1(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.3)
    canvas.line(ML,MB-2,W-MR,MB-2)
    canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawCentredString(W/2,MB-10,FOOTER)
    canvas.restoreState()


def draw_p2(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    # IP vertical mark — centred, brand moment
    from reportlab.lib.utils import ImageReader
    try:
        ip_w = 38*mm
        ip_h = ip_w / IP_V_RATIO
        ip_x = (W - ip_w) / 2
        ip_y = H/2 - ip_h/2 + 12*mm   # slightly above true centre
        canvas.drawImage(IP_V, ip_x, ip_y, ip_w, ip_h, mask='auto', preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.3)
    canvas.line(ML,MB-2,W-MR,MB-2)
    canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawCentredString(W/2,MB-10,FOOTER)
    canvas.restoreState()


def para(text, s, st='col_body'): return Paragraph(text, s[st])
def sp(n=4): return Spacer(1,n)


def build():
    out='/home/claude/investpuppy/vektor/output/pdf/vk5-at-a-glance.pdf'
    s=S()
    # Calculate logo height dynamically so frame starts reliably below it
    try:
        from reportlab.lib.utils import ImageReader as IR
        img=IR(LOGO); iw,ih=img.getSize(); lw_pts=min(W*0.35,160); lh_pts=lw_pts*ih/iw
    except: lh_pts=77
    # Frame top must be below logo bottom: logo_bottom = H - MT - lh_pts, add 8pt gap
    logo_bottom = H - MT - lh_pts - 2
    frame_top = logo_bottom - 8
    f1=Frame(ML,MB,COL_W,frame_top-MB,id='p1')
    f2=Frame(ML,MB,COL_W,H-MT-MB,id='p2')
    doc=BaseDocTemplate(out,pagesize=A4,leftMargin=ML,rightMargin=MR,
        topMargin=MT,bottomMargin=MB,title='Vektor at a Glance',author='InvestPuppy')
    doc.addPageTemplates([
        PageTemplate(id='P1',frames=[f1],onPage=_draw_logo_top),
    ])

    story=[]

    # ── LOGO + HEADER drawn in onPage; story starts below ─────────────────────
    # Draw logo in onPage function, story carries below-rule content
    # Actually, draw logo + rule at top of page directly on canvas via onPage
    # The Frame starts below the logo space

    # We'll draw the logo in the first page onPage and offset the frame

    story.append(sp(4))
    story.append(para('VEKTOR AT A GLANCE',s,'tag'))
    story.append(sp(5))
    story.append(HRule(COL_W, RULE_MAJ, 0.8))
    story.append(para(
        'Giving wealth teams the quantitative infrastructure that institutional asset managers take for granted.',
        s,'headline'))
    story.append(para('Without the cost, the complexity, or the minimum AUM.',s,'subline'))
    story.append(sp(4))
    # Honesty signal — scope statement at first contact
    story.append(para(
        'Listed equities. Any exchange. Any currency. Any number of concurrent mandates. '
        'We will tell you what Vektor does not yet do before you ask.',
        s,'scope_note'))

    # Three-column card
    cw3 = COL_W/3
    prob_body = (
        'Institutional-grade quantitative tools \u2014 portfolio optimisation, systematic signals, '
        'rigorous backtesting \u2014 require institutional infrastructure, headcount, and budgets. '
        'Independent wealth teams are left with Excel or retail robo-tools. Neither is adequate.')
    # CORRECTED platform description
    plat_body = (
        'Vektor is an eleven-step systematic portfolio management platform. It screens equity universes, '
        'generates 10,000 portfolio configurations to map the efficient frontier, applies Modern Portfolio '
        'Theory to identify the max-Sharpe allocation, selects per-instrument signals, allocates at live '
        'prices, and produces a fully auditable, trade-ready position set. Any listed equity market. Any currency.')
    result_body = (
        'A quantitatively constructed, genuinely diversified, compliance-ready portfolio \u2014 from '
        'first client meeting to funded positions \u2014 in a fraction of the time. '
        'Any listed equity market. Any currency. Any number of concurrent mandates.')
    three_col=[
        [para('THE PROBLEM',s,'col_hdr'),para('THE PLATFORM',s,'col_hdr'),para('THE RESULT',s,'col_hdr')],
        [para(prob_body,s),para(plat_body,s),para(result_body,s)],
    ]
    tc=Table(three_col,colWidths=[cw3,cw3,cw3])
    tc.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),CARD_BG),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,0),7),('BOTTOMPADDING',(0,0),(-1,0),5),
        ('TOPPADDING',(0,1),(-1,1),7),('BOTTOMPADDING',(0,1),(-1,1),10),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('LINEAFTER',(0,0),(1,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
    ]))
    story.append(tc)
    story.append(sp(8))

    # Four metric cards - CORRECTED: 99.94%, updated Monte Carlo label
    metrics=[
        ('10,000','portfolio configurations\nper strategy',
         'Efficient frontier mapped across\n10,000 portfolio configurations.\nMPT selects max-Sharpe.'),
        # CORRECTED: 99.94%
        ('99.94%','capital\nallocation\nefficiency',
         'Of target allocation deployed.\nThe gap between weight and\nposition is drag. Vektor eliminates it.'),
        ('6','signals per\ninstrument',
         'Per-stock optimised indicators.\nGrid search across 6 indicators\n\u00d7 3 years. Best Sharpe wins.'),
        ('3 yrs','daily data,\nrefreshed\ndaily',
         'Current signals, not stale history.\nOf price data updated every day.\nSignal selection reflects the market.'),
    ]
    mw=COL_W/4
    mrow_top=[[para(m[0],s,'metric_num') for m in metrics]]
    mrow_mid=[[para(m[1],s,'metric_label') for m in metrics]]
    mrow_bot=[[para(m[2],s,'metric_ctx') for m in metrics]]
    mt=Table(mrow_top+mrow_mid+mrow_bot, colWidths=[mw]*4)
    mt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),CARD_BG),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,0),8),('BOTTOMPADDING',(0,0),(-1,0),2),
        ('TOPPADDING',(0,1),(-1,1),2),('BOTTOMPADDING',(0,1),(-1,1),2),
        ('TOPPADDING',(0,2),(-1,2),4),('BOTTOMPADDING',(0,2),(-1,2),8),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('LINEAFTER',(0,0),(2,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
    ]))
    story.append(mt)
    story.append(sp(8))

    # Five reasons table
    reasons=[
        ('01','Every holding gets its own optimised signal.',
         'Grid search across 6 indicators \u00d7 3 years. Best Sharpe wins.'),
        ('02','Diversification is verified, not assumed.',
         'Full correlation matrix before every strategy is locked.'),
        ('03','Full transparency before a single order is placed.',
         'Instruments, weights, indicators, Sharpe \u2014 all visible pre-approval.'),
        # CORRECTED: 99.94%
        ('04','Capital deployed with precision, not approximation.',
         'Live prices. Lot-rounded. 99.94% efficiency. Every time.'),
        ('05','Any market. Any currency. Any number of mandates.',
         'Configure exchange, benchmark, currency. Engine does the rest.'),
    ]
    rrows=[[para(r[0],s,'reason_num'),
            Paragraph(f'<b>{r[1]}</b>',s['reason_title']),
            para(r[2],s,'reason_body')] for r in reasons]
    rt=Table(rrows,colWidths=[14*mm,COL_W*0.52,COL_W-14*mm-COL_W*0.52])
    rt.setStyle(TableStyle([
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[CARD_BG,colors.HexColor('#0F0F14')]),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
        ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MIN),
        ('LINEAFTER',(1,0),(1,-1),0.3,RULE_MIN),
    ]))
    story.append(rt)
    story.append(sp(8))

    # Proof of concept callout
    poc_rows=[[
        para('Show us a mandate. We’ll show you the platform.',
             s,'fmp_cta'),
        para('Pick any listed equity market, any currency, any benchmark. '
             'We will run the full Vektor workflow on your data and show you the output. '
             'No slides. No promises.',
             s,'fmp_body'),
    ]]
    pct=Table(poc_rows,colWidths=[COL_W*0.42,COL_W*0.58])
    pct.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#0D0D10')),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('LINEAFTER',(0,0),(0,-1),0.5,GOLD),
        ('BOX',(0,0),(-1,-1),0.4,RULE_MAJ),
    ]))
    story.append(pct)
    story.append(sp(4))

    # FMP section - two column
    fmp_left_body=(
        'Founding Mandate Programme \u2014 currently onboarding a small number of wealth teams managing '
        'listed equity mandates. Preferential commercial terms locked for the duration of the relationship. Direct access to the founding '
        'team. Availability limited.')
    fmp_right_body='<b>Enquire about Founding Mandate\navailability investpuppy.com</b>'
    fmp_cta2_style = ParagraphStyle('fmp_cta2',fontName='Helvetica-Bold',fontSize=9,
        textColor=GOLD,leading=14,alignment=TA_CENTER)
    fmp_rows=[[
        para(fmp_left_body,s,'fmp_body'),
        Paragraph(fmp_right_body, fmp_cta2_style),
    ]]
    ft=Table(fmp_rows,colWidths=[COL_W*0.62,COL_W*0.38])
    ft.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#0D0C0A')),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.8,GOLD),
    ]))
    story.append(ft)

    doc.build(story)

    print(f'Built: {out}')
    import subprocess
    r=subprocess.run(['pdfinfo',out],capture_output=True,text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l or 'File' in l: print(l)


def _draw_logo_top(canvas, doc):
    """Draw Vektor logo at top; IP horizontal mark anchors the footer."""
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    from reportlab.lib.utils import ImageReader
    # Vektor logo — centred at top
    try:
        img=ImageReader(LOGO); iw,ih=img.getSize()
        lw=min(W*0.35,160); lh=lw*ih/iw
        lx=(W-lw)/2; ly=H-MT-lh+2
        canvas.drawImage(LOGO,lx,ly,lw,lh,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
    # Footer — IP horizontal mark IS the footer, sits below frame boundary
    # Mark: 28mm wide, ~12mm tall. Sits from 1mm to 13mm from page edge.
    # Rule at MB (14mm) naturally separates frame content from footer.
    ip_w = 32*mm
    ip_h = ip_w / IP_H_RATIO          # ~12mm
    ip_x = ML
    ip_y = 1.0*mm
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.3)
    canvas.line(ML, MB-2, W-MR, MB-2)
    try:
        canvas.drawImage(IP_H, ip_x, ip_y, ip_w, ip_h, mask='auto', preserveAspectRatio=True)
    except Exception as e: print(e)
    # Right-aligned url + date — vertically centred on the mark
    canvas.setFont('Helvetica', 6.5)
    canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawRightString(W-MR, ip_y + ip_h/2 - 2.5, f'investpuppy.com  \u00b7  {DATE}')
    canvas.restoreState()


if __name__=='__main__': build()
