"""
Model Context Protocol (MCP) Adapter for Marketing Mix Copilot
Exports registered statistical and causal tools for consumption by standard MCP clients.
"""

from typing import Dict, Any, List
from tools.registry import registry


def export_mcp_tools() -> List[Dict[str, Any]]:
    """Exports all registered tools conforming to MCP tool specification."""
    mcp_tools = []
    for tool_def in registry.list_tools():
        properties = {}
        for param, info in tool_def.parameters_schema.items():
            type_str = "string"
            if "int" in info["type"]:
                type_str = "integer"
            elif "float" in info["type"]:
                type_str = "number"
            elif "bool" in info["type"]:
                type_str = "boolean"
            elif "dict" in info["type"] or "Dict" in info["type"]:
                type_str = "object"
            elif "list" in info["type"] or "List" in info["type"]:
                type_str = "array"

            properties[param] = {
                "type": type_str,
                "description": f"Parameter: {param}"
            }

        mcp_tools.append({
            "name": tool_def.name,
            "description": f"[{tool_def.permission.value.upper()}] {tool_def.description}",
            "inputSchema": {
                "type": "object",
                "properties": properties,
                "required": [p for p, info in tool_def.parameters_schema.items() if info["default"] is None]
            }
        })
    return mcp_tools


def handle_mcp_tool_call(tool_name: str, arguments: Dict[str, Any], allow_write: bool = False) -> Dict[str, Any]:
    """Handles an incoming MCP tool execution request."""
    record = registry.execute(tool_name, allow_write=allow_write, **arguments)
    return {
        "content": [
            {
                "type": "text",
                "text": str(record.outputs) if record.status == "success" else f"Error: {record.error}"
            }
        ],
        "isError": record.status != "success",
        "metadata": {
            "latency_ms": record.latency_ms,
            "permission": record.permission.value,
            "status": record.status
        }
    }
