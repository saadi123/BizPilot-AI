"""
documents/templates.py
Static text templates and copy used in PDF generation.
"""

DISCLAIMER = (
    "This document is informational and should be reviewed with a qualified "
    "legal, financial, or tax professional before making any business decisions."
)

COVER_TAGLINE = "AI-Powered Business Formation & Finance Roadmap"

SECTION_INTROS = {
    "Executive Summary": (
        "The following is an AI-generated overview of your business formation strategy. "
        "All recommendations are based on the profile you provided and should be validated "
        "with qualified professionals."
    ),
    "Entity Setup": (
        "Based on the information provided, the following entity structure analysis has been prepared. "
        "This is for informational purposes only and does not constitute legal advice."
    ),
    "Tax Readiness": (
        "The following tax readiness overview outlines the typical compliance requirements "
        "for your business type. Consult a CPA or enrolled agent for your specific situation."
    ),
    "Accounting Setup": (
        "The following accounting stack has been recommended based on your business profile, "
        "revenue level, and operational needs."
    ),
    "Workforce Planning": (
        "The following workforce analysis considers your budget, expected workload, "
        "and growth trajectory to recommend a hiring approach."
    ),
    "Compliance Checklist": (
        "The following checklist covers the key compliance steps required to legally "
        "form and operate your business. Timelines are estimates and may vary by jurisdiction."
    ),
    "30-Day Implementation Roadmap": (
        "The following week-by-week roadmap provides a practical starting point. "
        "Adjust timing based on your specific circumstances and professional guidance."
    ),
}

FOOTER_TEXT = (
    "© BizPilot AI · AI-Generated Business Formation Document · "
    "Not Legal, Financial, or Tax Advice"
)
