import logging
import os
from mcp_server.tools import (
    recommend_entity_structure,
    recommend_accounting_stack,
    decide_workforce_model,
    generate_tax_checklist,
    generate_integration_map
)

# ─────────────────────────────────────────────
# LOGGER  (writes to logs/mcp_activity.log)
# Uses a dedicated FileHandler so it works even
# when Streamlit has already configured the root
# logger (basicConfig is a no-op in that case).
# ─────────────────────────────────────────────
import os
import logging
_log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "mcp_activity.log")
_log_dir = os.path.dirname(_log_path)

os.makedirs(
    _log_dir,
    exist_ok=True
)
logger = logging.getLogger("MCP")
logger.setLevel(logging.INFO)
# Only add the handler once (guards against module reload in Streamlit)
if not logger.handlers:
    _fh = logging.FileHandler(_log_path, encoding="utf-8")
    _fh.setFormatter(logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.addHandler(_fh)
    logger.propagate = False  # don't bubble up to Streamlit's root logger

class FinanceMCPServer:
    """
BizPilot AI Domain MCP Server

Provides business formation,
tax readiness, accounting and
workforce tools to AI agents.
"""
    def list_tools(self):

        return [
            {
                "name": "entity_structure",
                "description":
                "Analyzes business entity options based on founder profile"
            },
            {
                "name": "accounting_stack",
                "description":
                "Recommends accounting and ecommerce integrations"
            },
            {
                "name": "workforce",
                "description":
                "Determines employee vs contractor approach"
            },
            {
                "name": "tax_checklist",
                "description":
                "Generates tax readiness checklist"
            },
            {
                "name": "integration_map",
                "description":
                "Creates recommended software ecosystem"
            }
        ]

    def run_tool(self, tool_name: str, data: dict):

        tools = {
            "entity_structure": recommend_entity_structure,
            "accounting_stack": recommend_accounting_stack,
            "workforce": decide_workforce_model,
            "tax_checklist": generate_tax_checklist,
            "integration_map": generate_integration_map
        }

        if tool_name not in tools:
            logger.warning("MCP Tool Error: %s — not found in registry", tool_name)
            return {"error": "Tool not found"}

        # Build a concise context summary for the log
        ctx_parts = []
        for key in ("revenue", "state", "structure", "workforce_decision"):
            if key in data:
                ctx_parts.append(f"{key}={data[key]}")
        ctx = " | ".join(ctx_parts) if ctx_parts else "no context"

        logger.info("MCP Tool Called: %-20s | %s", tool_name, ctx)

        result = tools[tool_name](data)

        # Extract a one-liner summary from the result for the completion log
        summary = "ok"
        if isinstance(result, dict):
            for peek_key in ("recommended_structure", "decision", "main_accounting", "recommended_stack"):
                val = result.get(peek_key)
                if val:
                    summary = str(val)[:60]
                    break
            if summary == "ok" and "tax_forms_and_schedules" in result:
                summary = f"{len(result['tax_forms_and_schedules'])} tax forms"

        logger.info("MCP Tool Completed: %-18s | %s", tool_name, summary)

        return result