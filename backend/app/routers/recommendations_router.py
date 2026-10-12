"""
Recommendations API Router for Marketing Mix Copilot
"""

from typing import Optional
from fastapi import APIRouter, HTTPException
from agents.orchestrator import copilot_orchestrator

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.get("")
def list_recommendations(
    agent: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None
):
    """Lists strategic recommendations with optional filtering."""
    recs = list(copilot_orchestrator.recommendations_store.values())

    if agent:
        recs = [r for r in recs if agent.lower() in r.agent.lower()]
    if priority:
        recs = [r for r in recs if r.priority.value.lower() == priority.lower()]
    if status:
        recs = [r for r in recs if r.status.value.lower() == status.lower()]

    return [r.model_dump() for r in recs]


@router.get("/{rec_id}")
def get_recommendation(rec_id: str):
    """Retrieves a single recommendation by unique identifier."""
    if rec_id not in copilot_orchestrator.recommendations_store:
        raise HTTPException(status_code=404, detail=f"Recommendation '{rec_id}' not found.")
    return copilot_orchestrator.recommendations_store[rec_id].model_dump()
