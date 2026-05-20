"""
InvestPuppy Investor One-Pager  v4
ip-investor-onepager.pdf

Fixes from Dan + panel:
1. All text strictly within its bounds — no overflows anywhere
2. Dark section: "Honest by design." + three short declarative sentences in the same voice
   (panel preferred: "The platform runs. It has not yet executed in a live account.
    That is what this round is for.")
3. Layout rebuilt with explicit Y boundaries per column
4. Beat labels at 7pt, thin rule above each
5. Logo at 12mm height
"""

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

HERE     = Path(__file__).resolve().parent
REPO     = HERE.parent.parent
FONTS    = REPO / "_shared" / "fonts"
LOGOS    = REPO / "_shared" / "logos"
OUT_DIR  = HERE.parent / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT      = OUT_DIR / "ip-investor-onepager.pdf"
LOGO_L   = LOGOS / "ip_logo_light_bg.png"
IP_RATIO = 911 / 746   # 1.221

for wt, fn in [
    ("Poppins-Light",  "Poppins-Light.ttf"),
    ("Poppins",        "Poppins-Regular.ttf"),
    ("Poppins-Medium", "Poppins-Medium.ttf"),
    ("Poppins-Bold",   "Poppins-Bold.ttf"),
    ("Poppins-Italic", "Poppins-Italic.ttf"),
]:
    pdfmetrics.registerFont(TTFont(wt, str(FONTS / fn)))

WHITE  = (1,     1,     1)
GREEN  = (0.522, 0.820, 0.333)
DARK   = (0.102, 0.102, 0.102)
MID    = (0.36,  0.36,  0.36)
DARKBG = (0.059, 0.059, 0.078)
BORDER = (0.86,  0.86,  0.86)
BGST   = (0.955, 0.955, 0.955)

W, H = A4   # 595.27 × 841.89 pt

ML    = 14 * mm
MR    = W - 14 * mm
TW    = MR - ML
GAP   = 6 * mm
CW    = (TW - GAP) / 2       # column width
COL2  = ML + CW + GAP        # x-start right column

DARK_H  = 68 * mm            # dark section — content area fills naturally below
CONT_Y  = H - DARK_H - 6*mm  # top of content area
FOOT_Y  = 18 * mm
CONT_B  = FOOT_Y + 8*mm

CALLOUT_H = 27 * mm
L_BOT = CONT_B
R_BOT = CONT_B + CALLOUT_H + 4*mm


# ── Helpers ────────────────────────────────────────────────────────────────────

def rgbf(c, col): c.setFillColorRGB(*col)
def rgbs(c, col): c.setStrokeColorRGB(*col)

def hrule(c, x1, y, x2, col=BORDER, t=0.4):
    rgbs(c, col)
    c.setLineWidth(t)
    c.line(x1, y, x2, y)

def beat_label(c, text, x, y):
    """7pt bold green label with thin green rule above."""
    hrule(c, x, y + 3.5*mm, x + CW, GREEN, 0.6)
    c.setFont("Poppins-Bold", 7)
    rgbf(c, GREEN)
    c.drawString(x, y, text.upper())

def wrap(c, text, x, y, w, size=8.6, col=MID,
         font="Poppins", lead=13.5, bot=0):
    """Wraps text; skips lines below bot. Returns new y."""
    words = text.split()
    line  = ""
    c.setFont(font, size)
    rgbf(c, col)
    for word in words:
        test = (line + " " + word).strip()
        if stringWidth(test, font, size) <= w:
            line = test
        else:
            if y >= bot:
                c.drawString(x, y, line)
            y -= lead
            line = word
    if line and y >= bot:
        c.drawString(x, y, line)
        y -= lead
    return y

def bul(c, text, x, y, w, size=8.6, col=MID, lead=13.5, bot=0):
    """Bullet item. Returns new y."""
    c.setFont("Poppins-Medium", size)
    rgbf(c, GREEN)
    if y >= bot:
        c.drawString(x, y, "·")
    return wrap(c, text, x + 7.5, y, w - 7.5,
                size=size, col=col, lead=lead, bot=bot)


