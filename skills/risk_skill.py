def calculate_business_risk(profile):

    score = 0


    if profile.get("inventory"):
        score += 20


    if profile.get("employees"):
        score += 20


    if profile.get("multi_state"):
        score += 30


    if profile.get("high_revenue"):
        score += 30


    if score < 40:
        level = "Low"

    elif score < 70:
        level = "Medium"

    else:
        level = "High"


    return {

        "risk_score": score,

        "risk_level": level

    }