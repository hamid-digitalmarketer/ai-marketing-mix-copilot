"""
Test Suite for Budget Optimization & Scenario Simulation
"""

import pytest
from modeling.budget_optimizer import budget_optimizer


def test_simulate_budget_scenario_reallocation():
    shifts = {"Google Search": -5000.0, "Retail Media (Amazon/Walmart)": 5000.0}
    res = budget_optimizer.simulate_budget_scenario(shifts)
    assert res["net_spend_change"] == 0.0
    # Shifting from saturated Search (mROI 0.78) to Retail Media (mROI 2.65) must yield positive net revenue lift
    assert res["predicted_weekly_revenue_lift"] > 0.0
    assert res["credible_interval_90pct"][0] > 0.0
    assert res["annualized_projected_revenue_lift"] > 0.0


def test_optimal_allocation_projection():
    opt = budget_optimizer.compute_optimal_allocation()
    assert opt["projected_weekly_revenue_gain"] > 5000.0
    assert opt["projected_annual_revenue_gain"] > 350000.0
    assert len(opt["recommended_allocations"]) == 5
