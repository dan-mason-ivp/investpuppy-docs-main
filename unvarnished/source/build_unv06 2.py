"""IP-UNV-06: The invisible stakeholders"""
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from unvarnished_builder import *

REF   = "IP-UNV-06  \u00b7  2026"
TITLE = "The invisible stakeholders"
PHOTO = "Boardroom meeting table, people working on laptops, foreground empty chair with COMPLIANCE name card."
NUM   = 6
OUT   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "output", "ip-unv-06-invisible-stakeholders.pdf")
IMG   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "..", "_shared", "cover-photos", "unv06_cover_photo.jpg")
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
    items = [Spacer(1, 4)]

    items.append(NoteBox([Paragraph(
        "Every financial software implementation has two sets of stakeholders. "
        "The first set attended the workshops, reviewed the specification, and signed "
        "the project plan. The second set did not attend anything. They were not "
        "invited, or were invited once and sent a delegate, or were told the project "
        "was being handled by the first set and they would be consulted when relevant. "
        "They discovered the system on go-live day. They have been explaining why it "
        "does not work for them ever since.", S['note_text'])]))
    items.append(Spacer(1, 14))

    items.append(SectionHeader("1. Who Is Not in the Room"))
    items.append(GreenRule(sa=6))
    for para in [
        "The workshop that produces the specification is not a representative sample "
        "of the people who will use the system. It is a sample of the people who were "
        "available, willing, and sufficiently senior to attend. These are not the "
        "same people.",
        "The operations director attends. The portfolio analyst who processes thirty "
        "transactions a day does not. The head of compliance attends. The compliance "
        "officer who produces the monthly regulatory report does not. The CTO attends "
        "the architecture session. The system administrator who will maintain the "
        "integrations does not.",
        "The people who attend the workshops describe the system at the level at which "
        "they interact with it \u2014 which is to say, the level at which they rarely "
        "interact with it at all. The people who interact with it daily, in detail, "
        "at volume, were not asked.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    items.append(NoteBox([Paragraph(
        "The specification that results from a workshop attended by senior stakeholders "
        "will correctly describe the high-level workflow. It will incompletely describe "
        "the exceptions, the edge cases, the manual processes, and the reporting "
        "requirements that matter most to the people who use the system every day. "
        "These are the things that generate post-go-live complaints. They were always "
        "present. Nobody asked.", S['note_text'])]))
    items.append(Spacer(1, 12))

    items.append(SectionHeader("2. The Map Is Not the Stakeholder"))
    items.append(GreenRule(sa=6))
    items.append(Paragraph(
        "The stakeholder map is not the same as the stakeholder. This distinction is "
        "where most stakeholder engagement processes fail.",
        S['body_j']))
    for para in [
        "Stakeholder mapping produces a document. The document lists the stakeholders, "
        "their level of interest, their level of influence, and their communication "
        "plan. It is produced in week two of the project and updated in week three. "
        "It is a governance artefact. It is not an engagement process.",
        "The compliance function listed on the stakeholder map as \u2018high interest / "
        "medium influence\u2019 with a bi-weekly update did not attend the configuration "
        "workshops. They received the updates. They may have read some of them. They "
        "were not asked whether the system would produce the regulatory report they need. "
        "The go-live post-implementation review will note that the compliance reporting "
        "requirement was not in scope, was raised as a post-go-live item, and is "
        "currently being assessed for inclusion in phase two.",
        "Listing a stakeholder on a map, sending them a fortnightly summary, and asking "
        "them to confirm receipt is not stakeholder engagement. It is stakeholder "
        "administration. The two things are not the same, and confusing them is one "
        "of the primary reasons invisible stakeholders remain invisible.",
    ]:
        items.append(Paragraph(para, S['body_j']))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("3. The Empty Chair"))
    items.append(GreenRule(sa=6))
    for para in [
        "There is a moment in every failed implementation where the invisible stakeholder "
        "becomes visible. It is usually about three weeks after go-live. The system is "
        "live. The immediate crisis of the cutover has passed. The project team is "
        "beginning to wind down. And then someone \u2014 a compliance officer, a "
        "back-office analyst, a reporting team lead \u2014 submits a ticket, or attends "
        "a post-go-live meeting, or walks into the project manager\u2019s office and "
        "says: this system does not do the thing I need it to do.",
        "They are not wrong. The system does not do the thing they need it to do, "
        "because they were not in the room when the configuration decisions were made.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    bq_body = [
        Paragraph("There is a more expensive version of this problem. It does not "
            "arrive at go-live. It arrives when regulatory requirements change after "
            "the system is live \u2014 and the architecture cannot accommodate the change "
            "because the compliance function was not involved in the design.",
            S['bq_body']),
        Paragraph("By this point the project is closed, the team is disbanded, and the "
            "cost of the remediation is a new project.", S['bq_body']),
    ]
    bq_close = Paragraph(
        "The chair had their name on it. It was empty when the room was designed.",
        S['bq_close'])
    items.append(ElevatedBlockquote(bq_body, bq_close))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("4. Finding the Invisible Stakeholders"))
    items.append(GreenRule(sa=6))
    for para in [
        "The invisible stakeholder is not hard to find. They are the person who "
        "currently does, manually or in a legacy system, the thing the new system is "
        "supposed to replace. They exist in every function the system touches. They "
        "are identifiable before the specification is written.",
        "The question that finds them is not \u2018who is responsible for this function?\u2019 "
        "It is \u2018who does this work?\u2019 These are frequently different people, and "
        "only one of them knows what the system needs to do.",
        "Three things that surface invisible stakeholders before go-live:",
    ]:
        items.append(Paragraph(para, S['body_j']))
    for text in [
        "<b>One.</b> A workflow walkthrough conducted with the people who do the work, "
        "not the people who manage it \u2014 specifically including the exception-handling "
        "processes that senior stakeholders may not know exist.",
        "<b>Two.</b> A reporting requirement sign-off process that includes the recipients "
        "of every report the system will produce, not only the commissioners. The person "
        "who uses the report is the authority on whether it is correct.",
        "<b>Three.</b> A UAT process that requires sign-off from every function that will "
        "use the system in production. Sign-off by a project team member on behalf of a "
        "function is not sign-off. It is documentation of the gap that will become "
        "visible at go-live.",
    ]:
        items.append(Paragraph(text, S['body_j']))
    items.append(Paragraph(
        "Ask who is not in the room. Then go and find them.", S['body_j']))

    items.append(Spacer(1, 14))
    items.append(HRFlowable(width="100%", thickness=0.75, color=RULE_GREY,
                             spaceAfter=10))
    items.append(Paragraph(
        "The empty chair was always there.", S['closing']))
    items.append(Paragraph("It had a name on it.", S['closing_green']))
    return items

if __name__ == '__main__':
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build_document(OUT, TITLE, REF, PHOTO, NUM,
                   preface_story(), content_story(), photo_path=IMG)
