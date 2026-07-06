from agents.orchestrator import orchestrator
from agents.entity_agent import entity_agent
from agents.tax_agent import tax_agent
from agents.workforce_agent import workforce_agent
from agents.accounting_agent import accounting_agent
from agents.integration_agent import integration_agent


print("🚀 Loading BizPilot AI Agent System\n")


agents = [
    orchestrator,
    entity_agent,
    tax_agent,
    workforce_agent,
    accounting_agent,
    integration_agent
]


for agent in agents:
    print(
        f"✅ Agent Loaded: {agent.name}"
    )


print("\nTotal Agents:", len(agents))