# ══════════════════════════════════════════════════════════════════════════════
def build():
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("InvestPuppy — Investor Overview")
    c.setAuthor("InvestPuppy")

    # ── WHITE BACKGROUND ──────────────────────────────────────────────────────
    rgbf(c, WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── DARK SECTION ──────────────────────────────────────────────────────────
    rgbf(c, DARKBG)
    c.rect(0, H - DARK_H, W, DARK_H, fill=1, stroke=0)

    # Thin green top rule
    rgbf(c, GREEN)
    c.rect(0, H - 2*mm, W, 2*mm, fill=1, stroke=0)

    # Logo — 12mm height, top-left
    LH = 12*mm
    LW = LH * IP_RATIO
    c.drawImage(str(LOGO_L), ML, H - LH - 11*mm,
                width=LW, height=LH,
                preserveAspectRatio=True, anchor="sw", mask="auto")

    # Seed badge — top right
    BW, BH = 48*mm, 8*mm
    BX = MR - BW
    BY = H - BH - 11*mm
    c.setFillColorRGB(0.11, 0.11, 0.15)
    c.roundRect(BX, BY, BW, BH, 1.5*mm, fill=1, stroke=0)
    c.setFont("Poppins-Bold", 7.5)
    rgbf(c, GREEN)
    c.drawCentredString(BX + BW/2, BY + 2.5*mm, "SEED ROUND  ·  S$1M – S$2M")

    # "Honest by design." — HERO
    c.setFont("Poppins-Bold", 33)
    rgbf(c, WHITE)
    c.drawString(ML, H - 38*mm, "Honest by design.")

    c.setFont("Poppins", 10.5)
    rgbf(c, GREEN)
    c.drawString(ML, H - 51*mm, "The platform runs.")
    c.setFont("Poppins-Italic", 10.5)
    rgbf(c, (0.72, 0.72, 0.75))
    c.drawString(ML + 36.5*mm, H - 51*mm,
        "It has not yet executed in a live account. That is what this round is for.")

    # Company line at base of dark section
    c.setFont("Poppins", 7.5)
    rgbf(c, (0.4, 0.4, 0.46))
    c.drawString(ML, H - DARK_H + 6*mm,
        "InvestPuppy Pte Ltd  ·  investpuppy.com  ·  contact@investpuppy.com")

    # ── CONTENT AREA ──────────────────────────────────────────────────────────
    y_l = CONT_Y   # left column y tracker
    y_r = CONT_Y   # right column y tracker

    # ── BEAT 1: THE PREMISE (left) ────────────────────────────────────────────
    beat_label(c, "The Premise", ML, y_l)
    y_l -= 11
    y_l = wrap(c,
        "The boutique wealth manager is systematically priced out of every "
        "tool that exists. Bloomberg Terminal: ~$32,000/seat/year (2026 verified). "
        "Bloomberg PORT adds S$8K–S$25K/seat on top. "
        "Bespoke quant builds: S$500K–S$2M and 12–24 months. "
        "Spreadsheets fill the gap.",
        ML, y_l, CW, lead=12.8, bot=L_BOT)
    y_l -= 3
    y_l = wrap(c,
        "2,000+ single family offices in Singapore (MAS, 2024). 500+ independent wealth managers. "
        "Every one managing client assets without the tools their clients "
        "would expect them to have. The gap is structural. "
        "It will not close itself.",
        ML, y_l, CW, lead=12.8, bot=L_BOT)

    y_l -= 11
    # ── BEAT 2: THE RESPONSE (left) ───────────────────────────────────────────
    beat_label(c, "The Response — Vektor", ML, y_l)
    y_l -= 11
    y_l = bul(c,
        "10,000 portfolio configurations per strategy. Systematic construction, "
        "not guesswork. Audit-ready output. 99.94% availability target.",
        ML, y_l, CW, bot=L_BOT)
    y_l -= 2
    y_l = bul(c,
        "Data-layer independent. Runs on IBKR market data as standard. "
        "Does not require Bloomberg feeds. "
        "Bloomberg Terminal users keep their Terminal — Vektor adds the construction layer.",
        ML, y_l, CW, bot=L_BOT)
    y_l -= 2
    y_l = bul(c,
        "Three entry motions: add systematic construction for 56% of one Terminal seat cost "
        "(capability provision); replace Bloomberg PORT's construction function, keep risk "
        "reporting (PORT replacement); or end in-house data-feed-funded quant development "
        "(development termination).",
        ML, y_l, CW, bot=L_BOT)

    y_l -= 11
    # ── BEAT 3: THE POSITION (left) ───────────────────────────────────────────
    beat_label(c, "The Position", ML, y_l)
    y_l -= 11
    y_l = bul(c,
        "Singapore now: 2,000+ single family offices (MAS, 2024), 500+ wealth managers, "
        "MAS regulatory clarity. Distribution-ready today.",
        ML, y_l, CW, bot=L_BOT)
    y_l -= 2
    y_l = bul(c,
        "Southeast Asia at 12–24 months. UK and established markets to follow. "
        "No structural platform change required.",
        ML, y_l, CW, bot=L_BOT)

    # Closing line — left column, anchored at same level as callout top
    ANCHOR_Y = FOOT_Y + 8*mm + CALLOUT_H + 10*mm   # matches callout top
    c.setFont("Poppins-Bold", 10.5)
    rgbf(c, DARK)
    c.drawString(ML, ANCHOR_Y, "The case is made.")
    c.setFont("Poppins-Italic", 10.5)
    rgbf(c, MID)
    c.drawString(ML, ANCHOR_Y - 14, "The conversation is open.")

    # ── BEAT 4: THE TEAM (right) ──────────────────────────────────────────────
    beat_label(c, "The Team", COL2, y_r)
    y_r -= 11

    for role, name, bio in [
        ("CEO", "[FOUNDER A — NAME]",
         "Senior leadership in fintech and financial software. "
         "B2B sales into wealth managers, RIAs, and institutional clients. "
         "A market we have worked in, not just analysed."),
        ("CTO", "[FOUNDER B — NAME]",
         "[To be completed. Platform architecture and quantitative systems.]"),
    ]:
        if y_r < R_BOT + 20*mm:
            break
        # Role badge
        rgbf(c, GREEN)
        c.roundRect(COL2, y_r - 1.5*mm, 17*mm, 5.5*mm, 1*mm, fill=1, stroke=0)
        c.setFont("Poppins-Bold", 6.5)
        rgbf(c, DARKBG)
        c.drawCentredString(COL2 + 8.5*mm, y_r + 0.5*mm, role)
        # Name
        c.setFont("Poppins-Bold", 8.5)
        rgbf(c, DARK)
        c.drawString(COL2 + 19*mm, y_r + 0.5*mm, name)
        y_r -= 9
        # Bio — capped to 2 lines to prevent overflow
        y_r = wrap(c, bio, COL2, y_r, CW,
                   size=7.8, col=MID, lead=11, bot=R_BOT)
        y_r -= 5

    y_r -= 6
    # ── BEAT 5: THE ASK (right) ───────────────────────────────────────────────
    beat_label(c, "The Ask", COL2, y_r)
    y_r -= 11

    c.setFont("Poppins-Bold", 13)
    rgbf(c, DARK)
    c.drawString(COL2, y_r, "S$1,000,000 – S$2,000,000")
    y_r -= 11
    c.setFont("Poppins-Italic", 8)
    rgbf(c, MID)
    c.drawString(COL2, y_r, "Seed round · Singapore-led close")
    y_r -= 13

    # Pricing tiers - two column, no overlap
    c.setFont("Poppins-Bold", 7)
    rgbf(c, GREEN)
    c.drawString(COL2, y_r, "INDICATIVE PRICING — AUM-TIERED SUBSCRIPTION")
    y_r -= 9

    for tier, price in [
        ("Entry  ≤S$75M AUM",        "S$24,000/yr"),
        ("Growth  S$75M–S$250M",     "S$48,000/yr"),
        ("Institutional  S$250–750M","S$108,000/yr"),
        ("Enterprise  S$750M+",      "S$168,000+/yr"),
        ("FM lock — years 1–3",       "S$18,000/yr"),
        ("FM post lock — 1 tier below (floor: Entry)", "S$24,000/yr+"),
    ]:
        if y_r < R_BOT + 4*mm: break
        c.setFont("Poppins", 8)
        rgbf(c, DARK if "Founding" not in tier else MID)
        c.drawString(COL2, y_r, tier)
        c.setFont("Poppins-Bold", 8)
        rgbf(c, GREEN)
        c.drawRightString(COL2 + CW, y_r, price)
        y_r -= 11

    y_r -= 3
    # Founding Mandate + revenue target
    if y_r > R_BOT + 16*mm:
        c.setFont("Poppins-Bold", 7.5)
        rgbf(c, DARK)
        c.drawString(COL2, y_r, "Founding Mandate Programme:")
        y_r -= 11
        y_r = wrap(c,
            "First cohort clients receive preferential commercial terms locked "
            "for the duration, co-design access, and direct founding team engagement.",
            COL2, y_r, CW, size=7.8, lead=11.2, bot=R_BOT)
        y_r -= 6

    if y_r > R_BOT + 4*mm:
        c.setFont("Poppins-Bold", 8.2)
        rgbf(c, DARK)
        c.drawString(COL2, y_r, "First revenue: 9–13 months from close.")
        y_r -= 14

    # ── CONCLUSION CALLOUT — fixed at bottom right, same level as left closing ──
    cal_top = FOOT_Y + 8*mm + CALLOUT_H
    rgbf(c, DARKBG)
    c.roundRect(COL2, cal_top - CALLOUT_H, CW, CALLOUT_H,
                2*mm, fill=1, stroke=0)
    rgbf(c, GREEN)
    c.rect(COL2, cal_top - 1.8*mm, CW, 1.8*mm, fill=1, stroke=0)

    c.setFont("Poppins-Bold", 9.5)
    rgbf(c, WHITE)
    c.drawString(COL2 + 5*mm, cal_top - 9*mm, "Honest by design.")
    c.setFont("Poppins", 7.5)
    rgbf(c, (0.6, 0.6, 0.65))
    c.drawString(COL2 + 5*mm, cal_top - 16*mm, "In our platform. In our documents.")
    c.drawString(COL2 + 5*mm, cal_top - 23*mm, "In how we work with investors.")

    # ── FOOTER ────────────────────────────────────────────────────────────────
    hrule(c, ML, FOOT_Y, MR, col=BORDER, t=0.4)
    c.setFont("Poppins", 6.8)
    rgbf(c, MID)
    c.drawString(ML, FOOT_Y - 5.5*mm,
        "InvestPuppy  ·  investpuppy.com  ·  contact@investpuppy.com")
    c.setFont("Poppins", 6.5)
    rgbf(c, BORDER)
    c.drawRightString(MR, FOOT_Y - 5.5*mm, "Confidential. Not an offer of securities.")

    c.save()
    print(f"Built: {OUT}")


if __name__ == "__main__":
    build()
