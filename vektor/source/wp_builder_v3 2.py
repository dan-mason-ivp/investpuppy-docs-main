"""
Shared white paper building utilities for Vektor Research Series.
Import and use in individual WP build scripts.
"""
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


# ── Repo-relative asset resolution ───────────────────────────────────────────
import os as _os
_SCRIPT_DIR = _os.path.dirname(_os.path.abspath(__file__))  # vektor/source/
_REPO_ROOT   = _os.path.dirname(_os.path.dirname(_SCRIPT_DIR))  # investpuppy/
_LOGOS       = _os.path.join(_REPO_ROOT, '_shared', 'logos')
_SCREENSHOTS = _os.path.join(_SCRIPT_DIR, 'screenshots')

W,H=A4; ML=MR=22*mm; MT1=16*mm; MT2=46*mm; MB=20*mm; COL_W=W-ML-MR
LOGO=_os.path.join(_LOGOS,'VEKTOR-transparent-v3.png'); DATE='May 2026'
SERIES_TAG='VEKTOR RESEARCH SERIES · 2026'
SERIES_FOOTER_TAG='VEKTOR RESEARCH SERIES · 2026 · May 2026'
IP_H=_os.path.join(_LOGOS,'IPHorizontalClear.png')
IP_H_RATIO=2.337


def mk(name,**kw):
    d=dict(fontName='Helvetica',fontSize=9.5,textColor=OFF_WHITE,leading=17,spaceAfter=8)
    d.update(kw); return ParagraphStyle(name,**d)

def make_styles():
    s={}
    s['tag']=mk('tag',fontSize=7,textColor=WARM_GREY,leading=11,letterSpacing=4,spaceAfter=4)
    s['wp_section']=mk('wps',fontName='Helvetica-Bold',fontSize=13,textColor=PLATINUM,
        leading=19,spaceAfter=5,spaceBefore=10)
    s['wp_sub']=mk('wpsub',fontName='Helvetica-Bold',fontSize=10.5,textColor=GOLD,
        leading=15,spaceAfter=5,spaceBefore=8)
    s['body']=mk('body',alignment=TA_JUSTIFY)
    s['body_grey']=mk('bgrey',textColor=WARM_GREY,alignment=TA_JUSTIFY)
    s['bullet']=mk('blt',fontSize=9.5,textColor=OFF_WHITE,leading=15,spaceAfter=4,
        leftIndent=8,alignment=TA_JUSTIFY)
    s['kt_body']=mk('ktb',fontSize=9,textColor=OFF_WHITE,leading=15,spaceAfter=5,
        leftIndent=8,alignment=TA_JUSTIFY)
    s['key_takeaway_title']=mk('ktt',fontName='Helvetica-Bold',fontSize=8,textColor=GOLD,
        leading=11,letterSpacing=2,spaceAfter=6)
    s['pull']=mk('pull',fontName='Helvetica-Oblique',fontSize=10,textColor=PLATINUM,
        leading=17,alignment=TA_CENTER)
    s['tbl_hdr']=mk('th',fontName='Helvetica-Bold',fontSize=7.5,textColor=PLATINUM,leading=11)
    s['tbl_body']=mk('tb',fontSize=8.5,textColor=OFF_WHITE,leading=12,alignment=TA_JUSTIFY)
    s['tbl_grey']=mk('tg',fontSize=8.5,textColor=WARM_GREY,leading=12,alignment=TA_JUSTIFY)
    s['tbl_gold']=mk('tgold',fontSize=8.5,textColor=GOLD,leading=12)
    s['ref_line']=mk('rl',fontName='Helvetica-Oblique',fontSize=8.5,textColor=WARM_GREY,
        leading=13,alignment=TA_JUSTIFY)
    s['wp_ref']=mk('wpr',fontSize=7.5,textColor=colors.HexColor('#555550'),
        leading=11,alignment=TA_CENTER)
    s['cover_label']=mk('cl',fontSize=7.5,textColor=WARM_GREY,leading=11)
    return s


class HRule(Flowable):
    def __init__(self,w,c=RULE_MIN,t=0.5,sa=4,sb=4):
        Flowable.__init__(self); self.rw=w; self.c=c; self.t=t
        self._sa=sa; self._sb=sb; self.height=sa+t+sb
    def wrap(self,aw,ah): return self.rw,self.height
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        self.canv.line(0,self._sb+self.t/2,self.rw,self._sb+self.t/2)


