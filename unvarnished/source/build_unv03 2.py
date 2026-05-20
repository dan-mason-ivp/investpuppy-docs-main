"""IP-UNV-03: Complexity as cover: The consultant layer"""
import sys, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from unvarnished_builder import *

REF   = "IP-UNV-03  \u00b7  2026"
TITLE = "Complexity as cover: The consultant layer"
PHOTO = "Multiple consulting firm business cards fanned on a desk beside a confidential acquisition integration plan document."
NUM   = 3
OUT   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "output", "ip-unv-03-complexity-as-cover.pdf")
IMG   = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "..", "_shared", "cover-photos", "unv03_cover_photo.jpg")
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
        "The consultant\u2019s primary product is not advice. It is a document. "
        "The document exists to justify the advice, to evidence the engagement, "
        "and to ensure that when the project fails, the advice was correctly recorded. "
        "The document does not make the project succeed. It makes the failure legible.",
        S['note_text'])]))
    items.append(Spacer(1, 14))

    items.append(SectionHeader("1. The Structure of the Relationship"))
    items.append(GreenRule(sa=6))
    for para in [
        "There is nothing dishonest about the consulting relationship as it is typically "
        "structured. The vendor sells software. The client buys software. Between them, "
        "one or more consulting firms are engaged to manage the implementation. The "
        "consulting firms charge by the day. This is where the incentive problem begins "
        "\u2014 not with bad faith, but with arithmetic.",
        "A ten-week implementation produces one invoice. A twenty-week implementation "
        "produces two. The consulting firm does not plan for the project to extend. "
        "It does not need to. The conditions that produce extension are already present "
        "in the structure of the engagement: an underdefined specification, a client "
        "who cannot evaluate what they are being told, and a project plan built before "
        "anyone understood the workflow it was meant to describe.",
        "Nobody produced these conditions deliberately. Nobody needed to. The incentive "
        "structure produced them automatically.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    items.append(NoteBox([Paragraph(
        "The question is not whether the consultant wants the project to succeed. "
        "Most do. The question is whether the conditions under which they are paid "
        "require the project to succeed. They do not. They require the project to continue.",
        S['note_text'])]))
    items.append(Spacer(1, 12))

    items.append(SectionHeader("2. When There Is More Than One Firm"))
    items.append(GreenRule(sa=6))
    for para in [
        "The single-firm engagement is the idealised case. The real case is more "
        "complicated: a systems integrator managing the technical implementation, "
        "a strategy firm that scoped the transformation, and a change management "
        "practice running the adoption programme. Three firms, three commercial "
        "relationships, three sets of incentives \u2014 none of which are aligned with "
        "each other, and none of which are fully transparent to the client.",
        "Each firm is protecting its relationship, its intellectual property, and its "
        "position for the next engagement. The systems integrator wants a clean "
        "technical handoff, regardless of whether the business is operationally ready "
        "to receive it. The strategy firm that designed the target operating model has "
        "a vested interest in the architecture remaining complex enough to require "
        "ongoing advisory. The change management practice is incentivised to run "
        "programmes, not to produce adoption.",
        "When something goes wrong in a multi-firm engagement, each firm\u2019s first "
        "move is to locate responsibility in another firm\u2019s workstream. The client "
        "watches three parties explain why it is someone else\u2019s fault while the "
        "project continues to fail. The blame routes between firms in a way that is "
        "entirely invisible to the client and produces a specific result: nobody is "
        "accountable for the outcome, only for their workstream. The project belongs "
        "to all of them. Which is to say, it belongs to none of them.",
    ]:
        items.append(Paragraph(para, S['body_j']))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("3. Complexity as a Product"))
    items.append(GreenRule(sa=6))
    for para in [
        "Complexity is not an inevitable feature of financial software implementations. "
        "It is, in many cases, a product \u2014 produced and maintained by the parties "
        "who benefit from its existence.",
        "A complex project plan requires a project manager. A complex integration "
        "architecture requires a solutions architect. A complex change management "
        "workstream requires a change management consultant. None of these roles is "
        "unnecessary in the abstract. All of them become necessary once the project "
        "has been structured to require them.",
        "The consultant who simplifies is the consultant who reduces their own "
        "engagement. This is not a character flaw. It is a rational response to a "
        "rational incentive. The implementation that could have been delivered in "
        "eight weeks with three people becomes the implementation delivered in "
        "twenty-four weeks with nine, because the specification was constructed in "
        "a way that made the longer engagement the only legible path.",
        "The client, who cannot evaluate the specification independently, accepts it. "
        "The project begins.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    items.append(NoteBox([Paragraph(
        "No practitioner, managing live client portfolios while attending project "
        "workshops, has ever thought: what would really help now is a few more cleverly "
        "constructed slides. They need a working system, configured for how they "
        "actually operate. The consultant\u2019s deliverables are not designed to produce "
        "that. They are designed to evidence the engagement.", S['note_text'])]))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("4. The Legibility Problem"))
    items.append(GreenRule(sa=6))
    for para in [
        "The client\u2019s inability to evaluate the specification is not stupidity. "
        "It is a structural feature of the market. Financial software is complex. "
        "The people who understand it in detail are, by definition, the people who "
        "have been working in it \u2014 which means the vendor and the consulting firms. "
        "The client is buying expertise they do not have. This is the correct reason "
        "to engage a consultant.",
        "The problem arises when the information asymmetry that justified the "
        "engagement is then used to extend it. The client cannot challenge a timeline "
        "they cannot evaluate. They cannot simplify an architecture they cannot read. "
        "They can ask whether it seems reasonable, and they will be told that it does.",
    ]:
        items.append(Paragraph(para, S['body_j']))

    bq_body = [
        Paragraph("The warmth of the consulting relationship is the mechanism by which "
            "this asymmetry is maintained. A trusted adviser is harder to challenge "
            "than a vendor. Asking whether the project could be simpler feels like "
            "asking whether the advice was good.", S['bq_body']),
        Paragraph("The relationship was built to prevent that question from being asked "
            "comfortably. In a multi-firm engagement, each relationship performs this "
            "function independently. Nobody designed it this way. Nobody needed to.",
            S['bq_body']),
    ]
    bq_close = Paragraph(
        "The complexity belongs to the engagement. Which means it belongs to no one.",
        S['bq_close'])
    items.append(ElevatedBlockquote(bq_body, bq_close))
    items.append(Spacer(1, 10))

    items.append(SectionHeader("5. What a Better Engagement Looks Like"))
    items.append(GreenRule(sa=6))
    items.append(Paragraph(
        "A consulting engagement structured around outcomes rather than duration looks "
        "different from the outside. The project plan is shorter. The workstreams are "
        "fewer. The specification is written in language the client can read and "
        "challenge. Milestones are tied to functional delivery, not document production. "
        "Where multiple firms are engaged, accountability for the outcome \u2014 not just "
        "the workstream \u2014 is assigned explicitly, at contract stage, before the "
        "relationship has been built and the complexity installed.",
        S['body_j']))
    items.append(Paragraph(
        "Three questions worth asking before the engagement begins:", S['body']))
    for text in [
        "<b>One.</b> Is the project plan written in language our operations team can "
        "evaluate without assistance?",
        "<b>Two.</b> Are the milestones defined by what the system does, or by what "
        "documents have been produced?",
        "<b>Three.</b> If we are engaging multiple firms, which single entity is "
        "accountable for the outcome \u2014 and what happens to their engagement if "
        "the outcome is not delivered?",
    ]:
        items.append(Paragraph(text, S['body_j']))

    items.append(Spacer(1, 14))
    items.append(HRFlowable(width="100%", thickness=0.75, color=RULE_GREY,
                             spaceAfter=10))
    items.append(Paragraph(
        "The consultant layer is not the problem. An engagement structure that rewards "
        "complexity and diffuses accountability is the problem.", S['closing']))
    items.append(Paragraph("They are not the same thing.", S['closing_green']))
    return items

if __name__ == '__main__':
    import os; os.makedirs(os.path.dirname(OUT), exist_ok=True)
    build_document(OUT, TITLE, REF, PHOTO, NUM,
                   preface_story(), content_story(), photo_path=IMG)
