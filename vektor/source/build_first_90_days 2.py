"""The First 90 Days — Founding Mandate onboarding guide. vk5 build."""
import sys, os
sys.path.insert(0, '/home/claude')
from wp_builder_v3 import *
from reportlab.platypus import PageBreak, NextPageTemplate
from reportlab.lib.enums import TA_CENTER

OUT  = '/home/claude/investpuppy/vektor/output/pdf/vk5-first-90-days.pdf'
REF  = 'IP-F90-260508-1.0'
SUB  = 'The First 90 Days'

# ── COVER ─────────────────────────────────────────────────────────────────────
def draw_cover(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG); canvas.rect(0, 0, W, H, fill=1, stroke=0)
    from reportlab.lib.utils import ImageReader
    try:
        img = ImageReader(LOGO); iw, ih = img.getSize()
        lw = min(W * 0.62, 320); lh = lw * ih / iw
        lx = (W - lw) / 2; ly = H * 0.56
        canvas.drawImage(LOGO, lx, ly - lh, lw, lh, mask='auto',
                         preserveAspectRatio=True)
        ry = ly - lh - 14
        canvas.setStrokeColor(GOLD); canvas.setLineWidth(0.8)
        canvas.line(ML, ry, W - MR, ry)
        y = ry - 52
        canvas.setFont('Helvetica-Bold', 30); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W / 2, y, 'The First 90 Days')
    except Exception as e:
        print(f'Cover: {e}')
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4)
    canvas.line(ML, 36 * mm, W - MR, 36 * mm)
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(WARM_GREY)
    canvas.drawCentredString(W / 2, 29 * mm,
        'For Founding Mandate partners \u2014 provided at mandate signing')
    canvas.setFont('Helvetica', 7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W / 2, 22 * mm, REF)
    canvas.drawCentredString(W / 2, 16 * mm, DATE)
    canvas.restoreState()

draw_page = make_page_fn(SUB)
doc, f_cov, f_fst, f_lat = make_doc(OUT, SUB)
doc.addPageTemplates([
    PageTemplate(id='Cover', frames=[f_cov], onPage=draw_cover),
    PageTemplate(id='First', frames=[f_fst], onPage=draw_page),
    PageTemplate(id='Later', frames=[f_lat], onPage=draw_page),
])

s = make_styles()

# Additional styles
S_pull = ParagraphStyle('pull', fontName='Helvetica-BoldOblique', fontSize=11,
    textColor=PLATINUM, leading=18, alignment=TA_CENTER, spaceAfter=6)
S_cto  = ParagraphStyle('cto', fontName='Helvetica-Bold', fontSize=10.5,
    textColor=PLATINUM, leading=17, alignment=TA_CENTER, spaceAfter=4)
S_cto_em = ParagraphStyle('cto_em', fontName='Helvetica-Bold', fontSize=11.5,
    textColor=GOLD, leading=18, alignment=TA_CENTER, spaceAfter=0)

story = [sp(1), NextPageTemplate('Later'), PageBreak()]

# ── PAGE 2 OPENS WITH THE GOLD RULE, THEN THE SHOUT ──────────────────────────
story += [
    sp(4),
    hrgold(),
    sp(20),
    p('What will the first 90 days look like\u2026',
      ParagraphStyle('pq1a', fontName='Helvetica-BoldOblique', fontSize=20,
          textColor=PLATINUM, leading=28, alignment=TA_CENTER, spaceAfter=4)),
    p('\u2026We don\u2019t know!',
      ParagraphStyle('pq1b', fontName='Helvetica-BoldOblique', fontSize=20,
          textColor=PLATINUM, leading=28, alignment=TA_CENTER, spaceAfter=14)),
    p('But here\u2019s how we\u2019ll approach it.',
      ParagraphStyle('pq2', fontName='Helvetica-Oblique', fontSize=13,
          textColor=WARM_GREY, leading=20, alignment=TA_CENTER, spaceAfter=0)),
    sp(24),
    HRule(COL_W, RULE_MIN, 0.4, 4, 4),
    sp(16),
]

# ── OPENING ───────────────────────────────────────────────────────────────────
story += [
    p('The honest reason we don\u2019t know is that your practice is not the same as '
      'every other practice. Your investable universe is different. Your client profiles '
      'are different. Your workflow \u2014 the way decisions actually get made on a '
      'Tuesday morning \u2014 is different from how any other DPM describes theirs. '
      'We could hand you a twelve-week implementation plan at signing. It would be '
      'wrong by week three.',
      s['body']),
    sp(6),
    p('So we do not start with a plan. We start with a week.', s['body']),
    sp(14),
]

