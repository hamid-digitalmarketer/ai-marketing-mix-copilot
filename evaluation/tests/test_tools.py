"""
Test Suite for Marketing Mix Copilot Tools & Permissions
"""

import pytest
from tools.registry import registry, ToolPermission


def test_tool_registration_completeness():
    tools = registry.list_tools()
    names = [t.name for t in tools]
    assert "load_raw_data" in names
    assert "validate_schema" in names
    assert "fit_bayesian_mmm" in names
    assert "compute_marginal_roi" in names
    assert "run_diff_in_diff" in names
    assert "simulate_budget_reallocation" in names
    assert "apply_budget_reallocation" in names


def test_read_only_tool_execution():
    res = registry.execute("compute_marginal_roi", allow_write=False)
    assert res.status == "success"
    assert isinstance(res.outputs, list)
    assert len(res.outputs) > 0


def test_write_capable_tool_blocked_without_permission():
    res = registry.execute(
        "apply_budget_reallocation",
        allow_write=False,
        plan_id="TEST-001",
        new_weekly_budgets={"Google Search": 15000.0}
    )
    assert res.status == "blocked"
    assert "requires explicit human approval" in res.error


def test_write_capable_tool_allowed_with_permission():
    res = registry.execute(
        "apply_budget_reallocation",
        allow_write=True,
        plan_id="TEST-001",
        new_weekly_budgets={"Google Search": 15000.0}
    )
    assert res.status == "success"
    assert res.outputs["success"] is True
