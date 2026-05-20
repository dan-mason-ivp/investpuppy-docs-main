"""IP-UNV-05: The change request trap"""
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from unvarnished_builder import *

REF   = "IP-UNV-05  \u00b7  2026"
TITLE = "The change request trap"
PHOTO = "Metal mesh office in-tray, three tiers, overflowing with papers and folders."
NUM   = 5
OUT   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "output", "ip-unv-05-change-request-trap.pdf")
IMG   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "..", "_shared", "cover-photos", "unv05_cover_photo.jpg")
S     = get_styles()

def preface_story():
    S = get_styles()
    items = [Spacer(1, 6)]
    items.append(SeriesBox("About InvestPuppy",
        [Paragraph(ATTRIBUTION, S['attribution'])], label_size=8))
    items.append(Spacer(1, 10))
    preface_items = [
        Paragraph("Every experienced practitioner thinks it. Almost nobody publishes it: "
            "<i>there has to be a better way.</i>", S['sb_hook']),
        Paragraph("We thought it long enough that we went and built one.", S['sb_light']),
        Spacer(1, 8),
        Paragraph("Before that, we spent decades in the rooms.", S['sb_light']),
        Paragraph("The same project was failing for the third time. "
            "The project plan had been signed off before anyone had understood "
            "the first requirement.", S['sb_bold']),
        Paragraph("The relationship was too warm for anyone to say so.", S['sb_light']),
        Spacer(1, 8),
        Paragraph("It isn\u2019t incompetence.", S['sb_bold']),
        Paragraph("It\u2019s the incentive structure doing its job perfectly.", S['sb_bold']),
        Paragraph("Nobody planned it this way. Nobody needed to.", S['sb_light']),
        Spacer(1, 4),
        Paragraph("We got frustrated enough to write it down. "
            "Then frustrated enough to build something.", S['sb_bold']),
        Paragraph("These papers are the writing-it-down part.", S['sb_bold']),
        Paragraph("The something we built is a separate conversation.", S['sb_italic']),
    ]
    items.append(SeriesBox("What this series is", preface_items, label_size=9))
    return items

