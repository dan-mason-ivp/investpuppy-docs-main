"""IP-UNV-01: Why financial software implementations fail — v4"""
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from unvarnished_builder import *

REF   = "IP-UNV-01  ·  May 2026"
TITLE = "Why financial software implementations fail"
PHOTO = ("Thick printed specification document, dog-eared, coffee ring stain "
         "over text, APPROVED stamp with date and initials visible.")
NUM   = 1
OUT   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "output", "ip-unv-01-why-implementations-fail.pdf")
IMG   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "..", "_shared", "cover-photos", "unv01_cover_photo.jpg")

S = get_styles()

def preface_story():
    S = get_styles()
    items = [Spacer(1, 6)]

    # Box 1 — Attribution
    items.append(SeriesBox(
        "About InvestPuppy",
        [Paragraph(ATTRIBUTION, S['attribution'])],
        label_size=8))
    items.append(Spacer(1, 10))

    # Box 2 — Series preface, mixed-weight typographic structure
    preface_items = [

        # Unit 1: The Hook
        Paragraph(
            "Every experienced practitioner thinks it. Almost nobody publishes it: "
            "<i>there has to be a better way.</i>",
            S['sb_hook']),
        Paragraph(
            "We thought it long enough that we went and built one.",
            S['sb_light']),

        Spacer(1, 8),

        # Unit 2: The Rooms
        Paragraph("Before that, we spent decades in the rooms.", S['sb_light']),
        Paragraph(
            "The same project was failing for the third time. "
            "The project plan had been signed off before anyone had understood "
            "the first requirement.",
            S['sb_bold']),
        Paragraph("The relationship was too warm for anyone to say so.", S['sb_light']),

        Spacer(1, 8),

        # Unit 3: Thesis and Purpose
        Paragraph("It isn\u2019t incompetence.", S['sb_bold']),
        Paragraph(
            "It\u2019s the incentive structure doing its job perfectly.",
            S['sb_bold']),
        Paragraph("Nobody planned it this way. Nobody needed to.", S['sb_light']),
        Spacer(1, 4),
        Paragraph(
            "We got frustrated enough to write it down. "
            "Then frustrated enough to build something.",
            S['sb_bold']),
        Paragraph("These papers are the writing-it-down part.", S['sb_bold']),
        Paragraph("The something we built is a separate conversation.", S['sb_italic']),
    ]

    items.append(SeriesBox("What this series is", preface_items, label_size=9))
    return items


