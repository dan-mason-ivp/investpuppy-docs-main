import os as _os
_SCRIPT_DIR  = _os.path.dirname(_os.path.abspath(__file__))
_REPO_ROOT   = _os.path.dirname(_os.path.dirname(_SCRIPT_DIR))
_LOGOS       = _os.path.join(_REPO_ROOT, '_shared', 'logos')
_SCREENSHOTS = _os.path.join(_SCRIPT_DIR, 'screenshots')
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
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
RED_DIM = colors.HexColor('#7C3A3A')

W, H   = A4
ML = MR = 18*mm
MT = 20*mm
MB = 16*mm
LOGO   = '/home/claude/investpuppy/_shared/logos/IPHorizontalClear.png'
COL_W  = W - ML - MR

def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9, textColor=OFF_W,
             leading=14, spaceAfter=0, spaceBefore=0, backColor=None)
    d.update(kw)
    return ParagraphStyle(name, **d)

s_tag   = S('tag', fontSize=7, textColor=W_GREY, letterSpacing=2.5)
s_cover1= S('cov1', fontName='Helvetica-Bold', fontSize=24, textColor=PLAT,
            leading=28, spaceAfter=4)
s_cover2= S('cov2', fontSize=10.5, textColor=OFF_W, leading=17)
s_intro = S('intro', fontSize=10, textColor=OFF_W, leading=16)
s_prin_n= S('prinn', fontName='Helvetica-Bold', fontSize=7,
            textColor=GOLD, leading=10, letterSpacing=2)
s_prin_t= S('print', fontName='Helvetica-Bold', fontSize=11, textColor=PLAT,
            leading=15, spaceAfter=3)
s_prin_b= S('prinb', fontSize=9.5, textColor=OFF_W, leading=15)
s_ex_h  = S('exh', fontName='Helvetica-Bold', fontSize=8,
            textColor=W_GREY, leading=11, letterSpacing=1.5)
s_do    = S('do', fontSize=9, textColor=OFF_W, leading=14)
s_dont  = S('dont', fontSize=9, textColor=W_GREY, leading=14)
s_ref   = S('ref', fontSize=7.5, textColor=W_GREY, leading=11)

def p(txt, st): return Paragraph(txt, st)
def sp(h=6):    return Spacer(1, h)
def hr(c=RULE_MJ, t=0.4, tb=3, bb=6):
    return HRFlowable(width=COL_W, color=c, thickness=t,
                      spaceBefore=tb, spaceAfter=bb)

def principle(num, title, body, do_list, dont_list):
    """Build a single principle block with do/don't examples."""
    items = []
    items.append([p(f'PRINCIPLE {num:02d}', s_prin_n)])
    items.append([p(title, s_prin_t)])
    items.append([p(body, s_prin_b)])
    items.append([sp(4)])

    # Do / Don't side by side
    do_rows   = [[p('\u2713  DO', S('doh', fontName='Helvetica-Bold', fontSize=7.5,
                    textColor=GREEN, leading=10, letterSpacing=1))]]
    dont_rows = [[p('\u2717  DON\u2019T', S('dnh', fontName='Helvetica-Bold', fontSize=7.5,
                    textColor=RED_DIM, leading=10, letterSpacing=1))]]
    for d in do_list:
        do_rows.append([p(f'\u2014 {d}', s_do)])
    for d in dont_list:
        dont_rows.append([p(f'\u2014 {d}', s_dont)])

    col = (COL_W - 4*mm) / 2
    do_t = Table(do_rows, colWidths=[col])
    do_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NOTE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBEFORE', (0,0), (-1,-1), 2, GREEN),
        ('BOX', (0,0), (-1,-1), 0.3, RULE_MN),
    ]))
    dn_t = Table(dont_rows, colWidths=[col])
    dn_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NOTE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBEFORE', (0,0), (-1,-1), 2, RED_DIM),
        ('BOX', (0,0), (-1,-1), 0.3, RULE_MN),
    ]))
    pair = Table([[do_t, dn_t]], colWidths=[col, col],
                 spaceBefore=0, spaceAfter=0)
    pair.setStyle(TableStyle([
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('INNERGRID', (0,0), (-1,-1), 4, BG),
    ]))
    items.append([pair])

    outer = Table(items, colWidths=[COL_W])
    outer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CARD),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('LINEBEFORE', (0,0), (-1,-1), 2.5, GOLD),
        ('BOX', (0,0), (-1,-1), 0.3, RULE_MN),
    ]))
    return outer

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
            'IP-BVG-260508-1.0  \u00b7  VEKTOR BY INVESTPUPPY  \u00b7  INTERNAL  \u00b7  MAY 2026')
        c.restoreState()

