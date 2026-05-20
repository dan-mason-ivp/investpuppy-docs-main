"""
ip-founder-context.pdf  v1.1
InvestPuppy — Founder Context document
Tier 1 registration-gated. No names. No vendor specifics.
Build: python3 build_founder_context.py
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 HRFlowable, Table, TableStyle)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.lib.utils import ImageReader

OUT  = "/home/claude/ip-founder-context.pdf"
LOGO = "/mnt/user-data/uploads/ip_logo_vertical.png"

GREEN = colors.HexColor("#85D155")
DARK  = colors.HexColor("#0A0A0A")
DARK2 = colors.HexColor("#0F1A0F")
BODY  = colors.HexColor("#1A1A1A")
GREY  = colors.HexColor("#888888")
WHITE = colors.white
GOLD  = colors.HexColor("#C8A96E")
LIGHT = colors.HexColor("#F7F7F7")
SECT  = colors.HexColor("#F0F7EA")
RULE  = colors.HexColor("#E0E0E0")
RULE2 = colors.HexColor("#2A2A2A")

FP = "/usr/share/fonts/truetype/google-fonts/"
for n in ["Poppins-Light","Poppins-Regular","Poppins-Medium","Poppins-Bold",
          "Poppins-Italic","Poppins-BoldItalic","Poppins-LightItalic"]:
    pdfmetrics.registerFont(TTFont(n, FP + n + ".ttf"))

W, H   = A4
ML, MR = 58, 58
MT, MB = 72, 60

# ── Styles ─────────────────────────────────────────────────────────────────────
def _styles():
    s = {}
    s["body"]  = ParagraphStyle("body",  fontName="Poppins-Light",   fontSize=10.5,
                  leading=17.5, textColor=BODY, spaceAfter=10, alignment=TA_JUSTIFY)
    s["bodyl"] = ParagraphStyle("bodyl", fontName="Poppins-Light",   fontSize=10.5,
                  leading=17.5, textColor=BODY, spaceAfter=10, alignment=TA_LEFT)
    s["lead"]  = ParagraphStyle("lead",  fontName="Poppins-Light",   fontSize=12,
                  leading=20,   textColor=BODY, spaceAfter=12, alignment=TA_JUSTIFY)
    s["h2"]    = ParagraphStyle("h2",    fontName="Poppins-Bold",    fontSize=13,
                  leading=20,   textColor=DARK, spaceAfter=6,  spaceBefore=22)
    s["h3"]    = ParagraphStyle("h3",    fontName="Poppins-Bold",    fontSize=10.5,
                  leading=16,   textColor=GREEN,spaceAfter=4,  spaceBefore=14)
    s["pq"]    = ParagraphStyle("pq",    fontName="Poppins-BoldItalic", fontSize=11.5,
                  leading=19,   textColor=GREEN,spaceAfter=6,  spaceBefore=6,
                  leftIndent=18, rightIndent=18, alignment=TA_LEFT)
    s["qt"]    = ParagraphStyle("qt",    fontName="Poppins-BoldItalic", fontSize=12,
                  leading=20,   textColor=GREEN,spaceAfter=8,  spaceBefore=8,
                  leftIndent=20, rightIndent=20, alignment=TA_CENTER)
    s["note"]  = ParagraphStyle("note",  fontName="Poppins-Regular", fontSize=9.5,
                  leading=15,   textColor=BODY, spaceAfter=6,
                  backColor=SECT, borderPadding=(8,12,8,12))
    s["small"] = ParagraphStyle("small", fontName="Poppins-Light",   fontSize=8.5,
                  leading=13,   textColor=GREY, spaceAfter=4)
    s["cta"]   = ParagraphStyle("cta",   fontName="Poppins-Bold",    fontSize=11,
                  leading=16,   textColor=GREEN,spaceAfter=4,  alignment=TA_CENTER)
    s["email"] = ParagraphStyle("email", fontName="Poppins-Bold",    fontSize=14,
                  leading=20,   textColor=GREEN,spaceAfter=4,  alignment=TA_CENTER)
    s["link"]  = ParagraphStyle("link",  fontName="Poppins-Light",   fontSize=9.5,
                  leading=14,   textColor=GREY, spaceAfter=0,  alignment=TA_CENTER)
    return s

ST = _styles()

def B(t): return f'<font name="Poppins-Bold">{t}</font>'
def I(t): return f'<font name="Poppins-Italic">{t}</font>'
def G(t): return f'<font color="#85D155">{t}</font>'

def hr(col=GREEN, t=1, spb=6, spa=10):
    return HRFlowable(width="100%", thickness=t, color=col,
                      spaceAfter=spa, spaceBefore=spb)

def SP(n=10): return Spacer(1, n)

def pq(text):
    """Pull quote — green left border, italic text."""
    return Paragraph(text, ST["pq"])

# ── Header / footer ────────────────────────────────────────────────────────────
def _hf(c, doc):
    c.saveState()
    pn = c.getPageNumber()
    if pn > 1:
        c.setStrokeColor(RULE); c.setLineWidth(0.5)
        c.line(ML, H - 36, W - MR, H - 36)
        c.setFont("Poppins-Bold", 9); c.setFillColor(DARK)
        c.drawString(ML, H - 26, "Invest")
        iw = c.stringWidth("Invest","Poppins-Bold", 9)
        c.setFillColor(GREEN)
        c.drawString(ML + iw, H - 26, "Puppy")
        c.setFont("Poppins-Light", 8); c.setFillColor(GREY)
        c.drawRightString(W - MR, H - 26,
            "Founder Context \u00b7 Registered distribution")
    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    c.line(ML, MB + 14, W - MR, MB + 14)
    c.setFont("Poppins-Light", 8); c.setFillColor(GREY)
    c.drawString(ML, MB + 3,
        "InvestPuppy Pte Ltd \u00b7 investpuppy.com")
    c.drawRightString(W - MR, MB + 3,
        f"IP-FOUNDER-CONTEXT-260518-1.1  \u00b7  {pn}")
    c.restoreState()

# ── Cover ──────────────────────────────────────────────────────────────────────
def _cover(c):
    c.setFillColor(DARK);  c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(GREEN); c.rect(0, 0, 4, H, fill=1, stroke=0)

    # Logo centred
    lh = 100; lw = 100
    lx = (W - lw) / 2
    ly = H - 54 - lh
    c.drawImage(LOGO, lx, ly, width=lw, height=lh, mask="auto")

    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.line(ML, ly - 22, W - MR, ly - 22)

    c.setFont("Poppins-Regular", 9); c.setFillColor(GREY)
    c.drawCentredString(W/2, ly - 42, "FOUNDER CONTEXT")

    c.setFont("Poppins-Bold", 30); c.setFillColor(WHITE)
    c.drawCentredString(W/2, ly - 86,  "The experience")
    c.drawCentredString(W/2, ly - 124, "behind the platform.")

    c.setFont("Poppins-BoldItalic", 11); c.setFillColor(GREEN)
    c.drawCentredString(W/2, ly - 156, "\u201cHonest by design.\u201d")

    c.setStrokeColor(RULE2); c.setLineWidth(0.5)
    c.line(ML, ly - 174, W - MR, ly - 174)

    meta = [
        ("Document",      "IP-FOUNDER-CONTEXT-260518-1.1"),
        ("Date",          "May 2026"),
        ("Distribution",  "Registered access \u2014 not for onward circulation"),
        ("Company",       "InvestPuppy Pte Ltd"),
    ]
    my = ly - 194
    for lbl, val in meta:
        c.setFont("Poppins-Bold", 8);    c.setFillColor(GREY)
        c.drawString(ML, my, lbl + ":")
        c.setFont("Poppins-Regular", 8); c.setFillColor(WHITE)
        c.drawString(ML + 96, my, val)
        my -= 14

    c.setStrokeColor(RULE2); c.setLineWidth(0.5)
    c.line(ML, MB + 14, W - MR, MB + 14)
    c.setFont("Poppins-Light", 8); c.setFillColor(GREY)
    c.drawString(ML, MB + 3, "InvestPuppy Pte Ltd \u00b7 investpuppy.com")
    c.drawRightString(W - MR, MB + 3, "1")

# ── Story ──────────────────────────────────────────────────────────────────────
def _story():
    s = []
    def H2(t):  s.append(Paragraph(t, ST["h2"]))
    def H3(t):  s.append(Paragraph(t, ST["h3"]))
    def P(t):   s.append(Paragraph(t, ST["body"]))
    def PL(t):  s.append(Paragraph(t, ST["bodyl"]))
    def N(t):   s.append(Paragraph(t, ST["note"]))
    def Q(t):   s.append(Paragraph(t, ST["qt"]))
    def PQ(t):  s.append(pq(t))
    def LG(t):  s.append(Paragraph(t, ST["lead"]))
    def sp(n=10): s.append(SP(n))

    # ── Opening — leads with the problem, not the document ────────────────────
    LG(f'Two people saw the same gap in institutional wealth management from '
       f'opposite ends of the industry. One spent the better part of three decades '
       f'inside the portfolio management technology that institutional asset managers '
       f'use as standard and boutique practitioners have never been able to access. '
       f'One spent two decades building the infrastructure layer \u2014 the cloud-native '
       f'financial architecture that makes institutional-grade systems possible without '
       f'legacy infrastructure constraints. {I("What they built together is the platform "
       f"that closes the gap they both saw.")}')

    sp(6)
    P('This document provides context on that experience \u2014 the domains it covers, '
      'the depth it represents, and why it is directly relevant to what InvestPuppy '
      'has built. It does not name the founders, the institutions they have worked '
      'with, or the platforms they have built on or for. Those details are disclosed '
      'in full at NDA stage.')

    s.append(hr(col=GREEN, t=1.5, spb=6, spa=18))

    # ── Section 1 ─────────────────────────────────────────────────────────────
    H2("1.  The gap we both saw")

    P('Boutique discretionary portfolio managers are managing institutional-scale '
      'complexity with tools that were not built for them. The systematic portfolio '
      'management infrastructure that institutional asset managers use as standard '
      'has never been accessible at boutique scale. The terminal costs are prohibitive. '
      'The integration complexity assumes a large technology team. The consumer-grade '
      'alternatives automate away the judgment that defines boutique wealth management.')

    P(f'This is not a technology gap. {B("It is an access gap.")}')

    P('The two founders of InvestPuppy saw this gap from different sides of the '
      'same industry \u2014 one from the portfolio management and wealth management '
      'application layer, one from the core financial technology infrastructure layer. '
      'They arrived at the same conclusion independently: the tools that boutique '
      'practitioners need have existed for decades at institutional scale. Nobody '
      'had built the version that boutique practitioners can actually use.')

    P(f'{B("InvestPuppy was not formed by strangers.")} The founding team\u2019s '
      f'professional relationship spans approximately a decade, established through '
      f'shared work in institutional financial technology. Vektor is not the output '
      f'of a six-month startup sprint. It is the output of a working partnership '
      f'that long preceded it.')

    sp(4)
    s.append(hr(col=RULE, t=0.5, spb=4, spa=4))

    # ── Section 2 ─────────────────────────────────────────────────────────────
    H2("2.  Chief Executive Officer")
    H3("Portfolio management \u00b7 Wealth management \u00b7 Institutional deployments")

    P(f'The {B("CEO")} spent the better part of three decades working inside the '
      f'institutional portfolio management technology that boutique practitioners '
      f'cannot access \u2014 spanning the product\u2019s full commercial lifecycle. '
      f'This was not observational experience. It was operational, at every stage '
      f'of the implementation lifecycle: vendor, implementation specialist, '
      f'solution architect, and programme and engagement management for '
      f'major institutional deployments.')

    P('The institutional clients in those engagements included some of the largest '
      'wealth management and private banking operations in the world. The CEO\u2019s '
      'role was to design, architect, and deliver solutions that met the operational, '
      'compliance, and performance requirements of Global Tier 1 banks and their '
      'wealth management divisions \u2014 and to own those client relationships '
      'commercially through delivery.')

    PQ('\u201cThe Unvarnished series is a partial record of what was seen in those '
       'rooms \u2014 not as an observer, but as the person responsible for the outcome.\u201d')

    P(f'What this experience provides is not a general familiarity with institutional '
      f'portfolio management technology. It is a {I("specific and forensic knowledge")} '
      f'of how these systems work from the inside \u2014 their architectural limitations, '
      f'their implementation failure modes, the commercial structures that make them '
      f'inaccessible at boutique scale, and the client relationship patterns that '
      f'determine whether they succeed or fail in deployment.')

    N(f'{B("What this means for Vektor:")} The platform was not designed by someone '
      f'who studied the problem from outside. It was designed by someone who spent '
      f'the better part of three decades inside the systems that boutique practitioners '
      f'cannot access \u2014 managing the engagements, owning the client relationships, '
      f'and building Vektor specifically to close the gap those systems leave open.')

    sp(4)
    s.append(hr(col=RULE, t=0.5, spb=4, spa=4))

    # ── Section 3 ─────────────────────────────────────────────────────────────
    H2("3.  Chief Technology Officer")
    H3("Core banking infrastructure \u00b7 Cloud-native architecture \u00b7 Digital banking")

    P(f'The {B("CTO")} spent two decades building the infrastructure layer of '
      f'institutional financial technology \u2014 the systems that financial applications '
      f'are built on, not the applications themselves. This distinction matters. '
      f'Most fintech products are built by teams who understand the application layer. '
      f'The CTO understands both: the infrastructure beneath and the applications above.')

    P('The technical architecture work spans cloud-native core banking infrastructure '
      'deployed by major financial institutions and the end-to-end architecture of '
      'digital challenger bank launches. These are production-grade financial '
      'infrastructure systems operating at institutional scale, built from first '
      'principles under the compliance, data governance, and integration security '
      'requirements that institutional financial technology demands.')

    PQ('\u201cInstitutional-grade financial technology does not happen by accident. '
       'Data residency, audit trail, API integration security \u2014 these are '
       'architectural decisions made at the first line of infrastructure, '
       'not features added afterwards.\u201d')

    P(f'The platform was built to operate {I("within")} custodian-connected financial '
      f'infrastructure, not alongside it. The integration architecture \u2014 including '
      f'the API connectivity model that allows Vektor to sit natively within '
      f'custodian bank operating environments \u2014 reflects two decades of building '
      f'exactly this kind of infrastructure at institutional scale.')

    N(f'{B("What this means for Vektor:")} The platform\u2019s technical architecture '
      f'was designed to meet institutional compliance standards from the ground up \u2014 '
      f'by a CTO who has built institutional-grade financial infrastructure before, '
      f'under the same frameworks that Vektor\u2019s institutional clients will require. '
      f'This is not the typical pre-revenue fintech technical risk profile.')

    sp(4)
    s.append(hr(col=RULE, t=0.5, spb=4, spa=4))

    # ── Section 4 ─────────────────────────────────────────────────────────────
    H2("4.  What the combination represents")

    P(f'The CEO and CTO backgrounds are individually significant. '
      f'Together they are {I("precisely complementary")} for the specific '
      f'problem InvestPuppy is solving.')

    P('The access gap in boutique wealth management has two components. '
      'The first: the portfolio management methodology and workflow used by '
      'institutional asset managers has never been built at boutique scale. '
      'The second: the technical architecture required to deliver that methodology '
      'to compliance, integration, and operational standards has never been '
      'accessible without institutional infrastructure beneath it.')

    P('The CEO\u2019s experience addresses the first component directly \u2014 '
      'three decades of building, implementing, managing, and owning the portfolio '
      'management application layer for institutional clients who take it for '
      'granted. The CTO\u2019s experience addresses the second \u2014 two decades '
      'of building the infrastructure layer that makes institutional-grade financial '
      'technology possible without legacy constraints.')

    Q('\u201cBetween the two founders, the complete institutional financial technology '
      'stack \u2014 from core banking infrastructure to portfolio management application '
      '\u2014 is represented from the inside. Vektor is the product of that combined '
      'knowledge, built for the practitioners who work within it daily.\u201d')

    P(f'This is not a coincidence of hiring. It is the reason Vektor was built '
      f'the way it was built: {I("architecture-first, compliance-by-design, "
      f"practitioner-workflow at the centre.")} The ten Unvarnished papers document '
      f'the failure modes this platform was specifically designed to avoid. '
      f'The technical white paper series documents the methodology it was designed '
      f'to deliver. Both were written by a founding team that has operated inside '
      f'the systems they describe \u2014 together, for approximately a decade, '
      f'before InvestPuppy existed.')

    sp(4)
    s.append(hr(col=RULE, t=0.5, spb=4, spa=4))

    # ── Section 5 ─────────────────────────────────────────────────────────────
    H2("5.  What this document does not tell you \u2014 and why")

    PQ('\u201cWe have not told you everything. That is intentional. And it is honest.\u201d')

    P('There are details of the specific platforms, institutions, and projects '
      'involved in the founding team\u2019s backgrounds that this document does '
      'not disclose. The reasons are straightforward: at this stage of '
      'InvestPuppy\u2019s development, the combination of those details would '
      'make the founding team identifiable in the market before the company '
      'is ready to be identified. This is a deliberate decision, not an evasion.')

    P(f'It is consistent with the same principle that governs the platform: '
      f'{B("\u201cHonest by design.\u201d")} The document is honest about what '
      f'it contains. It is equally honest about what it does not contain, '
      f'and about why. A document that claimed completeness while omitting '
      f'material information would be a different kind of dishonesty.')

    P('The full founding team biographies \u2014 including the specific platforms, '
      'institutions, and projects referenced here \u2014 are disclosed under NDA. '
      'If the experience described in this document raises questions that require '
      'specific answers before you can assess the proposition, the NDA conversation '
      'is the right next step.')

    N(f'{B("Bring your questions — we will answer every one directly.")} '
      f'The NDA unlocks the full document suite: nineteen Vektor documents, '
      f'full founder biographies, and the complete commercial terms. '
      f'There are no further gates after that.')

    sp(8)
    s.append(hr(col=GREEN, t=1.5, spb=4, spa=18))

    # ── CTA ───────────────────────────────────────────────────────────────────
    s.append(Paragraph("Ready for the full picture?", ST["cta"]))
    sp(6)

    s.append(Paragraph("contact@investpuppy.com", ST["email"]))
    sp(4)
    s.append(Paragraph("investpuppy.com/proof-partners", ST["link"]))
    sp(20)

    s.append(Paragraph(
        'This document is shared under registered access terms. '
        'Not for onward circulation or redistribution. '
        'InvestPuppy Pte Ltd \u00b7 May 2026 \u00b7 IP-FOUNDER-CONTEXT-260518-1.1',
        ST["small"]))

    return s

# ── Document ───────────────────────────────────────────────────────────────────
class _Doc(SimpleDocTemplate):
    def __init__(self, fn):
        super().__init__(fn, pagesize=A4,
                         leftMargin=ML, rightMargin=MR,
                         topMargin=MT, bottomMargin=MB)

def main():
    from pypdf import PdfWriter, PdfReader
    cp = "/tmp/fc_cover.pdf"
    bp = "/tmp/fc_body.pdf"
    c = pdfcanvas.Canvas(cp, pagesize=A4)
    _cover(c); c.save()
    doc = _Doc(bp)
    doc.build(_story(), onFirstPage=_hf, onLaterPages=_hf)
    w = PdfWriter()
    for path in [cp, bp]:
        r = PdfReader(path)
        for pg in r.pages: w.add_page(pg)
    with open(OUT, "wb") as f: w.write(f)
    for path in [cp, bp]: os.remove(path)
    r = PdfReader(OUT)
    print(f"Saved: {OUT} ({os.path.getsize(OUT)//1024}KB, {len(r.pages)} pages)")

if __name__ == "__main__": main()
