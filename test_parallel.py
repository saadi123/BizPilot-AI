import sys
import os
import json
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
walkthrough = blueprint.get("incorporation_walkthrough", {})

print("\n=== PARALLEL GROUP ASSIGNMENTS ===")
if isinstance(walkthrough, dict) and "steps" in walkthrough:
    for s in walkthrough["steps"]:
        pg = s.get("parallel_group", "MISSING")
        print(f"  parallel_group={pg!r:10} | step={s.get('step')} | {s.get('action')}")

    print("\n=== GROUPED ===")
    grouped = {}
    for i, s in enumerate(walkthrough["steps"]):
        key = s.get("parallel_group") or f"_solo_{i}"
        grouped.setdefault(key, []).append(s)
    for key, group in grouped.items():
        print(f"\n  Group '{key}' ({len(group)} steps):")
        for s in group:
            print(f"    - {s.get('action')}")
else:
    print("No steps found or walkthrough is not a dict.")
    print(repr(walkthrough))
