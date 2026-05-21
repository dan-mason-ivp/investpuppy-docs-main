import os as _os
_SCRIPT_DIR  = _os.path.dirname(_os.path.abspath(__file__))
_REPO_ROOT   = _os.path.dirname(_os.path.dirname(_SCRIPT_DIR))
_LOGOS       = _os.path.join(_REPO_ROOT, '_shared', 'logos')
_SCREENSHOTS = _os.path.join(_SCRIPT_DIR, 'screenshots')
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph,
    Spacer, Table, TableStyle, HRFlowable, PageBreak, NextPageTemplate
)
from reportlab.lib.utils import ImageReader
import os

BG      = colors.HexColor('#0A0A0F')
PLAT    = colors.HexColor('#E8E8EC')
GOLD    = colors.HexColor('#C8A96E')
OFF_W   = colors.HexColor('#E8E2D9')
W_GREY  = colors.HexColor('#9A9086')
CARD    = colors.HexColor('#111116')
NOTE    = colors.HexColor('#16161A')
RULE_MJ = colors.HexColor('#5A5A60')
RULE_MN = colors.HexColor('#2A2828')
GREEN   = colors.HexColor('#4A7C59')
AMBER   = colors.HexColor('#8C6A2A')
RED_MUT = colors.HexColor('#7C3A3A')
RED_TXT = colors.HexColor('#C87070')

W, H   = A4
ML = MR = 18*mm
MT = 20*mm
MB = 16*mm
LOGO   = '/home/claude/investpuppy/_shared/logos/IPHorizontalClear.png'
COL_W  = W - ML - MR

def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9, textColor=OFF_W,
             leading=14, spaceAfter=0, spaceBefore=0)
    d.update(kw)
    return ParagraphStyle(name, **d)

s_tag    = S('tag',  fontSize=7,  textColor=W_GREY, letterSpacing=2.5)
s_cov1   = S('cov1', fontName='Helvetica-Bold', fontSize=22, textColor=PLAT,
             leading=26, spaceAfter=4)
s_cov2   = S('cov2', fontName='Helvetica-Bold', fontSize=12, textColor=GOLD,
             leading=16, spaceAfter=8)
s_h2     = S('h2',   fontName='Helvetica-Bold', fontSize=11, textColor=PLAT,
             leading=15, spaceAfter=3)
s_h3     = S('h3',   fontName='Helvetica-Bold', fontSize=9.5, textColor=PLAT,
             leading=14, spaceAfter=2)
s_body   = S('body', fontSize=9, textColor=OFF_W, leading=14)
s_small  = S('small',fontSize=8, textColor=W_GREY, leading=12)
s_new    = S('new',  fontName='Helvetica-Bold', fontSize=7,
             textColor=GOLD, leading=10, letterSpacing=1.5)
s_upd    = S('upd',  fontName='Helvetica-Bold', fontSize=7,
             textColor=GREEN, leading=10, letterSpacing=1.5)
s_ref    = S('ref',  fontSize=7.5, textColor=W_GREY, leading=11)
s_code   = S('code', fontName='Courier', fontSize=8.5, textColor=GOLD,
             leading=13, backColor=CARD)
s_tbl_h  = S('tblh', fontName='Helvetica-Bold', fontSize=7.5, textColor=GOLD,
             leading=11, letterSpacing=1.5)
s_tbl_k  = S('tblk', fontSize=8.5, textColor=W_GREY, leading=12)
s_tbl_v  = S('tblv', fontSize=8.5, textColor=OFF_W, leading=12)
s_copy   = S('copy', fontName='Helvetica-Oblique', fontSize=8.5,
             textColor=GREEN, leading=13)
s_note_h = S('noteh',fontName='Helvetica-Bold', fontSize=8.5, textColor=PLAT,
             leading=13, leftIndent=8)
s_note_b = S('noteb',fontSize=8.5, textColor=W_GREY, leading=13, leftIndent=8)
s_voice  = S('voice',fontSize=8.5, textColor=GOLD, leading=13, leftIndent=8)

def p(txt, st):  return Paragraph(txt, st)
def sp(h=6):     return Spacer(1, h)
def hr(c=RULE_MJ,t=0.4,tb=3,bb=6):
    return HRFlowable(width=COL_W,color=c,thickness=t,
                      spaceBefore=tb,spaceAfter=bb)

def badge(txt, color):
    b = Table([[p(txt, S('b', fontName='Helvetica-Bold', fontSize=6.5,
                  textColor=color, leading=9, letterSpacing=1.5))]],
              colWidths=[None])
    b.setStyle(TableStyle([
        ('BOX',(0,0),(-1,-1),0.8,color),
        ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
    ]))
    return b

def note_box(title, body, gold=False):
    edge = GOLD if gold else RULE_MJ
    bg   = colors.HexColor('#1A1410') if gold else NOTE
    rows = [[p(title, s_note_h if not gold else
               S('ngh', fontName='Helvetica-Bold', fontSize=8.5,
                 textColor=GOLD, leading=13, leftIndent=8))]] if title else []
    rows.append([p(body, s_voice if gold else s_note_b)])
    t = Table(rows, colWidths=[COL_W - 8*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('LINEBEFORE',(0,0),(-1,-1),2.5,edge),
        ('BOX',(0,0),(-1,-1),0.3,RULE_MN),
    ]))
    return t

