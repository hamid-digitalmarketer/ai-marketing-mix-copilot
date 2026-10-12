"""
Test Suite for All 5 Specialized Copilot Agents
"""

import pytest
from agents.data_quality_agent import DataQualityAgent
from agents.model_agent import ModelAgent
from agents.incrementality_agent import IncrementalityAgent
from agents.scenario_agent import ScenarioAgent
from agents.explanation_agent import ExplanationAgent


def test_data_quality_agent():
    agent = DataQualityAgent(demo_mode=True)
    run = agent.run()
    assert run.status == "success"
    assert len(run.recommendations) >= 1
    assert any("Readiness" in str(r.evidence) for r in run.recommendations)


def test_model_agent_saturation_detection():
    agent = ModelAgent(demo_mode=True)
    run = agent.run()
    assert run.status == "success"
    # Saturated channel recommendation
    sat_rec = next((r for r in run.recommendations if "SATURATED" in r.id), None)
    assert sat_rec is not None
    assert sat_rec.priority.value == "critical"
    # Marginal ROAS evidence
    mroi_ev = next(e for e in sat_rec.evidence if e.metric == "Marginal ROAS (mROI)")
    assert "0.78" in str(mroi_ev.value)


def test_incrementality_agent():
    agent = IncrementalityAgent(demo_mode=True)
    run = agent.run()
    assert run.status == "success"
    lift_rec = next((r for r in run.recommendations if "CAUSAL-LIFT" in r.id), None)
    assert lift_rec is not None
    assert lift_rec.priority.value == "critical"


def test_scenario_agent():
    agent = ScenarioAgent(demo_mode=True)
    run = agent.run()
    assert run.status == "success"
    assert len(run.recommendations) >= 2


def test_explanation_agent():
    agent = ExplanationAgent(demo_mode=True)
    run = agent.run()
    assert run.status == "success"
    brief_rec = next((r for r in run.recommendations if "EXEC-BRIEF" in r.id), None)
    assert brief_rec is not None
