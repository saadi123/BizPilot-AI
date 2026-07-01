import streamlit as st
import streamlit.components.v1 as components
import html as html_mod
from dotenv import load_dotenv
load_dotenv()

from security.guardrails import GuardrailManager
from agents.orchestrator import run_business_architect
import json
from agents.coa_agent import coa_agent
from utils.coa_exporter import generate_qbo_csv
from documents.generator import generate_business_package, REPORTLAB_AVAILABLE


st.set_page_config(
    page_title="EcomFinance OS",
    layout="wide"
)

st.title("🚀 EcomFinance OS")
st.subheader("AI Business Formation & Finance Architect")

guard = GuardrailManager()



# -------------------------
# INPUT FORM
# -------------------------
st.markdown("### 🏢 Core Profile")
col1, col2, col3 = st.columns(3)
with col1:
    industry = st.selectbox("Industry", ["Ecommerce", "SaaS", "Services"])
with col2:
    state = st.selectbox("State of Incorporation", ["California", "Texas", "Florida", "New York", "Delaware", "Nevada", "Wyoming"])
with col3:
    revenue = st.number_input("Expected Annual Revenue ($)", min_value=0, step=10000)

st.markdown("### ⚙️ Operations & Budget")
col4, col5, col6 = st.columns(3)
with col4:
    owners = st.number_input("Number of Owners", min_value=1, value=1)
with col5:
    budget = st.number_input("Monthly Dept Budget ($)", min_value=0, step=1000)
with col6:
    workload = st.selectbox("Expected Workload", ["low", "medium", "high"])

st.markdown("### 📌 Characteristics")
col7, col8, col9 = st.columns(3)
with col7:
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    inventory = st.checkbox("📦 Inventory-based business")
with col8:
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    employees = st.checkbox("👥 Planning to hire employees")
with col9:
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    multi_state = st.checkbox("🌍 Multi-state operations")

st.markdown("<br>", unsafe_allow_html=True)



# -------------------------
# STATE SAFETY (IMPORTANT FIX)
# -------------------------
if "result" not in st.session_state:
    st.session_state.result = None