# ── SECTION 1: WEEK ONE ───────────────────────────────────────────────────────
story += [
    p('1.  WEEK ONE', s['wp_section']), hrm(),
    p('Before we build anything.', s['body_grey']),
    sp(4),
    p('In week one, our CEO and our CTO are in your office. In person. Not on a call, '
      'not reviewing documentation remotely \u2014 in your office, working alongside you.',
      s['body']),
    sp(6),
    NoteBox(COL_W,
        'We are not configuring anything. We are watching, listening, and learning.',
        ParagraphStyle('watch', fontName='Helvetica-BoldOblique', fontSize=10.5,
            textColor=PLATINUM, leading=17, alignment=TA_CENTER)),
    sp(10),
    p('What does your screening process actually look like? Where does the manual work '
      'happen? What takes longer than it should? What works well that you would not want '
      'disrupted? What have previous technology projects failed to understand about how '
      'you operate?', s['body']),
    p('By the end of the week we will have a clear picture of your practice \u2014 not '
      'a theoretical model of it, but the real one. That picture shapes everything '
      'that follows.', s['body']),
    sp(10),
    p('INTEGRATION TOUCHPOINTS', s['wp_sub']),
    p('Week one also identifies every integration point the implementation will touch. '
      'Data integration is not a marginal consideration and not an afterthought \u2014 '
      'it is fundamental to the success of the process, and the place where most platform '
      'adoptions quietly accumulate the failures that surface in week six.',
      s['body']),
    p('Two directions, both mapped in week one:', s['body']),
    p('\u2014 <b>Inbound:</b> market data. What data sources does your practice currently '
      'use? What quality standard do you require? What format? What needs to be '
      'configured, connected, or replaced?', s['bullet']),
    p('\u2014 <b>Outbound:</b> order and allocation output. How does the Vektor position '
      'file reach your PMS, your execution system, your broker? What format, what '
      'protocol, what testing is required before go-live?', s['bullet']),
    sp(10),
    p('THE UNKNOWNS REGISTER', s['wp_sub']),
    p('Every implementation surfaces things neither party anticipated. The unknowns '
      'register is our explicit acknowledgment of what we do not yet know how to resolve '
      '\u2014 workflow gaps, integration edge cases, role configurations that need '
      'adaptation, timing constraints specific to your client base.',
      s['body']),
    p('We document them honestly. We agree on them together. We build a plan to convert '
      'each unknown to a solution. The unknowns register is not a risk log to be reviewed '
      'in six months. It is the agenda for the weeks that follow.',
      s['body']),
    sp(10),
]

# ── SECTION 2: THE PLAN ───────────────────────────────────────────────────────
story += [
    sp(14),
    p('2.  THEN WE BUILD THE PLAN', s['wp_section']), hrm(),
    p('Only after week one.', s['body_grey']),
    sp(4),
    p('Most software adoptions work the other way around. The vendor hands you a plan '
      'at signing \u2014 before they have met your team, observed your workflow, or '
      'identified a single unknown. That plan reflects what they know, not what you need.',
      s['body']),
    p('The plan we build at the end of week one is different. It is built from what we '
      'learned about your practice. It covers timelines, client conversion sequencing, '
      'parallel running, integration milestones, and the go-live milestone \u2014 defined '
      'for your workflow specifically, not for a generic DPM practice.',
      s['body']),
    NoteBox(COL_W,
        'By the time we build it, both parties have a week of shared knowledge, a fully '
        'agreed unknowns register, and a documented integration map. You know more about '
        'how we work. We know more about how you work. The plan that emerges is one both '
        'sides can commit to with confidence \u2014 because it was built from understanding, '
        'not assumption.',
        s['body']),
    sp(14),
]

