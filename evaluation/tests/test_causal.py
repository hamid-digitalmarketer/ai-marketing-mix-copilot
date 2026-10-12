"""
Test Suite for Causal Inference & Difference-in-Differences Estimators
"""

import pytest
from modeling.causal_engine import causal_engine


def test_diff_in_diff_causal_lift():
    res = causal_engine.run_diff_in_diff_analysis()
    assert res["treatment_dmas_count"] == 15
    assert res["control_dmas_count"] == 15
    # Causal iROAS ground truth
    assert res["incremental_roas_iroas"] == 1.45
    # Platform reports 3.8x
    assert res["platform_reported_roas"] == 3.80
    assert res["attribution_haircut_pct"] > 50.0
    # Statistical significance
    sig = res["statistical_significance"]
    assert sig["is_statistically_significant"] is True
    assert sig["p_value"] < 0.05


def test_geo_holdout_design_planner():
    plan = causal_engine.design_geo_holdout_recommendation("Meta Ads")
    assert plan["target_channel"] == "Meta Ads"
    assert plan["recommended_holdout_pct"] == 15.0
    assert plan["recommended_duration_weeks"] == 4
