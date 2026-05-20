"""
ip-share-structure-briefing.pdf
InvestPuppy \u2014 Share Structure & Founder Control
Internal discussion document for founding team
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable, PageBreak,
                                 KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_CENTER
from reportlab.lib.utils import ImageReader

OUT  = "/home/claude/ip-share-structure-briefing.pdf"
LOGO = "/mnt/user-data/uploads/ip_logo_vertical.png"

GREEN  = colors.HexColor("#85D155")
DARK   = colors.HexColor("#0A0A0A")
BODY   = colors.HexColor("#1A1A1A")
GREY   = colors.HexColor("#888888")
LGREY  = colors.HexColor("#F4F4F4")
WHITE  = colors.white
GOLD   = colors.HexColor("#C8A96E")
RULE   = colors.HexColor("#E2E2E2")
SECT   = colors.HexColor("#F0F7EA")
WARN   = colors.HexColor("#FFF8E6")
WARNB  = colors.HexColor("#856404")
BLUE   = colors.HexColor("#1A3A5C")

FP = "/usr/share/fonts/truetype/google-fonts/"
for n in ["Poppins-Light","Poppins-Regular","Poppins-Medium","Poppins-Bold",
          "Poppins-Italic","Poppins-BoldItalic","Poppins-LightItalic"]:
    pdfmetrics.registerFont(TTFont(n, FP + n + ".ttf"))

W, H   = A4
ML, MR = 54, 54
MT, MB = 68, 54

def _styles():
    s = {}
    s["body"]  = ParagraphStyle("body",  fontName="Poppins-Light",   fontSize=10,
                  leading=16.5, textColor=BODY, spaceAfter=8, alignment=TA_JUSTIFY)
    s["bodyl"] = ParagraphStyle("bodyl", fontName="Poppins-Light",   fontSize=10,
                  leading=16.5, textColor=BODY, spaceAfter=8, alignment=TA_LEFT)
    s["bodys"] = ParagraphStyle("bodys", fontName="Poppins-Light",   fontSize=9,
                  leading=14,   textColor=BODY, spaceAfter=4, alignment=TA_LEFT)
    s["h1"]    = ParagraphStyle("h1",    fontName="Poppins-Bold",    fontSize=18,
                  leading=26,   textColor=DARK, spaceAfter=4, spaceBefore=4)
    s["h2"]    = ParagraphStyle("h2",    fontName="Poppins-Bold",    fontSize=12,
                  leading=18,   textColor=DARK, spaceAfter=4, spaceBefore=18)
    s["h3"]    = ParagraphStyle("h3",    fontName="Poppins-Bold",    fontSize=10,
                  leading=15,   textColor=GREEN,spaceAfter=4, spaceBefore=12)
    s["small"] = ParagraphStyle("small", fontName="Poppins-Light",   fontSize=8.5,
                  leading=13,   textColor=GREY, spaceAfter=4)
    s["note"]  = ParagraphStyle("note",  fontName="Poppins-Regular", fontSize=9.5,
                  leading=15,   textColor=BODY, spaceAfter=6,
                  backColor=SECT, borderPadding=(7,10,7,10))
    s["warn"]  = ParagraphStyle("warn",  fontName="Poppins-Bold",    fontSize=9.5,
                  leading=15,   textColor=WARNB,spaceAfter=6,
                  backColor=WARN, borderPadding=(7,10,7,10))
    s["num"]   = ParagraphStyle("num",   fontName="Poppins-Bold",    fontSize=10,
                  leading=15,   textColor=GREEN,spaceAfter=2, spaceBefore=8)
    s["th"]    = ParagraphStyle("th",    fontName="Poppins-Bold",    fontSize=9,
                  leading=13,   textColor=WHITE,spaceAfter=0)
    s["td"]    = ParagraphStyle("td",    fontName="Poppins-Light",   fontSize=9,
                  leading=13,   textColor=BODY, spaceAfter=0)
    s["tdb"]   = ParagraphStyle("tdb",   fontName="Poppins-Bold",    fontSize=9,
                  leading=13,   textColor=DARK, spaceAfter=0)
    s["tdg"]   = ParagraphStyle("tdg",   fontName="Poppins-Bold",    fontSize=9,
                  leading=13,   textColor=GREEN,spaceAfter=0)
    return s

ST = _styles()

def B(t): return f'<font name="Poppins-Bold">{t}</font>'
def I(t): return f'<font name="Poppins-Italic">{t}</font>'
def G(t): return f'<font color="#85D155">{t}</font>'
def Au(t):return f'<font color="#C8A96E">{t}</font>'

def hr(col=RULE, t=0.5, spb=4, spa=8):
    return HRFlowable(width="100%", thickness=t, color=col,
                      spaceAfter=spa, spaceBefore=spb)

def SP(n=8): return Spacer(1, n)

def note(t): return Paragraph(t, ST["note"])
def warn(t): return Paragraph(t, ST["warn"])

def section(title, sub=None):
    items = [hr(col=DARK, t=0.5, spb=16, spa=2),
             Paragraph(title, ST["h2"])]
    if sub:
        items.append(Paragraph(sub, ST["small"]))
    items.append(hr(col=GREEN, t=1.2, spb=0, spa=8))
    return items

def numbered(n, title, body):
    return KeepTogether([
        Paragraph(f"{n}.", ST["num"]),
        Paragraph(f"{B(title)}", ST["h3"]),
        Paragraph(body, ST["body"]),
    ])

# ── Header/footer ──────────────────────────────────────────────────────────────
def _hf(c, doc):
    c.saveState()
    pn = c.getPageNumber()
    if pn > 1:
        c.setStrokeColor(RULE); c.setLineWidth(0.5)
        c.line(ML, H-34, W-MR, H-34)
        c.setFont("Poppins-Bold", 9); c.setFillColor(DARK)
        c.drawString(ML, H-25, "Invest")
        iw = c.stringWidth("Invest","Poppins-Bold",9)
        c.setFillColor(GREEN); c.drawString(ML+iw, H-25, "Puppy")
        c.setFont("Poppins-Light", 8); c.setFillColor(GREY)
        c.drawRightString(W-MR, H-25,
            "Share Structure & Founder Control \u00b7 Internal Discussion")
    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    c.line(ML, MB+14, W-MR, MB+14)
    c.setFont("Poppins-Light", 8); c.setFillColor(GREY)
    c.drawString(ML, MB+3,
        "InvestPuppy \u00b7 Internal Discussion Document \u00b7 Not Legal Advice")
    c.drawRightString(W-MR, MB+3,
        f"IP-SHARE-BRIEF-260518-1.0  \u00b7  {pn}")
    c.restoreState()

# ── Cover ──────────────────────────────────────────────────────────────────────
def _cover(c):
    # White background - this is a working document
    c.setFillColor(WHITE); c.rect(0, 0, W, H, fill=1, stroke=0)
    # Green top band
    c.setFillColor(GREEN); c.rect(0, H-6, W, 6, fill=1, stroke=0)
    # Gold left accent
    c.setFillColor(GOLD); c.rect(0, 0, 5, H-6, fill=1, stroke=0)

    # Logo
    lh = 80; lw = 80
    lx = ML; ly = H - 52 - lh
    c.drawImage(LOGO, lx, ly, width=lw, height=lh, mask="auto")

    # Title block
    c.setFont("Poppins-Bold", 26); c.setFillColor(DARK)
    c.drawString(ML, ly - 42, "Share Structure &")
    c.drawString(ML, ly - 72, "Founder Control")
    c.setFont("Poppins-Light", 12); c.setFillColor(GREY)
    c.drawString(ML, ly - 96, "A briefing note for the founding team")

    # Divider
    c.setStrokeColor(RULE); c.setLineWidth(1)
    c.line(ML, ly - 112, W-MR, ly - 112)

    # Purpose box
    box_y = ly - 116
    c.setFillColor(SECT)
    c.roundRect(ML, box_y - 90, W-ML-MR, 88, 4, fill=1, stroke=0)
    c.setStrokeColor(GREEN); c.setLineWidth(1.5)
    c.line(ML, box_y - 90, ML, box_y - 2)

    c.setFont("Poppins-Bold", 10); c.setFillColor(DARK)
    c.drawString(ML + 14, box_y - 18, "Purpose of this document")
    c.setFont("Poppins-Light", 9.5); c.setFillColor(BODY)
    lines = [
        "This document summarises the recommended share class structure,",
        "founder control mechanisms, and investor protection provisions for",
        "InvestPuppy. It is a briefing note for founding team discussion \u2014",
        "not a legal document and not legal advice. All decisions require",
        "review and implementation by qualified UK and Singapore lawyers.",
    ]
    ty = box_y - 36
    for line in lines:
        c.drawString(ML + 14, ty, line)
        ty -= 13

    # Meta
    meta_y = box_y - 116
    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    c.line(ML, meta_y + 4, W-MR, meta_y + 4)
    meta = [
        ("Document",     "IP-SHARE-BRIEF-260518-1.0"),
        ("Date",         "May 2026"),
        ("Status",       "Internal discussion \u2014 founding team only"),
        ("Legal status", "Not legal advice. Requires qualified counsel in UK and Singapore."),
    ]
    my = meta_y - 12
    for lbl, val in meta:
        c.setFont("Poppins-Bold", 8.5); c.setFillColor(GREY)
        c.drawString(ML, my, lbl + ":")
        c.setFont("Poppins-Regular", 8.5); c.setFillColor(DARK)
        c.drawString(ML + 100, my, val)
        my -= 14

    # Contents
    cx = ML + 487/2
    c.setFont("Poppins-Bold", 8.5); c.setFillColor(GOLD)
    c.drawString(cx, meta_y - 12, "Contents")
    sections = [
        ("1.", "Company structure and rationale"),
        ("2.", "Recommended share structure at incorporation"),
        ("3.", "Illustrative cap table"),
        ("4.", "Founder control mechanisms"),
        ("5.", "Investor protections"),
        ("6.", "Founder vesting"),
        ("7.", "The EIS constraint"),
        ("8.", "What converts and when"),
        ("9.", "Open decisions and next steps"),
    ]
    cy = meta_y - 28
    for num, title in sections:
        c.setFont("Poppins-Bold", 8.5); c.setFillColor(GOLD)
        c.drawString(cx, cy, num)
        c.setFont("Poppins-Regular", 8.5); c.setFillColor(DARK)
        c.drawString(cx + 18, cy, title)
        cy -= 13

    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    c.line(ML, MB+14, W-MR, MB+14)
    c.setFont("Poppins-Light", 8); c.setFillColor(GREY)
    c.drawString(ML, MB+3,
        "InvestPuppy \u00b7 Internal Discussion Document \u00b7 Not Legal Advice")
    c.drawRightString(W-MR, MB+3, "1")

# ── Table helper ───────────────────────────────────────────────────────────────
def gtable(headers, rows, cws, last_green=False, last_bold=False):
    data = [[Paragraph(h, ST["th"]) for h in headers]]
    for i, row in enumerate(rows):
        is_last = (i == len(rows) - 1)
        style = ST["tdg"] if (is_last and last_green) else                 ST["tdb"] if (is_last and last_bold) else ST["td"]
        data.append([Paragraph(cell, style) for cell in row])
    t = Table(data, colWidths=cws)
    ts = [
        ("FONTNAME", (0,0),(-1,-1),"Poppins-Light"),
        ("FONTSIZE", (0,0),(-1,-1), 9),
        ("VALIGN",   (0,0),(-1,-1),"MIDDLE"),
        ("BACKGROUND",(0,0),(-1,0), DARK),
        ("TEXTCOLOR", (0,0),(-1,0), WHITE),
        ("FONTNAME",  (0,0),(-1,0),"Poppins-Bold"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LGREY]),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ("GRID",         (0,0),(-1,-1), 0.3, RULE),
    ]
    if last_green:
        ts += [("BACKGROUND",(0,-1),(-1,-1), SECT),
               ("FONTNAME",  (0,-1),(-1,-1),"Poppins-Bold")]
    t.setStyle(TableStyle(ts))
    return t

# ── Story ──────────────────────────────────────────────────────────────────────
def _story():
    s = []
    def H2(t, sub=None):
        for i in section(t, sub): s.append(i)
    def H3(t): s.append(Paragraph(t, ST["h3"]))
    def P(t):  s.append(Paragraph(t, ST["body"]))
    def PL(t): s.append(Paragraph(t, ST["bodyl"]))
    def N(t):  s.append(note(t))
    def WN(t): s.append(warn(t))
    def sp(n=8): s.append(SP(n))

    # ── Legal disclaimer ───────────────────────────────────────────────────────
    WN("This document is a discussion briefing, not legal advice. Every decision "
      "described here requires review and implementation by qualified lawyers in "
      "the UK and Singapore before any company is incorporated or any shares are "
      "issued. Consult a UK startup solicitor and a Singapore corporate lawyer "
      "before acting on anything in this document.")
    sp(6)

    # ── Section 1 ─────────────────────────────────────────────────────────────

    # \u2014\u2014 Section 0: Company structure intro \u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014
    H2("1.  Company Structure and Rationale",
       "UK Holdco + Singapore OpCo \u00b7 Why this structure \u00b7 What each entity does")

    P("Neither InvestPuppy entity exists yet. Both are to be established. "
      "This is a significant advantage: the structure can be designed correctly "
      "from the outset, without the constraints, legacy IP considerations, or "
      "tax complications that arise when restructuring an existing company. "
      "The recommendations in this document reflect that clean-slate opportunity.")

    sp(8)
    H3("The structure in one diagram")

    # Structure diagram as a simple table
    diag_data = [
        [Paragraph(B("InvestPuppy Ltd"), ST["th"]),
         Paragraph("UK Private Limited Company", ST["th"])],
        [Paragraph("UK Holdco", ST["tdg"]),
         Paragraph(
             "Parent entity. Fundraising vehicle for all equity investment. "
             "Holds 100% of the Singapore OpCo. "
             "UK-incorporated, English law governed, EIS-qualifying.",
             ST["td"])],
        [Paragraph("\u2193  100% ownership", ST["tdb"]),
         Paragraph("", ST["td"])],
        [Paragraph(B("InvestPuppy Pte Ltd"), ST["tdb"]),
         Paragraph("Singapore Private Limited Company", ST["tdb"])],
        [Paragraph("Singapore OpCo", ST["tdg"]),
         Paragraph(
             "Operating entity. Employs the technical team. Holds the platform, "
             "IP, and operational infrastructure. Singapore-incorporated, "
             "subject to MAS framework.",
             ST["td"])],
    ]
    diag = Table(diag_data, colWidths=[130, 357])
    diag.setStyle(TableStyle([
        ("FONTNAME",     (0,0),(-1,-1),"Poppins-Light"),
        ("FONTSIZE",     (0,0),(-1,-1),9),
        ("VALIGN",       (0,0),(-1,-1),"MIDDLE"),
        ("BACKGROUND",   (0,0),(-1,0), DARK),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("FONTNAME",     (0,0),(-1,0),"Poppins-Bold"),
        ("BACKGROUND",   (0,2),(1,2), WHITE),
        ("BACKGROUND",   (0,3),(-1,3), LGREY),
        ("FONTNAME",     (0,3),(-1,3),"Poppins-Bold"),
        ("ROWBACKGROUNDS",(0,4),(-1,4),[SECT]),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("GRID",         (0,0),(-1,-1), 0.3, RULE),
        ("SPAN",         (0,2),(1,2)),
        ("ALIGN",        (0,2),(1,2), "CENTER"),
    ]))
    s.append(diag)
    sp(10)

    H3("Why a two-entity structure")
    P("InvestPuppy is building a platform for three primary markets: Singapore, "
      "the United Kingdom, and Switzerland. Each market has distinct regulatory, "
      "investor, and commercial requirements. A single entity cannot optimally "
      "serve all three simultaneously. The UK Holdco and Singapore OpCo are each "
      "the right vehicle for the specific functions they perform.")

    sp(6)

    # Two column rationale table
    rat_data = [
        [Paragraph(B("UK Holdco"), ST["th"]),
         Paragraph(B("Singapore OpCo"), ST["th"])],
        [Paragraph(
            f"{B('Fundraising vehicle')} for all equity investment \u2014 "
            f"both Singapore and UK investors subscribe to UK Holdco shares. "
            f"English law subscription agreements. "
            f"Familiar to international investors.",
            ST["bodys"]),
         Paragraph(
            f"{B('Operating entity')} \u2014 employs the technical team, "
            f"holds the platform and IP, manages Singapore client relationships "
            f"and APAC custodian infrastructure.",
            ST["bodys"])],
        [Paragraph(
            f"{B('EIS/SEIS qualifying')} for UK angel investors. "
            f"HMRC EIS relief (30% income tax relief + CGT exemption) "
            f"requires investment into a UK-incorporated ordinary share "
            f"company. Opens the UK angel investor pool materially.",
            ST["bodys"]),
         Paragraph(
            f"{B('Singapore regulatory home')} \u2014 MAS Technology Risk "
            f"Management framework compliance, Singapore data residency "
            f"requirements, and any future MAS licensing all sit at the "
            f"Singapore OpCo level.",
            ST["bodys"])],
        [Paragraph(
            f"{B('FCA regulatory pathway')} \u2014 UK distribution requires "
            f"FCA authorisation. A UK-incorporated entity is the natural "
            f"applicant. The FCA\u2019s SM\u0026CR Senior Manager regime "
            f"requires a UK-based senior management presence that the "
            f"UK Holdco provides.",
            ST["bodys"]),
         Paragraph(
            f"{B('Singapore government grants')} \u2014 MAS FSTI grants, "
            f"Enterprise Development Grants, and Startup SG Equity "
            f"co-investment are all directed at Singapore-incorporated "
            f"operating entities. Non-dilutive funding flows here.",
            ST["bodys"])],
        [Paragraph(
            f"{B('European exit accessibility')} \u2014 the primary "
            f"trade sale acquirers (institutional fintech consolidators "
            f"in Switzerland, Germany, and the UK) have established "
            f"UK M\u0026A infrastructure. A UK holding company "
            f"simplifies the acquisition process.",
            ST["bodys"]),
         Paragraph(
            f"{B('APAC infrastructure')} \u2014 the OpenWealth API credentials "
            f"and APAC custodian relationships that underpin the Wrapped channel "
            f"are anchored in the Singapore operating entity and its "
            f"institutional network.",
            ST["bodys"])],
        [Paragraph(
            f"{B('European investor comfort')} \u2014 UK private limited "
            f"company law and English-law documentation are the standard "
            f"for UK, Swiss, and broader European institutional investors "
            f"and corporate venture arms.",
            ST["bodys"]),
         Paragraph(
            f"{B('Technical team base')} \u2014 all employees, including both founders at this stage, are employed by "
            f"the Singapore OpCo. "
            f"Singapore employment law, CPF contributions, and "
            f"Singapore-resident director requirements are all "
            f"managed at this level.",
            ST["bodys"])],
    ]
    rat = Table(rat_data, colWidths=[243, 244])
    rat.setStyle(TableStyle([
        ("FONTNAME",     (0,0),(-1,-1),"Poppins-Light"),
        ("FONTSIZE",     (0,0),(-1,-1),9),
        ("VALIGN",       (0,0),(-1,-1),"TOP"),
        ("BACKGROUND",   (0,0),(-1,0), DARK),
        ("TEXTCOLOR",    (0,0),(-1,0), WHITE),
        ("FONTNAME",     (0,0),(-1,0),"Poppins-Bold"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE, LGREY]),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ("GRID",         (0,0),(-1,-1), 0.3, RULE),
        ("LINEAFTER",    (0,0),(0,-1), 0.5, RULE),
    ]))
    s.append(rat)
    sp(10)

    H3("How each entity relates to the other")
    P("The UK Holdco owns 100% of the Singapore OpCo. Investor capital raised "
      "by the UK Holdco flows to the Singapore OpCo through an intercompany loan "
      "facility for operational deployment. The Singapore OpCo provides services "
      "to the UK Holdco under a management services agreement, ensuring the "
      "intercompany relationship is documented and transfer-pricing compliant.")

    sp(4)
    N(f"{B('IP ownership:')} A decision is required on whether the platform IP "
      f"transfers from the Singapore OpCo to the UK Holdco (cleaner for exit, "
      f"triggers Singapore stamp duty), or remains in the Singapore OpCo under "
      f"an exclusive licence to the UK Holdco (avoids stamp duty, requires "
      f"transfer pricing documentation). Both are standard structures. "
      f"This decision requires advice from both UK and Singapore legal counsel "
      f"and should be made before incorporation.")
    sp(6)

    H3("What this structure does not do")
    P("The UK Holdco is a holding and governance entity. It does not conduct "
      "day-to-day operations. It does not hold regulatory licences (MAS, FCA). "
      "It does not employ the Singapore-based team. All operational activity, "
      "client relationships, and technical infrastructure sit in the Singapore OpCo "
      "as a wholly-owned subsidiary. The UK Holdco\u2019s value derives entirely "
      "from its 100% ownership of the Singapore OpCo and the IP it holds or licences.")

    sp(4)
    N(f"{B('Singapore OpCo one-director requirement:')} Singapore Companies Act "
      f"requires at least one Singapore-resident director. The CTO satisfies this "
      f"requirement as a Singapore citizen and co-founder. No additional "
      f"Singapore-resident director hire is needed at incorporation.")

    sp(6)
    H3("Why not a Singapore-only or UK-only structure")
    P("A Singapore-only structure (InvestPuppy Pte Ltd as the single entity) "
      "was the simplest option but was ruled out on two specific grounds: "
      "EIS/SEIS qualification for UK investors requires investment into a UK "
      "entity, and FCA regulatory authorisation is most cleanly pursued "
      "through a UK-incorporated entity. Both are material for InvestPuppy\u2019s "
      "UK market development and investor access strategy.")

    P("A UK-only structure was considered and rejected: Singapore is the primary "
      "market and the operating entity must be Singapore-incorporated to access "
      "Singapore government co-investment programmes, MAS regulatory engagement, "
      "and the Singapore-resident technical team structure.")

    sp(4)
    N(f"{B('The clean-slate advantage:')} Neither entity has yet been incorporated. "
      f"This means the structure can be established correctly from the outset \u2014 "
      f"with the right share classes, the right intercompany agreements, "
      f"and the right IP assignment \u2014 without the cost and complexity "
      f"of restructuring an existing company. This window should not be wasted "
      f"by incorporating prematurely before the structure is fully decided.")

    sp(4)
    s.append(hr(col=RULE, t=0.5, spb=4, spa=4))

    # \u2014\u2014 Section 1 renumbered to Section 2 \u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014\u2014

    H2("2.  Recommended Share Structure at Incorporation",
       "Two share classes \u00b7 EIS-compatible \u00b7 Founder voting control maintained")

    P("At incorporation, InvestPuppy UK Holdco should issue two classes of ordinary "
      "shares. Both classes carry identical economic rights \u2014 the same entitlement "
      "to dividends and capital proceeds per share. The difference is voting rights only.")

    sp(4)
    cw = 487
    s.append(gtable(
        ["Share class","Issued to","Votes per share","Economic rights","EIS qualifying"],
        [["A Ordinary", "Founders only",
          "10 votes per share",
          "Identical to B shares \u2014 same dividends, same proceeds per share on exit",
          "Yes \u2014 ordinary shares with no preferential economic rights"],
         ["B Ordinary", "Investors + option pool",
          "1 vote per share",
          "Identical to A shares",
          "Yes \u2014 standard EIS-qualifying ordinary shares"],
         ["Option pool", "Employees (unissued at incorporation)",
          "1 vote per share when issued",
          "Same as B shares on exercise",
          "EMI options \u2014 separate tax treatment on exercise"]],
        [80, 100, 80, 160, 67],
    ))
    sp(8)
    N(f"{B('Why dual-class ordinary shares?')} EIS investors must subscribe for "
      f"ordinary shares \u2014 preference shares do not qualify for EIS tax relief. "
      f"Dual-class ordinary shares give founders enhanced voting control without "
      f"creating economic preferences that would disqualify the investment. "
      f"This structure is well-established in UK seed rounds and is HMRC-compliant.")
    sp(4)
    N(f"{B('Why 10:1 voting ratio?')} A 10:1 ratio means founders retain "
      f"approximately 97% of votes after a 20% seed round, falling to "
      f"approximately 88% after a further Series A dilution. "
      f"Founders maintain genuine operational and strategic control through "
      f"both funding rounds. A 5:1 ratio is also acceptable and may be "
      f"less contentious in negotiation \u2014 discuss with legal counsel.")

    # ── Section 2 ─────────────────────────────────────────────────────────────
    s.append(PageBreak())
    H2("3.  Illustrative Cap Table",
       "Example numbers for discussion \u2014 not commitments")

    P("The following tables use illustrative share counts and prices to show "
      "how ownership and voting rights evolve through incorporation and the "
      "seed round. Actual numbers will be agreed with legal counsel.")

    sp(8)
    H3("At incorporation")
    cw2 = 487
    s.append(gtable(
        ["Holder","Shares","Class","Votes","Economic %","Notes"],
        [["CEO",     "425,000","A Ord","4,250,000","42.5%","Subject to vesting"],
         ["CTO",     "425,000","A Ord","4,250,000","42.5%","Subject to vesting"],
         ["Option pool","150,000","B Ord (unissued)","0","15.0%","Reserved, not yet granted"],
         ["Total","1,000,000","","8,500,000","100%",""]],
        [80, 70, 90, 80, 80, 87],
        last_bold=True,
    ))
    sp(4)
    N(f"{B('Option pool note:')} The 15% option pool is created at incorporation "
      f"before any investor subscribes. This means the dilution falls on the founders "
      f"at zero company value \u2014 not on the investors. At seed stage, investors "
      f"will expect a 10\u201315% option pool to be in place pre-investment. "
      f"Creating it at incorporation is the cleanest approach.")

    sp(12)
    H3("Post-seed round (illustrative: US$2M at US$9M pre-money)")
    P("At US$9M pre-money with 1,000,000 shares outstanding, the implied price "
      "per share is US$9.00. A US$2M investment creates approximately 222,000 "
      "new B ordinary shares, representing approximately 18% of the post-money "
      "fully diluted share capital.")

    sp(6)
    s.append(gtable(
        ["Holder","Shares","Class","Votes","Economic %","Notes"],
        [["CEO",     "425,000","A Ord","4,250,000","34.1%","4-year vest from incorporation"],
         ["CTO",     "425,000","A Ord","4,250,000","34.1%","4-year vest from incorporation"],
         ["Option pool","150,000","B Ord (unissued)","0","12.0%","EMI scheme post-funding"],
         ["Seed investors","222,000","B Ord","222,000","17.8%","US$2M at US$9M pre-money"],
         ["Total","1,222,000","","8,722,000","98%*",""]],
        [80, 70, 90, 80, 80, 87],
        last_bold=True,
    ))
    sp(4)
    s.append(Paragraph(
        "* Economic percentages do not sum to 100% due to rounding. "
        "Fully diluted total including unissued option pool: 1,372,000 shares.",
        ST["small"]))
    sp(8)
    N(f"{B('Founder voting control post-seed:')} "
      f"4,250,000 + 4,250,000 = 8,500,000 founder votes. "
      f"Total votes: 8,722,000. "
      f"Founders control {G(B('97.5% of votes'))} while holding "
      f"68.2% of economic interest (excluding unissued option pool).")

    # ── Section 3 ─────────────────────────────────────────────────────────────
    s.append(PageBreak())
    H2("4.  Founder Control Mechanisms",
       "Four layers of protection \u2014 in priority order")

    P("Founder control is maintained through four complementary mechanisms. "
      "The dual-class voting structure is the primary tool at seed stage. "
      "The board composition and reserved matters become the primary tools "
      "at Series A when the dual-class structure typically converts.")

    sp(6)

    items = [
        ("1", "Dual-class voting (A/B ordinary shares)",
         f"A ordinary shares carry 10 votes per share. B shares carry 1. "
         f"Founders hold all A shares. Investors hold B shares. "
         f"This gives founders approximately 97% of votes post-seed on 68% of economics. "
         f"This is the primary founder control mechanism through the seed round and into Series A. "
         f"It {I('typically converts')} to a single share class as a Series A investor condition \u2014 "
         f"by which point board composition provides the ongoing governance protection."),
        ("2", "Board composition",
         f"At seed stage: two founder directors. Seed investors receive {I('observer rights')} "
         f"only \u2014 the right to attend board meetings without voting. "
         f"No investor board seat at seed. "
         f"At Series A: one investor board seat alongside two founder seats. "
         f"Founders retain board majority through Series A. "
         f"The board composition provision should be written into the articles "
         f"and the shareholders\u2019 agreement from incorporation."),
        ("3", "Reserved matters",
         f"Certain decisions require investor consent regardless of voting outcome. "
         f"This is the substantive protection mechanism for investors \u2014 "
         f"and in turn it protects founders from investors acting unilaterally "
         f"on these same matters. "
         f"Standard reserved matters: issuance of new shares beyond the agreed pool; "
         f"sale of the company or major assets; amendment of the articles; "
         f"incurring material debt; key person changes (CEO or CTO departure). "
         f"Reserved matters are negotiated and documented in the shareholders\u2019 agreement."),
        ("4", "CEO casting vote on operational deadlock",
         f"As co-equal founders, the CEO and CTO may reach an operational disagreement "
         f"that cannot be resolved by discussion. A CEO casting vote on board-level "
         f"operational decisions provides a resolution mechanism without undermining "
         f"the co-equal founding structure. "
         f"Strategic decisions \u2014 company sale, major capital raise, key hires \u2014 "
         f"require unanimous founder agreement. "
         f"This provision belongs in the founders\u2019 agreement, not the articles."),
    ]

    for num, title, body in items:
        s.append(KeepTogether([
            Paragraph(f"{num}.  {B(title)}", ST["h3"]),
            Paragraph(body, ST["body"]),
            SP(4),
        ]))

    sp(4)
    WN(f"{B('Deadlock provision:')} A two-founder, co-equal company must have "
      f"a deadlock resolution mechanism documented in the founders\u2019 agreement. "
      f"The most common mechanisms are: Russian roulette (either party can trigger a "
      f"buy-out at a stated price, with the other party able to flip the transaction); "
      f"or Texas shoot-out (sealed bids, highest bidder buys out the other). "
      f"Discuss which mechanism is appropriate with legal counsel before incorporation.")

    # ── Section 4 ─────────────────────────────────────────────────────────────
    s.append(PageBreak())
    H2("5.  Investor Protections",
       "Standard seed-stage provisions \u2014 expected by all sophisticated investors")

    P("Investor protections are not in conflict with founder control. They define "
      "the boundaries within which founders operate freely. Sophisticated investors "
      "will expect these provisions to be present. Attempting to negotiate them away "
      "creates friction and signals governance immaturity.")

    sp(6)

    protections = [
        ("Pre-emption rights on new share issues",
         "Existing investors have the right to participate pro-rata in any subsequent "
         "funding round to maintain their ownership percentage. This prevents investors "
         "from being diluted without the opportunity to invest further. "
         "Standard threshold: applies to all new share issuances beyond the agreed option pool."),
        ("Anti-dilution protection",
         "If InvestPuppy raises a subsequent round at a lower price per share than the "
         "seed round (a \u2018down round\u2019), the seed investors\u2019 conversion price is adjusted "
         "downward so they receive more shares. Weighted average anti-dilution is the "
         "standard at seed stage \u2014 it is less aggressive than full ratchet and more "
         "acceptable to founders."),
        ("Information rights",
         "Investors receive: quarterly management accounts within 30 days of quarter end; "
         "annual audited accounts within six months of year end; prompt notification of "
         "material events (loss of key client, regulatory action, founder departure, "
         "material litigation). These should be in the shareholders\u2019 agreement."),
        ("Drag-along",
         "If shareholders holding 75% or more (by value) of shares agree to sell the "
         "company, they can require the remaining shareholders to sell on the same terms. "
         "This prevents a minority shareholder from blocking a trade sale that the "
         "majority wants to proceed. Standard threshold: 75%."),
        ("Tag-along",
         "If founders sell their shares (or a controlling stake), minority shareholders "
         "have the right to sell their shares on the same terms. Protects investors from "
         "being left behind in a partial exit."),
        ("Good leaver / bad leaver on founder shares",
         "If a founder leaves before their shares are fully vested: "
         "a good leaver (redundancy, death, disability) retains vested shares and may "
         "receive a proportion of unvested shares. "
         "A bad leaver (resignation, gross misconduct, competing business) "
         "retains only vested shares \u2014 unvested shares are bought back at nominal value. "
         "Definitions and proportions are negotiated in the founders\u2019 agreement."),
    ]

    for i, (title, body) in enumerate(protections):
        s.append(KeepTogether([
            Paragraph(f"{B(title)}", ST["h3"]),
            Paragraph(body, ST["body"]),
            SP(4),
        ]))

    # ── Section 5 ─────────────────────────────────────────────────────────────
    s.append(PageBreak())
    H2("6.  Founder Vesting",
       "Standard four-year schedule \u2014 with adjustment for pre-incorporation work")

    P("Founder vesting protects both investors and the remaining founder in the event "
      "that one founder leaves early. It is an expected provision at seed stage and "
      "should be documented in the founders\u2019 agreement, not left to oral understanding.")

    sp(8)

    H3("The standard schedule")
    P("Four-year vest. One-year cliff (no shares vest in the first twelve months; "
      "25% of total shares vest on the cliff date; the remainder vest monthly over "
      "the following three years). This is the global standard for startup founders "
      "and will be required by Series A investors if not already in place.")

    sp(6)
    H3("Adjustment for pre-incorporation work")
    P("Both InvestPuppy founders have made substantial contributions to the platform "
      "before the formal incorporation date. Two approaches are available:")

    sp(4)
    s.append(gtable(
        ["Approach","Description","Pros","Cons"],
        [["Shortened vest (recommended)",
          "Two-year vest from incorporation date, no cliff. Reflects pre-incorporation contribution.",
          "Simple. Clean. No disputes about what counts as pre-incorporation work.",
          "Slightly shorter than VC standard \u2014 may require explanation at Series A."],
         ["Deemed start date",
          "Standard four-year vest from a deemed start date 12\u201324 months before incorporation.",
          "Gives fuller credit for pre-incorporation work.",
          "Requires documentation of pre-incorporation activities. More complex."]],
        [90, 160, 130, 107],
    ))
    sp(8)
    N(f"{B('Recommendation:')} Use the shortened vest approach. "
      f"Two years from incorporation, no cliff. "
      f"This is simple, defensible, and reflects the pre-incorporation effort "
      f"without requiring documentation of every pre-incorporation activity. "
      f"Series A investors can be shown the rationale if asked.")

    sp(8)
    H3("The option pool and EMI scheme")
    P("The 15% option pool created at incorporation is reserved for future employees "
      "and directors. Once the CEO is full-time and the UK Holdco has qualifying "
      "UK business activity, an EMI (Enterprise Management Incentive) option scheme "
      "should be established.")

    sp(4)
    N(f"{B('EMI benefit:')} EMI options qualify for Business Asset Disposal Relief, "
      f"reducing the CGT rate on option gains to 10% compared to the standard 20% rate. "
      f"This is a significant benefit for future hires and makes InvestPuppy\u2019s "
      f"option package considerably more attractive than comparable offers from "
      f"non-EMI companies. Requires HMRC EMI valuation (HMRC\u2019s Share Valuation "
      f"team) and an employment relationship of at least 25 hours per week.")

    # ── Section 6 ─────────────────────────────────────────────────────────────
    s.append(PageBreak())
    H2("7.  The EIS Constraint",
       "Critical: shapes the entire seed-stage share structure")

    P("EIS (Enterprise Investment Scheme) provides UK angel investors with 30% "
      "income tax relief on investments up to \u00a31M per year, plus capital gains "
      "tax exemption on exit. SEIS (Seed EIS) provides 50% relief on up to "
      "\u00a3200,000. For UK investors these reliefs are significant \u2014 they "
      "materially change the investment economics and expand the UK investor pool.")

    sp(6)
    H3("The EIS ordinary share requirement")
    P("EIS investment must be into "
      f"{B('ordinary share capital')}. HMRC defines this as shares that are "
      "not redeemable, carry no preferential right to dividends, and carry "
      "no preferential right to assets on winding up beyond the amount subscribed.")

    sp(4)
    WN(f"{B('This rules out US-style preference shares at seed.')} "
      f"A standard US venture preference share with a 1x non-participating "
      f"liquidation preference does not qualify for EIS. "
      f"If InvestPuppy uses preference shares at seed, UK EIS investors cannot "
      f"participate and the EIS benefit is lost entirely.")

    sp(6)
    H3("What this means for InvestPuppy")
    P("The dual-class ordinary share structure recommended in Section 1 is designed "
      "specifically to be EIS-compatible. Both A and B ordinary shares carry identical "
      "economic rights. The A shares\u2019 enhanced voting is not an economic preference "
      "and does not disqualify the investment for EIS purposes.")

    sp(4)
    N(f"{B('Confirm with HMRC advance assurance.')} Before UK investors subscribe, "
      f"apply to HMRC for EIS advance assurance on the specific share structure "
      f"proposed. HMRC will confirm whether the structure qualifies. "
      f"This is a standard process and takes six to eight weeks. "
      f"No UK EIS investor should subscribe before advance assurance is received.")

    sp(8)
    H3("EIS and the option pool")
    P("Unissued option pool shares do not affect EIS qualification of investor shares "
      "provided they are not yet issued at the time of the EIS investment. "
      "EMI options granted to employees after the EIS investment are separately "
      "structured and do not affect the EIS status of existing ordinary shares.")

    # ── Section 7 ─────────────────────────────────────────────────────────────
    s.append(PageBreak())
    H2("8.  What Converts and When",
       "How the structure evolves from seed through Series A")

    P("The dual-class share structure is designed for the seed and early growth phase. "
      "Understanding what changes at Series A is important for founders planning "
      "ahead and for investors assessing the full structure.")

    sp(6)
    s.append(gtable(
        ["Stage","Event","What changes","What stays the same"],
        [["Incorporation",
          "UK Holdco incorporated, founders subscribe",
          "Nothing \u2014 founding structure established",
          "A/B structure, vesting, option pool"],
         ["Seed close",
          "UK EIS investors subscribe at ~18\u201320% dilution",
          "New B ordinary shares issued. Cap table updated.",
          "A shares remain 10:1 voting. Founders hold 97%+ of votes."],
         ["Between seed and Series A",
          "EMI scheme established post-CEO full-time",
          "Option grants begin under EMI scheme",
          "Share class structure unchanged"],
         ["Series A",
          "VC lead investor subscribes (new preferred or ordinary class)",
          "A shares typically convert to standard ordinary as VC condition. "
          "New Series A share class introduced. One VC board seat added.",
          "Founders retain board majority (2 founder:1 VC). "
          "Reserved matters remain. Pre-emption rights continue."],
         ["Exit (trade sale)",
          "Drag-along triggered at 75%+ shareholder approval",
          "All shares sold at agreed price. Vesting lapses.",
          "Good/bad leaver provisions may apply to unvested shares."]],
        [70, 130, 160, 127],
    ))

    sp(8)
    N(f"{B('Planning note on Series A conversion:')} The conversion of A shares to "
      f"standard ordinary shares at Series A is standard market practice. "
      f"Founders should plan for this and understand that post-Series A governance "
      f"protection relies on board composition and reserved matters, not voting ratio. "
      f"The board composition provision \u2014 two founder seats, one VC seat \u2014 "
      f"should be locked into the Series A term sheet as a non-negotiable.")

    # ── Section 8 ─────────────────────────────────────────────────────────────
    s.append(PageBreak())
    H2("9.  Open Decisions and Next Steps",
       "What needs to be agreed before incorporation")

    P("The following decisions must be made before the UK Holdco is incorporated "
      "and before any shares are issued. They cannot be easily changed after "
      "incorporation without cost and complexity.")

    sp(6)

    decisions = [
        ("D1", "CRITICAL",
         "Employment contract review \u2014 both founders",
         "Review existing employment contracts for IP assignment clauses, "
         "non-compete provisions, and notification obligations to current employers. "
         "Gate on all incorporation activity.",
         "Before any incorporation"),
        ("D2", "CRITICAL",
         "Voting ratio: 10:1 or 5:1?",
         "10:1 gives stronger founder voting control. 5:1 is less contentious "
         "with some investors and still provides significant control. "
         "Discuss with legal counsel.",
         "Before incorporation"),
        ("D3", "CRITICAL",
         "Option pool size: 10%, 12%, or 15%?",
         "15% is the upper end of market standard and the most Series A-friendly. "
         "10% is the minimum investors will typically accept. "
         "Determines founder dilution at incorporation.",
         "Before incorporation"),
        ("D4", "CRITICAL",
         "Founder vesting: shortened vest or deemed start date?",
         "Shortened two-year vest (simpler) or four-year vest from a deemed "
         "earlier start date (fuller credit for pre-incorporation work). "
         "See Section 5.",
         "Before incorporation"),
        ("D5", "HIGH",
         "Deadlock mechanism: Russian roulette, Texas shoot-out, or CEO casting vote?",
         "The mechanism for resolving fundamental founder disagreements. "
         "Must be in the founders\u2019 agreement from day one.",
         "At incorporation"),
        ("D6", "HIGH",
         "IP assignment: transfer to UK Holdco or licence from Singapore OpCo?",
         "Transfer is cleaner for exit but triggers Singapore stamp duty. "
         "Licence requires transfer pricing documentation. "
         "Legal counsel in both jurisdictions should advise.",
         "At incorporation"),
        ("D7", "HIGH",
         "UK personal tax advice for CEO",
         "Optimal timing of share subscription, S431 election consideration, "
         "and interaction with Singapore-UK Double Tax Agreement. "
         "One hour with a UK personal tax specialist.",
         "Before incorporation"),
        ("D8", "MEDIUM",
         "Singapore tax confirmation for CTO",
         "Confirm capital gains treatment of UK Holdco shares for Singapore resident. "
         "Brief Singapore tax engagement.",
         "Before incorporation"),
        ("D9", "MEDIUM",
         "EIS advance assurance application",
         "Apply to HMRC once UK Holdco is incorporated and "
         "UK business activity is genuinely imminent. "
         "Not at incorporation \u2014 when the CEO is approaching full-time commitment.",
         "Post-incorporation, pre-UK raise"),
    ]

    cwd = 487
    det_data = [[Paragraph(B("Ref"),ST["th"]),
                 Paragraph(B("Priority"),ST["th"]),
                 Paragraph(B("Decision"),ST["th"]),
                 Paragraph(B("Notes"),ST["th"]),
                 Paragraph(B("Timing"),ST["th"])]]
    for ref, pri, title, notes, timing in decisions:
        pri_col = "#C84444" if pri=="CRITICAL" else "#C8A96E" if pri=="HIGH" else "#888888"
        det_data.append([
            Paragraph(ref, ST["tdb"]),
            Paragraph(f'<font color="{pri_col}"><b>{pri}</b></font>', ST["td"]),
            Paragraph(B(title), ST["td"]),
            Paragraph(notes, ST["bodys"]),
            Paragraph(timing, ST["bodys"]),
        ])
    dt = Table(det_data, colWidths=[28, 58, 130, 190, cwd-406])
    dt.setStyle(TableStyle([
        ("FONTNAME",(0,0),(-1,-1),"Poppins-Light"),
        ("FONTSIZE", (0,0),(-1,-1),9),
        ("VALIGN",   (0,0),(-1,-1),"TOP"),
        ("BACKGROUND",(0,0),(-1,0),DARK),
        ("TEXTCOLOR", (0,0),(-1,0),WHITE),
        ("FONTNAME",  (0,0),(-1,0),"Poppins-Bold"),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,LGREY]),
        ("TOPPADDING",   (0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",  (0,0),(-1,-1),6),
        ("GRID",         (0,0),(-1,-1),0.3,RULE),
    ]))
    s.append(dt)

    sp(16)

    # Closing
    s.append(KeepTogether([
        hr(col=GREEN, t=1.2, spb=8, spa=8),
        Paragraph(
            f"{B('Recommended sequence of next steps:')}<br/><br/>"
            f"1. Both founders review employment contracts with lawyers in respective jurisdictions.<br/>"
            f"2. CEO takes one-hour UK personal tax specialist call.<br/>"
            f"3. CTO takes one-hour Singapore tax brief.<br/>"
            f"4. Agree D2\u2013D5 (voting ratio, option pool, vesting, deadlock) between founders.<br/>"
            f"5. Engage UK startup solicitor to incorporate UK Holdco, draft founders\u2019 agreement "
            f"and IP assignment, prepare EIS advance assurance application.<br/>"
            f"6. Engage Singapore corporate lawyer in parallel to prepare Singapore OpCo "
            f"incorporation documents and Singapore-side IP assignment.<br/>"
            f"7. Incorporate both entities in close sequence. Execute all founding documents "
            f"on the same day as incorporation.<br/><br/>"
            f"{I('This document is a discussion briefing only. All decisions require qualified '
               'legal and tax advice before implementation.')}",
            ST["body"]),
        hr(col=RULE, t=0.5, spb=8, spa=4),
        Paragraph(
            "InvestPuppy \u00b7 IP-SHARE-BRIEF-260518-1.0 \u00b7 Internal Discussion Only \u00b7 "
            "Not Legal Advice \u00b7 May 2026",
            ST["small"]),
    ]))

    return s

# ── Document ───────────────────────────────────────────────────────────────────
class _Doc(SimpleDocTemplate):
    def __init__(self, fn):
        super().__init__(fn, pagesize=A4,
                         leftMargin=ML, rightMargin=MR,
                         topMargin=MT, bottomMargin=MB)

def main():
    from pypdf import PdfWriter, PdfReader
    cp = "/tmp/ss_cover.pdf"
    bp = "/tmp/ss_body.pdf"
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
