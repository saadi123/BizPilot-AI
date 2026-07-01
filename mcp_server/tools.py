from dataclasses import dataclass
from typing import Dict, Any


# ---------------------------
# 1. ENTITY STRUCTURE TOOL
# ---------------------------
def recommend_entity_structure(data: Dict[str, Any]) -> Dict[str, Any]:
    revenue = data.get("revenue", 0)
    owners = data.get("owners", 1)
    risk = data.get("risk", "low")
    state = data.get("state", "Unknown")

    if owners > 1:
        structure = "Multi-Member LLC"
        reason = "Multiple owners require clear liability + profit split structure"
    elif revenue > 120000:
        structure = "S-Corporation (future election)"
        reason = "High profit threshold makes S-Corp tax structure beneficial"
    else:
        structure = "Single Member LLC"
        reason = "Simple structure for early-stage business"

    state_map = {
        "California": {
            "state": "California",
            "incorporation_notes": "Higher compliance complexity and administrative burden.",
            "compliance_complexity": "High",
            "tax_environment": "High corporate and personal tax rates.",
            "business_friendliness_score": 4
        },
        "Texas": {
            "state": "Texas",
            "incorporation_notes": "Business-friendly environment.",
            "compliance_complexity": "Medium",
            "tax_environment": "No personal state income tax.",
            "business_friendliness_score": 8
        },
        "Florida": {
            "state": "Florida",
            "incorporation_notes": "Popular for small businesses.",
            "compliance_complexity": "Low",
            "tax_environment": "No personal state income tax.",
            "business_friendliness_score": 9
        },
        "Delaware": {
            "state": "Delaware",
            "incorporation_notes": "Startup-friendly incorporation environment.",
            "compliance_complexity": "Low",
            "tax_environment": "No sales tax, specialized corporate franchise tax.",
            "business_friendliness_score": 10
        },
        "Nevada": {
            "state": "Nevada",
            "incorporation_notes": "Strong privacy laws and business protections.",
            "compliance_complexity": "Low",
            "tax_environment": "No state income tax.",
            "business_friendliness_score": 9
        },
        "Wyoming": {
            "state": "Wyoming",
            "incorporation_notes": "LLC-friendly environment.",
            "compliance_complexity": "Low",
            "tax_environment": "No state corporate or personal income tax.",
            "business_friendliness_score": 9
        },
        "New York": {
            "state": "New York",
            "incorporation_notes": "Higher compliance complexity and publication requirements.",
            "compliance_complexity": "High",
            "tax_environment": "High tax rates in certain localities.",
            "business_friendliness_score": 5
        }
    }
    
    state_info = state_map.get(state, {
        "state": state,
        "incorporation_notes": "Standard rules apply.",
        "compliance_complexity": "Medium",
        "tax_environment": "Standard state taxes apply.",
        "business_friendliness_score": 5
    })

    return {
        "recommended_structure": structure,
        "reason": reason,
        "state_analysis": state_info
    }


# ---------------------------
# 2. ACCOUNTING STACK TOOL
# ---------------------------
def recommend_accounting_stack(data: Dict[str, Any]) -> Dict[str, Any]:
    revenue = data.get("revenue", 0)

    if revenue < 50000:
        stack = ["Shopify", "Stripe", "Excel / Google Sheets"]
    elif revenue < 200000:
        stack = ["Shopify", "QuickBooks Online", "Stripe", "PayPal"]
    else:
        stack = ["Shopify", "QuickBooks Advanced", "NetSuite (future)", "BI Dashboard"]

    return {
        "recommended_stack": stack
    }