class LaterTpl(PageTemplate):
    def beforeDrawPage(self, c, doc):
        c.saveState()
        c.setFillColor(BG); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(GOLD); c.rect(ML,H-11*mm,COL_W,0.8,fill=1,stroke=0)
        c.setFont('Helvetica',7); c.setFillColor(W_GREY)
        c.drawString(ML,H-9*mm,'INVESTPUPPY BRAND VOICE GUIDE')
        c.drawRightString(W-MR,H-9*mm,'IP-BVG-260508-1.0  \u00b7  INTERNAL')
        ip = ImageReader(LOGO); iw,ih = ip.getSize()
        lw=28*mm; lh=lw*ih/iw
        c.drawImage(LOGO,ML,1*mm,lw,lh,mask='auto')
        c.setFillColor(RULE_MJ)
        c.rect(ML,MB-2,COL_W,0.3,fill=1,stroke=0)
        c.setFont('Helvetica',6.5); c.setFillColor(W_GREY)
        c.drawRightString(W-MR,1*mm+lh/2-2,'investpuppy.com')
        c.drawCentredString(W/2,MB-7*mm,str(doc.page))
        c.restoreState()

OUT = '/home/claude/investpuppy/vektor/output/pdf/vk4-brand-voice-guide.pdf'
doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=ML, rightMargin=MR,
                      topMargin=MT, bottomMargin=MB+6*mm)
cf = Frame(ML,MB+6*mm,COL_W,H-MT-MB-6*mm,
           leftPadding=0,rightPadding=0,topPadding=38*mm,bottomPadding=0)
lf = Frame(ML,MB+6*mm,COL_W,H-MT-MB,
           leftPadding=0,rightPadding=0,topPadding=6*mm,bottomPadding=0)
doc.addPageTemplates([CoverTpl('Cover',[cf]), LaterTpl('Later',[lf])])

story = []

# ── COVER ─────────────────────────────────────────────────────────────────
story.append(p('INVESTPUPPY', s_cover1))
story.append(p('Brand Voice Guide', S('cov2', fontName='Helvetica-Bold',
    fontSize=16, textColor=GOLD, leading=20, spaceAfter=10)))
story.append(hr(GOLD, 0.8, 2, 10))
story.append(p(
    'How InvestPuppy communicates. What the voice is, what it is not, '
    'and how to apply it consistently across every touchpoint \u2014 '
    'from first contact to due diligence to internal communications.',
    S('ci', fontSize=10.5, textColor=OFF_W, leading=17, spaceAfter=8)))
story.append(p(
    'Every person who communicates on behalf of InvestPuppy or Vektor '
    'should read this document before writing anything.',
    S('ciq', fontName='Helvetica-Oblique', fontSize=9.5,
      textColor=W_GREY, leading=15)))

story.append(NextPageTemplate('Later'))
story.append(PageBreak())

# ── PAGE 2: THE INVESTPUPPY STANCE ────────────────────────────────────────
story.append(p('THE INVESTPUPPY STANCE', s_tag))
story.append(hr(GOLD, 0.8, 2, 10))
story.append(p(
    'Before the principles. Before the voice. The posture that produces both.',
    S('fp', fontName='Helvetica-Bold', fontSize=13, textColor=PLAT,
      leading=18, spaceAfter=10)))

