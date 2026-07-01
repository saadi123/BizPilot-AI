"""
security/guardrails.py
Context-aware STRIDE security guardrail for BizPilot AI.

Architecture:
    Streamlit Input
          |
          v
    GuardrailManager.validate_profile()
          |
     ---------------------
     |                   |
  PII Scan          STRIDE Checks
          |
          v
    Orchestrator → Agents → MCP Tools → LLM
          |
    Output Guardrail
          |
    PDF Generator

STRIDE Threats mitigated here:
    - Information Disclosure: PII & credential leakage detection BEFORE data reaches agents
    - Tampering: Prompt injection & jailbreak detection
"""

import re
from typing import Any, Dict, List, Tuple


# ─────────────────────────────────────────────────────────
# RISK LEVELS
# ─────────────────────────────────────────────────────────
RISK_LOW    = "LOW"     # Log-only, proceed
RISK_MEDIUM = "MEDIUM"  # Warn user, proceed with caution
RISK_HIGH   = "HIGH"    # Block immediately


class GuardrailManager:
    """
    Context-aware security guardrail.

    Instead of naively scanning all text for any 9-digit sequence (which
    would false-positive on revenue=$100,000,000), we validate each field
    of the profile dictionary according to its expected type and purpose.

    Risk Levels
    -----------
    HIGH   → Block. Credential leak, SSN, prompt injection.
    MEDIUM → Warn. Suspicious pattern, but not conclusive.
    LOW    → Allowed. Proceed normally.
    """

    # ──────────────────────────────────────────────────────
    # PUBLIC: PROFILE VALIDATION (main entry point)
    # ──────────────────────────────────────────────────────
    def validate_profile(self, profile: dict) -> Dict[str, Any]:
        """
        Field-aware profile validation. Each field is validated according
        to its expected data type to minimise false positives.

        Returns
        -------
        {
            "safe":   bool,
            "risk":   "LOW" | "MEDIUM" | "HIGH",
            "issues": ["description", ...],
            "reason": str  # primary reason (first HIGH, or first issue)
        }
        """
        issues: List[Tuple[str, str]] = []  # (risk_level, description)

        # ── 1. Numeric-only fields ──────────────────────────────────────
        # These should ONLY contain numbers; we only check for credit cards
        # because SSNs and bank accounts are not expected here.
        numeric_fields = {
            "revenue":           "Revenue",
            "owners":            "Number of owners",
            "department_budget": "Department budget",
        }
        for field_key, field_label in numeric_fields.items():
            value = str(profile.get(field_key, ""))
            if self._detect_credit_card(value):
                issues.append((RISK_HIGH, f"Possible credit card number in '{field_label}' field"))

        # ── 2. Short text fields ────────────────────────────────────────
        # State, industry — just check for injections
        text_fields = {
            "industry": "Industry",
            "state":    "State",
            "workload": "Workload",
        }
        for field_key, field_label in text_fields.items():
            value = str(profile.get(field_key, ""))
            if self._detect_prompt_injection(value):
                issues.append((RISK_HIGH, f"Prompt injection attempt in '{field_label}' field"))

        # ── 3. Full profile scan (context-aware) ───────────────────────
        # Convert entire profile to a string for catch-all scans.
        # Bank account detection only fires when BANKING CONTEXT is present
        # (e.g. "account number: 123456789012"), so revenue alone won't trigger.
        full_text = str(profile)

        if self._detect_ssn(full_text):
            issues.append((RISK_HIGH, "Social Security Number (SSN) detected"))

        if self._detect_api_key(full_text):
            issues.append((RISK_HIGH, "API key or secret credential detected"))

        if self._detect_bank_account_in_context(full_text):
            issues.append((RISK_HIGH, "Bank account number detected with banking context"))

        if self._detect_prompt_injection(full_text):
            # May already be caught above; dedup by risk level logic below
            issues.append((RISK_HIGH, "Prompt injection attempt detected in input"))

        # ── 4. Aggregate risk ──────────────────────────────────────────
        return self._build_result(issues)

    # ──────────────────────────────────────────────────────
    # PUBLIC: LEGACY TEXT VALIDATION (kept for backward compatibility)
    # Used by the PDF download guard and other single-string checks.
    # ──────────────────────────────────────────────────────
    def validate_input(self, text: str) -> Dict[str, Any]:
        """
        Lightweight single-string validation used outside profile context
        (e.g. scanning a document package string before PDF generation).
        """
        if not text or not isinstance(text, str):
            return {"safe": False, "risk": RISK_HIGH, "reason": "Empty or invalid input", "issues": []}

        issues: List[Tuple[str, str]] = []

        if self._detect_ssn(text):
            issues.append((RISK_HIGH, "SSN detected"))
        if self._detect_api_key(text):
            issues.append((RISK_HIGH, "API key or credential detected"))
        if self._detect_bank_account_in_context(text):
            issues.append((RISK_HIGH, "Bank account in banking context detected"))
        if self._detect_prompt_injection(text):
            issues.append((RISK_HIGH, "Prompt injection attempt detected"))

        return self._build_result(issues)

    # ──────────────────────────────────────────────────────
    # PUBLIC: OUTPUT NORMALIZATION
    # ──────────────────────────────────────────────────────
    def validate_output(self, response: Any) -> Dict[str, Any]:
        """Attach disclaimer to any agent output."""
        disclaimer = (
            "AI-generated recommendation. "
            "This is not financial or legal advice. "
            "Verify with a qualified professional."
        )
        if isinstance(response, dict):
            response["disclaimer"] = disclaimer
            return response
        return {"result": str(response), "disclaimer": disclaimer}

    # ──────────────────────────────────────────────────────
    # STRIDE DETECTORS
    # ──────────────────────────────────────────────────────
    def _detect_ssn(self, text: str) -> bool:
        """Detects formatted SSNs: 123-45-6789"""
        return bool(re.search(r"\b\d{3}-\d{2}-\d{4}\b", text))

    def _detect_credit_card(self, text: str) -> bool:
        """
        Detects credit card numbers (13-16 digits with optional spaces/dashes).
        Applied only to numeric fields to avoid false positives on revenue.
        """
        # Strip spaces/dashes then check if 13-16 contiguous digits remain
        stripped = re.sub(r"[\s\-]", "", text)
        return bool(re.fullmatch(r"\d{13,16}", stripped))

    def _detect_bank_account_in_context(self, text: str) -> bool:
        """
        Context-aware: only fires when banking keywords appear near a long number.
        Revenue=100000000 will NOT trigger this — no banking context present.
        """
        pattern = r"""
            (?:account|acct|bank\s*account|routing|iban|sort\s*code)
            [\s:=#\-]*
            \d{8,17}
        """
        return bool(re.search(pattern, text, re.I | re.X))

    def _detect_api_key(self, text: str) -> bool:
        """
        Detects well-known API key formats:
          - OpenAI: sk-...
          - Google: AIza...
          - xAI/Groq: xai-..., gsk_...
          - Generic bearer tokens
        """
        patterns = [
            r"sk-[a-zA-Z0-9]{20,}",
            r"AIza[0-9A-Za-z\-_]{20,}",
            r"xai-[a-zA-Z0-9]{10,}",
            r"gsk_[a-zA-Z0-9]{10,}",
            r"Bearer\s+[a-zA-Z0-9\-._~+/]{20,}",
        ]
        return any(re.search(p, text) for p in patterns)

    def _detect_prompt_injection(self, text: str) -> bool:
        """Detects common prompt injection / jailbreak patterns."""
        keywords = [
            "ignore previous instructions",
            "ignore all instructions",
            "reveal system prompt",
            "act as admin",
            "bypass safety",
            "disregard your instructions",
            "you are now",
            "pretend you are",
            "jailbreak",
            "dan mode",
        ]
        lower = text.lower()
        return any(kw in lower for kw in keywords)

    # ──────────────────────────────────────────────────────
    # HELPERS
    # ──────────────────────────────────────────────────────
    def _build_result(self, issues: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Aggregate issues into a final result dict with the highest risk level."""
        if not issues:
            return {"safe": True, "risk": RISK_LOW, "issues": [], "reason": "Input approved"}

        # Dedup descriptions
        seen = set()
        unique_issues = []
        for level, desc in issues:
            if desc not in seen:
                seen.add(desc)
                unique_issues.append((level, desc))

        # Determine highest risk
        risk_order = {RISK_LOW: 0, RISK_MEDIUM: 1, RISK_HIGH: 2}
        max_risk = max(unique_issues, key=lambda x: risk_order.get(x[0], 0))[0]

        safe = max_risk != RISK_HIGH
        descriptions = [desc for _, desc in unique_issues]

        return {
            "safe":   safe,
            "risk":   max_risk,
            "issues": descriptions,
            "reason": descriptions[0],  # Primary reason for UI display
        }