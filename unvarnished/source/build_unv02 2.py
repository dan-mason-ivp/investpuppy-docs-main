"""IP-UNV-02: Nobody owns it! — v4"""
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from unvarnished_builder import *

REF   = "IP-UNV-02  ·  May 2026"
TITLE = "Nobody owns it!"
PHOTO = ("Two uncapped fountain pens resting on a Consulting Services Agreement. "
         "One pen toward the signature line, one pointing away. Unsigned.")
NUM   = 2
OUT   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "output", "ip-unv-02-nobody-owns-it.pdf")
IMG   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "..", "_shared", "cover-photos", "unv02_cover_photo.jpg")

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
    items = [Spacer(1,10)]

    # ── Opening Q&A — bold, centred, spaced statement ─────────────────────────
    for line in [
        "Ask a vendor who owns the implementation.",
        "They will say the client.",
    ]:
        items.append(Paragraph(line, S['qa_line']))
    items.append(Spacer(1,6))
    for line in [
        "Ask the client.",
        "They will say the vendor.",
    ]:
        items.append(Paragraph(line, S['qa_line']))
    items.append(Spacer(1,4))

    # Spaced statement — bold, green, double space above/below
    items.append(Paragraph("Both are right. That is the problem.",
                            S['spaced_statement']))

    items.append(HRFlowable(width="100%",thickness=0.5,
                             color=RULE_GREY,spaceAfter=12,spaceBefore=0))

    # Section 1
    items.append(SectionHeader("1. How It Looks From The Inside"))
    items.append(GreenRule(sa=6))
    for para in [
        "At signing, the ownership question does not feel like a question. The "
        "vendor has a delivery methodology. The client has a project sponsor. "
        "The contract specifies deliverables and timelines. There is a project plan. "
        "There are weekly status meetings. There is, on paper, a clear structure.",
        "By week six, the ownership question has become the only question that "
        "matters. The decision that needed to be made last week has not been made. "
        "The sign-off that would unlock the next phase of configuration has not "
        "arrived. The escalation path that was supposed to resolve the integration "
        "question leads to someone who leads to someone else who is waiting for "
        "clarity from the vendor.",
        "Nobody planned for this. Nobody needed to. The ownership vacuum assembles "
        "itself from the normal operation of both parties\u2019 incentives, without a "
        "single bad decision being made by anyone.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    # Section 2
    items.append(Spacer(1,6))
    items.append(SectionHeader("2. The Blame Architecture"))
    items.append(GreenRule(sa=6))

    items.append(Paragraph(
        "The blame architecture assembles itself before the project begins. It is "
        "constructed from two perfectly rational decisions made independently by "
        "two parties who would both say they want the project to succeed.",
        S['body_j']))

    items.append(Paragraph(
        "The vendor does not assign a named individual with authority over the "
        "implementation outcome. The vendor assigns a project manager with authority "
        "over the vendor\u2019s deliverables. These are not the same thing. The first "
        "requires the authority to resolve issues on the client side. The second "
        "requires no such authority and does not claim it.", S['body_j']))

    items.append(Paragraph(
        "The client does not assign a named individual with authority over the "
        "implementation outcome. The client assigns a project sponsor with authority "
        "to sign off on milestones. These are not the same thing. The first requires "
        "the authority to make workflow decisions, resolve internal conflicts, and "
        "commit the practice\u2019s operating model to the new system. The second "
        "requires the authority to attend steering committee meetings and report upward.",
        S['body_j']))

    items.append(Paragraph(
        "The gap between these two arrangements is where implementations fail.",
        S['body_j']))

    items.append(Spacer(1,10))

    # ── Elevated blockquote — the locked core passage ─────────────────────────
    bq_body = [
        Paragraph("Ask a vendor who owns the implementation. They will say the client. "
                  "Ask the client. They will say the vendor.", S['bq_body']),
        Paragraph("Both are right. That is the problem.", S['bq_body']),
        Paragraph("Vendors train their sales teams to build relationships, not "
                  "accountability structures. Clients promote the people who don\u2019t "
                  "own things that fail. Nobody planned this. Nobody needed to.",
                  S['bq_body']),
        Paragraph("When things go wrong, the vacuum takes the blame. Not a planning "
                  "failure. Not a communication failure. A rational response to a "
                  "rational incentive \u2014 from both sides, without a word spoken.",
                  S['bq_body']),
    ]
    bq_close = Paragraph("The project belongs to no one.", S['bq_close'])
    items.append(ElevatedBlockquote(bq_body, bq_close))
    items.append(Spacer(1,10))

    # Dan's key insight — NoteBox
    items.append(NoteBox([Paragraph(
        "The deliberate ambiguity of ownership is often not accidental. It is "
        "a conscious \u2014 if unspoken \u2014 strategy from both sides to ensure that "
        "when things go wrong, the accountability cannot be cleanly located. "
        "The warmth of the sales relationship is not just a commercial mechanism. "
        "It is the specific instrument by which the accountability question is made "
        "too uncomfortable to ask at signing. By the time it needs to be asked, "
        "the relationship is too important to risk with the answer.",
        S['note_text'])]))
    items.append(Spacer(1,8))

    # Section 3
    items.append(SectionHeader("3. The Regulatory Dimension"))
    items.append(GreenRule(sa=6))
    for para in [
        "In a regulated financial services context, unclear implementation ownership "
        "is not merely an operational inconvenience. It is a compliance exposure.",
        "The audit trail for a financial software implementation \u2014 who approved what, "
        "when, and on what basis \u2014 is not a document that can be reconstructed after "
        "the fact. It requires clear ownership at every stage. When the question of "
        "who approved the go-live decision, who signed off on the integration testing, "
        "and who validated the output of the first live allocation cannot be answered "
        "clearly, the audit trail does not simply have gaps. It has the specific kind "
        "of gaps that compliance officers and regulators are trained to find.",
        "Unclear implementation ownership, in a regulated environment, is a risk "
        "that is rarely priced into the project at signing.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    # Section 4
    items.append(Spacer(1,6))
    items.append(SectionHeader("4. What Ownership Actually Looks Like"))
    items.append(GreenRule(sa=6))
    items.append(Paragraph(
        "Ownership is not a title on an org chart. It is not the name of the person "
        "who attended the kick-off meeting. It is the answer to a specific question: "
        "who has the authority and the accountability to make this implementation "
        "succeed, and who will bear the consequences if it does not?", S['body_j']))
    items.append(Paragraph(
        "Three things need to be true before configuration begins.", S['body']))
    for text in [
        "<b>One.</b> A named individual on the client side has the authority to make "
        "workflow decisions without referral upward. Not to report to someone who "
        "will make those decisions. To make them.",
        "<b>Two.</b> A named individual on the vendor side has the authority to commit "
        "the vendor\u2019s resources to resolving issues that arise during implementation. "
        "Not to escalate to someone who has that authority. To exercise it directly.",
        "<b>Three.</b> Both individuals have agreed, explicitly, on what success looks "
        "like \u2014 not in commercial terms, but in operational terms. The specific "
        "workflow. The specific outputs. The specific moment at which both parties "
        "will agree that the implementation is complete.",
    ]:
        items.append(Paragraph(text, S['body_j']))
    items.append(Paragraph(
        "These three things are rarely established at signing. They are almost never "
        "established in the contract. They require a conversation that the warmth of "
        "the sales relationship makes awkward and the pressure of the project "
        "timeline makes easy to defer.", S['body_j']))

    # Closing
    items.append(Spacer(1,14))
    items.append(HRFlowable(width="100%",thickness=0.75,
                             color=RULE_GREY,spaceAfter=10))
    items.append(Paragraph(
        "Own it. Before the configuration begins. Before the relationship makes "
        "it uncomfortable to ask.", S['closing']))
    items.append(Paragraph("Before week six.", S['closing_green']))

    return items

if __name__=='__main__':
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build_document(OUT,TITLE,REF,PHOTO,NUM,
                   preface_story(),content_story(),photo_path=IMG)
