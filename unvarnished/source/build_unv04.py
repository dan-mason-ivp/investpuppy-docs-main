"""IP-UNV-04: Plan last — discovery before configuration"""
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from unvarnished_builder import *

REF   = "IP-UNV-04  \u00b7  2026"
TITLE = "Plan last \u2014 discovery before configuration"
PHOTO = "Whiteboard with WEEK 1 / WEEK 2 / WEEK 3 headings, three blank columns below."
NUM   = 4
OUT   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "output", "ip-unv-04-plan-last.pdf")
IMG   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "..", "_shared", "cover-photos", "unv04_cover_photo.jpg")
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
        "The project plan is almost always the first formal document produced in a "
        "financial software implementation. It describes, in columns, what will happen "
        "in weeks one through thirty-six. It is produced before anyone has understood "
        "the workflow it is meant to govern. This is not a planning error. It is a "
        "procurement requirement. The client asked for a plan. The vendor produced one. "
        "The project was signed.", S['note_text'])]))
    items.append(Spacer(1, 14))

    items.append(SectionHeader("1. The Sequence Problem"))
    items.append(GreenRule(sa=6))
    for para in [
        "There is a correct sequence for implementing financial software. It is: "
        "discover, then design, then configure, then test, then deliver. Most "
        "implementations do not follow this sequence. Most implementations follow "
        "a different one: plan, then configure, then discover, then redesign, then "
        "raise a change request, then extend the timeline, then retest, then deliver late.",
        "The second sequence is not produced by incompetence. It is produced by a "
        "procurement process that requires a project plan before a discovery process "
        "has been completed. The client needs a timeline and a cost before they can "
        "approve the budget. The vendor needs a signed contract before they can begin "
        "the work. The project plan is the document that connects these two requirements.",
        "It is, necessarily, a work of fiction.",
    ]:
        items.append(Paragraph(para, S['body_j']))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("2. What Discovery Actually Is"))
    items.append(GreenRule(sa=6))
    for para in [
        "Discovery is not a workshop. It is not a series of stakeholder interviews "
        "documented in a requirements spreadsheet. It is not a two-day session in a "
        "hotel conference room that produces a one-hundred-slide deck and a \u2018discovery "
        "complete\u2019 milestone.",
        "Discovery is the process of understanding, in sufficient detail, how the "
        "organisation currently works \u2014 including the workarounds, the exceptions, "
        "the manual processes, the data quality problems, and the things that are done "
        "by one person who has been doing them for eleven years and has never written "
        "them down. None of this is in the procurement document. All of it will affect "
        "the implementation.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    items.append(NoteBox([Paragraph(
        "The organisation that knows exactly what it needs from a new system does not "
        "need a discovery process. That organisation does not exist. Every organisation "
        "that has implemented financial software has discovered, during or after the "
        "implementation, requirements it did not know it had. Discovery does not create "
        "these requirements. It finds them before the configuration does.",
        S['note_text'])]))
    items.append(Spacer(1, 12))

    items.append(SectionHeader("3. The Configuration Trap"))
    items.append(GreenRule(sa=6))
    for para in [
        "Configuration begins before discovery is complete because the project plan "
        "requires it to. Week four is the start of configuration. It says so in the "
        "plan. The discovery findings arrive in week three. Some of them are "
        "incompatible with the configuration decisions already made in weeks one and two.",
        "This is not a project management failure. It is the project plan doing exactly "
        "what it was designed to do \u2014 providing a structure that allows the project "
        "to proceed before the information needed to proceed correctly is available. "
        "The change request that follows is not a sign that the project has encountered "
        "an unexpected problem. It is the project encountering the problem it was always "
        "going to encounter, at the point in the timeline where encountering it is "
        "most expensive.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    bq_body = [
        Paragraph("A system configured before the workflow is understood is not a "
            "configured system. It is a system configured for the workflow that was "
            "assumed. The distance between the assumed workflow and the actual workflow "
            "is the scope of the rework.", S['bq_body']),
        Paragraph("Every implementation has this distance. Most implementations "
            "discover it in production.", S['bq_body']),
    ]
    bq_close = Paragraph(
        "The board should have been filled before the first screen was touched.",
        S['bq_close'])
    items.append(ElevatedBlockquote(bq_body, bq_close))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("4. The Correct First Artefact"))
    items.append(GreenRule(sa=6))
    for para in [
        "The correct first artefact in a financial software implementation is not a "
        "project plan. It is a workflow map \u2014 an accurate description of how the "
        "organisation currently processes the things the new system will process.",
        "This document does not need to be beautiful. It needs to be correct. It will "
        "be wrong in places. That is not a problem. The wrongness is the discovery. "
        "The places where the workflow map does not match reality are exactly the "
        "places where the configuration decisions need to be made carefully, before "
        "the configuration begins.",
        "The project plan comes second. It is built from the workflow map, not the "
        "other way around.",
        "Three things a real discovery process produces:",
    ]:
        items.append(Paragraph(para, S['body_j']))
    for text in [
        "<b>One.</b> A workflow map that the operations team recognises as accurate "
        "\u2014 not the process as it was designed, but the process as it is actually run.",
        "<b>Two.</b> A documented list of exceptions, workarounds, and edge cases that "
        "the system will need to handle, provided by the people who handle them daily.",
        "<b>Three.</b> A set of configuration decisions made before configuration begins, "
        "with the rationale recorded \u2014 so that when assumptions prove incorrect, "
        "the correction is made against a documented baseline, not against memory.",
    ]:
        items.append(Paragraph(text, S['body_j']))

    items.append(Spacer(1, 14))
    items.append(HRFlowable(width="100%", thickness=0.75, color=RULE_GREY,
                             spaceAfter=10))
    items.append(Paragraph(
        "Plan when you know what you are planning.", S['closing']))
    items.append(Paragraph("Not before.", S['closing_green']))
    return items

if __name__ == '__main__':
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build_document(OUT, TITLE, REF, PHOTO, NUM,
                   preface_story(), content_story(), photo_path=IMG)
