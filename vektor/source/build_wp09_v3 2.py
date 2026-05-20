"""WP-09: Risk & Limitation Disclosure — corrected rebuild."""
import sys; sys.path.insert(0,'/home/claude')
from wp_builder_v3 import *
from reportlab.platypus import PageBreak, NextPageTemplate

OUT='/home/claude/investpuppy/vektor/output/pdf/vk5-wp09-risk-disclosure.pdf'
SUBTITLE='Risk & Limitation Disclosure'
REF='IP-WP-RISK-260501-1.0'

def build():
    draw_cover=make_cover_fn(
        ['Risk & Limitation','Disclosure'],
        ['A structured, honest analysis of the risks and limitations of the Vektor platform \u2014',
         'model risk, execution risk, data risk, and operational risk \u2014',
         'with the mitigations in place and those still on the roadmap.'],
        'For institutional due diligence teams, risk committees, and compliance officers',REF)
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
        'This paper does not exist to satisfy a legal requirement. It exists because institutional investors '
        'conducting due diligence should have a single, structured document that addresses platform risk '
        'directly \u2014 not distributed across white papers or buried in product documentation. The tone is '
        'the same as the rest of the Vektor research series: specific, honest, and free of hedging language '
        'that obscures rather than informs. Where a risk is real, this paper says so. Where a mitigation is '
        'partial, this paper says that too.',s['body']),sp(10),
    key_takeaways_box([
        'Four risk categories are addressed: model risk, execution risk, data risk, and operational risk. Each is assessed with mitigations in place and those still on the roadmap.',
        'The most significant risk at the current stage is model risk \u2014 specifically, the gap between backtest performance and live performance. This risk is acknowledged directly, with the structural mitigations the platform provides.',
        'Human approval gates at every capital-at-risk stage are the primary operational risk mitigation. These gates are structural \u2014 they cannot be bypassed in configuration.',
        'Several mitigations are on the roadmap rather than live today. This paper states which are complete and which are pending, with defined trigger conditions.',
        'Founding Mandate partners are invited to raise any risk not addressed here. The Founding Mandate is a partnership in which both parties are building toward the same outcome \u2014 a platform that performs as described, with the governance and controls that institutional management requires.',
    ],s),sp(10),
    p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {REF}  \u00b7  Copyright 2026 InvestPuppy',s['wp_ref']),
    PageBreak(),sp(0),
    p('1. HOW TO READ THIS DOCUMENT',s['wp_section']),hrm(),
    p('What this document is, what it is not, and how it relates to the rest of the Vektor research series.',s['body_grey']),
    p("This document is a practitioner's risk analysis \u2014 structured in the same format as any internal risk assessment a portfolio manager or compliance officer would produce when evaluating a new system. It identifies risks, assesses likelihood and impact, states mitigations in place, and is honest about where mitigations are still on the roadmap.",s['body']),
    p("It is not a legal disclaimer. It does not attempt to limit liability through exhaustive caveats. Readers seeking a legal risk disclosure should request the separate legal documentation available to Founding Mandate partners.",s['body']),
    NoteBox(COL_W,
        'The risks described in this paper are the risks of adopting a systematic portfolio management platform '
        'at an early stage of its development. They are not unique to Vektor \u2014 every systematic platform '
        'carries model risk, execution risk, data risk, and operational risk. What is specific to Vektor is how '
        'each risk is structured, mitigated, and disclosed.',s['body']),
    sp(10),
    p('2. RISK SUMMARY',s['wp_section']),hrm(),
    p('Fourteen identified risks across four categories. Likelihood and impact reflect the current stage of platform development.',s['body_grey']),
    ]

    # Risk summary table
    risk_rows=[
        [p('RISK AREA',s['tbl_hdr']),p('LIKELIHOOD',s['tbl_hdr']),p('IMPACT',s['tbl_hdr']),p('MITIGATION IN PLACE',s['tbl_hdr'])],
        [p('Backtest vs live gap',s['tbl_gold']),p('High',s['tbl_body']),p('High',s['tbl_body']),
         p('XGBoost validation on live signals. Walk-forward validation on roadmap. PM approval gate before any position is taken.',s['tbl_body'])],
        [p('Overfitting (signal parameters)',s['tbl_body']),p('Medium',s['tbl_body']),p('Medium',s['tbl_body']),
         p("Three-year look-back. Six-indicator grid search limits parameter space. Sharpe ratio as objective function. Disclosed in WP-04.",s['tbl_body'])],
        [p('Signal decay',s['tbl_body']),p('Medium',s['tbl_body']),p('Medium',s['tbl_body']),
         p('Indicators re-optimised per strategy build. Rebalancing trigger detection on roadmap. PM reviews signal performance at each approval.',s['tbl_body'])],
        [p('Model (XGBoost) drift',s['tbl_body']),p('Medium',s['tbl_body']),p('Medium',s['tbl_body']),
         p('Manual review when validation results appear anomalous. Automated drift detection on near-term roadmap.',s['tbl_body'])],
        [p('Concentration risk',s['tbl_body']),p('Medium',s['tbl_body']),p('High',s['tbl_body']),
         p('Correlation matrix verification at optimisation stage. Sector screening in universe reduction.',s['tbl_body'])],
        [p('IBKR connectivity failure',s['tbl_body']),p('Low',s['tbl_body']),p('Medium',s['tbl_body']),
         p('SQS queue decouples order generation from execution \u2014 orders queue, not fail. Reconnection resumes processing automatically.',s['tbl_body'])],
        [p('Simulation vs live gap',s['tbl_body']),p('Medium',s['tbl_body']),p('High',s['tbl_body']),
         p('Current IBKR connection is simulation account. Full order flow tested in simulation. Live execution before first Founding Mandate onboarding.',s['tbl_body'])],
        [p('Lot rounding / mandate size',s['tbl_body']),p('Low',s['tbl_body']),p('Low\u2013Med',s['tbl_body']),
         p('Cash buffer absorbs rounding residual. Recommended minimum mandate size SGD 100,000+ for a ten-instrument portfolio to maintain efficiency above 99%.',s['tbl_body'])],
        [p('Market liquidity',s['tbl_body']),p('Low',s['tbl_body']),p('High',s['tbl_body']),
         p('Minimum average daily volume threshold applied in universe screening.',s['tbl_body'])],
        [p('Market data outage',s['tbl_body']),p('Low',s['tbl_body']),p('Medium',s['tbl_body']),
         p('Three years of daily history maintained in RDS. Slack alert on download failure for manual intervention.',s['tbl_body'])],
        [p('Data quality (Yahoo Finance)',s['tbl_body']),p('Low',s['tbl_body']),p('Medium',s['tbl_body']),
         p('Quality checks on ingestion. Corporate action adjustments applied. Institutional data feed substitution available on request.',s['tbl_body'])],
        [p('FX rate accuracy',s['tbl_body']),p('Low',s['tbl_body']),p('Low',s['tbl_body']),
         p('Daily FX rates fetched and stored. Position-level conversion documented in WP-05. FX source configurable.',s['tbl_body'])],
        [p('Unauthorised action',s['tbl_body']),p('Low',s['tbl_body']),p('High',s['tbl_body']),
         p('Three-role model enforced at application layer. Infrastructure-level RBAC on next prototype roadmap. Full audit trail of every action.',s['tbl_body'])],
        [p('Platform unavailability',s['tbl_body']),p('Low',s['tbl_body']),p('High',s['tbl_body']),
         p('ECS on Fargate auto-restarts failed tasks. RDS automated backups. Production observability alerting on near-term roadmap.',s['tbl_body'])],
    ]
    cw=[40*mm,20*mm,18*mm,COL_W-78*mm]
    rt=Table(risk_rows,colWidths=cw,repeatRows=1,splitByRow=1)
    rt.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD_BG,colors.HexColor('#0F0F14')]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
        ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MIN),
        ('LINEAFTER',(1,0),(1,-1),0.3,RULE_MIN),
        ('LINEAFTER',(2,0),(2,-1),0.3,RULE_MIN),
    ]))
    story.append(rt)
    story+=[PageBreak(),sp(0),
    p('3. MODEL RISK',s['wp_section']),hrm(),
    p('The risk that model-generated signals do not perform in live conditions as they did in backtests.',s['body_grey']),
    p('THE BACKTEST TO LIVE GAP',s['wp_sub']),
    p('The most significant risk in any systematic strategy is the gap between backtest performance and live performance. Backtests are optimised on historical data. Live markets introduce conditions historical data may not have captured: regime changes, liquidity shifts, correlation breakdowns, and the market impact of the strategy itself.',s['body']),
    p("Vektor's structural response is the XGBoost signal validation layer: every signal is evaluated against current market conditions before it is presented to the portfolio manager. A signal that performed well in backtests but is assessed as low-confidence against current conditions is filtered before PM review. This does not eliminate the gap \u2014 no tool does. It reduces the probability that a historically strong signal is applied in a market context where it is unlikely to perform.",s['body']),
    NoteBox(COL_W,
        "The most important mitigation for model risk is structural, not technical. No Vektor strategy reaches a "
        "client portfolio without a portfolio manager reviewing the complete strategy and taking an explicit "
        "approval action. The PM's contextual judgement is the final filter that no backtest optimisation can replace.",
        s['body']),
    sp(8),
    p('Overfitting',s['wp_sub']),
    p('The grid search optimises technical indicator parameters against a three-year historical window. Optimised parameters may reflect historical noise rather than genuine signal. Mitigations: Sharpe ratio as objective function, six-indicator universe limiting parameter space, three-year window covering multiple market regimes. Formal walk-forward validation is on the near-term roadmap and will materially strengthen this mitigation.',s['body']),
    p('Signal decay',s['wp_sub']),
    p("Technical indicators lose predictive power as market conditions change. Vektor's response: parameters are re-optimised at each strategy build, not fixed at initial setup. Rebalancing trigger detection is on the roadmap. Current practice: PM reviews signal performance against current market conditions at each strategy approval.",s['body']),
    p('Model drift',s['wp_sub']),
    p('The XGBoost model is trained on historical signal outcomes. As market conditions change, classification accuracy may degrade. Current mitigation: manual review when results appear anomalous. Automated drift detection with CloudWatch alerting is on the near-term roadmap.',s['body']),
    p('Concentration risk',s['wp_sub']),
    # CORRECTED: Monte Carlo optimisation → Efficient frontier optimisation
    p('Efficient frontier optimisation may produce concentrated allocations in instruments with correlated historical performance. Mitigation: correlation matrix verification is a required optimisation step, flagging high pairwise correlation before PM approval. Sector diversification screening applied in universe reduction.',s['body']),
    p('4. EXECUTION RISK',s['wp_section']),hrm(),
    p('The risk that approved positions are not executed as intended.',s['body_grey']),
    p('Simulation vs live gap',s['wp_sub']),
    p('The IBKR Gateway is currently connected to the IBKR simulation account. Simulation mode does not fully replicate live execution: fills are assumed at the requested price without market impact, partial fills do not occur, and liquidity is not modelled. The full order flow is operational and tested in simulation. Live execution will be activated before the first Founding Mandate client is onboarded \u2014 this is a defined trigger condition, not an open-ended roadmap item.',s['body']),
    p('IBKR connectivity failure',s['wp_sub']),
    p('If the IBKR Gateway loses connectivity, the SQS queue buffers orders rather than failing them. Orders are processed when connectivity is restored. The queue architecture was specifically designed to handle this scenario \u2014 see the decision log in WP-07. Slack notification on order completion means a failure to complete is visible immediately.',s['body']),
    p('Lot rounding and minimum mandate size',s['wp_sub']),
    # CORRECTED: 99.9%+ → 99.94%+
    p('Share quantities must be whole numbers. The allocation calculation rounds down to the nearest lot size, producing a residual cash balance. At 99.94%+ efficiency in simulation testing, this residual is immaterial for typical mandate sizes. The practical minimum recommended mandate size for a ten-instrument SGX portfolio is SGD 100,000 \u2014 below this threshold, lot rounding effects become more pronounced and capital allocation efficiency may fall below 98%. This threshold scales with instrument count and average lot value for other markets.',s['body']),
    p('Market liquidity',s['wp_sub']),
    p('Strategies that pass the liquidity screening may encounter reduced liquidity at execution time \u2014 particularly for smaller-cap instruments or in stressed market conditions. The PM review is the appropriate point to assess current liquidity conditions before approving execution.',s['body']),
    PageBreak(),sp(0),
    p('5. DATA RISK',s['wp_section']),hrm(),
    p('The risk that market data used for optimisation or execution is inaccurate, unavailable, or unrepresentative.',s['body_grey']),
    p('Market data source dependency',s['wp_sub']),
    p('Equity price history and live prices are currently sourced from Yahoo Finance via API \u2014 a widely used, generally reliable source for listed equity data, but a free provider without an enterprise SLA. Data quality issues do occur occasionally. Quality checks run on ingestion. The data source is configurable: a Bloomberg or institutional market data feed can be substituted without architectural changes \u2014 available as a Founding Mandate configuration option.',s['body']),
    p('Market data outage',s['wp_sub']),
    p('If the daily price download fails, existing three years of historical data in RDS is unaffected. Existing approved strategies continue to function. New strategy builds or signal re-optimisations require current data and would be deferred until the feed is restored. Slack notification on download completion means failure is visible immediately.',s['body']),
    p('Corporate action handling',s['wp_sub']),
    p('Yahoo Finance applies adjusted close prices that account for most corporate actions. Edge cases \u2014 recent corporate actions not yet reflected in adjusted prices \u2014 may affect signal quality for affected instruments. The PM review is the appropriate point to assess any known corporate action effects on the current strategy.',s['body']),
    p('FX rate accuracy',s['wp_sub']),
    p('Daily FX rates are fetched and stored for all configured currency pairs. Position-level conversion uses the most recent stored rate. For portfolios with significant cross-currency exposure, intraday FX movements may introduce a small conversion variance worth monitoring at execution time.',s['body']),
    p('6. OPERATIONAL RISK',s['wp_section']),hrm(),
    p('The risk that platform operations introduce errors or failures that affect client outcomes.',s['body_grey']),
    p('Human error at approval gates',s['wp_sub']),
    p('Every capital-affecting action requires explicit human approval \u2014 which is the primary operational risk mitigation and also the source of a residual risk: human error at the gate itself. Mitigations: the complete strategy breakdown is visible at the approval screen (instruments, weights, quantities, prices, efficiency), reducing undetected errors. The audit trail records every approval with PM identity and timestamp, supporting error investigation and correction.',s['body']),
    p('Role separation',s['wp_sub']),
    p('The three-role model separates research (Analyst), investment decisions (PM), and cash operations (Operations). An Analyst cannot approve strategies. Operations cannot initiate allocations. Infrastructure-level RBAC \u2014 enforcing this at the AWS IAM layer \u2014 is planned for the next prototype iteration.',s['body']),
    p('Platform unavailability',s['wp_sub']),
    p('ECS microservices on Fargate restart automatically on failure. RDS has automated daily backups. The SQS queue persists market orders through application restarts. No formal SLA is committed at the current stage. Production observability alerting is on the near-term roadmap. Availability commitments for Founding Mandate clients will be agreed as part of the mandate terms.',s['body']),
    p('Regulatory compliance',s['wp_sub']),
    p('Vektor is a portfolio construction and management platform. Regulatory obligations \u2014 licensing, client suitability, reporting \u2014 remain with the portfolio manager and the firm operating the platform. Vektor provides the audit trail and compliance documentation described in WP-06. Full details of regulatory standing are available to Founding Mandate partners on request.',s['body']),
    PageBreak(),sp(0),
    p('7. RISK MITIGATION ROADMAP',s['wp_section']),hrm(),
    p('Mitigations on the roadmap but not yet live \u2014 with defined trigger or condition for each.',s['body_grey']),
    ]
    roadmap_rows=[
        [p('MITIGATION',s['tbl_hdr']),p('RISK CATEGORY ADDRESSED',s['tbl_hdr']),p('TRIGGER / CONDITION',s['tbl_hdr'])],
        [p('Live IBKR execution',s['tbl_gold']),p('Execution \u2014 simulation vs live gap',s['tbl_body']),p('Before first Founding Mandate client onboards',s['tbl_body'])],
        [p('Walk-forward validation',s['tbl_body']),p('Model \u2014 overfitting and backtest-to-live gap',s['tbl_body']),p('After live track record of sufficient length established',s['tbl_body'])],
        [p('Automated drift detection',s['tbl_body']),p('Model \u2014 XGBoost model drift',s['tbl_body']),p('As part of production observability implementation',s['tbl_body'])],
        [p('CloudWatch alerting',s['tbl_body']),p('Operational \u2014 platform unavailability, data outage',s['tbl_body']),p('Before production environment promotion',s['tbl_body'])],
        [p('Infrastructure-level RBAC',s['tbl_body']),p('Operational \u2014 role separation',s['tbl_body']),p('Next prototype iteration',s['tbl_body'])],
        [p('Bloomberg / institutional data feed',s['tbl_body']),p('Data \u2014 market data source reliability',s['tbl_body']),p('Available as configuration for Founding Mandate partners',s['tbl_body'])],
    ]
    cw2=[42*mm,60*mm,COL_W-102*mm]
    rt2=Table(roadmap_rows,colWidths=cw2,repeatRows=1,splitByRow=1)
    rt2.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1A1A20')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[CARD_BG,colors.HexColor('#0F0F14')]),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('LINEBELOW',(0,0),(-1,-1),0.3,RULE_MIN),
        ('BOX',(0,0),(-1,-1),0.4,CARD_EDGE),
        ('LINEAFTER',(0,0),(0,-1),0.3,RULE_MIN),
        ('LINEAFTER',(1,0),(1,-1),0.3,RULE_MIN),
    ]))
    story.append(rt2)
    story+=[sp(12),
    p('8. CONCLUSION',s['wp_section']),hrm(),
    p('Risk disclosure is not the same as risk management. This document is both.',s['body_grey']),
    p('The risks described in this paper are real. Some are inherent to systematic portfolio management regardless of platform. Some are specific to the current stage of Vektor\u2019s development. The mitigations described are genuine \u2014 either structurally enforced by the platform architecture or explicitly on the roadmap with defined trigger conditions.',s['body']),
    NoteBox(COL_W,
        'The Founding Mandate is a partnership in which both parties are building toward the same outcome \u2014 '
        'a platform that performs as described, with the governance and controls that institutional management '
        'requires. Founding Mandate partners are invited to raise any risk they do not see addressed in this '
        'document. That conversation is part of the partnership.',s['body']),
    ]
    closing_row(
        'For compliance and audit trail architecture, see WP-06. For AI and ML governance, see WP-08. For technical infrastructure, see WP-07. All documents at investpuppy.com.',
        REF,s,story)

    doc.build(story)
    print(f'Built: {OUT}')
    import subprocess
    r=subprocess.run(['pdfinfo',OUT],capture_output=True,text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l: print(l)

if __name__=='__main__': build()
