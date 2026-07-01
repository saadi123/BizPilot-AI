from skills.entity_skill import analyze_entity_options
from skills.tax_skill import generate_tax_readiness_plan
from skills.workforce_skill import workforce_analysis
from skills.accounting_skill import design_accounting_workflow
from skills.risk_skill import calculate_business_risk



profile = {

    "revenue":250000,

    "owners":1,

    "inventory":True,

    "employees":False,

    "multi_state":True,

    "department_budget":3000,

    "workload":"medium"

}


print(
    analyze_entity_options(profile)
)

print(
    generate_tax_readiness_plan(profile)
)

print(
    workforce_analysis(profile)
)

print(
    design_accounting_workflow(profile)
)

print(
    calculate_business_risk(profile)
)