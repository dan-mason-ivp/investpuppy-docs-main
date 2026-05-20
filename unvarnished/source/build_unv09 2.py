"""IP-UNV-09: The U in UAT — kind of important..."""
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from unvarnished_builder import *

REF   = "IP-UNV-09  \u00b7  2026"
TITLE = "The U in UAT \u2014 kind of important..."
PHOTO = "UAT sign-off document, all test cases PASS, Project Accepted stamp. Takeaway coffee cup labelled James. Elliott Consulting business card. Packed bag visible. Empty chairs in background."
NUM   = 9
OUT   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "output", "ip-unv-09-u-in-uat.pdf")
IMG   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "..", "_shared", "cover-photos", "unv09_cover_photo.jpg")
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
        "The UAT sign-off document has the right signatures on it. The signatories "
        "were not users of the system. They were consultants working from test scripts "
        "written by other consultants, testing a configuration reviewed by a project "
        "team that had not spoken to the people who would use it in production. "
        "The document says PASS. The system goes live. Three weeks later, the people "
        "who use it every day explain, at length, why it does not.",
        S['note_text'])]))
    items.append(Spacer(1, 14))

    items.append(SectionHeader("1. What the U Is For"))
    items.append(GreenRule(sa=6))
    for para in [
        "User Acceptance Testing. Three words. Each one is load-bearing.",
        "<i>Testing</i> means that something is being evaluated against a standard. "
        "<i>Acceptance</i> means that the evaluation results in a judgment \u2014 this "
        "works, or it does not. <i>User</i> means that the person making that judgment "
        "is the person who will use the system in production, on real transactions, "
        "under real conditions, with real consequences for getting it wrong.",
        "Remove the user from User Acceptance Testing and you have acceptance testing. "
        "Which is a different thing. Acceptance testing establishes whether the system "
        "meets the specification. UAT establishes whether the system works for the "
        "people whose working lives depend on it. These are not the same test. A system "
        "can pass acceptance testing and fail UAT. This happens. It is, in fact, one "
        "of the most common outcomes in financial software implementation.",
        "The difference between the two tests is not technical. It is human. It is "
        "the difference between a system that does what it was specified to do and a "
        "system that does what the users actually need it to do. The specification was "
        "produced before the discovery was complete, before all the stakeholders were "
        "in the room, and before anyone had documented the workarounds and exceptions "
        "the users handle every day. The gap between the specification and the reality "
        "is exactly the gap that UAT is designed to find. It cannot find that gap if "
        "the users are not running the test.",
    ]:
        items.append(Paragraph(para, S['body_j']))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("2. How the Outsourcing Happens"))
    items.append(GreenRule(sa=6))
    for para in [
        "The decision to outsource UAT is rarely announced as a decision. It arrives "
        "as a resource allocation, a timeline pressure, or a project management "
        "convenience.",
        "The users are busy. The system is going live in six weeks. The project team "
        "has UAT test scripts. The consulting firm has testers. The testers are "
        "available. The users are not. The project manager makes a practical decision: "
        "the consultants will run the UAT. The users will be available for sign-off "
        "queries if needed.",
        "This is not cynicism. It is a rational response to a genuine resourcing "
        "constraint. The problem is that the rational response to the resourcing "
        "constraint produces exactly the outcome the UAT phase was designed to prevent.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    items.append(NoteBox([Paragraph(
        "The users are busy because the organisation has not protected their time for "
        "UAT. The organisation has not protected their time for UAT because UAT has "
        "been treated as a project team activity rather than an operational activity. "
        "It has been scheduled around the project\u2019s needs rather than the users\u2019 "
        "availability. The resourcing constraint that makes consultant-led UAT feel "
        "necessary is a planning failure, not a fixed condition. It was created by the "
        "same project planning process that will later cite it as the reason UAT "
        "was outsourced.", S['note_text'])]))
    items.append(Spacer(1, 12))

    items.append(SectionHeader("3. What the Consultant\u2019s UAT Actually Tests"))
    items.append(GreenRule(sa=6))
    for para in [
        "A consultant running UAT with a test script is not testing whether the system "
        "works. They are testing whether the system produces the outputs described in "
        "the test script, given the inputs described in the test script, in the "
        "sequence described in the test script.",
        "This is a narrower question. It excludes, by design, everything that is not "
        "in the test script. It excludes the transaction that occurs twice a month and "
        "was not in the test script because nobody thought to include it. It excludes "
        "the workflow exception that the operations team handles manually and never "
        "mentioned during requirements gathering because they assumed the system would "
        "handle it automatically. It excludes the report that the risk team runs every "
        "Friday that was not in the standard reports list because the risk team was "
        "not in the specification workshop.",
        "The consultant passes these tests because the tests do not test these things.",
        "In a regulated environment, the gap between what was tested and what was "
        "needed is not only an operational problem. A reporting process that fails "
        "in its first post-live run, because the compliance function was not "
        "represented in the UAT, is a reportable event. The consultant who signed "
        "the PASS is not the one who reports it.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    bq_body = [
        Paragraph("The test script was written from the specification. The specification "
            "was written from the workshops. The workshops were attended by the "
            "stakeholders who were available.", S['bq_body']),
        Paragraph("The users who were not available did not attend the workshops, did "
            "not shape the specification, and did not write the test scripts. A "
            "consultant running those test scripts is not testing whether the system "
            "works for the users. They are testing whether the system is consistent "
            "with a document that the users had limited input into.", S['bq_body']),
    ]
    bq_close = Paragraph(
        "The U was removed long before the UAT phase began.", S['bq_close'])
    items.append(ElevatedBlockquote(bq_body, bq_close))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("4. What Real UAT Looks Like"))
    items.append(GreenRule(sa=6))
    for para in [
        "Real UAT is operationally inconvenient. It requires the users to stop doing "
        "their jobs for long enough to test the system that will change their jobs. "
        "It requires the organisation to treat that time as a legitimate operational "
        "cost, not as a project overhead to be minimised. It requires test scripts "
        "that were written with user input, not only from the specification. And it "
        "requires someone with the authority to say, without commercial consequence, "
        "that the system is not ready.",
        "That last requirement is the hardest one. The user who runs UAT and finds "
        "that the system does not work for them is not raising a problem. They are "
        "doing their job. The organisation that has outsourced UAT to a consultant "
        "has, among other things, removed the person most likely to say that the "
        "system is not ready \u2014 and replaced them with a person whose engagement "
        "ends when the milestone is closed.",
        "Three things that make UAT real rather than documentary:",
    ]:
        items.append(Paragraph(para, S['body_j']))
    for text in [
        "<b>One.</b> Users \u2014 the actual people who will use the system in production "
        "\u2014 run the tests. Not a representative, not a delegate, not a consultant with "
        "a test script. The person who processes the transactions, produces the reports, "
        "handles the exceptions. That person.",
        "<b>Two.</b> The test scripts include the transactions that are not in the "
        "specification. The exceptions, the edge cases, the processes the users know "
        "exist and the project team does not. These are identified in a test script "
        "workshop attended by users before UAT begins \u2014 not assembled from "
        "the specification alone.",
        "<b>Three.</b> The sign-off authority rests with the users, not with the "
        "project team. A UAT phase in which the project manager can override a user\u2019s "
        "rejection of a test case is not a UAT phase. It is a documentation exercise. "
        "The user\u2019s judgment is the test. Everything else is administration.",
    ]:
        items.append(Paragraph(text, S['body_j']))
    items.append(Paragraph(
        "The organisation that protects user time for UAT, builds test scripts from "
        "user knowledge, and gives users genuine sign-off authority will find that "
        "UAT takes longer than the project plan anticipated. It will also find that "
        "go-live is not followed by three weeks of post-live crisis. The time is not "
        "lost. It is moved from after go-live to before it, where it costs a fraction "
        "of what it costs later.", S['body_j']))

    items.append(Spacer(1, 14))
    items.append(HRFlowable(width="100%", thickness=0.75, color=RULE_GREY,
                             spaceAfter=10))
    items.append(Paragraph(
        "User Acceptance Testing.", S['closing']))
    items.append(Paragraph(
        "The word \u2018user\u2019 is not decorative.", S['closing_green']))
    return items

if __name__ == '__main__':
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build_document(OUT, TITLE, REF, PHOTO, NUM,
                   preface_story(), content_story(), photo_path=IMG)
