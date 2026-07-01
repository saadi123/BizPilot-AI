from agents.base_agent import create_agent
from mcp_server.adk_tools import accounting_stack_tool



accounting_agent = create_agent(

    name="AccountingStackAgent",

    instruction="""
Design ecommerce finance stack.

Recommend:
- ONE best-of-pick primary accounting software (DO NOT suggest multiple redundant options like both QuickBooks and Xero. Pick the single best fit for the business profile).
- Complementary systems (e.g., payment processors, dedicated inventory management if needed).
- Bookkeeping workflow.

Important: You can suggest multiple systems ONLY if they complement each other (e.g., Shopify + Stripe + QuickBooks). Never suggest overlapping tools for the core accounting ledger.
""",

    tools=[
        accounting_stack_tool
    ]

)