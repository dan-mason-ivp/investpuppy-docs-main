"""
Brand & Build Specification — full branded ReportLab rebuild.
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

W, H = A4
ML = MR = 22*mm
MT1 = 16*mm; MT2 = 46*mm; MB = 20*mm
COL_W = W - ML - MR
LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png')
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')
IP_H_RATIO = 2.337
DATE = 'May 2026'
DOC_TITLE = 'Brand & Build Specification'
SUB = 'Brand & Build Specification'
FOOTER = f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  Internal Use Only \u2014 Not for Distribution  \u00b7  {DATE}'

def S():
    s = {}
    s['tag'] = ParagraphStyle('tag', fontName='Helvetica', fontSize=7,
        textColor=WARM_GREY, leading=11, spaceAfter=4, letterSpacing=4)
    s['sec_num'] = ParagraphStyle('sec_num', fontName='Helvetica-Bold',
        fontSize=64, textColor=colors.HexColor('#1E1E24'), leading=64)
    s['sec_title'] = ParagraphStyle('sec_title', fontName='Helvetica-Bold',
        fontSize=18, textColor=PLATINUM, leading=24, spaceAfter=4, spaceBefore=0)
    s['sec_lead'] = ParagraphStyle('sec_lead', fontName='Helvetica',
        fontSize=10, textColor=WARM_GREY, leading=16, spaceAfter=10)
    s['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5,
        textColor=OFF_WHITE, leading=17, spaceAfter=8, alignment=TA_JUSTIFY)
    s['body_grey'] = ParagraphStyle('body_grey', fontName='Helvetica', fontSize=9.5,
        textColor=WARM_GREY, leading=17, spaceAfter=8, alignment=TA_JUSTIFY)
    s['sub_head'] = ParagraphStyle('sub_head', fontName='Helvetica-Bold',
        fontSize=9, textColor=GOLD, leading=14, spaceAfter=5, spaceBefore=14, letterSpacing=1)
    s['code'] = ParagraphStyle('code', fontName='Courier', fontSize=8,
        textColor=colors.HexColor('#B8C0CC'), leading=13, spaceAfter=4)
    s['code_label'] = ParagraphStyle('code_label', fontName='Courier', fontSize=8,
        textColor=GOLD, leading=13, spaceAfter=4)
    s['tbl_hdr'] = ParagraphStyle('tbl_hdr', fontName='Helvetica-Bold',
        fontSize=7.5, textColor=PLATINUM, leading=11)
    s['tbl_mono'] = ParagraphStyle('tbl_mono', fontName='Courier', fontSize=8,
        textColor=WARM_GREY, leading=12)
    s['tbl_mono_gold'] = ParagraphStyle('tbl_mono_gold', fontName='Courier', fontSize=8,
        textColor=GOLD, leading=12)
    s['tbl_body'] = ParagraphStyle('tbl_body', fontName='Helvetica', fontSize=8.5,
        textColor=OFF_WHITE, leading=12, alignment=TA_JUSTIFY)
    s['tbl_name'] = ParagraphStyle('tbl_name', fontName='Helvetica-Bold',
        fontSize=8.5, textColor=OFF_WHITE, leading=12)
    s['contents_num'] = ParagraphStyle('contents_num', fontName='Helvetica-Bold',
        fontSize=11, textColor=PLATINUM, leading=15)
    s['contents_title'] = ParagraphStyle('contents_title', fontName='Helvetica',
        fontSize=11, textColor=WARM_GREY, leading=15)
    s['critical_title'] = ParagraphStyle('critical_title', fontName='Helvetica-Bold',
        fontSize=8, textColor=GOLD, leading=12, letterSpacing=2, spaceAfter=4, spaceBefore=10)
    s['footer'] = ParagraphStyle('footer', fontName='Helvetica', fontSize=6.5,
        textColor=colors.HexColor('#444440'), alignment=TA_CENTER, leading=10)
    s['wp_ref'] = ParagraphStyle('wp_ref', fontName='Helvetica', fontSize=7.5,
        textColor=colors.HexColor('#555550'), alignment=TA_CENTER, leading=11)
    s['closing'] = ParagraphStyle('closing', fontName='Helvetica-Oblique', fontSize=10,
        textColor=WARM_GREY, alignment=TA_CENTER, leading=16)
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
        self._p=Paragraph(text,style); self._iw=w-bw-ph*2
    def wrap(self, aw, ah):
        _, h=self._p.wrap(self._iw, ah); self.height=h+self.pv*2; return self._w,self.height
    def draw(self):
        c=self.canv; c.saveState()
        c.setFillColor(self.bg); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0,0,self._w,self.height,3,fill=1,stroke=1)
        c.setFillColor(self.bar); c.roundRect(0,0,self.bw,self.height,2,fill=1,stroke=0)
        self._p.wrap(self._iw,self.height); self._p.drawOn(c,self.bw+self.ph,self.pv)
        c.restoreState()


def dark_table(headers, rows, col_widths, s):
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


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    # Top banner
    bh=22; by=H-MB-bh
    canvas.setFillColor(colors.HexColor('#0D0C0A'))
    canvas.setStrokeColor(GOLD); canvas.setLineWidth(1.0)
    canvas.rect(ML, by, COL_W, bh, fill=1, stroke=1)
    canvas.setFont('Helvetica-Bold',7.5); canvas.setFillColor(GOLD)
    canvas.drawCentredString(W/2, by+7, 'INTERNAL USE ONLY \u2014 NOT FOR DISTRIBUTION')
    # Logo - centered, smaller
    from reportlab.lib.utils import ImageReader
    try:
        img=ImageReader(LOGO); iw,ih=img.getSize()
        lw=min(W*0.42,200); lh=lw*ih/iw; lx=(W-lw)/2; ly=H*0.54
        canvas.drawImage(LOGO,lx,ly-lh,lw,lh,mask='auto',preserveAspectRatio=True)
        ry=ly-lh-10
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8)
        canvas.line(ML,ry,W-MR,ry)
        canvas.setFont('Helvetica',7); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2,ry-14,'INTERNAL REFERENCE')
        canvas.setFont('Helvetica-Bold',28); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2,ry-48,'Brand & Build Specification')
        canvas.setFont('Helvetica',10); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2,ry-72,
            'The complete reference for rebuilding the Vektor document suite in any future session \u2014')
        canvas.drawCentredString(W/2,ry-86,
            'brand rules, colour values, component specifications, margin decisions, and standing panel rulings.')
    except Exception as e: print(e)
    # Contents table on cover
    cy=H*0.28
    contents=[
        ('01','Purpose of This Document'),('02','The Canonical Colour Palette'),
        ('03','Typographic Hierarchy'),('04','Page Layout & Margins'),
        ('05','Component Specifications'),('06','Document Register'),
        ('07','File Structure & Dependencies'),('08','Standing Panel Decisions'),
        ('09','Rebuild Instructions'),('10','Quick Reference \u2014 Key Values'),
    ]
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.3)
    row_h=16; tbl_w=COL_W*0.72; tx=(W-tbl_w)/2
    for i,(num,title) in enumerate(contents):
        y=cy-i*row_h
        canvas.setFillColor(CARD_BG if i%2==0 else colors.HexColor('#0F0F14'))
        canvas.rect(tx,y-3,tbl_w,row_h,fill=1,stroke=0)
        canvas.line(tx,y-3,tx+tbl_w,y-3)
        canvas.setFont('Helvetica-Bold',9); canvas.setFillColor(PLATINUM)
        canvas.drawString(tx+8,y+5,num)
        canvas.setFont('Helvetica',9); canvas.setFillColor(WARM_GREY)
        canvas.drawString(tx+30,y+5,title)
    canvas.setStrokeColor(CARD_EDGE); canvas.setLineWidth(0.4)
    canvas.rect(tx,cy-len(contents)*row_h-3+row_h,tbl_w,len(contents)*row_h,fill=0,stroke=1)
    # Footer
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4)
    canvas.line(ML,36*mm,W-MR,36*mm)
    canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawCentredString(W/2,28*mm,
        f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  Internal use only  \u00b7  {DATE}')
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


def para(text, s, st='body'): return Paragraph(text, s[st])
def sp(n=8): return Spacer(1,n)
def hrm(): return HRule(COL_W,RULE_MAJ,1.0,3,5)
def hrn(): return HRule(COL_W,RULE_MIN,0.3,3,4)


def section_header(num_str, title, lead, s, story):
    story.append(hrm())
    story.append(para(num_str, s, 'sec_num'))
    story.append(Spacer(1,-16))  # pull title up under number
    story.append(para(title, s, 'sec_title'))
    story.append(para(lead, s, 'sec_lead'))


def build():
    out='/home/claude/investpuppy/vektor/output/pdf/vk5-brand-build-specification.pdf'
    s=S()
    f_cover=Frame(0,0,W,H,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='cover')
    f_body=Frame(ML,MB,COL_W,H-MT2-MB,id='body')
    doc=BaseDocTemplate(out,pagesize=A4,leftMargin=ML,rightMargin=MR,
        topMargin=MT1,bottomMargin=MB,
        title='Vektor Brand & Build Specification',author='InvestPuppy')
    doc.addPageTemplates([
        PageTemplate(id='Cover',frames=[f_cover],onPage=draw_cover),
        PageTemplate(id='Body',frames=[f_body],onPage=draw_page),
    ])
    story=[]
    story.append(Spacer(1,1))
    story.append(NextPageTemplate('Body'))
    story.append(PageBreak())

    # ── 01 PURPOSE ────────────────────────────────────────────────────────────
    section_header('01','Purpose of This Document','Why this document exists and how to use it.',s,story)
    story.append(para(
        'This document captures every decision made during the development of the Vektor document library \u2014 brand '
        'rules, colour values, component specifications, typographic hierarchy, margin decisions, and the standing '
        'rulings of the Delphi advisory panel. It exists for one purpose: so that any future Claude session, starting '
        'from scratch with no memory of previous conversations, can rebuild any document in the Vektor suite with full '
        'consistency.',s))
    story.append(para(
        'Without this document, a new session will produce documents that are competent but not consistent. Small '
        'differences in spacing, colour application, or component styling will accumulate and break the coherence the '
        'panel worked to establish across twelve documents.',s))
    story.append(NoteBox(COL_W,
        "How to use this document: paste the contents of this file into a new Claude session along with the build "
        "scripts listed in Section 07. Say: 'Please rebuild [document name] using these brand specifications and "
        "build scripts.' The session will have everything it needs to produce a consistent result.",s['body_grey']))
    story.append(PageBreak())

    # ── 02 COLOUR PALETTE ─────────────────────────────────────────────────────
    section_header('02','The Canonical Colour Palette',
        'Three colours. Each one earns its place. These hex values are fixed.',s,story)
    colour_rows=[
        [para('Near-black',s,'tbl_name'),para('#0A0A0F',s,'tbl_mono'),para('BG',s,'tbl_mono'),
         para('Primary page background (PDF). Canonical dark ground. Word docs: C.DARK_H = \u20180A0A0F\u2019 for dark table headers.',s,'tbl_body')],
        [para('Platinum',s,'tbl_name'),para('#E8E8EC',s,'tbl_mono'),para('PLATINUM',s,'tbl_mono'),
         para('Primary mark colour. All letterforms in the Vektor logo. Section title text in PDFs.',s,'tbl_body')],
        [para('Amber Gold',s,'tbl_name'),para('#C8A96E',s,'tbl_mono'),para('GOLD',s,'tbl_mono'),
         para('Accent. Single use in primary mark: arrowhead strokes only. In docs: tags, metric numbers, gold rules, card top bars. NEVER decorative.',s,'tbl_body')],
        [para('Off-white',s,'tbl_name'),para('#E8E2D9',s,'tbl_mono'),para('OFF_WHITE',s,'tbl_mono'),
         para('Body text in PDFs (on dark bg). Maps to #1A1A1F in Word (white bg).',s,'tbl_body')],
        [para('Warm grey',s,'tbl_name'),para('#9A9086',s,'tbl_mono'),para('WARM_GREY',s,'tbl_mono'),
         para('Secondary text, captions, sub-labels, footer text, body_grey paragraphs.',s,'tbl_body')],
        [para('Major rule',s,'tbl_name'),para('#5A5A60',s,'tbl_mono'),para('RULE_MAJ',s,'tbl_mono'),
         para('Section divider rules (1.0pt). Platinum-toned. NOT gold \u2014 critical panel ruling.',s,'tbl_body')],
        [para('Minor rule',s,'tbl_name'),para('#2A2828',s,'tbl_mono'),para('RULE_MIN',s,'tbl_mono'),
         para('Thin dividers within sections (0.3\u20130.4pt). Dim grey.',s,'tbl_body')],
        [para('Card bg',s,'tbl_name'),para('#111116',s,'tbl_mono'),para('CARD_BG',s,'tbl_mono'),
         para('Surface for cards, tables, metric blocks in PDFs.',s,'tbl_body')],
        [para('Note bg',s,'tbl_name'),para('#16161A',s,'tbl_mono'),para('NOTE_BG',s,'tbl_mono'),
         para('Surface for NoteBox and aside boxes in PDFs.',s,'tbl_body')],
        [para('Step bg',s,'tbl_name'),para('#131210',s,'tbl_mono'),para('STEP_BG',s,'tbl_mono'),
         para('Metric card surfaces in PDFs.',s,'tbl_body')],
        [para('Card edge',s,'tbl_name'),para('#242428',s,'tbl_mono'),para('CARD_EDGE',s,'tbl_mono'),
         para('Border colour for all card and table edges in PDFs.',s,'tbl_body')],
    ]
    story.append(dark_table(['NAME','HEX','VARIABLE','ROLE & RULES'],colour_rows,
        [24*mm,20*mm,26*mm,COL_W-70*mm],s))
    story.append(sp(8))
    story.append(para('CRITICAL COLOUR RULES \u2014 PANEL DECISIONS',s,'critical_title'))
    story.append(hrn())
    critical_rules=[
        ('Gold appears ONCE in the primary mark.',
         'On the arrowhead strokes only. Not on the V, not on EKTOR, not on the sub-brand. '
         'The moment gold appears on more than one element it becomes decoration.'),
        ('Section rules are platinum-toned, not gold.',
         'RULE_MAJ (#5A5A60) is used for all section dividers. This was a specific panel ruling after the '
         'original gold rule treatment was rejected as contradicting the document\u2019s own colour argument.'),
        ('Sub-headings are warm grey, not platinum.',
         'WARM_GREY (#9A9086) for sub_head style. Platinum is reserved for section_title only. '
         'Platinum sub-heads create a hierarchy collision.'),
        ('Contents block numbers are platinum, not gold.',
         'Gold is not a navigational colour \u2014 this was changed after panel review.'),
        ("The Founder's Note left bar is platinum, not gold.",
         'RULE_MAJ bar colour. Gold bars are reserved for the single closing page rule only.'),
    ]
    for title, body in critical_rules:
        story.append(para(f'<b>{title}</b>',s))
        story.append(para(body,s,'body_grey'))
    story.append(PageBreak())

    # ── 03 TYPOGRAPHIC HIERARCHY ───────────────────────────────────────────────
    section_header('03','Typographic Hierarchy',
        'PDF uses Helvetica (built into ReportLab). Word uses Arial throughout.',s,story)
    story.append(para('PDF DOCUMENTS \u2014 REPORTLAB STYLES',s,'sub_head'))
    type_rows=[
        ['cover_label','Helvetica','7pt','WARM_GREY','Document type tag. Letter spacing 4. ALL CAPS.'],
        ['cover_title','Helvetica-Bold','24pt','PLATINUM','Cover main title. Leading 30.'],
        ['cover_distil','Helvetica-Oblique','11pt','WARM_GREY','Cover distillation. Leading 19. Italic.'],
        ['section_tag','Helvetica','7pt','WARM_GREY','Section number + label. Letter spacing 4. ALL CAPS.'],
        ['section_title','Helvetica-Bold','18pt','PLATINUM','Section headline. Leading 24.'],
        ['section_sub','Helvetica','11pt','WARM_GREY','Section sub-headline. Leading 17.'],
        ['sub_head','Helvetica-Bold','8.5pt','WARM_GREY','Sub-heading. Letter spacing 2. ALL CAPS. SpaceBefore 16pt.'],
        ['body','Helvetica','9.5pt','OFF_WHITE','Body text. Leading 17. Justified.'],
        ['body_grey','Helvetica','9.5pt','WARM_GREY','Secondary body. Leading 17. Justified.'],
        ['wp_section','Helvetica-Bold','14pt','PLATINUM','White paper section heading.'],
        ['wp_subsection','Helvetica-Bold','11pt','GOLD','White paper sub-section heading.'],
        ['wp_lead','Helvetica-Oblique','10pt','WARM_GREY','White paper lead-in italic summary.'],
        ['pull_quote','Helvetica-Oblique','11pt','PLATINUM','Pull quote. Leading 18. Centred.'],
        ['founder_label','Helvetica','7.5pt','GOLD','Founder\'s Note label. Letter spacing 3.5. Sits OUTSIDE and ABOVE box.'],
        ['founder_note','Helvetica-Oblique','10pt','WARM_GREY','Founder\'s Note body. Leading 17.'],
        ['metric_num','Helvetica-Bold','16pt','GOLD','Metric card number. Centred.'],
        ['footer','Helvetica','6.5pt','#444440','Footer text. Centred. All later pages.'],
        ['wp_ref','Helvetica','7.5pt','#555550','Captions, document identifiers.'],
    ]
    tbl_rows=[[Paragraph(r[0],s['tbl_mono']),Paragraph(r[1],s['tbl_body']),
               Paragraph(r[2],s['tbl_body']),Paragraph(r[3],s['tbl_mono']),
               Paragraph(r[4],s['tbl_body'])] for r in type_rows]
    story.append(dark_table(['STYLE','FONT','SIZE','COLOUR','NOTES'],tbl_rows,
        [28*mm,32*mm,14*mm,22*mm,COL_W-96*mm],s))
    story.append(sp(8))
    story.append(para('WORD DOCUMENTS \u2014 ARIAL STYLES',s,'sub_head'))
    story.append(para(
        'All Word documents use Arial. Background is white \u2014 brand identity expressed through colour accents. '
        'Key values (in half-points, 2\u00d7 the point size):',s,'body_grey'))
    word_styles=[
        'Heading 1: Arial Bold 40 half-pts (#1A1A1F), spacing before 280 after 120, outlineLevel 0',
        'Heading 2: Arial Bold 28 half-pts (#1A1A1F), spacing before 240 after 80, outlineLevel 1',
        'Body text: Arial 20 half-pts (#1A1A1F), justified, spacing after 100',
        'Section tags: Arial Bold 14 half-pts (#C8A96E), characterSpacing 80, ALL CAPS',
        'Gold rule: Paragraph border bottom, size 12, color #C8A96E, space 4',
        'Footer: Arial 14 half-pts (#9A9086), gold top border, right tab stop at CONTENT_W',
    ]
    for ws in word_styles:
        story.append(para(f'\u2014 {ws}',s,'body_grey'))
    story.append(PageBreak())

    # ── 04 PAGE LAYOUT ────────────────────────────────────────────────────────
    section_header('04','Page Layout & Margins',
        'All documents use A4. The following constants must not be approximated.',s,story)
    story.append(para('PDF CONSTANTS \u2014 vektor_styles.py',s,'sub_head'))
    for line in [
        'W, H = A4  # 595.27 \u00d7 841.89 points',
        'MARGIN_L = 22*mm  # Left margin',
        'MARGIN_R = 22*mm  # Right margin',
        'MARGIN_T1 = 16*mm  # Cover and first pages',
        'MARGIN_T2 = 46*mm  # Later pages \u2014 WITH PERSISTENT HEADER',
        'MARGIN_B = 20*mm  # Bottom margin',
        'COL_W = W - MARGIN_L - MARGIN_R  # Usable column width',
    ]:
        story.append(para(line,s,'code'))
    story.append(NoteBox(COL_W,
        '<b>CRITICAL: MARGIN_T2 was increased from 38mm to 46mm</b> during the session to fix a header overlap issue. '
        'Any future rebuild MUST use 46mm. Using 38mm will cause the persistent header to collide with the top of the '
        'content frame on all later pages.',s['body']))
    story.append(sp(8))
    story.append(para('THREE PAGE TEMPLATES',s,'sub_head'))
    templates=[
        ('Cover','Frame at (0, 0, W, H) \u2014 full bleed. Dark BG drawn on canvas. Logo centred. No header. No footer rule (closing page uses gold footer rule).'),
        ('First','Frame at (MARGIN_L, MARGIN_B, COL_W, H-MARGIN_T1-MARGIN_B). No persistent header. Footer present.'),
        ('Later','Frame at (MARGIN_L, MARGIN_B, COL_W, H-MARGIN_T2-MARGIN_B). Persistent header drawn at H-MARGIN_T2+14. Footer present.'),
    ]
    for name,desc in templates:
        story.append(para(f'<b>{name}</b>',s))
        story.append(para(desc,s,'body_grey'))
    story.append(sp(6))
    story.append(para('PERSISTENT HEADER \u2014 LATER PAGES',s,'sub_head'))
    for line in [
        '\u2014 Logo: height 22px at (MARGIN_L, H-MARGIN_T2+14). Width scales from PNG aspect ratio.',
        '\u2014 Page subtitle + number: Helvetica 7pt #555550, right-aligned at (W-MARGIN_R, H-MARGIN_T2+18).',
        '\u2014 Separator rule: 0.4pt RULE_MIN, drawn at y=H-MARGIN_T2+8, from MARGIN_L to W-MARGIN_R.',
    ]:
        story.append(para(line,s,'body_grey'))
    story.append(sp(6))
    story.append(para('FOOTER \u2014 ALL PAGES',s,'sub_head'))
    for line in [
        '\u2014 Separator rule: 0.3pt RULE_MIN at y=MARGIN_B-2.',
        '\u2014 Footer text: Helvetica 6.5pt #444440, centred at y=MARGIN_B-11.',
        '\u2014 Format: "Vektor by InvestPuppy \u00b7 investpuppy.com \u00b7 [subtitle] \u00b7 May 2026"',
    ]:
        story.append(para(line,s,'body_grey'))
    story.append(sp(8))
    story.append(para('WORD \u2014 PAGE CONSTANTS',s,'sub_head'))
    for line in [
        'PAGE_W = 11906 DXA (A4 width)',
        'PAGE_H = 16838 DXA (A4 height)',
        'MARGIN = 1134 DXA (~2cm all sides)',
        'CONTENT_W = PAGE_W - MARGIN*2 = 9638 DXA',
    ]:
        story.append(para(line,s,'code'))
    story.append(PageBreak())

    # ── 05 COMPONENT SPECS ────────────────────────────────────────────────────
    section_header('05','Component Specifications',
        'Custom Flowable classes defined in vektor_styles.py. Each must be implemented exactly.',s,story)
    components=[
        ('HRule \u2014 Horizontal Rule',
         'HRule(width, color=RULE_MIN, thickness=0.5, spaceAbove=5, spaceBelow=5)',
         ['\u2014 Major section rule: HRule(COL_W, color=RULE_MAJ, thickness=1.0, spaceAbove=2, spaceBelow=4)',
          '\u2014 Minor section rule: HRule(COL_W, color=RULE_MIN, thickness=0.3, spaceAbove=4, spaceBelow=3)',
          '\u2014 Gold closing rule: HRule(COL_W, color=GOLD, thickness=0.8) \u2014 closing page only']),
        ('NoteBox \u2014 Editorial Aside',
         'NoteBox(width, text, style, bg=NOTE_BG, bar_color=RULE_MAJ, pad_h=15, pad_v=13, bar=4)',
         ['\u2014 Default bar colour: RULE_MAJ (platinum-toned). Gold bars only in specific Why Vektor boxes.',
          '\u2014 Background: NOTE_BG (#16161A). Rounded corners 3pt. CARD_EDGE border 0.4pt.']),
        ('FounderNoteBox',
         'FounderNoteBox(width, text, style, pad_h=16, pad_v=14, bar=4)',
         ['\u2014 Bar colour: RULE_MAJ \u2014 was originally gold, changed to platinum after panel review.',
          '\u2014 Label placement: OUTSIDE and ABOVE the box as separate Paragraph \u2014 never inside the box.']),
        ('ScreenshotCard \u2014 Platform Interface Preview',
         "ScreenshotCard(width, img_path, caption, styles, max_img_h=120*mm, pad=10, label='PLATFORM INTERFACE')",
         ['\u2014 Sizing rule: Scale by WIDTH first: scale = min(inner_w/iw, max_img_h/ih). Critical \u2014 prevents landscape screenshots rendering as tiny strips.',
          '\u2014 White inner frame: 2pt padding only (not 4pt). rect() not roundRect() for inner frame.',
          "\u2014 Research env label: Use label='RESEARCH ENVIRONMENT' for Jupyter notebook screenshots."]),
        ('MetricCard \u2014 Key Metric Display',
         'MetricCard(width, number, label, context, styles)',
         ['\u2014 Layout: Groups of 4 across COL_W. Card height 54pt + context text below.',
          '\u2014 Number: Helvetica-Bold 18pt GOLD centred.',
          '\u2014 Label: Helvetica 7.5pt WARM_GREY centred (word-wrapped at 14 chars).']),
        ('CTABox \u2014 Call to Action',
         'CTABox(width, headline, body, ask, url, styles)',
         ['\u2014 Structure: Full-width. Gold 3pt bars top + bottom. Gold 1.2pt border all sides. CARD_BG.',
          '\u2014 Contents: Headline (cta_head, gold), body text, Vektor logo centred, CTA ask, URL with hyperlink.']),
        ('CoverPage \u2014 Document Cover',
         'CoverPage(W, H, doc_type, title, description, audience, logo_path)',
         ['\u2014 Logo position: ly = H \u00d7 0.52. lw = min(W \u00d7 0.62, 320). lh scales proportionally.',
          '\u2014 Gold rule: At ly-18, full page width.',
          '\u2014 Doc type: WARM_GREY, letter-spaced, below rule at rule_y-22.',
          '\u2014 Title: Helvetica-Bold 20pt PLATINUM. Lines split on \\n. Each centred.',
          '\u2014 Bottom section: RULE_MAJ separator at y=36mm. Audience at 28mm. Ref at 22mm. Date at 16mm.']),
        ('PullQuoteBox',
         'PullQuoteBox(width, text, style, pad_h=24, pad_v=18)',
         ['\u2014 Panel ruling: NO card background. Platinum rules top+bottom only (RULE_MAJ, 1.0pt). Open space between.']),
    ]
    for name, sig, notes_list in components:
        story.append(para(name,s,'sub_head'))
        story.append(para(sig,s,'code'))
        for note in notes_list:
            story.append(para(note,s,'body_grey'))
    story.append(PageBreak())

    # ── 06 DOCUMENT REGISTER ─────────────────────────────────────────────────
    section_header('06','Document Register',
        'Every document in the library with its fixed number, reference, and build script.',s,story)
    reg_rows=[
        [para('00',s,'tbl_mono'),para('Vektor at a Glance',s,'tbl_name'),
         para('\u2014',s,'tbl_body'),para('build_extras.py \u2192 build_executive_summary()',s,'tbl_mono')],
        [para('01',s,'tbl_mono'),para('Why Vektor',s,'tbl_name'),
         para('\u2014',s,'tbl_body'),para('build_final_suite.py \u2192 build_why_vektor()',s,'tbl_mono')],
        [para('02',s,'tbl_mono'),para('Brand Story',s,'tbl_name'),
         para('\u2014',s,'tbl_body'),para('build_final_suite.py \u2192 build_brand_story()',s,'tbl_mono')],
        [para('03',s,'tbl_mono'),para('WP-01: Portfolio Construction',s,'tbl_name'),
         para('IP-WP-QPC-260430-1.2',s,'tbl_mono'),para('build_final_suite.py \u2192 build_white_paper()',s,'tbl_mono')],
        [para('04',s,'tbl_mono'),para('Platform Brochure',s,'tbl_name'),
         para('\u2014',s,'tbl_body'),para('build_brochure_final.py \u2192 build()',s,'tbl_mono')],
        [para('WP-00',s,'tbl_mono'),para('Research Series Index',s,'tbl_name'),
         para('\u2014',s,'tbl_body'),para('build_extras.py \u2192 build_series_index()',s,'tbl_mono')],
        [para('WP-02',s,'tbl_mono'),para('Per-Instrument Signal Optimisation',s,'tbl_name'),
         para('IP-WP-SIG-260501-1.0',s,'tbl_mono'),para('build_white_papers.py \u2192 build_wp02()',s,'tbl_mono')],
        [para('WP-03',s,'tbl_mono'),para('Capital Allocation Precision',s,'tbl_name'),
         para('IP-WP-CAP-260501-1.0',s,'tbl_mono'),para('build_white_papers.py \u2192 build_wp03()',s,'tbl_mono')],
        [para('WP-04',s,'tbl_mono'),para('Technical Indicator Grid Search',s,'tbl_name'),
         para('IP-WP-TIS-260501-1.0',s,'tbl_mono'),para('build_white_papers.py \u2192 build_wp04()',s,'tbl_mono')],
        [para('WP-05',s,'tbl_mono'),para('Multi-Currency Infrastructure',s,'tbl_name'),
         para('IP-WP-FX-260501-1.0',s,'tbl_mono'),para('build_white_papers.py \u2192 build_wp05()',s,'tbl_mono')],
        [para('WP-06',s,'tbl_mono'),para('Audit Trail & Compliance',s,'tbl_name'),
         para('IP-WP-AUD-260501-1.0',s,'tbl_mono'),para('build_white_papers.py \u2192 build_wp06()',s,'tbl_mono')],
        [para('INT',s,'tbl_mono'),para('Document Journey Guide (internal)',s,'tbl_name'),
         para('\u2014',s,'tbl_body'),para('build_journey_guide.py \u2192 build()',s,'tbl_mono')],
    ]
    story.append(dark_table(['#','DOCUMENT','REFERENCE','BUILD SCRIPT'],reg_rows,
        [16*mm,52*mm,36*mm,COL_W-104*mm],s))
    story.append(PageBreak())

    # ── 07 FILE STRUCTURE ─────────────────────────────────────────────────────
    section_header('07','File Structure & Dependencies',
        'What must be present to rebuild any document.',s,story)
    story.append(para('REQUIRED FILES',s,'sub_head'))
    req_files=[
        ('vektor_styles.py','MUST be present first. All scripts import from this. Contains brand constants, styles, Flowable classes.'),
        ('/home/claude/vk2-work/VEKTOR-transparent-v3.png','Vektor logo with transparent background. Used on every page of every PDF. Path: /mnt/user-data/uploads/VEKTOR-transparent-v3.png (update LOGO_PATH if different).'),
        ('build_brochure_final.py','Brochure with UC01 screenshots. Set SC = path to your 11 screenshot PNGs.'),
        ('build_final_suite.py','Why Vektor, Brand Story, WP-01.'),
        ('build_white_papers.py','WP-02 through WP-06.'),
        ('build_extras.py','At a Glance + Research Series Index.'),
        ('build_journey_guide.py','Internal Document Journey Guide.'),
        ('build_word_docs.js','All 12 Word documents. Requires Node.js + docx@9.6.1.'),
    ]
    for fname, desc in req_files:
        story.append(para(fname,s,'code_label'))
        story.append(para(desc,s,'body_grey'))
    story.append(sp(8))
    story.append(para('PYTHON INSTALLATION',s,'sub_head'))
    story.append(para('pip install reportlab Pillow --break-system-packages',s,'code'))
    story.append(sp(4))
    story.append(para('NODE.JS INSTALLATION',s,'sub_head'))
    story.append(para('npm install -g docx',s,'code'))
    story.append(sp(8))
    story.append(para('BUILD ORDER',s,'sub_head'))
    build_steps=[
        ('1.','python3 build_final_suite.py','# 01, 02, 03'),
        ('2.','python3 build_brochure_final.py','# 04 (use this, not build_final_suite for brochure)'),
        ('3.','python3 build_white_papers.py','# WP-02 through WP-06'),
        ('4.','python3 build_extras.py','# 00, WP-00'),
        ('5.','python3 build_journey_guide.py','# Internal journey guide'),
        ('6.','node build_word_docs.js','# All 12 Word documents'),
    ]
    for step, cmd, comment in build_steps:
        is_new = '[NEW]' in comment
        colour = GOLD if is_new else colors.HexColor('#B8C0CC')
        line_style=ParagraphStyle(f'bs_{step}',fontName='Courier',fontSize=8,
            textColor=colour,leading=13,spaceAfter=3)
        story.append(Paragraph(f'{step}  {cmd}  {comment}',line_style))
    story.append(PageBreak())

    # ── 08 STANDING PANEL DECISIONS ──────────────────────────────────────────
    section_header('08','Standing Panel Decisions',
        'Rulings made by the five-expert Delphi advisory panel. Fixed. Do not change without explicit instruction.',s,story)
    story.append(para('BRAND ARCHITECTURE',s,'sub_head'))
    brand_decisions=[
        ("Vektor leads. InvestPuppy is the maker's mark.",
         'BY INVESTPUPPY in spaced full capitals at approximately one-quarter the cap height of VEKTOR. This hierarchy is fixed.'),
        ("InvestPuppy is NOT a 'tech lab'.",
         'This positioning was specifically considered and unanimously rejected by the panel. The current framing \u2014 InvestPuppy as founding entity, Vektor as the product \u2014 is correct and must not be changed.'),
        ("The Founder's Note is the correct response to the name question.",
         "It declares. It does not explain. The Brand Story's Founder's Note is the canonical treatment."),
    ]
    for title, body in brand_decisions:
        story.append(para(f'<b>{title}</b>',s))
        story.append(para(body,s,'body_grey'))
    story.append(sp(8))
    story.append(para('BRAND STORY SPECIFIC',s,'sub_head'))
    brand_story_decisions=[
        ('"Every element earns its place. Nothing is decorative." \u2014 appears exactly twice.',
         'Once in the Brand in One Paragraph (page 6 of the Brand Story). Once on the closing page. It was removed from the cover distillation in the final iteration. Do not add it back to the cover.'),
        ('"THE BRAND IN ONE PARAGRAPH" section tag was removed.',
         'The paragraph stands alone without announcement. Do not reintroduce the section tag.'),
        ('Brand in One Paragraph is open italic text \u2014 not boxed.',
         'This was a specific panel ruling. Boxing it signals supplementary when it should signal definitive.'),
        ('Pull Quote has no card background.',
         'Platinum rules top and bottom, open space between. The card background was removed after panel review.'),
    ]
    for title, body in brand_story_decisions:
        story.append(para(f'<b>{title}</b>',s))
        story.append(para(body,s,'body_grey'))
    story.append(sp(8))
    story.append(para('TECHNICAL DECISIONS',s,'sub_head'))
    tech_decisions=[
        ('MARGIN_T2 = 46mm.',
         'Increased from 38mm to fix header overlap on later pages. Any future session must use 46mm.'),
        ('Screenshots sized by WIDTH first.',
         'scale = min(inner_w/iw, max_img_h/ih). Prevents landscape screenshots rendering as tiny strips.'),
        ('Series label is "VEKTOR RESEARCH SERIES \u00b7 2026".',
         'Not "InvestPuppy Research Series" \u2014 changed after panel identified brand hierarchy inconsistency.'),
        ('Overfitting section in WP-04 is mandatory.',
         'Must include three mitigations (bounded search, Sharpe objective, daily re-optimisation) and the candour note acknowledging the limitation.'),
        ('Regulatory standing note is mandatory in Why Vektor and WP-06.',
         'Present but not detailed \u2014 available on request.'),
    ]
    for title, body in tech_decisions:
        story.append(para(f'<b>{title}</b>',s))
        story.append(para(body,s,'body_grey'))
    story.append(sp(8))
    story.append(para('INTENTIONALLY ABSENT \u2014 DO NOT ADD',s,'sub_head'))
    story.append(para(
        'The following are intentionally absent from all documents. Do not include unless explicitly instructed: '
        'founder name \u2014 not disclosed. Regulatory standing detail \u2014 available on request only. '
        'Social proof / reference clients \u2014 available on request only. '
        'Post-trade audit trail \u2014 on roadmap with IBKR. '
        'Formal walk-forward validation \u2014 on roadmap.',s,'body_grey'))
    story.append(PageBreak())

    # ── 09 REBUILD INSTRUCTIONS ───────────────────────────────────────────────
    section_header('09','How to Rebuild in a New Session',
        'Follow these steps to rebuild any document with full consistency.',s,story)
    rebuild_steps=[
        ('Step 1 \u2014 Provide context',
         "Start the new session with: 'I am working on the Vektor document library for InvestPuppy (investpuppy.com). I need to rebuild [document name]. Please read the attached Brand Specification Document before doing anything.'"),
        ('Step 2 \u2014 Upload this document',
         'Upload this Brand & Build Specification (PDF or Word version). Claude will read all colour values, component specifications, margin decisions, and panel rulings before starting.'),
        ('Step 3 \u2014 Upload the build scripts',
         'Upload the relevant scripts from the ZIP file. At minimum: vektor_styles.py and the specific build script for the document you need. For the brochure, also upload the screenshot PNGs.'),
        ('Step 4 \u2014 Upload the logo',
         'Upload VEKTOR-transparent-v3.png. Required for every PDF document. Claude will need to confirm the LOGO_PATH variable points to the uploaded file location (/mnt/user-data/uploads/).'),
        ('Step 5 \u2014 Specify the change precisely',
         'Tell Claude exactly what changed \u2014 which document, which section, which paragraph, and the exact new text. The more specific you are, the more accurate the rebuild will be.'),
        ('Step 6 \u2014 Verify before distributing',
         'Always open the rebuilt PDF and verify the change is correct and surrounding formatting is intact before distributing. Check the page of the change and the pages immediately before and after.'),
    ]
    for title, body in rebuild_steps:
        story.append(para(f'<b>{title}</b>',s,'body'))
        story.append(para(body,s,'body_grey'))
    story.append(sp(8))
    story.append(NoteBox(COL_W,
        'Consistency guarantee: Claude cannot guarantee pixel-perfect consistency across sessions for '
        'subjective spacing decisions caused by different text lengths. What WILL be consistent: colours, '
        'component behaviour, margins, typography hierarchy, and all brand rules captured here.',s['body_grey']))
    story.append(PageBreak())

    # ── 10 QUICK REFERENCE ────────────────────────────────────────────────────
    section_header('10','Quick Reference \u2014 Key Values',
        'The five constants that must never change and the key values to verify.',s,story)
    story.append(para('FIVE THINGS THAT MUST NOT CHANGE',s,'sub_head'))
    five=[
        '1. MARGIN_T2 = 46mm (not 38mm) \u2014 header overlap fix.',
        '2. Section rules = RULE_MAJ (#5A5A60) not gold.',
        '3. Sub-headings = WARM_GREY (#9A9086) not platinum.',
        '4. Screenshot sizing: scale by width first, not height.',
        '5. Series label: \u2018VEKTOR RESEARCH SERIES\u2019 not \u2018InvestPuppy Research Series\u2019.',
    ]
    for item in five:
        story.append(para(item,s,'body'))
    story.append(sp(10))
    story.append(para('KEY CONSTANTS \u2014 COPY EXACTLY',s,'sub_head'))
    constants=[
        'LOGO_PATH = "/mnt/user-data/uploads/VEKTOR-transparent-v3.png"',
        'DOC_DATE = "May 2026"',
        'BG = colors.HexColor("#0A0A0F")  # near-black page background',
        'PLATINUM = colors.HexColor("#E8E8EC")  # primary type',
        'GOLD = colors.HexColor("#C8A96E")  # accent \u2014 arrowhead only in mark',
        'OFF_WHITE = colors.HexColor("#E8E2D9")  # body text on dark background',
        'WARM_GREY = colors.HexColor("#9A9086")  # secondary text',
        'RULE_MAJ = colors.HexColor("#5A5A60")  # major rules \u2014 PLATINUM-TONED NOT GOLD',
        'RULE_MIN = colors.HexColor("#2A2828")  # minor rules \u2014 dim grey',
        'CARD_BG = colors.HexColor("#111116")  # card surfaces',
        'NOTE_BG = colors.HexColor("#16161A")  # NoteBox background',
        'CARD_EDGE = colors.HexColor("#242428")  # card borders',
        'MARGIN_T2 = 46*mm  # CRITICAL \u2014 not 38mm',
    ]
    for c in constants:
        story.append(para(c,s,'code'))
    story.append(sp(14))
    story.append(HRule(COL_W,GOLD,0.8,4,6))
    story.append(sp(8))
    story.append(para('Every element earns its place. Nothing is decorative.',s,'closing'))
    story.append(sp(10))
    # Updated deployment sequence
    story.append(para(
        'Deployment sequence: 00 At a Glance \u2192 04 Brochure \u2192 01 Why Vektor \u2192 03 WP-01 \u2192 '
        '02 Brand Story \u2192 Proof Partners conversation \u2192 WP-02 through WP-06.',s,'body_grey'))
    story.append(sp(10))
    story.append(para(
        f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  Brand & Build Specification  \u00b7  Internal Use Only  \u00b7  {DATE}',
        s,'wp_ref'))

    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    r=subprocess.run(['pdfinfo',out],capture_output=True,text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l or 'File' in l: print(l)

if __name__=='__main__': build()