def content_story():
    items = [Spacer(1,4)]

    # Opening NoteBox
    items.append(NoteBox([Paragraph(
        "The same failures repeat across every financial software implementation "
        "in this industry. The same conversations happen. The same silences happen. "
        "The same blame is distributed in the same directions. Nobody writes it down "
        "because nobody benefits from writing it down. This series does.",
        S['note_text'])]))
    items.append(Spacer(1,14))

    # Section 1
    items.append(SectionHeader("1. The Pattern"))
    items.append(GreenRule(sa=6))
    for para in [
        "The pattern is recognisable to anyone who has been through one of these "
        "implementations. Not recognisable in retrospect \u2014 recognisable in real "
        "time, from week three, while it is still happening. The problem is not that "
        "the pattern is invisible. The problem is that by the time it is visible, "
        "the incentives that produced it are already in place.",

        "A financial software implementation begins with optimism on both sides. "
        "The vendor has sold a capable platform. The client has bought a solution "
        "to a real problem. The project plan looks comprehensive. The timelines look "
        "achievable. The kick-off meeting produces the right kind of energy.",

        "By week six, something is wrong. Not dramatically wrong \u2014 not a visible "
        "crisis \u2014 but wrong in the specific, quiet way that financial software "
        "implementations go wrong. A deadline has slipped. An integration point has "
        "turned out to be more complex than anticipated. A workflow assumption that "
        "seemed reasonable at signing has turned out not to reflect how the practice "
        "actually operates. The people who should be making decisions are not making them.",

        "By month three, the project is in a different shape from the one that was "
        "sold and bought. The question of whose fault this is will eventually need "
        "an answer. The answer will be complicated.",

        "This is not a story about a single implementation. It is the same story, "
        "told with different names on the door, across decades of financial services "
        "technology adoption.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    # Section 2
    items.append(Spacer(1,6))
    items.append(SectionHeader("2. The Failure Modes"))
    items.append(GreenRule(sa=6))
    items.append(Paragraph(
        "Five patterns appear in every failed implementation. They rarely appear alone.",
        S['body_j']))

    failures = [
        ("Nobody owns it.",
         "At signing, the vendor believes the client owns the implementation. "
         "The client believes the vendor owns it. Both are correct. The accountability "
         "gap is not a misunderstanding \u2014 it is a structural feature of how these "
         "projects are sold and bought. The next paper in this series examines this in full."),
        ("The plan was built before anyone understood the workflow.",
         "The implementation plan was written before week one. Before a single "
         "conversation about how the practice actually operates. Before the specific "
         "quirks of the client\u2019s approval process were understood. Before the edge "
         "cases in the data integration were mapped. The plan reflects what the vendor "
         "knows how to deliver. It does not reflect what the client needs to receive."),
        ("Integration was the afterthought.",
         "Every implementation has integration touchpoints \u2014 inbound data, outbound "
         "order files, connectivity to existing systems. In every failed implementation, "
         "these touchpoints were identified late, scoped inadequately, and tested under "
         "pressure at go-live. Integration is not a peripheral concern. It is the "
         "implementation. Treating it as a marginal consideration guarantees a marginal result."),
        ("Go-live was declared before confidence was earned.",
         "The go-live date was in the contract. It was on the project plan. The pressure "
         "to hit it was real from both sides \u2014 the vendor needed to close the project, "
         "the client needed to demonstrate progress internally. The confidence required "
         "to actually go live \u2014 the practitioner\u2019s settled sense that the system "
         "is behaving correctly \u2014 was not present. The date was hit. The confidence was not."),
        ("The vendor relationship prevented honest conversation.",
         "The sales relationship that brought the project into being is the same "
         "relationship that makes it difficult to say, six months in, that something "
         "is wrong. The warmth that was an asset in the sales process becomes a "
         "liability in the delivery process. The honest conversation that would have "
         "identified the problem in week three is the same conversation the "
         "relationship cannot afford."),
    ]
    for label, body in failures:
        items.append(Paragraph(label, S['failure_label']))
        items.append(Paragraph(body, S['body_j']))

    # Section 3
    items.append(Spacer(1,6))
    items.append(SectionHeader("3. Why They Keep Happening"))
    items.append(GreenRule(sa=6))
    for para in [
        "These failures are not caused by incompetence. They are caused by incentive "
        "structures that make them the rational outcome.",
        "The vendor\u2019s incentives are aligned toward signing, not toward implementation "
        "success. The sales team is measured on contracts, not on outcomes. The delivery "
        "team inherits the commitments made in the sales process and is measured on "
        "hitting the timeline, not on whether the client\u2019s practice actually changed.",
        "The client\u2019s incentives are aligned toward purchasing, not toward adoption. "
        "The person who bought the platform is measured on having bought a credible "
        "solution, not on whether their team uses it. The people who will use it "
        "are not always the people who decided to buy it.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    items.append(Spacer(1,8))
    items.append(NoteBox([Paragraph(
        "The implementation fails in the space between these two incentive structures. "
        "Not because anyone planned for it to fail. Because neither side\u2019s incentives "
        "required it to succeed.", S['note_text'])]))
    items.append(Spacer(1,8))

    items.append(Paragraph(
        "This matters because the fix is not found in the people. Better project "
        "managers, more experienced consultants, stronger governance \u2014 these "
        "mitigate the symptoms. They do not address the cause. The cause is "
        "structural. It will reproduce itself with every new project until the "
        "structure changes.", S['body_j']))

    # Section 4
    items.append(Spacer(1,6))
    items.append(SectionHeader("4. What This Series Is"))
    items.append(GreenRule(sa=6))
    for para in [
        "This series is not a consulting framework. It is not a methodology. It is "
        "not a set of best practices derived from industry research. It is field "
        "notes \u2014 observations from inside the implementations, from both sides of "
        "the table, across enough projects to know that the patterns are structural, "
        "not accidental.",
        "Each paper in this series takes one failure mode and examines it directly. "
        "Not to assign blame. Not to propose a universal fix. To name the mechanism "
        "accurately \u2014 so that the people sitting in those rooms can recognise it "
        "when it is happening, not in retrospect, but in real time.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    items.append(Spacer(1,14))
    items.append(HRFlowable(width="100%",thickness=0.75,
                             color=RULE_GREY,spaceAfter=10))
    # Isolated statement — generous space above already in style
    items.append(Paragraph("This series locates the cause.",
                            S['isolated_statement']))
    return items

if __name__=='__main__':
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build_document(OUT,TITLE,REF,PHOTO,NUM,
                   preface_story(),content_story(),photo_path=IMG)