# Founding thought — centred pull quote, floating above the structure
story.append(sp(14))
story.append(p(
    '\u201cThere\u2019s got to be a better way\u2026\u201d',
    S('founding', fontName='Helvetica-BoldOblique', fontSize=23,
      textColor=PLAT, leading=30, alignment=TA_CENTER, spaceAfter=0)))
story.append(sp(20))

preamble = Table([
    [p('This philosophy was not assembled from a marketing guide. '
       'It was not learned from a textbook or arrived at through brand workshops.',
       S('pre1', fontName='Helvetica-Oblique', fontSize=10,
         textColor=W_GREY, leading=16, spaceAfter=8))],
    [p('It evolved from decades of experiencing the traditional way \u2014 '
       'the overselling, the selective disclosure, the capability claims that outran '
       'the evidence \u2014 and thinking, every time: there must be a better way.',
       S('pre2', fontSize=10, textColor=OFF_W, leading=16, spaceAfter=8))],
    [p('The InvestPuppy Stance is what happens when the people who built this platform '
       'decided to do the opposite of everything that frustrated them as practitioners. '
       'Not as a positioning strategy. As a professional conviction built over years, '
       'in rooms where the wrong way was the standard way.',
       S('pre3', fontSize=10, textColor=OFF_W, leading=16, spaceAfter=8))],
    [p('Vektor exists for the same reason. Not because a market opportunity was identified '
       '\u2014 because a professional frustration became a decision.',
       S('pre4', fontName='Helvetica-Bold', fontSize=10,
         textColor=PLAT, leading=16, spaceAfter=8))],
    [p('That is where the honesty comes from.',
       S('pre5', fontName='Helvetica-BoldOblique', fontSize=11,
         textColor=GOLD, leading=16, spaceAfter=0))],
], colWidths=[COL_W])
preamble.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,-1), colors.HexColor('#0D0D12')),
    ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
    ('LEFTPADDING',(0,0),(-1,-1),16),('RIGHTPADDING',(0,0),(-1,-1),16),
    ('LINEBEFORE',(0,0),(-1,-1),3,GOLD),
    ('BOX',(0,0),(-1,-1),0.4,RULE_MN),
]))
story.append(preamble)
story.append(sp(12))

stance = Table([
    [p('WHEN CRITICISM ARRIVES', S('st_tag', fontName='Helvetica-Bold',
       fontSize=8, textColor=GOLD, leading=11, letterSpacing=2))],
    [p(
        'When criticism arrives \u2014 from the market, from a prospect, from a reviewer, '
        'from your own honest assessment \u2014 the InvestPuppy response is not to defend, '
        'redirect, or minimise. It is to ask a different question:',
        S('st_b', fontSize=10, textColor=OFF_W, leading=16, spaceAfter=6))],
    [p(
        '\u201cWhat does this give us?\u201d',
        S('st_q', fontName='Helvetica-BoldOblique', fontSize=14,
          textColor=PLAT, leading=18, spaceAfter=6))],
    [p(
        'The name was a problem. It became the most memorable signal in the category. '
        'The absence of a track record was a vulnerability. It became the most trusted '
        'sentence in the suite. The limitations of the current product were risks to manage. '
        'They became a document that no competitor will write.',
        S('st_b2', fontSize=9.5, textColor=OFF_W, leading=15, spaceAfter=8))],
    [p(
        'This is not optimism. It is method. Every criticism contains information. '
        'Most firms suppress that information. InvestPuppy uses it.',
        S('st_b3', fontName='Helvetica-Bold', fontSize=9.5,
          textColor=PLAT, leading=15, spaceAfter=8))],
    [p(
        'This is where the honesty comes from. Not from a commitment to transparency '
        'in the abstract \u2014 but from a genuine conviction that what is true, '
        'including what is uncomfortable, is always more useful than what sounds good.',
        S('st_close', fontName='Helvetica-Oblique', fontSize=9.5,
          textColor=W_GREY, leading=15, spaceAfter=0))],
], colWidths=[COL_W])
stance.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,-1), NOTE),
    ('TOPPADDING', (0,0),(-1,-1), 12),
    ('BOTTOMPADDING', (0,0),(-1,-1), 12),
    ('LEFTPADDING', (0,0),(-1,-1), 16),
    ('RIGHTPADDING', (0,0),(-1,-1), 16),
    ('LINEBEFORE', (0,0),(-1,-1), 3, GOLD),
    ('BOX', (0,0),(-1,-1), 0.4, RULE_MN),
]))
story.append(stance)
story.append(sp(12))