# ---------------------------
# 3. WORKFORCE DECISION TOOL
# ---------------------------
def decide_workforce_model(data: Dict[str, Any]) -> Dict[str, Any]:
    budget = data.get("budget", 0)
    workload = data.get("workload", "low")
    revenue = data.get("revenue", 0)

    # For larger scale businesses, suggest a hybrid mix
    if revenue > 5000000 or budget > 50000:
        decision = "Hybrid (Employee + Contractor)"
        reason = "At this scale, a mix of full-time core employees for stability and specialized contractors for flexibility is optimal."
    elif budget < 2000:
        decision = "No Hire - Automate or Delay"
        reason = "Budget too low for sustainable hiring"
    elif budget < 5000:
        decision = "Contractor"
        reason = "Flexible cost structure suitable for early-stage"
    else:
        if workload == "high":
            decision = "Full-Time Employee"
            reason = "Stable workload + sufficient budget"
        else:
            decision = "Contractor (Scalable)"
            reason = "Budget allows flexibility before committing to payroll"

    return {
        "decision": decision,
        "reason": reason
    }


# ---------------------------
# 4. TAX CHECKLIST TOOL
# ---------------------------
def generate_tax_checklist(data: Dict[str, Any]) -> Dict[str, Any]:
    structure = data.get("structure", "LLC")
    state = data.get("state", "Unknown")
    workforce_decision = data.get("workforce_decision", "")
    revenue = data.get("revenue", 0)

    checklist = [
        "Separate business bank account required",
        "Track all business expenses with receipts",
        "Maintain monthly bookkeeping reconciliation"
    ]

    tax_forms = []

    # Entity structure forms
    tax_forms.append("Form 1040 (U.S. Individual Income Tax Return) - Due April 15 (Each individual owner must file their own personal return)")
    
    if "S-Corporation" in structure or "C-Corporation" in structure:
        checklist.append("Run payroll for owner salary")
        checklist.append("Maintain reasonable compensation documentation")
        tax_forms.append("Form 1120-S (U.S. Income Tax Return for an S Corporation) - Due March 15")
    elif "Multi-Member LLC" in structure:
        tax_forms.append("Form 1065 (U.S. Return of Partnership Income) - Due March 15")
        tax_forms.append("Schedule K-1 (Partner's Share of Income) - Due March 15")
    elif "Single Member LLC" in structure or "Sole Proprietor" in structure:
        tax_forms.append("Form 1040 Schedule C (Profit or Loss from Business) - Due April 15")
        
    if "Corporation" not in structure:
        if revenue < 250000: # Threshold for corporate tax returns for simplicity
            checklist.append("Note: Income is currently below the threshold to prepare corporate tax returns.")
    elif revenue < 250000 and "Corporation" in structure:
        checklist.append("Note: While a corporate return is required, you are below the $250,000 threshold for filing Schedules L, M-1, and M-2.")

    # Workforce forms
    if "Contractor" in workforce_decision:
        tax_forms.append("Form 1099-NEC (Nonemployee Compensation) - Due Jan 31 (if contractor is US-based)")
        tax_forms.append("Form 1096 (Annual Summary and Transmittal) - Due Jan 31")
    if "Employee" in workforce_decision:
        tax_forms.append("Form W-2 (Wage and Tax Statement) - Due Jan 31")
        tax_forms.append("Form W-3 (Transmittal of Wage and Tax Statements) - Due Jan 31")
        tax_forms.append("Form 941 (Employer's Quarterly Federal Tax Return) - Due Quarterly")
        tax_forms.append("Form 940 (Employer's Annual Federal Unemployment Tax Return) - Due Jan 31")
        tax_forms.append(f"{state} State Unemployment Insurance (SUI) & Withholding - Check state specific quarterly due dates")

    # State specific forms
    state_upper = state.upper()
    if state_upper == "CALIFORNIA":
        tax_forms.append("California Form 3522 (LLC Tax Voucher) - Due 15th day of 4th month ($800 minimum)")
        tax_forms.append("California Form 568 (LLC Return of Income) - Due 15th day of 4th month")
    elif state_upper == "DELAWARE":
        tax_forms.append("Delaware Franchise Tax - Due June 1 for LLCs, March 1 for Corporations")
    elif state_upper == "TEXAS":
        tax_forms.append("Texas Franchise Tax Report - Due May 15")
    elif state_upper == "NEW YORK":
        tax_forms.append("New York IT-204-LL (Partnership, LLC, and LLP filing fee) - Due 15th day of 3rd month")
    elif state_upper == "FLORIDA":
        tax_forms.append("Florida Corporate Income Tax Return (Form F-1120) - Due 1st day of 5th month (if applicable)")
        tax_forms.append("Florida Annual Report - Due May 1")
    elif state_upper == "NEVADA":
        tax_forms.append("Nevada Annual List & State Business License - Due annually by incorporation month end")
    elif state_upper == "WYOMING":
        tax_forms.append("Wyoming Annual Report & License Tax - Due 1st day of your incorporation month")

    return {
        "tax_checklist": checklist,
        "tax_forms_and_schedules": tax_forms
    }


