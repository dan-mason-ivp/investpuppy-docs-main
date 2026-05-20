"""
Internal Document Journey Guide — full branded ReportLab rebuild.
Includes all FMP additions: 43 files, FMP in inventory, Stage 4, Stage 7, quick reference.
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
STAGE_BG  = colors.HexColor('#131318')

W, H = A4
ML = MR = 22*mm
MT1 = 16*mm; MT2 = 46*mm; MB = 20*mm
COL_W = W - ML - MR
LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png')
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')
IP_H_RATIO = 2.337
DATE = 'May 2026'
SUB  = 'Document Journey Guide'
FOOTER = f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  VEKTOR  \u00b7  INTERNAL USE ONLY  \u00b7  {DATE}'

def S():
    s = {}
    s['tag'] = ParagraphStyle('tag', fontName='Helvetica', fontSize=7,
        textColor=WARM_GREY, leading=11, spaceAfter=4, letterSpacing=4)
    s['sec_title'] = ParagraphStyle('sec_title', fontName='Helvetica-Bold',
        fontSize=16, textColor=PLATINUM, leading=22, spaceAfter=5)
    s['sec_lead'] = ParagraphStyle('sec_lead', fontName='Helvetica-Oblique',
        fontSize=10, textColor=WARM_GREY, leading=16, spaceAfter=10, alignment=TA_JUSTIFY)
    s['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5,
        textColor=OFF_WHITE, leading=17, spaceAfter=8, alignment=TA_JUSTIFY)
    s['body_grey'] = ParagraphStyle('body_grey', fontName='Helvetica', fontSize=9.5,
        textColor=WARM_GREY, leading=17, spaceAfter=8, alignment=TA_JUSTIFY)
    s['mono'] = ParagraphStyle('mono', fontName='Courier', fontSize=8,
        textColor=WARM_GREY, leading=12)
    s['tbl_hdr'] = ParagraphStyle('tbl_hdr', fontName='Helvetica-Bold',
        fontSize=7.5, textColor=PLATINUM, leading=11)
    s['tbl_name'] = ParagraphStyle('tbl_name', fontName='Helvetica-Bold',
        fontSize=8.5, textColor=OFF_WHITE, leading=12)
    s['tbl_body'] = ParagraphStyle('tbl_body', fontName='Helvetica', fontSize=8.5,
        textColor=OFF_WHITE, leading=12, alignment=TA_JUSTIFY)
    s['tbl_mono'] = ParagraphStyle('tbl_mono', fontName='Courier', fontSize=7.5,
        textColor=WARM_GREY, leading=11)
    s['stage_n'] = ParagraphStyle('stage_n', fontName='Helvetica-Bold',
        fontSize=7, textColor=GOLD, leading=10, letterSpacing=2, spaceAfter=2)
    s['stage_title'] = ParagraphStyle('stage_title', fontName='Helvetica-Bold',
        fontSize=14, textColor=PLATINUM, leading=18, spaceAfter=2)
    s['stage_sub'] = ParagraphStyle('stage_sub', fontName='Helvetica-Oblique',
        fontSize=9, textColor=WARM_GREY, leading=13)
    s['action_label'] = ParagraphStyle('action_label', fontName='Helvetica-Bold',
        fontSize=7.5, textColor=GOLD, leading=11, alignment=TA_CENTER)
    s['goal'] = ParagraphStyle('goal', fontName='Helvetica-Oblique', fontSize=9,
        textColor=WARM_GREY, leading=14, spaceAfter=6, alignment=TA_JUSTIFY)
    s['rule_title'] = ParagraphStyle('rule_title', fontName='Helvetica-Bold',
        fontSize=10, textColor=GOLD, leading=15, spaceAfter=4, spaceBefore=12)
    s['footer'] = ParagraphStyle('footer', fontName='Helvetica', fontSize=6.5,
        textColor=colors.HexColor('#444440'), alignment=TA_CENTER, leading=10)
    s['wp_ref'] = ParagraphStyle('wp_ref', fontName='Helvetica', fontSize=7.5,
        textColor=colors.HexColor('#555550'), alignment=TA_CENTER, leading=11)
    s['tbl_group'] = ParagraphStyle('tbl_group', fontName='Helvetica-Bold',
        fontSize=7.5, textColor=GOLD, leading=11, spaceAfter=4, letterSpacing=2)
    s['new_tag'] = ParagraphStyle('new_tag', fontName='Helvetica-Bold',
        fontSize=8.5, textColor=GOLD, leading=12)
    return s


class HRule(Flowable):
    def __init__(self, w, c=RULE_MIN, t=0.5, sa=4, sb=4):
        Flowable.__init__(self)
        self.rw=w; self.c=c; self.t=t; self._sa=sa; self._sb=sb
        self.height=sa+t+sb
    def wrap(self, aw, ah): return self.rw, self.height
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        self.canv.line(0, self._sb+self.t/2, self.rw, self._sb+self.t/2)


class NoteBox(Flowable):
    def __init__(self, w, text, style, bg=NOTE_BG, bar=RULE_MAJ, ph=14, pv=12, bw=4):
        Flowable.__init__(self)
        self._w=w; self.bg=bg; self.bar=bar; self.ph=ph; self.pv=pv; self.bw=bw
        self._p=Paragraph(text, style); self._iw=w-bw-ph*2
    def wrap(self, aw, ah):
        _, h = self._p.wrap(self._iw, ah)
        self.height=h+self.pv*2; return self._w, self.height
    def draw(self):
        c=self.canv; c.saveState()
        c.setFillColor(self.bg); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0,0,self._w,self.height,3,fill=1,stroke=1)
        c.setFillColor(self.bar); c.roundRect(0,0,self.bw,self.height,2,fill=1,stroke=0)
        self._p.wrap(self._iw,self.height); self._p.drawOn(c,self.bw+self.ph,self.pv)
        c.restoreState()


class StageCard(Flowable):
    """Stage header card."""
    def __init__(self, w, stage_num, title, subtitle, s):
        Flowable.__init__(self)
        self._w=w; self._s=s
        self._pn=Paragraph(f'STAGE {stage_num}', s['stage_n'])
        self._pt=Paragraph(title, s['stage_title'])
        self._ps=Paragraph(subtitle, s['stage_sub'])
        self._pad=10
    def wrap(self, aw, ah):
        inner=self._w-self._pad*2
        _,hn=self._pn.wrap(inner,ah); _,ht=self._pt.wrap(inner,ah); _,hs=self._ps.wrap(inner,ah)
        self.height=hn+ht+hs+self._pad*2+4; return self._w,self.height
    def draw(self):
        c=self.canv; c.saveState()
        c.setFillColor(STAGE_BG); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0,0,self._w,self.height,3,fill=1,stroke=1)
        c.setFillColor(GOLD); c.setLineWidth(3)
        c.line(0,self.height-1.5,self._w,self.height-1.5)
        x=self._pad; y=self.height-self._pad; inner=self._w-self._pad*2
        _,h=self._pn.wrap(inner,self.height); y-=h; self._pn.drawOn(c,x,y); y-=2
        _,h=self._pt.wrap(inner,self.height); y-=h; self._pt.drawOn(c,x,y); y-=2
        _,h=self._ps.wrap(inner,self.height); y-=h; self._ps.drawOn(c,x,y)
        c.restoreState()


def inv_table(headers, rows, col_widths, s):
    hrow=[Paragraph(h,s['tbl_hdr']) for h in headers]
    data=[hrow]+rows
    t=Table(data,colWidths=col_widths,repeatRows=1,splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD_BG,colors.HexColor('#0F0F14')]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
        ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MIN),
        ('LINEAFTER',(1,0),(1,-1),0.3,RULE_MIN),
    ]))
    return t


def stage_doc_table(rows, s):
    cw=[20*mm,42*mm,38*mm,COL_W-100*mm]
    hrow=[Paragraph(h,s['tbl_hdr']) for h in ['ACTION','DOCUMENT','FILENAME','NOTES']]
    data=[hrow]+rows
    t=Table(data,colWidths=cw,repeatRows=1,splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD_BG,colors.HexColor('#0F0F14')]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
        ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
        ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MIN),
        ('LINEAFTER',(1,0),(1,-1),0.3,RULE_MIN),
        ('LINEAFTER',(2,0),(2,-1),0.3,RULE_MIN),
    ]))
    return t


def action(label, s): return Paragraph(label, s['action_label'])
def doc_name(name, s): return Paragraph(name, s['tbl_name'])
def fn(name, s): return Paragraph(name, s['tbl_mono'])
def notes(text, s): return Paragraph(text, s['tbl_body'])


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    from reportlab.lib.utils import ImageReader
    try:
        img=ImageReader(LOGO); iw,ih=img.getSize()
        lw=min(W*0.62,320); lh=lw*ih/iw; lx=(W-lw)/2; ly=H*0.52
        canvas.drawImage(LOGO,lx,ly-lh,lw,lh,mask='auto',preserveAspectRatio=True)
        ry=ly-lh-14
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8)
        canvas.line(ML,ry,W-MR,ry)
        canvas.setFont('Helvetica',7); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2,ry-14,'INTERNAL USE ONLY')
        canvas.setFont('Helvetica-Bold',24); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2,ry-46,'Document Journey Guide')
        canvas.setFont('Helvetica',10); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2,ry-68,
            'The complete Vektor document suite \u2014 what each document is, when to use it,')
        canvas.drawCentredString(W/2,ry-82,
            'who it is for, and how it fits the Founding Mandate sales journey.')
    except Exception as e: print(e)
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4)
    canvas.line(ML,36*mm,W-MR,36*mm)
    canvas.setFont('Helvetica-Bold',7.5); canvas.setFillColor(GOLD)
    canvas.drawCentredString(W/2,28*mm,'NOT FOR EXTERNAL DISTRIBUTION')
    canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W/2,16*mm,DATE)
    canvas.restoreState()


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    from reportlab.lib.utils import ImageReader
    hy=H-MT2+14
    try:
        img=ImageReader(LOGO); iw,ih=img.getSize()
        lh=22; lw=lh*iw/ih
        canvas.drawImage(LOGO,ML,hy,lw,lh,mask='auto',preserveAspectRatio=True)
    except:
        canvas.setFont('Helvetica-Bold',9); canvas.setFillColor(PLATINUM)
        canvas.drawString(ML,hy+4,'VEKTOR')
    canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawRightString(W-MR,H-MT2+18,f'{SUB}  \u00b7  {doc.page-1:02d}')
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.4)
    canvas.line(ML,H-MT2+8,W-MR,H-MT2+8)
    canvas.setLineWidth(0.3)
    canvas.line(ML,MB-2,W-MR,MB-2)
    ip_w=32*mm; ip_h=ip_w/IP_H_RATIO
    try:
        canvas.drawImage(IP_H,ML,1.0*mm,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawRightString(W-MR,1.0*mm+ip_h/2-2.5,f'investpuppy.com  ·  {DATE}')
    canvas.restoreState()


def para(text,s,st='body'): return Paragraph(text,s[st])
def sp(n=8): return Spacer(1,n)
def hrm(): return HRule(COL_W,RULE_MAJ,1.0,3,5)


def build():
    out='/home/claude/investpuppy/vektor/output/pdf/vk5-internal-document-journey.pdf'
    s=S()
    f_cover=Frame(0,0,W,H,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='cover')
    f_body=Frame(ML,MB,COL_W,H-MT2-MB,id='body')
    doc=BaseDocTemplate(out,pagesize=A4,leftMargin=ML,rightMargin=MR,
        topMargin=MT1,bottomMargin=MB,
        title='Vektor Internal Document Journey Guide',author='InvestPuppy')
    doc.addPageTemplates([
        PageTemplate(id='Cover',frames=[f_cover],onPage=draw_cover),
        PageTemplate(id='Body',frames=[f_body],onPage=draw_page),
    ])
    story=[]
    story.append(Spacer(1,1))
    story.append(NextPageTemplate('Body'))
    story.append(PageBreak())

    # ── PAGE 2: OVERVIEW ──────────────────────────────────────────────────────
    story.append(para('OVERVIEW',s,'tag'))
    # CORRECTED: 43 files
    story.append(NoteBox(COL_W,
        'This guide maps the complete Vektor document suite \u2014 43 files across two naming groups \u2014 '
        'against the seven stages of the Founding Mandate sales journey. For each document: what it is, '
        'when to deploy it, who it is for, and its canonical filename. Internal documents are marked. This '
        'document is not for external distribution.',s['body']))
    story.append(sp(12))
    story.append(para('NAMING CONVENTION',s,'tag'))
    story.append(HRule(COL_W,RULE_MIN,0.3,3,4))

    nc_rows=[
        [Paragraph('vektor-[name].pdf / .docx',s['tbl_mono']),
         Paragraph('Commercial documents, support documents, decks, NDA, internal guides',s['tbl_body'])],
        [Paragraph('wp[00-10]-[name].pdf / .docx',s['tbl_mono']),
         Paragraph('Vektor Research Series white papers (WP-00 index through WP-10)',s['tbl_body'])],
        [Paragraph('vektor-deck[1-5]-[name].pptx',s['tbl_mono']),
         Paragraph('Presentation decks (five decks, each for a specific meeting type)',s['tbl_body'])],
    ]
    t=Table(nc_rows,colWidths=[50*mm,COL_W-50*mm])
    t.setStyle(TableStyle([
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[CARD_BG,colors.HexColor('#0F0F14')]),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
        ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MIN),
    ]))
    story.append(t)
    story.append(PageBreak())

    # ── PAGE 3: FILE INVENTORY ─────────────────────────────────────────────────
    story.append(para('COMPLETE FILE INVENTORY',s,'sec_title'))
    story.append(para('All 43 files in the canonical outputs folder, by category.',s,'sec_lead'))
    cw4=[38*mm,42*mm,62*mm,COL_W-142*mm]

    def inv_row(doc,fn_str,purpose,audience):
        return[Paragraph(doc,s['tbl_name']),Paragraph(fn_str,s['tbl_mono']),
               Paragraph(purpose,s['tbl_body']),Paragraph(audience,s['tbl_body'])]

    story.append(para('COMMERCIAL DOCUMENTS (vektor- prefix, PDF + Word)',s,'tbl_group'))
    comm_rows=[
        inv_row('Vektor at a Glance','vektor-at-a-glance.pdf / .docx',
                'One-page executive overview of the platform','All audiences \u2014 first contact'),
        inv_row('Why Vektor','vektor-why-vektor.pdf / .docx',
                'Commercial argument for systematic portfolio management',
                'DPMs, family office principals'),
        inv_row('The Vektor Brand Story','vektor-brand-story.pdf / .docx',
                'Origin, philosophy, and mission',
                'Founders, principals, cultural fit conversations'),
        inv_row('Platform Brochure','vektor-brochure.pdf / .docx',
                'Full eleven-step platform workflow with screenshots',
                'DPMs, PMs, operations \u2014 anyone evaluating the platform'),
        inv_row('Mutual NDA','vektor-mutual-nda.pdf / .docx',
                'Singapore-law mutual confidentiality agreement',
                'Any counterparty before detailed information sharing'),
        # FMP NEW ENTRY
        [Paragraph('Founding Mandate Programme \u25b6 NEW',s['new_tag']),
         Paragraph('vektor-founding-mandate-programme.pdf',s['tbl_mono']),
         Paragraph('Complete programme specification \u2014 commercial terms, partner obligations, '
                   'slot availability, twelve-month founding period',s['tbl_body']),
         Paragraph('Prospective Founding Mandate partners (post-NDA)',s['tbl_body'])],
    ]
    story.append(inv_table(['DOCUMENT','FILENAME','PURPOSE','PRIMARY AUDIENCE'],
                           comm_rows,cw4,s))
    story.append(sp(8))

    story.append(para('RESEARCH SERIES (wp prefix, PDF; WP-01 to WP-06 also in Word)',s,'tbl_group'))
    res_rows=[
        inv_row('WP-00: Research Series Index','wp00-research-series-index.pdf / .docx',
                'Catalogue of all ten research papers with abstracts',
                'Any reader receiving the white paper series'),
        inv_row('WP-01: Quantitative Portfolio Construction',
                'wp01-quantitative-portfolio-construction.pdf / .docx',
                'Five-stage framework \u2014 universe screening to benchmark validation',
                'DPMs, family office analysts, institutional allocators'),
        inv_row('WP-02: Per-Instrument Signal Optimisation',
                'wp02-signal-optimisation.pdf / .docx',
                'Grid search methodology and XGBoost validation layer',
                'Quant analysts, systematic traders, technical DPMs'),
        inv_row('WP-03: Capital Allocation Precision',
                'wp03-capital-allocation.pdf / .docx',
                'Weights to positions \u2014 lot rounding, cash buffer, efficiency',
                'DPMs, operations teams, family office managers'),
        inv_row('WP-04: Technical Indicator Selection',
                'wp04-indicator-selection.pdf / .docx',
                'Six indicators, grid search, Sharpe objective, overfitting controls',
                'Quant analysts, risk managers'),
        inv_row('WP-05: Multi-Currency Portfolio Infrastructure',
                'wp05-multi-currency.pdf / .docx',
                'FX rate collection, position-level conversion, base currency',
                'Multi-mandate family offices, cross-border DPMs'),
        inv_row('WP-06: Audit Trail & Compliance Architecture',
                'wp06-audit-compliance.pdf / .docx',
                'Three-role model, complete action logging, compliance architecture',
                'Compliance officers, institutional due diligence teams'),
        inv_row('WP-07: Production Infrastructure & Technical Architecture',
                'wp07-technical-architecture.pdf',
                'AWS stack, architecture diagram, decision log, region-agnostic design',
                'CTOs, technical due diligence teams'),
        inv_row('WP-08: AI as Instrument',
                'wp08-ai-ml-philosophy.pdf',
                'ML governance, human approval gates, MAS/SFC/FCA alignment',
                'Compliance officers, risk committees, institutional DD'),
        inv_row('WP-09: Risk & Limitation Disclosure',
                'wp09-risk-disclosure.pdf',
                'Fourteen risks across four categories \u2014 mitigations and roadmap',
                'Due diligence teams, risk committees, compliance officers'),
        inv_row('WP-10: Evaluating Systematic Strategy Performance',
                'wp10-evaluating-performance.pdf',
                'Sharpe, drawdown, benchmark, signal decay, walk-forward validation',
                'DPMs, family office analysts, CIOs'),
    ]
    story.append(inv_table(['DOCUMENT','FILENAME','PURPOSE','PRIMARY AUDIENCE'],
                           res_rows,cw4,s))
    story.append(PageBreak())

    story.append(Spacer(1,0))
    story.append(para('SUPPORT DOCUMENTS (vektor- prefix, PDF)',s,'tbl_group'))
    sup_rows=[
        inv_row('Due Diligence Navigation Guide','vektor-dd-navigation-guide.pdf',
                'Which document answers which question \u2014 13-step reading sequence',
                'Founding Mandate partners, institutional DD teams'),
        inv_row('FAQ \u2014 Frequently Asked Questions','vektor-faq.pdf',
                '12 plain-language questions and direct answers',
                'DPMs, family office principals, conference contacts'),
        inv_row('Workflow Integration Guide','vektor-workflow-integration-guide.pdf',
                'Replaces / Augments / Unchanged \u2014 task-by-task workflow map',
                'DPMs evaluating Vektor alongside existing infrastructure'),
        inv_row('Website Specification','vektor-website-specification.pdf',
                'Seven-page site specification and Webflow build guide',
                'Internal \u2014 web build team'),
    ]
    story.append(inv_table(['DOCUMENT','FILENAME','PURPOSE','PRIMARY AUDIENCE'],
                           sup_rows,cw4,s))
    story.append(sp(8))

    story.append(para('PRESENTATION DECKS (vektor-deck prefix, PPTX)',s,'tbl_group'))
    deck_rows=[
        inv_row('Deck 1 \u2014 60-Minute Meeting',
                'vektor-deck1-sixty-minute-meeting.pptx',
                '12 slides \u2014 primary sales deck for DPMs and family office principals',
                'DPMs, family office principals'),
        inv_row('Deck 2 \u2014 Technical Deep Dive',
                'vektor-deck2-technical-deep-dive.pptx',
                '14 slides \u2014 quant methodology, architecture, AI governance',
                'Quant analysts, CIOs, technical evaluators'),
        inv_row('Deck 3 \u2014 Institutional Partner',
                'vektor-deck3-institutional-partner.pptx',
                '13 slides \u2014 partnership framing for established institutions',
                'Large DPMs, established family offices'),
        inv_row('Deck 4 \u2014 Lightning Deck',
                'vektor-deck4-lightning-deck.pptx',
                '6 slides \u2014 conference and event first-contact deck',
                'Mixed audience \u2014 conferences, events'),
        inv_row('Deck 5 \u2014 Due Diligence Presentation',
                'vektor-deck5-due-diligence.pptx',
                '9 slides \u2014 governance and risk review for compliance/CTO',
                'Compliance officers, CTOs, risk committees'),
    ]
    story.append(inv_table(['DOCUMENT','FILENAME','PURPOSE','PRIMARY AUDIENCE'],
                           deck_rows,cw4,s))
    story.append(sp(8))

    story.append(para('INTERNAL DOCUMENTS (vektor- prefix, PDF + Word where applicable)',s,'tbl_group'))
    int_rows=[
        inv_row('Internal Document Journey Guide [INTERNAL]',
                'vektor-internal-document-journey.pdf / .docx',
                'This document \u2014 complete suite map and sales journey guide',
                'Internal team only \u2014 not for external distribution'),
        inv_row('Brand Build Specification [INTERNAL]',
                'vektor-brand-build-specification.pdf / .docx',
                'Brand system specification \u2014 colours, typography, components',
                'Internal team, design partners'),
    ]
    story.append(inv_table(['DOCUMENT','FILENAME','PURPOSE','PRIMARY AUDIENCE'],
                           int_rows,cw4,s))
    story.append(PageBreak())

    # ── PAGE 5+: SALES JOURNEY ─────────────────────────────────────────────────
    story.append(Spacer(1,0))
    story.append(para('THE FOUNDING MANDATE SALES JOURNEY',s,'sec_title'))
    story.append(para('Seven stages from cold outreach to signed mandate \u2014 with the right document for every moment.',s,'sec_lead'))
    story.append(NoteBox(COL_W,
        'The DD Navigation Guide (vektor-dd-navigation-guide.pdf) is the external-facing version of this '
        'journey map. This internal guide goes deeper \u2014 it includes sequencing rationale, talking points, '
        'and internal notes for each stage.',s['body']))
    story.append(sp(10))

    def stage(num, title, sub, rows, also, goal, story, s):
        story.append(StageCard(COL_W, num, title, sub, s))
        story.append(sp(6))
        story.append(stage_doc_table(rows, s))
        if also:
            story.append(sp(6))
            story.append(NoteBox(COL_W, also, s['body_grey']))
        story.append(sp(4))
        story.append(para(f'<i>Goal: {goal}</i>', s, 'goal'))
        story.append(sp(10))

    # Stage 1
    stage(1,'COLD OUTREACH','First contact \u2014 no prior relationship',[
        [action('SEND',s), doc_name('Vektor at a Glance',s),
         fn('vektor-at-a-glance.pdf',s),
         notes('One page. Establishes what Vektor is and the Founding Mandate concept. Low commitment ask \u2014 easy to forward.',s)],
    ],
    'Also available: Deck 4 (Lightning Deck) if presenting at a conference or event. FAQ as an optional attachment if the contact has asked a question the At a Glance does not answer.',
    'one follow-up meeting. Do not send more than one document at this stage \u2014 information overload kills first contact.',
    story, s)

    # Stage 2
    stage(2,'FIRST TOUCH MEETING','Interest established \u2014 30-minute intro call',[
        [action('PRESENT',s), doc_name('Deck 4 \u2014 Lightning Deck',s),
         fn('vektor-deck4-lightning-deck.pptx',s),
         notes('6 slides. Commercial argument and Founding Mandate proposition. Designed to fit a 20-minute slot with 10 minutes for questions.',s)],
        [action('LEAVE BEHIND',s), doc_name('Vektor at a Glance',s),
         fn('vektor-at-a-glance.pdf',s),
         notes('The one-pager they take away. Simple, scannable, shareable.',s)],
        [action('LEAVE BEHIND',s), doc_name('FAQ',s),
         fn('vektor-faq.pdf',s),
         notes('12 plain-language answers to the questions that always come up. Useful for contacts who need to brief a colleague or principal.',s)],
    ],
    'Goal: 60-minute follow-up meeting with the decision-maker. Qualify: are they a DPM, family office, or emerging manager? Which deck is correct for the 60-minute meeting?',
    '60-minute follow-up meeting with the decision-maker.',
    story, s)

    story.append(PageBreak())
    story.append(Spacer(1,0))

    # Stage 3
    stage(3,'60-MINUTE SALES MEETING','Decision-maker in the room',[
        [action('PRESENT',s), doc_name('Deck 1 \u2014 60-Minute Meeting',s),
         fn('vektor-deck1-sixty-minute-meeting.pptx',s),
         notes('12 slides. Full platform story, workflow integration map, risk honesty slide, Founding Mandate proposition. Sequenced: context \u2192 platform \u2192 workflow fit \u2192 risks \u2192 FMP.',s)],
        [action('LEAVE BEHIND',s), doc_name('Platform Brochure',s),
         fn('vektor-brochure.pdf',s),
         notes("The full workflow with screenshots. Best read after the meeting when the context from the presentation is fresh.",s)],
        [action('LEAVE BEHIND',s), doc_name('Why Vektor',s),
         fn('vektor-why-vektor.pdf',s),
         notes('The commercial argument in full. For the principal who wants the reasoning, not just the features.',s)],
        [action('OPTIONAL',s), doc_name('Workflow Integration Guide',s),
         fn('vektor-workflow-integration-guide.pdf',s),
         notes("If the conversation has gone deep on 'how does this fit my workflow?' \u2014 send this as a follow-up within 24 hours.",s)],
    ],
    "Also available: If the meeting involves a quant analyst or CIO alongside the principal, have Deck 2 (Technical Deep Dive) available as a pivot.",
    "NDA signed and a second meeting scoped. At this stage the partner should receive the mutual NDA.",
    story, s)

    # Stage 4 — FMP added
    stage(4,'SERIOUS CONVERSATION','NDA signed \u2014 substantive due diligence begins',[
        [action('SEND',s), doc_name('Mutual NDA',s),
         fn('vektor-mutual-nda.pdf',s),
         notes('Singapore law primary. Must be reviewed by qualified Singapore solicitor before use. Do not send unsigned.',s)],
        [action('SEND',s), doc_name('Founding Mandate Programme',s),
         fn('vektor-founding-mandate-programme.pdf',s),
         notes('Send at this stage \u2014 the first time commercial terms and programme structure are discussed in detail. Reference: IP-FMP-260501-1.0.',s)],
        [action('SEND',s), doc_name('DD Navigation Guide',s),
         fn('vektor-dd-navigation-guide.pdf',s),
         notes('Send with the full white paper suite. Tells the partner which document to read in response to which question. The 13-step recommended sequence is the reading roadmap.',s)],
        [action('SEND',s), doc_name('WP-01: Portfolio Construction',s),
         fn('wp01-quantitative-portfolio-construction.pdf',s),
         notes('The foundational methodology paper. Should be read first in the white paper series.',s)],
        [action('SEND',s), doc_name('WP-09: Risk Disclosure',s),
         fn('wp09-risk-disclosure.pdf',s),
         notes('Send proactively \u2014 do not wait to be asked. Intellectual honesty at this stage builds trust faster than any feature demonstration.',s)],
        [action('SEND',s), doc_name('WP-10: Evaluating Performance',s),
         fn('wp10-evaluating-performance.pdf',s),
         notes('Gives the partner the vocabulary to evaluate strategy outputs. Read before any strategy demonstration.',s)],
    ],
    'Also available: Send the full Research Series (WP-01 through WP-10) with the DD Navigation Guide as the cover document. The partner reads in the sequence that matches their questions.',
    'due diligence meeting scoped \u2014 either Deck 2 (technical) or Deck 5 (governance/compliance) depending on who is doing the DD.',
    story, s)

    story.append(PageBreak())
    story.append(Spacer(1,0))

    # Stage 5
    stage(5,'TECHNICAL DUE DILIGENCE','Quant analyst, CIO, or CTO in the room',[
        [action('PRESENT',s), doc_name('Deck 2 \u2014 Technical Deep Dive',s),
         fn('vektor-deck2-technical-deep-dive.pptx',s),
         notes('14 slides. Quantitative methodology, architecture diagram, AI governance, performance evaluation framework. For quant analysts and CIOs evaluating the engine.',s)],
        [action('REFERENCE',s), doc_name('WP-02 through WP-04',s),
         fn('wp02 / wp03 / wp04',s),
         notes('Signal optimisation, capital allocation, indicator selection. Have these available for deep dives on specific methodology questions.',s)],
        [action('REFERENCE',s), doc_name('WP-07: Technical Architecture',s),
         fn('wp07-technical-architecture.pdf',s),
         notes('AWS stack, architecture diagram, decision log. For CTOs and technical evaluators.',s)],
        [action('REFERENCE',s), doc_name('WP-10: Evaluating Performance',s),
         fn('wp10-evaluating-performance.pdf',s),
         notes("If the CIO asks 'how do I evaluate this?' \u2014 the performance evaluation slide in Deck 2 covers this, and WP-10 is the full reference.",s)],
    ],
    None,
    'technical sign-off from the quant/CTO stakeholder. Compliance/governance review is the next stage if not concurrent.',
    story, s)

    # Stage 6
    stage(6,'COMPLIANCE & GOVERNANCE REVIEW','Compliance officer, risk committee, or legal counsel',[
        [action('PRESENT',s), doc_name('Deck 5 \u2014 Due Diligence Presentation',s),
         fn('vektor-deck5-due-diligence.pptx',s),
         notes('9 slides. Leads with audit trail and human approval gates. AI governance. Risk summary. Regulatory alignment (MAS/SFC/FCA). Designed for compliance officers and risk committees \u2014 not a sales deck.',s)],
        [action('REFERENCE',s), doc_name('WP-06: Audit Trail & Compliance',s),
         fn('wp06-audit-compliance.pdf',s),
         notes('The detailed compliance architecture. Compliance officers should read this in full.',s)],
        [action('REFERENCE',s), doc_name('WP-08: AI as Instrument',s),
         fn('wp08-ai-ml-philosophy.pdf',s),
         notes('AI governance and regulatory alignment. MAS FEAT / SFC TM-G-1 / PRA SS1/23 references included.',s)],
        [action('REFERENCE',s), doc_name('WP-09: Risk Disclosure',s),
         fn('wp09-risk-disclosure.pdf',s),
         notes('The structured risk analysis. Should already have been sent at Stage 4 \u2014 if not, send before this meeting.',s)],
        [action('REFERENCE',s), doc_name('WP-07: Technical Architecture',s),
         fn('wp07-technical-architecture.pdf',s),
         notes('For the CTO or head of technology attending the governance review. Data residency, security, encryption \u2014 all in Section 7.',s)],
    ],
    None,
    'governance and compliance sign-off from the institutional machinery. Once this is done, the commercial decision is the only remaining gate.',
    story, s)

    story.append(PageBreak())
    story.append(Spacer(1,0))

    # Stage 7 — FMP added
    stage(7,'FOUNDING MANDATE CLOSE','Commercial terms and onboarding',[
        [action('PRESENT',s), doc_name('Deck 3 \u2014 Institutional Partner',s),
         fn('vektor-deck3-institutional-partner.pptx',s),
         notes("13 slides. Partnership framing \u2014 'a different kind of partnership.' Integration architecture. Founding Mandate commercial terms. Designed for the close conversation with the principal.",s)],
        [action('REFERENCE',s), doc_name('Founding Mandate Programme',s),
         fn('vektor-founding-mandate-programme.pdf',s),
         notes('Should already have been read at Stage 4. If not, send before this conversation. The commercial terms, programme obligations, and three-step engagement path are all in this document.',s)],
        [action('REFERENCE',s), doc_name('Brand Story',s),
         fn('vektor-brand-story.pdf',s),
         notes('Optional \u2014 for partners who want to understand the people and philosophy behind the platform before committing.',s)],
        [action('ACTION',s), doc_name('Mutual NDA (if not yet signed)',s),
         fn('vektor-mutual-nda.pdf',s),
         notes('If NDA has not been executed, execute before discussing specific commercial terms.',s)],
    ],
    'At this stage the partner has completed due diligence. The conversation is about terms, configuration, and onboarding timeline. Deck 3 frames this as a partnership, not a purchase.',
    'signed Founding Mandate agreement. Onboarding scoped. Platform configuration begins.',
    story, s)

    # ── DEPLOYMENT RULES ──────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Spacer(1,0))
    story.append(para('DEPLOYMENT RULES',s,'sec_title'))
    story.append(para('Standing instructions for document distribution.',s,'sec_lead'))
    story.append(hrm())

    rules=[
        ('Never send more than the stage requires',
         'Information overload at the wrong stage is a sales killer. The cold outreach stage sends one document. The serious conversation stage sends the full suite with a navigation guide. Every document has a stage. Respect the sequence.'),
        ('Always send WP-09 before asking for a decision',
         'Risk disclosure sent proactively signals intellectual honesty. Risk disclosure sent in response to a question signals defensiveness. Send WP-09 at Stage 4, without being asked.'),
        ('Always send the Founding Mandate Programme document at Stage 4',
         'The FMP (vektor-founding-mandate-programme.pdf) is the first document that defines commercial terms and programme obligations in full. It should be sent when the NDA is signed, not withheld until Stage 7. A partner who arrives at Stage 7 without having read the FMP is unprepared for the close conversation.'),
        ('The DD Navigation Guide always accompanies the white paper suite',
         'Never send ten white papers without the navigation guide. A partner who receives the full suite without the guide faces an orientation problem. The guide converts it into a reading journey.'),
        ('Internal documents are never distributed externally',
         'vektor-internal-document-journey.pdf and vektor-brand-build-specification.pdf are internal only. They are not referenced in any external document.'),
        ('The Mutual NDA must be reviewed by a Singapore solicitor before use',
         'This is stated in the NDA itself and repeated here. Do not use the NDA as a live document without qualified legal review.'),
        ('Deck selection follows audience, not preference',
         'Deck 1: DPM/principal. Deck 2: quant/CIO/CTO. Deck 3: institutional partner close. Deck 4: conference/event. Deck 5: compliance/governance. Using the wrong deck for the wrong audience undermines credibility.'),
    ]
    for title, body in rules:
        story.append(para(title, s, 'rule_title'))
        story.append(para(body, s))

    # ── QUICK REFERENCE ───────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Spacer(1,0))
    story.append(para('QUICK REFERENCE \u2014 DOCUMENT BY AUDIENCE',s,'sec_title'))
    story.append(para('If you know the audience but not the stage.',s,'sec_lead'))
    story.append(hrm())

    qa_rows=[
        [Paragraph('DPM / Portfolio Manager',s['tbl_name']),
         Paragraph('At a Glance \u2192 Brochure \u2192 Why Vektor \u2192 Deck 1 \u2192 FMP \u2192 WP-01, WP-02, WP-03',s['tbl_body'])],
        [Paragraph('Family Office Principal',s['tbl_name']),
         Paragraph('At a Glance \u2192 FAQ \u2192 Deck 1 \u2192 FMP \u2192 Brand Story \u2192 WP-09 \u2192 Deck 3',s['tbl_body'])],
        [Paragraph('Quant Analyst / CIO',s['tbl_name']),
         Paragraph('WP-01 \u2192 WP-02 \u2192 WP-04 \u2192 WP-10 \u2192 Deck 2 \u2192 WP-07',s['tbl_body'])],
        [Paragraph('Compliance Officer',s['tbl_name']),
         Paragraph('WP-06 \u2192 WP-08 \u2192 WP-09 \u2192 Deck 5',s['tbl_body'])],
        [Paragraph('CTO / Head of Technology',s['tbl_name']),
         Paragraph('WP-07 \u2192 Deck 2 (architecture slides) \u2192 Deck 5',s['tbl_body'])],
        [Paragraph('Risk Committee',s['tbl_name']),
         Paragraph('WP-09 \u2192 WP-08 \u2192 WP-06 \u2192 Deck 5',s['tbl_body'])],
        [Paragraph('Conference / Event Contact',s['tbl_name']),
         Paragraph('Deck 4 \u2192 At a Glance \u2192 FAQ',s['tbl_body'])],
        [Paragraph('Legal Counsel',s['tbl_name']),
         Paragraph('Mutual NDA \u2192 WP-06 \u2192 WP-09',s['tbl_body'])],
    ]
    qa_t=Table(qa_rows,colWidths=[50*mm,COL_W-50*mm],splitByRow=1)
    qa_t.setStyle(TableStyle([
        ('ROWBACKGROUNDS',(0,0),(-1,-1),[CARD_BG,colors.HexColor('#0F0F14')]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
        ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MIN),
    ]))
    story.append(qa_t)
    story.append(sp(14))
    story.append(HRule(COL_W,RULE_MAJ,1.0,4,4))
    story.append(sp(6))
    # CORRECTED: 43 files
    story.append(para(
        'This document should be updated whenever a new document is added to the suite or a document is revised. '
        'Current version: May 2026. <b>43 files. 7 stages.</b> NOT FOR EXTERNAL DISTRIBUTION.',
        s,'body_grey'))
    story.append(sp(8))
    story.append(para(
        f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  Internal use only  \u00b7  Copyright 2026 InvestPuppy',
        s,'wp_ref'))

    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    r=subprocess.run(['pdfinfo',out],capture_output=True,text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l or 'File' in l: print(l)

if __name__=='__main__': build()