def page_spec(url, name, tag, arrival, departure, sections):
    """Build a page specification block."""
    # Header
    hdr_data = [
        [p(tag, S('ptag', fontName='Helvetica-Bold', fontSize=7,
                  textColor=W_GREY, leading=10, letterSpacing=2)),
         p('', s_tag)],
        [p(url, S('purl', fontName='Courier', fontSize=10,
                  textColor=GOLD, leading=13)),
         p('', s_tag)],
        [p(name, S('pnam', fontName='Helvetica-Bold', fontSize=12,
                   textColor=PLAT, leading=16)),
         p('', s_tag)],
    ]
    hdr = Table(hdr_data, colWidths=[COL_W*0.6, COL_W*0.4])
    hdr.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#0D0D12')),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('BOX',(0,0),(-1,-1),0.3,RULE_MN),
    ]))

    # Journey
    j_data = [
        [p('PROSPECT ON ARRIVAL', s_tbl_h), p('PROSPECT ON DEPARTURE', s_tbl_h)],
        [p(arrival, s_tbl_v), p(departure, s_tbl_v)],
    ]
    jt = Table(j_data, colWidths=[COL_W/2, COL_W/2])
    jt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),CARD),
        ('BACKGROUND',(0,1),(-1,1),NOTE),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MN),
        ('BOX',(0,0),(-1,-1),0.3,RULE_MN),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))

    # Section table
    s_rows = [[p('SECTION', s_tbl_h), p('COMPONENTS', s_tbl_h),
               p('COPY DIRECTION', s_tbl_h)]]
    for sec, comp, copy_dir in sections:
        s_rows.append([p(sec, s_tbl_k), p(comp, s_tbl_v), p(copy_dir, s_copy)])
    st = Table(s_rows, colWidths=[34*mm, COL_W*0.38, COL_W - 34*mm - COL_W*0.38])
    st.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),CARD),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[NOTE,CARD]),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('LINEBELOW',(0,0),(-1,-2),0.3,RULE_MN),
        ('BOX',(0,0),(-1,-1),0.4,RULE_MN),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))

    return [hdr, sp(4), jt, sp(4), st]

class CoverTpl(PageTemplate):
    def beforeDrawPage(self, c, doc):
        c.saveState()
        c.setFillColor(BG); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(GOLD); c.rect(0,H-2.5,W,2.5,fill=1,stroke=0)
        ip = ImageReader(LOGO); iw,ih = ip.getSize()
        lw=44*mm; lh=lw*ih/iw
        c.drawImage(LOGO,ML,H-MT-lh,lw,lh,mask='auto')
        c.setFont('Helvetica',6.5); c.setFillColor(W_GREY)
        c.drawString(ML,MB-4,
            'IP-WEB-SPEC-260508-2.0  \u00b7  VEKTOR BY INVESTPUPPY  \u00b7  INTERNAL  \u00b7  MAY 2026')
        c.restoreState()

class LaterTpl(PageTemplate):
    def beforeDrawPage(self, c, doc):
        c.saveState()
        c.setFillColor(BG); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(GOLD); c.rect(ML,H-11*mm,COL_W,0.8,fill=1,stroke=0)
        c.setFont('Helvetica',7); c.setFillColor(W_GREY)
        c.drawString(ML,H-9*mm,'WEBSITE SPECIFICATION v2.0  \u00b7  VEKTOR BY INVESTPUPPY')
        c.drawRightString(W-MR,H-9*mm,'IP-WEB-SPEC-260508-2.0')
        ip = ImageReader(LOGO); iw,ih = ip.getSize()
        lw=28*mm; lh=lw*ih/iw
        c.drawImage(LOGO,ML,1*mm,lw,lh,mask='auto')
        c.setFillColor(RULE_MJ); c.rect(ML,MB-2,COL_W,0.3,fill=1,stroke=0)
        c.setFont('Helvetica',6.5); c.setFillColor(W_GREY)
        c.drawRightString(W-MR,1*mm+lh/2-2,'investpuppy.com')
        c.drawCentredString(W/2,MB-7*mm,str(doc.page))
        c.restoreState()

OUT = '/home/claude/investpuppy/vektor/output/pdf/vk4-website-specification.pdf'
doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=ML, rightMargin=MR,
                      topMargin=MT, bottomMargin=MB+6*mm)
cf = Frame(ML,MB+6*mm,COL_W,H-MT-MB-6*mm,
           leftPadding=0,rightPadding=0,topPadding=38*mm,bottomPadding=0)
lf = Frame(ML,MB+6*mm,COL_W,H-MT-MB,
           leftPadding=0,rightPadding=0,topPadding=6*mm,bottomPadding=0)
doc.addPageTemplates([CoverTpl('Cover',[cf]), LaterTpl('Later',[lf])])

story = []

# ── COVER ──────────────────────────────────────────────────────────────────
story.append(p('WEBSITE SPECIFICATION', s_cov1))
story.append(p('Version 2.0  \u00b7  IP-WEB-SPEC-260508-2.0',
               S('vs', fontName='Helvetica-Bold', fontSize=12,
                 textColor=GOLD, leading=16, spaceAfter=6)))
story.append(hr(GOLD,0.8,2,10))
story.append(p(
    'This document supersedes IP-WEB-SPEC-260501-1.0. '
    'It incorporates all changes recommended by the Meridian and Arclight '
    'marketing panels following their review of the completed vk4 document suite. '
    'Platform recommendation, tool comparison, and build guide from v1.0 remain valid '
    'and are not repeated here.',
    S('ci', fontSize=10, textColor=OFF_W, leading=16, spaceAfter=8)))

