"""
documents/generator.py
Generates the Business Launch Package PDF using ReportLab.
"""

import io
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        HRFlowable, PageBreak
    )
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ─────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────
BRAND_NAVY   = colors.HexColor("#0F172A")
BRAND_BLUE   = colors.HexColor("#2563EB")
BRAND_GREEN  = colors.HexColor("#16A34A")
BRAND_AMBER  = colors.HexColor("#D97706")
LIGHT_GRAY   = colors.HexColor("#F1F5F9")
MID_GRAY     = colors.HexColor("#94A3B8")
BORDER_GRAY  = colors.HexColor("#E2E8F0")
WHITE        = colors.white


def _build_styles():
    base = getSampleStyleSheet()

    styles = {
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="Helvetica-Bold",
            fontSize=32,
            textColor=WHITE,
            alignment=TA_CENTER,
            spaceAfter=6,
            leading=38,
        ),
        "cover_subtitle": ParagraphStyle(
            "cover_subtitle",
            fontName="Helvetica",
            fontSize=14,
            textColor=colors.HexColor("#CBD5E1"),
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "cover_meta": ParagraphStyle(
            "cover_meta",
            fontName="Helvetica",
            fontSize=11,
            textColor=colors.HexColor("#94A3B8"),
            alignment=TA_CENTER,
        ),
        "section_heading": ParagraphStyle(
            "section_heading",
            fontName="Helvetica-Bold",
            fontSize=16,
            textColor=BRAND_NAVY,
            spaceBefore=18,
            spaceAfter=6,
            leading=20,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#1E293B"),
            spaceAfter=4,
            leading=15,
            alignment=TA_JUSTIFY,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#1E293B"),
            leftIndent=16,
            spaceAfter=3,
            leading=14,
        ),
        "label": ParagraphStyle(
            "label",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=BRAND_BLUE,
            spaceAfter=2,
        ),
        "week_header": ParagraphStyle(
            "week_header",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=BRAND_NAVY,
            spaceAfter=3,
            spaceBefore=8,
        ),
        "disclaimer": ParagraphStyle(
            "disclaimer",
            fontName="Helvetica-Oblique",
            fontSize=8,
            textColor=MID_GRAY,
            alignment=TA_CENTER,
            spaceBefore=6,
        ),
        "toc_item": ParagraphStyle(
            "toc_item",
            fontName="Helvetica",
            fontSize=11,
            textColor=colors.HexColor("#334155"),
            spaceAfter=5,
            leftIndent=12,
        ),
        "subheading": ParagraphStyle(
            "subheading",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=BRAND_BLUE,
            spaceBefore=10,
            spaceAfter=4,
        ),
    }
    return styles


# ─────────────────────────────────────────────
# COVER PAGE
# ─────────────────────────────────────────────
def _cover_page(elements, profile, styles):
    """Dark navy cover page with branding."""

    # Full-width dark banner table
    banner_content = [
        [Paragraph("🚀 EcomFinance OS", styles["cover_title"])],
        [Paragraph("30-Day Business Launch Package", styles["cover_subtitle"])],
        [Paragraph("— Powered by Multi-Agent AI Architecture —", styles["cover_meta"])],
    ]
    banner = Table(banner_content, colWidths=[18 * cm])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND_NAVY),
        ("TOPPADDING", (0, 0), (-1, 0), 40),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 40),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [BRAND_NAVY]),
    ]))
    elements.append(banner)
    elements.append(Spacer(1, 0.5 * cm))

    # Business summary card
    industry  = profile.get("industry", "N/A")
    state     = profile.get("state", "N/A")
    revenue   = profile.get("revenue", 0)
    owners    = profile.get("owners", 1)
    gen_date  = datetime.now().strftime("%B %d, %Y")

    card_data = [
        [Paragraph("<b>Business Profile</b>", ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=12, textColor=BRAND_BLUE))],
        [Paragraph(f"Industry: <b>{industry}</b>", styles["body"])],
        [Paragraph(f"State of Formation: <b>{state}</b>", styles["body"])],
        [Paragraph(f"Expected Annual Revenue: <b>${revenue:,}</b>", styles["body"])],
        [Paragraph(f"Number of Owners: <b>{owners}</b>", styles["body"])],
        [Paragraph(f"Report Generated: <b>{gen_date}</b>", styles["body"])],
    ]
    card = Table(card_data, colWidths=[18 * cm])
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("BOX", (0, 0), (-1, -1), 1, BORDER_GRAY),
        ("ROUNDEDCORNERS", [6]),
    ]))
    elements.append(card)
    elements.append(Spacer(1, 0.4 * cm))

    # Disclaimer banner
    disc = Table(
        [[Paragraph(
            "⚠️  This document is AI-generated and informational only. It does not constitute legal, "
            "financial, or tax advice. Always consult a qualified professional before making decisions.",
            ParagraphStyle("d", fontName="Helvetica-Oblique", fontSize=8,
                           textColor=colors.HexColor("#92400E"), alignment=TA_CENTER)
        )]],
        colWidths=[18 * cm]
    )
    disc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FEF3C7")),
        ("BOX", (0, 0), (-1, -1), 1, BRAND_AMBER),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    elements.append(disc)
    elements.append(PageBreak())


