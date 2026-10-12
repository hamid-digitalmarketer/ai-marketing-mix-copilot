"""
Base Agent Foundation for Marketing Mix Copilot
Handles tool execution telemetry, token tracking, error containment, and AgentRun generation.
"""

import time
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import tools
from tools.registry import registry, ToolRecord
from agents.schemas import AgentRun, Recommendation


class BaseCopilotAgent:
    """Base class for all specialized marketing mix and causal inference agents."""

    def __init__(self, name: str, demo_mode: bool = True):
        self.name = name
        self.demo_mode = demo_mode
        self.tool_calls_trace: List[Dict[str, Any]] = []
        self.total_tokens: int = 0
        self.estimated_api_cost: float = 0.0

    def call_tool(self, tool_name: str, allow_write: bool = False, **kwargs) -> Any:
        """Executes a tool through the registry and logs telemetry."""
        record: ToolRecord = registry.execute(tool_name, allow_write=allow_write, **kwargs)
        
        trace_entry = {
            "tool_name": record.tool_name,
            "permission": record.permission.value,
            "inputs": record.inputs,
            "outputs_summary": str(record.outputs)[:300] if record.outputs is not None else None,
            "latency_ms": record.latency_ms,
            "status": record.status,
            "error": record.error,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.tool_calls_trace.append(trace_entry)
        
        # Token telemetry estimation
        estimated_input_chars = len(str(kwargs)) + (len(str(record.outputs)) if record.outputs else 0)
        tokens = int(estimated_input_chars / 4) + 160
        self.total_tokens += tokens
        if not self.demo_mode:
            self.estimated_api_cost += round((tokens / 1_000_000) * 2.50, 6)

        if record.status == "error":
            return None
        return record.outputs

    def run(self, input_context: Optional[Dict[str, Any]] = None) -> AgentRun:
        """Runs the agent workflow and produces an AgentRun with structured recommendations."""
        start_time = time.perf_counter()
        run_id = f"run_{self.name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}"
        started_at = datetime.utcnow().isoformat()
        
        self.tool_calls_trace = []
        self.total_tokens = 0
        self.estimated_api_cost = 0.0
        
        recommendations: List[Recommendation] = []
        run_status = "success"
        error_msg = None
        
        try:
            recommendations = self.execute_reasoning(input_context or {})
        except Exception as e:
            run_status = "failed"
            error_msg = str(e)
            
        total_latency = round((time.perf_counter() - start_time) * 1000, 2)
        finished_at = datetime.utcnow().isoformat()
        
        return AgentRun(
            run_id=run_id,
            agent=self.name,
            started_at=started_at,
            finished_at=finished_at,
            input_summary=f"Processed analysis for {self.name} with {len(self.tool_calls_trace)} tool calls.",
            tool_calls=self.tool_calls_trace,
            recommendations=recommendations,
            token_cost=self.total_tokens,
            api_cost_estimate=round(self.estimated_api_cost, 4),
            latency_ms=total_latency,
            status=run_status,
            error=error_msg
        )

    def execute_reasoning(self, input_context: Dict[str, Any]) -> List[Recommendation]:
        """Domain specific reasoning logic implemented by child agents."""
        raise NotImplementedError