# Three steps
steps = [
    ('01', 'See it clearly.',
     'Do not look away from a criticism. Do not minimise it. '
     'Do not redirect toward something more comfortable. '
     'The criticism is information. Treat it as such.'),
    ('02', 'Own it completely.',
     'No qualifying, no deflecting, no "but on the other hand". '
     'If the criticism is valid, say so directly. '
     'The InvestPuppy name. The absent track record. The current equity-only scope. '
     'All owned, all stated first, all without apology.'),
    ('03', 'Ask what it gives you.',
     'This is the step that separates the stance from ordinary honesty. '
     'Not just: what do we do with this criticism? But: what does this criticism '
     'make possible that defensiveness would not? '
     'Every time InvestPuppy has asked this question, '
     'the answer has been better than the alternative.'),
]
step_rows = []
for num, title, body in steps:
    num_cell = Table([[p(num, S('sn', fontName='Helvetica-Bold', fontSize=14,
        textColor=BG, leading=18, alignment=TA_CENTER))]],
        colWidths=[10*mm], rowHeights=[10*mm])
    num_cell.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), GOLD),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
    ]))
    body_cell = Table([
        [p(title, S('steptit', fontName='Helvetica-Bold', fontSize=10,
                    textColor=PLAT, leading=14, spaceAfter=3))],
        [p(body, S('stepbod', fontSize=9, textColor=OFF_W, leading=14))],
    ], colWidths=[COL_W - 14*mm])
    body_cell.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), CARD),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),10),
    ]))
    row = Table([[num_cell, body_cell]], colWidths=[10*mm, COL_W - 10*mm])
    row.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ('BOX',(0,0),(-1,-1),0.3,RULE_MN),
    ]))
    step_rows.append(row)

for row in step_rows:
    story.append(row)
    story.append(sp(4))

story.append(PageBreak())

# ── PAGE 3: THE CORE PRINCIPLE ─────────────────────────────────────────────
story.append(p('THE FOUNDATION', s_tag))
story.append(hr(GOLD, 0.8, 2, 10))
story.append(p(
    'The stance produces one governing principle.',
    S('fp', fontName='Helvetica-Bold', fontSize=13, textColor=PLAT,
      leading=18, spaceAfter=8)))

core = Table([
    [p('HONEST BY DESIGN', S('core_tag', fontName='Helvetica-Bold',
       fontSize=8, textColor=GOLD, leading=11, letterSpacing=2))],
    [p(
        'Say the uncomfortable thing first. Capability claims follow evidence, '
        'not precede it. Acknowledge limitations before they are asked about. '
        'Answer the hard question directly. Never present a selective version '
        'of the truth.',
        S('core_b', fontSize=10.5, textColor=PLAT, leading=17, spaceAfter=8))],
    [p(
        'This is not a communications strategy. It is a behavioural standard. '
        'Every document, every conversation, every message should pass a single test: '
        '\u2018Are we being as honest here as we are capable of being?\u2019',
        S('core_q', fontName='Helvetica-Oblique', fontSize=9.5,
          textColor=W_GREY, leading=15, spaceAfter=0))],
], colWidths=[COL_W])
core.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,-1), NOTE),
    ('TOPPADDING', (0,0),(-1,-1), 14),
    ('BOTTOMPADDING', (0,0),(-1,-1), 14),
    ('LEFTPADDING', (0,0),(-1,-1), 16),
    ('RIGHTPADDING', (0,0),(-1,-1), 16),
    ('LINEBEFORE', (0,0),(-1,-1), 3, GOLD),
    ('BOX', (0,0),(-1,-1), 0.4, RULE_MN),
]))
story.append(core)
story.append(sp(14))

