"""
Budget Scenario & Allocation Optimization Tools
Enables agents to simulate counterfactual shifts, solve for equalized marginal ROI, and apply approved budget reallocations.
"""

from typing import Dict, Any, Optional
from tools.registry import registry, ToolPermission
from modeling.budget_optimizer import budget_optimizer


@registry.register(
    name="simulate_budget_reallocation",
    description="Simulates counterfactual budget reallocations across channels and predicts net revenue delta with 90% credible intervals.",
    permission=ToolPermission.READ_ONLY
)
def simulate_budget_reallocation(google_search_shift: float = -5000.0, retail_media_shift: float = 5000.0) -> Dict[str, Any]:
    shifts = {
        "Google Search": google_search_shift,
        "Retail Media (Amazon/Walmart)": retail_media_shift
    }
    return budget_optimizer.simulate_budget_scenario(shifts)


@registry.register(
    name="optimize_allocation",
    description="Solves for optimal budget allocation across paid marketing channels by equalizing marginal ROAS.",
    permission=ToolPermission.READ_ONLY
)
def optimize_allocation(total_weekly_budget: Optional[float] = None) -> Dict[str, Any]:
    return budget_optimizer.compute_optimal_allocation(total_weekly_budget=total_weekly_budget)


@registry.register(
    name="forecast_outcomes",
    description="Forecasts total revenue and ROI under optimized budget allocation over 12 months.",
    permission=ToolPermission.READ_ONLY
)
def forecast_outcomes() -> Dict[str, Any]:
    opt = budget_optimizer.compute_optimal_allocation()
    return {
        "annual_projected_revenue_lift_usd": opt["projected_annual_revenue_gain"],
        "weekly_projected_revenue_lift_usd": opt["projected_weekly_revenue_gain"],
        "capital_efficiency_verdict": opt["projected_overall_roas_lift"]
    }


@registry.register(
    name="apply_budget_reallocation",
    description="Write-capable tool to update live media channel budget allocations. Requires explicit human approval.",
    permission=ToolPermission.WRITE_CAPABLE
)
def apply_budget_reallocation(plan_id: str, new_weekly_budgets: Dict[str, float]) -> Dict[str, Any]:
    return {
        "success": True,
        "action": "apply_budget_reallocation",
        "plan_id": plan_id,
        "applied_weekly_budgets": new_weekly_budgets,
        "status": "applied_to_dsp_and_search_engines",
        "timestamp": "2026-10-12T10:00:00Z"
    }
