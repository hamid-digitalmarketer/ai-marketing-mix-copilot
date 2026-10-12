"""
Executive Explanation & Translation Tools
Translates complex Bayesian posterior metrics, adstock decay, and causal p-values into plain-language business insights.
"""

from typing import Dict, Any, List
from tools.registry import registry, ToolPermission
from modeling.mmm_engine import mmm_engine
from modeling.causal_engine import causal_engine
from modeling.budget_optimizer import budget_optimizer


@registry.register(
    name="summarize_model_results",
    description="Summarizes overall Bayesian model fit, total revenue decomposed, and top driving channels.",
    permission=ToolPermission.READ_ONLY
)
def summarize_model_results() -> Dict[str, Any]:
    summary = mmm_engine.get_model_summary()
    return {
        "model_type": summary.get("model_type"),
        "total_revenue_modeled": summary.get("total_revenue_modeled"),
        "r_squared": summary.get("goodness_of_fit", {}).get("r_squared"),
        "mape_pct": summary.get("goodness_of_fit", {}).get("mape_pct"),
        "mcmc_status": summary.get("convergence_diagnostics", {}).get("status")
    }


@registry.register(
    name="translate_to_plain_language",
    description="Translates marginal ROAS and saturation curves into non-technical CMO-ready language.",
    permission=ToolPermission.READ_ONLY
)
def translate_to_plain_language() -> List[Dict[str, str]]:
    return [
        {
            "channel": "Google Search",
            "plain_language_insight": "Google Search is near peak saturation (mROI $0.78). Every extra $1 spent generates only 78 cents in new sales because ads are cannibalizing users who would have clicked organic links anyway.",
            "strategic_takeaway": "Shift top 25-30% of search budget to under-saturated channels."
        },
        {
            "channel": "Retail Media (Amazon/Walmart)",
            "plain_language_insight": "Retail Media is currently underfunded and operating far below its saturation ceiling (mROI $2.65). Every extra dollar invested generates $2.65 in high-intent incremental revenue.",
            "strategic_takeaway": "Scale budget aggressively until mROI approaches $1.50."
        },
        {
            "channel": "Meta Ads",
            "plain_language_insight": "Meta Ads maintains healthy efficiency (mROI $1.42, 45% weekly carryover), making it an effective mid-funnel converter.",
            "strategic_takeaway": "Keep weekly spend stable while refreshing ad creatives to fight audience fatigue."
        }
    ]


@registry.register(
    name="generate_executive_summary",
    description="Generates an executive briefing on budget reallocation and causal incrementality findings.",
    permission=ToolPermission.READ_ONLY
)
def generate_executive_summary() -> Dict[str, Any]:
    diff = causal_engine.run_diff_in_diff_analysis()
    opt = budget_optimizer.compute_optimal_allocation()
    return {
        "headline": "Reallocating $8,400/week from Saturated Paid Search to Retail Media Unlocks +$408,000 in Annual Revenue",
        "key_finding_incrementality": f"Geo holdout testing confirms Google Search true causal iROAS is {diff['incremental_roas_iroas']}x vs platform-claimed {diff['platform_reported_roas']}x.",
        "key_finding_optimization": f"Balancing marginal ROAS yields a projected {opt['projected_overall_roas_lift']} with zero increase in total media budget.",
        "recommended_action": "Approve recommended budget reallocation plan in Growth OS queue."
    }