# Change summary table
chg = [
    [p('CHANGE', s_tbl_h), p('TYPE', s_tbl_h), p('SECTION', s_tbl_h)],
    [p('Brand Voice Guide added as mandatory pre-read', s_tbl_v),
     p('NEW', S('nt', fontName='Helvetica-Bold', fontSize=7.5,
                textColor=GOLD, leading=11)), p('Section 01', s_tbl_k)],
    [p('8th page: /what-we-are-not', s_tbl_v),
     p('NEW', S('nt', fontName='Helvetica-Bold', fontSize=7.5,
                textColor=GOLD, leading=11)), p('Page 8', s_tbl_k)],
    [p('Prospect journey map added to all pages', s_tbl_v),
     p('NEW', S('nt', fontName='Helvetica-Bold', fontSize=7.5,
                textColor=GOLD, leading=11)), p('All pages', s_tbl_k)],
    [p('Home: scope honesty line + InvestPuppy name card', s_tbl_v),
     p('UPDATED', S('ut', fontName='Helvetica-Bold', fontSize=7.5,
                    textColor=GREEN, leading=11)), p('Page 1', s_tbl_k)],
    [p('Why Vektor: full nine NOT statements', s_tbl_v),
     p('UPDATED', S('ut2', fontName='Helvetica-Bold', fontSize=7.5,
                    textColor=GREEN, leading=11)), p('Page 3', s_tbl_k)],
    [p('Platform: multi-mandate in LIVE TODAY column', s_tbl_v),
     p('UPDATED', S('ut3', fontName='Helvetica-Bold', fontSize=7.5,
                    textColor=GREEN, leading=11)), p('Page 2', s_tbl_k)],
    [p('Documents: ungated WVIN + WNIC, updated library structure', s_tbl_v),
     p('UPDATED', S('ut4', fontName='Helvetica-Bold', fontSize=7.5,
                    textColor=GREEN, leading=11)), p('Page 7', s_tbl_k)],
    [p('Story: reframed around problem, not founders', s_tbl_v),
     p('UPDATED', S('ut5', fontName='Helvetica-Bold', fontSize=7.5,
                    textColor=GREEN, leading=11)), p('Page 6', s_tbl_k)],
    [p('NOT block added to design system', s_tbl_v),
     p('UPDATED', S('ut6', fontName='Helvetica-Bold', fontSize=7.5,
                    textColor=GREEN, leading=11)), p('Section 02', s_tbl_k)],
    [p('Proof Partners programme: conditional proof-of-concept framing', s_tbl_v),
     p('UPDATED', S('ut7', fontName='Helvetica-Bold', fontSize=7.5,
                    textColor=GREEN, leading=11)), p('Page 5', s_tbl_k)],
]
ct = Table(chg, colWidths=[COL_W*0.6, 20*mm, COL_W - COL_W*0.6 - 20*mm])
ct.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),CARD),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[NOTE,CARD]),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ('LINEBELOW',(0,0),(-1,-2),0.3,RULE_MN),
    ('BOX',(0,0),(-1,-1),0.4,RULE_MN),
]))
story.append(ct)

story.append(NextPageTemplate('Later'))
story.append(PageBreak())

# ── SECTION 01: BRAND VOICE REFERENCE ────────────────────────────────────
story.append(p('SECTION 01  \u00b7  MANDATORY PRE-READ', s_tag))
story.append(hr(GOLD,0.8,2,10))
story.append(p('Before writing any copy for this site, read the InvestPuppy '
    'Brand Voice Guide (IP-BVG-260508-1.0).', s_h2))
story.append(sp(6))
story.append(note_box('Why this is mandatory',
    'The Brand Voice Guide establishes the standard every sentence on this site '
    'is measured against. The copy direction notes in this specification describe '
    'what to say. The Brand Voice Guide describes how to say it.',
    gold=False))
story.append(sp(8))

story.append(p('THREE PRINCIPLES THAT GOVERN THIS SITE SPECIFICALLY', s_tag))
story.append(hr(RULE_MJ,0.4,2,8))

principles = [
    ('Principle 01 \u2014 Honest before impressive',
     'Every page leads with what is true, including limitations. '
     'The home page carries a scope statement. The Why Vektor page '
     'carries the full nine NOT statements. The /what-we-are-not page exists. '
     'No page makes a claim that is not supported by evidence elsewhere in the site.'),
    ('Principle 05 \u2014 Dry, not breathless',
     'No exclamation marks. No "revolutionary", "cutting-edge", or "game-changing". '
     'The site does not describe itself as impressive. The content is impressive. '
     'The writing is precise.'),
    ('Principle 09 \u2014 Short, then deep',
     'The home page is ninety seconds. The platform page is the brochure translated. '
     'The research page leads to ten white papers. This is the correct sequence. '
     'Do not put depth on the home page or brevity in the research series.'),
]
for title, body in principles:
    rows = [[p(title, S('ph', fontName='Helvetica-Bold', fontSize=9,
                        textColor=PLAT, leading=13))],
            [p(body, s_body)]]
    t = Table(rows, colWidths=[COL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),CARD),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
        ('LINEBEFORE',(0,0),(-1,-1),2.5,GOLD),
        ('BOX',(0,0),(-1,-1),0.3,RULE_MN),
    ]))
    story.append(t)
    story.append(sp(6))

