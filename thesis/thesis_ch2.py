import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from thesis_prelim import add_paragraph, add_heading_1, add_heading_2, add_heading_3

def build_chapter_2(doc):
    add_heading_1(doc, "CHAPTER 2: LITERATURE REVIEW")
    
    # 2.1 EVOLUTION OF ACCREDITATION FRAMEWORKS
    add_heading_2(doc, "2.1 EVOLUTION OF REGULATORY ACCREDITATION FRAMEWORKS IN HIGHER TECHNICAL EDUCATION")
    
    p1 = (
        "The conceptual framework governing institutional quality assurance in higher technical education has undergone profound philosophical "
        "and operational transitions over the past half-century. Globally, the paradigm has shifted decisively from input-centric inspection regimes—which "
        "measured institutional merit primarily by physical assets such as campus acreage, library book volumes, and gross capital expenditure—toward "
        "rigorous, output-oriented Outcome-Based Education (OBE) paradigms that evaluate student learning attainments, pedagogical effectiveness, and "
        "continuous quality enhancement mechanisms (Spady, 1994; Biggs, 2003)."
    )
    add_paragraph(doc, p1)
    
    p2 = (
        "In the Indian higher education landscape, this transformation was catalyzed by the landmark establishment of the All India Council for Technical "
        "Education (AICTE) pursuant to the AICTE Act No. 52 of 1987. AICTE was endowed with statutory authority to regulate the establishment of new "
        "technical institutions, approve academic programs, mandate minimum infrastructural norms, and prescribe faculty qualification and cadre standards. "
        "AICTE operationalizes this legal mandate through its annual Approval Process Handbook (APH), a comprehensive statutory regulatory codex that "
        "stipulates exacting quantitative thresholds for institutional approvals, program extensions, and intake augmentations. In recent editions "
        "(AICTE APH 2024-2027), the Council has integrated progressive norms emphasizing multidisciplinary technical flexibility, industry-aligned faculty "
        "recruitment, and digital governance mandates."
    )
    add_paragraph(doc, p2)
    
    p3 = (
        "Concurrently, the international recognition of Indian engineering credentials necessitated alignment with the highest global benchmarks. "
        "In 1989, the world’s leading engineering accreditation agencies established the Washington Accord, an international multilateral agreement that "
        "recognizes the substantial equivalence of professional engineering degree programs accredited by signatory bodies. In 2014, India—represented by "
        "the National Board of Accreditation (NBA)—achieved permanent signatory status to the Washington Accord. This milestone mandated that Indian "
        "engineering curricula, examination systems, and evaluation frameworks be re-engineered strictly around Outcome-Based Education principles."
    )
    add_paragraph(doc, p3)
    
    p4 = (
        "Under the NBA accreditation paradigm, engineering institutions submit exhaustive Self-Assessment Reports (SAR) structured around ten "
        "interdependent criteria for Tier-I (autonomous colleges and university departments) and Tier-II (affiliated non-autonomous colleges) institutions. "
        "The NBA 1000-point rubric demands quantitative verification across a vast spectrum of indicators, including Program Educational Objectives (PEOs), "
        "Program Outcomes (POs 1 through 12), Course Outcomes (COs), Student-to-Faculty Ratios (SFR ≤ 1:15), Faculty Cadre Proportions (FCP), Faculty "
        "Retention Rates (FRR ≥ 85%), Student Success Indices (SI), and Placement and Higher Education Ratios. Simultaneously, the National Assessment "
        "and Accreditation Council (NAAC) enforces its Revised Accreditation Framework (RAF), which evaluates the holistic institutional health of colleges "
        "across seven criteria, weighting 70% of the score on quantitative metrics subjected to third-party Data Validation and Verification (DVV). "
        "Finally, the National Institutional Ranking Framework (NIRF) applies annual competitive benchmarking across Teaching, Learning & Resources (TLR), "
        "Research and Professional Practice (RPC), and Graduation Outcomes (GO)."
    )
    add_paragraph(doc, p4)
    
    # Table 2.1: Regulatory bodies comparison
    add_paragraph(doc, "Table 2.1: Comparative Analysis of Major Regulatory Accreditation Frameworks in India", font_size=11, bold=True, italic=True, space_after=4)
    tbl_reg = doc.add_table(rows=5, cols=5)
    tbl_reg.alignment = WD_TABLE_ALIGNMENT.CENTER
    reg_data = [
        ("Parameter", "AICTE (APH)", "NBA (SAR Tier-I)", "NAAC (RAF)", "NIRF Ranking"),
        ("Statutory Mandate", "Statutory Apex Regulator (Act 52 of 1987)", "Autonomous Programmatic Accreditation Body", "Autonomous Institutional Assessment Body (UGC)", "Ministry of Education Benchmarking Framework"),
        ("Focus Level", "Institutional & Infrastructural Compliance", "Program-Specific Outcome-Based Education", "Holistic Institutional Quality & Governance", "Comparative National Ranking & Performance"),
        ("Evaluation Model", "Input Norms & Spatial / Cadre Compliance", "1000-Point Rubric across 10 Criteria", "Seven Curricular & Institutional Criteria", "Metric Weightings (TLR, RPC, GO, OI, PR)"),
        ("Frequency", "Annual Approval Scrutiny Cycle", "Every 3 or 6 Years Cycle", "Every 5 Years (Cycle 1, 2, 3...)", "Annual Competitive Ranking Cycle"),
    ]
    for r_idx, row in enumerate(reg_data):
        for c_idx, val in enumerate(row):
            cell = tbl_reg.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.font.bold = True
                
    # 2.2 ADVANCES IN DOCUMENT AI AND OCR
    add_heading_2(doc, "2.2 ADVANCES IN DOCUMENT AI, LAYOUT ANALYSIS, AND TABLE EXTRACTION")
    
    p5 = (
        "Extracting structured regulatory entities from heterogeneous institutional dossiers represents a classic, highly challenging problem "
        "in Document AI and computer vision. Historically, document processing relied on standard Optical Character Recognition (OCR) engines such as "
        "Tesseract OCR (Smith, 2007) and ABBYY FineReader. While early OCR frameworks demonstrated reasonable character recognition on clean, single-column "
        "typewritten text, they suffered catastrophic failures when exposed to complex academic regulatory dossiers characterized by dense multi-page "
        "tabular layouts, merged header cells, nested tables, bilingual stamps, and degraded scan resolutions."
    )
    add_paragraph(doc, p5)
    
    p6 = (
        "The advent of deep learning transformed document analysis through multimodal vision-language models. The seminal LayoutLM series "
        "(Xu et al., 2020; Huang et al., 2022) established the power of joint pre-training over text, layout geometry (2D spatial bounding boxes), "
        "and visual image patches. LayoutLM demonstrated that understanding document semantics requires perceiving where text is placed relative to "
        "visual separators, cell borders, and header coordinates. Concurrently, end-to-end transformer architectures such as Donut (Kim et al., 2022) "
        "and Nougat (Blecher et al., 2023) explored OCR-free document parsing, mapping raw document images directly into structured JSON or LaTeX tokens. "
        "However, these end-to-end generative models exhibit severe hallucinations when processing non-standard financial balance sheets or dense "
        "50-row faculty rosters, often inventing numerical values or skipping middle rows."
    )
    add_paragraph(doc, p6)
    
    p7 = (
        "To achieve enterprise-grade fidelity on complex institutional portfolios, recent research has converged toward hybrid deep-parsing frameworks. "
        "The emergence of Docling (IBM Research, 2024) represents a state-of-the-art breakthrough in document layout analysis. Docling integrates deep "
        "visual layout detection models trained specifically on complex technical documentation, combined with high-precision programmatic PDF stream "
        "extractors (such as PyMuPDF). Docling explicitly segments document pages into semantically typed bounding boxes: headings, body paragraphs, "
        "table cells, footnotes, and figures. Crucially, Docling reconstructs the exact row-span, column-span, and structural grid of complex tabular data, "
        "converting chaotic visual layouts into clean, hierarchical Markdown and structured dictionaries. By bridging pixel-level vision with programmatic "
        "PDF token streams, Docling provides the robust structural foundation required for downstream cognitive language models."
    )
    add_paragraph(doc, p7)
    
    # Table 2.2: Document Processing Evolution
    add_paragraph(doc, "Table 2.2: Evolution of Document Processing Frameworks from OCR to Multimodal Cognitive Engines", font_size=11, bold=True, italic=True, space_after=4)
    tbl_doc = doc.add_table(rows=5, cols=5)
    tbl_doc.alignment = WD_TABLE_ALIGNMENT.CENTER
    doc_tech = [
        ("Generation", "Frameworks", "Underlying Architecture", "Table Handling Capability", "Hallucination Risk"),
        ("Gen 1: Classical OCR", "Tesseract OCR, CuneiForm", "Connected Component Analysis + HMM", "Extremely Poor (Raw Text Stream Only)", "Zero (Deterministic, but high typo rate)"),
        ("Gen 2: Layout Models", "LayoutLMv1-v3, BROS", "BERT + 2D Spatial Positional Embeddings", "Moderate (Extracts Bounding Box Text)", "Low (Sequence classification)"),
        ("Gen 3: OCR-Free Vision", "Donut, Nougat, Pix2Struct", "Swin Transformer Encoder + BART Decoder", "Variable (Struggles with Dense Tables)", "High (Token hallucination in tables)"),
        ("Gen 4: Hybrid Deep AI", "Docling + Gemini 2.5 Flash", "Visual Segmentation + Multimodal LLM", "Outstanding (Full Row/Col Span Recovery)", "Negligible (Schema-Grounded Outputs)"),
    ]
    for r_idx, row in enumerate(doc_tech):
        for c_idx, val in enumerate(row):
            cell = tbl_doc.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.font.bold = True
                
    # 2.3 LLMS IN REGULATORY GOVERNANCE
    add_heading_2(doc, "2.3 LARGE LANGUAGE MODELS IN REGULATORY GOVERNANCE AND ACADEMIC AUDITING")
    
    p8 = (
        "The emergence of advanced Large Language Models (LLMs), exemplified by OpenAI’s GPT-4 (Achiam et al., 2023) and Google’s Gemini family "
        "(Gemini Team, Google, 2024), has unlocked extraordinary frontiers in semantic reasoning, multi-document synthesis, and code generation. "
        "In domain-specific applications such as legal contract analysis, financial compliance, and medical informatics, LLMs have demonstrated the "
        "capacity to digest complex statutory texts and verify adherence to codified rules (Katz et al., 2024; Bommarito et al., 2023)."
    )
    add_paragraph(doc, p8)
    
    p9 = (
        "However, direct deployment of generic LLMs to higher education accreditation auditing encounters critical theoretical and operational roadblocks. "
        "The foremost obstacle is hallucination—the tendency of autoregressive language models to generate plausible-sounding but factually ungrounded "
        "or mathematically erroneous statements (Ji et al., 2023). In an AICTE or NBA regulatory audit, an AI hallucination that fabricates a single "
        "non-existent Professor or miscomputes an instructional space shortfall by 50 square meters can trigger catastrophic institutional consequences, "
        "including illegitimate approval revocations or unwarranted litigations. Consequently, naive zero-shot querying of LLMs is entirely unacceptable "
        "in high-stakes statutory compliance."
    )
    add_paragraph(doc, p9)
    
    p10 = (
        "To mitigate hallucination and enforce rigid mathematical determinism, modern AI engineering employs three crucial techniques: "
        "(1) In-Context Learning and Grounded Few-Shot Prompting (Brown et al., 2020), wherein the model is provided with explicit statutory definitions, "
        "handbook formulas, and few-shot exemplary input-output pairs; (2) Structured Output Decoding via Pydantic Schemas and JSON Schema mode, "
        "which forces the model’s decoding logits to adhere strictly to pre-compiled formal data models; and (3) Decoupled Cognitive Parsing and Deterministic "
        "Rule Execution (Madaan et al., 2023). Under this decoupled paradigm, the LLM is restricted exclusively to entity extraction and normalization "
        "(e.g., extracting faculty names, designations, dates of joining, and floor areas), while all mathematical computations (ratios, sums, thresholds, "
        "and rubric scores) are delegated to deterministic, mathematically verified Python code execution engines."
    )
    add_paragraph(doc, p10)
    
    # 2.4 TIME-SERIES AND FORECASTING
    add_heading_2(doc, "2.4 TIME-SERIES ANALYSIS AND PREDICTIVE FORECASTING IN EDUCATIONAL ANALYTICS")
    
    p11 = (
        "Academic analytics has evolved from descriptive dashboards toward predictive intelligence and prescriptively guided institutional "
        "governance (Siemens & Long, 2011; Baker & Inventado, 2014). In higher educational management, longitudinal tracking of academic performance "
        "indicators—such as graduation efficiency, faculty turnover, placement velocity, and research publication momentum—provides invaluable strategic "
        "foresight (Pardos et al., 2014)."
    )
    add_paragraph(doc, p11)
    
    p12 = (
        "Classical statistical time-series forecasting relies heavily on Autoregressive Integrated Moving Average (ARIMA) and Seasonal Autoregressive "
        "Integrated Moving Average (SARIMA) methodologies (Box et al., 2015). A standard SARIMA(p, d, q) x (P, D, Q)s model captures both non-seasonal "
        "autoregressive trends and periodic academic cycles (e.g., annual admission surges, semester examination result distributions, and campus placement "
        "seasons). When combined with multivariate polynomial regression, these statistical models can project institutional trajectory across three- to "
        "five-year planning horizons with quantifiable confidence intervals (Hyndman & Athanasopoulos, 2018). In an accreditation context, predictive "
        "modeling enables institutions to detect 'compliance drift'—identifying subtle, cumulative deficits years before a formal NBA or AICTE visit occurs, "
        "allowing timely corrective interventions."
    )
    add_paragraph(doc, p12)
    
    # 2.5 COMPARATIVE ANALYSIS
    add_heading_2(doc, "2.5 COMPARATIVE REVIEW OF EXISTING PLATFORMS AND RESEARCH GAPS")
    
    p13 = (
        "To establish the unique positioning and scholarly contribution of Smart Approval AI, existing commercial and academic solutions "
        "were systematically evaluated across seven cardinal capability dimensions: (1) Deep Multimodal PDF Table Parsing; (2) Cognitive LLM-Powered "
        "Entity Extraction; (3) Deterministic Multi-Framework Compliance Engines (AICTE, NBA, NAAC, NIRF); (4) Longitudinal Multi-Year Analytics; "
        "(5) Predictive Time-Series Forecasting (SARIMA); (6) Automated Cryptographic Report Generation; and (7) Dedicated Port-Isolated Microservices Architecture."
    )
    add_paragraph(doc, p13)
    
    # Table 2.3: Systematic Comparison
    add_paragraph(doc, "Table 2.3: Systematic Feature Comparison: Smart Approval AI vs Existing Industry & Academic Solutions", font_size=11, bold=True, italic=True, space_after=4)
    tbl_comp = doc.add_table(rows=6, cols=8)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_matrix = [
        ("Platform / System", "Deep Table OCR", "Cognitive LLM", "Multi-Reg. Rules", "Multi-Year Analytics", "SARIMA Forecast", "Auto Reports", "Port Isolated"),
        ("Traditional Manual Audit", "None (Manual)", "None (Manual)", "Manual (Error-prone)", "Partial (Spreadsheets)", "None", "Manual Typing", "N/A"),
        ("Campus ERPs (SAP/InPods)", "None (Form DB)", "None", "Rigid Static Forms", "Basic Dashboards", "None", "Static Templates", "No (Monolithic)"),
        ("Generic Cloud OCR (Textract)", "OCR BBoxes Only", "None", "None", "None", "None", "None (Raw JSON)", "No (Cloud API)"),
        ("Academic AI Prototypes", "Basic PyPDF", "Generic Zero-Shot", "Single Framework", "None", "None", "Rudimentary", "No (Port 8000)"),
        ("Smart Approval AI (Proposed)", "Docling + PyMuPDF", "Gemini 2.5 Flash", "AICTE+NBA+NAAC+NIRF", "Full Longitudinal", "Multivariate+SARIMA", "Full SAR/PDF/Word", "Yes (3051/8051)"),
    ]
    for r_idx, row in enumerate(comp_matrix):
        for c_idx, val in enumerate(row):
            cell = tbl_comp.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
            if r_idx == 5:
                run.font.bold = True
                
    # 2.6 SUMMARY OF RESEARCH GAPS
    add_heading_2(doc, "2.6 SUMMARY OF IDENTIFIED RESEARCH GAPS")
    
    p14 = (
        "The comprehensive literature review reveals four critical, unaddressed research and technological gaps in the current state-of-the-art:"
    )
    add_paragraph(doc, p14)
    
    gaps = [
        ("Gap 1: Absence of Layout-Aware Multimodal Parsing for Indian Regulatory Dossiers: ",
         "Existing higher education ERPs and OCR utilities treat regulatory PDF documents as linear text streams, completely discarding the complex 2D "
         "spatial relationships, nested headers, and merged cells inherent to AICTE Mandatory Disclosures and NBA SAR portfolios. A dedicated visual "
         "layout chunker specifically tuned for complex regulatory tables is urgently required."),
         
        ("Gap 2: Fragility and Hallucination Risks of Generic Generative AI in Regulatory Scrutiny: ",
         "Prior academic experiments applying generative AI to administrative documents have relied on ungrounded zero-shot prompting, yielding high "
         "hallucination rates in numerical extraction. There is a total lack of an integrated cognitive architecture combining multimodal LLMs with rigid "
         "Pydantic schemas and deterministic mathematical rule execution."),
         
        ("Gap 3: Compartmentalized, Single-Framework Evaluations Lacking Holistic Integration: ",
         "Current commercial software systems operate in isolated silos—focusing exclusively on NAAC or basic college attendance—without providing "
         "a unified regulatory intelligence hub capable of evaluating AICTE Approval Handbook norms, NBA Tier-I OBE rubrics, NAAC quantitative criteria, "
         "and NIRF parameters concurrently from a single institutional repository."),
         
        ("Gap 4: Absence of Predictive Longitudinal Forecasting in Institutional Quality Management: ",
         "Academic compliance evaluation has remained exclusively retrospective and episodic. Literature lacks an end-to-end framework that couples "
         "multi-year historical compliance extraction with predictive time-series models (e.g., SARIMA) to forecast compliance drift and provide actionable "
         "preventive interventions before formal regulatory inspections.")
    ]
    for gtitle, gdesc in gaps:
        p = add_paragraph(doc)
        p.add_run(gtitle).font.bold = True
        p.add_run(gdesc)
        
    doc.add_page_break()
    print("Built Chapter 2 successfully.")

if __name__ == "__main__":
    test_doc = docx.Document()
    build_chapter_2(test_doc)
    test_doc.save("thesis/test_ch2_out.docx")
    print("Saved test_ch2_out.docx")
