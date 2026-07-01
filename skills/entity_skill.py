def analyze_entity_options(profile):

    revenue = profile.get("revenue",0)
    owners = profile.get("owners",1)
    liability = profile.get("liability","medium")


    recommendations = []


    if owners == 1:
        recommendations.append(
            "Single Member LLC may provide simplicity and liability separation"
        )


    if revenue > 120000:
        recommendations.append(
            "Evaluate whether S-Corporation election could be beneficial"
        )


    if liability == "high":
        recommendations.append(
            "Prioritize liability protection"
        )


    return {
        "entity_analysis": recommendations
    }