story.append(PageBreak())

# ── SECTION 02: DESIGN SYSTEM UPDATE ─────────────────────────────────────
story.append(p('SECTION 02  \u00b7  DESIGN SYSTEM UPDATES', s_tag))
story.append(hr(GOLD,0.8,2,10))
story.append(p('Two new components added since v1.0. '
    'All other components in v1.0 remain valid.', s_body))
story.append(sp(8))

story.append(p('NEW COMPONENT \u2014 NOT BLOCK', s_h3))
story.append(sp(4))
comp1 = [
    [p('Property', s_tbl_h), p('Value', s_tbl_h)],
    [p('Purpose', s_tbl_k), p('Display a "What Vektor Is Not" statement', s_tbl_v)],
    [p('Background', s_tbl_k), p('#16161A (NOTE)', s_tbl_v)],
    [p('Left border', s_tbl_k), p('3px \u00b7 #C87070 (muted red)', s_tbl_v)],
    [p('Label style', s_tbl_k), p('Helvetica Bold \u00b7 8pt \u00b7 uppercase \u00b7 letter-spaced \u00b7 #C87070', s_tbl_v)],
    [p('Body style', s_tbl_k), p('Helvetica \u00b7 9.5pt \u00b7 #E8E2D9 \u00b7 leading 1.6', s_tbl_v)],
    [p('Used on', s_tbl_k), p('/what-we-are-not, /why-vektor', s_tbl_v)],
    [p('Paired with', s_tbl_k), p('IS block (gold left border, #111116 bg) for the positive statement', s_tbl_v)],
]
c1 = Table(comp1, colWidths=[36*mm, COL_W-36*mm])
c1.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),CARD),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[NOTE,CARD]),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ('LINEBELOW',(0,0),(-1,-2),0.3,RULE_MN),
    ('BOX',(0,0),(-1,-1),0.4,RULE_MN),
    ('LINEBEFORE',(0,0),(-1,-1),3,RED_TXT),
]))
story.append(c1)
story.append(sp(10))

story.append(p('NEW COMPONENT \u2014 NAME CARD', s_h3))
story.append(sp(4))
comp2 = [
    [p('Property', s_tbl_h), p('Value', s_tbl_h)],
    [p('Purpose', s_tbl_k), p('Surfaces the InvestPuppy name question on first visit', s_tbl_v)],
    [p('Trigger text', s_tbl_k), p('"You\'re probably wondering about the name."', s_tbl_v)],
    [p('Answer text', s_tbl_k), p('Two lines max. Links to full story on /why-vektor', s_tbl_v)],
    [p('Style', s_tbl_k), p('Dark card \u00b7 gold top bar \u00b7 single-column \u00b7 centred', s_tbl_v)],
    [p('Position', s_tbl_k), p('Home page: below Five Reasons, above Proof Partners programme form', s_tbl_v)],
    [p('Used on', s_tbl_k), p('/ (Home) only', s_tbl_v)],
]
c2 = Table(comp2, colWidths=[36*mm, COL_W-36*mm])
c2.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),CARD),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[NOTE,CARD]),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ('LINEBELOW',(0,0),(-1,-2),0.3,RULE_MN),
    ('BOX',(0,0),(-1,-1),0.4,RULE_MN),
    ('LINEBEFORE',(0,0),(-1,-1),3,GOLD),
]))
story.append(c2)

story.append(PageBreak())

# ── SECTION 03: SITE ARCHITECTURE ────────────────────────────────────────
story.append(p('SECTION 03  \u00b7  SITE ARCHITECTURE  \u2014  8 PAGES', s_tag))
story.append(hr(GOLD,0.8,2,10))
story.append(note_box('Change from v1.0',
    'v1.0 specified seven pages. v2.0 adds an eighth: /what-we-are-not. '
    'This page should appear in the navigation between /why-vektor and /research.',
    gold=True))
story.append(sp(8))

arch = [
    [p('URL', s_tbl_h), p('PAGE', s_tbl_h),
     p('PRIMARY PURPOSE', s_tbl_h), p('PRIMARY CTA', s_tbl_h), p('', s_tbl_h)],
    [p('/', s_code), p('Home', s_tbl_v),
     p('Qualify & intrigue', s_tbl_k), p('Proof Partners programme form', s_tbl_v),
     p('', s_tbl_k)],
    [p('/platform', s_code), p('The Platform', s_tbl_v),
     p('Show the product', s_tbl_k), p('Download brochure', s_tbl_v),
     p('', s_tbl_k)],
    [p('/why-vektor', s_code), p('Why Vektor', s_tbl_v),
     p('Make the commercial case', s_tbl_k), p('Proof Partners programme \u2192', s_tbl_v),
     p('', s_tbl_k)],
    [p('/what-we-are-not', s_code), p('What We Are Not', s_tbl_v),
     p('Brand differentiation \u00b7 honesty signal', s_tbl_k),
     p('Show us a mandate \u2192', s_tbl_v),
     p('NEW', S('nw', fontName='Helvetica-Bold', fontSize=7,
                textColor=GOLD, leading=10))],
    [p('/research', s_code), p('Research', s_tbl_v),
     p('Technical credibility', s_tbl_k), p('Download white papers', s_tbl_v),
     p('', s_tbl_k)],
    [p('/founding-mandate', s_code), p('Proof Partners programme', s_tbl_v),
     p('Convert enquiries', s_tbl_k), p('Submit enquiry form', s_tbl_v),
     p('', s_tbl_k)],
    [p('/story', s_code), p('The Story', s_tbl_v),
     p('Deepen relationship', s_tbl_k), p('Contact', s_tbl_v),
     p('UPDATED', S('up2', fontName='Helvetica-Bold', fontSize=7,
                    textColor=GREEN, leading=10))],
    [p('/documents', s_code), p('Documents', s_tbl_v),
     p('Document library', s_tbl_k), p('Register & download', s_tbl_v),
     p('UPDATED', S('up3', fontName='Helvetica-Bold', fontSize=7,
                    textColor=GREEN, leading=10))],
]
at = Table(arch, colWidths=[28*mm, 28*mm, COL_W*0.32, COL_W*0.22, 16*mm])
at.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),CARD),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[NOTE,CARD]),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
    ('LINEBELOW',(0,0),(-1,-2),0.3,RULE_MN),
    ('BOX',(0,0),(-1,-1),0.4,RULE_MN),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
]))
story.append(at)
story.append(sp(10))

