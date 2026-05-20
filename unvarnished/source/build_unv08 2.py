"""IP-UNV-08: Life after live"""
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from unvarnished_builder import *

REF   = "IP-UNV-08  \u00b7  2026"
TITLE = "Life after live"
PHOTO = "Worn desk calendar, July go-live date circled in blue, crossed out in red, circled again. Cluttered office desk."
NUM   = 8
OUT   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "output", "ip-unv-08-life-after-live.pdf")
IMG   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "..", "_shared", "cover-photos", "unv08_cover_photo.jpg")
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

    items.append(Paragraph("The system went live.", S['spaced_statement']))
    items.append(Paragraph("The implementation did not.", S['spaced_statement']))
    items.append(HRFlowable(width="100%", thickness=0.5,
                             color=RULE_GREY, spaceAfter=12, spaceBefore=0))

    items.append(NoteBox([Paragraph(
        "Go-live is the end of the project. It says so in the project plan \u2014 the "
        "final milestone, the one the Gantt chart terminates at, the one the steering "
        "committee has been tracking for eleven months. It is not the end of anything. "
        "It is the beginning of a different, harder problem: the problem of an "
        "organisation built around a legacy system encountering, for the first time "
        "at production volume, the system that was supposed to replace it.",
        S['note_text'])]))
    items.append(Spacer(1, 14))

    items.append(SectionHeader("1. The Mythology of Go-Live"))
    items.append(GreenRule(sa=6))
    for para in [
        "The go-live date functions as a destination. Everything before it is a journey. "
        "The kick-off is the departure. The UAT phase is the approach. Go-live is "
        "arrival. This mythology is maintained because it is useful: it gives the "
        "project a shape, gives the steering committee something to track, gives the "
        "vendor a milestone against which payment is triggered, and gives the project "
        "team a moment of completion.",
        "What it does not give anyone is an accurate description of what actually "
        "happens on go-live day, or in the weeks that follow.",
        "Go-live day is the first day the system is used in production, at volume, "
        "by the people who were not in the UAT environment, on the data that was not "
        "in the test dataset, for the transactions that were not in the test scripts. "
        "It is the first real test of the implementation. The eleven months that "
        "preceded it were, in various ways, a preparation for this test. The project "
        "plan treated it as the finish line. It is the starting gun.",
    ]:
        items.append(Paragraph(para, S['body_j']))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("2. The Hypercare Fiction"))
    items.append(GreenRule(sa=6))
    for para in [
        "Most project plans include a hypercare phase \u2014 a period of intensified "
        "support immediately following go-live, typically two to four weeks. Hypercare "
        "ends when the project ends. The issues do not.",
        "The issues that surface during hypercare are the obvious ones: configuration "
        "errors that appear under production load, data migration problems that emerge "
        "at volume, interface failures that the test environment did not replicate. "
        "These are resolved. The project team departs. Hypercare is logged as complete.",
        "The issues that surface after hypercare are the real ones. The reporting that "
        "does not match the legacy system output the risk team was using as their "
        "source of truth. The workflow exception that occurs twice a month and was not "
        "in the test scripts. The user who has been processing transactions incorrectly "
        "for six weeks because the training did not cover the edge case they encounter "
        "daily. And \u2014 critically \u2014 the regulatory reporting failures that emerge "
        "when the first post-live reporting period closes and the output does not match "
        "what the compliance function was producing from the old system. These are not "
        "merely operational problems. They are reportable events. They arrive after "
        "the project manager\u2019s engagement has ended.",
    ]:
        items.append(Paragraph(para, S['body_j']))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("3. The Workaround Economy"))
    items.append(GreenRule(sa=6))
    for para in [
        "Every organisation that has been using a legacy financial system for more "
        "than five years has built a workaround economy around it. Spreadsheets that "
        "compensate for reporting limitations. Manual processes that handle transactions "
        "the system cannot. Institutional knowledge held by specific individuals who "
        "know which sequence of operations produces the output the system was not "
        "designed to produce directly.",
        "The new system was not configured to accommodate these workarounds, because "
        "nobody documented them during discovery. They were not on the process maps. "
        "They were in the heads of the people who performed them.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    bq_body = [
        Paragraph("The system that was built for the specification meets the "
            "organisation that has been using workarounds for eighteen months. "
            "Between them is a gap.", S['bq_body']),
        Paragraph("The gap is filled initially by people who know the old workarounds "
            "and have not yet learned the new ones. Then it is filled by new workarounds "
            "\u2014 built on top of the new system, invisible to the vendor, undocumented, "
            "dependent on the continued employment of the people who invented them.",
            S['bq_body']),
    ]
    bq_close = Paragraph("The system went live. The implementation did not.", S['bq_close'])
    items.append(ElevatedBlockquote(bq_body, bq_close))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("4. What Comes After Live"))
    items.append(GreenRule(sa=6))
    items.append(Paragraph(
        "The post-live phase is not a support problem. It is an adoption problem, a "
        "change management problem, a configuration problem, and a data quality problem "
        "\u2014 and it is substantially larger, in real terms, than most project plans "
        "acknowledge.", S['body_j']))
    items.append(Paragraph(
        "A post-live plan adequate to the actual challenge has five components:",
        S['body']))
    for text in [
        "<b>One.</b> A structured process for capturing and resolving configuration "
        "issues that only appear under production load \u2014 not a support ticket queue "
        "but a prioritised, resourced backlog with vendor involvement and defined "
        "resolution timelines.",
        "<b>Two.</b> An adoption tracking mechanism that measures not go-live usage, "
        "but correct usage \u2014 the proportion of transactions being processed through "
        "the system in the way it was designed, rather than around it.",
        "<b>Three.</b> A workaround audit conducted sixty days after go-live, "
        "identifying manual processes that have emerged around the system and the "
        "configuration changes that would eliminate them. This audit should be "
        "conducted by someone with access to the original specification \u2014 the gap "
        "between the specification and the workaround is the measure of the "
        "implementation\u2019s actual completeness.",
        "<b>Four.</b> A regulatory reporting validation conducted at the close of the "
        "first full reporting period post-live, comparing system output against legacy "
        "output for every report with a regulatory or compliance dimension. Discrepancies "
        "are not post-live issues. They are pre-live failures that went undetected.",
        "<b>Five.</b> A data quality review at ninety days, measuring mandate compliance, "
        "data completeness, and the accuracy of the migrated data against the source. "
        "Data quality problems that were present at migration but below the threshold "
        "of immediate visibility will surface here. They should be surfaced by design, "
        "not by a client complaint.",
    ]:
        items.append(Paragraph(text, S['body_j']))
    items.append(Paragraph(
        "The project plan that ends at go-live is not a plan for the implementation. "
        "It is a plan for the project. These are not the same thing.", S['body_j']))

    items.append(Spacer(1, 14))
    items.append(HRFlowable(width="100%", thickness=0.75, color=RULE_GREY,
                             spaceAfter=10))
    items.append(Paragraph(
        "Plan for what comes after live.", S['closing']))
    items.append(Paragraph("It is longer than the project.", S['closing_green']))
    return items

if __name__ == '__main__':
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build_document(OUT, TITLE, REF, PHOTO, NUM,
                   preface_story(), content_story(), photo_path=IMG)