class NoteBox(Flowable):
    def __init__(self,w,text,style,bg=NOTE_BG,bar=RULE_MAJ,ph=15,pv=13,bw=4):
        Flowable.__init__(self); self._w=w; self.bg=bg; self.bar=bar
        self.ph=ph; self.pv=pv; self.bw=bw
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


def make_cover_fn(title_lines, distil, audience, ref_code):
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
            canvas.drawCentredString(W/2,ry-14,SERIES_TAG)
            y=ry-44
            canvas.setFont('Helvetica-Bold',18); canvas.setFillColor(PLATINUM)
            for line in title_lines:
                canvas.drawCentredString(W/2,y,line); y-=26
            canvas.setFont('Helvetica-Oblique',10); canvas.setFillColor(WARM_GREY)
            y-=4
            for line in distil:
                canvas.drawCentredString(W/2,y,line); y-=16
        except Exception as e: print(e)
        canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4); canvas.line(ML,36*mm,W-MR,36*mm)
        canvas.setFont('Helvetica',7.5); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2,29*mm,audience)
        canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#555550'))
        canvas.drawCentredString(W/2,22*mm,ref_code)
        canvas.drawCentredString(W/2,16*mm,DATE)
        canvas.restoreState()
    return draw_cover


def make_page_fn(doc_subtitle):
    footer=f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  {doc_subtitle}  \u00b7  May 2026'
    def draw_page(canvas,doc):
        canvas.saveState()
        canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
        from reportlab.lib.utils import ImageReader
        hy=H-MT2+14
        try:
            img=ImageReader(LOGO); iw,ih=img.getSize(); lh=22; lw=lh*iw/ih
            canvas.drawImage(LOGO,ML,hy,lw,lh,mask='auto',preserveAspectRatio=True)
        except: pass
        canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#555550'))
        canvas.drawRightString(W-MR,H-MT2+18,f'{doc_subtitle}  \u00b7  {doc.page-1:02d}')
        canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.4); canvas.line(ML,H-MT2+8,W-MR,H-MT2+8)
        canvas.setLineWidth(0.3); canvas.line(ML,MB-2,W-MR,MB-2)
        ip_w=32*mm; ip_h=ip_w/IP_H_RATIO
        try:
            canvas.drawImage(IP_H,ML,1.0*mm,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
        except Exception as e: print(e)
        canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#444440'))
        canvas.drawRightString(W-MR,1.0*mm+ip_h/2-2.5,f'investpuppy.com  \u00b7  {DATE}')
        canvas.restoreState()
    return draw_page


def make_doc(output_path, title, author='InvestPuppy'):
    f_cov=Frame(0,0,W,H,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='cov')
    f_fst=Frame(ML,MB,COL_W,H-MT1-MB,id='fst')
    f_lat=Frame(ML,MB,COL_W,H-MT2-MB,id='lat')
    return (BaseDocTemplate(output_path,pagesize=A4,leftMargin=ML,rightMargin=MR,
        topMargin=MT1,bottomMargin=MB,title=title,author=author), f_cov, f_fst, f_lat)


def p(text,style): return Paragraph(text,style)
def sp(n=8): return Spacer(1,n)
def hrm(): return HRule(COL_W,RULE_MAJ,1.0,3,5)
def hrn(): return HRule(COL_W,RULE_MIN,0.3,3,3)
def hrgold(): return HRule(COL_W,GOLD,0.8,4,6)


def key_takeaways_box(items, s):
    """Build the KEY TAKEAWAYS note box."""
    rows=[[p('KEY TAKEAWAYS',s['key_takeaway_title'])]]
    for item in items:
        rows.append([p(f'\u2014 {item}',s['kt_body'])])
    t=Table(rows,colWidths=[COL_W-8])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),NOTE_BG),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
        ('LINEABOVE',(0,1),(-1,-1),0,colors.white),
    ]))
    return t


def closing_row(cross_refs, ref_code, s, story):
    story.append(sp(10)); story.append(hrgold()); story.append(sp(6))
    story.append(p(cross_refs, s['ref_line']))
    story.append(sp(8))
    story.append(p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {ref_code}  \u00b7  Copyright 2026 InvestPuppy',s['wp_ref']))
