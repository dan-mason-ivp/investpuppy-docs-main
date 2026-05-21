"""
WP-00: Vektor Research Series Index — dark-branded ReportLab rebuild.
Corrections: all 10 papers listed (was only 6 in docx / 8 in PDF), 99.94% in WP-03 description.
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

W,H=A4; ML=MR=22*mm; MT1=16*mm; MT2=46*mm; MB=20*mm; COL_W=W-ML-MR
LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png'); DATE='May 2026'
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')
IP_H_RATIO = 2.337
DOC_SERIES='VEKTOR RESEARCH SERIES · 2026'
SUB='Research Series Index'
FOOTER=f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  {DATE}'

def S():
    s={}
    s['tag']=ParagraphStyle('tag',fontName='Helvetica',fontSize=7,textColor=WARM_GREY,
        leading=11,spaceAfter=4,letterSpacing=4)
    s['overview']=ParagraphStyle('ov',fontName='Helvetica',fontSize=9.5,textColor=OFF_WHITE,
        leading=17,spaceAfter=8,alignment=TA_JUSTIFY)
    s['ref']=ParagraphStyle('ref',fontName='Helvetica-Bold',fontSize=9,textColor=GOLD,
        leading=13)
    s['title']=ParagraphStyle('ttl',fontName='Helvetica-Bold',fontSize=9,textColor=PLATINUM,
        leading=13)
    s['desc']=ParagraphStyle('dsc',fontName='Helvetica',fontSize=8.5,textColor=OFF_WHITE,
        leading=13,alignment=TA_JUSTIFY)
    s['audience']=ParagraphStyle('aud',fontName='Helvetica-Oblique',fontSize=8,
        textColor=WARM_GREY,leading=12)
    s['tbl_hdr']=ParagraphStyle('th',fontName='Helvetica-Bold',fontSize=7.5,
        textColor=PLATINUM,leading=11)
    s['footer']=ParagraphStyle('ftr',fontName='Helvetica',fontSize=6.5,
        textColor=colors.HexColor('#444440'),alignment=TA_CENTER,leading=10)
    s['wp_ref']=ParagraphStyle('wpr',fontName='Helvetica',fontSize=7.5,
        textColor=colors.HexColor('#555550'),alignment=TA_CENTER,leading=11)
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
    def __init__(self,w,text,style):
        Flowable.__init__(self); self._w=w
        self._p=Paragraph(text,style); self._iw=w-4-15*2
    def wrap(self,aw,ah):
        _,h=self._p.wrap(self._iw,ah); self.height=h+13*2; return self._w,self.height
    def draw(self):
        c=self.canv; c.saveState()
        c.setFillColor(NOTE_BG); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0,0,self._w,self.height,3,fill=1,stroke=1)
        c.setFillColor(RULE_MAJ); c.roundRect(0,0,4,self.height,2,fill=1,stroke=0)
        self._p.wrap(self._iw,self.height); self._p.drawOn(c,4+15,13)
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
        canvas.drawCentredString(W/2,ry-14,DOC_SERIES)
        canvas.setFont('Helvetica-Bold',22); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2,ry-42,'Research Series Index')
        canvas.setFont('Helvetica-Oblique',10); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2,ry-62,
            'Ten white papers covering the methodology, infrastructure,')
        canvas.drawCentredString(W/2,ry-76,
            'and compliance architecture of the Vektor platform.')
    except Exception as e: print(e)
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4); canvas.line(ML,36*mm,W-MR,36*mm)
    canvas.setFont('Helvetica',7.5); canvas.setFillColor(WARM_GREY)
    canvas.drawCentredString(W/2,28*mm,'For professional and institutional investors only')
    canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W/2,16*mm,DATE)
    canvas.restoreState()


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
    canvas.drawRightString(W-MR,H-MT2+18,f'{SUB}  \u00b7  {doc.page-1:02d}')
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.4)
    canvas.line(ML,H-MT2+8,W-MR,H-MT2+8)
    canvas.setLineWidth(0.3); canvas.line(ML,MB-2,W-MR,MB-2)
    ip_w=32*mm; ip_h=ip_w/IP_H_RATIO
    try:
        canvas.drawImage(IP_H,ML,1.0*mm,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawRightString(W-MR,1.0*mm+ip_h/2-2.5,f'investpuppy.com  ·  {DATE}')
    canvas.restoreState()


def build():
    out='/home/claude/investpuppy/vektor/output/pdf/vk5-wp00-research-series-index.pdf'
    s=S()
    f_cov=Frame(0,0,W,H,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='cover')
    f_body=Frame(ML,MB,COL_W,H-MT2-MB,id='body')
    doc=BaseDocTemplate(out,pagesize=A4,leftMargin=ML,rightMargin=MR,
        topMargin=MT1,bottomMargin=MB,
        title='Vektor Research Series Index',author='InvestPuppy')
    doc.addPageTemplates([
        PageTemplate(id='Cover',frames=[f_cov],onPage=draw_cover),
        PageTemplate(id='Body',frames=[f_body],onPage=draw_page),
    ])

    story=[]
    story.append(Spacer(1,1)); story.append(NextPageTemplate('Body')); story.append(PageBreak())

    story.append(Paragraph('SERIES OVERVIEW',s['tag']))
    story.append(NoteBox(COL_W,
        'These ten papers exist because every claim Vektor makes deserves documentation. '
        'If a question about the platform\u2019s methodology is not answered here, it should be '
        '\u2014 and we would like to know. The series covers every major component of the platform: '
        'foundational portfolio construction methodology, per-instrument signal selection, capital '
        'allocation precision, multi-currency infrastructure, compliance architecture, technical '
        'infrastructure, AI governance, risk disclosure, and performance evaluation. '
        'Each paper is self-contained and can be read independently.',
        s['overview']))
    story.append(Spacer(1,10))

    # All 10 papers — complete and corrected
    papers=[
        ('WP-01','Quantitative Portfolio Construction for Single-Country Equity Markets',
         'The foundational paper. A replicable five-stage framework \u2014 universe screening, '
         '10,000 portfolio configurations mapping the efficient frontier, and benchmark validation '
         '\u2014 illustrated with a worked SGX implementation.',
         'DPMs, family office analysts, institutional allocators'),
        ('WP-02','Per-Instrument Signal Optimisation & XGBoost Validation',
         'How Vektor selects the optimal technical indicator for every individual holding through '
         'a grid search across six indicators \u2014 and how XGBoost validates every live signal '
         'before execution.',
         'Quant analysts, systematic traders, technical DPMs'),
        # CORRECTED: 99.94%
        ('WP-03','Capital Allocation Precision: From Weights to Positions',
         'How percentage weights become actual share quantities at live prices. Lot size rounding, '
         'cash buffer configuration, and how 99.94% capital allocation efficiency is achieved and verified.',
         'DPMs, operations teams, family office managers'),
        ('WP-04','Technical Indicator Selection: Grid Search Methodology',
         'A practitioner\u2019s guide to systematic parameter optimisation. Full parameter space '
         'specification, Sharpe ratio as objective function, three-year look-back rationale, and '
         'overfitting controls.',
         'Quant analysts, risk managers, systematic traders'),
        ('WP-05','Multi-Currency Portfolio Infrastructure',
         'Daily FX rate collection, position-level currency conversion, per-client base currency '
         'configuration, and generalisation to any market and currency pair.',
         'Multi-mandate family offices, cross-border DPMs'),
        ('WP-06','Audit Trail & Compliance Architecture',
         'The three-role accountability structure, complete action logging across all eleven workflow '
         'steps, and how Vektor produces an institutional-grade audit trail as a by-product of '
         'normal platform operation.',
         'Compliance officers, institutional due diligence teams'),
        ('WP-07','Production Infrastructure: The Vektor Technical Architecture',
         'The AWS services, architectural decisions, and design principles behind the Vektor platform '
         '\u2014 documented as a record of choices made. Includes integration architecture for PMS '
         'connectivity, region-agnostic deployment, and current deployment status.',
         'CTOs, technical due diligence teams, institutional partners'),
        ('WP-08','AI as Instrument: Machine Learning in Systematic Portfolio Management',
         'Where ML is used in Vektor, where it is not, human approval gates at every decision point, '
         'model governance framework, and alignment with MAS FEAT principles for responsible AI '
         'in financial services.',
         'Compliance officers, risk committees, institutional due diligence'),
        ('WP-09','Risk & Limitation Disclosure',
         'Fourteen identified risks across four categories \u2014 data, methodology, operational, '
         'and regulatory \u2014 with mitigations currently in place and those on the near-term '
         'roadmap. Read before any risk committee or compliance presentation.',
         'Due diligence teams, risk committees, compliance officers'),
        ('WP-10','Evaluating Systematic Strategy Performance',
         'A framework for evaluating the outputs of a systematic platform. Sharpe ratio, drawdown, '
         'benchmark comparison, signal decay analysis, and walk-forward validation methodology. '
         'Essential reading before reviewing any Vektor strategy output.',
         'DPMs, family office analysts, CIOs, investment committees'),
    ]

    cw=[18*mm, 52*mm, COL_W-18*mm-52*mm-36*mm, 36*mm]
    hrow=[Paragraph(h,s['tbl_hdr']) for h in ['REF','DOCUMENT','DESCRIPTION','RECOMMENDED FOR']]
    rows=[hrow]
    for ref,title,desc,aud in papers:
        rows.append([
            Paragraph(ref,s['ref']),
            Paragraph(title,s['title']),
            Paragraph(desc,s['desc']),
            Paragraph(aud,s['audience']),
        ])

    t=Table(rows,colWidths=cw,repeatRows=1,splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD_BG,colors.HexColor('#0F0F14')]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
        ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MIN),
        ('LINEAFTER',(1,0),(1,-1),0.3,RULE_MIN),
        ('LINEAFTER',(2,0),(2,-1),0.3,RULE_MIN),
    ]))
    story.append(t)
    story.append(Spacer(1,12))
    story.append(HRule(COL_W,GOLD,0.8,4,6))
    story.append(Spacer(1,6))
    story.append(Paragraph(
        'All white papers available at investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  '
        'For professional and institutional enquiries only',
        s['wp_ref']))

    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    r=subprocess.run(['pdfinfo',out],capture_output=True,text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l or 'File' in l: print(l)

if __name__=='__main__': build()
