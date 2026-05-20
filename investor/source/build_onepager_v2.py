"""
ip-investor-onepager.pdf  — true single page, v2 with corrected spacing
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

OUT   = '/home/claude/ip-investor-onepager.pdf'
GREEN = colors.HexColor('#85D155')
DARK  = colors.HexColor('#0A0A0A')
BODY  = colors.HexColor('#1A1A1A')
GREY  = colors.HexColor('#888888')
WHITE = colors.white
RULE  = colors.HexColor('#E0E0E0')

FP = '/usr/share/fonts/truetype/google-fonts/'
for n in ['Poppins-Light','Poppins-Regular','Poppins-Bold',
          'Poppins-Italic','Poppins-BoldItalic']:
    pdfmetrics.registerFont(TTFont(n, FP+n+'.ttf'))

W, H  = A4
LX    = 44;  LW = 240
RX    = 314; RW = 238
HDR   = 52;  FTR = 38

def wrap(c, x, y, text, font='Poppins-Light', size=9,
         color=BODY, max_w=None, lh=13):
    if max_w is None: max_w = LW
    c.setFont(font, size); c.setFillColor(color)
    words = text.split(); line = ''
    for word in words:
        test = (line+' '+word).strip()
        if c.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            c.drawString(x, y, line); y -= lh; line = word
    if line: c.drawString(x, y, line); y -= lh
    return y

def lbl(c, x, y, text, color=GREEN):
    """Section label — draws text, returns y below it with proper gap."""
    c.setFont('Poppins-Bold', 7.5); c.setFillColor(color)
    c.drawString(x, y, text.upper())
    return y - 11   # 7.5pt text height + 3.5pt gap

def bul(c, x, y, text, size=9, lh=13, max_w=None):
    if max_w is None: max_w = LW - 10
    pfx = '\u00b7  '
    pw  = c.stringWidth(pfx, 'Poppins-Light', size)
    c.setFont('Poppins-Light', size); c.setFillColor(BODY)
    words = text.split(); line = ''; first = True
    for word in words:
        test = (line+' '+word).strip()
        if c.stringWidth(test,'Poppins-Light',size) <= max_w - pw:
            line = test
        else:
            c.drawString(x, y, (pfx if first else '   ')+line)
            y -= lh; line = word; first = False
    if line:
        c.drawString(x, y, (pfx if first else '   ')+line); y -= lh
    return y

def hrule(c, x, y, w, col=RULE, t=0.5):
    c.setStrokeColor(col); c.setLineWidth(t)
    c.line(x, y, x+w, y)

def kv_row(c, x, y, key, val, kw=RW):
    c.setFont('Poppins-Bold', 9); c.setFillColor(DARK)
    c.drawString(x, y, key+':')
    y -= 12
    y = wrap(c, x+8, y, val, size=9, max_w=kw-8, lh=12)
    return y - 3

def build():
    cv = canvas.Canvas(OUT, pagesize=A4)
    cv.setTitle('InvestPuppy — Investor Overview')

    # Header
    cv.setFillColor(DARK); cv.rect(0, H-HDR, W, HDR, fill=1, stroke=0)
    cv.setFillColor(GREEN); cv.rect(0, 0, 4, H, fill=1, stroke=0)
    cv.setFont('Poppins-Bold',15); cv.setFillColor(WHITE)
    cv.drawString(LX, H-22, 'Invest')
    iw = cv.stringWidth('Invest','Poppins-Bold',15)
    cv.setFillColor(GREEN); cv.drawString(LX+iw, H-22, 'Puppy')
    cv.setFont('Poppins-Italic',8); cv.setFillColor(GREY)
    cv.drawString(LX, H-36, 'Serious when it matters.')
    cv.setFont('Poppins-Regular',8); cv.setFillColor(GREY)
    cv.drawRightString(W-LX, H-22, 'Investor Overview')
    cv.drawRightString(W-LX, H-34, 'Confidential \u00b7 May 2026')
    hrule(cv, 0, H-HDR, W, col=GREEN, t=1.5)

    # Column divider
    cv.setStrokeColor(RULE); cv.setLineWidth(0.4)
    cv.line(RX-12, H-HDR-6, RX-12, FTR+8)

    # ── LEFT COLUMN ───────────────────────────────────────────────────────────
    y = H - HDR - 18

    # Hook
    cv.setFont('Poppins-Bold',13); cv.setFillColor(DARK)
    cv.drawString(LX, y, 'Systematic portfolio management.')
    y -= 17
    cv.setFont('Poppins-Bold',13); cv.setFillColor(GREEN)
    cv.drawString(LX, y, 'Built for practitioners who')
    y -= 17; cv.drawString(LX, y, 'know what good looks like.')
    y -= 13
    y = wrap(cv, LX, y, 'Vektor is a systematic listed equity portfolio management '
        'platform for boutique DPMs, independent wealth managers, and family offices. '
        'One product. Three delivery models. Honest by design.',
        size=9.5, lh=14, max_w=LW)
    y -= 10

    # Problem
    hrule(cv, LX, y+3, LW)
    y = lbl(cv, LX, y, 'The Problem')
    y = bul(cv, LX, y, 'Bloomberg Terminal ~US$32,000/seat/year. Built for '
        'sell-side research, not systematic portfolio construction.', lh=13)
    y = bul(cv, LX, y, 'Signal application, rebalancing, and audit trail '
        'generation are manual, error-prone, and compliance-fragile.', lh=13)
    y = bul(cv, LX, y, 'Implementation failures are endemic. The same projects '
        'fail for the same reasons. Nobody publishes it. We did.', lh=13)
    y -= 9

    # What Vektor does — metrics
    hrule(cv, LX, y+3, LW)
    y = lbl(cv, LX, y, 'What Vektor Does')
    y -= 6  # clearance for 18pt metric ascenders
    for num, desc, ns in [
        ('10,000', 'portfolio configurations per strategy', 18),
        ('99.94%', 'capital allocation efficiency', 18),
        ('Tier 1', 'OpenWealth API credential \u2014 CEO, live EMEA + APAC', 13),
    ]:
        cv.setFont('Poppins-Bold', ns); cv.setFillColor(GREEN)
        cv.drawString(LX, y, num)
        nw = cv.stringWidth(num, 'Poppins-Bold', ns)
        cv.setFont('Poppins-Light', 8.5); cv.setFillColor(GREY)
        cv.drawString(LX+nw+5, y+2, desc)
        y -= ns * 1.1 + 5
    y -= 2
    y = wrap(cv, LX, y, 'Full audit trail on every decision. Multi-custodian '
        'mandate management. IBKR integrated. RBAC maker/checker.',
        size=9, lh=13, max_w=LW)
    y -= 9

    # Three delivery models
    hrule(cv, LX, y+3, LW)
    y = lbl(cv, LX, y, 'Three Delivery Models')
    y -= 3
    for name, desc in [
        ('Vektor : Boutique', 'Direct AUM-tiered subscription. From US$18,000/yr.'),
        ('Vektor : House',    'Institutional via Alloy Partners. Stage 1 open now.'),
        ('Vektor : Wrapped',  'Licensed via custodian banks for EAM clients.'),
    ]:
        cv.setFont('Poppins-Bold', 9); cv.setFillColor(GREEN)
        cv.drawString(LX, y, name)
        y -= 12
        cv.setFont('Poppins-Light', 9); cv.setFillColor(GREY)
        cv.drawString(LX+8, y, '\u2014 '+desc)
        y -= 13
    y -= 8

    # Honest by design box
    bh = 46
    cv.setFillColor(DARK)
    cv.rect(LX, y-bh+10, LW, bh, fill=1, stroke=0)
    cv.setFont('Poppins-BoldItalic',11); cv.setFillColor(GREEN)
    cv.drawCentredString(LX+LW/2, y-4, '"Honest by design."')
    cv.setFont('Poppins-Light',8); cv.setFillColor(GREY)
    cv.drawCentredString(LX+LW/2, y-18, '10 published papers on why implementations fail.')
    cv.setFont('Poppins-Regular',8.5); cv.setFillColor(GREEN)
    cv.drawCentredString(LX+LW/2, y-32, 'investpuppy.com/unvarnished')

    # ── RIGHT COLUMN ──────────────────────────────────────────────────────────
    y = H - HDR - 18

    # The Raise
    y = lbl(cv, RX, y, 'The Raise')
    for key, val in [
        ('Target',       'US$2M \u2013 US$2.5M'),
        ('Pre-money',    'US$9M \u2013 US$10M'),
        ('Structure',    'Quiet raise \u00b7 3\u20135 investors \u00b7 boutique wealth '
                         'practitioners or fintech-experienced angels'),
        ('Compatibility','Stealth-compatible \u00b7 both founders commit full-time on close'),
        ('Runway',       '18\u201324 months to Series A milestone'),
    ]:
        y = kv_row(cv, RX, y, key, val)
    y -= 8

    # Market
    hrule(cv, RX, y+3, RW)
    y = lbl(cv, RX, y, 'Market')
    for m in [
        'Singapore \u2014 2,000+ SFOs (MAS, 2024). Primary market.',
        'Switzerland \u2014 FinIA compliance. OpenWealth established. Near-term.',
        'UK \u2014 FCA regulatory opinion underway.',
        'Rest of Europe, Channel Islands, SE Asia, DIFC/UAE \u2014 pipeline.',
    ]:
        y = bul(cv, RX, y, m, size=9, lh=12, max_w=RW-10)
    y -= 3
    y = wrap(cv, RX, y, '~US$15M ARR at 10% penetration (SG, CH, UK only \u2014 '
        'pipeline markets excluded). Institutional roadmap extends beyond Vektor '
        '\u2014 disclosed under NDA.',
        size=8.5, lh=12, max_w=RW, color=GREY)
    y -= 9

    # Competitive position
    hrule(cv, RX, y+3, RW)
    y = lbl(cv, RX, y, 'Competitive Position')
    cols_x = [RX, RX+116, RX+182]
    cv.setFont('Poppins-Bold',7.5); cv.setFillColor(GREY)
    for x_, hdr in zip(cols_x, ['', 'Annual cost', 'What you get']):
        cv.drawString(x_, y, hdr)
    y -= 11
    for name, cost, what in [
        ('Vektor : Boutique Entry','US$18,000/yr','Full platform'),
        ('Bloomberg Terminal',     '~US$32,000/yr','Market data only'),
        ('Bloomberg PORT',         '+US$6\u201325K/yr','Analytics only, no execution'),
    ]:
        is_v = 'Vektor' in name
        cv.setFont('Poppins-Bold' if is_v else 'Poppins-Light', 9)
        cv.setFillColor(GREEN if is_v else GREY)
        cv.drawString(cols_x[0], y, name)
        cv.setFont('Poppins-Regular' if is_v else 'Poppins-Light', 9)
        cv.setFillColor(GREEN if is_v else GREY)
        cv.drawString(cols_x[1], y, cost)
        cv.setFont('Poppins-Light',9); cv.setFillColor(GREY)
        cv.drawString(cols_x[2], y, what)
        y -= 12
    y -= 8

    # Team
    hrule(cv, RX, y+3, RW)
    y = lbl(cv, RX, y, 'Team')
    y = wrap(cv, RX, y, 'CEO: three decades inside institutional portfolio management '
        'technology \u2014 vendor, solution architect, programme management for '
        'Global Tier 1 banks. Production OpenWealth credentials EMEA + APAC.',
        size=9, lh=12, max_w=RW)
    y -= 4
    y = wrap(cv, RX, y, 'CTO: two decades of institutional financial technology '
        'architecture \u2014 cloud-native core banking, digital challenger '
        'bank launches. Platform built to compliance standards from first principles.',
        size=9, lh=12, max_w=RW)
    y -= 4
    cv.setFont('Poppins-Italic',8.5); cv.setFillColor(GREY)
    cv.drawString(RX, y, 'Founding partnership: approximately a decade.')
    y -= 12
    cv.setFont('Poppins-Italic',8.5); cv.setFillColor(GREY)
    cv.drawString(RX, y, 'Full biographies: Founder Context available on request.')
    y -= 14

    # CTA
    hrule(cv, RX, y+3, RW, col=GREEN, t=1)
    y -= 10
    cv.setFont('Poppins-Bold',9); cv.setFillColor(GREEN)
    cv.drawCentredString(RX+RW/2, y, 'To begin a conversation:')
    y -= 13
    cv.setFont('Poppins-Regular',9); cv.setFillColor(DARK)
    cv.drawCentredString(RX+RW/2, y, 'CEO@investpuppy.com \u00b7 investpuppy.com')

    # Footer
    hrule(cv, LX, FTR+16, W-2*LX)
    cv.setFont('Poppins-Light',7.5); cv.setFillColor(GREY)
    cv.drawString(LX, FTR+4,
        'InvestPuppy \u00b7 investpuppy.com \u00b7 CEO@investpuppy.com')
    cv.drawRightString(W-LX, FTR+4,
        'Confidential \u00b7 Not for distribution \u00b7 May 2026')

    cv.save()
    print(f'Saved: {OUT}')

if __name__ == '__main__':
    build()
