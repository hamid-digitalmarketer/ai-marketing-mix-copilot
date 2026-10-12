"""
Structured Agent Data Schemas for Marketing Mix Copilot
Implements the exact Recommendation and ModelResult schemas defined in Phase 3.
"""

from enum import Enum
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field


class PriorityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EffortLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RecommendationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    MEASURED = "measured"


class EvidenceItem(BaseModel):
    source: str = Field(..., description="Data source name (e.g. Bayesian MMM Engine, Geo Holdout Test)")
    metric: str = Field(..., description="Name of the observed metric (e.g. Marginal ROAS, iROAS, p-value)")
    value: Union[str, float, int] = Field(..., description="The concrete numerical or observed value")
    confidence_interval: Optional[List[float]] = Field(None, description="Optional 90% or 95% credible / confidence interval")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class Recommendation(BaseModel):
    id: str = Field(..., description="Unique recommendation identifier")
    agent: str = Field(..., description="Name of originating agent")
    issue: str = Field(..., description="Concise description of detected problem or optimization opportunity")
    evidence: List[EvidenceItem] = Field(..., description="List of concrete, verifiable data points backing this issue")
    priority: PriorityLevel = Field(..., description="Calculated priority level")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")
    expected_impact: str = Field(..., description="Estimated business impact")
    effort: EffortLevel = Field(..., description="Implementation effort required")
    proposed_action: str = Field(..., description="Specific, actionable operational proposal")
    next_steps: List[str] = Field(..., description="Step-by-step checklist to execute")
    requires_approval: bool = Field(True, description="Enforces human sign-off before write actions take effect")
    status: RecommendationStatus = Field(RecommendationStatus.PENDING, description="Current workflow lifecycle status")


class ChannelMetric(BaseModel):
    channel_name: str
    total_spend: float
    modeled_contribution: float
    contribution_pct: float
    blended_roas: float
    marginal_roas: float
    saturation_status: str


class ModelResult(BaseModel):
    model_id: str
    model_type: str
    channels: List[ChannelMetric]
    diagnostics: Dict[str, Any]
    backtest_metrics: Dict[str, Any]
    token_cost: int = 0
    api_cost_estimate: float = 0.0
    latency_ms: float = 0.0


class AgentRun(BaseModel):
    run_id: str
    agent: str
    started_at: str
    finished_at: str
    input_summary: str
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    recommendations: List[Recommendation] = Field(default_factory=list)
    token_cost: int = 0
    api_cost_estimate: float = 0.0
    latency_ms: float = 0.0
    status: str = "success"
    error: Optional[str] = None
