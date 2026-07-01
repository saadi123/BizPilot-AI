def generate_tax_readiness_plan(profile):

    plan = [

        "Maintain separate business banking",

        "Track expenses with documentation",

        "Perform regular bookkeeping review"

    ]


    if profile.get("employees"):

        plan.append(
            "Establish payroll compliance workflow"
        )


    if profile.get("inventory"):

        plan.append(
            "Track inventory and cost of goods sold"
        )


    return {
        "tax_readiness_plan": plan
    }