def content_story():
    items = [Spacer(1, 8)]

    items.append(Paragraph(
        "The change request was not unexpected.",
        S['spaced_statement']))
    items.append(Paragraph(
        "It was inevitable from the day the specification was signed.",
        S['spaced_statement']))
    items.append(HRFlowable(width="100%", thickness=0.5,
                             color=RULE_GREY, spaceAfter=12, spaceBefore=0))

    items.append(NoteBox([Paragraph(
        "A change request is a formal acknowledgement that the original specification "
        "was wrong. It is also a commercial mechanism \u2014 a way for the vendor to "
        "charge for the work that should have been included in the original scope, "
        "and a way for the client to request the thing they needed but did not know "
        "how to ask for. It is not a sign that something has gone unexpectedly wrong. "
        "It is a sign that the project was specified before it was understood.",
        S['note_text'])]))
    items.append(Spacer(1, 14))

    items.append(SectionHeader("1. The Anatomy of a Change Request"))
    items.append(GreenRule(sa=6))
    for para in [
        "Every change request has a before and an after. Before: a specification that "
        "described what the system would do. After: a discovery that the specification "
        "was incomplete, incorrect, or based on an assumption that turned out to be false.",
        "The commercial context of this discovery matters. The power dynamic at change "
        "request stage is not the same as the power dynamic at procurement stage. When "
        "the specification was being written, the client had choices. They could "
        "negotiate scope, challenge assumptions, request more discovery time. By the "
        "time the first substantive change request arrives, the client has invested in "
        "the relationship, committed to a go-live date, and is in no position to walk "
        "away. The vendor knows this. The change request is priced accordingly \u2014 "
        "frequently at a premium to the original day rate, because the client\u2019s "
        "ability to renegotiate is now effectively zero.",
        "This is not a surprise event. It was a predictable commercial outcome from "
        "the moment the specification was signed without adequate discovery. The "
        "question is not whether change requests will arrive. It is when, and at "
        "what price.",
    ]:
        items.append(Paragraph(para, S['body_j']))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("2. The Volume Problem"))
    items.append(GreenRule(sa=6))
    for para in [
        "A single change request is a correction. Five change requests is a pattern. "
        "Ten change requests means the specification was not fit for purpose.",
        "Most implementations with significant CR volumes reach that volume not through "
        "a series of genuinely unforeseeable events, but through the systematic "
        "underspecification of a small number of critical areas. Integration points "
        "are underspecified because they require coordination between the vendor and "
        "third-party systems that the vendor does not control. Exception handling is "
        "underspecified because it requires the client to document the things they "
        "handle manually, which nobody asked them to document before the specification "
        "was signed. Reporting requirements are underspecified because \u2018standard "
        "reports\u2019 means different things to different stakeholders, and the "
        "stakeholders who care most about reporting were not in the specification workshop.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    items.append(NoteBox([Paragraph(
        "None of these are surprises in retrospect. They are the same underspecified "
        "areas in every implementation. The vendor has seen them before. The consulting "
        "firm has seen them before. The client has not. The asymmetry of experience is "
        "one reason these areas remain underspecified: the party with the most incentive "
        "to specify them thoroughly is the party least likely to flag the gap before "
        "the contract is signed.", S['note_text'])]))
    items.append(Spacer(1, 12))

    items.append(SectionHeader("3. The Contract Behind the Change Request"))
    items.append(GreenRule(sa=6))
    for para in [
        "The change request mechanism does not operate in isolation. It is supported "
        "by the contract. A well-drafted vendor contract places the risk of "
        "specification incompleteness on the client: the vendor delivers what was "
        "specified, and if what was specified is not what was needed, that is a scope "
        "change. Scope changes are change requests.",
        "What many clients do not examine carefully enough at contract stage is the "
        "definition of \u2018specification\u2019. In most vendor contracts, this definition "
        "is limited to the signed document. Verbal representations made during the "
        "sales process, demonstrations of functionality, and commitments made in "
        "pre-contract workshops are explicitly excluded. The gap between what was "
        "shown and what was signed is a gap that belongs entirely to the client.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    bq_body = [
        Paragraph("The change request is not a failure of process. It is the process. "
            "The original specification was always going to be incomplete. The vendor "
            "knew this. The consultant knew this. The client suspected it but could "
            "not prove it.", S['bq_body']),
        Paragraph("The CR mechanism is the commercial structure that converts that "
            "incompleteness into revenue. It does not need to be dishonest to "
            "be problematic.", S['bq_body']),
    ]
    bq_close = Paragraph("It only needs to exist.", S['bq_close'])
    items.append(ElevatedBlockquote(bq_body, bq_close))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("4. Reducing CR Exposure"))
    items.append(GreenRule(sa=6))
    items.append(Paragraph(
        "CR exposure is not eliminated by a tighter contract. A tighter contract "
        "produces a more defensive vendor, a more adversarial relationship, and the "
        "same change requests priced differently. CR exposure is reduced by completing "
        "the discovery before the specification is written, the specification before "
        "the contract is signed, and the contract before the configuration begins.",
        S['body_j']))
    items.append(Paragraph(
        "Three mechanisms that reduce CR volume in practice:", S['body']))
    for text in [
        "<b>One.</b> Specification sign-off by the people who will use the system, "
        "not only the people who commissioned it \u2014 including explicit sign-off on "
        "the handling of the twenty most common workflow exceptions.",
        "<b>Two.</b> Integration mapping completed and agreed before the contract is "
        "signed, with third-party system owners included in that process, not added later.",
        "<b>Three.</b> A contract definition of \u2018specification\u2019 that explicitly "
        "includes demonstrated functionality, pre-contract commitments, and any "
        "functionality referenced in the sales process \u2014 and a vendor willing to sign it.",
    ]:
        items.append(Paragraph(text, S['body_j']))

    items.append(Spacer(1, 14))
    items.append(HRFlowable(width="100%", thickness=0.75, color=RULE_GREY,
                             spaceAfter=10))
    items.append(Paragraph(
        "Every change request is a discovery session that happened too late.",
        S['isolated_statement']))
    return items

if __name__ == '__main__':
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build_document(OUT, TITLE, REF, PHOTO, NUM,
                   preface_story(), content_story(), photo_path=IMG)
