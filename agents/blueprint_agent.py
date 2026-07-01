from utils.models import BusinessBlueprint


def generate_blueprint(results):


    blueprint = BusinessBlueprint(

        business_summary=
        results.get(
            "summary",
            "Ecommerce startup"
        ),


        entity_recommendation=
        results["entity"],


        workforce_plan=
        results["workforce"],


        accounting_stack=
        results["accounting"],


        tax_plan=
        results["tax"],


        integration_map=
        results["integration"],


        risk_score=
        results["risk"]["risk_score"],


        risk_level=
        results["risk"]["risk_level"]

    )


    return blueprint