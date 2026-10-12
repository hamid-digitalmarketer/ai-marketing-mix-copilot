"""
Human-in-the-Loop Governance & Outcome Tracking API
"""

from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from agents.orchestrator import copilot_orchestrator

router = APIRouter(prefix="/api/approvals", tags=["Human-in-the-Loop Governance"])


class ApproveRequest(BaseModel):
    reviewer: str = "hamid-lead"


class RejectRequest(BaseModel):
    reason: str = "Allocation window deferred"


@router.post("/{rec_id}/approve")
def approve_recommendation(rec_id: str, payload: Optional[ApproveRequest] = None):
    """Marks recommendation as APPROVED by authorized marketing lead."""
    reviewer = payload.reviewer if payload else "hamid-lead"
    res = copilot_orchestrator.approve_recommendation(rec_id, reviewer=reviewer)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@router.post("/{rec_id}/reject")
def reject_recommendation(rec_id: str, payload: Optional[RejectRequest] = None):
    """Rejects recommendation with documented justification."""
    reason = payload.reason if payload else "Allocation window deferred"
    res = copilot_orchestrator.reject_recommendation(rec_id, reason=reason)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@router.post("/{rec_id}/execute")
def execute_recommendation(rec_id: str):
    """
    Executes an action.
    SAFETY GUARD: Blocked if recommendation is not in APPROVED state.
    """
    res = copilot_orchestrator.execute_approved_action(rec_id)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@router.post("/{rec_id}/measure")
def measure_outcome(rec_id: str):
    """Measures post-reallocation incremental lift against pre-action baseline."""
    res = copilot_orchestrator.measure_action_outcome(rec_id)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("error"))
    return res


@router.get("/outcomes")
def list_outcomes():
    """Lists all tracked actions and verified outcome improvements."""
    return list(copilot_orchestrator.outcomes_store.values())