# -------------------------
# RUN BUTTON
# -------------------------
if st.button("Generate Business Blueprint"):

    # ── Build profile first so guardrail has full context ──
    profile_candidate = {
        "industry": industry,
        "revenue": revenue,
        "owners": owners,
        "state": state,
        "inventory": inventory,
        "employees": employees,
        "multi_state": multi_state,
        "department_budget": budget,
        "workload": workload,
        "sales_platforms": ["Shopify", "Amazon", "Etsy", "WooCommerce", "Own Website"],
        "payment_processors": ["Stripe", "PayPal", "Square", "Klarna/Afterpay"],
        "physical_assets": True,
        "business_loans": True,
        "home_office": True
    }

    # ── Context-aware STRIDE guardrail ──────────────────────
    validation = guard.validate_profile(profile_candidate)
    risk = validation.get("risk", "LOW")

    if risk == "HIGH":
        st.error(
            f"🚫 **Security check failed [{risk}]:** {validation['reason']}  \n"
            f"Please remove any sensitive credentials or PII before proceeding."
        )
        st.session_state.result = None

    else:
        if risk == "MEDIUM":
            issues_list = "  \n".join(f"• {i}" for i in validation.get("issues", []))
            st.warning(
                f"⚠️ **Security advisory [{risk}]:** Suspicious content detected.  \n"
                f"{issues_list}  \n"
                f"Proceeding with caution."
            )

        st.session_state.profile = profile_candidate

        import time
        status_box = st.empty()
        
        checks = [
            "Sensitive data detection",
            "Input validation",
            "Output filtering",
            "STRIDE review completed"
        ]
        
        style = """
        <style>
        .sec-spin {
            display: inline-block;
            width: 15px; height: 15px;
            border: 2px solid rgba(59,130,246,0.3);
            border-radius: 50%;
            border-top-color: #3b82f6;
            animation: sec-spin 0.8s ease-in-out infinite;
            margin-right: 8px;
            vertical-align: middle;
        }
        @keyframes sec-spin { to { transform: rotate(360deg); } }
        .sec-chk {
            display: inline-block;
            color: #10b981; font-weight: 900; margin-right: 8px; font-size:16px;
            vertical-align: middle; width: 15px; text-align: center;
        }
        .sec-text { font-family: 'Courier New', monospace; font-size: 14px; vertical-align: middle; color: inherit; opacity: 0.85; }
        .sec-text-active { font-family: 'Courier New', monospace; font-size: 14px; vertical-align: middle; color: #3b82f6; font-weight: 600; opacity: 1.0; }
        .sec-container {
            background-color: transparent; border: 1px solid rgba(128,128,128,0.2); border-radius: 8px; padding: 16px; margin-bottom: 20px;
        }
        </style>
        """
        
        completed_checks = []
        for check in checks:
            # Render state with current item spinning
            lines = [f"<div style='margin-bottom:6px;'><span class='sec-chk'>✓</span><span class='sec-text'>{c}</span></div>" for c in completed_checks]
            active_line = f"<div style='margin-bottom:6px;'><span class='sec-spin'></span><span class='sec-text-active'>{check}...</span></div>"
            status_box.markdown(f"{style}<div class='sec-container'>{''.join(lines)}{active_line}</div>", unsafe_allow_html=True)
            
            # Spin for 1.2s to add character and realistic delay
            time.sleep(1.2)
            completed_checks.append(check)
            
        # Final spinning state for the generation process
        lines = [f"<div style='margin-bottom:6px;'><span class='sec-chk'>✓</span><span class='sec-text'>{c}</span></div>" for c in completed_checks]
        final_loading = f"<div style='margin-top:12px; border-top:1px dashed rgba(128,128,128,0.3); padding-top:12px;'><span class='sec-spin'></span><span class='sec-text-active' style='color:#6366f1;'>Generating AI Business Blueprint...</span></div>"
        status_box.markdown(f"{style}<div class='sec-container'>{''.join(lines)}{final_loading}</div>", unsafe_allow_html=True)

        result = run_business_architect(st.session_state.profile)
        
        status_box.empty()
        st.session_state.result = result

        st.success("Blueprint Generated Successfully")

# ──────────────────────────────────────────
# GLOBAL CSS INJECTION
# ──────────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.bp-section {
    margin-bottom: 28px;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07), 0 4px 16px rgba(0,0,0,0.04);
    border: 1px solid #f1f5f9;
}
.bp-section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 20px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
}
.bp-section-body { padding: 20px 24px; }

/* Stat pill */
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 999px;
    padding: 5px 14px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #334155;
    margin: 3px;
}

