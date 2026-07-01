from mcp_server.server import FinanceMCPServer


mcp = FinanceMCPServer()


def entity_structure_tool(
    revenue: int,
    owners: int,
    risk: str,
    state: str
):

    return mcp.run_tool(
        "entity_structure",
        {
            "revenue": revenue,
            "owners": owners,
            "risk": risk,
            "state": state
        }
    )


def accounting_stack_tool(
    revenue: int
):

    return mcp.run_tool(
        "accounting_stack",
        {
            "revenue": revenue
        }
    )


def workforce_tool(
    budget: int,
    workload: str,
    revenue: int
):

    return mcp.run_tool(
        "workforce",
        {
            "budget": budget,
            "workload": workload,
            "revenue": revenue
        }
    )


def tax_checklist_tool(
    structure: str,
    state: str,
    workforce_decision: str,
    revenue: int
):

    return mcp.run_tool(
        "tax_checklist",
        {
            "structure": structure,
            "state": state,
            "workforce_decision": workforce_decision,
            "revenue": revenue
        }
    )


def integration_tool(
    workforce_decision: str,
    accounting_stack: list,
    sales_platforms: list
):

    return mcp.run_tool(
        "integration_map",
        {
            "workforce_decision": workforce_decision,
            "accounting_stack": accounting_stack,
            "sales_platforms": sales_platforms
        }
    )