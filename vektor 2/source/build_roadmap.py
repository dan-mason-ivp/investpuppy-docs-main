"""
ip-brand-product-roadmap.pdf  v1.3
InvestPuppy internal brand and product roadmap
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, PageBreak, HRFlowable)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.utils import ImageReader

OUT        = '/home/claude/investpuppy/vektor/output/pdf/ip-brand-product-roadmap.pdf'
VEKTOR_PNG = '/home/claude/investpuppy/_shared/logos/VEKTOR-transparent-v3.png'
IP_LOGO    = '/home/claude/investpuppy/_shared/logos/ip_logo_vertical.png'

GREEN   = colors.HexColor('#85D155')
DARK    = colors.HexColor('#0A0A0A')
DARK2   = colors.HexColor('#111111')
BODY    = colors.HexColor('#1A1A1A')
GREY    = colors.HexColor('#888888')
WHITE   = colors.white
GOLD    = colors.HexColor('#C8A96E')
PLAT    = colors.HexColor('#9EA8B3')
LIGHT   = colors.HexColor('#F4F4F4')
SECT    = colors.HexColor('#F0F7EA')
WARN_BG = colors.HexColor('#FFF3CD')
WARN_FG = colors.HexColor('#856404')
DARKRED = colors.HexColor('#8B0000')
RED     = colors.HexColor('#C84444')

FP = '/usr/share/fonts/truetype/google-fonts/'
for n in ['Poppins-Light','Poppins-Regular','Poppins-Medium','Poppins-Bold',
          'Poppins-Italic','Poppins-BoldItalic','Poppins-LightItalic']:
    pdfmetrics.registerFont(TTFont(n, FP+n+'.ttf'))

try:
    pdfmetrics.registerFont(TTFont('TF',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf'))
    TF = 'TF'
except:
    TF = 'Poppins-Light'

W, H = A4
ML,MR,MT,MB = 52,52,72,54

def _s():
    s = {}
    b = dict(fontName='Poppins-Light',fontSize=10,leading=16,textColor=BODY,spaceAfter=8)
    s['body']   = ParagraphStyle('body',   **b, alignment=TA_JUSTIFY)
    s['bodyl']  = ParagraphStyle('bodyl',  **b, alignment=TA_LEFT)
    s['h2']     = ParagraphStyle('h2',   fontName='Poppins-Bold',fontSize=12,
                  textColor=DARK,leading=18,spaceAfter=4,spaceBefore=14)
    s['h3']     = ParagraphStyle('h3',   fontName='Poppins-Bold',fontSize=10.5,
                  textColor=GREEN,leading=16,spaceAfter=4,spaceBefore=10)
    s['h3g']    = ParagraphStyle('h3g',  fontName='Poppins-Bold',fontSize=10.5,
                  textColor=GOLD,leading=16,spaceAfter=4,spaceBefore=10)
    s['h3p']    = ParagraphStyle('h3p',  fontName='Poppins-Bold',fontSize=10.5,
                  textColor=PLAT,leading=16,spaceAfter=4,spaceBefore=10)
    s['small']  = ParagraphStyle('small',fontName='Poppins-Light',fontSize=8.5,
                  textColor=GREY,leading=13,spaceAfter=4)
    s['bb']     = ParagraphStyle('bb',   fontName='Poppins-Bold',fontSize=10,
                  textColor=DARK,leading=15,spaceAfter=6)
    s['qt']     = ParagraphStyle('qt',   fontName='Poppins-BoldItalic',fontSize=11,
                  textColor=GREEN,leading=18,spaceAfter=8,
                  leftIndent=16,rightIndent=16,alignment=TA_CENTER)
    s['bul']    = ParagraphStyle('bul',  fontName='Poppins-Light',fontSize=10,
                  textColor=BODY,leading=15,spaceAfter=4,leftIndent=14,bulletIndent=0)
    s['note']   = ParagraphStyle('note', fontName='Poppins-Regular',fontSize=9,
                  textColor=BODY,leading=14,spaceAfter=4,
                  leftIndent=10,backColor=SECT,borderPadding=(6,8,6,8))
    s['warn']   = ParagraphStyle('warn', fontName='Poppins-Bold',fontSize=9,
                  textColor=WARN_FG,leading=14,spaceAfter=4,
                  leftIndent=10,backColor=WARN_BG,borderPadding=(6,8,6,8))
    return s

ST = _s()

def B(t): return f'<font name="Poppins-Bold">{t}</font>'
def G(t): return f'<font color="#85D155">{t}</font>'
def Au(t):return f'<font color="#C8A96E">{t}</font>'
def Pl(t):return f'<font color="#9EA8B3">{t}</font>'
def RE(t):return f'<font color="#C84444">{t}</font>'

def hr(color=GREEN,thick=1.5,spb=6,spa=10):
    return HRFlowable(width='100%',thickness=thick,color=color,spaceAfter=spa,spaceBefore=spb)

def bul(t):
    return Paragraph(f'<bullet>&bull;</bullet> {t}',ST['bul'])

def sec_hdr(title,sub=None):
    r = [hr(color=DARK,thick=0.5,spb=14,spa=2), Paragraph(title,ST['h2'])]
    if sub: r.append(Paragraph(sub,ST['small']))
    r.append(hr(color=GREEN,thick=1,spb=0,spa=8))
    return r

def note(t): return Paragraph(t,ST['note'])
def warn(t): return Paragraph(t,ST['warn'])

def kv(rows,cw=None):
    if cw is None: cw=[160,W-ML-MR-160]
    data=[[Paragraph(B(k),ST['bodyl']),Paragraph(v,ST['bodyl'])] for k,v in rows]
    t=Table(data,colWidths=cw)
    t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'Poppins-Light'),('FONTSIZE',(0,0),(-1,-1),10),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,0),(-1,-1),[WHITE,LIGHT]),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
    ]))
    return t

def grid_table(headers,rows,cw):
    data = [[Paragraph(B(h),ST['bodyl']) for h in headers]]
    for row in rows:
        data.append([Paragraph(cell,ST['bodyl']) for cell in row])
    t = Table(data,colWidths=cw)
    t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'Poppins-Light'),('FONTSIZE',(0,0),(-1,-1),9),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),DARK),
        ('TEXTCOLOR',(0,0),(-1,0),WHITE),('FONTNAME',(0,0),(-1,0),'Poppins-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LIGHT]),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
    ]))
    return t

def _hf(c,doc):
    c.saveState()
    pn=c.getPageNumber()
    if pn>1:
        c.setFillColor(DARK); c.rect(0,H-38,W,38,fill=1,stroke=0)
        c.setFont('Poppins-Bold',10); c.setFillColor(WHITE)
        c.drawString(ML,H-22,'Invest')
        iw=c.stringWidth('Invest','Poppins-Bold',10)
        c.setFillColor(GREEN); c.drawString(ML+iw,H-22,'Puppy')
        c.setFont('Poppins-Regular',7.5); c.setFillColor(GREY)
        c.drawString(ML,H-33,'Brand & Product Architecture · Internal Only · May 2026')
        c.setFillColor(WHITE)
        c.drawRightString(W-MR,H-22,'Not for external distribution')
        c.setFillColor(GREY)
        c.drawRightString(W-MR,H-33,f'IP-BRAND-ROADMAP-260518-1.3  ·  p{pn}')
        c.setStrokeColor(GOLD); c.setLineWidth(1.5); c.line(0,H-38,W,H-38)
    c.setStrokeColor(colors.HexColor('#DDDDDD')); c.setLineWidth(0.5)
    c.line(ML,MB+16,W-MR,MB+16)
    c.setFont('Poppins-Light',7.5); c.setFillColor(GREY)
    c.drawString(ML,MB+4,'InvestPuppy Pte Ltd · INTERNAL ONLY · Not for client distribution')
    c.drawRightString(W-MR,MB+4,str(pn))
    c.restoreState()

def _tenzor_mark(c,x,y,sz=22,byline=True):
    tr=sz*0.18; chars=list('TENZOR')
    c.setFont(TF,sz)
    cw=[c.stringWidth(ch,TF,sz) for ch in chars]
    tw=sum(cw)+tr*(len(chars)-1)
    cx=x; zx=zw=None
    for i,(ch,w) in enumerate(zip(chars,cw)):
        if ch=='Z': zx=cx; zw=w
        c.setFillColor(PLAT); c.drawString(cx,y,ch); cx+=w+tr
    if zx:
        c.setStrokeColor(GOLD); c.setLineWidth(max(1.2,sz*0.055))
        c.line(zx-sz*0.04,y+sz*0.52,zx+zw+sz*0.04,y+sz*0.14)
    if byline:
        bs=max(6.5,sz*0.38); by=y-sz*0.52; bt='BY INVESTPUPPY'
        c.setFont('Poppins-Light',bs); bw=c.stringWidth(bt,'Poppins-Light',bs)
        bx=x+(tw-bw)/2; rg=6
        c.setStrokeColor(GREY); c.setLineWidth(0.4)
        c.line(x,by+bs*0.45,bx-rg,by+bs*0.45)
        c.line(bx+bw+rg,by+bs*0.45,x+tw,by+bs*0.45)
        c.setFillColor(GREY); c.drawString(bx,by,bt)
    ls=max(5.5,sz*0.3); lbl='[WORKING]'
    lw=c.stringWidth(lbl,'Poppins-Regular',ls)
    c.setFont('Poppins-Regular',ls); c.setFillColor(colors.HexColor('#666666'))
    c.drawString(x+(tw-lw)/2,y+sz+2,lbl)
    return tw

def _cover(c):
    c.setFillColor(DARK); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(GOLD); c.rect(0,0,5,H,fill=1,stroke=0)
    c.setFillColor(DARKRED); c.rect(5,H-30,W-5,30,fill=1,stroke=0)
    c.setFont('Poppins-Bold',8.5); c.setFillColor(WHITE)
    c.drawCentredString(W/2,H-18,'INTERNAL ONLY — NOT FOR EXTERNAL DISTRIBUTION')

    # InvestPuppy header — actual logo
    ip_logo_h = 88          # display height on cover
    ip_logo_w = ip_logo_h   # logo is ~square
    ip_logo_y = H - 42 - ip_logo_h   # 42px below internal banner
    # Centre the logo on the page
    ip_logo_x = (W - ip_logo_w) / 2
    c.drawImage(IP_LOGO, ip_logo_x, ip_logo_y,
                width=ip_logo_w, height=ip_logo_h, mask='auto')
    # Subtle gold rule below logo
    rule_y = ip_logo_y - 14
    c.setStrokeColor(GOLD); c.setLineWidth(1)
    c.line(ML, rule_y, W - MR, rule_y)

    # Title
    ty = rule_y - 28  # title top, below logo rule
    c.setFont('Poppins-Bold',26); c.setFillColor(WHITE)
    c.drawString(ML,ty,'Brand & Product Architecture')
    c.setFont('Poppins-Light',11); c.setFillColor(colors.HexColor('#AAAAAA'))
    c.drawString(ML,ty-24,'InvestPuppy · Vektor · Tenzor')
    c.setFont('Poppins-BoldItalic',10); c.setFillColor(GREEN)
    c.drawString(ML,ty-44,'"Honest by design."')

    # ── Marks panel: Vektor (left) + Tenzor (right) — full width, generous spacing ──
    half   = (W - ML - MR) / 2        # each column width
    vcx    = ML + half / 2             # Vektor column centre x
    tcx    = ML + half + half / 2      # Tenzor column centre x
    mp_top = ty - 92
    mp_h   = 210

    # Panel background
    c.setFillColor(DARK2)
    c.roundRect(ML - 12, mp_top - mp_h, W - ML - MR + 24, mp_h + 10,
                6, fill=1, stroke=0)

    # Panel label — top left, small
    c.setFont('Poppins-Regular', 7)
    c.setFillColor(GREY)
    c.drawString(ML, mp_top - 2, 'PRODUCT IDENTITY SYSTEM')

    # Soft top rule
    c.setStrokeColor(colors.HexColor('#222222'))
    c.setLineWidth(0.4)
    c.line(ML - 12, mp_top - 12, W - MR + 12, mp_top - 12)

    # ── Vektor (left column) ──────────────────────────────────────────────────
    # Status label
    c.setFont('Poppins-Regular', 7)
    c.setFillColor(GREY)
    lbl_v = 'VEKTOR  ·  LOCKED'
    lbl_vw = c.stringWidth(lbl_v, 'Poppins-Regular', 7)
    c.drawString(vcx - lbl_vw / 2, mp_top - 26, lbl_v)

    # Vektor logo — centred in left column
    vi = ImageReader(VEKTOR_PNG)
    viw, vih = vi.getSize()
    v_target_h = 76
    v_target_w = viw * v_target_h / vih
    if v_target_w > half - 30:
        v_target_w = half - 30
        v_target_h = vih * v_target_w / viw
    v_img_x = vcx - v_target_w / 2
    v_img_y = mp_top - 46 - v_target_h   # top of image sits 46px below label row
    c.drawImage(VEKTOR_PNG, v_img_x, v_img_y,
                width=v_target_w, height=v_target_h, mask='auto')

    # Colour chips — Vektor: light grey wordmark + gold arrowhead (no green in Vektor identity)
    chip_y_v = v_img_y - 28
    VEKTOR_MARK_GREY = colors.HexColor('#DEDEDE')
    c.setFillColor(VEKTOR_MARK_GREY)
    c.rect(vcx - 32, chip_y_v, 26, 12, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(vcx + 6,  chip_y_v, 26, 12, fill=1, stroke=0)
    # Thin border on grey chip so it shows on dark background
    c.setStrokeColor(colors.HexColor('#555555')); c.setLineWidth(0.3)
    c.rect(vcx - 32, chip_y_v, 26, 12, fill=0, stroke=1)
    c.setFont('Poppins-Light', 6.5); c.setFillColor(GREY)
    c.drawCentredString(vcx - 19, chip_y_v - 9, 'Wordmark')
    c.drawCentredString(vcx + 19, chip_y_v - 9, '#C8A96E')

    # Soft vertical divider
    c.setStrokeColor(colors.HexColor('#222222'))
    c.setLineWidth(0.4)
    c.line(ML + half, mp_top - 12, ML + half, mp_top - mp_h)

    # ── Tenzor (right column) ─────────────────────────────────────────────────
    # "working concept" — very light, above status label
    c.setFont('Poppins-LightItalic', 6.5)
    c.setFillColor(colors.HexColor('#555555'))
    wc = 'working concept'
    wcw = c.stringWidth(wc, 'Poppins-LightItalic', 6.5)
    c.drawString(tcx - wcw / 2, mp_top - 18, wc)

    # Status label
    c.setFont('Poppins-Regular', 7)
    c.setFillColor(GREY)
    lbl_t = 'TENZOR  ·  IN DEVELOPMENT'
    lbl_tw = c.stringWidth(lbl_t, 'Poppins-Regular', 7)
    c.drawString(tcx - lbl_tw / 2, mp_top - 30, lbl_t)

    # Tenzor wordmark — sized to roughly match Vektor visual weight
    tsz = 24
    c.setFont(TF, tsz)
    tch     = list('TENZOR')
    tcw_l   = [c.stringWidth(ch, TF, tsz) for ch in tch]
    ttr     = tsz * 0.15
    ttw     = sum(tcw_l) + ttr * (len(tch) - 1)
    tx0     = tcx - ttw / 2
    # Vertically: align baseline with approximate Vektor visual centre
    t_base  = v_img_y + v_target_h / 2 - tsz * 0.3
    tcx2    = tx0
    tzx = tzw = None
    for ch, cw in zip(tch, tcw_l):
        if ch == 'Z': tzx = tcx2; tzw = cw
        c.setFillColor(PLAT)
        c.drawString(tcx2, t_base, ch)
        tcx2 += cw + ttr

    # Gold Z crossbar
    if tzx is not None:
        c.setStrokeColor(GOLD)
        c.setLineWidth(max(1.3, tsz * 0.055))
        c.line(tzx - tsz * 0.04, t_base + tsz * 0.52,
               tzx + tzw + tsz * 0.04, t_base + tsz * 0.14)

    # BY INVESTPUPPY — below wordmark with clear gap
    bys   = 8
    by_y  = t_base - tsz * 0.55
    byt   = 'BY INVESTPUPPY'
    c.setFont('Poppins-Light', bys)
    byw   = c.stringWidth(byt, 'Poppins-Light', bys)
    byx   = tcx - byw / 2
    rg    = 10
    c.setStrokeColor(GREY); c.setLineWidth(0.4)
    c.line(tx0,       by_y + bys * 0.45, byx - rg,       by_y + bys * 0.45)
    c.line(byx + byw + rg, by_y + bys * 0.45, tx0 + ttw, by_y + bys * 0.45)
    c.setFillColor(GREY)
    c.drawString(byx, by_y, byt)

    # Colour chips — Tenzor, aligned with Vektor chips
    chip_y_t = chip_y_v
    c.setFillColor(PLAT); c.rect(tcx - 32, chip_y_t, 26, 12, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(tcx + 6,  chip_y_t, 26, 12, fill=1, stroke=0)
    c.setFont('Poppins-Light', 6.5); c.setFillColor(GREY)
    c.drawCentredString(tcx - 19, chip_y_t - 9, '#9EA8B3')
    c.drawCentredString(tcx + 19, chip_y_t - 9, '#C8A96E')

    # Meta + Contents — redesigned to prevent overflow
    meta_y = mp_top - mp_h - 16
    c.setStrokeColor(colors.HexColor('#333333')); c.setLineWidth(0.5)
    c.line(ML, meta_y + 4, W - MR, meta_y + 4)

    # Helper: draw text constrained to max width, truncating with ellipsis
    def bounded(cx, cy, text, font, size, color, max_w):
        c.setFont(font, size); c.setFillColor(color)
        while text and c.stringWidth(text, font, size) > max_w:
            text = text[:-1]
        if text:
            c.drawString(cx, cy, text)

    # ── Meta grid: 2 columns × 2 rows ────────────────────────────────────────
    col_w   = (W - ML - MR) / 2 - 8   # each meta column
    lbl_w   = 78                        # label width
    val_x_l = ML + lbl_w               # value start, left col
    val_x_r = ML + col_w + 8 + lbl_w   # value start, right col
    val_w   = col_w - lbl_w - 6        # max value width

    rows = [
        [('Document',  'IP-BRAND-ROADMAP-260518-1.3'),
         ('Date',      'May 2026')],
        [('Classification', 'Founding team + named advisors'),
         ('Status',    'Draft — subject to revision')],
    ]
    ry = meta_y - 14
    for row in rows:
        for col_idx, (lbl, val) in enumerate(row):
            lx = ML if col_idx == 0 else ML + col_w + 8
            vx = val_x_l if col_idx == 0 else val_x_r
            c.setFont('Poppins-Bold', 7.5); c.setFillColor(GREY)
            c.drawString(lx, ry, lbl + ':')
            bounded(vx, ry, val, 'Poppins-Regular', 7.5, WHITE, val_w)
        ry -= 14

    # ── Contents: full width, 2 columns of sections ───────────────────────────
    ry -= 8
    c.setFont('Poppins-Bold', 8); c.setFillColor(GOLD)
    c.drawString(ML, ry, 'Contents')
    ry -= 14

    sections = [
        ('1.', 'Current brand positioning',              '2'),
        ('2.', 'The challenge of evolving functionality', '3'),
        ('3.', 'Commercial rationale for Tenzor',         '4'),
        ('4.', 'Tenzor — brand and positioning',          '5'),
        ('5.', 'Risks',                                   '6'),
        ('6.', 'Brand system reference',                  '7'),
        ('7.', 'Open items and decisions required',       '8'),
    ]
    # Two columns of sections — 4 left, 3 right
    sec_col_w = (W - ML - MR) / 2 - 8
    left_secs  = sections[:4]
    right_secs = sections[4:]
    start_ry = ry
    for num, title, pg in left_secs:
        c.setFont('Poppins-Bold', 7.5); c.setFillColor(GOLD)
        c.drawString(ML, ry, num)
        bounded(ML + 16, ry, title, 'Poppins-Regular', 7.5, WHITE, sec_col_w - 30)
        c.setFont('Poppins-Regular', 7.5); c.setFillColor(GREY)
        c.drawRightString(ML + sec_col_w, ry, pg)
        ry -= 12
    ry = start_ry
    rx = ML + sec_col_w + 8
    for num, title, pg in right_secs:
        c.setFont('Poppins-Bold', 7.5); c.setFillColor(GOLD)
        c.drawString(rx, ry, num)
        bounded(rx + 16, ry, title, 'Poppins-Regular', 7.5, WHITE, sec_col_w - 30)
        c.setFont('Poppins-Regular', 7.5); c.setFillColor(GREY)
        c.drawRightString(W - MR, ry, pg)
        ry -= 12

    c.setFillColor(DARKRED); c.rect(ML,MB+20,W-ML-MR,20,fill=1,stroke=0)
    c.setFont('Poppins-Bold',7.5); c.setFillColor(WHITE)
    c.drawCentredString(W/2,MB+28,
        'This document contains unpublished product and brand strategy. Handle accordingly.')
    c.setFont('Poppins-Light',7.5); c.setFillColor(GREY)
    c.drawString(ML,MB+4,'InvestPuppy Pte Ltd · INTERNAL ONLY · May 2026')
    c.drawRightString(W-MR,MB+4,'1')


def _story():
    s=[]
    def H2(t,sub=None):
        for i in sec_hdr(t,sub): s.append(i)
    def H3(t,st='h3'): s.append(Paragraph(t,ST[st]))
    def P(t):  s.append(Paragraph(t,ST['body']))
    def PL(t): s.append(Paragraph(t,ST['bodyl']))
    def BUL(t):s.append(bul(t))
    def N(t):  s.append(note(t))
    def WN(t): s.append(warn(t))
    def SP(n=8):s.append(Spacer(1,n))

    # Page 2 header
    s.append(Paragraph('\u26a0  INTERNAL ONLY \u2014 NOT FOR CLIENT, INVESTOR, OR EXTERNAL DISTRIBUTION  \u26a0',ST['warn']))
    SP(10)

    # Executive summary
    for i in sec_hdr('Executive Summary','What this document covers and why it exists'):
        s.append(i)
    s.append(Paragraph(
        f'{B("InvestPuppy Pte Ltd")} is building two complementary portfolio management products '
        f'under the {B("BY INVESTPUPPY")} maker\u2019s mark. This document records the brand '
        f'architecture of both products, the commercial rationale for maintaining them as '
        f'distinct rather than expanding one, and the open decisions required before Tenzor '
        f'enters production. It is a living internal reference \u2014 not a client document '
        f'and not for external distribution.',
        ST['body']))
    SP(8)

    exec_rows = [
        (f'{B("Vektor")}',
         'Systematic listed equity portfolio management for boutique DPMs, IWMs, and family offices. '
         'Three delivery models. Distribution-ready. First Proof Partners being signed now. '
         'Addressable market: \u223cUS$15M ARR across three primary markets at 10\u0025 penetration.'),
        (f'{B("Tenzor")}',
         'Institutional portfolio management platform built on the same codebase as Vektor. '
         'Native capabilities include systematic portfolio construction, performance attribution, '
         'and core corporate actions. Integrates with OMS and regulatory reporting solutions. '
         'Targets DPM desks at '
         'regional banks, large MFOs, and institutional asset managers. In development. '
         'Addressable market: \u223cUS$10M\u2013US$14M ARR direct subscription across three '
         'markets at 10\u0025 penetration, plus \u223cUS$12M+ via the Wrapped channel.'),
        (f'{B("Combined TAM")}',
         'Approximately US$25M\u2013US$30M ARR at 10\u0025 penetration across Vektor and Tenzor '
         'combined, across Singapore, UK, and Switzerland. The two addressable markets are largely '
         'non-overlapping.'),
        (f'{B("Why two products")}',
         'Expanding Vektor\u2019s scope to cover institutional requirements would dilute the '
         'boutique positioning, break the pricing architecture, and create conflicting sales cycles. '
         'Tenzor is the correct structural response \u2014 same codebase, different scope, '
         'different client, different price. The naming architecture is mathematically coherent: '
         'vectors generalise to tensors.'),
        (f'{B("Brand architecture")}',
         'InvestPuppy is the parent. Vektor and Tenzor are siblings, not tiers. '
         'Both carry the BY INVESTPUPPY maker\u2019s mark in identical grey treatment. '
         'Governing principle: \u201cHonest by design.\u201d'),
        (f'{B("Current status")}',
         'Vektor: pre-revenue, first Proof Partner not yet signed. '
         'Tenzor: brand in working direction (not locked), development timeline TBC. '
         'See Section 6 for full open items.'),
    ]
    s.append(kv(exec_rows, cw=[100, W-ML-MR-100]))
    SP(6)
    s.append(hr(color=DARK, thick=0.5, spb=4, spa=4))

    # Document-level functional scope note
    s.append(warn('Functional scope note: capability descriptions and examples throughout this document \u2014 including references to order management, performance attribution, corporate actions, and regulatory reporting \u2014 are illustrative of intended product direction. They do not constitute a committed functional roadmap, a product specification, or a contractual commitment. Tenzor is in development; scope will be confirmed through the founding team\u2019s product planning process.'))
    SP(6)


    # Version history
    SP(6)
    # Version history
    H3('Version history')
    vw=W-ML-MR
    vh=Table([
        [Paragraph(B('Version'),ST['bodyl']),Paragraph(B('Date'),ST['bodyl']),
         Paragraph(B('Status'),ST['bodyl']),Paragraph(B('Notes'),ST['bodyl'])],
        [Paragraph('1.0',ST['bodyl']),Paragraph('18 May 2026',ST['bodyl']),
         Paragraph('Initial draft',ST['bodyl']),
         Paragraph('First full version',ST['bodyl'])],
        [Paragraph('1.1',ST['bodyl']),Paragraph('18 May 2026',ST['bodyl']),
         Paragraph('Revised',ST['bodyl']),
         Paragraph('Version history, status panel, open items, cover marks, Section 4 status label',ST['bodyl'])],
        [Paragraph('1.2',ST['bodyl']),Paragraph('18 May 2026',ST['bodyl']),
         Paragraph('Revised',ST['bodyl']),
         Paragraph('Exec summary, Avaloq, Vektor colour fix, Wrapped estimate, SE Asia note, conversion note, competitor table',ST['bodyl'])],
        [Paragraph('1.3',ST['bodyl']),Paragraph('18 May 2026',ST['bodyl']),
         Paragraph('Revised',ST['bodyl']),
         Paragraph('Title updated to Architecture. Functional scope note added. Risks section added. CEO disclosure tiers. OMS/reg reporting/corporate actions scope refined throughout.',ST['bodyl'])],
    ],colWidths=[40,80,80,vw-200])
    vh.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'Poppins-Light'),('FONTSIZE',(0,0),(-1,-1),9),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),DARK),
        ('TEXTCOLOR',(0,0),(-1,0),WHITE),('FONTNAME',(0,0),(-1,0),'Poppins-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LIGHT]),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
    ]))
    s.append(vh); SP(12)

    # Status at a glance
    H3('Status at a glance \u2014 May 2026')
    sw=W-ML-MR
    st_data=[
        [Paragraph(B('Element'),ST['bodyl']),Paragraph(B('Status'),ST['bodyl']),Paragraph(B('Note'),ST['bodyl'])],
        [Paragraph('InvestPuppy brand',ST['bodyl']),Paragraph(G(B('Locked')),ST['bodyl']),Paragraph('Parent identity stable',ST['bodyl'])],
        [Paragraph('Vektor brand',ST['bodyl']),Paragraph(Au('Locked \u2014 typeface TBC'),ST['bodyl']),Paragraph('Wordmark typeface unconfirmed \u2014 see T1',ST['bodyl'])],
        [Paragraph('Vektor product',ST['bodyl']),Paragraph(Au('Pre-revenue'),ST['bodyl']),Paragraph('First Proof Partner not yet signed',ST['bodyl'])],
        [Paragraph('Tenzor name',ST['bodyl']),Paragraph(RE('Working \u2014 not locked'),ST['bodyl']),Paragraph('Shortlisted from Tenzor/Vertex/Kern \u2014 see T2',ST['bodyl'])],
        [Paragraph('Tenzor concept',ST['bodyl']),Paragraph(RE('Preferred direction \u2014 not locked'),ST['bodyl']),Paragraph('Platinum + gold Z (Meridian) \u2014 pending T1, T2, T6',ST['bodyl'])],
        [Paragraph('Tenzor typeface',ST['bodyl']),Paragraph(RE('TBC'),ST['bodyl']),Paragraph('Awaiting Vektor typeface confirmation \u2014 see T1',ST['bodyl'])],
        [Paragraph('Tenzor development',ST['bodyl']),Paragraph(RE('Timeline TBC'),ST['bodyl']),Paragraph('No formal roadmap yet \u2014 see P1',ST['bodyl'])],
    ]
    st_t=Table(st_data,colWidths=[130,148,sw-278])
    st_t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'Poppins-Light'),('FONTSIZE',(0,0),(-1,-1),9),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),DARK),
        ('TEXTCOLOR',(0,0),(-1,0),WHITE),('FONTNAME',(0,0),(-1,0),'Poppins-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LIGHT]),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
    ]))
    s.append(st_t); SP(6)
    s.append(hr(color=DARK,thick=0.5,spb=8,spa=4))

    # Sec 1
    H2('1.  Current Brand Positioning','InvestPuppy as parent · Vektor as first product')
    P(f'{B("InvestPuppy Pte Ltd")} is the company. {B("Vektor")} is the product. Every product InvestPuppy builds carries the {B("BY INVESTPUPPY")} maker\'s mark. InvestPuppy is not a product name and is not for sale. It is the name on the door.')
    SP(6); H3('InvestPuppy \u2014 the parent identity')
    P(f'{B("Honest by design.")} This is not a marketing claim. It is a methodology: see it clearly, own it completely, ask what it gives you.')
    SP(4)
    s.append(kv([
        ('Brand voice','\u201cHonest by design.\u201d Direct. Confident. Not performing institutional gravitas.'),
        ('Visual identity','GREEN #85D155 \xb7 DARK #0A0A0A \xb7 Poppins typeface family'),
        ('Strapline','\u201cSerious when it matters.\u201d'),
        ('Maker\'s mark','BY INVESTPUPPY \u2014 grey, all caps, Poppins Light. Consistent across all products.'),
        ('Thought leadership','The Unvarnished series \u2014 10 published papers on why financial software implementations fail'),
    ]))
    SP(12); H3('Vektor \u2014 the first product')
    P(f'{B("Vektor")} is a systematic listed equity portfolio management platform for boutique DPMs, IWMs, and family offices. Three delivery models. One platform.')
    SP(6)
    N(f'{B("What Vektor is:")} Systematic signal application, 10,000 portfolio configurations per strategy, full audit trail, custodian-agnostic architecture.')
    SP(6)
    N(f'{B("What Vektor is not:")} A Bloomberg Terminal replacement. An enterprise PMS. A robo-advisory platform. A reporting layer on top of manual execution.')
    SP(8); H3('Three delivery models')
    BUL(f'{B("Vektor : Boutique")} \u2014 Direct subscription. AUM-tiered (US$18,000\u2013US$175,000). Proof Partners programme for early-commitment clients.')
    BUL(f'{B("Vektor : House")} \u2014 Institutional subscription via Alloy Partners. Staged and gated. InvestPuppy screens and selects partners.')
    BUL(f'{B("Vektor : Wrapped")} \u2014 Licensed via custodian banks. CEO holds production OpenWealth API credentials across Tier 1 institutions globally.')
    SP(8); H3('Vektor pricing \u2014 confirmed May 2026')
    s.append(kv([
        ('Entry (\u2264US$55M)',       'US$18,000/yr'),
        ('Growth (\u2264US$185M)',      'US$36,000/yr'),
        ('Institutional (\u2264US$550M)','US$105,000/yr'),
        ('Enterprise (US$550M+)',       'US$175,000/yr'),
        ('Proof Partners (Tier A)',     'US$13,500 Year 1 \xb7 25% below standard ongoing'),
        ('Proof Partners (Tier B)',     '35% below standard Year 1 \xb7 20% below standard ongoing'),
        ('Vektor : House (ACV)',        'US$250,000 base \u2014 Stage 3 only, not public'),
    ],cw=[185,W-ML-MR-185]))

    # Sec 2
    s.append(PageBreak())
    H2('2.  The Challenge of Evolving Functionality','Why the current structure creates tension as the product matures')
    P('Vektor was designed with a precise scope. This precision is the product\'s commercial strength \u2014 it creates a coherent, defensible market position. As InvestPuppy grows, two forces create tension.')
    SP(8); H3('Force one \u2014 institutional client requirements')
    P(f'The {B("Alloy Partners")} pathway brings institutional clients onto the platform. These clients require capabilities beyond systematic portfolio management:')
    SP(4)
    for t in [f'{B("Order workflow and OMS integration")} \u2014 order routing and workflow with integration to the client\u2019s existing OMS infrastructure.',
              f'{B("Performance attribution")} \u2014 multi-factor attribution, benchmark comparison, formal institutional reporting.',
              f'{B("Core corporate actions")} \u2014 events with direct position or performance impact (see scope note).',
              f'{B("Multi-asset class support")} \u2014 fixed income, alternatives, structured products.',
              f'{B("Regulatory reporting integration")} \u2014 data and integration infrastructure feeding specialist regulatory reporting solutions.']: BUL(t)
    SP(8); H3('Force two \u2014 the Vektor brand scope problem')
    P(f'Adding these capabilities to {B("Vektor")} changes what Vektor is. Three specific risks:')
    SP(4)
    BUL(f'{B("Brand dilution:")} The boutique practitioner feels the product has been repositioned around a different audience. The most common failure mode in B2B software.')
    BUL(f'{B("Pricing incoherence:")} Institutional OMS at boutique pricing is not sustainable. Institutional clients should pay US$250,000\u2013US$400,000+ ACV.')
    BUL(f'{B("Sales cycle conflict:")} Boutique clients close in weeks. Institutional clients close in 12\u201318 months. Running both under the same product name dilutes the Proof Partner motion.')
    SP(8)
    N(f'{B("The structural conclusion:")} Vektor remains precisely what it is. Institutional clients who need order management workflow, performance attribution, and corporate actions handling need {B("Tenzor.")} ')

    # Sec 3
    s.append(PageBreak())
    H2('3.  Commercial and Logical Rationale for Tenzor','Why a separate PMS product \u2014 and why now')
    H3('The mathematical case')
    P(f'A {B("vector")} describes direction and magnitude. A {B("tensor")} generalises a vector into multiple simultaneous dimensions. Vektor handles systematic listed equity construction. Tenzor handles the portfolio management layer at institutional scale \u2014 order workflow, attribution, core corporate actions, multi-asset \u2014 integrating with the execution and compliance infrastructure that surrounds it.')
    SP(6); N(f'{B("Naming architecture:")} Vektor \u2192 Tenzor is the same product logic written in linear algebra. The mathematical coherence of the naming is a competitive asset.')
    SP(6)
    s.append(warn('Functional scope reminder: capability references in this section are illustrative of intended direction. See the functional scope note on page 2 for the full document-level qualification.'))
    SP(10); H3('The commercial case')
    BUL(f'{B("ACV expansion:")} Vektor Enterprise peaks at US$175,000. Tenzor target clients should carry US$250,000\u2013US$400,000+ ACV. Impossible under the Vektor pricing architecture.')
    SP(4)
    BUL(f'{B("Market separation:")} Vektor targets boutique practitioners. Tenzor targets institutional DPM desks, large MFOs, and institutional asset managers. Different procurement, decision-makers, sales cycles.')
    SP(4)
    BUL(f'{B("Natural conversion:")} Vektor : House clients who grow AUM or add asset classes are the natural first Tenzor clients. Vektor builds the relationship; Tenzor scales it.')
    SP(10); H3('Competitive position')
    vv=W-ML-MR
    ct=grid_table(
        ['Platform','Indicative ACV','Gap vs Tenzor'],
        [['Advent Geneva / SS\u0026C','US$100,000+','Built for fund administrators, not boutique-origin practitioners. Heavy SS\u0026C integration overhead.'],
         ['Enfusion','US$150,000+','Strongest at hedge fund scale; heavy implementation overhead; not designed for practitioner-origin boutique growth.'],
         ['Charles River / BlackRock Aladdin','US$250,000+','Enterprise-only; 12\u201318-month implementation; requires dedicated IT resource; not boutique-accessible.'],
         ['Temenos TripleA Plus','US$150,000\u2013US$400,000+','Strong in European private banking and wealth management; broad functionality but significant implementation complexity; less focus on systematic/algorithmic PM; expensive to maintain and upgrade. Actively improving its wealth management positioning.'],
         ['Avaloq','US$200,000\u2013US$500,000+','Core banking platform first, portfolio management second. Significant market presence in Switzerland and Singapore private banking. Strong custodian connectivity but heavy infrastructure overhead and vendor lock-in. Not designed for systematic/algorithmic PM. Long implementation cycles.'],
         ['Bloomberg AIM/PORT','US$30,000\u2013US$80,000','Analytics and reporting add-on to Terminal. Not a systematic execution platform. No native portfolio construction or core corporate actions handling.'],
         [G(B('Tenzor (target)')),Au('US$250,000\u2013US$400,000+'),'Institutional capability on practitioner-proven methodology. Conversion from Vektor relationship, not a cold sale. Systematic PM embedded by design.']],
        [125,110,vv-235])
    ct.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'Poppins-Light'),('FONTSIZE',(0,0),(-1,-1),9),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),DARK),
        ('TEXTCOLOR',(0,0),(-1,0),WHITE),('FONTNAME',(0,0),(-1,0),'Poppins-Bold'),
        ('BACKGROUND',(0,-1),(-1,-1),SECT),
        ('ROWBACKGROUNDS',(0,1),(-1,-2),[WHITE,LIGHT]),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
    ]))
    s.append(ct); SP(10); H3('Timing and sequencing')
    P('Tenzor does not launch before Vektor\'s first Proof Partner is active. Sequence: Proof Partners \u2192 Vektor live accounts \u2192 Alloy Partners Stage 2 \u2192 Tenzor commercial conversations.')
    SP(4)
    N(f'{B("Dependency note:")} If the Vektor commercial launch is delayed, the Tenzor timeline slides proportionally. Development timeline not yet formally specified \u2014 see Open Items, Section 6.')

    SP(10); H3('Addressable market \u2014 Tenzor PMS')
    P('Tenzor targets a distinct and materially larger revenue opportunity than Vektor. '
      'The institutional PMS client \u2014 a DPM desk at a regional bank, a large MFO, '
      'or an institutional asset manager \u2014 carries an ACV three to five times that '
      'of a Vektor : Boutique subscription. The addressable universe across the three '
      'primary markets is smaller in client count but significantly larger in revenue potential.')
    SP(6)

    # TAM table
    vv2=W-ML-MR
    tam=grid_table(
        ['Market','Target profile','Estimated universe','10% penetration @ US$300K ACV'],
        [['Singapore',
          'Institutional DPM desks, large MFOs (>US$500M AUM), EAMs needing full PMS',
          '\u223c80\u2013100 qualifying operations',
          G('\u223cUS$2.5M\u2013US$3M ARR')],
         ['United Kingdom',
          'Mid-tier DPM desks, post-MiFID II boutique institutions, large wealth managers',
          '\u223c150\u2013200 qualifying operations',
          G('\u223cUS$4.5M\u2013US$6M ARR')],
         ['Switzerland',
          'EAMs and IAMs needing portfolio management + attribution, private bank subsidiaries',
          '\u223c100\u2013150 qualifying operations',
          G('\u223cUS$3M\u2013US$4.5M ARR')],
         [B('Three-market primary'),B('Direct subscription only'),
          B('\u223c330\u2013450 total'),
          G(B('\u223cUS$10M\u2013US$14M ARR'))]],
        [100,160,130,vv2-390])
    tam.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'Poppins-Light'),('FONTSIZE',(0,0),(-1,-1),9),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),DARK),
        ('TEXTCOLOR',(0,0),(-1,0),WHITE),('FONTNAME',(0,0),(-1,0),'Poppins-Bold'),
        ('BACKGROUND',(0,-1),(-1,-1),SECT),('FONTNAME',(0,-1),(-1,-1),'Poppins-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-2),[WHITE,LIGHT]),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
    ]))
    s.append(tam); SP(8)
    N(f'{B("Wrapped channel multiplier:")} The above table covers direct Tenzor subscription only. '
      f'If the Wrapped channel delivers two major custodian bank partnerships, '
      f'each bringing 40 EAMs requiring full PMS capability at a Tenzor Wrapped fee of US$150,000 per year, '
      f'the calculation is: 2 \u00d7 40 \u00d7 US$150,000 = {B("US$12M additional ARR.")} '
      f'Adding this to the direct subscription market gives a total Tenzor addressable of '
      f'approximately {B("US$22M\u2013US$26M ARR")} at conservative assumptions. '
      f'The Wrapped channel is excluded from the table above to keep primary market sizing independently defensible.')
    SP(8)
    N(f'{B("Relationship to Vektor TAM:")} The Vektor and Tenzor addressable markets are largely '
      f'non-overlapping. Vektor targets boutique practitioners (typically below US$550M AUM). '
      f'Tenzor targets institutional operations that have outgrown boutique tooling or require '
      f'attribution and order management capability from the outset. '
      f'Combined three-market addressable across both products: approximately US$25M\u2013US$30M ARR '
      f'at 10% penetration.')
    SP(6)
    N(f'{B("Second-wave markets:")} The table covers Singapore, UK, and Switzerland as primary markets. '
      f'Indonesia, Malaysia, Thailand, and the Philippines represent a subsequent expansion wave \u2014 '
      f'institutional asset management is growing rapidly across Southeast Asia and tooling '
      f'remains significantly more primitive than Singapore. '
      f'The Wrapped channel through major Asian custodians is the natural entry mechanism '
      f'for these markets rather than direct subscription sales.')

    # Sec 4
    s.append(PageBreak())
    H2('4.  Tenzor \u2014 Brand and Positioning','Identity, visual system, and market position')
    WN('WORKING DIRECTION \u2014 not formally locked. All specifications are subject to change pending: T1 (Vektor typeface confirmation), T2 (Tenzor name lock), T6 (preferred concept formal lock). Do not treat anything below as production-ready.')
    SP(8); s.append(Paragraph('\u201cThe institutional portfolio management platform for operations that cannot afford approximation.\u201d',ST['qt']))
    P('Tenzor is positioned as the institutional operating layer \u2014 the tool for DPM desks, large MFOs, and institutional asset managers who need the full spectrum of portfolio management capability at the same quality standard Vektor delivers for systematic listed equity.')
    SP(6)
    N('Core corporate actions: Tenzor handles corporate actions events with direct position or '
      'performance impact \u2014 dividends, stock splits, rights issues, and mandatory events '
      'such as mergers, redemptions, and demergers. Excluded from core scope: optional or elective '
      'events requiring client instruction; complex events requiring specialist processing; and '
      'non-financial events with no position or performance impact \u2014 for example AGM notices. '
      'These exclusions reflect deliberate architectural design.')
    SP(6)
    N(f'{B("The conversion advantage:")} No competitor in the institutional PMS market can replicate the Tenzor commercial motion. Tenzor\u2019s first clients are not cold sales \u2014 they are Vektor : House clients who have already adopted InvestPuppy\u2019s methodology, trust the team, and are growing into institutional requirements. A conversion from an established relationship, not a new customer acquisition. This is a brand asset as much as a commercial one: it signals that Tenzor clients are chosen, not simply sold to.')
    SP(10); H3('Preferred visual direction \u2014 Meridian Studio concept','h3p')
    s.append(kv([
        ('Wordmark colour',    'Platinum #9EA8B3 \u2014 preferred, not locked'),
        ('Z crossbar',         'Gold #C8A96E \u2014 same gold as Vektor V arrowhead'),
        ('BY INVESTPUPPY',     'Grey \u2014 consistent with actual Vektor mark treatment'),
        ('Typeface',           'Same family as Vektor (TBC \u2014 awaiting T1 confirmation)'),
        ('Tagline direction',  '\u201cEvery dimension. Every decision.\u201d (candidate \u2014 not locked)'),
        ('Background',         'DARK #0A0A0A \u2014 Tier 1 full dark brand treatment'),
    ],cw=[170,W-ML-MR-170]))
    SP(10); H3('The gold Z crossbar \u2014 rationale','h3g')
    P(f'The gold crossbar through the central Z echoes the Vektor V arrowhead (also Gold #C8A96E). This creates a visible family link \u2014 platinum carries Tenzor\'s independent identity; gold marks the shared InvestPuppy accent both products carry.')
    SP(10); H3('Scale variants')
    BUL(f'{B("Variant A \u2014 Full display (20px+):")} Platinum wordmark + Gold Z crossbar + Grey BY INVESTPUPPY. Primary mark.')
    BUL(f'{B("Variant B \u2014 Reduced small (12\u201320px):")} Platinum wordmark only + Grey BY INVESTPUPPY. No crossbar.')
    BUL(f'{B("Variant C \u2014 Monochrome:")} White wordmark + White BY INVESTPUPPY. Not yet fully specified.')
    SP(8); N(f'{B("Governance note:")} Full mark at 20px and above; reduced mark below 20px. This rule must be documented and applied by everyone producing Tenzor-branded materials.')
    SP(8); H3('Colour architecture \u2014 forward note')
    P('GREEN belongs to both InvestPuppy and Vektor. With a third product, a formal colour architecture decision will be required: does green belong to InvestPuppy specifically, or to Vektor? Resolve before a third product enters development.')


    # Sec 5 — Risks
    s.append(PageBreak())
    H2('5.  Risks','Known risks and mitigations')
    P('This section documents known risks. Acknowledging them clearly is consistent with the governing principle.')
    SP(8)
    risks = [
        (f'{B("R1 \u2014 Product boundary management")}',
         f'The boundary between Vektor and Tenzor functionality must be actively governed. '
         f'Multi-asset strategies could be argued for either product; without a clear decision framework, '
         f'the boundary will be negotiated case-by-case under client pressure, diluting both products. '
         f'{B("Mitigation:")} Establish a product boundary framework before Tenzor is commercially described. '
         f'Criterion: institutional operations requirements (order workflow, full attribution, complex corporate actions) '
         f'belong to Tenzor. Boutique practitioner requirements belong to Vektor.'),
        (f'{B("R2 \u2014 Team bandwidth and focus dilution")}',
         f'Five people carrying Vektor commercial launch, Tenzor development, Alloy Partners, and investor '
         f'relations simultaneously creates real execution risk across all streams. '
         f'{B("Mitigation:")} Sequence deliberately. Vektor Proof Partners must close before Tenzor '
         f'development is prioritised at scale. See Open Items P1 and P2.'),
        (f'{B("R3 \u2014 Regulatory scope expansion")}',
         f'Tenzor\u2019s order workflow and institutional client profile may trigger MAS or FCA '
         f'licensing requirements the current entity does not hold. '
         f'{B("Mitigation:")} Legal review of Tenzor\u2019s regulatory footprint must be commissioned '
         f'before any commercial offer is made, in any market.'),
        (f'{B("R4 \u2014 Competitive response")}',
         f'Announcing Tenzor signals to Temenos, Avaloq, Advent, and Enfusion that InvestPuppy is '
         f'entering institutional territory. Competitors may improve boutique offerings or price '
         f'aggressively against Vektor to block InvestPuppy\u2019s institutional pathway. '
         f'{B("Mitigation:")} Manage the timing of Tenzor\u2019s public announcement relative to '
         f'Vektor\u2019s commercial launch. Vektor relationships should be established first.'),
        (f'{B("R5 \u2014 Client confusion at the product boundary")}',
         f'A fast-growing Vektor client approaching institutional scale may resist moving to Tenzor '
         f'rather than seeing Vektor grow with them. '
         f'{B("Mitigation:")} Develop a conversion narrative before the first client reaches '
         f'institutional scale. Frame Tenzor as the institutional expression of the same methodology, '
         f'not a different product.'),
        (f'{B("R6 \u2014 Investor disclosure timing")}',
         f'Raising the seed round on a Vektor-only narrative and announcing Tenzor post-close '
         f'risks investor surprise. Introducing Tenzor too early creates expectations the team '
         f'may not meet on the projected timeline. '
         f'{B("Mitigation:")} Decide the investor disclosure posture for Tenzor before the first '
         f'investor meeting. This document is internal only for this reason.'),
        (f'{B("R7 \u2014 Brand sequencing")}',
         f'Vektor establishes InvestPuppy in the market as boutique-focused. Tenzor\u2019s '
         f'institutional positioning must overcome that first impression. '
         f'{B("Mitigation:")} The BY INVESTPUPPY maker\u2019s mark and open architecture philosophy '
         f'are the bridging elements. The narrative \u2014 Vektor proved the methodology at boutique '
         f'scale; Tenzor scales it to institutional operations \u2014 must be embedded from the outset.'),
    ]
    for label, body in risks:
        s.append(Paragraph(label, ST['h3']))
        s.append(Paragraph(body, ST['body']))
        SP(8)

    # Sec 6
    s.append(PageBreak())
    H2('6.  Brand System Reference','Locked elements \u2014 do not change without founding team decision')
    WN('All locked elements require a founding team decision to change and must be propagated across all documents, website, and admin portal.')
    SP(10); H3('InvestPuppy \u2014 parent (locked)')
    s.append(kv([
        ('Primary green',  'GREEN #85D155'),
        ('Dark ground',    'DARK #0A0A0A'),
        ('Body typeface',  'Poppins (Light, Regular, Medium, Bold, Italic)'),
        ('Strapline',      '\u201cSerious when it matters.\u201d'),
        ('Principle',      '\u201cHonest by design.\u201d'),
        ('Brand method',   'See it clearly. Own it completely. Ask what it gives you.'),
        ('Maker\'s mark', 'BY INVESTPUPPY \u2014 grey, all caps, Poppins Light, tracked'),
        ('Gold accent',    '#C8A96E \u2014 secondary system colour'),
    ]))
    SP(12); H3('Vektor \u2014 first product (locked)')
    s.append(kv([
        ('Wordmark colour', 'Grey/white \u2014 thin geometric letterforms. Not green. Green belongs to InvestPuppy.'),
        ('Wordmark',       'TBC typeface \u2014 thin geometric sans, light weight'),
        ('Arrowhead',      'Gold #C8A96E \u2014 locked element'),
        ('BY INVESTPUPPY', 'Grey \u2014 confirmed from actual mark'),
        ('Delivery models','Vektor : Boutique \xb7 Vektor : House \xb7 Vektor : Wrapped'),
        ('Tagline',        '\u201cHonest by design.\u201d'),
    ]))
    SP(12); H3('Tenzor \u2014 second product (working direction)','h3p')
    s.append(kv([
        ('Primary colour', 'Platinum #9EA8B3 \u2014 preferred, not locked'),
        ('Z crossbar',     'Gold #C8A96E \u2014 shared family accent'),
        ('BY INVESTPUPPY', 'Grey \u2014 consistent with Vektor mark'),
        ('Typeface',       'TBC \u2014 same family as Vektor'),
        ('Voice direction','\u201cEvery dimension. Every decision.\u201d \u2014 candidate'),
        ('Status',         'In development \u2014 not for external use'),
    ]))
    SP(12); H3('Locked terminology')
    s.append(kv([
        ('10,000 portfolio configurations','Never: \u201cMonte Carlo\u201d or \u201csimulations\u201d'),
        ('99.94%',                          'Never: \u201c99.9%\u201d'),
        ('Preferential commercial terms locked for the duration','Never: \u201cpermanently preferential\u201d'),
        ('Proof Partners',                  'Never: \u201cProof Partners programme\u201d or \u201cearly-commitment partners\u201d'),
        ('Has not yet executed in a live account','Never: \u201csimulation mode\u201d'),
        ('Boutique wealth practitioners',   'Never: only \u201cfamily office investors\u201d'),
        ('Vektor : Boutique / House / Wrapped','Space before colon \u2014 always'),
    ],cw=[220,W-ML-MR-220]))

    # Sec 6
    s.append(PageBreak())
    H2('7.  Open Items and Decisions Required','What needs to happen next \u2014 founding team decisions')
    N('This section tracks decisions required before Tenzor brand and product work can progress. CRITICAL items gate all downstream work.')
    SP(10); H3('Tenzor brand open items')
    ow=W-ML-MR
    oi=grid_table(
        ['#','Item','Priority','Detail'],
        [['T1',f'{B("Vektor typeface confirmation")}',RE(B('CRITICAL')),'Actual typeface in Vektor production mark is unconfirmed. Josefin Sans Light used as working approximation. Gates all Tenzor wordmark production work.'],
         ['T2','Tenzor name lock',RE(B('HIGH')),'Tenzor is working name; shortlisted with Vertex and Kern. Confirm before investing further in brand execution.'],
         ['T3','Two-variant system governance',RE(B('HIGH')),'Who owns the usage rule? How is it enforced as the team grows?'],
         ['T4','Monochrome variant specification',Au(B('MEDIUM')),'Variant C (white on dark) not yet specified. Needed for legal documents and single-colour print.'],
         ['T5','Minimum clear space rule',Au(B('MEDIUM')),'Convention: cap-height on all sides. Not yet formally specified.'],
         ['T6','Preferred concept formal lock',RE(B('HIGH')),'Dan has expressed preference for Meridian concept (platinum + gold Z). Not formally locked.'],
         ['T7','Voice direction decision',Au(B('MEDIUM')),'\u201cEvery dimension. Every decision.\u201d is a candidate tagline. \u201cFor institutions that cannot afford approximation.\u201d is the positioning statement. Neither formally adopted.']],
        [25,130,72,ow-227])
    s.append(oi); SP(16); H3('Product and commercial open items')
    pi=grid_table(
        ['#','Item','Priority','Detail'],
        [['P1',f'{B("Tenzor development timeline")}',RE(B('HIGH')),'No formal development roadmap. Is this a 12-month or 24-month build? Does it require additional engineering resource?'],
         ['P2','Team and resource for Tenzor',RE(B('HIGH')),'Confirm whether current team builds Tenzor or whether new hires are required alongside the Vektor commercial launch.'],
         ['P3','Vektor : House \u2192 Tenzor relationship',RE(B('HIGH')),'Two options: (a) House converts to Tenzor at a defined trigger; or (b) they co-exist as separate institutional options. This shapes the entire commercial architecture.'],
         ['P4','Tenzor pricing logic',Au(B('MEDIUM')),'US$250,000\u2013US$400,000+ ACV stated without supporting rationale. How was this range derived?'],
         ['P5','Long-term colour architecture',Au(B('MEDIUM')),'GREEN belongs to InvestPuppy and Vektor. What happens with a third product? Resolve before third product enters development.']],
        [25,140,72,ow-237])
    s.append(pi); SP(16)

    H3('CEO background — disclosure tier framework')
    s.append(warn('INTERNAL ONLY. The following framework must not be reproduced in any external document. '
         'Premature disclosure of the CEO background at Tier 2 or Tier 3 specificity would make '
         'him identifiable in the market even without disclosing his name.'))
    SP(6)

    tier_data = [
        [Paragraph(B('Tier'), ST['bodyl']),
         Paragraph(B('Context'), ST['bodyl']),
         Paragraph(B('Approved language'), ST['bodyl'])],
        [Paragraph('Tier 1', ST['bodyl']),
         Paragraph('Public / all external documents, website, investor pack', ST['bodyl']),
         Paragraph('Institutional wealth management technology experience at enterprise scale.', ST['bodyl'])],
        [Paragraph('Tier 2', ST['bodyl']),
         Paragraph('NDA context — qualified investor or partner under NDA', ST['bodyl']),
         Paragraph('Extensive experience as a vendor and implementation specialist for a leading '
                   'institutional portfolio management platform, including solution architecture '
                   'for Global Tier 1 bank deployments.', ST['bodyl'])],
        [Paragraph('Tier 3', ST['bodyl']),
         Paragraph('Internal only — this document and founding team', ST['bodyl']),
         Paragraph('CEO has worked with Temenos TripleA Plus since its commercial launch in 1997, '
                   'from vendor, implementation, and solution architecture perspectives, '
                   'including multiple Global Tier 1 bank projects. This provides InvestPuppy '
                   'with competitive intelligence on its primary European competitor that is '
                   'not available to most market entrants.', ST['bodyl'])],
    ]
    vw3 = W - ML - MR
    tier_table = Table(tier_data, colWidths=[40, 140, vw3 - 180])
    tier_table.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),'Poppins-Light'), ('FONTSIZE',(0,0),(-1,-1),9),
        ('VALIGN',(0,0),(-1,-1),'TOP'), ('BACKGROUND',(0,0),(-1,0),DARK),
        ('TEXTCOLOR',(0,0),(-1,0),WHITE), ('FONTNAME',(0,0),(-1,0),'Poppins-Bold'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,LIGHT]),
        ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
    ]))
    s.append(tier_table)
    SP(8)
    N(f'{B("Competitive intelligence note:")} The CEO\u2019s Tier 3 background in Temenos TripleA Plus '
      f'provides InvestPuppy with first-hand knowledge of TripleA\u2019s architectural limitations, '
      f'implementation failure modes, commercial pricing dynamics, and client relationship patterns. '
      f'This directly informs Tenzor\u2019s product design decisions and competitive positioning. '
      f'The detailed competitive characterisation of Temenos TripleA Plus in Section 3 reflects '
      f'this insider knowledge, not external research.')
    SP(8)
    N(f'{B("Temenos competitive gap note:")} Temenos is actively investing in its SaaS transformation '
      f'and wealth management capabilities. The competitive gap between Tenzor and TripleA Plus '
      f'should not be assumed to be static. Monitor Temenos product announcements as part of '
      f'ongoing competitive intelligence.')
    SP(16)
    s.append(Paragraph('\u201cHonest by design.\u201d',ST['qt']))
    return s

class _Doc(SimpleDocTemplate):
    def __init__(self,fn):
        super().__init__(fn,pagesize=A4,leftMargin=ML,rightMargin=MR,topMargin=MT,bottomMargin=MB)

def main():
    from pypdf import PdfWriter, PdfReader
    cp='/tmp/rm_cover.pdf'; bp='/tmp/rm_body.pdf'
    c=pdfcanvas.Canvas(cp,pagesize=A4); _cover(c); c.save()
    doc=_Doc(bp); doc.build(_story(),onFirstPage=_hf,onLaterPages=_hf)
    w=PdfWriter()
    for p in [cp,bp]:
        r=PdfReader(p)
        for pg in r.pages: w.add_page(pg)
    with open(OUT,'wb') as f: w.write(f)
    for p in [cp,bp]: os.remove(p)
    r=PdfReader(OUT)
    print(f'Saved: {OUT} ({os.path.getsize(OUT)//1024}KB, {len(r.pages)} pages)')

if __name__=='__main__': main()
