"""
Test Suite for Bayesian MMM & Mathematical Transformations
"""

import pytest
import numpy as np
from modeling.mmm_engine import geometric_adstock, hill_saturation, mmm_engine


def test_geometric_adstock_decay():
    spend = np.array([100.0, 0.0, 0.0, 0.0])
    alpha = 0.5
    adstocked = geometric_adstock(spend, alpha)
    # Period 0: 100, Period 1: 50, Period 2: 25, Period 3: 12.5
    assert adstocked[0] == 100.0
    assert adstocked[1] == 50.0
    assert adstocked[2] == 25.0
    assert adstocked[3] == 12.5


def test_hill_saturation_diminishing_returns():
    k = 1000.0
    s = 2.0
    spend = np.array([0.0, 1000.0, 5000.0])
    sat = hill_saturation(spend, k, s)
    assert sat[0] == 0.0
    # At half-saturation point k, sat is exactly 0.5
    assert pytest.approx(sat[1], 0.01) == 0.50
    # Higher spend approaches 1.0 asymptotically
    assert sat[2] > 0.90


def test_bayesian_mmm_diagnostics():
    diag = mmm_engine.run_diagnostics()
    assert diag["status"] == "PASSED"
    assert diag["max_r_hat"] <= 1.05
    assert diag["effective_sample_size"] >= 1000
    assert diag["mape_pct"] <= 8.5


def test_saturation_curve_generation():
    curve = mmm_engine.generate_saturation_curve("Google Search", steps=10)
    assert curve["channel"] == "Google Search"
    assert len(curve["curve_points"]) == 10
    # Expected revenue increases monotonically with spend
    revs = [p["expected_weekly_revenue"] for p in curve["curve_points"]]
    assert revs[-1] > revs[0]
