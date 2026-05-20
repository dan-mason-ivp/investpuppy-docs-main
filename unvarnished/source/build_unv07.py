"""IP-UNV-07: A hammer is a tool, not a methodology"""
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from unvarnished_builder import *

REF   = "IP-UNV-07  \u00b7  2026"
TITLE = "A hammer is a tool, not a methodology"
PHOTO = "Swiss Army knife with blade extended on a desk with financial spreadsheet, circuit board, and annotated legal document."
NUM   = 7
OUT   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "output", "ip-unv-07-hammer-tool-methodology.pdf")
IMG   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "..", "_shared", "cover-photos", "unv07_cover_photo.jpg")
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
    S = get_styles()
    items = [Spacer(1, 4)]

    items.append(NoteBox([Paragraph(
        "A tool is something you pick up, use for the task it is suited for, and put "
        "down. A methodology is something that requires certification, governance, a "
        "steering committee, a maturity model, and a two-day offsite. The gap between "
        "these two things is not semantic. It is the gap between something that serves "
        "the work and something that the work is made to serve. Most of the "
        "methodologies in current circulation were tools before they were elevated. "
        "The elevation was not accidental.", S['note_text'])]))
    items.append(Spacer(1, 10))

    items.append(Paragraph(
        "The tool became a methodology when there was money in the methodology.",
        S['spaced_statement']))

    items.append(SectionHeader("1. How Tools Get Elevated"))
    items.append(GreenRule(sa=6))
    for para in [
        "The elevation of a tool to a philosophy follows a consistent pattern. The tool "
        "is genuinely useful \u2014 it solves a real problem in a specific context. Early "
        "adopters use it well, for that problem, in that context. Results are good. "
        "Case studies are written.",
        "Then something shifts. The tool acquires a name. The name acquires a capital "
        "letter. Consultants begin building practices around it. Certification "
        "programmes are created. Organisations begin asking not \u2018does this tool fit "
        "our problem?\u2019 but \u2018are we doing this correctly?\u2019 The question of fit "
        "is replaced by the question of compliance.",
        "At this point, the tool is no longer a tool. It has become a methodology. "
        "And the incentive structure that elevated it ensures it will remain one "
        "\u2014 because the people who benefit from the methodology are not the people "
        "who need to solve the problem. They are the people who are paid to administer it.",
        "There are two distinct failure modes worth separating. The first is the tool "
        "applied in the wrong context \u2014 a genuinely useful tool deployed against a "
        "problem it was not designed for. The second is the tool elevated to replace "
        "judgment \u2014 where the question of whether to use the tool at all has stopped "
        "being asked. Both appear below. They require different remedies.",
    ]:
        items.append(Paragraph(para, S['body_j']))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("2. Six Tools That Became Methodologies"))
    items.append(GreenRule(sa=6))
    items.append(Paragraph(
        "The sequence below is roughly chronological \u2014 ordered from the tools whose "
        "methodology phase is most clearly behind them to the tool currently at its "
        "peak. The example that is clearly over is the proof of what happens when "
        "the dust settles. The example that is current is the one that needs to be "
        "assessed now, while it is still possible to make the distinction.",
        S['body_j']))
    items.append(Spacer(1, 6))

    tools = [
        ("Agile.",
         "Agile began as a set of principles for software development teams working "
         "on problems too complex to specify in advance. It worked, in that context. "
         "It then became a universal project philosophy. Organisations began applying "
         "Agile to regulatory compliance programmes, infrastructure rollouts, and "
         "financial software implementations where the work was not complex in the "
         "Agile sense \u2014 it was simply uncertain. The ceremonies remained. The "
         "retrospectives, the standups, the sprints, the velocity charts. The process "
         "managed the work instead of serving it. This is the wrong-context failure mode."),
        ("Design thinking.",
         "A creative problem-framing tool applied to regulatory compliance challenges. "
         "Financial services firms sitting through design thinking workshops on problems "
         "that had nothing to do with user experience and everything to do with process "
         "discipline. The tool is real and valuable in its context. Applied outside it, "
         "it consumes time and produces empathy maps for problems that needed process "
         "maps. Wrong context."),
        ("Blockchain.",
         "Between 2017 and 2020, a significant portion of financial services strategy "
         "documents contained the word \u2018blockchain\u2019. Most no longer do. The distributed "
         "trust mechanism was proposed for systems that already had trust mechanisms "
         "that worked. The use cases remain valid. The methodology phase has, "
         "mercifully, passed. This is what the dust settling looks like."),
        ("Data-driven decision making.",
         "The corrective was necessary. Gut instinct was overrated; data was underused. "
         "The correction was right. Then the correction became the religion. Organisations "
         "that could not approve a budget without a dashboard. Metric gaming. The "
         "confusion of correlation with insight. This is the elevation-replaces-judgment "
         "failure mode: the tool stopped being a corrective and became the "
         "decision-making process itself."),
        ("JIRA and tooling as methodology.",
         "The project management tool becomes the project management methodology. The "
         "tool determines the work structure, the priority-setting process, the progress "
         "reporting cadence. The tail wags the dog. This is perhaps the most widely "
         "experienced example in this series\u2019 audience: the operations director who "
         "has attended fourteen Jira refinement ceremonies for a project that needed "
         "three conversations and a spreadsheet. Immediately recognisable. Ongoing."),
        ("AI and machine learning.",
         "The term \u2018AI-powered\u2019 has become a marketing claim so widely applied that "
         "it has ceased to carry information. This is the characteristic end-state of a "
         "tool elevated to a philosophy: it is everywhere, it means everything, and "
         "therefore it means nothing. The tool is genuinely transformationally powerful "
         "for the tasks it is designed for. The elevation is happening now. The dust "
         "has not settled. Which means the choice of how to use it \u2014 as a tool with "
         "a defined scope, or as a methodology with a governance committee \u2014 "
         "is still available."),
    ]
    for label, body in tools:
        items.append(Paragraph(f"<b>{label}</b>", S['failure_label']))
        items.append(Paragraph(body, S['body_j']))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("3. On AI Specifically"))
    items.append(GreenRule(sa=6))
    for para in [
        "It is worth being direct about AI, because the current moment makes "
        "indirectness dishonest.",
        "AI is a powerful tool. The capabilities are real: pattern recognition at "
        "scale, anomaly detection, systematic optimisation across large parameter "
        "spaces. For these tasks \u2014 tasks where the problem is defined, the data is "
        "available, and the output can be evaluated objectively \u2014 AI performs at a "
        "level that human analysts cannot match consistently over volume and time. "
        "This should not be hedged. The tool is real.",
        "It is also the wrong tool \u2014 not merely imperfect, but genuinely unsuited "
        "\u2014 for tasks that require contextual judgment, accountability, relationship "
        "management, and regulatory interpretation. These are not tasks that decompose "
        "into pattern-recognition problems without losing the thing that makes them "
        "hard. The context is not incidental. It is the problem.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    items.append(NoteBox([Paragraph(
        "When we built our own portfolio management platform, we made these decisions "
        "explicitly before writing a line of code. Systematic methods \u2014 signal "
        "selection, portfolio optimisation, lot sizing \u2014 are pattern-recognition and "
        "calculation problems. They do not tire, do not carry last week\u2019s client "
        "conversation into this week\u2019s analysis, and produce a complete audit trail. "
        "We used them. Client judgment, mandate interpretation, relationship management, "
        "and the recognition that something has changed that the data hasn\u2019t yet "
        "captured \u2014 these are not pattern-recognition problems. We did not use "
        "systematic methods there. The platform works because the boundary was "
        "drawn first.", S['note_text'])]))
    items.append(Spacer(1, 8))
    items.append(Paragraph(
        "The AI implementations that fail share one characteristic: the boundary was "
        "not drawn. The tool was deployed because it was available, and because "
        "deploying it looked like innovation. The question of whether it was the right "
        "tool for this specific task was not asked, or was asked and answered by the "
        "people selling the tool.", S['body_j']))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("4. Using Tools as Tools"))
    items.append(GreenRule(sa=6))
    for para in [
        "A tool used correctly has a defined scope: the tasks it performs, and the "
        "tasks it does not. This is not a limitation. It is the condition of the "
        "tool\u2019s usefulness. A Swiss Army knife asked to repair a circuit board is "
        "not a bad Swiss Army knife. It is the wrong tool for that task.",
        "The question for any tool is not \u2018is this capable?\u2019 but \u2018is this suited?\u2019 "
        "Capability is necessary but not sufficient. A capable tool applied to the "
        "wrong problem produces the wrong result efficiently, at scale, and with the "
        "confidence of a methodology behind it.",
        "Three questions before deploying any tool as a methodology:",
    ]:
        items.append(Paragraph(para, S['body_j']))
    for text in [
        "<b>One.</b> For what specific tasks is this tool the best available option? "
        "Name them precisely.",
        "<b>Two.</b> For what tasks is this tool being proposed that it was not "
        "designed for?",
    ]:
        items.append(Paragraph(text, S['body_j']))

    items.append(NoteBox([Paragraph(
        "<b>Three.</b> Who benefits from the deployment of this tool as a methodology "
        "\u2014 and is their benefit aligned with the quality of the outcome? This is the "
        "question that explains most of the elevation events described above. It is "
        "also the question that is almost never asked in the room where the deployment "
        "decision is made.", S['note_text'])]))
    items.append(Spacer(1, 12))

    # ReferenceCallout — inline implementation: grey rule above, italic 9pt grey
    items.append(HRFlowable(width="100%", thickness=0.5,
                             color=RULE_GREY, spaceAfter=6, spaceBefore=8))
    ref_style = ParagraphStyle('ref_callout', fontName=F_REG_I, fontSize=9,
                                leading=13, textColor=GREY_TEXT, spaceAfter=0)
    items.append(Paragraph(
        "If you\u2019d like to read how we applied this in practice: "
        "contact@investpuppy.com \u00b7 Vektor Research Series \u2014 \u2018AI as Instrument: "
        "Machine Learning in Systematic Portfolio Management\u2019 "
        "(IP-WP-AIML-260501-1.0) \u2014 investpuppy.com",
        ref_style))
    items.append(Spacer(1, 14))

    items.append(HRFlowable(width="100%", thickness=0.75, color=RULE_GREY,
                             spaceAfter=10))
    items.append(Paragraph("Pick it up. Use it for what it does.", S['closing']))
    items.append(Paragraph("Put it down.", S['closing_green']))
    return items

if __name__ == '__main__':
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build_document(OUT, TITLE, REF, PHOTO, NUM,
                   preface_story(), content_story(), photo_path=IMG)
