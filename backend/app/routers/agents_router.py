"""
Agents API Router for Marketing Mix Copilot
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from agents.orchestrator import copilot_orchestrator
from agents.data_quality_agent import DataQualityAgent
from agents.model_agent import ModelAgent
from agents.incrementality_agent import IncrementalityAgent
from agents.scenario_agent import ScenarioAgent
from agents.explanation_agent import ExplanationAgent

router = APIRouter(prefix="/api/agents", tags=["Agents"])


@router.post("/run-all")
def run_all_agents(goal: str = Query("Optimize Marketing Mix & Prove Incrementality")):
    """Executes all 5 specialized agents and generates the unified strategic plan."""
    return copilot_orchestrator.run_full_copilot_audit(goal=goal)


@router.post("/run/{agent_name}")
def run_single_agent(agent_name: str, goal: Optional[str] = "Domain Specific Analysis"):
    """Triggers an individual domain agent."""
    name_lower = agent_name.lower()
    if "quality" in name_lower or "data" in name_lower:
        agent = DataQualityAgent(demo_mode=copilot_orchestrator.demo_mode)
    elif "model" in name_lower or "mmm" in name_lower:
        agent = ModelAgent(demo_mode=copilot_orchestrator.demo_mode)
    elif "incrementality" in name_lower or "causal" in name_lower or "holdout" in name_lower:
        agent = IncrementalityAgent(demo_mode=copilot_orchestrator.demo_mode)
    elif "scenario" in name_lower or "budget" in name_lower:
        agent = ScenarioAgent(demo_mode=copilot_orchestrator.demo_mode)
    elif "explain" in name_lower or "executive" in name_lower:
        agent = ExplanationAgent(demo_mode=copilot_orchestrator.demo_mode)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown agent: {agent_name}. Valid agents: quality, model, incrementality, scenario, explanation"
        )

    run = agent.run({"marketing_goal": goal})
    copilot_orchestrator.runs_history.append(run)
    for rec in run.recommendations:
        copilot_orchestrator.recommendations_store[rec.id] = rec

    return run.model_dump()


@router.get("/runs")
def list_agent_runs():
    """Lists historical agent execution telemetry."""
    return [r.model_dump() for r in copilot_orchestrator.runs_history]
