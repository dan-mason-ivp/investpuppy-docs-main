"""IP-UNV-10: 9 Women Cannot Make a Baby in 1 Month"""
import sys, os as _os
sys.path.insert(0, '/tmp/unv_work/investpuppy/unvarnished/source')
from unvarnished_builder import *

REF   = "IP-UNV-10  \u00b7  2026"
TITLE = "9 Women Cannot Make a Baby in 1 Month"
PHOTO = "Long boardroom table, too many chairs, too many laptops, too many coffee cups. \
Far end of table: one person with a single notepad and pen, no laptop. \
Projected slide reads: RESOURCE PLAN \u2013 PHASE 1. Dense grid of names and roles. \
Overhead fluorescent light."
NUM   = 10
OUT   = "/mnt/user-data/outputs/ip-unv-10-nine-women.pdf"
# Use unv08 cover as placeholder — no unv10 photo yet
IMG   = "/tmp/unv_work/investpuppy/_shared/cover-photos/unv10_cover_photo.jpg"
S     = get_styles()

ATTRIBUTION = (
    "InvestPuppy builds Vektor \u2014 a systematic listed equity portfolio management "
    "platform. Before we built it, we spent decades in the rooms where financial software "
    "implementations fail. These papers are what we saw. The something we built is a "
    "separate conversation."
)


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
            "The proposal had arrived with twelve consultants, a competitive day rate, "
            "and a Gantt chart that implied all twelve would be productive simultaneously.",
            S['sb_bold']),
        Paragraph("The maths looked right. The outcome was already written.", S['sb_light']),
        Spacer(1, 8),
        Paragraph("It isn\u2019t incompetence.", S['sb_bold']),
        Paragraph("It\u2019s procurement doing its job perfectly, "
            "optimising for the wrong variable.", S['sb_bold']),
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
    S = get_styles()
    items = []

    # ── Opening ──────────────────────────────────────────────────────────────
    items.append(NoteBox([Paragraph(
        "Fred Brooks named it in 1975. "
        "Fifty years later the same meeting is still happening in the same boardroom. "
        "A project is late. The proposal on the table is more people. "
        "The logic is intuitive: if one consultant takes twelve months, "
        "twelve consultants take one month. "
        "The logic is wrong. It has always been wrong. "
        "It will be wrong the next time this meeting happens. "
        "It fails because it treats knowledge work as a production line, "
        "where capacity is fungible and output scales with headcount.",
        S['note_text'])]))
    items.append(Spacer(1, 8))

    items.append(GreenRule(sa=6))

    # ── Section 1: Gestation ─────────────────────────────────────────────────
    items.append(Spacer(1, 10))
    items.append(Paragraph("Some things take the time they take.", S['spaced_statement']))
    items.append(Spacer(1, 6))
    items.append(Paragraph(
        "A baby takes nine months. Not because the process is inefficient. "
        "Because the process is sequential. There are things that cannot begin "
        "until other things are complete. There are decisions that cannot be made "
        "before the consequences of earlier decisions are understood.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "A financial platform implementation has the same structure. "
        "The data model must be settled before the order management logic can be built. "
        "The order management logic must be built before the reconciliation layer can be tested. "
        "The reconciliation layer must be tested before the compliance team can begin their review. "
        "The compliance review must be complete before the UAT plan can be written.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "You can have twenty people standing in the corridor waiting for each handoff. "
        "The sequence does not compress. "
        "The calendar moves at one day per day regardless of headcount.",
        S['isolated_statement']))
    items.append(Spacer(1, 10))
    items.append(NoteBox([
        Paragraph(
            "The irreducible sequence is not a project management problem. "
            "It is a physics problem. You cannot parallelize work that depends on the "
            "output of preceding work. Adding people to a sequential process "
            "does not accelerate it. It creates a queue.",
            S['note_text'])
    ]))
    items.append(Spacer(1, 8))

    # ── Section 2: Coordination tax ──────────────────────────────────────────
    items.append(Paragraph("The coordination tax.", S['spaced_statement']))
    items.append(Spacer(1, 6))
    items.append(Paragraph(
        "A team of two requires one communication channel. "
        "A team of five requires ten. "
        "A team of twelve requires sixty-six.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "This is not a hypothesis. It is arithmetic. "
        "Every person added to a project adds n\u22121 new communication channels, "
        "where n is the new team size. Each channel requires maintenance: "
        "alignment meetings, status updates, decision documentation, "
        "context transfers when someone rotates off the engagement.",
        S['body']))
    items.append(Spacer(1, 8))

    items.append(Paragraph(
        "The day rate spreadsheet captures twelve daily rates. "
        "It does not capture the client\u2019s internal cost of managing twelve people. "
        "It does not capture the weekly steering committee. "
        "It does not capture the three-hour alignment call that produces a document "
        "that says what everyone already agreed in the previous three-hour alignment call.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "This is not a management problem. "
        "It is arithmetic operating on the wrong inputs: "
        "more people does not mean more output "
        "when the cost of connecting them exceeds the value they produce.",
        S['isolated_statement']))
    items.append(Spacer(1, 8))

    # ── Stat callout ─────────────────────────────────────────────────────────
    items.append(NoteBox([
        Paragraph(
            "The fully-loaded cost of a twelve-person consulting engagement "
            "includes the client\u2019s internal management burden, the rework generated "
            "by miscommunication across sixty-six channels, and the delay caused by "
            "decisions that cannot be made until all twelve people are in the same room. "
            "This cost does not appear on the procurement spreadsheet. "
            "It appears on the project timeline six months later.",
            S['note_text'])
    ]))
    items.append(Spacer(1, 8))

    # ── Section 3: Rework multiplier ─────────────────────────────────────────
    items.append(GreenRule(sa=6))
    items.append(Spacer(1, 10))
    items.append(Paragraph("The rework multiplier.", S['spaced_statement']))
    items.append(Spacer(1, 6))
    items.append(Paragraph(
        "A wrong architectural decision in month one costs one hour to make "
        "and approximately four months to undo.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "The pattern is consistent. A data model designed for one portfolio per client. "
        "Six months into the build, the requirement for multiple portfolios per client "
        "is confirmed. The data model change takes four days. "
        "The regression testing, the re-migration of historical data, and the retesting "
        "of every downstream function built on the original model takes eleven weeks. "
        "The decision that cost an hour to make costs a quarter to undo.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "This is the number that never appears in the proposal. "
        "The proposal prices inputs: consultant days, travel, licensing. "
        "It does not price the probability of a wrong decision, "
        "multiplied by the cost of that decision compounded over the engagement.",
        S['body']))
    items.append(Spacer(1, 8))

    items.append(Paragraph(
        "The experienced practitioner recognises the decision point before it becomes a problem. "
        "They have seen the cascade that follows the wrong choice. "
        "They know which question to ask in the meeting that has not happened yet.",
        S['isolated_statement']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "You are not paying a premium rate for time. "
        "You are paying for the map of the minefield. "
        "You are not paying for the map because the map is expensive. "
        "You are paying for it because it is the only thing that prevents "
        "month one from becoming month five\u2019s rework. "
        "The map was not cheap to produce. "
        "Every failed project in the practitioner\u2019s history was one of the surveys.",
        S['body']))
    items.append(Spacer(1, 8))

    # ── Section 4: Week-two signal ────────────────────────────────────────────
    items.append(GreenRule(sa=6))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "Everyone sees it in week two.", S['spaced_statement']))
    items.append(Spacer(1, 6))
    items.append(Paragraph(
        "The warning sign is visible early. The plan requires twelve weeks of delivery "
        "work from a team already running at capacity. The maths do not work. "
        "Anyone who looks at the project plan in week two can see that week eight will fail.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "Nobody says so. Not because they cannot see it. "
        "Because saying so requires a conversation "
        "that is more uncomfortable than not saying so.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "The problem enters the status report as amber. "
        "Amber is the natural habitat of problems that everyone knows about "
        "and nobody wants to own. "
        "Week three: amber. Week five: amber. Week seven: amber. "
        "Day one of week eight: crisis.",
        S['isolated_statement']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "The crisis produces a response. Additional people are assigned. "
        "They arrive on the morning the deliverable was due.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "The person who has been doing the work now has two jobs. "
        "The first is delivering the work. "
        "The second is bringing the new arrivals up to speed on eight weeks of context, "
        "decisions, and dead ends. "
        "These two jobs are not compatible. "
        "The second displaces the first at exactly the moment "
        "the first cannot afford to be displaced.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "The signal in week two was actionable. "
        "A scope adjustment, a timeline extension, an honest conversation. "
        "All cheaper than the crisis they would have prevented.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "The deliverable is missed. The cost has doubled. "
        "The post-project review will recommend earlier escalation next time.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(NoteBox([Paragraph(
        "Next time, the signal will arrive in week two. "
        "The status report will turn amber. "
        "The structural incentive has not changed: "
        "an uncomfortable conversation now versus an impossible situation later. "
        "Amber exists precisely because it lets everyone acknowledge the problem "
        "without owning it.",
        S['note_text'])]))
    items.append(Spacer(1, 8))

    # ── Section 5: The procurement problem ───────────────────────────────────
    items.append(GreenRule(sa=6))
    items.append(Spacer(1, 10))
    items.append(Paragraph(
        "The procurement committee is not wrong.", S['spaced_statement']))
    items.append(Spacer(1, 6))
    items.append(Paragraph(
        "A board paper that approves eight junior consultants at rate X "
        "demonstrably minimises the visible input cost. "
        "A board paper that approves two senior practitioners at 2.5X "
        "fails the line-item review on day rate alone.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "The procurement committee is optimising for the metric it can measure. "
        "Day rate is measurable. Rework probability is not. "
        "Coordination overhead is not. "
        "The cost of a wrong data model decision in month one "
        "does not appear in the approval paper because nobody put it there. "
        "Nobody put it there because nobody was asked to. "
        "The approval process was designed to approve spending, not to model outcomes.",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "This is not a failure of the procurement system. "
        "It is the procurement system performing exactly as designed, "
        "measuring exactly what it was built to measure, "
        "and producing a decision that looks correct in the room "
        "and looks catastrophic eighteen months later.",
        S['isolated_statement']))
    items.append(Spacer(1, 10))
    items.append(NoteBox([
        Paragraph(
            "The argument for premium rates is not that senior practitioners work harder. "
            "It is that they make fewer decisions that need to be reversed. "
            "Every reversed decision in a financial platform implementation "
            "carries a multiplier: the work undone, the work redone, the downstream "
            "work that was built on the wrong foundation and must now also be rebuilt. "
            "A single avoided reversal typically costs more than the rate differential "
            "for the entire engagement.",
            S['note_text'])
    ]))
    items.append(Spacer(1, 8))

    # ── Closing ───────────────────────────────────────────────────────────────
    items.append(GreenRule(sa=6))
    items.append(Spacer(1, 10))
    items.append(Paragraph(
        "Before the next proposal lands on your desk, two questions.",
        S['spaced_statement']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "The proposal will show you a day rate, a team size, a timeline. "
        "Ask instead: what is the probability that a decision made in month one "
        "will need to be reversed in month five? "
        "And what does that reversal cost, fully loaded?",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "Then ask the second question: if the signal arrives in week two "
        "that resources will be insufficient in week eight, "
        "what is the cost of naming it then "
        "rather than discovering it on day one of week eight?",
        S['body']))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "If the proposal cannot answer either question, it is a resourcing schedule "
        "dressed as a project plan. They look identical in a board paper. "
        "They produce very different outcomes at go-live.",
        S['isolated_statement']))
    items.append(Spacer(1, 8))

    # ── Closing statement ─────────────────────────────────────────────────────
    items.append(NoteBox([
        Paragraph(
            "Nine women cannot make a baby in one month. "
            "Some things take the time they take. "
            "The only variable you control is whether the person doing the work "
            "has seen the path before. "
            "The same distribution that removes accountability removes capacity.",
            S['note_text'])
    ]))
    items.append(Spacer(1, 10))
    items.append(Paragraph(
        "This paper is part of the Unvarnished series \u2014 field notes from decades "
        "of bad projects. The series is published by InvestPuppy. "
        "For the full series and other work visit investpuppy.com.",
        S['attribution']))

    return items


if __name__ == '__main__':
    import os
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build_document(OUT, TITLE, REF, PHOTO, NUM,
                   preface_story(), content_story(), photo_path=IMG)
    print(f"Built: {OUT}")