story.append(p('WHY THIS MATTERS FOR INVESTPUPPY SPECIFICALLY', s_tag))
story.append(hr(RULE_MJ, 0.4, 2, 8))
story.append(p(
    'Boutique DPMs, family office principals, and independent wealth managers '
    'have been oversold to their entire careers. Their default posture in any '
    'vendor conversation is: <i>what are they not telling me?</i> The InvestPuppy '
    'voice resolves this before it forms. By the time a prospect reaches the due '
    'diligence stage, the answer to that question should already be: <i>nothing. '
    'They told us everything, including the things we didn\u2019t ask about.</i>',
    S('why', fontSize=9.5, textColor=OFF_W, leading=16, spaceAfter=10)))
story.append(p(
    'Honesty is also the brand characteristic that cannot be replicated without '
    'actually being honest. A competitor can copy the methodology. '
    'They cannot copy a culture of institutional integrity that is visible '
    'in every communication from day one.',
    S('why2', fontSize=9.5, textColor=OFF_W, leading=16)))

story.append(PageBreak())

# ── PAGES 3-4: TEN PRINCIPLES ─────────────────────────────────────────────
story.append(p('TEN PRINCIPLES', s_tag))
story.append(hr(GOLD, 0.8, 2, 12))

PRINCIPLES = [
    (1, 'Honest before impressive.',
     'Lead with what is true, including what is inconvenient. '
     'Capability claims come after evidence, not before it. '
     'If the full picture includes a limitation, include the limitation first.',
     ['We don\u2019t yet have a live track record. Here is what we have instead.',
      '99.94% is an operational metric. It is not a performance claim.',
      'Vektor currently supports listed equities only.'],
     ['Vektor delivers exceptional risk-adjusted returns.',
      'Our proprietary AI generates market-beating signals.',
      'The most advanced platform in its class.']),

    (2, 'Specific, not general.',
     'Replace every vague claim with a precise one. '
     'If you cannot be specific, you probably should not be making the claim.',
     ['10,000 portfolio configurations map the efficient frontier.',
      '99.94% capital allocation efficiency at live prices.',
      '6 indicators per instrument, 3-year daily history, XGBoost validation.'],
     ['Highly efficient capital deployment.',
      'Rigorous signal selection methodology.',
      'Sophisticated risk management framework.']),

    (3, 'Confident without apology.',
     'State limitations directly and move on. Do not apologise for the '
     'company name, the stage of development, the scope of the product, '
     'or the honest answer to a hard question. '
     'Confidence and honesty are not in tension.',
     ['Vektor does not yet have a live track record.',
      'Yes, the company is called InvestPuppy.',
      'We are currently in IBKR simulation mode.'],
     ['We acknowledge that our limited history may be a concern...',
      'Despite the unconventional name...',
      'While we are still in early stages...']),

    (4, 'Pre-emptive, not reactive.',
     'Raise the difficult question before it is asked. '
     'Answer the objection before the prospect forms it. '
     'The document \u2018What Vektor Is Not\u2019 exists for this reason.',
     ['We recommend reading WP-09, which covers what can go wrong.',
      'We do not yet support fixed income or alternatives.',
      'Here are the scenarios under which this approach underperforms.'],
     ['\u2014 (silence on limitations, waiting to be asked)',
      'As with any systematic approach, results may vary.',
      'Past performance is not indicative of future results.']),

    (5, 'Dry, not breathless.',
     'No exclamation marks. No superlatives. No \u2018exciting\u2019, '
     '\u2018revolutionary\u2019, \u2018game-changing\u2019, or \u2018cutting-edge\u2019. '
     'Let the content generate the excitement. '
     'If the content requires amplification to be impressive, the content is not impressive.',
     ['The platform runs 10,000 portfolio configurations per strategy.',
      'Multi-mandate is live. Different clients, different mandates, concurrently.',
      'One Size Fits None.'],
     ['We are thrilled to introduce the most exciting development in...',
      'Vektor is revolutionising the way boutique DPMs...',
      'Our cutting-edge, game-changing systematic approach!']),

    (6, 'Irreverent about ourselves, rigorous about the work.',
     'The company is called InvestPuppy. The methodology is documented '
     'across ten research papers. Both things are simultaneously true and '
     'neither undermines the other. The name is not an apology and the '
     'rigour is not a defence. They simply coexist.',
     ['Yes, we\u2019re called InvestPuppy. Vektor is the platform.',
      'Serious when it matters.',
      'The work speaks for itself. The name is a signal about how we see ourselves.'],
     ['Despite the name, we are a serious firm.',
      'InvestPuppy \u2014 don\u2019t let the name fool you.',
      'We know the name is unusual for an institutional product...']),

    (7, 'Evidence-anchored.',
     'Every claim has a backing reference. The white paper series exists '
     'precisely for this purpose. Use it. \u2018We believe\u2019 and \u2018we think\u2019 '
     'are acceptable for opinions. For facts and methodology, cite the evidence.',
     ['See: WP-01 \u2014 Quantitative Portfolio Construction.',
      'The 99.94% figure is documented in the brochure with methodology.',
      'Signal selection is described in full in WP-02.'],
     ['We believe our methodology is among the most rigorous available.',
      'Our approach is based on proven quantitative techniques.',
      'The platform is designed with institutional-grade precision.']),

    (8, 'Human voice, not corporate voice.',
     '\u2018We\u2019 not \u2018the company\u2019 or \u2018the platform\u2019. '
     'Direct address, active voice, present tense. '
     'Write as a person who knows what they are talking about, '
     'not as a firm that needs to sound official.',
     ['We will run the full workflow on your data.',
      'Ask us. We will tell you.',
      'Show us a mandate. We\u2019ll show you the platform.'],
     ['InvestPuppy is committed to delivering value to its clients.',
      'The platform is designed to provide wealth management professionals with...',
      'Vektor\u2019s proprietary methodology enables users to...']),

    (9, 'Short, then deep.',
     'First contact should be one page or five slides. '
     'Due diligence should be ten white papers. '
     'Never reverse this. The depth exists to reward those who earned it, '
     'not to overwhelm those who have not yet decided to care.',
     ['At a Glance: one page. White papers: ten volumes.',
      'Lightning Deck: six slides. Technical Deep Dive: fifteen.',
      'FAQ first. White papers if they ask.'],
     ['Here is our comprehensive 46-document suite for your initial review.',
      'We\u2019ve prepared an extensive overview covering all aspects of...',
      'To fully understand the platform, please read the following twelve documents.']),

    (10, 'Complete, not selective.',
     'If honest communication requires including something uncomfortable, '
     'include it. Selective truth is not honesty. '
     'The test is not \u2018does this help our case?\u2019 '
     'but \u2018does this give the reader what they need to make an informed decision?\u2019',
     ['WP-09 covers market regime risk in detail.',
      'We have listed all open items in our outstanding register.',
      'The Proof Partners programme is honest about what we are offering and why.'],
     ['We focus on our strengths in all client communications.',
      '\u2014 (omitting known limitations from due diligence materials)',
      'All relevant information is available on request.']),
]

