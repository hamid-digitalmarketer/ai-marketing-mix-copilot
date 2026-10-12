"""
Tool Registry & Safety Guard for Marketing Mix Copilot
Enforces:
- Schema validation
- Least-privilege permissions: READ_ONLY vs WRITE_CAPABLE
- Execution timing & observability
- Graceful error containment
"""

import time
import inspect
from enum import Enum
from typing import Dict, Any, Callable, Optional, List
from pydantic import BaseModel


class ToolPermission(str, Enum):
    READ_ONLY = "read_only"
    WRITE_CAPABLE = "write_capable"


class ToolRecord(BaseModel):
    tool_name: str
    permission: ToolPermission
    inputs: Dict[str, Any]
    outputs: Any
    latency_ms: float
    status: str = "success"  # success, error, blocked
    error: Optional[str] = None


class ToolDefinition(BaseModel):
    name: str
    description: str
    permission: ToolPermission
    parameters_schema: Dict[str, Any]


class ToolRegistry:
    """Central registry for marketing mix & causal inference tools."""

    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._metadata: Dict[str, ToolDefinition] = {}

    def register(self, name: str, description: str, permission: ToolPermission = ToolPermission.READ_ONLY):
        """Decorator to register a tool with documentation and permissions."""
        def decorator(func: Callable):
            sig = inspect.signature(func)
            params = {}
            for param_name, param in sig.parameters.items():
                params[param_name] = {
                    "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any",
                    "default": str(param.default) if param.default != inspect.Parameter.empty else None
                }
            
            tool_def = ToolDefinition(
                name=name,
                description=description,
                permission=permission,
                parameters_schema=params
            )
            self._tools[name] = func
            self._metadata[name] = tool_def
            return func
        return decorator

    def execute(self, tool_name: str, allow_write: bool = False, **kwargs) -> ToolRecord:
        """Executes a registered tool within security and telemetry boundaries."""
        start_time = time.perf_counter()
        
        if tool_name not in self._tools:
            return ToolRecord(
                tool_name=tool_name,
                permission=ToolPermission.READ_ONLY,
                inputs=kwargs,
                outputs=None,
                latency_ms=0.0,
                status="error",
                error=f"Tool '{tool_name}' is not registered."
            )
            
        tool_meta = self._metadata[tool_name]
        
        # Human-in-the-loop Guardrail: block write-capable tools unless explicitly approved
        if tool_meta.permission == ToolPermission.WRITE_CAPABLE and not allow_write:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return ToolRecord(
                tool_name=tool_name,
                permission=tool_meta.permission,
                inputs=kwargs,
                outputs=None,
                latency_ms=latency_ms,
                status="blocked",
                error=f"Tool '{tool_name}' requires explicit human approval before execution."
            )

        try:
            func = self._tools[tool_name]
            result = func(**kwargs)
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return ToolRecord(
                tool_name=tool_name,
                permission=tool_meta.permission,
                inputs=kwargs,
                outputs=result,
                latency_ms=latency_ms,
                status="success"
            )
        except Exception as e:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return ToolRecord(
                tool_name=tool_name,
                permission=tool_meta.permission,
                inputs=kwargs,
                outputs=None,
                latency_ms=latency_ms,
                status="error",
                error=str(e)
            )

    def list_tools(self) -> List[ToolDefinition]:
        return list(self._metadata.values())


registry = ToolRegistry()
