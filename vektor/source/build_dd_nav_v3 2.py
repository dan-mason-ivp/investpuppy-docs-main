"""
Vektor DD Navigation Guide — updated to include Founding Mandate Programme document.
Matches original visual style exactly.
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

W, H   = A4
ML = MR = 22*mm
MT1    = 16*mm
MT2    = 46*mm
MB     = 20*mm
COL_W  = W - ML - MR
LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png')
DATE   = 'May 2026'
REF    = 'IP-DDG-260501-2.0'
SUB    = 'Due Diligence Navigation Guide'


def S():
    s = {}
    s['tag'] = ParagraphStyle('tag', fontName='Helvetica', fontSize=7,
        textColor=WARM_GREY, leading=11, spaceAfter=4, letterSpacing=4)
    s['sec'] = ParagraphStyle('sec', fontName='Helvetica-Bold', fontSize=16,
        textColor=PLATINUM, leading=22, spaceAfter=4)
    s['sec_sub'] = ParagraphStyle('sec_sub', fontName='Helvetica-Oblique',
        fontSize=10, textColor=WARM_GREY, leading=15, spaceAfter=10)
    s['doc_name'] = ParagraphStyle('doc_name', fontName='Helvetica-Bold',
        fontSize=10, textColor=GOLD, leading=15, spaceAfter=2, spaceBefore=10)
    s['doc_q'] = ParagraphStyle('doc_q', fontName='Helvetica-Oblique',
        fontSize=9, textColor=WARM_GREY, leading=14, spaceAfter=4)
    s['doc_body'] = ParagraphStyle('doc_body', fontName='Helvetica',
        fontSize=9.5, textColor=OFF_WHITE, leading=15, spaceAfter=2)
    s['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5,
        textColor=OFF_WHITE, leading=17, spaceAfter=8, alignment=TA_JUSTIFY)
    s['footer'] = ParagraphStyle('footer', fontName='Helvetica', fontSize=6.5,
        textColor=colors.HexColor('#444440'), alignment=TA_CENTER, leading=10)
    s['wp_ref'] = ParagraphStyle('wp_ref', fontName='Helvetica', fontSize=7.5,
        textColor=colors.HexColor('#555550'), alignment=TA_CENTER, leading=11)
    s['tbl_hdr'] = ParagraphStyle('tbl_hdr', fontName='Helvetica-Bold',
        fontSize=8, textColor=PLATINUM, leading=12)
    s['tbl_step'] = ParagraphStyle('tbl_step', fontName='Helvetica-Bold',
        fontSize=9, textColor=GOLD, leading=13)
    s['tbl_doc'] = ParagraphStyle('tbl_doc', fontName='Helvetica-Bold',
        fontSize=8.5, textColor=OFF_WHITE, leading=12)
    s['tbl_body'] = ParagraphStyle('tbl_body', fontName='Helvetica',
        fontSize=8.5, textColor=OFF_WHITE, leading=12, alignment=TA_JUSTIFY)
    s['new_badge'] = ParagraphStyle('new_badge', fontName='Helvetica-Bold',
        fontSize=7, textColor=GOLD, leading=10)
    return s


class HRule(Flowable):
    def __init__(self, w, c=RULE_MIN, t=0.5, sa=5, sb=5):
        Flowable.__init__(self)
        self.rw=w; self.c=c; self.t=t; self._sa=sa; self._sb=sb
        self.height = sa+t+sb
    def wrap(self, aw, ah): return self.rw, self.height
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        self.canv.line(0, self._sb+self.t/2, self.rw, self._sb+self.t/2)


class NoteBox(Flowable):
    def __init__(self, w, text, style):
        Flowable.__init__(self)
        self._w=w; self._p=Paragraph(text, style)
        self._ph=15; self._pv=13; self._bw=4
        self._iw = w - self._bw - self._ph*2
    def wrap(self, aw, ah):
        _, h = self._p.wrap(self._iw, ah)
        self.height = h + self._pv*2
        return self._w, self.height
    def draw(self):
        c=self.canv; c.saveState()
        c.setFillColor(NOTE_BG); c.setStrokeColor(CARD_EDGE); c.setLineWidth(0.4)
        c.roundRect(0, 0, self._w, self.height, 3, fill=1, stroke=1)
        c.setFillColor(RULE_MAJ); c.roundRect(0,0,self._bw,self.height,2,fill=1,stroke=0)
        self._p.wrap(self._iw, self.height)
        self._p.drawOn(c, self._bw+self._ph, self._pv)
        c.restoreState()


def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    from reportlab.lib.utils import ImageReader
    try:
        img = ImageReader(LOGO); iw,ih = img.getSize()
        lw=min(W*0.62,320); lh=lw*ih/iw; lx=(W-lw)/2; ly=H*0.52
        canvas.drawImage(LOGO, lx, ly-lh, lw, lh, mask='auto', preserveAspectRatio=True)
        ry = ly-lh-14
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8)
        canvas.line(ML, ry, W-MR, ry)
        canvas.setFont('Helvetica-Bold', 22); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2, ry-40, 'Due Diligence')
        canvas.drawCentredString(W/2, ry-66, 'Navigation Guide')
        canvas.setFont('Helvetica', 10); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2, ry-90,
            'Which document answers which question \u2014 a reading guide for')
        canvas.drawCentredString(W/2, ry-104,
            'institutional partners working through the full Vektor document suite.')
    except Exception as e: print(e)
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4)
    canvas.line(ML, 36*mm, W-MR, 36*mm)
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(WARM_GREY)
    canvas.drawCentredString(W/2, 28*mm, 'For Founding Mandate partners and institutional due diligence teams')
    canvas.setFont('Helvetica', 7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W/2, 22*mm, REF); canvas.drawCentredString(W/2, 16*mm, DATE)
    try:
        ip_w=38*mm; ip_h=ip_w/IP_H_RATIO
        canvas.drawImage(IP_H,ML,9*mm,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.restoreState()


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0,0,W,H,fill=1,stroke=0)
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.3)
    canvas.line(ML, MB-2, W-MR, MB-2)
    canvas.setFont('Helvetica', 6.5)
    canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawCentredString(W/2, MB-11,
        f'Vektor by InvestPuppy  \u00b7  investpuppy.com  \u00b7  VEKTOR  \u00b7  INVESTPUPPY.COM  \u00b7  {DATE}')
    canvas.restoreState()


def build():
    out = '/home/claude/investpuppy/vektor/output/pdf/vk5-dd-navigation-guide.pdf'
    s = S()

    f_cover = Frame(0,0,W,H,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='cover')
    f_body  = Frame(ML, MB, COL_W, H-MT1-MB, id='body')

    doc = BaseDocTemplate(out, pagesize=A4,
        leftMargin=ML, rightMargin=MR, topMargin=MT1, bottomMargin=MB,
        title='Vektor Due Diligence Navigation Guide',
        author='InvestPuppy')
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=[f_cover], onPage=draw_cover),
        PageTemplate(id='Body',  frames=[f_body],  onPage=draw_page),
    ])

    story = []
    story.append(Spacer(1,1))
    story.append(NextPageTemplate('Body'))
    story.append(PageBreak())

    # HOW TO USE
    story.append(Paragraph('HOW TO USE THIS GUIDE', s['tag']))
    story.append(NoteBox(COL_W,
        'The Vektor document suite now contains twenty documents, including four new additions in vk5. '
        'This guide tells you which one to read in '
        'response to the question you are actually trying to answer. It is not a catalogue \u2014 it is a '
        'navigation tool. The recommended sequence for a Founding Mandate due diligence process is at the end.',
        s['body']))
    story.append(Spacer(1, 14))

    # ── COMMERCIAL ──────────────────────────────────────────────────────────────
    story.append(HRule(COL_W, RULE_MAJ, 1.0, 2, 6))
    story.append(Paragraph('IF YOUR QUESTION IS COMMERCIAL', s['sec']))
    story.append(Paragraph('Start here. These documents make the commercial case.', s['sec_sub']))

    def doc_entry(name, answers_line, body, story, s, new=False):
        if new:
            story.append(Paragraph(f'{name}\u2002\u2002\u25b6 NEW', ParagraphStyle('dn_new',
                fontName='Helvetica-Bold', fontSize=10, textColor=GOLD,
                leading=15, spaceAfter=2, spaceBefore=10)))
        else:
            story.append(Paragraph(name, s['doc_name']))
        story.append(Paragraph(f'Answers: {answers_line}', s['doc_q']))
        story.append(Paragraph(body, s['doc_body']))

    doc_entry('Vektor at a Glance',
        'What is Vektor, and why does it exist?',
        'One page. Start here for any first conversation.',
        story, s)

    doc_entry('What We Are Not',
        'What does Vektor not do? What are the scope limitations and honest disclosures?',
        'Nine explicit statements of limitation, followed by six IS statements. '
        'Read this before the brochure. The most differentiated document in the suite. '
        'In START HERE folder and QUICK-SEND. Reference: IP-WVIN-260508-1.0.',
        story, s)

    doc_entry('Why Not the Incumbents?',
        'How does Vektor compare to Bloomberg PORT, FactSet, Excel, robo-advisory, or building in-house?',
        'Honest assessment of five alternatives. Written by practitioners who used these platforms '
        'professionally before building Vektor. Includes honest notes where an alternative may be the '
        'better answer. Reference: IP-WNIC-260508-1.0.',
        story, s)

    doc_entry('Platform Brochure',
        'What does Vektor actually do, step by step?',
        'The eleven-step workflow with screenshots. The most complete overview of the platform in operation.',
        story, s)

    doc_entry('Why Vektor',
        'What is the commercial argument for systematic portfolio management?',
        'The market problem, the DPM workflow, the Founding Mandate proposition. Contains a summary of the '
        'Founding Mandate Programme on page\u00a06.',
        story, s)

    doc_entry('Founding Mandate Programme',
        'What exactly is the Founding Mandate? What are the commercial terms, obligations, and programme mechanics?',
        'The complete programme specification: what partners receive, what they commit to, slot availability, '
        'the twelve-month founding period, and the three-step path to engagement. Read this after Why Vektor '
        'for the full programme detail. Reference: IP-FMP-260501-1.0.',
        story, s)

    doc_entry('The Vektor Brand Story',
        'Who built this and why?',
        'The origin story and the philosophy behind the platform.',
        story, s)

    story.append(Spacer(1, 14))

    # ── METHODOLOGICAL ───────────────────────────────────────────────────────────
    story.append(HRule(COL_W, RULE_MAJ, 1.0, 2, 6))
    story.append(Paragraph('IF YOUR QUESTION IS METHODOLOGICAL', s['sec']))
    story.append(Paragraph('How the quantitative engine works.', s['sec_sub']))

    doc_entry('WP-01: Quantitative Portfolio Construction',
        'How does the portfolio construction process work end to end?',
        'The foundational paper. Five-stage framework with a worked SGX example. Start here before reading '
        'any other white paper.',
        story, s)

    doc_entry('WP-02: Per-Instrument Signal Optimisation',
        'How does Vektor select the right indicator for each instrument?',
        'The grid search methodology and XGBoost validation layer.',
        story, s)

    doc_entry('WP-03: Capital Allocation Precision',
        'How do portfolio weights become actual share quantities?',
        'Lot rounding, cash buffer, and capital allocation efficiency.',
        story, s)

    doc_entry('WP-04: Technical Indicator Selection',
        'What are the six indicators, and how are parameters optimised?',
        'Full parameter space specification and overfitting controls.',
        story, s)

    doc_entry('WP-05: Multi-Currency Portfolio Infrastructure',
        'How does Vektor handle portfolios across multiple currencies?',
        'FX rate collection, position-level conversion, base currency configuration.',
        story, s)

    doc_entry('WP-10: Evaluating Performance Without a Track Record',
        'What metrics should I use to evaluate a systematic strategy?',
        'Sharpe ratio, drawdown, benchmark comparison, signal decay, walk-forward validation. '
        'Essential reading before reviewing any Vektor strategy output.',
        story, s)

    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # ── GOVERNANCE ───────────────────────────────────────────────────────────────
    story.append(HRule(COL_W, RULE_MAJ, 1.0, 2, 6))
    story.append(Paragraph('IF YOUR QUESTION IS ABOUT GOVERNANCE & COMPLIANCE', s['sec']))
    story.append(Paragraph('Controls, audit trail, and regulatory alignment.', s['sec_sub']))

    doc_entry('WP-06: Audit Trail & Compliance Architecture',
        'What is the audit trail? Who approves what?',
        'The three-role model, complete action logging, compliance architecture. '
        'The first white paper a compliance officer should read.',
        story, s)

    doc_entry('WP-08: AI as Instrument',
        'Where is AI used? Can the machine trade without human approval?',
        'Governing principle, human approval gates, MAS FEAT / SFC / FCA alignment.',
        story, s)

    doc_entry('WP-09: Risk & Limitation Disclosure',
        "What are the platform's risks and limitations?",
        'Fourteen identified risks across four categories with mitigations in place and those on the '
        'roadmap. Read before any risk committee presentation.',
        story, s)

    doc_entry('Mutual NDA',
        'What confidentiality terms govern our discussions?',
        'Singapore law primary. Requires review by qualified Singapore solicitor before use.',
        story, s)

    story.append(Spacer(1, 14))

    # ── TECHNICAL ────────────────────────────────────────────────────────────────
    story.append(HRule(COL_W, RULE_MAJ, 1.0, 2, 6))
    story.append(Paragraph('IF YOUR QUESTION IS TECHNICAL', s['sec']))
    story.append(Paragraph('Infrastructure, integration, and architecture.', s['sec_sub']))

    doc_entry('WP-07: Production Infrastructure & Technical Architecture',
        'How is the platform built? Can it integrate with our existing infrastructure?',
        'AWS service inventory, architecture diagram, decision log, data flows, integration patterns, '
        'region-agnostic deployment, and current deployment status. For CTOs and technical due diligence teams.',
        story, s)

    doc_entry('Workflow Integration Guide',
        'What does adopting Vektor mean for the way I work today?',
        'Task-by-task workflow map \u2014 what Vektor replaces, augments, and leaves unchanged. '
        'Covers Bloomberg integration, existing PMS connectivity, and the DPM without a PMS.',
        story, s)

    story.append(Spacer(1, 14))

    # ── OPERATIONAL ──────────────────────────────────────────────────────────────
    story.append(HRule(COL_W, RULE_MAJ, 1.0, 2, 6))
    story.append(Paragraph('IF YOUR QUESTION IS OPERATIONAL', s['sec']))
    story.append(Paragraph('Day-to-day use and getting started.', s['sec_sub']))

    doc_entry('Frequently Asked Questions',
        'Quick answers to the fifteen questions that come up in every conversation.',
        'Plain language. Two pages. Useful leave-behind for any meeting.',
        story, s)

    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # ── RECOMMENDED SEQUENCE ─────────────────────────────────────────────────────
    story.append(HRule(COL_W, RULE_MAJ, 1.0, 2, 6))
    story.append(Paragraph('RECOMMENDED SEQUENCE \u2014 FOUNDING MANDATE DUE DILIGENCE', s['sec']))
    story.append(Paragraph(
        'For a partner working through the full suite for the first time. '
        'Each step builds on the previous one.',
        s['sec_sub']))

    seq = [
        ('1',  'Vektor at a Glance',
         'Establish the platform\u2019s proposition and the problem it solves \u2014 in two minutes'),
        ('2',  'What We Are Not',
         'Read the explicit constraint list before the pitch. Honest self-limitation is the basis for everything that follows'),
        ('3',  'Why Not the Incumbents?',
         'Understand where Vektor sits relative to every serious alternative'),
        ('4',  'Platform Brochure',
         'Understand the full workflow and platform capability'),
        ('5',  'Why Vektor',
         'Evaluate the commercial argument and Founding Mandate summary'),
        ('6',  'Workflow Integration Guide',
         'Understand how Vektor fits your existing workflow before committing to the programme'),
        ('7 \u2605', 'Founding Mandate Programme',
         'Understand the full programme structure before entering due diligence'),
        ('8',  'WP-01: Quantitative Portfolio Construction',
         'Understand the quantitative methodology foundation'),
        ('9',  'WP-09: Risk & Limitation Disclosure',
         'Assess platform risk with full information before evaluating outputs'),
        ('10', 'WP-10: Evaluating Performance Without a Track Record',
         'Acquire the vocabulary to evaluate strategy outputs'),
        ('11', 'WP-06: Audit Trail & Compliance Architecture',
         'Review governance and audit trail'),
        ('12', 'WP-08: AI as Instrument',
         'Assess AI governance and regulatory alignment'),
        ('13', 'WP-07: Technical Architecture',
         'Technical due diligence \u2014 infrastructure and integration'),
        ('14', 'WP-02 through WP-05',
         'Deep methodology review as required'),
        ('15', 'Mutual NDA',
         'Establish confidentiality terms for detailed commercial discussions'),
    ]

    hrow = [Paragraph(h, s['tbl_hdr']) for h in ['STEP', 'DOCUMENT', 'PURPOSE']]
    rows = [hrow]
    for step, doc_name, purpose in seq:
        is_new = '\u2605' in step
        doc_p = Paragraph(doc_name,
            ParagraphStyle('dn_seq_new', fontName='Helvetica-Bold', fontSize=8.5,
                textColor=GOLD, leading=13)
            if is_new else s['tbl_doc'])
        rows.append([
            Paragraph(step, s['tbl_step']),
            doc_p,
            Paragraph(purpose, s['tbl_body']),
        ])

    t = Table(rows, colWidths=[14*mm, 64*mm, COL_W-78*mm], repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD_BG, colors.HexColor('#0F0F14')]),
        # Highlight FMP row (row 6)
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor('#161208')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, RULE_MIN),
        ('BOX', (0,0), (-1,-1), 0.4, CARD_EDGE),
        ('LINEAFTER', (0,0), (0,-1), 0.3, RULE_MIN),
        ('LINEAFTER', (1,0), (1,-1), 0.3, RULE_MIN),
        # Gold for FMP row only
        # Gold left border for FMP row
        ('LINEABOVE', (0,6), (-1,6), 0.5, GOLD),
        ('LINEBELOW', (0,6), (-1,6), 0.5, GOLD),
    ]))
    story.append(t)

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        'What We Are Not (IP-WVIN-260508-1.0) and Why Not the Incumbents? (IP-WNIC-260508-1.0) '
        'are in START HERE and QUICK-SEND folders. '
        '\u2605 Founding Mandate Programme (IP-FMP-260501-1.0) \u2014 read after Why Vektor.',
        ParagraphStyle('note', fontName='Helvetica-Oblique', fontSize=8,
            textColor=WARM_GREY, leading=12)))

    story.append(Spacer(1, 14))
    story.append(HRule(COL_W, RULE_MAJ, 1.0, 4, 4))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '<b>Note for UK-based readers.</b> '
        'Vektor is currently distributed in Singapore. UK distribution is subject to regulatory review. '
        'UK-based prospective partners should contact contact@investpuppy.com before proceeding '
        'beyond this guide. We will confirm what applies to your jurisdiction before any further '
        'documentation is shared.',
        s['body']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        'Questions not answered by any document in the suite should be directed to '
        'contact@investpuppy.com. All documents available at investpuppy.com.',
        s['body']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {REF}  \u00b7  Copyright 2026 InvestPuppy',
        s['wp_ref']))

    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    r = subprocess.run(['pdfinfo', out], capture_output=True, text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l or 'File' in l: print(l)

if __name__ == '__main__':
    build()
