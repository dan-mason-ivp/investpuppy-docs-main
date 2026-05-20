"""
Vektor FAQ — vk3 rebuild.
vk2 baseline + brand integration:
  - Q2 added: "Why is the company called InvestPuppy?" (Expert G draft, Dan-approved)
  - Q2–Q12 renumbered to Q3–Q13
  - Cover + intro updated: "Twelve" → "Fifteen questions"
  - Cover: IP horizontal mark 38mm bottom-left
  - Footer: IP horizontal mark 32mm standard
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
S_decl_swim = ParagraphStyle('dswim', fontName='Helvetica-BoldOblique', fontSize=13, textColor=OFF_WHITE, leading=18, alignment=TA_CENTER)
WARM_GREY = colors.HexColor('#9A9086')
RULE_MAJ  = colors.HexColor('#5A5A60')
RULE_MIN  = colors.HexColor('#2A2828')
CARD_EDGE = colors.HexColor('#242428')

W, H = A4
ML = MR = 22*mm
MT1 = 16*mm; MT2 = 46*mm; MB = 20*mm
COL_W = W - ML - MR
LOGO = _os.path.join(_LOGOS, 'VEKTOR-transparent-v3.png')
DATE = 'May 2026'
DOC_REF = 'IP-FAQ-260501-1.0'
SUB = 'Frequently Asked Questions'
IP_H = _os.path.join(_LOGOS, 'IPHorizontalClear.png')
IP_H_RATIO = 2.337

def S():
    s = {}
    s['q'] = ParagraphStyle('q', fontName='Helvetica-Bold', fontSize=10,
        textColor=GOLD, leading=15, spaceAfter=4, spaceBefore=8)
    s['a'] = ParagraphStyle('a', fontName='Helvetica', fontSize=9.5,
        textColor=OFF_WHITE, leading=17, spaceAfter=5, alignment=TA_JUSTIFY)
    s['see'] = ParagraphStyle('see', fontName='Helvetica', fontSize=8.5,
        textColor=WARM_GREY, leading=13, spaceAfter=6)
    s['section_tag'] = ParagraphStyle('section_tag', fontName='Helvetica-Bold',
        fontSize=7, textColor=GOLD, leading=10, letterSpacing=3, spaceAfter=6, spaceBefore=10)
    s['intro'] = ParagraphStyle('intro', fontName='Helvetica', fontSize=9.5,
        textColor=OFF_WHITE, leading=17, spaceAfter=8, alignment=TA_JUSTIFY)
    s['footer'] = ParagraphStyle('footer', fontName='Helvetica', fontSize=6.5,
        textColor=colors.HexColor('#444440'), alignment=TA_CENTER, leading=10)
    s['wp_ref'] = ParagraphStyle('wp_ref', fontName='Helvetica', fontSize=7.5,
        textColor=colors.HexColor('#555550'), alignment=TA_CENTER, leading=11)
    return s


class HRule(Flowable):
    def __init__(self, w, c=RULE_MIN, t=0.4, sa=3, sb=3):
        Flowable.__init__(self)
        self.rw=w; self.c=c; self.t=t; self._sa=sa; self._sb=sb
        self.height=sa+t+sb
    def wrap(self, aw, ah): return self.rw, self.height
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        self.canv.line(0, self._sb+self.t/2, self.rw, self._sb+self.t/2)


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
        canvas.setFont('Helvetica-Bold',22); canvas.setFillColor(PLATINUM)
        canvas.drawCentredString(W/2,ry-40,'Frequently Asked')
        canvas.drawCentredString(W/2,ry-66,'Questions')
        canvas.setFont('Helvetica',10); canvas.setFillColor(WARM_GREY)
        canvas.drawCentredString(W/2,ry-90,
            'Fifteen questions that come up in every conversation about Vektor \u2014 answered directly, in plain language.')
    except Exception as e: print(e)
    canvas.setStrokeColor(RULE_MAJ); canvas.setLineWidth(0.4)
    canvas.line(ML,36*mm,W-MR,36*mm)
    canvas.setFont('Helvetica',7.5); canvas.setFillColor(WARM_GREY)
    canvas.drawCentredString(W/2,28*mm,'For DPMs, family office principals, and prospective partners')
    canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawCentredString(W/2,22*mm,DOC_REF)
    canvas.drawCentredString(W/2,16*mm,DATE)
    # IP horizontal mark — bottom-left, maker's attribution
    try:
        ip_w=38*mm; ip_h=ip_w/IP_H_RATIO
        canvas.drawImage(IP_H,ML,9*mm,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
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
    except: pass
    canvas.setFont('Helvetica',7); canvas.setFillColor(colors.HexColor('#555550'))
    canvas.drawRightString(W-MR,H-MT2+18,f'{SUB}  \u00b7  {doc.page-1:02d}')
    canvas.setStrokeColor(RULE_MIN); canvas.setLineWidth(0.4)
    canvas.line(ML,H-MT2+8,W-MR,H-MT2+8)
    # Footer — IP horizontal mark standard
    canvas.setLineWidth(0.3); canvas.line(ML,MB-2,W-MR,MB-2)
    try:
        from reportlab.lib.utils import ImageReader as _IR
        ip_w=32*mm; ip_h=ip_w/IP_H_RATIO
        canvas.drawImage(IP_H,ML,1.0*mm,ip_w,ip_h,mask='auto',preserveAspectRatio=True)
    except Exception as e: print(e)
    canvas.setFont('Helvetica',6.5); canvas.setFillColor(colors.HexColor('#444440'))
    canvas.drawRightString(W-MR,1.0*mm+((32*mm/IP_H_RATIO)/2)-2.5,f'investpuppy.com  \u00b7  {DATE}')
    canvas.restoreState()


def para(text, s, st='a'): return Paragraph(text, s[st])
def sp(n=4): return Spacer(1,n)
def hr(): return HRule(COL_W, RULE_MIN, 0.3, 4, 3)
def hrm(): return HRule(COL_W, RULE_MAJ, 1.0, 2, 6)

def qa(q_text, a_text, see_text, s, story):
    story.append(hr())
    story.append(para(q_text, s, 'q'))
    story.append(para(a_text, s, 'a'))
    story.append(para(see_text, s, 'see'))


def build():
    out='/home/claude/investpuppy/vektor/output/pdf/vk5-faq.pdf'
    s=S()
    f_cover=Frame(0,0,W,H,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id='cover')
    f_body=Frame(ML,MB,COL_W,H-MT2-MB,id='body')
    doc=BaseDocTemplate(out,pagesize=A4,leftMargin=ML,rightMargin=MR,
        topMargin=MT1,bottomMargin=MB,title='Vektor FAQ',author='InvestPuppy')
    doc.addPageTemplates([
        PageTemplate(id='Cover',frames=[f_cover],onPage=draw_cover),
        PageTemplate(id='Body',frames=[f_body],onPage=draw_page),
    ])

    story=[]
    story.append(Spacer(1,1))
    story.append(NextPageTemplate('Body'))
    story.append(PageBreak())

    story.append(para(
        'These are the fifteen questions that come up in every conversation about Vektor. '
        'The answers here are plain-language summaries. For the full technical and methodological '
        'detail behind each answer, the relevant document is noted at the end of each response.',
        s, 'intro'))

    story.append(sp(6))
    story.append(para('ABOUT THE PLATFORM', s, 'section_tag'))
    story.append(hrm())

    qa('Q1. Is Vektor an AI trading system?',
       'No. Vektor is a systematic portfolio management platform. It uses machine learning in two specific, '
       'bounded roles: filtering the instrument universe during research, and validating trading signals before '
       'they are reviewed by a portfolio manager. In both cases, machine learning produces an output \u2014 a '
       'screened list, a confidence score \u2014 that a human reviews and acts on. No position is taken without '
       'explicit portfolio manager approval. The machine does not trade.',
       'See: WP-08: AI as Instrument', s, story)

    qa('Q2. Why is the company called InvestPuppy?',
       'Because we wanted to. More specifically: because a name you remember is more useful than a name '
       'that sounds like everyone else\u2019s. If you\u2019re reading this, the name got you curious enough '
       'to keep going \u2014 which is exactly what it was designed to do.'
       '\n\nThe work is serious. The name is a signal that we don\u2019t take ourselves seriously. We think '
       'those two things are compatible. If you disagree, other, more traditional vendors are available.'
       '\n\nVektor is the platform. InvestPuppy is the company that built it. You\u2019ll be working with Vektor.',
       'See: Why Vektor \u2014 The InvestPuppy Question', s, story)
    story.append(sp(10))
    story.append(HRule(COL_W,RULE_MAJ,0.5,4,4))
    story.append(sp(8))
    story.append(Paragraph('Serious when it matters.',S_decl_swim))
    story.append(sp(14))

    qa('Q3. Who approves the trades?',
       'The portfolio manager approves every strategy before any client assignment proceeds. The operations '
       'team records every cash funding. The portfolio manager confirms the allocation before any orders are '
       'submitted. These are three separate human actions \u2014 none can be automated or skipped.',
       'See: WP-06: Audit Trail & Compliance, WP-08: AI as Instrument', s, story)

    qa('Q4. What happens if the market crashes?',
       'Vektor does not automatically liquidate positions in response to market movements \u2014 there is no '
       'automatic stop-loss or liquidation trigger. The portfolio manager reviews the strategy and decides '
       'whether to rebalance, hold, or exit positions. The platform provides current position data, signal '
       'status, and allocation calculation to support that decision. How a mandate responds to a market crash '
       'is a portfolio management decision, not a platform decision.',
       'See: WP-02, WP-09: Risk Disclosure', s, story)

    qa('Q5. Can I use Vektor alongside my existing holdings and systems?',
       'Yes. Vektor is designed to complement existing infrastructure, not replace it. The platform outputs a '
       'complete allocation table via API \u2014 instruments, quantities, and values \u2014 that can feed into '
       'an existing PMS or execution system. A client with an existing equity research process can use Vektor '
       'for the systematic portfolio construction layer while continuing to use existing tools for everything else.',
       'See: WP-07: Technical Architecture, Workflow Integration Guide', s, story)

    qa('Q6. What data does Vektor use?',
       'Three years of daily OHLCV (open, high, low, close, volume) price history for all configured instruments, '
       'sourced from Yahoo Finance. Daily FX rates for all configured currency pairs. Data quality checks run on '
       'ingestion and corporate action adjustments are applied. The data source is configurable \u2014 a Bloomberg '
       'or institutional data feed can be substituted without architectural changes. '
       'On the question of data dependency: Vektor\u2019s use of Yahoo Finance reflects the current stage of '
       'development. A data quality failure at source triggers a platform alert before any strategy execution '
       'proceeds \u2014 the system will not act on incomplete price data. All historical price data is stored '
       'within the platform, so a temporary data provider outage does not affect existing strategies or '
       'historical analysis. Data portability is by design: the full instrument and price database can be '
       'exported at any point.',
       'See: WP-04: Indicator Selection, WP-05: Multi-Currency', s, story)

    qa('Q7. Which markets does Vektor support?',
       'Any listed equity market. Exchange, benchmark, currency, and lot sizes are configuration parameters \u2014 '
       'not hard-coded values. The platform is illustrated with an SGX implementation because that is the initial '
       'deployment market, but the same methodology applies to any exchange with sufficient historical price data.',
       'See: WP-01: Portfolio Construction', s, story)

    qa('Q7a. We already have Bloomberg. How does Vektor relate to it?',
       'Bloomberg is three distinct products, each with a different relationship to Vektor. '
       'The Bloomberg Terminal ($31,980/year per seat in 2026; approximately S$43,000+ SGD) provides '
       'news, messaging, fixed income data, and market analytics. Vektor does not compete with the Terminal \u2014 '
       'it stays. '
       'Bloomberg PORT is the portfolio construction module, an additional subscription on top of the Terminal '
       '(typically S$8,000\u2013S$25,000 per seat per year). Vektor directly replaces PORT for listed equity '
       'construction. The Terminal stays. PORT is cancelled. The Bloomberg bill falls. Construction capability improves. '
       'Bloomberg data feeds (B-PIPE) are enterprise data agreements for programmatic data consumption. '
       'Firms running data feeds for in-house quant development are building what Vektor already is. '
       'Vektor terminates that effort \u2014 immediately, at lower cost, with better systematic construction.',
       'See: Workflow Integration Guide', s, story)

    qa('Q8. Does Vektor support multiple clients and mandates simultaneously?',
       'Yes. Different client accounts can be assigned to different mandates concurrently \u2014 '
       'different universe, different benchmark, different base currency \u2014 and managed '
       'independently within a single platform instance. Each mandate runs its own signal '
       'optimisation, its own portfolio construction, and its own execution workflow. '
       'There is no limit on the number of concurrent mandates.',
       'See: WP-05: Multi-Currency Architecture', s, story)

    story.append(PageBreak())
    story.append(Spacer(1,0))
    story.append(para('ABOUT GETTING STARTED', s, 'section_tag'))
    story.append(hrm())

    qa('Q9. Is my data kept in Singapore?',
       'The current deployment is in AWS ap-southeast-1 (Singapore). Data does not leave the configured AWS '
       'region as part of normal platform operation. AWS data residency guarantees apply per region. A client '
       'with UK or Hong Kong data residency requirements can deploy to the appropriate AWS region \u2014 the '
       'architecture is region-agnostic by design.',
       'See: WP-07: Technical Architecture', s, story)

    # Q8 UPDATED: now cross-references FMP document
    qa('Q10. What is the Founding Mandate?',
       'The Founding Mandate is the early-adopter programme. Founding Mandate partners work directly with the '
       'Vektor team to configure the platform around their specific workflow, and receive founding commercial '
       'terms not available after the programme closes. In exchange, Founding Mandate partners are building '
       'the platform alongside us \u2014 their feedback shapes the product roadmap. The number of Founding '
       'Mandate positions is deliberately limited. For the complete programme specification \u2014 commercial '
       'structure, partner obligations, slot availability, and the twelve-month founding period \u2014 see the '
       'Founding Mandate Programme document.',
       'See: Why Vektor, Founding Mandate Programme (IP-FMP-260501-1.0)', s, story)

    qa('Q11. Does Vektor have a live track record?',
       'No. We are telling you this before you ask because it is the right thing to do. '
       'The platform is built and running \u2014 the complete eleven-step workflow has been '
       'built, tested, and validated. It has not yet executed in a live account. '
       'That is the primary milestone the Founding Mandate first production period achieves. '
       'A live track record begins with the first Founding Mandate client. '
       'We have written a full white paper on how to evaluate a systematic '
       'platform without a live track record. We recommend reading it before any commercial '
       'discussion. WP-09 covers the risks of systematic approaches in full. We recommend '
       'reading that one first.',
       'See: WP-09: Risk Disclosure (read this first) \u00b7 WP-10: Evaluating Performance Without a Track Record \u00b7 Founding Mandate Programme (IP-FMP-260501-1.0)', s, story)

    qa('Q12. What does Vektor cost?',
       'Vektor uses AUM-tiered annual subscription pricing. Entry tier (up to S$75M AUM): S$24,000/year. '
       'Growth tier (S$75M\u2013S$250M): S$48,000/year. Institutional tier (S$250M\u2013S$750M): S$108,000/year. '
       'Enterprise (S$750M+): from S$168,000/year. '
       'All tiers are positioned materially below the Bloomberg Terminal + PORT spend for a firm at the same AUM level. '
       'Founding Mandate partners receive a 12-month founding rate at S$18,000/year, then permanently '
       'one tier below their AUM tier. '
       'On pricing philosophy: Vektor pricing is published openly and held consistently. It is not inflated '
       'to create negotiating room. Structured commercial flexibility exists for two defined reasons: '
       'multi-year subscription commitments, and reference partnerships where both parties receive something '
       'of genuine value. Outside those structures, the published rate applies. '
       'We set prices we can defend \u2014 and we defend them. This pricing policy applies consistently across all clients. That is what honest by design means in practice. '
       'Contact contact@investpuppy.com to begin that conversation.',
       '', s, story)

    qa('Q13. Is Vektor regulated?',
       'Vektor is a portfolio construction and management platform. Regulatory obligations \u2014 licensing, '
       'client suitability, reporting \u2014 remain with the portfolio manager and the firm operating the '
       'platform. Vektor provides the audit trail and compliance documentation that supports those obligations. '
       'Specific regulatory standing and applicable permissions by jurisdiction are discussed in the Founding '
       'Mandate due diligence process.',
       'See: WP-06: Audit Trail & Compliance, WP-08: AI as Instrument', s, story)

    qa('Q14. How do I get started?',
       'Reach out to contact@investpuppy.com or visit investpuppy.com. The first conversation is about '
       'understanding your current workflow, your client base, and whether Vektor is the right fit \u2014 '
       'there is no commitment required. If you prefer, it can be covered by mutual NDA from the outset. '
       'We would genuinely like to hear from you.',
       '', s, story)

    qa('Q15. Can you demonstrate Vektor on our data?',
       'Yes. Pick any listed equity market, any currency, any benchmark. '
       'We will run the full Vektor workflow against it and show you the output: '
       'the efficient frontier, the correlation matrix, the max-Sharpe allocation, '
       'and the per-instrument signal selection. No slides. No promises. '
       'Just the platform, working on your data.',
       'Enquire about Founding Mandate availability at investpuppy.com',
       s, story)

    story.append(sp(10))
    story.append(HRule(COL_W, GOLD, 0.8, 4, 4))
    story.append(sp(6))
    story.append(para(
        f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  Full document suite available on request.',
        s, 'see'))
    story.append(sp(4))
    story.append(para(
        f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {DOC_REF}  \u00b7  Copyright 2026 InvestPuppy',
        s, 'wp_ref'))

    doc.build(story)
    print(f'Built: {out}')
    import subprocess
    r=subprocess.run(['pdfinfo',out],capture_output=True,text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l or 'File' in l: print(l)

if __name__=='__main__': build()
