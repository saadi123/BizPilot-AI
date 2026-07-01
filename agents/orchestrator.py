import json
import re
from agents.entity_agent import entity_agent
from agents.tax_agent import tax_agent
from agents.workforce_agent import workforce_agent
from agents.accounting_agent import accounting_agent
from agents.integration_agent import integration_agent
from agents.incorporation_agent import incorporation_agent
from agents.coa_agent import coa_agent
from agents.document_agent import document_agent

from mcp_server.adk_tools import (
    entity_structure_tool,
    workforce_tool,
    accounting_stack_tool,
    tax_checklist_tool,
    integration_tool
)
from mcp_server.incorporation_urls import get_urls_for_state


def clean_json(text: str) -> str:
    """Extract and parse JSON block from LLM output, ignoring surrounding text."""
    # Find the first { and last }
    match = re.search(r'(\{.*\})', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback to finding [ and ]
    match = re.search(r'(\[.*\])', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def run_business_architect(profile: dict):
    """
    REAL multi-agent orchestration pipeline.
    Each step passes the business profile and state to specialized agents.
    State flows: Streamlit → Guardrails → Orchestrator → Agents → MCP tools → Blueprint
    """

    # -----------------------------
    # 1. ENTITY AGENT
    # State is passed here so the MCP tool can look up the state knowledge map.
    # -----------------------------
    entity_tool_output = entity_structure_tool(
        revenue=profile["revenue"],
        owners=profile["owners"],
        risk="medium",
        state=profile.get("state", "Unknown")
    )

    entity_reasoning_str = entity_agent.run(
        f"""
        Analyze this business profile and explain entity recommendation:
        {profile}
        Tool output: {entity_tool_output}
        """
    )

    try:
        entity_reasoning = json.loads(clean_json(entity_reasoning_str))
    except json.JSONDecodeError:
        entity_reasoning = {"raw_output": entity_reasoning_str}


    # -----------------------------
    # 2. WORKFORCE AGENT
    # -----------------------------
    workforce_tool_output = workforce_tool(
        budget=profile["department_budget"],
        workload=profile["workload"],
        revenue=profile["revenue"]
    )

    workforce_reasoning_str = workforce_agent.run(
        f"""
        Decide hiring strategy (employee vs contractor):
        Profile: {profile}
        Tool output: {workforce_tool_output}
        """
    )

    try:
        workforce_reasoning = json.loads(clean_json(workforce_reasoning_str))
    except json.JSONDecodeError:
        workforce_reasoning = {"raw_output": workforce_reasoning_str}


    # -----------------------------
    # 3. TAX AGENT
    # State tax environment is embedded in profile and passed to agent.
    # -----------------------------
    # Use the precise decision from the tool to avoid hallucinated/over-inclusive strings from LLM
    workforce_decision = ""
    if isinstance(workforce_tool_output, dict):
        workforce_decision = workforce_tool_output.get("decision", "")
    elif isinstance(workforce_tool_output, str):
        workforce_decision = workforce_tool_output

    entity_type = "LLC"
    if isinstance(entity_reasoning, dict):
        entity_type = entity_reasoning.get("recommended_structure", "LLC")

    tax_tool_output = tax_checklist_tool(
        structure=entity_type,
        state=profile.get("state", "Unknown"),
        workforce_decision=workforce_decision,
        revenue=profile.get("revenue", 0)
    )

    tax_reasoning_str = tax_agent.run(
        f"""
        Generate tax strategy and compliance checklist:
        Profile: {profile}
        Tool output: {tax_tool_output}
        """
    )

    try:
        tax_reasoning = json.loads(clean_json(tax_reasoning_str))
    except json.JSONDecodeError:
        tax_reasoning = {"raw_output": tax_reasoning_str}


    # -----------------------------
    # 4. ACCOUNTING AGENT
    # -----------------------------
    accounting_tool_output = accounting_stack_tool(
        revenue=profile["revenue"]
    )

    accounting_reasoning_str = accounting_agent.run(
        f"""
        Design accounting stack for ecommerce business:
        Profile: {profile}
        Tool output: {accounting_tool_output}
        """
    )

    try:
        accounting_reasoning = json.loads(clean_json(accounting_reasoning_str))
    except (json.JSONDecodeError, Exception):
        accounting_reasoning = {"raw_output": accounting_reasoning_str}


    # -----------------------------
    # 5. INTEGRATION AGENT
    # -----------------------------
    # Safely extract accounting stack
    accounting_stack = []
    if isinstance(accounting_tool_output, dict):
        accounting_stack = accounting_tool_output.get("recommended_stack", [])

    integration_output = integration_tool(
        workforce_decision=workforce_decision,
        accounting_stack=accounting_stack,
        sales_platforms=profile.get("sales_platforms", [])
    )

    integration_reasoning_str = integration_agent.run(
        f"""
        Design the integration and data flow section using the pre-computed mappings below.
        DO NOT invent new software or mappings. Reproduce the mappings EXACTLY as listed in the tool output.

        Sales Channel Mappings (already includes correct middleware): {integration_output.get('sales_channel_mappings', [])}
        Payment Processor Mappings: {integration_output.get('payment_mappings', [])}
        HR / Payroll Mappings: {integration_output.get('hr_mappings', [])}
        Main Accounting System: {integration_output.get('main_accounting', 'Accounting System')}
        """
    )

    try:
        integration_reasoning = json.loads(clean_json(integration_reasoning_str))
    except json.JSONDecodeError:
        integration_reasoning = {"raw_output": integration_reasoning_str}

    # -----------------------------
    # 7. INCORPORATION WALKTHROUGH AGENT
    # Generates an ordered, state+federal document checklist with response times and links.
    # Runs last because it depends on the entity recommendation from agent 1.
    # Verified URLs are injected from the URL knowledge base to prevent hallucination.
    # -----------------------------
    entity_type = entity_reasoning.get("recommended_structures", ["LLC"])[0] if isinstance(entity_reasoning, dict) else "LLC"
    url_map = get_urls_for_state(profile.get("state", "Unknown"))

    incorporation_str = incorporation_agent.run(
        f"""
        Generate a complete, ordered incorporation walkthrough for this business:
        State: {profile.get('state', 'Unknown')}
        Entity Type: {entity_type}
        Owners: {profile.get('owners', 1)}
        Industry: {profile.get('industry', 'Ecommerce')}
        Planning to hire employees: {profile.get('employees', False)}
        State analysis: {entity_tool_output.get('state_analysis', {})}

        VERIFIED URL REFERENCE MAP (use these URLs only — do not invent any):
        State URLs: {url_map['state_urls']}
        Federal URLs: {url_map['federal_urls']}
        """
    )

    try:
        incorporation_walkthrough = json.loads(clean_json(incorporation_str))
    except json.JSONDecodeError:
        incorporation_walkthrough = {"raw_output": incorporation_str}

    # -----------------------------
    # 8. CHART OF ACCOUNTS AGENT
    # -----------------------------
    coa_profile = {
        **profile,
        "entity_structure": entity_type
    }
    coa_data = {}
    for _ in range(3):
        coa_str = coa_agent.run(
            f"""
            Generate Chart of Accounts for:
            {json.dumps(coa_profile)}
            """
        )
        try:
            coa_data = json.loads(clean_json(coa_str))
            if isinstance(coa_data, dict) and "accounts" in coa_data:
                break
        except json.JSONDecodeError:
            coa_data = {"raw_output": coa_str}

    # -----------------------------
    # 9. DOCUMENT GENERATOR AGENT
    # Summarises all agent outputs into a founder-friendly structured document.
    # Runs last — depends on all prior agent results.
    # -----------------------------
    doc_input = {
        "profile": profile,
        "entity_analysis": entity_reasoning if isinstance(entity_reasoning, dict) else {},
        "tax_analysis": tax_reasoning if isinstance(tax_reasoning, dict) else {},
        "workforce_analysis": workforce_reasoning,
        "accounting_analysis": accounting_reasoning,
        "incorporation_walkthrough": {
            "total_time": incorporation_walkthrough.get("total_estimated_time", "N/A")
            if isinstance(incorporation_walkthrough, dict) else "N/A",
            "steps_count": len(incorporation_walkthrough.get("steps", []))
            if isinstance(incorporation_walkthrough, dict) else 0,
        },
    }

    document_package = {}
    for _ in range(3):
        doc_str = document_agent.run(
            f"""
            Generate the full founder-facing Business Launch Package from this blueprint:
            {json.dumps(doc_input)}
            """
        )
        try:
            document_package = json.loads(clean_json(doc_str))
            if isinstance(document_package, dict) and "sections" in document_package:
                break
        except json.JSONDecodeError:
            document_package = {"raw_output": doc_str}

    # -----------------------------
    # FINAL SYNTHESIS
    # -----------------------------
    final_blueprint = {
        "summary": f"{profile['industry']} business architecture in {profile.get('state', 'Unknown')}",
        "state_analysis": entity_tool_output.get("state_analysis", {}),
        "entity_analysis": entity_reasoning,
        "tax_analysis": tax_reasoning,
        "workforce_analysis": workforce_reasoning,
        "accounting_analysis": accounting_reasoning,
        "integration": integration_reasoning,
        "risks": "Standard execution risks apply.",
        "incorporation_walkthrough": incorporation_walkthrough,
        "chart_of_accounts": coa_data,
        "document_package": document_package,

        "raw_tool_outputs": {
            "entity_tool": entity_tool_output,
            "tax_tool": tax_tool_output,
            "workforce_tool": workforce_tool_output,
            "accounting_tool": accounting_tool_output
        }
    }

    return final_blueprint


class BusinessOrchestratorAgent:
    def __init__(self):
        self.name = "BusinessOrchestratorAgent"

    def run(self, profile):
        return run_business_architect(profile)


orchestrator = BusinessOrchestratorAgent()