story.append(p('NAVIGATION CHANGE', s_h3))
story.append(sp(4))
story.append(note_box('Updated nav order',
    'Platform \u00b7 Why Vektor \u00b7 What We Are Not \u00b7 Research \u00b7 '
    'Proof Partners programme \u00b7 The Story \u00b7 Documents\n'
    '"What We Are Not" sits between Why Vektor and Research. '
    'It is the honesty bridge between the commercial case and the technical depth. '
    '"Proof Partners programme" remains visually distinct: gold text, subtle gold border.',
    gold=False))

story.append(PageBreak())

# ── PAGE SPECS ────────────────────────────────────────────────────────────
story.append(p('SECTION 04  \u00b7  PAGE SPECIFICATIONS', s_tag))
story.append(hr(GOLD,0.8,2,10))
story.append(note_box('Italic green copy direction',
    'Copy direction notes in italic green describe what to write. '
    'How to write it is governed by the Brand Voice Guide (IP-BVG-260508-1.0). '
    'Sections marked [UNCHANGED FROM v1.0] need no rewrite.', gold=False))
story.append(sp(10))

# PAGE 1: HOME
for el in page_spec(
    '/ (Home)', 'Home', 'PAGE 01  \u00b7  UPDATED',
    'May have found site via search, referral, or direct. '
    'Knows little or nothing about Vektor. Default posture: mild scepticism. '
    'Will decide in ninety seconds whether to continue.',
    'Understands what Vektor is, what it is not, who it is for, and what the company is called. '
    'Has one clear next action: enquire about the Proof Partners programme.',
    [
        ('HERO\n(Full viewport)',
         'Vektor mark \u00b7 H1 \u00b7 sub-line \u00b7 scope line \u00b7 CTA',
         'H1: One Size Fits None.\nSub-line: Giving wealth teams the quantitative '
         'infrastructure institutional asset managers take for granted.\n'
         'Scope line [NEW]: Listed equities. Any exchange. Any currency. '
         'Any number of concurrent mandates.\nCTA: Enquire about Proof Partners programme \u2192'),
        ('THE PROBLEM\n(3-column)',
         '3 columns: Spreadsheet / Bloomberg PORT / Robo-tools',
         '[UNCHANGED FROM v1.0]'),
        ('THE PLATFORM\n(4 metrics)',
         '10,000 / 99.94% / 6 / 3yrs \u00b7 dark card',
         'Use 99.94% (not 99.9%). Copy from canonical metric descriptions.'),
        ('FIVE REASONS\n(Accordion)',
         '5 expandable rows \u00b7 gold number + platinum headline',
         'Verbatim from Why Vektor document. Reason 03 now reads: '
         '"Full transparency before a single order is placed \u2014 '
         'and full honesty about scope."'),
        ('NAME CARD\n[NEW]',
         'Single dark card \u00b7 gold top bar \u00b7 centred',
         '"You\'re probably wondering about the name. Good.\nInvestPuppy is the '
         'company. Vektor is the platform.\nWe kept the name because a name you '
         'remember is more useful than a name that sounds like everyone else\'s."\n'
         'Link: Read the full story \u2192 /why-vektor'),
        ('FOUNDING MANDATE\n(Form)',
         'Dark section \u00b7 gold top bar \u00b7 inline form',
         'H2: Show us a mandate. We\'ll show you whether Vektor is the '
         'right answer for yours.\nForm fields: Full name, Firm, Role, '
         'AUM band, Mandate description, Message.'),
        ('DOCUMENT TILES\n(3 cards)',
         'At a Glance \u00b7 What We Are Not \u00b7 Brochure',
         '[UPDATED] Replace third card from Research Series to '
         '"What We Are Not" \u2014 this is now a first-contact document. '
         'All three ungated.'),
    ]
):
    story.append(el)
story.append(sp(8))

story.append(PageBreak())

