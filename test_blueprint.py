from dotenv import load_dotenv
load_dotenv()

from agents.orchestrator import run_business_architect



profile = {

    "industry":
    "Ecommerce",


    "revenue":
    250000,


    "owners":
    1,


    "state":
    "Texas",


    "inventory":
    True,


    "employees":
    False,


    "multi_state":
    True,


    "department_budget":
    3000,


    "workload":
    "medium"

}



result = run_business_architect(profile)


print(result)