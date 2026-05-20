"""
InvestPuppy: Unvarnished — Design System v5
Typography: Poppins Light body / Regular italic / Bold headers
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLTTF
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, PageBreak,
    HRFlowable, NextPageTemplate
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable
import os

# ── Register Poppins family ───────────────────────────────────────────────────

# ── Repo-relative asset resolution ───────────────────────────────────────────
import os as _os
_SCRIPT_DIR = _os.path.dirname(_os.path.abspath(__file__))  # unvarnished/source/
_REPO_ROOT   = _os.path.dirname(_os.path.dirname(_SCRIPT_DIR))  # investpuppy/
_SHARED      = _os.path.join(_REPO_ROOT, '_shared')
_FONT_DIR    = _os.path.join(_SHARED, 'fonts')
_LOGO_DIR    = _os.path.join(_SHARED, 'logos')
_COVER_DIR   = _os.path.join(_SHARED, 'cover-photos')
_STAMP_DIR   = _os.path.join(_SHARED, 'stamp')

def _asset(subdir, filename):
    """Return path to a shared asset, raising if not found."""
    p = _os.path.join(_SHARED, subdir, filename)
    if not _os.path.exists(p):
        raise FileNotFoundError(f"Shared asset not found: {p}")
    return p

_POPPINS = {
    'Poppins-Light':    _os.path.join(_FONT_DIR, 'Poppins-Light.ttf'),
    'Poppins':          _os.path.join(_FONT_DIR, 'Poppins-Regular.ttf'),
    'Poppins-Medium':   _os.path.join(_FONT_DIR, 'Poppins-Medium.ttf'),
    'Poppins-Bold':     _os.path.join(_FONT_DIR, 'Poppins-Bold.ttf'),
    'Poppins-LightIta': _os.path.join(_FONT_DIR, 'Poppins-LightItalic.ttf'),
    'Poppins-Italic':   _os.path.join(_FONT_DIR, 'Poppins-Italic.ttf'),
    'Poppins-MedIta':   _os.path.join(_FONT_DIR, 'Poppins-MediumItalic.ttf'),
    'Poppins-BoldIta':  _os.path.join(_FONT_DIR, 'Poppins-BoldItalic.ttf'),
}
for _name, _path in _POPPINS.items():
    pdfmetrics.registerFont(RLTTF(_name, _path))
pdfmetrics.registerFontFamily('Poppins',
    normal='Poppins', bold='Poppins-Bold',
    italic='Poppins-Italic', boldItalic='Poppins-BoldIta')
pdfmetrics.registerFontFamily('Poppins-Light',
    normal='Poppins-Light', bold='Poppins-Bold',
    italic='Poppins-LightIta', boldItalic='Poppins-BoldIta')

# ── Type system ───────────────────────────────────────────────────────────────
# Body:        Poppins Light       — main text
# Body italic: Poppins Italic      — quotes, elevation (Regular weight, not Light)
# Small text:  Poppins Regular     — noteboxes, seriesboxes, anything <10pt
# Headers:     Poppins Bold        — section headers, cover title, statements
# Mid weight:  Poppins Medium      — closing lines, emphasis within body

F_LIGHT   = 'Poppins-Light'
F_REG     = 'Poppins'
F_MEDIUM  = 'Poppins-Medium'
F_BOLD    = 'Poppins-Bold'
F_LITE_I  = 'Poppins-LightIta'
F_REG_I   = 'Poppins-Italic'
F_MED_I   = 'Poppins-MedIta'
F_BOLD_I  = 'Poppins-BoldIta'

# ── Colours ───────────────────────────────────────────────────────────────────
GREEN       = HexColor('#85D155')
DARK        = HexColor('#0A0A0A')
GREY_TEXT   = HexColor('#888888')
BODY_TEXT   = HexColor('#1A1A1A')
PLACEHOLDER = HexColor('#B0A89E')
PH_TEXT     = HexColor('#6A6058')
NOTE_BG     = HexColor('#F5F7F2')
SERIES_BG   = HexColor('#F4F4F4')
SERIES_BDR  = HexColor('#C8C8C8')
RULE_GREY   = HexColor('#DDDDDD')

# ── Dimensions ────────────────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN_L  = 52
MARGIN_R  = 52
MARGIN_B  = 44
HEADER_H  = 38
HEADER_RL = 1.5
BODY_W    = PAGE_W - MARGIN_L - MARGIN_R
BODY_TOP  = PAGE_H - HEADER_H - HEADER_RL - 18
BODY_H    = BODY_TOP - MARGIN_B
COL_GAP   = 18
COL_W     = (BODY_W - COL_GAP) / 2
TOP_H     = 255
TOP_Y     = BODY_TOP - TOP_H
COL_H_P1  = TOP_Y - MARGIN_B - 10
COVER_SPLIT = 0.58
DARK_BAND_H = PAGE_H * (1 - COVER_SPLIT)
PHOTO_H     = PAGE_H * COVER_SPLIT

LOGO_DARK  = _os.path.join(_LOGO_DIR, 'ip_logo_dark_bg.png')
LOGO_VERT  = _os.path.join(_LOGO_DIR, 'ip_logo_vertical.png')

# ── Series locked text ────────────────────────────────────────────────────────
ATTRIBUTION = (
    "InvestPuppy builds Vektor, a systematic portfolio management "
    "platform for wealth management professionals."
)
SERIES_PREFACE = (
    "Every experienced practitioner thinks it. Almost nobody publishes it: "
    "<i>there has to be a better way.</i> We thought it long enough that we "
    "went and built one. Before that, we spent decades in the rooms \u2014 the ones "
    "where the same project was failing for the third time, the project plan "
    "had been signed off before anyone had understood the first requirement, "
    "and the relationship was too warm for anyone to say so. We know exactly "
    "why this keeps happening. It isn\u2019t incompetence. It\u2019s something more "
    "interesting than that. It\u2019s the incentive structure doing its job "
    "perfectly. Nobody planned it this way. Nobody needed to. We got "
    "frustrated enough to write it down. Then frustrated enough to build "
    "something. These papers are the writing-it-down part. The something "
    "we built is a separate conversation."
)

_pn = [2]


# ═════════════════════════════════════════════════════════════════════════════
# COVER
# ═════════════════════════════════════════════════════════════════════════════

def draw_cover(c, title, ref, photo_desc, num, photo_path=None):
    # Photo
    if photo_path and os.path.exists(photo_path):
        c.drawImage(photo_path, 0, DARK_BAND_H, width=PAGE_W, height=PHOTO_H,
                    preserveAspectRatio=False, mask='auto')
    else:
        c.setFillColor(PLACEHOLDER)
        c.rect(0, DARK_BAND_H, PAGE_W, PHOTO_H, fill=1, stroke=0)
        c.setFillColor(PH_TEXT); c.setFont('Helvetica-Oblique', 9)
        c.drawCentredString(PAGE_W/2, DARK_BAND_H+PHOTO_H/2+20, "[ PHOTOGRAPH ]")
        c.setFont('Helvetica', 8)
        words=photo_desc.split(); lines,cur=[],[]
        for w in words:
            if len(' '.join(cur+[w]))<=62: cur.append(w)
            else:
                if cur: lines.append(' '.join(cur))
                cur=[w]
        if cur: lines.append(' '.join(cur))
        for i,ln in enumerate(lines[:3]):
            c.drawCentredString(PAGE_W/2, DARK_BAND_H+PHOTO_H/2-i*12, ln)

    # Stamp — fully within photo area, lower-right
    # DARK_BAND_H + 90 keeps stamp centre well above the divider
    stamp_cx = PAGE_W - 88
    stamp_cy = DARK_BAND_H + 88
    draw_stamp(c, stamp_cx, stamp_cy)

    # Green divider
    c.setFillColor(GREEN)
    c.rect(0, DARK_BAND_H-1.5, PAGE_W, 2.5, fill=1, stroke=0)

    # Dark band
    c.setFillColor(DARK)
    c.rect(0, 0, PAGE_W, DARK_BAND_H, fill=1, stroke=0)

    # ── ALL CENTRED — GENEROUS SPACING ───────────────────────────────────────

    # Working from top of dark band downward
    y = DARK_BAND_H

    # 1. Logo — centred, 90pt
    logo_h = 90
    logo_w = 90 * (1003/1006)
    y -= 18                          # top padding
    logo_y = y - logo_h              # bottom-left y for drawImage
    c.drawImage(LOGO_VERT, (PAGE_W - logo_w)/2, logo_y,
                width=logo_w, height=logo_h,
                mask='auto', preserveAspectRatio=True)
    y = logo_y                       # y now = bottom of logo

    # 2. "UNVARNISHED" in green — centred
    y -= 14                          # gap below logo
    c.setFillColor(GREEN); c.setFont(F_BOLD, 10.5)
    c.drawCentredString(PAGE_W/2, y, "UNVARNISHED")

    # 3. Thin green rule — centred
    y -= 18                          # gap below series name
    rule_w = 100
    c.setFillColor(GREEN)
    c.rect((PAGE_W - rule_w)/2, y, rule_w, 0.75, fill=1, stroke=0)

    # 4. Paper title — centred, Poppins Bold, white
    # Gap: 24pt to clear 22pt cap ascent (≈15pt) with comfortable breathing room
    y -= 24
    fs = 22
    c.setFont(F_BOLD, fs)
    tw = PAGE_W - MARGIN_L*2
    words = title.split(); t_lines, cur = [], []
    for w in words:
        if c.stringWidth(' '.join(cur+[w]), F_BOLD, fs) <= tw: cur.append(w)
        else:
            if cur: t_lines.append(' '.join(cur))
            cur = [w]
    if cur: t_lines.append(' '.join(cur))
    c.setFillColor(HexColor('#FFFFFF'))
    lh = fs * 1.3
    for i, ln in enumerate(t_lines):
        c.drawCentredString(PAGE_W/2, y - i*lh, ln)

    # 5. Footer
    c.setFillColor(GREEN)
    c.rect(MARGIN_L, 36, PAGE_W-MARGIN_L*2, 0.75, fill=1, stroke=0)
    c.setFont(F_REG_I, 9.5)
    c.drawCentredString(PAGE_W/2, 24, "Serious when it matters.")
    c.setFillColor(GREY_TEXT); c.setFont(F_REG, 7)
    c.drawString(MARGIN_L, 13, ref)
    c.drawRightString(PAGE_W-MARGIN_R, 13, "investpuppy.com")


# ═════════════════════════════════════════════════════════════════════════════
# INTERIOR CHROME
# ═════════════════════════════════════════════════════════════════════════════

def _chrome(c, doc):
    c.setFillColor(DARK)
    c.rect(0, PAGE_H-HEADER_H, PAGE_W, HEADER_H, fill=1, stroke=0)
    if os.path.exists(LOGO_DARK):
        lh=20; lw=20*(911/746)
        c.drawImage(LOGO_DARK, MARGIN_L, PAGE_H-HEADER_H+(HEADER_H-lh)/2,
                    width=lw, height=lh, mask='auto', preserveAspectRatio=True)
        c.setFillColor(HexColor('#FFFFFF')); c.setFont(F_BOLD, 7.5)
        c.drawString(MARGIN_L+lw+6, PAGE_H-HEADER_H+HEADER_H/2+1,
                     "InvestPuppy: Unvarnished")
        c.setFillColor(GREY_TEXT); c.setFont(F_REG_I, 6.5)
        c.drawString(MARGIN_L+lw+6, PAGE_H-HEADER_H+HEADER_H/2-8,
                     "field notes from decades of bad projects.")
    c.setFillColor(GREY_TEXT); c.setFont(F_REG, 7)
    c.drawRightString(PAGE_W-MARGIN_R, PAGE_H-HEADER_H+14, "investpuppy.com")
    c.setFillColor(GREEN)
    c.rect(0, PAGE_H-HEADER_H-HEADER_RL, PAGE_W, HEADER_RL, fill=1, stroke=0)
    c.setFillColor(GREY_TEXT); c.setFont(F_REG, 7.5)
    c.drawCentredString(PAGE_W/2, 16, str(_pn[0]))
    _pn[0] += 1


# ═════════════════════════════════════════════════════════════════════════════
# STYLES
# ═════════════════════════════════════════════════════════════════════════════

def get_styles():
    S = {}
    BL = 15.5

    # ── Body ─────────────────────────────────────────────────────────────────
    S['body']     = ParagraphStyle('body', fontName=F_LIGHT, fontSize=10.5,
                        leading=BL, textColor=BODY_TEXT, spaceAfter=8)
    S['body_j']   = ParagraphStyle('body_j', parent=S['body'],
                        alignment=TA_JUSTIFY)

    # ── Series framing (Regular weight — larger than 9.5pt so Light would work,
    #    but Regular for NoteBox/SeriesBox to hold weight at small sizes) ─────
    S['attribution'] = ParagraphStyle('attribution', fontName=F_REG,
                        fontSize=8.5, leading=12.5,
                        textColor=HexColor('#555555'), spaceAfter=0)
    S['preface']  = ParagraphStyle('preface', fontName=F_REG, fontSize=10,
                        leading=14.5, textColor=BODY_TEXT, spaceAfter=0,
                        alignment=TA_JUSTIFY)

    # ── Q&A openers ──────────────────────────────────────────────────────────
    S['qa_line']  = ParagraphStyle('qa_line', fontName=F_BOLD, fontSize=10.5,
                        leading=17, textColor=BODY_TEXT,
                        spaceAfter=2, spaceBefore=2, alignment=TA_CENTER)
    S['spaced_statement'] = ParagraphStyle('spaced_statement',
                        fontName=F_BOLD, fontSize=11, leading=16,
                        textColor=GREEN, spaceAfter=18, spaceBefore=18,
                        alignment=TA_CENTER)

    # ── Blockquote (Regular Italic — not Light Italic — holds on the page) ──
    S['bq_body']  = ParagraphStyle('bq_body', fontName=F_REG_I, fontSize=10.5,
                        leading=16, textColor=BODY_TEXT,
                        spaceAfter=5, leftIndent=14, rightIndent=8)
    S['bq_close'] = ParagraphStyle('bq_close', fontName=F_BOLD_I, fontSize=10.5,
                        leading=16, textColor=GREEN,
                        spaceAfter=0, leftIndent=14, rightIndent=8)

    # ── Failure mode labels ───────────────────────────────────────────────────
    S['failure_label'] = ParagraphStyle('failure_label', fontName=F_BOLD,
                        fontSize=10.5, leading=14, textColor=GREEN,
                        spaceBefore=10, spaceAfter=2)

    # ── Closings ─────────────────────────────────────────────────────────────
    S['closing']       = ParagraphStyle('closing', fontName=F_MEDIUM,
                        fontSize=10.5, leading=15, textColor=BODY_TEXT,
                        spaceAfter=3, spaceBefore=14)
    S['closing_green'] = ParagraphStyle('closing_green', fontName=F_BOLD,
                        fontSize=10.5, leading=15, textColor=GREEN, spaceAfter=0)
    S['isolated_statement'] = ParagraphStyle('isolated_statement',
                        fontName=F_BOLD, fontSize=10.5, leading=15,
                        textColor=BODY_TEXT, spaceAfter=0, spaceBefore=22)

    # ── NoteBox — Regular (not Light) at 9.5pt ────────────────────────────────
    S['note_text'] = ParagraphStyle('note_text', fontName=F_REG, fontSize=9.5,
                        leading=14, textColor=BODY_TEXT, spaceAfter=0,
                        leftIndent=10, rightIndent=10, alignment=TA_JUSTIFY)

    # ── Series box mixed-weight styles ───────────────────────────────────────
    S['sb_hook']   = ParagraphStyle('sb_hook',   fontName=F_BOLD,   fontSize=10.5,
                        leading=15.5, textColor=BODY_TEXT, spaceAfter=4, spaceBefore=0)
    S['sb_light']  = ParagraphStyle('sb_light',  fontName=F_LIGHT,  fontSize=9.5,
                        leading=14,   textColor=BODY_TEXT, spaceAfter=3, spaceBefore=0)
    S['sb_bold']   = ParagraphStyle('sb_bold',   fontName=F_BOLD,   fontSize=9.5,
                        leading=14,   textColor=BODY_TEXT, spaceAfter=3, spaceBefore=0)
    S['sb_green']  = ParagraphStyle('sb_green',  fontName=F_BOLD,   fontSize=9.5,
                        leading=14,   textColor=GREEN,     spaceAfter=3, spaceBefore=0)
    S['sb_italic'] = ParagraphStyle('sb_italic', fontName=F_REG_I,  fontSize=9.5,
                        leading=14,   textColor=BODY_TEXT, spaceAfter=0, spaceBefore=0)

    S['series_closer'] = ParagraphStyle('series_closer', fontName=F_BOLD,
                        fontSize=10.5, leading=15, textColor=BODY_TEXT,
                        spaceAfter=0, spaceBefore=12)
    return S


# ═════════════════════════════════════════════════════════════════════════════
# FLOWABLES
# ═════════════════════════════════════════════════════════════════════════════

class GreenRule(Flowable):
    def __init__(self,t=1.0,sb=4,sa=8):
        super().__init__(); self.t=t; self.sb=sb; self.sa=sa
    def wrap(self,w,h): self._w=w; return w,self.t+self.sb+self.sa
    def draw(self):
        self.canv.setFillColor(GREEN)
        self.canv.rect(0,self.sa,self._w,self.t,fill=1,stroke=0)


class NoteBox(Flowable):
    """Green-bar callout — paper content. Regular weight at 9.5pt."""
    def __init__(self,paras,pad=10):
        super().__init__(); self.paras=paras; self.pad=pad
    def wrap(self,aw,ah):
        self._w=aw; iw=aw-self.pad*2-5
        h=self.pad
        for p in self.paras:
            _,ph=p.wrap(iw,ah); h+=ph+getattr(p.style,'spaceAfter',5)
        h+=self.pad; self.height=h; return aw,h
    def draw(self):
        c=self.canv
        c.setFillColor(NOTE_BG); c.rect(0,0,self._w,self.height,fill=1,stroke=0)
        c.setFillColor(GREEN);   c.rect(0,0,4,self.height,fill=1,stroke=0)
        iw=self._w-self.pad*2-5; y=self.height-self.pad
        for p in self.paras:
            _,ph=p.wrap(iw,9999); y-=ph
            p.drawOn(c,5+self.pad,y); y-=getattr(p.style,'spaceAfter',5)


class ElevatedBlockquote(Flowable):
    """Green left rule, indented Regular Italic, final line in green."""
    def __init__(self,body_paras,close_para,pad_v=10,pad_l=12):
        super().__init__()
        self.body_paras=body_paras; self.close_para=close_para
        self.pad_v=pad_v; self.pad_l=pad_l
    def wrap(self,aw,ah):
        self._w=aw; iw=aw-self.pad_l-8
        h=self.pad_v
        for p in self.body_paras:
            _,ph=p.wrap(iw,ah); h+=ph+getattr(p.style,'spaceAfter',5)
        _,ph=self.close_para.wrap(iw,ah)
        h+=ph+self.pad_v; self.height=h; return aw,h
    def draw(self):
        c=self.canv
        c.setFillColor(GREEN); c.rect(0,0,2,self.height,fill=1,stroke=0)
        iw=self._w-self.pad_l-8; y=self.height-self.pad_v
        for p in self.body_paras:
            _,ph=p.wrap(iw,9999); y-=ph
            p.drawOn(c,self.pad_l,y); y-=getattr(p.style,'spaceAfter',5)
        _,ph=self.close_para.wrap(iw,9999); y-=ph
        self.close_para.drawOn(c,self.pad_l,y)


class SeriesBox(Flowable):
    """Grey-bordered context box. Accepts Paragraphs and Spacers."""
    def __init__(self,label,paras,pad=12,label_size=8):
        super().__init__(); self.label=label; self.paras=paras
        self.pad=pad; self.label_size=label_size
    def _item_height(self, item, iw, ah=9999):
        from reportlab.platypus import Spacer as _Sp
        if isinstance(item, _Sp):
            return item.height if hasattr(item,'height') else item._height
        _, h = item.wrap(iw, ah)
        return h
    def wrap(self,aw,ah):
        self._w=aw; iw=aw-self.pad*2
        h=self.pad+16+6
        for item in self.paras:
            from reportlab.platypus import Spacer as _Sp
            if isinstance(item, _Sp):
                h += item.height if hasattr(item,'height') else item._height
            else:
                _,ph=item.wrap(iw,ah); h+=ph+getattr(item.style,'spaceAfter',3)
        h+=self.pad; self.height=h; return aw,h
    def draw(self):
        from reportlab.platypus import Spacer as _Sp
        c=self.canv
        c.setFillColor(SERIES_BG); c.rect(0,0,self._w,self.height,fill=1,stroke=0)
        c.setStrokeColor(SERIES_BDR); c.setLineWidth(0.75)
        c.rect(0,0,self._w,self.height,fill=0,stroke=1)
        c.setFillColor(GREY_TEXT); c.setFont(F_BOLD, self.label_size)
        c.drawString(self.pad,self.height-self.pad-self.label_size,self.label)
        c.setFillColor(SERIES_BDR)
        c.rect(self.pad,self.height-self.pad-self.label_size-5,
               self._w-self.pad*2,0.5,fill=1,stroke=0)
        iw=self._w-self.pad*2; y=self.height-self.pad-self.label_size-11
        for item in self.paras:
            if isinstance(item, _Sp):
                sp_h = item.height if hasattr(item,'height') else item._height
                y -= sp_h
            else:
                _,ph=item.wrap(iw,9999); y-=ph
                item.drawOn(c,self.pad,y); y-=getattr(item.style,'spaceAfter',3)


class SectionHeader(Flowable):
    """Bold header with green underline."""
    def __init__(self,text,fs=12.5):
        super().__init__(); self.text=text; self.fs=fs
    def wrap(self,w,h):
        self._w=w; self.height=self.fs*1.3+8+12; return w,self.height
    def draw(self):
        c=self.canv
        c.setFillColor(BODY_TEXT); c.setFont(F_BOLD,self.fs)
        c.drawString(0,self.height-self.fs*1.3,self.text)
        c.setFillColor(GREEN)
        c.rect(0,self.height-self.fs*1.3-4,self._w,1.2,fill=1,stroke=0)


# ═════════════════════════════════════════════════════════════════════════════
# DOCUMENT BUILDER
# ═════════════════════════════════════════════════════════════════════════════

STAMP_IMG = '/home/claude/stamp_graphic.png'

def draw_stamp(c, cx, cy, angle=-12):
    """
    Embed the PIL-generated rubber stamp PNG, rotated, within the photo area.
    cx, cy = centre point of stamp in PDF coordinates.
    """
    if not os.path.exists(STAMP_IMG):
        return
    # Stamp dimensions in PDF points (380x240px → 130x82pt)
    sw, sh = 132, 92      # 380x265 px aspect
    c.saveState()
    c.translate(cx, cy)
    c.rotate(angle)
    c.drawImage(STAMP_IMG, -sw/2, -sh/2,
                width=sw, height=sh, mask='auto')
    c.restoreState()


def build_document(output_path, cover_title, ref, photo_desc,
                   series_num, preface_story, content_story,
                   photo_path=None):
    from io import BytesIO
    from pypdf import PdfWriter, PdfReader

    _pn[0]=2
    int_buf=BytesIO()

    top_f=Frame(MARGIN_L,BODY_TOP-TOP_H,BODY_W,TOP_H,
                leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='top')
    lp1  =Frame(MARGIN_L,MARGIN_B,COL_W,COL_H_P1,
                leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='lp1')
    rp1  =Frame(MARGIN_L+COL_W+COL_GAP,MARGIN_B,COL_W,COL_H_P1,
                leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='rp1')
    lpN  =Frame(MARGIN_L,MARGIN_B,COL_W,BODY_H,
                leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='l')
    rpN  =Frame(MARGIN_L+COL_W+COL_GAP,MARGIN_B,COL_W,BODY_H,
                leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='r')

    doc=BaseDocTemplate(int_buf,pagesize=A4,
        leftMargin=MARGIN_L,rightMargin=MARGIN_R,
        topMargin=HEADER_H+HEADER_RL+18,bottomMargin=MARGIN_B)
    doc.addPageTemplates([
        PageTemplate(id='first',  frames=[top_f,lp1,rp1], onPage=_chrome),
        PageTemplate(id='content',frames=[lpN,rpN],        onPage=_chrome),
    ])

    story=([NextPageTemplate('content')]
           + preface_story
           + [HRFlowable(width="100%",thickness=0.5,color=RULE_GREY,
                         spaceAfter=10,spaceBefore=8)]
           + content_story)
    doc.build(story)

    cov_buf=BytesIO()
    cv=canvas.Canvas(cov_buf,pagesize=A4)
    draw_cover(cv,cover_title,ref,photo_desc,series_num,photo_path=photo_path)
    cv.save()

    w=PdfWriter()
    for p in PdfReader(cov_buf).pages: w.add_page(p)
    for p in PdfReader(int_buf).pages: w.add_page(p)
    os.makedirs(os.path.dirname(output_path),exist_ok=True)
    with open(output_path,'wb') as f: w.write(f)
    print(f"Built: {output_path}  ({len(w.pages)} pages)")
