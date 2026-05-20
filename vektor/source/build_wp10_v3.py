"""WP-10: Evaluating Systematic Strategy Performance — corrected rebuild."""
import sys; sys.path.insert(0,'/home/claude')
from wp_builder_v3 import *
from reportlab.platypus import PageBreak, NextPageTemplate

OUT='/home/claude/investpuppy/vektor/output/pdf/vk5-wp10-evaluating-performance.pdf'
SUBTITLE='Evaluating Systematic Strategy Performance'
REF='IP-WP-PERF-260501-1.0'

def build():
    draw_cover=make_cover_fn(
        ['Evaluating Systematic','Strategy Performance'],
        ["A practitioner's guide to the metrics that matter \u2014 Sharpe ratio, drawdown,",
         "signal decay, and benchmark comparison \u2014 and how to apply them",
         "when evaluating a systematic listed equity strategy."],
        'For DPMs, family office analysts, and institutional allocators',REF)
    draw_page=make_page_fn(SUBTITLE)
    doc,f_cov,f_fst,f_lat=make_doc(OUT,SUBTITLE)
    doc.addPageTemplates([
        PageTemplate(id='Cover',frames=[f_cov],onPage=draw_cover),
        PageTemplate(id='First',frames=[f_fst],onPage=lambda c,d:(c.saveState(),c.setFillColor(BG),c.rect(0,0,W,H,fill=1,stroke=0),HRule(COL_W,RULE_MIN,0.3,3,3),draw_page(c,d),c.restoreState()) and None or draw_page(c,d)),
        PageTemplate(id='Later',frames=[f_lat],onPage=draw_page),
    ])
    s=make_styles()
    story=[sp(1),NextPageTemplate('Later'),PageBreak()]

    story+=[p('ABSTRACT',s['tag']),
    NoteBox(COL_W,
        'We wrote this paper because we expect to be asked how to evaluate a systematic platform '
        'with no live track record. The honest answer requires a framework, not a talking point. '
        'This is the framework. '
        'Systematic strategies are frequently evaluated using the wrong metrics, applied incorrectly, against '
        'inappropriate benchmarks. This produces two failure modes: good strategies are rejected because they '
        'score poorly on a metric they were not designed to optimise, and poor strategies are adopted because '
        'they score well on metrics that do not capture their actual risk. This paper gives a DPM the vocabulary '
        'and framework to evaluate any systematic listed equity strategy \u2014 and specifically to evaluate the '
        'strategy outputs that Vektor produces. The metrics covered here are the same metrics Vektor uses in its '
        'optimisation process, which means they are directly applicable to interpreting every output the platform generates.',
        s['body']),sp(10),
    key_takeaways_box([
        'Sharpe ratio is the primary evaluation metric for systematic strategies \u2014 and the same metric Vektor uses as its optimisation objective. Understanding it correctly is the starting point for evaluating any Vektor strategy output.',
        'Maximum drawdown and drawdown duration together tell you more about a strategy\u2019s risk than volatility alone \u2014 and reveal how a strategy behaves across different market regimes.',
        'Benchmark comparison for a systematic multi-instrument strategy should use a blended benchmark weighted to match the portfolio\u2019s actual sector composition \u2014 not a single index.',
        'Signal decay is the most underappreciated risk in technical indicator strategies. Vektor\u2019s structural response is re-optimisation at each strategy build \u2014 but the DPM should monitor for early warning signs.',
        'The most honest evaluation is a live track record. In its absence, walk-forward validation is the most rigorous available proxy \u2014 and it is on the Vektor near-term roadmap.',
    ],s),sp(10),
    p(f'investpuppy.com  \u00b7  contact@investpuppy.com  \u00b7  {REF}  \u00b7  Copyright 2026 InvestPuppy',s['wp_ref']),
    PageBreak(),sp(0),
    p('1. THE RIGHT QUESTION',s['wp_section']),hrm(),
    p('Before choosing a metric, choose the question you are trying to answer.',s['body_grey']),
    p('The most common evaluation mistake is applying a metric without first stating what question it is supposed to answer. A DPM evaluating a systematic strategy \u2014 including a strategy produced by Vektor \u2014 typically has three distinct questions: Does this strategy generate returns that justify its risk? Does it perform consistently across different market conditions? And will it continue to perform when deployed with real capital?',s['body']),
    p('These are three different questions requiring different metrics. Sharpe ratio addresses the first \u2014 and is the same metric Vektor uses as its optimisation objective, making it directly applicable to every strategy output the platform produces. Drawdown analysis addresses the second. Walk-forward validation and signal decay analysis address the third. Applying any single metric to all three questions will produce a misleading evaluation.',s['body']),
    p('2. SHARPE RATIO \u2014 THE PRIMARY METRIC',s['wp_section']),hrm(),
    p('What the Sharpe ratio measures, what it does not measure, and how to interpret it for a systematic listed equity strategy.',s['body_grey']),
    p('The Sharpe ratio is the ratio of excess return (above the risk-free rate) to the standard deviation of returns. It answers: how much return does this strategy generate per unit of risk taken? A Sharpe ratio of 1.0 means one unit of excess return for every unit of volatility \u2014 a reasonable target for a systematic equity strategy. Vektor uses Sharpe ratio as the objective function in both the efficient frontier optimisation and the technical indicator grid search, making it the directly applicable metric for evaluating Vektor\u2019s outputs.',s['body']),
    p('Interpreting Sharpe ratios in backtests',s['wp_sub']),
    p('Backtest Sharpe ratios are consistently higher than live Sharpe ratios because backtests do not include transaction costs, market impact, or execution slippage in full. A live Sharpe ratio of 50\u201370% of the backtest Sharpe ratio is a reasonable expectation for a well-constructed systematic strategy. A backtest Sharpe above 2.0 should prompt questions about overfitting \u2014 it is unusual for a genuine alpha-generating strategy to sustain a Sharpe above 2.0 in live conditions.',s['body']),
    p('What the Sharpe ratio does not measure',s['wp_sub']),
    p('The Sharpe ratio assumes normally distributed returns. Momentum signal strategies often have skewed distributions \u2014 relatively small, frequent gains and occasional larger losses. For strategies with non-normal distributions, the Sortino ratio \u2014 which uses downside deviation rather than total standard deviation \u2014 is a more appropriate risk-adjusted measure.',s['body']),
    p('Sharpe ratio in Vektor\u2019s optimisation',s['wp_sub']),
    # CORRECTED: Monte Carlo portfolio optimisation → efficient frontier optimisation
    p('Vektor uses Sharpe ratio as the objective function in both the efficient frontier optimisation (identifying the max-Sharpe allocation from 10,000 portfolio configurations) and the technical indicator grid search (selecting the highest-Sharpe indicator configuration per instrument). This means Sharpe ratio is the directly relevant metric for evaluating both the portfolio construction and the signal selection outputs that Vektor produces.',s['body']),
    PageBreak(),sp(0),
    p('3. DRAWDOWN ANALYSIS',s['wp_section']),hrm(),
    p('Maximum drawdown and drawdown duration \u2014 the metrics that reveal how a strategy behaves in adverse conditions.',s['body_grey']),
    p('Maximum drawdown measures the largest peak-to-trough decline in portfolio value over a given period. It answers: what is the worst experience a client would have had if they invested at the worst possible time? Drawdown duration \u2014 time to recover from a drawdown to a new high \u2014 addresses the second dimension: how long did recovery take?',s['body']),
    p('Why drawdown duration matters as much as depth',s['wp_sub']),
    p('A strategy with a 20% maximum drawdown recovering in three months is a very different client experience from one with a 20% drawdown taking three years to recover. The depth tells you the magnitude; the duration tells you the psychological and practical cost for a client who cannot time the market.',s['body']),
    p('Drawdown in trending vs mean-reverting markets',s['wp_sub']),
    p('Technical indicator strategies \u2014 particularly momentum signals like SMA, EMA, and MACD \u2014 tend to generate larger drawdowns in mean-reverting market conditions. A market that moves sharply in one direction then reverses quickly will trigger momentum signals caught by the reversal. This is a known characteristic of momentum strategies: drawdown analysis should be conducted across multiple market regimes, not just the dominant regime in the backtest period.',s['body']),
    p('Calmar ratio',s['wp_sub']),
    p('The Calmar ratio \u2014 annualised return divided by maximum drawdown \u2014 combines return and drawdown in a single metric. A Calmar ratio above 1.0 is generally acceptable for a systematic equity strategy. Like the Sharpe ratio, backtest Calmar ratios are typically higher than live ratios.',s['body']),
    p('4. BENCHMARK COMPARISON',s['wp_section']),hrm(),
    p('How to choose the right benchmark for a systematic multi-instrument strategy \u2014 and why a single index is usually the wrong choice.',s['body_grey']),
    p('A benchmark serves one purpose: to establish what return a passive investor would have earned by holding a comparable portfolio. A systematic strategy that underperforms its benchmark on a risk-adjusted basis does not justify active management fees. One that outperforms (positive alpha) is generating value passive exposure cannot replicate.',s['body']),
    p('Why a single index is usually wrong',s['wp_sub']),
    p('A single-country index like the STI is the correct passive benchmark only if the strategy holds all instruments in proportion to their index weights. A concentrated ten-instrument portfolio selected from a 500-instrument universe will have very different sector and size exposure from the index. Comparing it against the index conflates active sector allocation with stock selection skill.',s['body']),
    p('Constructing a blended benchmark',s['wp_sub']),
    p('The appropriate benchmark for a Vektor strategy is a blended index weighted to match the portfolio\u2019s sector composition \u2014 the same sectors represented in the selected instruments, weighted by their portfolio allocation. This isolates the contribution of instrument selection from sector allocation. A strategy that outperforms on a sector-blended benchmark is generating genuine stock selection alpha.',s['body']),
    p('Information ratio',s['wp_sub']),
    p('The information ratio \u2014 excess return over benchmark divided by tracking error \u2014 measures consistency of outperformance. A high information ratio means the strategy outperforms consistently, not just in certain periods. For a systematic strategy with regular rebalancing, the information ratio is a more meaningful measure of skill than single-period alpha.',s['body']),
    PageBreak(),sp(0),
    p('5. SIGNAL DECAY',s['wp_section']),hrm(),
    p('The most underappreciated risk in technical indicator strategies \u2014 and how to detect it early.',s['body_grey']),
    p('Signal decay occurs when a technical indicator loses its predictive power over time. A momentum indicator reliable during a trending market regime will underperform \u2014 and may reverse \u2014 during a mean-reverting regime. A signal optimised on three years of data may already be decaying by the time it is deployed.',s['body']),
    p('Early warning signs',s['wp_sub']),
    p('The earliest observable signal of decay is a reduction in XGBoost confidence scores for an instrument\u2019s assigned indicator. If the model consistently assigns low confidence to signals that were high-confidence at strategy build time, the indicator parameters may need re-optimisation. A second signal: actual portfolio performance diverging from the projected performance implied by the backtest Sharpe ratio.',s['body']),
    p('Structural response: re-optimisation',s['wp_sub']),
    p('Vektor\u2019s primary structural response to signal decay is re-optimisation at each strategy build. Indicator parameters are not fixed at initial setup \u2014 they are re-selected by the grid search each time the strategy is rebuilt, using the most recent three years of data. A strategy rebuilt regularly will naturally adapt to changing market conditions.',s['body']),
    p('Walk-forward validation as the honest test',s['wp_sub']),
    p('The most rigorous test of whether a signal is genuinely predictive is walk-forward validation: optimise parameters on an in-sample window, test on the immediately following out-of-sample period, advance the window, and repeat. A strategy maintaining acceptable Sharpe ratios across multiple out-of-sample windows has demonstrated robustness that a single backtest cannot provide. Walk-forward validation is on the Vektor near-term roadmap.',s['body']),
    p('6. THE LIVE TRACK RECORD',s['wp_section']),hrm(),
    p('The only truly honest evaluation of a systematic strategy is what it does with real capital in live markets.',s['body_grey']),
    p('All backtest metrics are approximations of what a strategy might do. They are constrained by the backtest period\u2019s market regime, assumptions about execution, and the optimisation choices that produced the strategy. A live track record removes all of these constraints.',s['body']),
    p('Vektor does not yet have a live track record with real client capital. The platform is operational in simulation mode and the full workflow \u2014 from research through execution \u2014 has been tested and validated. The Founding Mandate programme exists specifically to begin building a live track record under real conditions, with partners who understand they are participating in the early stage of platform development.',s['body']),
    NoteBox(COL_W,
        'The Founding Mandate proposition is explicit: early partners accept the absence of a live track record '
        'in exchange for founding terms, direct input into platform development, and the positioning advantage '
        'of a platform built around their specific workflow requirements. The track record will be built. The '
        'question is who builds it with us.',s['body']),
    PageBreak(),sp(0),
    p('7. PRACTICAL EVALUATION CHECKLIST',s['wp_section']),hrm(),
    p('Six questions to ask when evaluating any systematic listed equity strategy \u2014 including strategies produced by Vektor.',s['body_grey']),
    ]
    checklist=[
        ('What is the Sharpe ratio, and over what period?',
         'A three-year backtest Sharpe above 1.0 is a reasonable starting point. Ask what the Sharpe looks like over sub-periods \u2014 a strategy scoring 2.0 over three years but 0.3 in the most recent year is showing signs of decay. For Vektor strategies, the Sharpe ratio is the optimisation objective \u2014 it is the primary output to evaluate.'),
        ('What is the maximum drawdown, and how long did recovery take?',
         'Assess both dimensions. A deep, short drawdown and a shallow, long drawdown may have the same maximum drawdown figure but very different client experience implications.'),
        ('What is the benchmark, and is it appropriate?',
         "The benchmark should match the strategy's sector and geographic exposure, not just the exchange. A sector-blended benchmark is more meaningful than a single index for a concentrated portfolio."),
        ('What is the correlation between instruments in the portfolio?',
         'A portfolio holding ten instruments with average pairwise correlation above 0.7 is effectively concentrated in fewer positions. Correlation matrix verification is a required step in Vektor\u2019s optimisation workflow.'),
        ('Has the strategy been tested out-of-sample?',
         'A backtest optimised on the full history is always overfit to some degree. Walk-forward validation on held-out periods is the most honest available test of whether the signal is genuine or historical.'),
        ('What is the rebalancing frequency, and what are the transaction costs?',
         'A strategy requiring frequent rebalancing may look strong on a pre-cost Sharpe ratio but weak after costs. '
         'Vektor\u2019s current implementation uses market orders. Transaction cost modelling \u2014 '
         'bid-ask spread, market impact, brokerage \u2014 is not yet embedded in the optimisation engine; '
         'it is applied at the mandate design stage using the position set as input. '
         'This is a known gap in the current platform. Cost-adjusted optimisation is on the near-term roadmap. '
         'Until it is live, Founding Mandate partners are advised to apply cost assumptions to any Sharpe ratio '
         'comparison between Vektor strategy outputs and passive alternatives.'),
    ]
    for title, body in checklist:
        story.append(p(title,s['wp_sub']))
        story.append(p(body,s['body']))
    closing_row(
        'For signal optimisation methodology, see WP-02 and WP-04. For capital allocation precision, see WP-03. For risk and limitation disclosure, see WP-09. All documents at investpuppy.com.',
        REF,s,story)

    doc.build(story)
    print(f'Built: {OUT}')
    import subprocess
    r=subprocess.run(['pdfinfo',OUT],capture_output=True,text=True)
    for l in r.stdout.split('\n'):
        if 'Pages' in l: print(l)

if __name__=='__main__': build()