/* Tag chip */
.tag-chip {
    display: inline-block;
    background: linear-gradient(135deg,#6366f1,#8b5cf6);
    color: #fff;
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    margin: 3px;
}

/* Flow row */
.flow-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.88rem;
    font-weight: 500;
    color: #1e293b;
    padding: 8px 0;
    border-bottom: 1px dashed #e2e8f0;
}
.flow-row:last-child { border-bottom: none; }
.flow-node {
    background: #f1f5f9;
    border-radius: 6px;
    padding: 4px 12px;
    font-weight: 600;
    white-space: nowrap;
}
.flow-mid {
    background: linear-gradient(135deg,#fbbf24,#f59e0b);
    color: #fff;
    border-radius: 6px;
    padding: 4px 12px;
    font-weight: 700;
    font-size: 0.78rem;
    white-space: nowrap;
}
.flow-arrow { color: #94a3b8; font-size: 1rem; }

/* Form badge */
.form-badge {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #f1f5f9;
}
.form-badge:last-child { border-bottom: none; }
.form-code {
    background: #1e293b;
    color: #38bdf8;
    border-radius: 6px;
    padding: 3px 9px;
    font-size: 0.78rem;
    font-weight: 700;
    white-space: nowrap;
    font-family: 'Courier New', monospace;
    flex-shrink: 0;
    margin-top: 1px;
}
.form-detail { font-size: 0.85rem; color: #475569; line-height: 1.5; }
.form-due { font-size: 0.75rem; color: #f59e0b; font-weight: 600; margin-top: 2px; }
</style>
"""

# ──────────────────────────────────────────
# SECTION RENDERERS
# ──────────────────────────────────────────

def render_state_analysis(data: dict) -> str:
    if not isinstance(data, dict): return ""
    score = data.get("business_friendliness_score", "?")
    complexity = data.get("compliance_complexity", "?")
    tax_env = html_mod.escape(str(data.get("tax_environment", "")))
    notes = html_mod.escape(str(data.get("incorporation_notes", "")))
    state = html_mod.escape(str(data.get("state", "")))
    score_color = "#22c55e" if int(score) >= 7 else ("#f59e0b" if int(score) >= 4 else "#ef4444") if str(score).isdigit() else "#94a3b8"
    complexity_color = {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"}.get(str(complexity), "#94a3b8")
    return f"""
    <div class="bp-section">
      <div class="bp-section-header" style="background:linear-gradient(135deg,#0f172a,#1e3a5f);color:#e2e8f0;">📍 State Analysis — {state}</div>
      <div class="bp-section-body">
        <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;">
          <div class="stat-pill">🏆 Friendliness Score: <span style="color:{score_color};font-size:1rem;">{score}/10</span></div>
          <div class="stat-pill">⚖️ Compliance: <span style="color:{complexity_color};">{complexity}</span></div>
        </div>
        <div style="font-size:0.88rem;color:#334155;line-height:1.7;margin-bottom:8px;">💰 <strong>Tax Environment:</strong> {tax_env}</div>
        <div style="font-size:0.88rem;color:#64748b;line-height:1.7;">📝 {notes}</div>
      </div>
    </div>"""


def render_entity(data: dict) -> str:
    if not isinstance(data, dict): return ""
    rec = html_mod.escape(str(data.get("recommended_structure",
          (data.get("recommended_structures") or ["LLC"])[0] if isinstance(data.get("recommended_structures"), list) else "LLC")))
    reason = html_mod.escape(str(data.get("reason", data.get("strategic_rationale", ""))))
    state_note = html_mod.escape(str(data.get("state_considerations", "")))

    # Pre-compute optional blocks
    extras_parts = []
    for k in ["tax_implications", "liability_protection", "scalability"]:
        val = data.get(k)
        if val:
            label = k.replace("_", " ").title()
            extras_parts.append(
                '<div style="font-size:0.85rem;color:#475569;padding:8px 0;border-bottom:1px solid #f1f5f9;">'
                '<span style="font-weight:600;color:#1e293b;">' + label + ':</span> ' + html_mod.escape(str(val)) + '</div>'
            )
    extras_html = "".join(extras_parts)

    state_html = (
        '<div style="margin-top:10px;font-size:0.82rem;color:#64748b;border-top:1px solid #f1f5f9;padding-top:10px;">'
        + '\U0001f4cd ' + state_note + '</div>'
    ) if state_note else ""

    return (
        '<div class="bp-section">'
        '<div class="bp-section-header" style="background:linear-gradient(135deg,#14532d,#166534);color:#dcfce7;">'
        '\U0001f3db\ufe0f Entity &amp; Structure</div>'
        '<div class="bp-section-body">'
        '<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:.08em;color:#86efac;margin-bottom:4px;">Recommended Structure</div>'
        '<div style="font-size:1.6rem;font-weight:800;color:#16a34a;margin-bottom:10px;">' + rec + '</div>'
        '<div style="font-size:0.9rem;color:#374151;line-height:1.7;margin-bottom:12px;">' + reason + '</div>'
        + extras_html + state_html +
        '</div></div>'
    )



def render_workforce(data: dict) -> str:
    if not isinstance(data, dict): return ""
    model = html_mod.escape(str(data.get("recommended_model", "")))
    core = html_mod.escape(str(data.get("core_team_strategy", "")))
    flex = html_mod.escape(str(data.get("flexible_talent_strategy", "")))
    rationale = html_mod.escape(str(data.get("strategic_rationale", "")))
    timeline = html_mod.escape(str(data.get("hiring_timeline", "")))
    raw = html_mod.escape(str(data.get("raw_output", "")))
    if not model and raw:
        return f'<div style="font-size:0.9rem;color:#374151;line-height:1.7;">{raw}</div>'
    rows = []
    if core:   rows.append(("👥 Core Team", core, "#3b82f6"))
    if flex:   rows.append(("🔄 Flexible Talent", flex, "#8b5cf6"))
    if rationale: rows.append(("💡 Rationale", rationale, "#0891b2"))
    if timeline:  rows.append(("🗓️ Hiring Timeline", timeline, "#f59e0b"))
    rows_html = "".join(f"""
      <div style="display:flex;gap:14px;padding:12px 0;border-bottom:1px solid #f1f5f9;align-items:flex-start;">
        <div style="width:4px;border-radius:4px;background:{c};flex-shrink:0;min-height:40px;"></div>
        <div><div style="font-size:0.78rem;font-weight:700;color:{c};text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px;">{lbl}</div>
        <div style="font-size:0.88rem;color:#374151;line-height:1.6;">{txt}</div></div>
      </div>""" for lbl, txt, c in rows)
    return f"""
    <div class="bp-section">
      <div class="bp-section-header" style="background:linear-gradient(135deg,#1e1b4b,#312e81);color:#e0e7ff;">💼 Workforce Strategy</div>
      <div class="bp-section-body">
        <div style="display:inline-block;background:linear-gradient(135deg,#4f46e5,#7c3aed);color:#fff;border-radius:8px;padding:6px 18px;font-size:0.88rem;font-weight:700;margin-bottom:16px;">{model}</div>
        {rows_html}
      </div>
    </div>"""


def render_tax(data: dict) -> str:
    if not isinstance(data, dict): return ""
    forms = data.get("tax_forms_and_schedules", [])
    considerations = data.get("tax_considerations", [])
    compliance = data.get("compliance_items", [])
    records = data.get("records_to_keep", [])
    raw = data.get("raw_output", "")

    def parse_form_line(line: str):
        """Returns (code, description, due_date) from a form line."""
        import re
        m = re.match(r'(Form [\w-]+|Schedule [\w-]+|[\w]+\s?[\w-]+(?:\s[\w]+)?)(.*?)(?:- Due (.+))?$', str(line))
        if m:
            code = m.group(1).strip()
            desc = (m.group(2) or "").strip().lstrip('(')
            desc = desc.rstrip(')').strip()
            due  = (m.group(3) or "").strip()
            return code, desc, due
        return str(line), "", ""

    forms_html = ""
    for f in forms:
        code, desc, due = parse_form_line(f)
        forms_html += f"""
        <div class="form-badge">
          <div><div class="form-code">{html_mod.escape(code)}</div></div>
          <div><div class="form-detail">{html_mod.escape(desc)}</div>
          {f'<div class="form-due">📅 Due: {html_mod.escape(due)}</div>' if due else ''}</div>
        </div>"""

    def bullet_list(items, color):
        if not items: return ""
        lis = "".join(f'<li style="padding:4px 0;font-size:0.85rem;color:#374151;">{html_mod.escape(str(i))}</li>' for i in items)
        return f'<ul style="margin:0;padding-left:18px;list-style:none;">' + "".join(f'<li style="padding:4px 0;font-size:0.85rem;color:#374151;"><span style="color:{color};margin-right:6px;">▸</span>{html_mod.escape(str(i))}</li>' for i in items) + "</ul>"

    return f"""
    <div class="bp-section">
      <div class="bp-section-header" style="background:linear-gradient(135deg,#7c1d1d,#991b1b);color:#fecaca;">📋 Tax &amp; Compliance</div>
      <div class="bp-section-body">
        {f'<div style="margin-bottom:18px;"><div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#f87171;margin-bottom:10px;">Required Forms &amp; Schedules</div>{forms_html}</div>' if forms_html else ''}
        {f'<div style="margin-bottom:14px;"><div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#fb923c;margin-bottom:8px;">Tax Considerations</div>{bullet_list(considerations, "#fb923c")}</div>' if considerations else ''}
        {f'<div style="margin-bottom:14px;"><div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#fbbf24;margin-bottom:8px;">Compliance Items</div>{bullet_list(compliance, "#fbbf24")}</div>' if compliance else ''}
        {f'<div><div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#a3e635;margin-bottom:8px;">Records to Keep</div>{bullet_list(records, "#a3e635")}</div>' if records else ''}
        {f'<div style="font-size:0.88rem;color:#374151;">{html_mod.escape(str(raw))}</div>' if raw and not forms else ''}
      </div>
    </div>"""


def render_accounting(data) -> str:
    import re as _re

    KNOWN_TOOLS = {
        "shopify": "🛒", "quickbooks": "📊", "quickbooks advanced": "📊",
        "netsuite": "🏢", "xero": "🧾", "stripe": "💳", "paypal": "🅿️",
        "excel": "📋", "bi dashboard": "📈", "wave": "🌊", "freshbooks": "🧾",
        "sage": "🏛️", "zoho books": "📒", "gusto": "👥", "bill.com": "💸",
        "a2x": "🔗", "taxjar": "🧮", "avalara": "🧮",
    }
    accent_colors = ["#0ea5e9", "#38bdf8", "#7dd3fc", "#0284c7", "#0369a1", "#075985"]

    def extract_tools_from_text(text: str):
        """Scan raw LLM text for known tool names and return ordered unique list."""
        found, seen = [], set()
        lower = text.lower()
        for name in KNOWN_TOOLS:
            if name in lower and name not in seen:
                found.append(name)
                seen.add(name)
        return found

    def build_rows(items):
        html = ""
        for i, key in enumerate(items):
            icon  = KNOWN_TOOLS.get(key, "⚙️")
            color = accent_colors[i % len(accent_colors)]
            label = key.title()
            html += (
                f'<div style="display:flex;gap:14px;padding:12px 0;'
                f'border-bottom:1px solid #f1f5f9;align-items:center;">'
                f'<div style="width:4px;border-radius:4px;background:{color};'
                f'flex-shrink:0;min-height:36px;"></div>'
                f'<div style="font-size:1.15rem;flex-shrink:0;">{icon}</div>'
                f'<div style="font-size:0.88rem;font-weight:600;color:#1e293b;">'
                f'{html_mod.escape(label)}</div></div>'
            )
        return html

    def wrap_section(inner_html: str) -> str:
        return (
            '<div class="bp-section">'
            '<div class="bp-section-header" style="background:linear-gradient(135deg,#0c4a6e,#075985);color:#bae6fd;">📊 Accounting Stack</div>'
            f'<div class="bp-section-body">{inner_html}</div>'
            '</div>'
        )

    # ── Normalise input ──────────────────────────────────────────────────────
    if isinstance(data, str):
        raw_text = data
        stack, rationale = [], ""
    elif isinstance(data, list):
        stack = [str(x) for x in data]; raw_text = ""; rationale = ""
    elif isinstance(data, dict):
        stack     = data.get("recommended_stack", data.get("accounting_stack", []))
        raw_text  = str(data.get("raw_output", ""))
        rationale = str(data.get("rationale", data.get("reason", "")))
    else:
        stack = []; raw_text = ""; rationale = ""

    # ── Structured path: we have an actual list of tools ────────────────────
    if stack:
        stack_label = (
            '<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:.08em;'
            'color:#7dd3fc;margin-bottom:4px;">Recommended Stack</div>'
        )
        rows_html = build_rows([str(x).lower().split('/')[0].strip() for x in stack])
        rat_html = ""
        if rationale:
            rat_html = (
                '<div style="display:flex;gap:14px;padding:12px 0;align-items:flex-start;">'
                '<div style="width:4px;border-radius:4px;background:#0ea5e9;flex-shrink:0;min-height:40px;"></div>'
                '<div>'
                '<div style="font-size:0.78rem;font-weight:700;color:#0ea5e9;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px;">💡 Rationale</div>'
                f'<div style="font-size:0.88rem;color:#374151;line-height:1.6;">{html_mod.escape(rationale)}</div>'
                '</div></div>'
            )
        return wrap_section(stack_label + rows_html + rat_html)

    # ── Fallback path: raw prose from LLM ───────────────────────────────────
    # Try to salvage tool names from the text as accent rows
    detected = extract_tools_from_text(raw_text)
    detected_html = ""
    if detected:
        detected_html = (
            '<div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:.08em;'
            'color:#7dd3fc;margin-bottom:4px;">Recommended Stack</div>'
            + build_rows(detected)
        )

    # Only show the raw prose if no tools were detected — prevents duplicate "Recommended Stack" heading
    prose_html = ""
    if raw_text and not detected:
        prose = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_mod.escape(raw_text))
        prose = prose.replace('&lt;strong&gt;', '<strong>').replace('&lt;/strong&gt;', '</strong>')
        prose_html = (
            '<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:.08em;color:#7dd3fc;margin-top:16px;margin-bottom:8px;">Details</div>'
            f'<div style="font-size:0.88rem;color:#374151;line-height:1.75;white-space:pre-wrap;">'
            f'{prose}</div>'
        )

    return wrap_section(detected_html + prose_html)


def render_integration(data: dict) -> str:
    if not isinstance(data, dict): return ""
    overview = html_mod.escape(str(data.get("system_overview", "")))
    raw = html_mod.escape(str(data.get("raw_output", "")))

    def flow_section(label, items, accent):
        if not items: return ""
        rows = ""
        for item in items:
            parts = [p.strip() for p in str(item).split("----->" )]
            nodes_html = ""
            for i, part in enumerate(parts):
                is_middleware = 0 < i < len(parts) - 1
                css_class = "flow-mid" if is_middleware else "flow-node"
                nodes_html += '<span class="' + css_class + '">' + html_mod.escape(part) + '</span>'
                if i < len(parts) - 1:
                    nodes_html += '<span class="flow-arrow">\u2192</span>'
            rows += '<div class="flow-row">' + nodes_html + '</div>'
        return (
            '<div style="margin-bottom:18px;">'
            '<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:' + accent + ';margin-bottom:8px;">'
            + html_mod.escape(label) + '</div>' + rows + '</div>'
        )

    sections_html = ""
    for key, accent in [("Sales Channels", "#38bdf8"), ("Payments", "#34d399"), ("HR & Payroll", "#a78bfa"), ("integration_mappings", "#38bdf8")]:
        items = data.get(key, [])
        if items:
            label = key.replace("_", " ").title()
            sections_html += flow_section(label, items, accent)

    overview_html = (
        '<div style="font-size:0.9rem;color:#374151;line-height:1.7;margin-bottom:18px;border-left:3px solid #2dd4bf;padding-left:14px;">'
        + overview + '</div>'
    ) if overview else ""

    raw_html = '<div style="font-size:0.85rem;color:#475569;">' + raw + '</div>' if (raw and not sections_html) else ""

    return (
        '<div class="bp-section">'
        '<div class="bp-section-header" style="background:linear-gradient(135deg,#134e4a,#115e59);color:#ccfbf1;">'
        '\U0001f517 Integration &amp; Data Flow</div>'
        '<div class="bp-section-body">' + overview_html + sections_html + raw_html + '</div>'
        '</div>'
    )



# ──────────────────────────────────────────
# OUTPUT (SAFE RENDER)
# ──────────────────────────────────────────
if st.session_state.result is not None:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 📊 Your Generated Business Blueprint")
    st.caption(st.session_state.result.get("summary", "Business Architecture"))

    r = st.session_state.result

    # ── Parse entity once ──
    entity_raw = r.get("entity_analysis", {})
    if isinstance(entity_raw, str):
        try: entity_raw = json.loads(entity_raw)
        except Exception: entity_raw = {}

    # ── ROW 1: State Analysis ──
    st.markdown(render_state_analysis(r.get("state_analysis", {})), unsafe_allow_html=True)

    # ── ROW 2: Entity & Structure ──
    st.markdown(render_entity(entity_raw), unsafe_allow_html=True)

    # ── ROW 3: Workforce Strategy ──
    st.markdown(render_workforce(r.get("workforce_analysis", {})), unsafe_allow_html=True)

    # ── ROW 4: Tax & Compliance ──
    st.markdown(render_tax(r.get("tax_analysis", {})), unsafe_allow_html=True)

    # ── ROW 5: Accounting Stack + COA ──
    st.markdown(render_accounting(r.get("accounting_analysis", {})), unsafe_allow_html=True)
    coa_data = r.get("chart_of_accounts")
    if coa_data and isinstance(coa_data, dict) and "accounts" in coa_data:
        accounts = coa_data.get("accounts", [])
        if accounts:
            csv_data = generate_qbo_csv(accounts)
            colA, colB = st.columns([3, 1])
            with colA:
                st.success(f"📒 QuickBooks Chart of Accounts — {len(accounts)} accounts generated for your structure.")
            with colB:
                st.download_button("⬇️ Download QBO CSV", data=csv_data, file_name="qbo_chart_of_accounts.csv", mime="text/csv")
            with st.expander("👀 Preview Chart of Accounts", expanded=False):
                st.dataframe(accounts, use_container_width=True)

    # ── ROW 6: Integration & Data Flow ──
    st.markdown(render_integration(r.get("integration", {})), unsafe_allow_html=True)

    # -------------------------
    # INCORPORATION WALKTHROUGH
    # -------------------------
    walkthrough = st.session_state.result.get("incorporation_walkthrough")
    if walkthrough and isinstance(walkthrough, dict) and "steps" in walkthrough:
        st.markdown("---")
        st.markdown("## 📋 Incorporation Walkthrough")
        st.caption("Complete these steps in order — both state and federal — to legally form your business.")

        steps = walkthrough.get("steps", [])
        total_time = walkthrough.get("total_estimated_time", "N/A")

        # Group by parallel_group field; fallback to unique key if missing
        grouped_steps = {}
        for i, step in enumerate(steps):
            group_key = step.get("parallel_group") or f"_solo_{i}"
            if group_key not in grouped_steps:
                grouped_steps[group_key] = []
            grouped_steps[group_key].append(step)

        def sort_key(item):
            group = item[1]
            try:
                return int(group[0].get("step", 999))
            except Exception:
                return 999


        for group_key, group in sorted(grouped_steps.items(), key=sort_key):
            st.markdown("<div style='margin-bottom:4px;'></div>", unsafe_allow_html=True)
            cols = st.columns(max(len(group), 1))
            for idx, step in enumerate(group):
                with cols[idx]:
                    level       = step.get("level", "")
                    badge       = "🏛️ State" if level == "State" else "🇺🇸 Federal"
                    color       = "rgba(34, 139, 230, 0.1)" if level == "State" else "rgba(245, 159, 0, 0.1)"
                    border      = "#228be6" if level == "State" else "#f59f00"
                    filing_url  = step.get("filing_url", "")
                    pdf_url     = step.get("pdf_url", "")

                    # Escape every LLM-sourced value so special characters can't break the HTML
                    disp_step   = html_mod.escape(str(step.get("step", "")))
                    action      = html_mod.escape(str(step.get("action", "")))
                    where       = html_mod.escape(str(step.get("where_to_file", "")))
                    response_t  = html_mod.escape(str(step.get("response_time", "N/A")))
                    docs_raw    = step.get("documents", [])
                    docs        = html_mod.escape(", ".join(docs_raw) if isinstance(docs_raw, list) else str(docs_raw))

                    filing_btn = (
                        f'<a href="{filing_url}" target="_blank" style="'
                        f'display:inline-block; margin-right:8px; padding:5px 12px; '
                        f'background:#228be6; color:#fff; border-radius:4px; text-decoration:none; font-size:0.82rem; font-weight:600;">'
                        f'🌐 File Online</a>'
                    ) if filing_url else ""

                    pdf_btn = (
                        f'<a href="{pdf_url}" target="_blank" style="'
                        f'display:inline-block; padding:5px 12px; '
                        f'background:#e67700; color:#fff; border-radius:4px; text-decoration:none; font-size:0.82rem; font-weight:600;">'
                        f'📄 Download PDF</a>'
                    ) if pdf_url and pdf_url.lower().endswith('.pdf') else ""

                    # Build the card as a clean string — no nested f-string expressions
                    card_html = (
                        f'<div style="background:{color}; border-left:5px solid {border}; '
                        f'border-radius:6px; padding:14px 18px; margin-bottom:12px; height:100%;">'
                        f'<div style="font-size:0.78rem; opacity:0.7; margin-bottom:4px;">'
                        f'Step {disp_step} &nbsp;·&nbsp; <strong>{badge}</strong></div>'
                        f'<div style="font-size:1.05rem; font-weight:700; margin-bottom:6px;">'
                        f'📌 {action}</div>'
                        f'<div style="margin-bottom:4px;"><strong>Documents:</strong> {docs}</div>'
                        f'<div style="margin-bottom:8px;"><strong>File at:</strong> {where}</div>'
                        f'<div style="margin-bottom:10px;">{filing_btn}{pdf_btn}</div>'
                        f'<div style="color:#22c55e; font-weight:600;">⏱ Response Time: {response_t}</div>'
                        f'</div>'
                    )
                    st.markdown(card_html, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div style="
                background:#ebfbee;
                border: 2px solid #2f9e44;
                border-radius: 8px;
                padding: 16px 20px;
                margin-top: 16px;
                text-align: center;
                font-size: 1.1rem;
                font-weight: 700;
                color: #2f9e44;
            ">
                ✅ Total Estimated Timeline: {total_time}
            </div>
            """,
            unsafe_allow_html=True
        )
    elif walkthrough and isinstance(walkthrough, dict) and "raw_output" in walkthrough:
        st.markdown("---")
        st.markdown("## 📋 Incorporation Walkthrough")
        st.markdown(walkthrough["raw_output"])

    # ─────────────────────────────────────────────────────────
    # BUSINESS LAUNCH PACKAGE  (PDF Download)
    # ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 📦 Business Launch Package")
    st.write(
        "Generate a professionally formatted PDF implementation roadmap — ready to share "
        "with your accountant, attorney, or co-founders."
    )

    if not REPORTLAB_AVAILABLE:
        st.warning("⚠️ `reportlab` is not installed. Run `pip install reportlab` then restart the app.")
    else:
        if st.button("📄 Generate Business Launch Package", type="primary"):
            doc_package = st.session_state.result.get("document_package", {})

            # Security guard: scan the stringified package
            guard_check = guard.validate_input(str(doc_package)[:2000])
            if not guard_check["safe"]:
                st.error(f"🚫 Security check failed: {guard_check['reason']}")
            elif not doc_package or "sections" not in doc_package:
                st.error(
                    "🚨 The AI document package was not generated correctly. "
                    "Please click **Generate Business Blueprint** again to retry."
                )
            else:
                with st.spinner("📄 Building your PDF..."):
                    try:
                        profile_data = st.session_state.get("profile", {})
                        pdf_bytes = generate_business_package(doc_package, profile_data)

                        st.success("✅ Your Business Launch Package is ready!")
                        st.download_button(
                            label="⬇️ Download Business Launch Package (PDF)",
                            data=pdf_bytes,
                            file_name="EcomFinanceOS_Business_Launch_Package.pdf",
                            mime="application/pdf",
                            type="primary",
                        )

                        # Preview section chips
                        sections = doc_package.get("sections", [])
                        if sections:
                            st.markdown("**Package includes:**")
                            cols = st.columns(min(len(sections), 4))
                            for i, sec in enumerate(sections):
                                with cols[i % 4]:
                                    st.markdown(
                                        f"<div style='border:1px solid #e2e8f0; border-radius:8px; "
                                        f"padding:10px 14px; font-size:0.88rem; font-weight:600; "
                                        f"text-align:center;'>📄 {sec.get('name','')}</div>",
                                        unsafe_allow_html=True
                                    )
                    except Exception as e:
                        st.error(f"🚨 PDF generation failed: {e}")