# PAGE 2: PLATFORM
for el in page_spec(
    '/platform', 'The Platform', 'PAGE 02  \u00b7  MINOR UPDATE',
    'Has read the home page or At a Glance. Wants to understand how the platform works.',
    'Understands the eleven-step workflow. Knows what is live today vs. what is coming. '
    'Has a specific question to ask or is ready to enquire.',
    [
        ('PAGE INTRO', '4 metric cards \u00b7 role summary', '[UNCHANGED FROM v1.0]'),
        ('STEPS 01\u201311', 'Screenshot cards per step', '[UNCHANGED FROM v1.0]'),
        ('PLATFORM STATUS\n[UPDATED]',
         '3-column: Live Today / Coming Next / Built to Scale',
         'LIVE TODAY column now includes:\n\u2014 Multiple clients, any mandate size\n'
         '\u2014 Add a mandate in minutes\n'
         'Move SAA & model portfolios to BUILT TO SCALE column.\n'
         'Copy verbatim from updated brochure capability table.'),
        ('PAGE CTA', 'Link to Proof Partners programme', '[UNCHANGED FROM v1.0]'),
    ]
):
    story.append(el)
story.append(sp(8))

# PAGE 3: WHY VEKTOR
for el in page_spec(
    '/why-vektor', 'Why Vektor', 'PAGE 03  \u00b7  MAJOR UPDATE',
    'Qualified prospect. Has seen the home page or a referral. '
    'Wants the commercial argument and honest assessment.',
    'Has read the full commercial case. Knows the limitations. '
    'Has seen the honest answer to every hard question. '
    'Is ready for due diligence or a Proof Partner engagement conversation.',
    [
        ('INVESTPUPPY\nQUESTION\n(Top of page)',
         'Gold left bar \u00b7 italic text \u00b7 labelled section',
         'Verbatim from Why Vektor document \u2014 The InvestPuppy Question section.\n'
         'This is now the OPENING of the page, not a buried section.\n'
         'Panel ruling: own the name aggressively at first contact, '
         'not as a response to an objection.'),
        ('THE CASE\n(Hero)',
         'Section tag \u00b7 H1 \u00b7 lead paragraph',
         '[UNCHANGED FROM v1.0]'),
        ('THE PROBLEM\n(3 alternatives)',
         '3 sections: Spreadsheet / Institutional / Retail',
         '[UNCHANGED FROM v1.0]'),
        ('FIVE REASONS\n(Full text)',
         '5 reasons at full text \u00b7 not accordion',
         'Verbatim from Why Vektor document. Reason 03 updated:\n'
         '"Full transparency before a single order is placed \u2014 '
         'and full honesty about scope."'),
        ('WHAT VEKTOR\nIS NOT\n[MAJOR UPDATE]',
         'H2: What Vektor Is Not \u00b7 9 NOT blocks',
         'Full nine NOT statements from IP-WVIN-260508-1.0.\n'
         'Use NOT block component (red left border) for each statement.\n'
         'All nine: black box / investment judgment / AI trading / live trading yet / '
         'multi-asset yet / live track record / regulated product / '
         'every mandate type / guarantee of any outcome.\n'
         'v1.0 had four abbreviated candour points. Replace entirely.'),
        ('HONEST ANSWER\n(Track record)',
         'Separate section below NOT blocks',
         '"No. We are telling you this before you ask because it is '
         'the right thing to do."\nVerbatim from FAQ Q11 updated answer.\n'
         'Link: See WP-09 (read this first) and WP-10.'),
        ('PAGE CTA', 'Links to Proof Partners programme + Research',
         '[UNCHANGED FROM v1.0]'),
    ]
):
    story.append(el)

story.append(PageBreak())

# PAGE 4: WHAT WE ARE NOT (NEW)
for el in page_spec(
    '/what-we-are-not', 'What We Are Not', 'PAGE 04  \u00b7  NEW PAGE',
    'May be a sceptic. May have been referred specifically to this page. '
    'Wants to know what the platform cannot do before believing what it can.',
    'Has read all nine NOT statements. Has read the corresponding IS statements. '
    'Scepticism is addressed before it was voiced. '
    'Trust signal delivered. Ready to engage seriously.',
    [
        ('PAGE HERO',
         'H1: What Vektor Is Not \u00b7 intro paragraph',
         '"An honest description of scope, limitation, and design intent.\n'
         'We believe you should know what this platform does not do '
         'before we tell you what it does.\n'
         'The questions these pages do not answer \u2014 ask us. '
         'We will tell you."'),
        ('9 NOT BLOCKS',
         'NOT block component (red left border) \u00b7 one per statement',
         'Verbatim from IP-WVIN-260508-1.0. All nine statements.\n'
         'Order: black box \u00b7 investment judgment \u00b7 guarantee of any outcome '
         '(move to 3rd \u2014 panel recommendation) \u00b7 AI trading \u00b7 '
         'live trading yet \u00b7 multi-asset yet \u00b7 live track record \u00b7 '
         'regulated product \u00b7 every mandate type.'),
        ('DIVIDER\n(Transition)',
         'Gold rule \u00b7 section break',
         '"Having been precise about what Vektor is not, '
         'here is what it is. With the same precision."'),
        ('6 IS BLOCKS',
         'IS block component (gold left border) \u00b7 one per statement',
         'Verbatim from IP-WVIN-260508-1.0. All six IS statements.\n'
         'Systematic listed equity \u00b7 multi-mandate \u00b7 institutional rigour '
         '\u00b7 human-gated \u00b7 fully auditable \u00b7 proof-of-concept offer.'),
        ('PAGE CTA',
         'Proof-of-concept offer \u00b7 link to Proof Partners programme',
         '"Show us a mandate. We\'ll show you the platform."\n'
         'CTA: Enquire about Proof Partners programme \u2192'),
    ]
):
    story.append(el)
