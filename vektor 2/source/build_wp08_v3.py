"""WP-08: AI as Instrument — corrected rebuild."""
import sys; sys.path.insert(0,'/home/claude')
from wp_builder_v3 import *
from reportlab.platypus import PageBreak, NextPageTemplate

OUT='/home/claude/investpuppy/vektor/output/pdf/vk5-wp08-ai-ml-philosophy.pdf'
SUBTITLE='AI & Machine Learning Philosophy'
REF='IP-WP-AIML-260501-1.0'

def build():
    draw_cover=make_cover_fn(
        ['AI as Instrument:','Machine Learning in','Systematic Portfolio Management'],
        ['Where machine learning is used in Vektor, where it is not, why those',
         'boundaries exist, and how human judgement is preserved at every gate.'],
        'For institutional investors, compliance officers, and risk committees',REF)
    draw_page=make_page_fn(SUBTITLE)
    doc,f_cov,f_fst,f_lat=make_doc(OUT,SUBTITLE)
    doc.addPageTemplates([
        PageTemplate(id='Cover',frames=[f_cov],onPage=draw_cover),
        PageTemplate(id='Later',frames=[f_lat],onPage=draw_page),
    ])
    s=make_styles()
    story=[sp(1),NextPageTemplate('Later'),PageBreak()]

    story+=[p('ABSTRACT',s['tag']),
    NoteBox(COL_W,
        "The term 'AI-powered' has become a marketing claim so widely applied that it has ceased to carry "
        "information. This paper takes the opposite approach: it states precisely where machine learning is "
        "used in the Vektor platform, what it does at each point, and where it is explicitly not used. The "
        "governing principle is simple: AI in Vektor is an instrument of computation, not a maker of decisions. "
        "Every investment decision requires explicit human action. This governance framework is consistent with "
        "the AI governance principles published by financial regulators in Singapore (MAS FEAT), Hong Kong "
        "(SFC/HKMA), and the United Kingdom (FCA/PRA) \u2014 three jurisdictions that have independently "
        "converged on the same four requirements.",s['body']),sp(10),
    key_takeaways_box([
        'ML is used in two bounded roles: universe screening optimisation and XGBoost signal validation. Neither role makes investment decisions.',
        'XGBoost validates signals \u2014 it does not generate, approve, or act on them. A portfolio manager must approve the complete strategy before any position is taken.',
        'Human approval gates exist at every capital-at-risk stage: strategy approval, allocation execution, and cash funding are explicit human actions that cannot be automated away.',
        'Every model is trained on explicit historical data, produces an interpretable confidence score, and can be inspected, versioned, and rolled back. No black boxes.',
        'MAS FEAT (Singapore), SFC/HKMA (Hong Kong), and FCA/PRA (UK) all converge on the same four requirements: explainability, human oversight, accountability, and auditability. Vektor\u2019s framework aligns with all four across all three jurisdictions.',
    ],s),sp(10),
    p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {REF}  \u00b7  Copyright 2026 InvestPuppy',s['wp_ref']),
    PageBreak(),sp(0),
    p('1. THE GOVERNING PRINCIPLE',s['wp_section']),hrm(),
    p('One sentence. Every other decision follows from it.',s['body_grey']),
    NoteBox(COL_W,
        'AI in Vektor is an instrument of computation. It does not make investment decisions, client decisions, '
        'or compliance decisions. Humans make those decisions \u2014 every time, at every gate, with full information.',
        s['body']),sp(8),
    p('This principle was the starting position of the design process, not a response to regulatory pressure. The question asked at the outset: where does machine learning outperform human analysis on a clearly defined, measurable task \u2014 and where does human judgement remain essential? The boundary between those two categories is structural. It cannot be toggled in configuration.',s['body']),
    p('2. WHERE MACHINE LEARNING IS USED',s['wp_section']),hrm(),
    p('Two specific, bounded applications \u2014 defined input, defined output, defined role in the workflow.',s['body_grey']),
    p('APPLICATION 1 \u2014 UNIVERSE SCREENING (RESEARCH ENVIRONMENT)',s['wp_sub']),
    p('Statistical analysis in the SageMaker JupyterLab environment reduces an exchange universe of 500+ instruments to a target portfolio size, applying liquidity, sector, and dividend continuity criteria.',s['body']),
    p('What it does',s['wp_sub']),
    p('Ranks instruments against explicit screening parameters. Every criterion is stated: minimum average daily volume, sector membership, dividend continuity threshold. The reason any instrument is included or excluded can be stated precisely.',s['body']),
    p('What it does not do',s['wp_sub']),
    p('It does not select the final portfolio. The screened universe is the input to portfolio optimisation \u2014 a human analyst reviews the screening output before the optimisation runs.',s['body']),
    p('APPLICATION 2 \u2014 XGBOOST SIGNAL VALIDATION (PRODUCTION INFERENCE)',s['wp_sub']),
    p('The XGBoost classification model validates live trading signals before they are presented to the portfolio manager for approval.',s['body']),
    p('Training data',s['wp_sub']),
    p('Three years of daily OHLCV price history and historical signal outcomes.',s['body']),
    p('What it does',s['wp_sub']),
    p('Outputs a confidence score per signal. Signals below the configured threshold are flagged and filtered from the strategy record before PM review.',s['body']),
    p('What it does not do',s['wp_sub']),
    p('It does not approve strategies, execute trades, assign clients, or make any capital-affecting decision. Its output is one input to the PM review.',s['body']),
    p('Model management',s['wp_sub']),
    p('Trained, versioned, and deployed via SageMaker. Each version stored as an artefact in S3. Deployment requires an explicit promotion step \u2014 not automatic replacement. Rollback is a single operation.',s['body']),
    p('Transparency',s['wp_sub']),
    p('Confidence threshold is a configurable, visible parameter. Training data window and feature set are documented. Validation result \u2014 confidence score and pass/fail \u2014 stored in the strategy record and visible to PM at review.',s['body']),
    ]

    # XGBoost visual evidence
    import os as _xos, sys as _xs
    _SC2 = '/home/claude/investpuppy/vektor/source/screenshots'
    from reportlab.platypus import Image as _RLI2
    from reportlab.lib.utils import ImageReader as _IRI2
    for _sc_file, _caption in [
        ('sc13_xgboost_setup.png',
         'XGBoost Price Direction Prediction \u2014 the 11 features used by ml_validator.py at inference. '
         'Same feature set at training and inference ensures no train-serve skew. Model: SageMaker XGBoost.'),
        ('sc14_xgboost_test.png',
         'ML Validation test output \u2014 BUY on BS6 produces WEAK_BUY (ml_direction=UP, confidence=LOW, agreement=YES). '
         'SELL produces WEAK_SELL (agreement=NO). Full JSON output stored in strategy record.'),
    ]:
        _p2 = _xos.path.join(_SC2, _sc_file)
        try:
            _ir2 = _IRI2(_p2); _iw2, _ih2 = _ir2.getSize()
            _w2 = COL_W; _h2 = _w2 * _ih2 / _iw2
            story.append(p('PLATFORM EVIDENCE', s['wp_sub']))
            story.append(_RLI2(_p2, width=_w2, height=_h2))
            story.append(sp(4))
            story.append(p(_caption, s['body_grey']))
            story.append(sp(8))
        except Exception as _e2:
            print(f'Screenshot {_sc_file}: {_e2}')

    story += [
        PageBreak(),sp(0),
        p('3. WHERE MACHINE LEARNING IS NOT USED',s['wp_section']),hrm(),
        p('Explicit exclusions \u2014 and the reasons behind each one.',s['body_grey']),
        p('Stating where machine learning is not used is as important as stating where it is. The following exclusions are design decisions that will not change as the platform develops.',s['body']),
    p('Investment decisions',s['wp_sub']),
    p('No model approves, rejects, or modifies a strategy. The portfolio manager approves the complete strategy before any client assignment. This approval is a human action, recorded with timestamp and user identity.',s['body']),
    p('Portfolio weight determination',s['wp_sub']),
    # CORRECTED: Monte Carlo simulation → portfolio configuration sampling
    p('Weights are produced by portfolio configuration sampling and efficient frontier optimisation via Modern Portfolio Theory \u2014 mathematical processes, not ML models. The max-Sharpe allocation is deterministic: same inputs, same output, explainable step by step.',s['body']),
    p('Client suitability',s['wp_sub']),
    p('Risk profiles are set and reviewed by portfolio managers. No model assesses whether a client is suitable for a given strategy.',s['body']),
    p('Compliance sign-off',s['wp_sub']),
    p('Every audit trail gate \u2014 strategy approval, cash funding, allocation execution \u2014 requires human action. These gates cannot be automated.',s['body']),
    p('Instrument selection',s['wp_sub']),
    p('Final instrument selection is a human decision made by the Stock Analyst from the screened universe. Screening reduces the universe; it does not select the portfolio.',s['body']),
    p('4. THE BLACK BOX QUESTION',s['wp_section']),hrm(),
    p('Addressed directly \u2014 because it is the right question to ask.',s['body_grey']),
    NoteBox(COL_W,
        '\u201cIs Vektor a black box?\u201d \u2014 No. Here is the precise answer.',s['pull']),sp(8),
    p('Strategy record transparency',s['wp_sub']),
    p('For every instrument in every strategy, a PM can inspect: which indicator was assigned, what parameters were optimised, the backtest Sharpe ratio, and whether XGBoost validation passed or filtered the signal.',s['body']),
    p('Model output visibility',s['wp_sub']),
    p('Confidence score and pass/fail classification stored in the strategy record. PM sees which signals passed and which were filtered.',s['body']),
    p('Allocation transparency',s['wp_sub']),
    p('Complete breakdown: instrument, target weight, live price, lot-rounded quantity, target value, efficiency figure. Nothing summarised.',s['body']),
    p('Audit trail completeness',s['wp_sub']),
    p('Every action logged with timestamp and user or service identity. Complete chain from model inference to trade-ready position is retrievable.',s['body']),
    PageBreak(),sp(0),
    p('5. HUMAN APPROVAL GATES',s['wp_section']),hrm(),
    p('Every point in the workflow where human action is required before capital can move.',s['body_grey']),
]
    gate_rows=[
            [p('GATE',s['tbl_hdr']),p('ROLE',s['tbl_hdr']),p('WHAT IS REQUIRED',s['tbl_hdr'])],
            [p('Strategy approval',s['tbl_gold']),p('Portfolio Manager',s['tbl_body']),
             p('PM reviews all instruments, weights, indicators, and XGBoost validation results. Explicit approval action required. No strategy can be assigned to a client before this record exists.',s['tbl_body'])],
            [p('Client assignment',s['tbl_body']),p('Portfolio Manager',s['tbl_body']),
             p('PM creates client profile and assigns the approved strategy. Separate explicit action from strategy approval.',s['tbl_body'])],
            [p('Allocation execution',s['tbl_body']),p('Portfolio Manager',s['tbl_body']),
             p('PM reviews full breakdown (symbols, quantities, prices, efficiency) and confirms. Cannot proceed without explicit PM confirmation.',s['tbl_body'])],
            [p('Cash funding',s['tbl_body']),p('Operations',s['tbl_body']),
             p('Operations records wire transfer with currency, amount, and reference. Operations cannot approve strategies or initiate allocations \u2014 structurally separated from the investment decision chain.',s['tbl_body'])],
            [p('Market order submission (post-approval)',s['tbl_body']),p('System',s['tbl_body']),
             p('SQS delivers orders to IBKR Gateway only after strategy approval and cash funding are complete. Executes only positions a human PM has already approved in full.',s['tbl_body'])],
        ]
    gt=Table(gate_rows,colWidths=[36*mm,30*mm,COL_W-66*mm],repeatRows=1,splitByRow=1)
    gt.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1A1A20')),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD_BG,colors.HexColor('#0F0F14')]),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
            ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_MIN),
            ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
            ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MIN),
            ('LINEAFTER',(1,0),(1,-1),0.3,RULE_MIN),
        ]))
    story.append(gt)
    story+=[PageBreak(),sp(0),
        p('6. MODEL GOVERNANCE',s['wp_section']),hrm(),
        p('How models are trained, deployed, monitored, and updated.',s['body_grey']),
        p('Model training',s['wp_sub']),
        p('XGBoost trained in SageMaker using three years of daily price history and historical signal outcomes. Training is triggered explicitly. Each run produces a versioned model artefact stored in S3.',s['body']),
        p('Model deployment',s['wp_sub']),
        p('Deployment to the inference endpoint requires an explicit promotion step. New version does not automatically replace the live model. Previous version available for immediate rollback.',s['body']),
        p('Drift detection',s['wp_sub']),
        p('Automated observability monitoring is on the near-term roadmap. Currently, model performance is reviewed when signal validation results appear anomalous. Formal drift detection will be implemented as part of the production observability work.',s['body']),
        p('Anomalous output response',s['wp_sub']),
        p('If the endpoint produces output outside the expected confidence range, the signal is flagged rather than passed or filtered. The PM sees the flag and decides. The model cannot produce an outcome that bypasses the PM review gate.',s['body']),
        p('Rollback',s['wp_sub']),
        p('Rollback to a previous version is a single SageMaker endpoint update. Previous artefact remains in S3. All versions retained.',s['body']),
        p('7. REGULATORY ALIGNMENT \u2014 THREE JURISDICTIONS',s['wp_section']),hrm(),
        p('How the Vektor AI governance framework relates to published regulatory guidance across Singapore, Hong Kong, and the United Kingdom.',s['body_grey']),
        NoteBox(COL_W,
            'Three financial regulators \u2014 MAS (Singapore), SFC/HKMA (Hong Kong), and FCA/PRA (United Kingdom) '
            '\u2014 have independently published guidance on responsible AI use in financial services. Despite different '
            'regulatory traditions and market contexts, all three converge on the same four requirements: '
            '(1)\u00a0explainability of AI outputs, (2)\u00a0human oversight at decision points, '
            '(3)\u00a0clear accountability for AI-assisted decisions, and (4)\u00a0the ability to audit and review AI '
            'behaviour. The Vektor governance framework was designed against these shared first principles \u2014 not '
            'against any single jurisdiction\u2019s specific rules. This makes it durable as regulation evolves and '
            'portable across markets.',s['body']),sp(10),
        p('VEKTOR\u2019S ALIGNMENT WITH THE FOUR SHARED REQUIREMENTS',s['wp_sub']),
        p('1. Explainability',s['wp_sub']),
        p('Regulatory requirement: AI outputs must be explainable and interpretable.',s['body_grey']),
        p('Vektor alignment: The XGBoost model produces a confidence score and pass/fail for each signal \u2014 both stored in the strategy record and visible to the PM. Training data window, feature set, and threshold are documented. A compliance reviewer can trace any signal back to the model version, training data, and confidence score that produced it.',s['body']),
        p('2. Human oversight',s['wp_sub']),
        p('Regulatory requirement: Human oversight must be maintained at AI-influenced decision points.',s['body_grey']),
        p('Vektor alignment: Human approval gates exist at every capital-at-risk stage. Strategy approval, allocation execution, and cash funding are explicit human actions. The XGBoost output is an input to the PM review, not a substitute for it.',s['body']),
        p('3. Accountability',s['wp_sub']),
        p('Regulatory requirement: Clear responsibility must exist for AI-assisted decisions.',s['body_grey']),
        p('Vektor alignment: Every AI output is attributable to a specific model version, training dataset, and inference request. Every investment decision that follows is attributable to a specific human \u2014 PM identity, timestamp, action \u2014 in the audit log.',s['body']),
        p('4. Auditability',s['wp_sub']),
        p('Regulatory requirement: AI behaviour must be auditable and reviewable.',s['body_grey']),
        p('Vektor alignment: Every model call, signal validation result, strategy approval, and allocation is logged with timestamp and identity. The complete chain from inference to trade-ready position is retrievable at any point.',s['body']),
        PageBreak(),sp(0),
        p('JURISDICTIONAL REFERENCES',s['wp_sub']),
        p('Singapore \u2014 MAS',s['wp_sub']),
        p('\u2014 MAS FEAT Principles (Fairness, Ethics, Accountability, Transparency) \u2014 Veritas initiative, 2019 onwards',s['bullet']),
        p('\u2014 MAS Guidelines on the Use of Artificial Intelligence and Data Analytics in Financial Services',s['bullet']),
        p('The MAS FEAT framework is the most developed AI governance framework in the ASEAN region. Its four principles map directly to Vektor\u2019s governance design. MAS\u2019s Veritas initiative provides implementation guidance for financial services firms seeking to operationalise FEAT.',s['body']),
        p('Hong Kong \u2014 SFC / HKMA',s['wp_sub']),
        p('\u2014 SFC Circular on Algorithmic Trading \u2014 March 2018 (reinforced in subsequent guidance)',s['bullet']),
        p('\u2014 HKMA Supervisory Policy Manual TM-G-1 \u2014 Technology Risk Management: explainability and human oversight of automated systems',s['bullet']),
        p("The SFC's algorithmic trading circular requires that automated trading systems have appropriate governance, testing, and human oversight before deployment. HKMA TM-G-1 addresses technology risk management and specifically requires explainability and human oversight of automated systems \u2014 directly relevant to XGBoost signal validation. Vektor\u2019s documented model governance and human approval gates are consistent with both frameworks.",s['body']),
        p('United Kingdom \u2014 FCA / PRA',s['wp_sub']),
        p('\u2014 PRA Supervisory Statement SS1/23 \u2014 Model Risk Management Principles (supervisory expectation, not advisory guidance)',s['bullet']),
        p('\u2014 FCA DP5/22 \u2014 Artificial Intelligence and Machine Learning (discussion paper indicating regulatory direction)',s['bullet']),
        p("PRA SS1/23 is the most directly applicable document \u2014 it is supervisory expectation, not advisory guidance, and requires model explainability, governance, and the ability to intervene in automated processes. The FCA's DP5/22 signals the direction of future binding rules. Vektor's framework \u2014 documented model versions, explicit promotion steps, rollback capability, and human approval at every investment gate \u2014 is consistent with SS1/23 expectations.",s['body']),
        NoteBox(COL_W,
            'The regulatory landscape for AI in financial services is evolving rapidly across all three jurisdictions. '
            'The Vektor governance framework is designed to be durable \u2014 anchored to the shared first principles '
            'that regulators are converging on, not tied to any single jurisdiction\u2019s current rules. Regulatory '
            'standing note: Vektor is a portfolio construction platform. Regulatory status and applicable permissions '
            'vary by jurisdiction and use case. Full details are available to Proof Partners on request.',
            s['body']),
        PageBreak(),sp(0),
        p('8. AI CAPABILITY ROADMAP',s['wp_section']),hrm(),
        p('Future ML applications under consideration \u2014 each evaluated against the same governing principle.',s['body_grey']),
        p('Each future capability will be evaluated against the same question: does it perform a computation task better than human analysis, without displacing a human decision that carries accountability?',s['body']),
        p('Formal walk-forward validation',s['wp_sub']),
        p('Out-of-sample validation of XGBoost model against live performance data. Directly addresses the overfitting risk acknowledged in WP-04.',s['body']),
        p('Automated drift detection',s['wp_sub']),
        p('CloudWatch-based monitoring of XGBoost inference quality, triggering alerts when patterns diverge from historical norms. Output: alert to a human reviewer \u2014 not automatic model retraining.',s['body']),
        p('Enhanced signal universe',s['wp_sub']),
        p('Evaluation of additional technical indicators or alternative data sources. Any new signal type goes through the same grid search and XGBoost validation before inclusion in production strategies.',s['body']),
        p('Rebalancing trigger detection',s['wp_sub']),
        p('ML-assisted identification of when positions have drifted materially from target weights. Output: a rebalancing recommendation to the PM \u2014 not an automatic trade.',s['body']),
        p('9. CONCLUSION',s['wp_section']),hrm(),
        p('The governing framework does not change as the technology develops \u2014 the technology is evaluated against the framework.',s['body_grey']),
        p('AI is used in Vektor where it outperforms human analysis on a well-defined, measurable task. It is not used where the decision carries accountability and requires contextual judgement. This boundary is structural \u2014 enforced by the platform\u2019s workflow architecture, not by a policy that could be overridden.',s['body']),
        p('The governance framework described in this paper aligns with the shared principles that financial regulators in Singapore, Hong Kong, and the United Kingdom have independently arrived at. That convergence is not coincidence \u2014 it reflects a shared view that AI in financial services must augment human judgement, not replace it. Vektor was built on that view from the start.',s['body']),
        ]
    closing_row(
        'For technical infrastructure supporting ML deployment, see WP-07. For compliance and audit trail architecture, see WP-06. For signal optimisation methodology, see WP-02. All documents at investpuppy.com.',
        REF,s,story)
    doc.build(story)
    print(f'Built: {OUT}')
    import subprocess
    r=subprocess.run(['pdfinfo',OUT],capture_output=True,text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l: print(l)

if __name__=='__main__': build()