for i, pr in enumerate(PRINCIPLES):
    story.append(principle(*pr))
    story.append(sp(8))
    if i == 4:
        story.append(PageBreak())
        story.append(p('TEN PRINCIPLES (CONTINUED)', s_tag))
        story.append(hr(GOLD, 0.8, 2, 12))

story.append(PageBreak())

# ── FINAL PAGE: APPLICATION ────────────────────────────────────────────────
story.append(p('APPLYING THE VOICE', s_tag))
story.append(hr(GOLD, 0.8, 2, 12))

contexts = [
    ('FIRST CONTACT', 'EXTERNAL',
     'Bold layer. Lead with the name, the proof-of-concept offer, or the '
     '\u2018What Vektor Is Not\u2019 document. '
     'Personality visible from the first sentence. No product detail until asked.'),
    ('COMMERCIAL DOCUMENTS', 'EXTERNAL',
     'Confident, specific, evidence-anchored. '
     'Brochure, Why Vektor, Proof Partners programme. '
     'Claims supported by white paper references throughout.'),
    ('DUE DILIGENCE', 'EXTERNAL',
     'Conservative layer. Rigour, evidence, complete disclosure. '
     'Limitations stated without apology. References to WP-09 and risk disclosure '
     'are features, not footnotes. No personality amplification here.'),
    ('WHITE PAPERS', 'EXTERNAL',
     'Technical and precise. Evidence-anchored throughout. '
     'Readable by a non-quant practitioner but rigorous enough for a quant. '
     'Never promotional. The work speaks for itself.'),
    ('INTERNAL DOCUMENTS', 'INTERNAL',
     'Same honesty standard as external. Internal documents that suppress '
     'bad news or overstate progress are a failure of the brand principle, '
     'not just a management problem.'),
    ('ANY COMMUNICATION', 'ALL',
     'If you are unsure whether something passes the voice standard, '
     'apply the single test: \u2018Are we being as honest here '
     'as we are capable of being?\u2019 If the answer is no, rewrite it.'),
]

