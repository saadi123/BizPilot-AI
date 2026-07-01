# Verified filing URLs and PDF links for each supported state + federal forms.
# These are injected into the IncorporationAgent prompt so the LLM never has to guess URLs.
# Update this map as agencies change their portals.

INCORPORATION_URLS = {

    # ─────────────────────────────────────────────
    # FEDERAL (IRS)
    # ─────────────────────────────────────────────
    "federal": {
        "EIN Application (Online)": {
            "filing_url": "https://www.irs.gov/businesses/small-businesses-self-employed/apply-for-an-employer-identification-number-ein-online",
            "pdf_url":    "https://www.irs.gov/pub/irs-pdf/fss4.pdf",
            "form_name":  "IRS Form SS-4"
        },
        "S-Corp Election": {
            "filing_url": "https://www.irs.gov/forms-pubs/about-form-2553",
            "pdf_url":    "https://www.irs.gov/pub/irs-pdf/f2553.pdf",
            "form_name":  "IRS Form 2553"
        },
        "Entity Classification Election": {
            "filing_url": "https://www.irs.gov/forms-pubs/about-form-8832",
            "pdf_url":    "https://www.irs.gov/pub/irs-pdf/f8832.pdf",
            "form_name":  "IRS Form 8832"
        },
        "Beneficial Ownership Information (BOI)": {
            "filing_url": "https://boiefiling.fincen.gov/",
            "pdf_url":    "https://www.fincen.gov/sites/default/files/shared/BOI_Small_Compliance_Guide.pdf",
            "form_name":  "FinCEN BOI Report"
        },
    },

    # ─────────────────────────────────────────────
    # CALIFORNIA
    # ─────────────────────────────────────────────
    "California": {
        "Articles of Organization": {
            "filing_url": "https://bizfileonline.sos.ca.gov/",
            "pdf_url":    "https://www.sos.ca.gov/business-programs/business-entities/forms/limited-liability-company-forms",
            "form_name":  "CA Form LLC-1"
        },
        "Statement of Information": {
            "filing_url": "https://bizfileonline.sos.ca.gov/",
            "pdf_url":    "https://www.sos.ca.gov/business-programs/business-entities/forms/limited-liability-company-forms",
            "form_name":  "CA Form LLC-12"
        },
        "Business License": {
            "filing_url": "https://business.ca.gov/california-business-portal/",
            "pdf_url":    "https://business.ca.gov/california-business-portal/",
            "form_name":  "California Business License"
        },
        "Registered Agent Designation": {
            "filing_url": "https://bizfileonline.sos.ca.gov/",
            "pdf_url":    "https://www.sos.ca.gov/business-programs/business-entities/forms",
            "form_name":  "CA Registered Agent Form"
        },
    },

    # ─────────────────────────────────────────────
    # TEXAS
    # ─────────────────────────────────────────────
    "Texas": {
        "Certificate of Formation": {
            "filing_url": "https://www.sos.state.tx.us/corp/online_filings.shtml",
            "pdf_url":    "https://www.sos.state.tx.us/corp/forms/205_boc.pdf",
            "form_name":  "TX Form 205"
        },
        "Registered Agent Consent": {
            "filing_url": "https://www.sos.state.tx.us/corp/online_filings.shtml",
            "pdf_url":    "https://www.sos.state.tx.us/corp/forms/401_boc.pdf",
            "form_name":  "TX Form 401"
        },
        "Texas Business License / Sales Tax Permit": {
            "filing_url": "https://comptroller.texas.gov/taxes/permit/",
            "pdf_url":    "https://comptroller.texas.gov/taxes/permit/",
            "form_name":  "Texas Sales and Use Tax Permit"
        },
        "Franchise Tax Registration": {
            "filing_url": "https://comptroller.texas.gov/taxes/franchise/",
            "pdf_url":    "https://comptroller.texas.gov/taxes/franchise/",
            "form_name":  "Texas Franchise Tax"
        },
    },

    # ─────────────────────────────────────────────
    # FLORIDA
    # ─────────────────────────────────────────────
    "Florida": {
        "Articles of Organization": {
            "filing_url": "https://dos.myflorida.com/sunbiz/manage-e-file/",
            "pdf_url":    "https://dos.fl.gov/media/693739/llc_articles_of_org.pdf",
            "form_name":  "FL Articles of Organization"
        },
        "Registered Agent Designation": {
            "filing_url": "https://dos.myflorida.com/sunbiz/manage-e-file/",
            "pdf_url":    "https://dos.fl.gov/media/693739/llc_articles_of_org.pdf",
            "form_name":  "FL Registered Agent Section (within Articles)"
        },
        "Annual Report": {
            "filing_url": "https://dos.myflorida.com/sunbiz/manage-e-file/annual-report/",
            "pdf_url":    "https://dos.myflorida.com/sunbiz/manage-e-file/annual-report/",
            "form_name":  "FL Annual Report"
        },
        "Business Tax Receipt": {
            "filing_url": "https://dos.myflorida.com/sunbiz/",
            "pdf_url":    "https://dos.myflorida.com/sunbiz/",
            "form_name":  "FL Local Business Tax Receipt"
        },
    },

    # ─────────────────────────────────────────────
    # NEW YORK
    # ─────────────────────────────────────────────
    "New York": {
        "Articles of Organization": {
            "filing_url": "https://apps.dos.ny.gov/publicInquiry/",
            "pdf_url":    "https://dos.ny.gov/system/files/documents/2024/01/1336.pdf",
            "form_name":  "NY DOS Form 1336"
        },
        "Publication Requirement": {
            "filing_url": "https://dos.ny.gov/guidance-documents/llc-publication-requirement",
            "pdf_url":    "https://dos.ny.gov/guidance-documents/llc-publication-requirement",
            "form_name":  "NY LLC Publication Notice"
        },
        "Registered Agent Designation": {
            "filing_url": "https://apps.dos.ny.gov/publicInquiry/",
            "pdf_url":    "https://dos.ny.gov/system/files/documents/2024/01/1336.pdf",
            "form_name":  "Included in NY DOS Form 1336"
        },
        "Certificate of Publication": {
            "filing_url": "https://apps.dos.ny.gov/publicInquiry/",
            "pdf_url":    "https://dos.ny.gov/system/files/documents/2024/01/1336-f.pdf",
            "form_name":  "NY DOS Form 1336-F"
        },
    },

    # ─────────────────────────────────────────────
    # DELAWARE
    # ─────────────────────────────────────────────
    "Delaware": {
        "Certificate of Formation": {
            "filing_url": "https://icis.corp.delaware.gov/Ecorp/EntitySearch/NameSearch.aspx",
            "pdf_url":    "https://corp.delaware.gov/pdf/llcform.pdf",
            "form_name":  "DE Certificate of Formation"
        },
        "Registered Agent Agreement": {
            "filing_url": "https://corp.delaware.gov/",
            "pdf_url":    "https://corp.delaware.gov/",
            "form_name":  "DE Registered Agent Agreement"
        },
        "Annual Franchise Tax Report": {
            "filing_url": "https://corp.delaware.gov/paytaxes.shtml",
            "pdf_url":    "https://corp.delaware.gov/paytaxes.shtml",
            "form_name":  "DE Franchise Tax Report"
        },
    },

    # ─────────────────────────────────────────────
    # NEVADA
    # ─────────────────────────────────────────────
    "Nevada": {
        "Articles of Organization": {
            "filing_url": "https://esos.nv.gov/",
            "pdf_url":    "https://www.nvsos.gov/sos/home/showpublisheddocument/888",
            "form_name":  "NV Articles of Organization"
        },
        "Initial List of Managers / Members": {
            "filing_url": "https://esos.nv.gov/",
            "pdf_url":    "https://www.nvsos.gov/sos/home/showpublisheddocument/892",
            "form_name":  "NV Initial List"
        },
        "State Business License": {
            "filing_url": "https://esos.nv.gov/",
            "pdf_url":    "https://www.nvsos.gov/sos/home/showpublisheddocument/892",
            "form_name":  "NV State Business License"
        },
    },

    # ─────────────────────────────────────────────
    # WYOMING
    # ─────────────────────────────────────────────
    "Wyoming": {
        "Articles of Organization": {
            "filing_url": "https://wyobiz.wyo.gov/",
            "pdf_url":    "https://sos.wyo.gov/Forms/Business/LLC/LLC-Articles.pdf",
            "form_name":  "WY Articles of Organization"
        },
        "Registered Agent Consent": {
            "filing_url": "https://wyobiz.wyo.gov/",
            "pdf_url":    "https://sos.wyo.gov/Forms/Business/LLC/LLC-Articles.pdf",
            "form_name":  "WY Registered Agent Consent (included in Articles)"
        },
        "Annual Report": {
            "filing_url": "https://wyobiz.wyo.gov/",
            "pdf_url":    "https://sos.wyo.gov/Forms/Business/AnnualReport/AR-LimitedLiabilityCompany.pdf",
            "form_name":  "WY Annual Report"
        },
    },
}


def get_urls_for_state(state: str) -> dict:
    """Return combined federal + state URL map for the given state."""
    state_urls = INCORPORATION_URLS.get(state, {})
    federal_urls = INCORPORATION_URLS.get("federal", {})
    return {
        "state_urls": state_urls,
        "federal_urls": federal_urls,
    }
