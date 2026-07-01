import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator import run_business_architect

profile = {
    "industry": "Ecommerce",
    "revenue": 100000,
    "owners": 1,
    "state": "California",
    "inventory": True,
    "employees": False,
    "multi_state": False,
    "department_budget": 5000,
    "workload": "medium"
}

blueprint = run_business_architect(profile)

print("--- FLOWCHART ---")
print(repr(blueprint.get("flowchart")))

print("\n--- INCORPORATION WALKTHROUGH ---")
walkthrough = blueprint.get("incorporation_walkthrough", {})
print(repr(walkthrough.get("mermaid_flowchart")))