rows = [[p('CONTEXT', S('th', fontName='Helvetica-Bold', fontSize=7.5,
           textColor=GOLD, leading=11, letterSpacing=1.5)),
         p('AUDIENCE', S('th2', fontName='Helvetica-Bold', fontSize=7.5,
           textColor=GOLD, leading=11, letterSpacing=1.5)),
         p('VOICE NOTE', S('th3', fontName='Helvetica-Bold', fontSize=7.5,
           textColor=GOLD, leading=11, letterSpacing=1.5))]]
for ctx, aud, note in contexts:
    rows.append([p(ctx, S('ctxk', fontName='Helvetica-Bold', fontSize=8.5,
                   textColor=PLAT, leading=12)),
                 p(aud, S('ctxa', fontSize=8, textColor=W_GREY, leading=12)),
                 p(note, S('ctxv', fontSize=8.5, textColor=OFF_W, leading=13))])

ct = Table(rows, colWidths=[36*mm, 22*mm, COL_W-62*mm])
ct.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,0), CARD),
    ('ROWBACKGROUNDS', (0,1),(-1,-1), [NOTE, CARD]),
    ('TOPPADDING', (0,0),(-1,-1), 7),
    ('BOTTOMPADDING', (0,0),(-1,-1), 7),
    ('LEFTPADDING', (0,0),(-1,-1), 10),
    ('RIGHTPADDING', (0,0),(-1,-1), 10),
    ('LINEBELOW', (0,0),(-1,-2), 0.3, RULE_MN),
    ('BOX', (0,0),(-1,-1), 0.4, RULE_MN),
    ('VALIGN', (0,0),(-1,-1), 'TOP'),
]))
story.append(ct)
story.append(sp(16))
story.append(hr(GOLD, 0.5, 4, 8))
story.append(p(
    'Honest by design. Every sentence, every document, every time.',
    S('close', fontName='Helvetica-BoldOblique', fontSize=11,
      textColor=PLAT, leading=17, alignment=TA_CENTER)))
story.append(sp(6))
story.append(p(
    'The audience will know the difference. Make sure they do.',
    S('close2', fontName='Helvetica-Oblique', fontSize=10,
      textColor=W_GREY, leading=16, alignment=TA_CENTER)))

doc.build(story)
sz = os.path.getsize(OUT)
print(f"Built: {OUT}")
print(f"Size:  {sz:,} bytes ({sz//1024}KB)")