# ---------------------------
# 5. INTEGRATION TOOL
# ---------------------------

# Platforms that need middleware to integrate cleanly with accounting software.
# Key = platform identifier (lowercase), Value = (middleware_name, direct_or_not)
# direct=True means a native integration exists; direct=False means middleware is required.
PLATFORM_MIDDLEWARE = {
    "amazon":    ("A2X", False),
    "shopify":   ("A2X or Synder", False),
    "etsy":      ("Link My Books", False),
    "woocommerce": ("Synder", False),
    "own website": ("Synder", False),
    "stripe":    (None, True),   # Native QBO/Xero connector exists
    "paypal":    ("PayTraQer", False),
    "square":    (None, True),   # Native connector exists
}

def generate_integration_map(data: Dict[str, Any]) -> Dict[str, Any]:
    workforce_decision = data.get("workforce_decision", "")
    accounting_stack = data.get("accounting_stack", ["Accounting System"])
    sales_platforms = data.get("sales_platforms", [])

    # Extract primary accounting software name
    main_accounting = "Accounting System"
    for software in ["QuickBooks Advanced", "QuickBooks Online", "QuickBooks", "NetSuite", "Xero"]:
        if any(software.lower() in str(item).lower() for item in accounting_stack):
            main_accounting = next(item for item in accounting_stack if software.split()[0].lower() in str(item).lower())
            break

    # Build per-platform integration chains
    sales_channel_mappings = []
    for platform in sales_platforms:
        key = platform.lower()
        match = PLATFORM_MIDDLEWARE.get(key)
        if match:
            middleware, is_direct = match
            if is_direct or middleware is None:
                sales_channel_mappings.append(f"{platform} -----> {main_accounting} (native connector)")
            else:
                sales_channel_mappings.append(f"{platform} -----> {middleware} -----> {main_accounting}")
        else:
            # Unknown platform — flag that middleware may be needed
            sales_channel_mappings.append(f"{platform} -----> [Check middleware availability] -----> {main_accounting}")

    # Payment processors
    payment_mappings = []
    for proc in ["Stripe", "PayPal", "Square", "Klarna/Afterpay"]:
        key = proc.lower().split("/")[0]
        match = PLATFORM_MIDDLEWARE.get(key)
        if match and not match[1]:  # needs middleware
            payment_mappings.append(f"{proc} -----> {match[0]} -----> {main_accounting}")
        else:
            payment_mappings.append(f"{proc} -----> {main_accounting} (native connector)")

    # HR/Payroll mappings
    hr_mappings = []
    if "Employee" in workforce_decision and "Contractor" in workforce_decision:
        hr_mappings.append(f"Gusto/Rippling (Employees) -----> {main_accounting} (Payroll Journal Entries)")
        hr_mappings.append(f"Deel/Bill.com (Contractors) -----> {main_accounting} (Expense Sync)")
    elif "Employee" in workforce_decision:
        hr_mappings.append(f"Gusto or Rippling -----> {main_accounting} (Payroll Journal Entries)")
    elif "Contractor" in workforce_decision:
        hr_mappings.append(f"Deel or Bill.com -----> {main_accounting} (Expense Sync)")

    return {
        "main_accounting": main_accounting,
        "sales_channel_mappings": sales_channel_mappings,
        "payment_mappings": payment_mappings,
        "hr_mappings": hr_mappings,
    }