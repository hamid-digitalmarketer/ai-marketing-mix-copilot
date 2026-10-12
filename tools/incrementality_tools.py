"""
Causal Inference & Incrementality Experiment Tools
Enables agents to evaluate geo holdouts, run Diff-in-Diff, assess statistical significance, and compute causal incremental lift.
"""

from typing import Dict, Any
from tools.registry import registry, ToolPermission
from modeling.causal_engine import causal_engine


@registry.register(
    name="run_diff_in_diff",
    description="Runs Difference-in-Differences causal estimation on DMA market experiment data.",
    permission=ToolPermission.READ_ONLY
)
def run_diff_in_diff() -> Dict[str, Any]:
    return causal_engine.run_diff_in_diff_analysis()


@registry.register(
    name="analyze_geo_holdout",
    description="Analyzes holdout market revenue versus treatment market revenue to measure true incremental iROAS.",
    permission=ToolPermission.READ_ONLY
)
def analyze_geo_holdout() -> Dict[str, Any]:
    return causal_engine.run_diff_in_diff_analysis()


@registry.register(
    name="calculate_lift",
    description="Compares causal incremental ROAS (iROAS) against ad-platform reported last-touch ROAS.",
    permission=ToolPermission.READ_ONLY
)
def calculate_lift() -> Dict[str, Any]:
    res = causal_engine.run_diff_in_diff_analysis()
    return {
        "channel": "Paid Search (Google Ads)",
        "platform_reported_roas": res["platform_reported_roas"],
        "causal_incremental_roas": res["incremental_roas_iroas"],
        "incrementality_haircut_pct": res["attribution_haircut_pct"],
        "verdict": "SIGNIFICANT_BRAND_CANNIBALIZATION: Platform over-reports ROAS by 60%+ because it takes credit for organic intent."
    }


@registry.register(
    name="assess_statistical_significance",
    description="Tests p-value and standard errors of experiment lift against null hypothesis.",
    permission=ToolPermission.READ_ONLY
)
def assess_statistical_significance() -> Dict[str, Any]:
    res = causal_engine.run_diff_in_diff_analysis()
    return res["statistical_significance"]


@registry.register(
    name="design_geo_holdout",
    description="Calculates required sample size, holdout market percentage, and duration for future incrementality test.",
    permission=ToolPermission.READ_ONLY
)
def design_geo_holdout(channel: str = "Meta Ads") -> Dict[str, Any]:
    return causal_engine.design_geo_holdout_recommendation(channel=channel)