story.append(sp(8))

# PAGE 5: RESEARCH
for el in page_spec(
    '/research', 'Research', 'PAGE 05  \u00b7  MINOR UPDATE',
    'Technically motivated. Has read Why Vektor or a colleague directed them here. '
    'Wants methodology depth.',
    'Has accessed or registered for the research series. '
    'Understands the methodology is documented in full. '
    'Trust in the technical approach is established.',
    [
        ('PAGE INTRO',
         'Section tag \u00b7 H1 \u00b7 philosophy statement',
         '[UNCHANGED FROM v1.0]\nPhilosophy: "These are not marketing documents. '
         'They are technical methodology papers."'),
        ('WP-00\n(Featured)',
         'Series index card \u00b7 ungated',
         '[UNCHANGED FROM v1.0]'),
        ('WP-01 to WP-10\n[UPDATED]',
         '10 paper cards (was 6) \u00b7 gated after registration',
         'Suite now has WP-01 through WP-10 (10 papers).\n'
         'Update card count from 6 to 10.\n'
         'Add new cards: WP-07 Technical Architecture, WP-08 AI/ML Philosophy, '
         'WP-09 Risk Disclosure (featured \u2014 "read this first"), '
         'WP-10 Evaluating Performance.\n'
         'WP-09 card treatment: gold border, "Read this first" label.'),
        ('CROSS-REF',
         'Links to Platform and Proof Partners programme',
         '[UNCHANGED FROM v1.0]'),
    ]
):
    story.append(el)

story.append(PageBreak())

# PAGE 6: FOUNDING MANDATE
for el in page_spec(
    '/founding-mandate', 'Proof Partners programme', 'PAGE 06  \u00b7  UPDATED',
    'Serious prospect. Has done enough reading to want to engage formally.',
    'Has submitted the enquiry form. '
    'Understands the three-step process (NDA, DD, commercial). '
    'Expects to hear from the team directly.',
    [
        ('PAGE HERO\n[UPDATED]',
         'Section tag \u00b7 H1 \u00b7 2-sentence description',
         'H1: Show us a mandate.\nSub-head: We\'ll show you whether Vektor '
         'is the right answer for yours.\n'
         '[UPDATED: "whether" not "we\'ll show you the platform" \u2014 '
         'conditional framing signals confidence, not desperation.]\n'
         'Body: "Pick any listed equity market, any currency, any benchmark. '
         'We will run the full Vektor workflow and show you the output. '
         'No slides. No promises. Just the platform, working on your data."'),
        ('WHAT IT IS',
         'FMP description \u00b7 3-step process',
         '[UNCHANGED FROM v1.0]'),
        ('WHO IT IS FOR',
         '3 audience types',
         '[UNCHANGED FROM v1.0]'),
        ('SCOPE NOTE\n[NEW]',
         'Single note card below audience section',
         '"The Proof Partners programme is currently open to teams '
         'managing listed equity mandates across any exchange and currency. '
         'Multi-asset mandates are on our roadmap. '
         'If your mandate includes fixed income or alternatives, '
         'enquire anyway \u2014 we will tell you honestly where we stand."'),
        ('THE FORM',
         'Full qualifying form',
         '[UNCHANGED FROM v1.0]'),
    ]
):
    story.append(el)
story.append(sp(8))

# PAGE 7: STORY
for el in page_spec(
    '/story', 'The Story', 'PAGE 07  \u00b7  MAJOR UPDATE',
    'Engaged prospect or potential partner. Wants to understand who is behind this.',
    'Understands the problem Vektor was built to solve. '
    'Understands the InvestPuppy brand philosophy. '
    'Trust in the team is built through the quality of the thinking, '
    'not through personal biography.',
    [
        ('THE PROBLEM\n(Opening)',
         'H1: The Problem We Decided to Solve\n\u00b7 Three sections',
         '[MAJOR UPDATE FROM v1.0]\n'
         'v1.0 specified a Founder\'s Note and team biography section. '
         'These are replaced entirely due to founder anonymity constraint.\n'
         'Open with the problem: boutique DPMs are managing institutional-scale '
         'complexity with non-institutional tools. This is not a technology gap. '
         'It is an access gap. Vektor exists to close it.\n'
         'Written in first person plural ("we") not attributed to any individual.'),
        ('TWO MARKS\n(Brand story)',
         'Vektor mark \u00b7 InvestPuppy mark \u00b7 Two-column explanation',
         'Verbatim from Brand Story document \u2014 Section 01 and Section 02.\n'
         '"Two marks. One purpose."\n'
         'The name explanation lives here in full, for those who want the full version.\n'
         'Closes with: "Serious when it matters."'),
        ('THE APPROACH\n(Philosophy)',
         'Three philosophy cards',
         '"Honest by design. We tell you what we cannot do before '
         'we tell you what we can.\n'
         'Rigorous by necessity. The people who use this platform '
         'are responsible for other people\'s money.\n'
         'Independent by choice. We are building this for the teams '
         'who chose to work differently."'),
        ('CROSS-REF',
         'Links to Research and Proof Partners programme',
         '[UNCHANGED FROM v1.0]'),
    ]
):
    story.append(el)

story.append(PageBreak())