# ── SECTION 3: WHAT COMES NEXT ────────────────────────────────────────────────
story += [
    p('3.  WHAT COMES NEXT', s['wp_section']), hrm(),
    p('Every plan will be specific to the practice. These are the phases it will address.',
      s['body_grey']),
    sp(4),
    p('CONFIGURATION', s['wp_sub']),
    p('The platform configured around your actual instruments, benchmark, clients\u2019 '
      'base currencies, and team role structure \u2014 informed by what was learned in '
      'week one. A note on roles: Vektor separates the Analyst, Portfolio Manager, and '
      'Operations functions. In a boutique practice these are often one or two people. '
      'The platform accommodates this. The configuration will reflect how your team '
      'actually works.',
      s['body']),
    sp(6),
    p('FIRST STRATEGY BUILD', s['wp_sub']),
    p('Your Analyst builds the first strategy on your instruments. The grid search runs '
      'across six indicators for every holding. The efficient frontier is generated from '
      '10,000 portfolio configurations. The Portfolio Manager reviews the complete output '
      '\u2014 instruments, weights, signals, Sharpe ratios \u2014 before approving '
      'anything.',
      s['body']),
    p('This is the moment the platform stops being a proposition and becomes a tool. '
      'Some of what it produces will match your current process. Some will not. Both '
      'outcomes are useful. Agreement builds confidence. Disagreement starts the most '
      'valuable conversation of the implementation \u2014 why does the systematic '
      'process see this differently? The answer is always in the data.',
      s['body']),
    sp(6),
    p('PARALLEL RUNNING', s['wp_sub']),
    p('Vektor produces recommendations. Your PM evaluates them. Your existing process '
      'continues alongside. This phase is confidence-dependent, not time-dependent. '
      'It ends when the Portfolio Manager has reviewed enough Vektor recommendations '
      'to be satisfied they are ready to execute with real capital. We will not set '
      'a calendar deadline for this. We will work with you until the confidence '
      'is genuinely there.',
      s['body']),
    sp(6),
    p('FIRST LIVE EXECUTION', s['wp_sub']),
    p('One strategy. One client. One mandate. The eleven steps, end to end, with real '
      'capital, for the first time. Everything visible, everything logged, everything '
      'approved before a single order is placed. This is the milestone \u2014 not the '
      'end of anything, but the beginning of the operating relationship.',
      s['body']),
    sp(10),
]

# ── SECTION 4: THE FOUNDING RELATIONSHIP ──────────────────────────────────────
story += [
    sp(14),
    p('4.  THE FOUNDING RELATIONSHIP', s['wp_section']), hrm(),
    p('Co-builder. Not consumer.', s['body_grey']),
    sp(4),
    p('The founding partner is not a beta tester and not an early adopter. They are a '
      'co-author of the production system. Every defect they identify is a contribution. '
      'Every fix they validate is a joint decision. Every release they test before '
      'general availability is the founding partnership working as it was designed.',
      s['body']),
    NoteBox(COL_W,
        'InvestPuppy gets what no amount of internal testing can provide: a live workflow, '
        'real capital, and practitioners who know what correct output looks like. '
        'The founding partner gets a platform built around their specific practice, '
        'fixed when it fails, and improved by their direct input. '
        'Neither party is doing the other a favour. This is what founding means.',
        s['body']),
    sp(10),
    p('HOW DEFECTS, FIXES AND RELEASES WORK', s['wp_sub']),
    p('Defect management is not an external process. It is built into every step of '
      'the implementation and the operating relationship that follows.',
      s['body']),
    p('\u2014 Critical defects affecting live execution reach us directly \u2014 '
      'no ticket queue, no triage, no escalation path. Timeline agreed within '
      'hours, not days.', s['bullet']),
    p('\u2014 Non-critical defects are tracked in the unknowns register and addressed '
      'on the agreed release schedule.', s['bullet']),
    p('\u2014 The founding partner validates every fix before it goes to production.',
      s['bullet']),
    p('\u2014 Every new capability reaches the founding partner before general release. '
      'They validate it against their workflow before anyone else sees it.',
      s['bullet']),
    sp(8),
    p('This is not optional. It is the process.',
      ParagraphStyle('not_optional', fontName='Helvetica-BoldOblique', fontSize=10,
          textColor=PLATINUM, leading=16, alignment=TA_CENTER)),
    sp(12),
    hrgold(),
    sp(10),
    p('The developer will be dedicated to resolving defects.', S_cto),
    p('The CEO will be driving the developer.', S_cto),
    p('The CTO will BE the developer.', S_cto_em),
    sp(10),
    hrgold(),
    sp(14),
]

