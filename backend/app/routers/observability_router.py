"""
Observability & Telemetry API Router
Exposes token usage, cost controls, latency, tool call traces, and MCP adapters.
"""

from typing import Dict, Any
from pydantic import BaseModel
from fastapi import APIRouter
from agents.orchestrator import copilot_orchestrator
from tools.mcp_adapter import export_mcp_tools, handle_mcp_tool_call

router = APIRouter(prefix="/api/observability", tags=["Observability & Telemetry"])


class MCPCallRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    allow_write: bool = False


@router.get("/stats")
def get_system_stats():
    """Returns aggregated observability telemetry across all agent runs."""
    runs = copilot_orchestrator.runs_history
    total_runs = len(runs)
    total_tokens = sum(r.token_cost for r in runs)
    total_cost = sum(r.api_cost_estimate for r in runs)
    avg_latency = round(sum(r.latency_ms for r in runs) / total_runs, 2) if total_runs > 0 else 0.0

    all_tool_calls = []
    for r in runs:
        all_tool_calls.extend(r.tool_calls)

    total_calls = len(all_tool_calls)
    successful_calls = len([c for c in all_tool_calls if c.get("status") == "success"])
    tool_success_rate = round((successful_calls / total_calls) * 100, 2) if total_calls > 0 else 100.0

    return {
        "total_agent_runs": total_runs,
        "total_tokens_consumed": total_tokens,
        "estimated_api_cost_usd": round(total_cost, 4),
        "average_run_latency_ms": avg_latency,
        "total_tool_executions": total_calls,
        "tool_success_rate_pct": tool_success_rate,
        "demo_mode_active": copilot_orchestrator.demo_mode,
        "cost_controls": "ACTIVE (Rule-based zero-cost mode enabled)" if copilot_orchestrator.demo_mode else "LIVE_API_METERED"
    }


@router.get("/traces")
def get_execution_traces():
    """Returns granular tool call logs for debugging and auditing."""
    traces = []
    for r in copilot_orchestrator.runs_history:
        for call in r.tool_calls:
            traces.append({
                "run_id": r.run_id,
                "agent": r.agent,
                **call
            })
    return traces


@router.get("/mcp/tools")
def get_mcp_tools():
    """Exposes all registered tools in standard Model Context Protocol (MCP) schema."""
    return export_mcp_tools()


@router.post("/mcp/call")
def call_mcp_tool(req: MCPCallRequest):
    """Executes a tool call using the Model Context Protocol."""
    return handle_mcp_tool_call(req.tool_name, req.arguments, allow_write=req.allow_write)