# PAGE 8: DOCUMENTS
for el in page_spec(
    '/documents', 'Documents', 'PAGE 08  \u00b7  ARCHITECTURE UPDATE',
    'Prospect in due diligence or evaluation mode. '
    'Wants systematic access to all suite materials.',
    'Has accessed the documents relevant to their stage. '
    'Commercial documents available without friction. '
    'Research series and technical documents gated after registration.',
    [
        ('UNGATED\nDOCUMENTS\n[UPDATED]',
         'Document tiles \u00b7 direct download',
         '[UPDATED: Now 4 ungated documents (was 2)]\n'
         '1. At a Glance (1pp)\n'
         '2. What Vektor Is Not (IP-WVIN-260508-1.0)\n'
         '3. Why Not the Incumbents? (IP-WNIC-260508-1.0)\n'
         '4. Platform Brochure (14pp)\n'
         'Rationale: WVIN and WNIC are first-contact documents. '
         'Gating them defeats their purpose.'),
        ('GATED\nDOCUMENTS\n(Registration)',
         'Form modal: name + email \u00b7 one registration unlocks all',
         'Research Series: WP-01 through WP-10\n'
         'Why Vektor (full document)\n'
         'Proof Partners programme\n'
         'DD Navigation Guide\n'
         'One registration gives access to all gated documents.'),
        ('LIBRARY\nSTRUCTURE\n[UPDATED]',
         'Tabbed or sectioned layout matching vk4 suite structure',
         '[UPDATED: Structure now mirrors vk4 suite navigation]\n'
         'START HERE \u00b7 QUICK-SEND \u00b7 01 WHY VEKTOR \u00b7 '
         '02 THE PLATFORM \u00b7 03 FOUNDING MANDATE \u00b7 '
         '04 RESEARCH SERIES \u00b7 05 DUE DILIGENCE\n'
         'Label each section with its purpose (one line) '
         'matching the ABOUT-THIS-FOLDER.txt convention.'),
        ('PRESENTATIONS\n(On request)',
         'Greyed section \u00b7 contact link',
         '"Five presentation decks are available on request. '
         'Contact us to discuss which format matches your context."'),
    ]
):
    story.append(el)

story.append(PageBreak())

# ── SECTION 05: POST-LAUNCH CHECKLIST UPDATE ──────────────────────────────
story.append(p('SECTION 05  \u00b7  POST-LAUNCH CHECKLIST UPDATES', s_tag))
story.append(hr(GOLD,0.8,2,10))
story.append(p('The following items are added to the v1.0 post-launch checklist.',
               s_body))
story.append(sp(8))

checklist = [
    [p('ITEM', s_tbl_h), p('DESCRIPTION', s_tbl_h), p('STATUS', s_tbl_h)],
    [p('Fix page title typo', s_tbl_k),
     p('"Institutional Portfolio Infrstructure" \u2192 "Infrastructure"', s_tbl_v),
     p('GoDaddy page settings', s_tbl_v)],
    [p('Remove GoDaddy label', s_tbl_k),
     p('"Additional Information" label above proposition copy', s_tbl_v),
     p('GoDaddy page settings', s_tbl_v)],
    [p('Swap At a Glance PDF', s_tbl_k),
     p('Replace embedded PDF with vk4-at-a-glance.pdf', s_tbl_v),
     p('GoDaddy PDF embed', s_tbl_v)],
    [p('Add /what-we-are-not page', s_tbl_k),
     p('New page spec above. Add to navigation.', s_tbl_v),
     p('New build required', s_tbl_v)],
    [p('UK-01 compliance', s_tbl_k),
     p('FCA regulatory context page/FAQ entry. UK distribution BLOCKER.', s_tbl_v),
     p('Compliance review required', s_tbl_v)],
    [p('Verify scope line', s_tbl_k),
     p('Confirm "Listed equities. Any exchange..." in hero sub-line', s_tbl_v),
     p('Copy update', s_tbl_v)],
    [p('Add Name Card component', s_tbl_k),
     p('InvestPuppy name card on home page below Five Reasons', s_tbl_v),
     p('New component build', s_tbl_v)],
    [p('Update Platform Status', s_tbl_k),
     p('Multi-mandate in LIVE TODAY column', s_tbl_v),
     p('Copy update', s_tbl_v)],
    [p('Update document tiles', s_tbl_k),
     p('Replace Research Series tile with What We Are Not on home page', s_tbl_v),
     p('Content update', s_tbl_v)],
    [p('Cookie / PDPA compliance', s_tbl_k),
     p('CookieYes (free tier). Install before any paid traffic.', s_tbl_v),
     p('One-line install', s_tbl_v)],
]
clt = Table(checklist, colWidths=[38*mm, COL_W*0.52, COL_W - 38*mm - COL_W*0.52])
clt.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),CARD),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[NOTE,CARD]),
    ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
    ('LINEBELOW',(0,0),(-1,-2),0.3,RULE_MN),
    ('BOX',(0,0),(-1,-1),0.4,RULE_MN),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
]))
story.append(clt)

story.append(sp(16))
story.append(hr(GOLD,0.5,4,8))
story.append(p(
    'This specification supersedes IP-WEB-SPEC-260501-1.0 for all new build work. '
    'The platform recommendation (Webflow), tool comparison, and step-by-step '
    'build guide in v1.0 remain valid and should be read alongside this document.',
    S('fin', fontSize=8.5, textColor=W_GREY, leading=14, alignment=TA_CENTER)))

doc.build(story)
sz = os.path.getsize(OUT)
print(f"Built: {OUT}")
print(f"Size:  {sz:,} bytes ({sz//1024}KB)")