# ── SECTION 5: WHAT WE COMMIT TO ─────────────────────────────────────────────
story += [
    p('5.  WHAT WE COMMIT TO', s['wp_section']), hrm(),
    p('Throughout the ninety-day period and the founding relationship beyond it.',
      s['body_grey']),
    sp(4),
    p('<b>We will tell you what is not yet built before it becomes a problem.</b> '
      'If a capability you need is on the roadmap rather than live today, you will '
      'know before it affects the plan \u2014 not during the week you needed it.',
      s['body']),
    p('<b>CEO and CTO are your direct contacts.</b> Not an onboarding manager. Not a '
      'customer success function. The people who built the platform, available to you '
      'for questions about methodology, workflow, integration, and anything the '
      'implementation surfaces. In person in week one. Directly reachable throughout.',
      s['body']),
    p('<b>Integration is treated as fundamental.</b> Not a marginal consideration. '
      'Not an afterthought. Integration touchpoints are identified in week one, '
      'planned in the implementation plan, and tracked through to completion.',
      s['body']),
    p('<b>The unknowns register is maintained.</b> Every item identified in week one '
      'is tracked to resolution. New unknowns that emerge during configuration or '
      'parallel running are added. Nothing disappears because it is inconvenient.',
      s['body']),
    p('<b>Implementation commitments are kept.</b> The timelines in the plan built '
      'at the end of week one are treated as commitments, not estimates. If something '
      'changes, we tell you immediately and we tell you why.',
      s['body']),
    sp(14),
]

# ── SECTION 6: THE HONEST VERSION ────────────────────────────────────────────
story += [
    PageBreak(), sp(0),
    p('6.  THE HONEST VERSION OF WHAT IS HARD', s['wp_section']), hrm(),
    p('Three things to expect.', s['body_grey']),
    sp(8),
    NoteBox(COL_W,
        '<b>The first strategy build is not the final one.</b> The PM\u2019s review '
        'will identify adjustments \u2014 instruments that should not be in the universe '
        'for reasons the screening did not capture, constraints that need tightening, '
        'a benchmark weighting that needs refinement. This is not a failure. It is the '
        'calibration working correctly. Expect to rebuild the first strategy at least once.',
        s['body']),
    sp(8),
    NoteBox(COL_W,
        '<b>Parallel running requires discipline.</b> The temptation to run for two '
        'weeks and go live is real. The value of parallel running comes from evaluating '
        'the platform\u2019s output across multiple market conditions and multiple '
        'strategy cycles \u2014 not from checking it once and feeling ready. We will '
        'recommend the right duration. We will not enforce it.',
        s['body']),
    sp(8),
    NoteBox(COL_W,
        '<b>Your team\u2019s workflow will change.</b> The Analyst\u2019s role expands. '
        'The PM\u2019s role shifts. The Operations function acquires new responsibilities. '
        'None of these changes are difficult. All of them are different from what your '
        'team does today. Budget time for the adjustment.',
        s['body']),
    sp(20),
]

# ── CLOSING ───────────────────────────────────────────────────────────────────
story += [
    HRule(COL_W, RULE_MAJ, 1.0, 4, 8),
    p('The first Founding Mandate partner is not receiving a proven process. They are '
      'participating in the first real-world execution of one \u2014 alongside the '
      'people who designed it, who will be there in person from day one, and who will '
      'be fixing it when it needs fixing.',
      s['body']),
    sp(8),
    p('We do not know exactly what your first ninety days will look like. '
      'We know precisely how we will approach them.',
      ParagraphStyle('close_decl', fontName='Helvetica-BoldOblique', fontSize=10.5,
          textColor=PLATINUM, leading=17, alignment=TA_CENTER)),
    sp(14),
    hrgold(),
    sp(8),
    p('Show us a mandate. The ninety days start there.',
      ParagraphStyle('cta_final', fontName='Helvetica-Bold', fontSize=11,
          textColor=PLATINUM, leading=17, alignment=TA_CENTER)),
    sp(8),
    p('investpuppy.com  \u00b7  contact@investpuppy.com',
      ParagraphStyle('ref_close', fontName='Helvetica', fontSize=8,
          textColor=WARM_GREY, leading=12, alignment=TA_CENTER)),
    sp(10),
    HRule(COL_W, RULE_MAJ, 1.0, 4, 8),
    sp(10),
    p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {REF}  \u00b7  '
      f'Copyright 2026 InvestPuppy', s['wp_ref']),
]

doc.build(story)
sz = os.path.getsize(OUT)
import subprocess
r = subprocess.run(['pdfinfo', OUT], capture_output=True, text=True)
for l in r.stdout.split('\n'):
    if 'Pages' in l or 'File size' in l:
        print(l)
print(f'Built: {OUT}')
print(f'Size:  {sz:,} bytes ({sz//1024}KB)')
