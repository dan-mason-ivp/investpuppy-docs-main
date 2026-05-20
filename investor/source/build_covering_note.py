"""
ip-investor-covering-note.pdf
InvestPuppy investor pack covering note — 1 page
Build: python3 covering-note/source/build_covering_note.py
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

OUT = '/home/claude/ip-investor-covering-note.pdf'

GREEN  = colors.HexColor('#85D155')
DARK   = colors.HexColor('#0A0A0A')
WHITE  = colors.white
GREY   = colors.HexColor('#888888')
BODY   = colors.HexColor('#1A1A1A')

W, H = A4
ML = 62
MR = 62
FONT_PATH = '/usr/share/fonts/truetype/google-fonts/'

for name in ['Poppins-Light','Poppins-Regular','Poppins-Bold',
             'Poppins-Italic','Poppins-BoldItalic','Poppins-LightItalic']:
    pdfmetrics.registerFont(TTFont(name, f'{FONT_PATH}{name}.ttf'))

def txt(c, x, y, s, font='Poppins-Regular', size=10, color=BODY, align='left'):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == 'center':
        c.drawCentredString(x, y, s)
    elif align == 'right':
        c.drawRightString(x, y, s)
    else:
        c.drawString(x, y, s)

def wrapped(c, x, y, text, font='Poppins-Light', size=10.5, color=BODY,
            max_w=None, line_h=15):
    if max_w is None:
        max_w = W - ML - MR
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line = ''
    for word in words:
        test = f'{line} {word}'.strip()
        if c.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            c.drawString(x, y, line)
            y -= line_h
            line = word
    if line:
        c.drawString(x, y, line)
        y -= line_h
    return y

def rule(c, x, y, w, color=GREEN, t=1.5):
    c.setStrokeColor(color)
    c.setLineWidth(t)
    c.line(x, y, x + w, y)

def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle('InvestPuppy — Investor Pack Covering Note')

    # Dark header band
    c.setFillColor(DARK)
    c.rect(0, H - 58, W, 58, fill=1, stroke=0)

    # Green left accent
    c.setFillColor(GREEN)
    c.rect(0, 0, 5, H, fill=1, stroke=0)

    # Logo
    txt(c, ML, H - 24, 'Invest', font='Poppins-Bold', size=16, color=WHITE)
    iw = c.stringWidth('Invest', 'Poppins-Bold', 16)
    txt(c, ML + iw, H - 24, 'Puppy', font='Poppins-Bold', size=16, color=GREEN)
    txt(c, ML, H - 40, 'Serious when it matters.', font='Poppins-Italic',
        size=8.5, color=GREY)
    txt(c, W - MR, H - 26, 'May 2026', font='Poppins-Regular',
        size=8.5, color=GREY, align='right')
    txt(c, W - MR, H - 40, 'Confidential · Not for distribution',
        font='Poppins-Regular', size=8, color=GREY, align='right')

    rule(c, 0, H - 58, W, color=GREEN, t=1.5)

    y = H - 88

    # Salutation
    txt(c, ML, y, 'Dear Investor,', font='Poppins-Regular', size=11, color=DARK)
    y -= 24

    # Para 1 — why you are receiving this
    y = wrapped(c, ML, y,
        'We are sharing this pack because we think you may be one of a small number '
        'of the right investors for what we are building. If you manage your own '
        'investment activities and recognise the operational problem Vektor is built '
        'to solve, you are exactly the investor we are looking for — not simply '
        'capital, but someone who works in exactly the room Vektor was built to change. '
        'We are looking for three to five partners who have seen what bad '
        'implementations look like, and want to back a team that has spent years '
        'doing the work before asking for the money.',
        font='Poppins-Light', size=10.5, color=BODY, line_h=15)
    y -= 12

    # Para 2 — before we showed you the product
    y = wrapped(c, ML, y,
        'Before we showed you a product, we published ten papers under our own name '
        'about why platforms like this fail. Not to build an audience. To make sure '
        'we understood the failure modes well enough to avoid them. The Unvarnished '
        'series is available at investpuppy.com/unvarnished. We recommend reading '
        'UNV-01 first. It describes the room we built Vektor to replace.',
        font='Poppins-Light', size=10.5, color=BODY, line_h=15)
    y -= 12

    # Para 3 — the product and the credential
    y = wrapped(c, ML, y,
        'Vektor is a systematic listed equity portfolio management platform for '
        'boutique discretionary managers, independent wealth managers, and family '
        'offices. Three years in development. Built by practitioners who have '
        'operated at institutional scale. The CEO holds a production OpenWealth API '
        'credential across Tier 1 custodian institutions in Europe, the Middle East, '
        'and Asia Pacific — a network that took years to build and that opens the '
        'institutional channel before most competitors can get a meeting.',
        font='Poppins-Light', size=10.5, color=BODY, line_h=15)
    y -= 12

    # Para 4 — the raise
    y = wrapped(c, ML, y,
        'We are raising US$2.5M at a pre-money valuation of '
        'US$9M to US$10M. The raise funds eighteen to twenty-four months of '
        'commercial runway — long enough to sign the first Proof Partners, '
        'build the institutional relationships that take time regardless of '
        'capital, and demonstrate the revenue model across all three streams. '
        'Upon close of the raise, both founders commit full-time to InvestPuppy. '
        'We are not raising to build. We have built. We are raising to sell.',
        font='Poppins-Light', size=10.5, color=BODY, line_h=15)
    y -= 12

    # Para 5 — the pack and the ask
    y = wrapped(c, ML, y,
        'This pack contains four additional documents — we suggest reading in order: '
        'the two-page overview first, then the deck, then the full memo, '
        'then the financial model if you would like to go deeper. '
        'A Founder Context document on the founding team\'s background '
        'is available on request at investpuppy.com before the NDA conversation. '
        'Full team biographies are disclosed in full under NDA. '
        'If this is of interest, the right next step is a conversation. '
        'We will not oversell the stage we are at. We will show you what exists, '
        'be direct about what does not yet, and let you decide.',
        font='Poppins-Light', size=10.5, color=BODY, line_h=15)
    y -= 30

    # Pull quote
    rule(c, ML, y + 4, W - ML - MR, color=DARK, t=0.5)
    y -= 10
    txt(c, W / 2, y, '"Honest by design."', font='Poppins-BoldItalic',
        size=12, color=GREEN, align='center')
    y -= 14
    rule(c, ML, y + 4, W - ML - MR, color=DARK, t=0.5)
    y -= 20

    # Signature block
    txt(c, ML, y, 'With respect,', font='Poppins-Light', size=10.5, color=BODY)
    y -= 22
    txt(c, ML, y, 'CEO · Co-founder', font='Poppins-Bold', size=11, color=DARK)
    y -= 15
    txt(c, ML, y, 'InvestPuppy',
        font='Poppins-Light', size=9.5, color=GREY)
    y -= 14
    txt(c, ML, y, 'CEO@investpuppy.com · investpuppy.com',
        font='Poppins-Light', size=9.5, color=GREY)

    # Footer
    rule(c, ML, 46, W - ML - MR, color=colors.HexColor('#DDDDDD'), t=0.5)
    txt(c, ML, 30,
        'Confidential · Not for distribution · InvestPuppy Pte Ltd · May 2026',
        font='Poppins-Light', size=7.5, color=GREY)
    txt(c, W - MR, 30, 'investpuppy.com',
        font='Poppins-Light', size=7.5, color=GREY, align='right')

    c.save()
    print(f'Saved: {OUT}')

if __name__ == '__main__':
    build()
