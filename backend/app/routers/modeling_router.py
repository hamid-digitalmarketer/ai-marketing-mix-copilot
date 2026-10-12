"""
Modeling & Scenario Simulation API Router
Exposes Bayesian MMM parameters, Hill saturation curves, causal lift, and counterfactual simulation endpoints.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from fastapi import APIRouter
from modeling.mmm_engine import mmm_engine
from modeling.causal_engine import causal_engine
from modeling.budget_optimizer import budget_optimizer

router = APIRouter(prefix="/api/modeling", tags=["Modeling & Scenarios"])


class SimulationRequest(BaseModel):
    google_search_shift: float = -5000.0
    retail_media_shift: float = 5000.0
    meta_ads_shift: float = 0.0
    youtube_shift: float = 0.0
    email_shift: float = 0.0


@router.get("/summary")
def get_model_summary():
    """Returns Bayesian MMM decomposition, diagnostics, and goodness-of-fit."""
    return mmm_engine.get_model_summary()


@router.get("/channels")
def get_channels():
    """Returns channel contributions, blended ROAS, and marginal ROAS."""
    return mmm_engine.get_channel_metrics()


@router.get("/saturation-curve/{channel_name}")
def get_saturation_curve(channel_name: str):
    """Returns Hill saturation curve data points across spend levels."""
    return mmm_engine.generate_saturation_curve(channel_name=channel_name)


@router.get("/causal-lift")
def get_causal_lift():
    """Returns Difference-in-Differences causal incrementality results from geo holdout."""
    return causal_engine.run_diff_in_diff_analysis()


@router.post("/simulate-scenario")
def simulate_scenario(req: SimulationRequest):
    """Simulates counterfactual budget reallocations and returns predicted revenue lift with 90% CI."""
    shifts = {
        "Google Search": req.google_search_shift,
        "Retail Media (Amazon/Walmart)": req.retail_media_shift,
        "Meta Ads": req.meta_ads_shift,
        "YouTube Video": req.youtube_shift,
        "Email Marketing": req.email_shift
    }
    return budget_optimizer.simulate_budget_scenario(shifts)


@router.get("/optimal-allocation")
def get_optimal_allocation(total_budget: Optional[float] = None):
    """Solves for optimal budget allocation balancing marginal ROAS across channels."""
    return budget_optimizer.compute_optimal_allocation(total_weekly_budget=total_budget)
