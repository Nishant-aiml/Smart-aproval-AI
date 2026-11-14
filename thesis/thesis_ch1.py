"""
Chapter 1: Introduction for Smart Approval AI
Streamlined to 5 precise academic pages (Pages 1 to 5)
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from thesis_prelim import add_paragraph, add_heading_1, add_heading_2, add_heading_3

def build_chapter_1(doc):
    add_heading_1(doc, "CHAPTER 1: INTRODUCTION")
    
    # 1.1 BACKGROUND
    add_heading_2(doc, "1.1 BACKGROUND AND MOTIVATION")
    
    p1 = (
        "Higher technical education constitutes the primary engine of national competitiveness, technological innovation, "
        "and socio-economic development in the twenty-first century. Over the past four decades, India's engineering education "
        "ecosystem has experienced immense expansion, encompassing upwards of 6,000 approved technical institutions enrolling "
        "over 3.5 million undergraduate and postgraduate scholars. While this growth has democratized technical education, "
        "it has simultaneously introduced critical systemic challenges in maintaining pedagogical rigor, faculty competence, "
        "laboratory modernization, and statutory governance compliance across diverse institutions."
    )
    add_paragraph(doc, p1)
    
    p2 = (
        "In response to these imperatives, statutory authorities enforce multi-tiered regulatory and accreditation frameworks: "
        "(1) The All India Council for Technical Education (AICTE), which mandates annual compliance with its Approval Process "
        "Handbook (APH), enforcing quantitative Student-Faculty Ratios (SFR 1:15 to 1:20), 1:2:6 Faculty Cadre Ratios (Professor : "
        "Associate Professor : Assistant Professor), built-up space norms, and laboratory readiness; (2) The National Board of "
        "Accreditation (NBA), which conducts Washington Accord-aligned Tier-I and Tier-II programmatic evaluations across a rigorous "
        "1000-point Outcome-Based Education (OBE) rubric; (3) The National Assessment and Accreditation Council (NAAC), assessing "
        "institutional governance and research via its Revised Accreditation Framework (RAF); and (4) The National Institutional "
        "Ranking Framework (NIRF), benchmarked annually across teaching, research, graduation outcomes, and perception."
    )
    add_paragraph(doc, p2)
    
    p3 = (
        "Complying with these apex mandates requires technical colleges to assemble, verify, and maintain thousands of heterogeneous "
        "documents annually - ranging from faculty appointment orders and salary bank scrolls to land deeds, laboratory invoices, "
        "and continuous internal evaluation sheets. Under conventional administrative workflows, this audit process is predominantly "
        "manual, highly labor-intensive, error-prone, and entirely devoid of forward-looking predictive analytics."
    )
    add_paragraph(doc, p3)
    
    # 1.2 PROBLEM STATEMENT
    add_heading_2(doc, "1.2 PROBLEM STATEMENT AND RESEARCH CHALLENGES")
    
    p4 = (
        "Despite enterprise software adoption in academic administration, regulatory accreditation workflows face five fundamental bottlenecks:"
    )
    add_paragraph(doc, p4)
    
    challenges = [
        ("1. Heterogeneity of Regulatory Portfolios: ",
         "Dossiers comprise scanned multi-page PDF approvals, complex spreadsheets, and raster certificates. Standard OCR engines "
         "consistently fail to preserve nested sub-tables and multi-column layouts, corrupting institutional compliance data."),
         
        ("2. Hallucination Risks in Generic LLMs: ",
         "Direct application of generic Large Language Models introduces severe operational risks. Without strict schema constraints "
         "and deterministic math execution, LLMs fabricate credentials, hallucinate carpet areas, and compute inaccurate ratios."),
         
        ("3. Severe Administrative Burden: ",
         "Compiling and vetting an NBA Self-Assessment Report or AICTE compliance portfolio requires 45 to 60 working days of continuous "
         "faculty effort, diverting high-value academic capital away from technical research and student mentorship."),
         
        ("4. Lack of Predictive Analytics: ",
         "Audits operate as retrospective snapshots occurring once every 3 to 5 years, leaving leadership blind to creeping compliance "
         "deficits such as cadre degradation or impending spatial shortages before punitive sanctions occur."),
         
        ("5. Port Collision & Deployment Instabilities: ",
         "Workstations running multiple concurrent projects on tunneling services face port collisions and tunnel exhaustion without "
         "dedicated port-isolated microservices and single-tunnel reverse proxy architectures.")
    ]
    for ctitle, cdesc in challenges:
        p = add_paragraph(doc)
        p.add_run(ctitle).font.bold = True
        p.add_run(cdesc)
        
    p5 = (
        "Formally stated, the core research challenge is: \"How can an autonomous, decoupled multi-modal cognitive architecture be engineered "
        "to ingest multi-format institutional dossiers, execute high-precision layout extraction without hallucination, evaluate mathematical "
        "compliance across AICTE, NBA, NAAC, and NIRF standards deterministically, forecast longitudinal compliance trajectories via SARIMA, "
        "and generate publication-grade compliance portfolios on a dedicated, non-conflicting port architecture?\""
    )
    add_paragraph(doc, p5, italic=True)
    
    # 1.3 OBJECTIVES
    add_heading_2(doc, "1.3 OBJECTIVES OF THE PROJECT")
    
    p6 = (
        "To systematically resolve this research problem, the primary objectives of this dissertation are:"
    )
    add_paragraph(doc, p6)
    
    objs = [
        ("1. Multi-Format Layout Ingestion: ",
         "Engineer a robust document ingestion pipeline coupling IBM Docling visual layout parsing with PyMuPDF, achieving a table cell "
         "recovery accuracy exceeding 98% across scanned and native PDF dossiers."),
         
        ("2. Grounded Entity Extraction: ",
         "Deploy a cognitive extraction engine powered by Google Gemini 2.5 Flash orchestrated with domain-specific prompting and Pydantic "
         "schemas to extract normalized institutional entities (faculty rosters, spatial areas, budgets) with zero mathematical hallucination."),
         
        ("3. Deterministic Regulatory Compliance Engines: ",
         "Implement deterministic algorithmic engines that evaluate AICTE APH clauses (cadre ratio 1:2:6, spatial carpet area, SFR), "
         "score NBA Tier-I SAR portfolios across all ten criteria (1000 points), and quantify NAAC RAF metrics."),
         
        ("4. Longitudinal Multi-Year Forecasting: ",
         "Integrate Seasonal AutoRegressive Integrated Moving Average (SARIMA) time-series forecasting to predict institutional compliance "
         "trajectories and detect anomalies 12 to 24 months before formal peer-team on-site inspections."),
         
        ("5. Dedicated Port-Isolated Microservice Architecture: ",
         "Architect an enterprise microservice stack featuring Next.js 14 on Port 3051, FastAPI on Port 8051, and Ngrok Inspector on Port 4051 "
         "unified via a reverse proxy to guarantee zero port collisions across multi-project environments.")
    ]
    for otitle, odesc in objs:
        p = add_paragraph(doc)
        p.add_run(otitle).font.bold = True
        p.add_run(odesc)
        
    # 1.4 SIGNIFICANCE
    add_heading_2(doc, "1.4 SIGNIFICANCE OF THE STUDY")
    
    p7 = (
        "The significance of Smart Approval AI extends across multiple administrative and educational tiers: (1) For Institutional Leadership, "
        "it transforms retrospective compliance panic into strategic quality governance via real-time risk dashboards; (2) For Faculty Steering "
        "Committees, it reduces audit preparation from 45 days to under 8.4 seconds per dossier, reclaiming hundreds of academic person-hours; "
        "(3) For Regulatory Bodies (AICTE/NBA), it provides standardized, tamper-evident digital verification portfolios backed by SHA-256 "
        "cryptographic hashes; and (4) For the Engineering Community, it establishes an open, verifiable reference architecture for grounded "
        "document AI in statutory governance."
    )
    add_paragraph(doc, p7)
    
    # 1.5 SCOPE
    add_heading_2(doc, "1.5 SCOPE AND DELIMITATIONS")
    
    p8 = (
        "The functional scope encompasses undergraduate engineering institutions governed by AICTE Approval Process Handbooks, NBA Tier-I "
        "accreditation manuals (Washington Accord), and NAAC autonomous college guidelines. The system processes heterogeneous digital files "
        "including text PDFs, scanned documents (>= 150 DPI), and tabular spreadsheets. Physical biometric verifications and non-academic "
        "statutory litigations are outside the immediate computational boundary."
    )
    add_paragraph(doc, p8)
    
    # 1.6 OUTLINE
    add_heading_2(doc, "1.6 ORGANIZATION OF THE THESIS")
    
    p9 = (
        "The remainder of this dissertation is organized as follows: Chapter 2 reviews statutory accreditation frameworks, document AI, "
        "and time-series forecasting. Chapter 3 details the system architecture, Docling parsing, Gemini cognitive extraction, and deterministic "
        "audit engines. Chapter 4 specifies hardware, software, relational database schemas, and RESTful APIs. Chapter 5 presents empirical "
        "benchmarks, captured UI artifacts, and comparative evaluations. Chapter 6 concludes with research contributions and future directions."
    )
    add_paragraph(doc, p9)
    doc.add_page_break()
    print("Built Streamlined Chapter 1 successfully.")

if __name__ == "__main__":
    test_doc = docx.Document()
    build_chapter_1(test_doc)
    test_doc.save("thesis/test_ch1_streamlined.docx")
    print("Saved test_ch1_streamlined.docx")
