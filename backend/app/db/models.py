"""
SQLAlchemy Models for Copilot Persistence
"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime
from backend.app.db.database import Base


class DBCopilotRecommendation(Base):
    __tablename__ = "copilot_recommendations"

    id = Column(String, primary_key=True, index=True)
    agent = Column(String, index=True)
    issue = Column(Text, nullable=False)
    evidence_json = Column(Text, nullable=False)
    priority = Column(String, index=True)
    confidence = Column(Float, nullable=False)
    expected_impact = Column(Text, nullable=False)
    effort = Column(String)
    proposed_action = Column(Text, nullable=False)
    next_steps_json = Column(Text, nullable=False)
    requires_approval = Column(Boolean, default=True)
    status = Column(String, default="pending", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DBCopilotAgentRun(Base):
    __tablename__ = "copilot_agent_runs"

    run_id = Column(String, primary_key=True, index=True)
    agent = Column(String, index=True)
    started_at = Column(String, nullable=False)
    finished_at = Column(String, nullable=False)
    input_summary = Column(Text)
    tool_calls_json = Column(Text)
    token_cost = Column(Integer, default=0)
    api_cost_estimate = Column(Float, default=0.0)
    latency_ms = Column(Float, default=0.0)
    status = Column(String, default="success")
    error = Column(Text, nullable=True)


class DBCopilotOutcome(Base):
    __tablename__ = "copilot_action_outcomes"

    rec_id = Column(String, primary_key=True, index=True)
    executed_at = Column(String, nullable=False)
    execution_result_json = Column(Text)
    measurement_status = Column(String, default="in_progress")
    measured_improvement_json = Column(Text, nullable=True)
    measured_at = Column(String, nullable=True)
