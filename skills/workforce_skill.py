def workforce_analysis(profile):

    budget = profile.get(
        "department_budget",
        0
    )

    workload = profile.get(
        "workload",
        "low"
    )


    if budget < 2000:
        decision = "Delay hiring"

    elif workload == "high":
        decision = "Consider employee"

    else:
        decision = "Use contractor"


    return {
        "workforce_recommendation": decision
    }