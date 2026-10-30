import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from thesis_prelim import add_paragraph, add_heading_1, add_heading_2, add_heading_3

def build_chapter_1(doc):
    add_heading_1(doc, "CHAPTER 1: INTRODUCTION")
    
    # 1.1 BACKGROUND
    add_heading_2(doc, "1.1 BACKGROUND AND MOTIVATION")
    
    p1 = (
        "Higher technical education constitutes the indispensable engine of national economic competitiveness, technological sovereignty, "
        "and socio-economic transformation in the twenty-first century. Over the past four decades, India’s engineering and technological "
        "education ecosystem has experienced an unprecedented quantitative expansion, evolving from a modest network of state-funded engineering "
        "colleges into the world’s largest and most geographically diversified technical education architecture. According to the All India Survey "
        "on Higher Education (AISHE) and statistical releases from statutory apex authorities, the nation currently accommodates upwards of 6,000 "
        "approved degree- and diploma-granting technical institutions, enrolling more than 3.5 million undergraduate and postgraduate scholars across "
        "a vast array of core, interdisciplinary, and emerging technological disciplines."
    )
    add_paragraph(doc, p1)
    
    p2 = (
        "This rapid democratization of technical education has dramatically expanded opportunities for professional advancement across diverse "
        "regional and socio-economic demographics. However, this exponential institutional proliferation has simultaneously introduced severe "
        "systemic challenges concerning quality assurance, pedagogical rigor, faculty competence, laboratory modernization, and graduate employability. "
        "Industry surveys and national employability reports have consistently revealed an alarming divergence between the competencies imparted by "
        "many engineering institutions and the multidisciplinary, problem-solving proficiencies demanded by contemporary digital industries. In "
        "response to these pressing national imperatives, the Ministry of Education (MoE), Government of India, along with statutory regulatory "
        "councils, instituted an exacting quality assurance and accreditation framework anchored by four major statutory and autonomous mechanisms:"
    )
    add_paragraph(doc, p2)
    
    mechanisms = [
        ("1. All India Council for Technical Education (AICTE): ",
         "Constituted as a statutory apex body by an Act of Parliament (AICTE Act No. 52 of 1987), AICTE is legally vested with the mandate for "
         "the coordinated planning, formulation, and maintenance of norms and standards across all technical and management institutions in India. "
         "AICTE enforces regulatory compliance through its annual Approval Process Handbook (APH). Under the APH, institutions must undergo mandatory "
         "annual scrutiny covering quantitative thresholds for Student-Faculty Ratios (SFR 1:15 for Tier-I programs, 1:20 for standard degree engineering), "
         "Faculty Cadre Ratios (Professor : Associate Professor : Assistant Professor = 1:2:6), instructional and administrative built-up space adequacy, "
         "laboratory equipment readiness, digital library holdings, barrier-free physical infrastructure for persons with disabilities, and statutory safety N.O.C. certifications."),
         
        ("2. National Board of Accreditation (NBA): ",
         "Established as an autonomous programmatic accreditation body, the NBA assesses technical programs (such as B.Tech in Information Technology) "
         "to ensure alignment with the highest international quality standards. In June 2014, India attained permanent signatory status to the Washington Accord, "
         "an elite multilateral agreement among leading international engineering accreditation authorities. This signatory status requires Indian "
         "institutions to adhere strictly to an Outcome-Based Education (OBE) paradigm. Under NBA's Tier-I (for autonomous institutions and university colleges) "
         "and Tier-II rubrics, programs are rigorously evaluated across a 1000-point framework spanning ten discrete criteria. Programs must demonstrate "
         "attainment of Program Educational Objectives (PEOs), Course Outcomes (COs), Program Outcomes (POs), Faculty Retention Rates (FRR >= 85%), "
         "and Student Success Indices (SI)."),
         
        ("3. National Assessment and Accreditation Council (NAAC): ",
         "An autonomous institution established by the University Grants Commission (UGC) in 1994, NAAC conducts comprehensive institutional-level "
         "accreditations to evaluate the governance, academic culture, research productivity, infrastructure, and societal impact of universities and colleges. "
         "Under its Revised Accreditation Framework (RAF), institutions submit detailed Annual Quality Assurance Reports (AQAR) and Self-Study Reports (SSR). "
         "The evaluation framework is heavily data-driven, with 70% of the overall score determined by quantitative metrics subjected to independent Data Validation "
         "and Verification (DVV), complemented by qualitative on-site peer-team inspections."),
         
        ("4. National Institutional Ranking Framework (NIRF): ",
         "Launched in 2015 by the Ministry of Education, NIRF provides a transparent, annual comparative benchmarking mechanism that ranks engineering "
         "and technological institutions across five cardinal pillars: Teaching, Learning & Resources (TLR), Research and Professional Practice (RPC), "
         "Graduation Outcomes (GO), Outreach and Inclusivity (OI), and Public Perception (PR). NIRF rankings carry substantial public prestige and directly "
         "govern student admissions, governmental research grant allocations, and corporate recruitment partnerships.")
    ]
    for mtitle, mdesc in mechanisms:
        p = add_paragraph(doc)
        p.add_run(mtitle).font.bold = True
        p.add_run(mdesc)
        
    p3 = (
        "While these regulatory frameworks have established clear benchmarks of educational excellence, complying with their mandates requires "
        "engineering colleges to collect, format, cross-verify, and maintain astronomical volumes of institutional documentation. A mid-sized engineering "
        "institution with an approved intake of 720 students generates between 3,500 and 5,000 pages of compliance dossiers annually. These dossiers "
        "include detailed faculty appointment ledgers, salary bank disbursement statements, provident fund records, course syllabi, continuous internal "
        "evaluation (CIE) records, laboratory equipment invoices, campus floor plans, and audited balance sheets. Historically, this compilation has "
        "relied on manual administrative workflows that are intensely labor-intensive, error-prone, and devoid of predictive analytics."
    )
    add_paragraph(doc, p3)
    
    # 1.2 PROBLEM STATEMENT
    add_heading_2(doc, "1.2 PROBLEM STATEMENT AND RESEARCH CHALLENGES")
    
    p4 = (
        "Despite extensive enterprise resource planning (ERP) investments in higher education, institutional accreditation workflows remain "
        "predominantly manual, reactive, and fragmented. The primary research and engineering bottlenecks can be categorized into five critical dimensions:"
    )
    add_paragraph(doc, p4)
    
    challenges = [
        ("1. Heterogeneity and Spatial Complexity of Regulatory Portfolios: ",
         "Accreditation dossiers are characterized by extreme structural and formatting entropy. Key compliance evidence is dispersed across scanned "
         "PDF approvals, native digital reports, complex multi-row financial spreadsheets, and raster image certificates. Standard optical character "
         "recognition (OCR) tools fail to capture merged table cells, nested sub-tables, and multi-column academic layouts, leading to corrupted data "
         "and fractured tabular relationships."),
         
        ("2. Cognitive Extraction Bottlenecks and Hallucination Risks in Generic LLMs: ",
         "Applying generic Large Language Models (LLMs) to statutory audits introduces severe operational vulnerabilities. Generic models lack "
         "domain knowledge of AICTE handbook clauses, NBA Tier-I rubrics, and NAAC metric boundaries. Crucially, without rigid structural constraints "
         "and deterministic schema enforcement, LLMs frequently hallucinate—fabricating faculty credentials, miscalculating carpet areas, or generating "
         "erroneous budgetary percentages. In regulatory scrutiny, a single hallucination can invalidate an entire institutional submission."),
         
        ("3. Massive Administrative Burden and Person-Hour Misallocation: ",
         "Under conventional manual paradigms, assembling and auditing an NBA Self-Assessment Report or AICTE Mandatory Disclosure demands between 45 and "
         "60 working days of continuous clerical effort by senior professors and steering committees. This severe misallocation of academic human capital "
         "diverts leading faculty from high-impact technical research, student mentoring, and pedagogical innovation toward clerical bookkeeping."),
         
        ("4. Total Absence of Longitudinal Multi-Year Tracking and Predictive Forecasting: ",
         "Current accreditation processes operate on an episodic, snapshot-in-time basis, typically occurring once every three to five years. Consequently, "
         "institutional leadership remains blind to creeping compliance deficits—such as gradual cadre degradation caused by recruiting junior faculty without "
         "promoting senior staff, or impending spatial shortages driven by intake expansions. Existing tools lack predictive time-series models (e.g., SARIMA) "
         "to identify compliance drift before formal regulatory penalties occur."),
         
        ("5. Deployment Instabilities and Port Collision Bottlenecks: ",
         "In modern developer workstations and campus servers hosting multiple concurrent applications on tunneling services (e.g., Ngrok), port conflicts "
         "and exhaustion of tunnel allocations represent major failure points. Existing academic prototypes fail to implement dedicated port-isolated "
         "microservices, single-tunnel reverse proxy architectures, or robust stateless token authentication capable of surviving intermittent networks.")
    ]
    for ctitle, cdesc in challenges:
        p = add_paragraph(doc)
        p.add_run(ctitle).font.bold = True
        p.add_run(cdesc)
        
    p5 = (
        "Formally stated, the core research challenge is: “How can a decoupled, multi-modal cognitive architecture be engineered to autonomously "
        "ingest unstructured, multi-format institutional regulatory dossiers, execute high-precision layout-aware entity extraction using Google Gemini "
        "2.5 Flash without hallucination, evaluate mathematical compliance across AICTE, NBA, NAAC, and NIRF standards deterministically, model "
        "multi-year longitudinal trajectories through predictive time-series forecasting, and generate publication-grade compliance dossiers on a "
        "dedicated, non-conflicting port architecture?”"
    )
    add_paragraph(doc, p5, italic=True)
    
    # 1.3 OBJECTIVES
    add_heading_2(doc, "1.3 OBJECTIVES OF THE PROJECT")
    
    p6 = (
        "To systematically address the research problem and build a production-grade, industrial-strength solution, the specific objectives "
        "of this project are formulated as follows:"
    )
    add_paragraph(doc, p6)
    
    objs = [
        ("Objective 1: Multi-Format Ingestion and Layout-Aware Deep Document Parsing: ",
         "Develop a high-throughput document parsing pipeline utilizing Docling deep visual layout analysis and PyMuPDF that extracts text, "
         "hierarchical sections, and complex tabular structures from multi-page scanned and native PDF dossiers, achieving a table cell recovery "
         "rate exceeding 95%."),
         
        ("Objective 2: Cognitive Information Extraction with Zero Hallucination: ",
         "Design and deploy a cognitive extraction pipeline powered by Google Gemini 2.5 Flash orchestrated with domain-specific few-shot prompting "
         "and rigid Pydantic structured output schemas, achieving normalized entity resolution (faculty rosters, spatial infrastructure, financial budgets, "
         "student placement statistics) with an F1-score exceeding 0.98."),
         
        ("Objective 3: Deterministic Regulatory Compliance Engines: ",
         "Program and validate four dedicated algorithmic compliance engines that deterministically execute statutory mathematical formulas:\n"
         "  a) AICTE Approval Process Handbook Engine: Computes Cadre Ratio (1:2:6), Student-Faculty Ratio (1:20), instructional/administrative spatial norms, and equipment checklists.\n"
         "  b) NBA Outcome-Based Education SAR Engine: Implements the complete 1000-point rubric across Criteria 1 through 10, computing SFR (1:15), Faculty Retention Rate (FRR), Academic Performance Index (API), and PO attainment levels.\n"
         "  c) NAAC Quality Synthesizer: Evaluates the seven key quantitative criteria under the Revised Accreditation Framework.\n"
         "  d) NIRF Benchmark Engine: Computes TLR, RPC, GO, OI, and PR index scores."),
         
        ("Objective 4: Longitudinal Multi-Year Analytics and Predictive Time-Series Forecasting: ",
         "Engineer an analytical engine utilizing multivariate polynomial regression and Seasonal Autoregressive Integrated Moving Average (SARIMA) "
         "algorithms to assimilate multi-year institutional data, detect year-over-year statistical anomalies (±10% threshold), and forecast future "
         "compliance drift with 95% confidence intervals."),
         
        ("Objective 5: Port-Isolated Full-Stack Deployment and Single-Tunnel Reverse Proxy: ",
         "Architect and deploy a modern, reactive full-stack application featuring Next.js 14 App Router on dedicated port 3051 and FastAPI on dedicated "
         "port 8051, unified behind a single Ngrok tunnel (inspector port 4051) through Next.js reverse-proxy rewrites, eliminating TCP port conflicts "
         "and preserving tunnel allocations in multi-project development environments."),
         
        ("Objective 6: Automated Dossier Compilation and Cryptographic Reporting: ",
         "Engineer an automated document generation subsystem capable of producing publication-ready, fully formatted PDF, Word (.docx), and Excel (.xlsx) "
         "Self-Assessment Reports, AICTE deficiency checklists, and executive governing body briefs, embedded with SHA-256 cryptographic audit hashes for tamper-proof data provenance.")
    ]
    for otitle, odesc in objs:
        p = add_paragraph(doc)
        p.add_run(otitle).font.bold = True
        p.add_run(odesc)
        
    # 1.4 SIGNIFICANCE
    add_heading_2(doc, "1.4 SIGNIFICANCE OF THE STUDY")
    
    p7 = (
        "The development and deployment of Smart Approval AI delivers transformative value across multiple tiers of the higher technical education ecosystem:"
    )
    add_paragraph(doc, p7)
    
    sigs = [
        ("• For Institutional Leadership and College Principals: ",
         "Transitions institutional accreditation from an episodic, panic-inducing administrative burden into a continuous, real-time quality assurance "
         "dashboard. Principals, Directors, and Internal Quality Assurance Cells (IQAC) gain continuous visibility into institutional health, enabling proactive "
         "faculty recruitment, targeted laboratory investments, and strategic budget allocations years ahead of formal regulatory visits."),
         
        ("• For Academic Faculty and Departmental Steering Committees: ",
         "Saves thousands of faculty person-hours previously consumed by tedious data entry, arithmetic calculations, and table formatting. Faculty can "
         "re-channel their intellectual efforts toward core pedagogical excellence, sponsored research, technological innovation, and personalized student mentoring."),
         
        ("• For Statutory Regulatory Councils (AICTE, NBA, NAAC, NIRF): ",
         "Provides visiting peer teams with standardized, verified, pre-audited digital dossiers where all mathematical formulas, cadre ratios, and spatial "
         "disclosures are pre-validated against primary evidence documents. This eliminates human calculation errors, reduces inter-evaluator subjectivity, "
         "and establishes a consistent national quality benchmark."),
         
        ("• For Students, Parents, and Corporate Recruiters: ",
         "Enhances public transparency and confidence in institutional quality ratings. Transparent accreditation verification ensures students receive "
         "education meeting international Washington Accord standards, directly enhancing global degree mobility and corporate recruitment confidence.")
    ]
    for stitle, sdesc in sigs:
        p = add_paragraph(doc)
        p.add_run(stitle).font.bold = True
        p.add_run(sdesc)
        
    # 1.5 SCOPE AND DELIMITATIONS
    add_heading_2(doc, "1.5 SCOPE AND DELIMITATIONS")
    
    p8 = (
        "To ensure precise engineering execution and robust empirical evaluation, the operational scope and boundary delimitations of this dissertation "
        "are explicitly defined:\n\n"
        "1. In-Scope Regulatory Codices: AICTE Approval Process Handbook (APH 2024-2027), NBA Tier-I/II Undergraduate Engineering Manuals (Washington "
        "Accord model), NAAC Revised Accreditation Framework for Autonomous/Affiliated Colleges, and NIRF Engineering Discipline metrics.\n\n"
        "2. In-Scope Ingestion Formats: Multi-page digital PDF documents, scanned PDF reports (minimum 150 DPI), Microsoft Excel spreadsheets (.xlsx), "
        "and CSV ledgers containing institutional administrative, academic, physical, and financial disclosures.\n\n"
        "3. Computational Platform: FastAPI Python backend running on dedicated port 8051, Next.js 14 App Router frontend running on dedicated port 3051, "
        "Ngrok tunneling on port 4051, and Google Gemini 2.5 Flash cloud API for multimodal extraction.\n\n"
        "4. Delimitations: The system serves as an autonomous pre-scrutiny auditor and internal compliance tool; it does not replace the statutory authority "
        "of AICTE or NBA to grant official legal accreditation. Verification of physical civil building structures is performed based on uploaded licensed "
        "architectural plans and official government N.O.C. certificates, without direct on-site physical material testing."
    )
    add_paragraph(doc, p8)
    
    # 1.6 OUTLINE
    add_heading_2(doc, "1.6 ORGANIZATION OF THE THESIS")
    
    p9 = (
        "The remainder of this dissertation is organized into six comprehensive chapters:\n"
        "• Chapter 2: Literature Review & Theoretical Foundations explores the historical evolution of accreditation, advances in Document AI and OCR, "
        "large language model applications and hallucination mitigation, time-series forecasting in academic analytics, and a comparative survey of existing systems.\n"
        "• Chapter 3: Methodology & Proposed System Architecture details the multi-tier system architecture, the Docling deep-layout parsing pipeline, "
        "Gemini 2.5 Flash cognitive extraction, mathematical formulations of the AICTE, NBA, NAAC, and NIRF rule engines, SARIMA forecasting, and port-isolated deployment.\n"
        "• Chapter 4: Hardware and Software Requirements & System Specifications provides hardware specs, software stack dependencies, relational database "
        "schemas, entity-relationship models, and RESTful API endpoint contracts.\n"
        "• Chapter 5: Results, System Implementation & Discussions presents an operational software walkthrough with captured UI screenshots, comprehensive "
        "benchmarking across 50 real-world dossiers, precision/recall metrics, latency benchmarks, and a comparative evaluation against manual peer-team audits.\n"
        "• Chapter 6: Conclusion and Future Scope summarizes contributions, practical implications, system limitations, and an ambitious future roadmap."
    )
    add_paragraph(doc, p9)
    
    doc.add_page_break()
    print("Built Enriched Chapter 1 successfully.")

if __name__ == "__main__":
    test_doc = docx.Document()
    build_chapter_1(test_doc)
    test_doc.save("thesis/test_ch1_enriched.docx")
    print("Saved test_ch1_enriched.docx")
