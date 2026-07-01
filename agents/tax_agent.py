from agents.base_agent import create_agent
from mcp_server.adk_tools import tax_checklist_tool



tax_agent = create_agent(

    name="TaxStrategyAgent",

    instruction="""

Create tax readiness checklist.
Analyze entity impact and state-level tax environment.
Keep output educational and avoid tax guarantees or legal advice.

CRITICAL: You MUST output ONLY valid JSON in the following exact format. Do not use markdown blocks:
{
 "tax_considerations": ["list", "of", "considerations"],
 "compliance_items": ["list", "of", "items"],
 "tax_forms_and_schedules": ["Include EXACT tax forms and due dates provided in the tool output"],
 "records_to_keep": ["list", "of", "records"]
}

Rule: Always include all forms from the `tax_forms_and_schedules` field of the Tool Output.
Rule: Explicitly suggest the names of individual tax returns (e.g., Form 1040) and explain that each individual should be filing it by their due date (e.g., April 15).
Rule: If the tool output indicates that income is below the threshold to prepare corporate tax returns or that schedules are not required due to the threshold, explicitly let the user know.
""",

    tools=[
        tax_checklist_tool
    ]

)