# ─────────────────────────────────────────────
# SECTION HEADER HELPER
# ─────────────────────────────────────────────
def _section_header(elements, number, title, styles):
    """Numbered pill-style section header."""
    pill_data = [[
        Paragraph(f"<b>{number}</b>",
                  ParagraphStyle("num", fontName="Helvetica-Bold", fontSize=12,
                                 textColor=WHITE, alignment=TA_CENTER)),
        Paragraph(f"<b>{title}</b>",
                  ParagraphStyle("ttl", fontName="Helvetica-Bold", fontSize=13,
                                 textColor=WHITE, alignment=TA_LEFT)),
    ]]
    pill = Table(pill_data, colWidths=[1 * cm, 17 * cm])
    pill.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), BRAND_BLUE),
        ("BACKGROUND", (1, 0), (1, 0), BRAND_NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (0, 0), 4),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(Spacer(1, 0.3 * cm))
    elements.append(pill)
    elements.append(Spacer(1, 0.25 * cm))


# ─────────────────────────────────────────────
# BODY CONTENT RENDERER
# ─────────────────────────────────────────────
def _render_content(elements, content, styles, section_name=""):
    """Smart renderer: detects bullets, week headers, checklist tables."""
    import re
    if not content:
        return

    # Convert basic markdown bold to ReportLab bold tags
    content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
    
    lines = [l.strip() for l in content.split("\n") if l.strip()]

    # --- Compliance Checklist → Table ---
    if section_name == "Compliance Checklist":
        table_data = [[
            Paragraph("<b>Action Item</b>", styles["label"]),
            Paragraph("<b>Authority</b>", styles["label"]),
            Paragraph("<b>Timeline</b>", styles["label"]),
        ]]
        for line in lines:
            if line.startswith("- "):
                parts = line[2:].split("|")
                row = [Paragraph(p.strip(), styles["bullet"]) for p in parts]
                while len(row) < 3:
                    row.append(Paragraph("", styles["bullet"]))
                table_data.append(row[:3])
        tbl = Table(table_data, colWidths=[8 * cm, 5 * cm, 5 * cm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BRAND_NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
            ("BOX", (0, 0), (-1, -1), 0.5, BORDER_GRAY),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, BORDER_GRAY),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(tbl)
        return

    # --- 30-Day Roadmap → Week blocks ---
    if section_name == "30-Day Implementation Roadmap":
        current_week = None
        current_items = []
        week_colors = [
            colors.HexColor("#EFF6FF"),
            colors.HexColor("#F0FDF4"),
            colors.HexColor("#FFFBEB"),
            colors.HexColor("#FDF2F8"),
        ]
        week_borders = [BRAND_BLUE, BRAND_GREEN, BRAND_AMBER, colors.HexColor("#9333EA")]
        week_idx = 0

        def _flush_week(wk_title, items, idx):
            if not wk_title:
                return
            bg = week_colors[idx % 4]
            bd = week_borders[idx % 4]
            rows = [[Paragraph(f"<b>{wk_title}</b>",
                               ParagraphStyle("wh", fontName="Helvetica-Bold", fontSize=11,
                                              textColor=bd))]]
            for item in items:
                rows.append([Paragraph(f"• {item}", styles["bullet"])])
            wt = Table(rows, colWidths=[18 * cm])
            wt.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 1.5, bd),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]))
            elements.append(wt)
            elements.append(Spacer(1, 0.2 * cm))

        for line in lines:
            if line.lower().startswith("week"):
                _flush_week(current_week, current_items, week_idx)
                current_week = line.rstrip(":")
                current_items = []
                week_idx += 1
            elif line.startswith("- ") or line.startswith("•"):
                current_items.append(line.lstrip("- •").strip())
            else:
                # inline items after colon
                current_items.extend([i.strip() for i in line.split(".") if i.strip()])
        _flush_week(current_week, current_items, week_idx)
        return

    # --- Generic content ---
    for line in lines:
        if line.startswith("### "):
            elements.append(Paragraph(line[4:].strip(), styles["subheading"]))
        elif line.startswith("## "):
            elements.append(Paragraph(line[3:].strip(), styles["subheading"]))
        elif line.startswith("# "):
            elements.append(Paragraph(line[2:].strip(), styles["subheading"]))
        elif line.startswith("- ") or line.startswith("•") or line.startswith("* "):
            elements.append(Paragraph(f"• {line.lstrip('- •*').strip()}", styles["bullet"]))
        else:
            elements.append(Paragraph(line, styles["body"]))
    elements.append(Spacer(1, 0.1 * cm))


# ─────────────────────────────────────────────
# MAIN GENERATOR
# ─────────────────────────────────────────────
def generate_business_package(document_data: dict, profile: dict) -> bytes:
    """
    Accepts the structured document dict from DocumentGeneratorAgent
    and the raw business profile. Returns PDF as bytes.
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError(
            "reportlab is not installed. Run: pip install reportlab"
        )

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="BizPilot AI Business Launch Package",
        author="BizPilot AI",
    )

    styles = _build_styles()
    elements = []

    # ── Cover ──
    _cover_page(elements, profile, styles)

    # ── Sections ──
    sections = document_data.get("sections", [])
    for i, section in enumerate(sections, start=1):
        name    = section.get("name", f"Section {i}")
        content = section.get("content", "")

        _section_header(elements, i, name, styles)
        _render_content(elements, content, styles, section_name=name)
        elements.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_GRAY,
                                   spaceAfter=6))

    # ── Footer disclaimer ──
    elements.append(Spacer(1, 1 * cm))
    elements.append(Paragraph(
        "© BizPilot AI · AI-generated document · Not legal, financial, or tax advice · "
        f"Generated {datetime.now().strftime('%B %d, %Y')}",
        styles["disclaimer"]
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()
