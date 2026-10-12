"""
Bayesian MMM & Statistical Modeling Tools
Enables agents to query MCMC convergence, channel contributions, saturation response, and marginal ROAS.
"""

from typing import Dict, Any, List
from tools.registry import registry, ToolPermission
from modeling.mmm_engine import mmm_engine


@registry.register(
    name="select_model",
    description="Selects MMM model specification (Adstock decay + Hill saturation with Gaussian random walk priors).",
    permission=ToolPermission.READ_ONLY
)
def select_model(model_family: str = "Bayesian_Adstock_Hill") -> Dict[str, Any]:
    return {
        "selected_model": model_family,
        "adstock_transformation": "Geometric Adstock (single-parameter decay)",
        "saturation_transformation": "Two-parameter Hill Function (S-shape with half-saturation K)",
        "sampler": "No-U-Turn Sampler (NUTS / HMC)"
    }


@registry.register(
    name="fit_bayesian_mmm",
    description="Loads or executes Bayesian MMM estimation and decomposes channel revenue contributions.",
    permission=ToolPermission.READ_ONLY
)
def fit_bayesian_mmm() -> Dict[str, Any]:
    return mmm_engine.get_model_summary()


@registry.register(
    name="check_convergence",
    description="Checks Gelman-Rubin R-hat and Effective Sample Size (ESS) MCMC convergence diagnostics.",
    permission=ToolPermission.READ_ONLY
)
def check_convergence() -> Dict[str, Any]:
    return mmm_engine.run_diagnostics()


@registry.register(
    name="plot_contributions",
    description="Returns modeled revenue contribution percentages across all marketing channels and organic baseline.",
    permission=ToolPermission.READ_ONLY
)
def plot_contributions() -> List[Dict[str, Any]]:
    channels = mmm_engine.get_channel_metrics()
    return [
        {
            "channel": c["channel_name"],
            "contribution_usd": c["modeled_contribution"],
            "contribution_pct": c["contribution_pct"],
            "total_spend_usd": c["total_spend"]
        }
        for c in channels
    ]


@registry.register(
    name="compute_roi",
    description="Computes blended Return on Ad Spend (ROAS) across all modeled channels.",
    permission=ToolPermission.READ_ONLY
)
def compute_roi() -> List[Dict[str, Any]]:
    channels = mmm_engine.get_channel_metrics()
    return [
        {
            "channel": c["channel_name"],
            "blended_roas": c["blended_roas"],
            "total_spend": c["total_spend"],
            "modeled_revenue": c["modeled_contribution"]
        }
        for c in channels if c["total_spend"] > 0
    ]


@registry.register(
    name="compute_marginal_roi",
    description="Computes instantaneous Marginal ROAS (mROI = dRevenue/dSpend) at current weekly spend levels.",
    permission=ToolPermission.READ_ONLY
)
def compute_marginal_roi() -> List[Dict[str, Any]]:
    channels = mmm_engine.get_channel_metrics()
    return [
        {
            "channel": c["channel_name"],
            "current_blended_roas": c["blended_roas"],
            "current_marginal_roas": c["marginal_roas"],
            "saturation_status": c["saturation_status"],
            "recommendation_bias": c["recommendation_bias"]
        }
        for c in channels if c["total_spend"] > 0
    ]


@registry.register(
    name="generate_saturation_curves",
    description="Generates non-linear Hill response curves showing diminishing marginal returns by channel.",
    permission=ToolPermission.READ_ONLY
)
def generate_saturation_curves(channel_name: str = "Google Search") -> Dict[str, Any]:
    return mmm_engine.generate_saturation_curve(channel_name=channel_name)
