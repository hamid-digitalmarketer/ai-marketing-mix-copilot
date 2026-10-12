"""
Tools Package Initialization for Marketing Mix Copilot
Loads all tool definitions into registry upon package import.
"""

from tools.registry import registry, ToolPermission, ToolRecord, ToolDefinition
import tools.data_quality_tools
import tools.modeling_tools
import tools.incrementality_tools
import tools.scenario_tools
import tools.explanation_tools
from tools.mcp_adapter import export_mcp_tools, handle_mcp_tool_call

__all__ = [
    "registry",
    "ToolPermission",
    "ToolRecord",
    "ToolDefinition",
    "export_mcp_tools",
    "handle_mcp_tool_call"
]
