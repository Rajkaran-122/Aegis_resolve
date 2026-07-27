"""Generate BRD.pdf for Aegis Resolve AI submission."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

OUTPUT = r"c:\Users\digital metro\Documents\Scanned Documents\aegis-resolve\submission\BRD.pdf"

styles = getSampleStyleSheet()
title_style = ParagraphStyle("Title", parent=styles["Title"], fontSize=22, spaceAfter=20, textColor=colors.HexColor("#06182c"))
heading_style = ParagraphStyle("Heading", parent=styles["Heading1"], fontSize=14, spaceBefore=16, spaceAfter=8, textColor=colors.HexColor("#0077b6"))
sub_style = ParagraphStyle("Sub", parent=styles["Heading2"], fontSize=12, spaceBefore=12, spaceAfter=6, textColor=colors.HexColor("#0077b6"))
body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=8)
meta_style = ParagraphStyle("Meta", parent=styles["Normal"], fontSize=9, textColor=colors.grey)

def build_pdf():
    doc = SimpleDocTemplate(OUTPUT, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch,
                             leftMargin=0.85*inch, rightMargin=0.85*inch)
    story = []

    story.append(Paragraph("Business Requirements Document", title_style))
    story.append(Paragraph("Aegis Resolve AI — Digital Arbitration Court", heading_style))
    story.append(Spacer(1, 12))

    meta_data = [
        ["Field", "Value"],
        ["Product", "Aegis Resolve AI"],
        ["Version", "MVP 0.1.0"],
        ["Document Owner", "Business & Product Team"],
        ["Date", "July 27, 2026"],
        ["Classification", "Internal — Demo Submission"],
        ["Status", "Approved"],
    ]
    t = Table(meta_data, colWidths=[1.8*inch, 4.2*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0077b6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#e8f4fc")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    sections = [
        ("1. Executive Summary",
         "Aegis Resolve AI addresses the critical business need for faster, fairer, and more transparent "
         "payment dispute resolution. The platform models card and payment disputes as a Digital Arbitration "
         "Court, providing evidence-led decisions with full auditability. This MVP demonstrates the business "
         "viability of AI-assisted dispute resolution to stakeholders including card issuers, merchants, "
         "and compliance teams."),

        ("2. Business Problem",
         "Payment disputes represent a significant operational cost and customer satisfaction risk for "
         "financial institutions. Current processes are characterized by: (a) resolution timelines of "
         "2–6 weeks, (b) opaque decision-making that erodes customer trust, (c) inconsistent analyst "
         "quality under high volume, (d) incomplete audit trails for regulatory compliance, and "
         "(e) adversarial merchant-cardholder dynamics without structured evidence evaluation."),

        ("3. Business Objectives",
         "Primary objectives for the Aegis Resolve platform include: reduce average dispute resolution "
         "time from weeks to minutes; increase decision transparency with policy citations and "
         "explainable rationale; maintain fairness parity above 90% across all case types; provide "
         "100% auditable replay trails for compliance review; and route ambiguous edge cases to human "
         "analysts with full context preserved."),

        ("4. Stakeholders",
         ""),
    ]

    for title, content in sections:
        story.append(Paragraph(title, heading_style))
        if content:
            story.append(Paragraph(content, body_style))

    stakeholder_data = [
        ["Stakeholder", "Role", "Interest"],
        ["Card Members", "Consumers", "Fast, fair resolution of disputed charges"],
        ["Merchants", "Businesses", "Evidence-based defense, reduced chargeback losses"],
        ["Dispute Analysts", "Operations", "Efficient queue management, override capability"],
        ["Compliance Officers", "Regulatory", "Complete audit trails, policy adherence"],
        ["Product Leadership", "Strategy", "Platform differentiation, cost reduction"],
        ["Engineering", "Delivery", "Scalable, maintainable architecture"],
    ]
    st = Table(stakeholder_data, colWidths=[1.5*inch, 1.3*inch, 3.2*inch])
    st.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0077b6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(st)
    story.append(Spacer(1, 16))

    story.append(Paragraph("5. Business Requirements", heading_style))
    req_data = [
        ["ID", "Requirement", "Priority"],
        ["BR-01", "Support card member dispute filing and status tracking", "Must Have"],
        ["BR-02", "Enable merchant evidence submission and case response", "Must Have"],
        ["BR-03", "Provide enterprise analyst review queue with override", "Must Have"],
        ["BR-04", "Generate policy-grounded verdicts with AMEX reason codes", "Must Have"],
        ["BR-05", "Score evidence trust and case fairness (0–100)", "Must Have"],
        ["BR-06", "Maintain complete courtroom replay audit trail", "Must Have"],
        ["BR-07", "Route ambiguous cases to human review automatically", "Must Have"],
        ["BR-08", "Deliver operational KPI dashboard for analysts", "Should Have"],
        ["BR-09", "Support real-time event streaming for live replay", "Should Have"],
        ["BR-10", "Integrate with payment network evidence sources", "Future"],
        ["BR-11", "Deploy LLM agent orchestration for reasoning", "Future"],
        ["BR-12", "Implement authentication and tenant isolation", "Future"],
    ]
    rt = Table(req_data, colWidths=[0.6*inch, 4.0*inch, 1.0*inch])
    rt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0077b6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(rt)
    story.append(PageBreak())

    story.append(Paragraph("6. Success Metrics & KPIs", heading_style))
    kpi_data = [
        ["Metric", "Current Baseline", "MVP Target", "Production Target"],
        ["Avg Resolution Time", "2–6 weeks", "≤ 8 minutes", "≤ 15 minutes"],
        ["Fairness Index", "Unmeasured", "≥ 90 avg", "≥ 95 avg"],
        ["Audit Completeness", "Partial", "100%", "100% immutable"],
        ["Human Review Rate", "100% manual", "40% (edge cases)", "≤ 15%"],
        ["Customer Satisfaction", "Low (opaque)", "Demo validated", "≥ 4.5/5"],
        ["Compliance Pass Rate", "Variable", "Full replay", "Automated checks"],
    ]
    kt = Table(kpi_data, colWidths=[1.5*inch, 1.3*inch, 1.3*inch, 1.5*inch])
    kt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0077b6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(kt)
    story.append(Spacer(1, 16))

    story.append(Paragraph("7. Business Constraints", heading_style))
    constraints = [
        "MVP must run locally without external API keys or cloud dependencies.",
        "Demo must include five pre-seeded scenarios covering all AMEX reason codes.",
        "No production authentication required for hackathon/demo submission.",
        "AMEX reason codes used as policy proxy — not affiliated with American Express.",
        "Agent pipeline is conceptual in MVP; real LLM integration deferred to production.",
        "Budget constraint: zero external service costs for demo phase.",
    ]
    for c in constraints:
        story.append(Paragraph(f"• {c}", body_style))

    story.append(Spacer(1, 12))
    story.append(Paragraph("8. Assumptions & Dependencies", heading_style))
    assumptions = [
        "Stakeholders have access to modern browsers for demo presentation.",
        "Python 3.12 and Node.js are available on demo machines.",
        "Compliance team will validate policy code mappings before production.",
        "LLM provider selection requires enterprise security review.",
        "Payment network integration requires partnership agreements.",
    ]
    for a in assumptions:
        story.append(Paragraph(f"• {a}", body_style))

    story.append(Spacer(1, 12))
    story.append(Paragraph("9. Risks & Mitigations", heading_style))
    risk_data = [
        ["Risk", "Impact", "Mitigation"],
        ["LLM hallucination in verdicts", "High", "Policy engine guardrails + human review routing"],
        ["Regulatory non-compliance", "High", "Immutable audit store + policy versioning"],
        ["Merchant adoption resistance", "Medium", "Transparent evidence graph + dual advocacy"],
        ["Demo reliability issues", "Medium", "Seeded data + frontend fallback + Docker"],
        ["Scalability bottlenecks", "Low (MVP)", "PostgreSQL + microservices roadmap defined"],
    ]
    rkt = Table(risk_data, colWidths=[1.8*inch, 0.8*inch, 3.0*inch])
    rkt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0077b6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(rkt)

    story.append(Spacer(1, 16))
    story.append(Paragraph("10. Approval", heading_style))
    approval_data = [
        ["Role", "Name", "Signature", "Date"],
        ["Product Owner", "Dictatordaddy", "Approved", "July 27, 2026"],
        ["Technical Lead", "Dictatordaddy", "Approved", "July 27, 2026"],
        ["Business Sponsor", "Pending", "", ""],
    ]
    at = Table(approval_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.1*inch])
    at.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0077b6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(at)

    story.append(Spacer(1, 30))
    story.append(Paragraph("— End of Business Requirements Document —", ParagraphStyle("Footer", parent=meta_style, alignment=TA_CENTER)))

    doc.build(story)
    print(f"Generated: {OUTPUT}")

if __name__ == "__main__":
    build_pdf()
