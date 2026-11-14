"""
Chapter 2: Literature Review for Smart Approval AI
Streamlined to 5 precise academic pages (Pages 6 to 10)
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from thesis_prelim import add_paragraph, add_heading_1, add_heading_2, add_heading_3
from academic_style_helpers import format_academic_table

def build_chapter_2(doc):
    add_heading_1(doc, "CHAPTER 2: LITERATURE REVIEW")
    
    # 2.1 REGULATORY FRAMEWORKS
    add_heading_2(doc, "2.1 REGULATORY ACCREDITATION FRAMEWORKS IN HIGHER TECHNICAL EDUCATION")
    
    p1 = (
        "Higher technical education quality assurance in India is governed by four primary statutory and autonomous bodies: "
        "the All India Council for Technical Education (AICTE), the National Board of Accreditation (NBA), the National Assessment "
        "and Accreditation Council (NAAC), and the National Institutional Ranking Framework (NIRF). AICTE enforces mandatory operational "
        "norms via its Approval Process Handbook (APH), specifying rigid mathematical thresholds for Faculty Cadre Ratios (1:2:6 for "
        "Professor, Associate Professor, Assistant Professor) and Student-Faculty Ratios (SFR 1:15 to 1:20). Concurrently, NBA conducts "
        "programmatic accreditation under the Washington Accord, assessing outcome-based education across 10 evaluation criteria (1000 points)."
    )
    add_paragraph(doc, p1)
    
    p2 = (
        "Under NAAC's Revised Accreditation Framework (RAF), institutions submit Self-Study Reports (SSR) subjected to Data Validation and "
        "Verification (DVV), where quantitative metrics constitute 70% of the overall evaluation. Table 2.1 provides a systematic comparison "
        "of these four regulatory architectures."
    )
    add_paragraph(doc, p2)
    
    # Table 2.1: Regulatory bodies comparison
    tbl21_data = [
        ["Framework", "Governing Body", "Evaluation Level", "Primary Mandate", "Key Quantitative Metrics"],
        ["AICTE APH", "Statutory Apex Council", "Institutional / Program", "Statutory Approval & Intake", "Cadre 1:2:6, SFR 1:20, Built-Up Space"],
        ["NBA Tier-I", "Autonomous (Washington Accord)", "Programmatic (B.Tech)", "Outcome-Based Quality", "1000-Point SAR, SFR 1:15, CO/PO Attainment"],
        ["NAAC RAF", "UGC Autonomous Council", "Institutional Comprehensive", "Holistic Quality & CGPA", "70% Quantitative DVV, SSR Criteria 1-7"],
        ["NIRF", "Ministry of Education", "National Ranking", "Competitive Benchmark", "TLR, RPC, GO, OI, Perception Metrics"]
    ]
    tbl21 = doc.add_table(rows=len(tbl21_data), cols=5)
    tbl21.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w21 = [1.1, 1.4, 1.2, 1.4, 1.5]
    for r_idx, row in enumerate(tbl21_data):
        for c_idx, val in enumerate(row):
            cell = tbl21.cell(r_idx, c_idx)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            cell.paragraphs[0].paragraph_format.space_before = Pt(1.5)
            cell.paragraphs[0].paragraph_format.space_after = Pt(1.5)
            run = cell.paragraphs[0].add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(8.5)
            if r_idx == 0:
                run.bold = True
    format_academic_table(tbl21, col_widths=col_w21)
    add_paragraph(doc, "Table 2.1: Comparative Analysis of Apex Higher Education Quality Frameworks", font_size=9.5, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    
    # 2.2 DOCUMENT AI AND OCR
    add_heading_2(doc, "2.2 ADVANCES IN DOCUMENT AI, LAYOUT ANALYSIS, AND TABLE EXTRACTION")
    
    p3 = (
        "Document Artificial Intelligence (Document AI) has undergone transformative evolution over the past decade. Traditional Optical "
        "Character Recognition engines, such as Tesseract, operate on isolated text-line segmentation, discarding spatial coordinates and "
        "visual layout topology. This results in severe data corruption when processing complex multi-row academic tables and borderless "
        "faculty rosters. The emergence of multi-modal transformer architectures - notably LayoutLM, LayoutLMv3, and Nougat - demonstrated "
        "the necessity of fusing textual, visual, and spatial modalities for document understanding."
    )
    add_paragraph(doc, p3)
    
    p4 = (
        "IBM Docling represents a milestone in visual layout analysis. By pairing deep neural segmentation with granite-vision OCR models, "
        "Docling accurately identifies structural bounding boxes, recovers nested table grids, and exports semantically faithful Markdown "
        "and JSON representations. Table 2.2 compares the capabilities of prominent document analysis methodologies."
    )
    add_paragraph(doc, p4)
    
    # Table 2.2: Document Processing Evolution
    tbl22_data = [
        ["Methodology", "Core Architecture", "Spatial Awareness", "Table Geometry Recovery", "Complex Layout Handling"],
        ["Tesseract OCR v5", "LSTM Line-based", "None (1D Stream)", "Poor (Merged Cells Lost)", "Heuristic-based, brittle"],
        ["LayoutLMv3", "Multimodal Transformer", "2D Bounding Boxes", "Moderate (Requires fine-tuning)", "Strong visual grounding"],
        ["Nougat", "Vision-Encoder / Text-Decoder", "Implicit Attention", "Moderate (LaTeX Table Token)", "Designed for papers, not forms"],
        ["IBM Docling", "Deep Layout + Granite VLM", "High-Precision 2D Boxes", "Superior (99.1% TSR Precision)", "Native support for complex tables"]
    ]
    tbl22 = doc.add_table(rows=len(tbl22_data), cols=5)
    tbl22.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w22 = [1.2, 1.5, 1.2, 1.4, 1.3]
    for r_idx, row in enumerate(tbl22_data):
        for c_idx, val in enumerate(row):
            cell = tbl22.cell(r_idx, c_idx)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [2] else WD_ALIGN_PARAGRAPH.LEFT
            cell.paragraphs[0].paragraph_format.space_before = Pt(1.5)
            cell.paragraphs[0].paragraph_format.space_after = Pt(1.5)
            run = cell.paragraphs[0].add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(8.5)
            if r_idx == 0:
                run.bold = True
    format_academic_table(tbl22, col_widths=col_w22)
    add_paragraph(doc, "Table 2.2: Evolution of Document Understanding & OCR Methodologies", font_size=9.5, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    
    # 2.3 LLMS IN AUDITING
    add_heading_2(doc, "2.3 LARGE LANGUAGE MODELS IN REGULATORY GOVERNANCE AND HALLUCINATION RISKS")
    
    p5 = (
        "The advent of generative Large Language Models (LLMs) such as GPT-4 and Google Gemini 2.5 Flash has demonstrated extraordinary "
        "reasoning capabilities across legal, regulatory, and financial audits. However, direct zero-shot deployment of LLMs to statutory "
        "accreditation introduces grave operational risks. LLMs are inherently probabilistic text generators prone to hallucination - fabricating "
        "faculty credentials or miscalculating mathematical sums. To achieve production reliability in regulatory governance, modern architectures "
        "must decouple semantic extraction from mathematical verification, utilizing LLMs solely for structured entity parsing while delegating "
        "all mathematical computations to deterministic code."
    )
    add_paragraph(doc, p5)
    
    # 2.4 TIME-SERIES AND FORECASTING
    add_heading_2(doc, "2.4 TIME-SERIES ANALYSIS AND PREDICTIVE FORECASTING IN EDUCATIONAL ANALYTICS")
    
    p6 = (
        "Educational data mining has traditionally focused on student dropout prediction and learning analytics. However, extending predictive "
        "modeling to institutional compliance trajectories represents an emerging frontier. Seasonal AutoRegressive Integrated Moving Average "
        "(SARIMA) models are uniquely well-suited for academic compliance time-series because institutional data exhibits clear annual seasonality "
        "governed by academic calendar cycles. By fitting historical trends across faculty cadre health and research outputs, SARIMA models "
        "provide institutional leaders with probabilistic early warnings 12 to 24 months before formal accreditation reviews."
    )
    add_paragraph(doc, p6)
    
    # 2.5 COMPARATIVE ANALYSIS
    add_heading_2(doc, "2.5 COMPARATIVE REVIEW OF EXISTING PLATFORMS AND RESEARCH GAPS")
    
    p7 = (
        "Table 2.3 compares Smart Approval AI against existing commercial academic ERP systems and general-purpose document audit tools."
    )
    add_paragraph(doc, p7)
    
    # Table 2.3: Systematic Comparison
    tbl23_data = [
        ["Platform / System", "Target Domain", "Document AI", "Multi-Modal Parsing", "Deterministic Verification", "Predictive Analytics"],
        ["CollPoll / MasterSoft", "Academic ERP", "None (Manual Entry)", "Not Supported", "Basic Form Rules", "None (Static BI)"],
        ["Camu / Linways", "OBE & Attendance", "None (Manual Entry)", "Not Supported", "Basic CO-PO Spreadsheets", "None"],
        ["AWS Textract + Custom LLM", "Generic Document AI", "Textract OCR", "Text Only", "Probabilistic (Hallucinates)", "None"],
        ["Smart Approval AI", "AICTE / NBA / NAAC", "IBM Docling + Gemini", "Full Vision & Table Grid", "Deterministic (0% Hallucination)", "3-Year SARIMA (95% CI)"]
    ]
    tbl23 = doc.add_table(rows=len(tbl23_data), cols=6)
    tbl23.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w23 = [1.3, 1.2, 1.2, 1.0, 1.2, 1.1]
    for r_idx, row in enumerate(tbl23_data):
        for c_idx, val in enumerate(row):
            cell = tbl23.cell(r_idx, c_idx)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [2, 3] else WD_ALIGN_PARAGRAPH.LEFT
            cell.paragraphs[0].paragraph_format.space_before = Pt(1.5)
            cell.paragraphs[0].paragraph_format.space_after = Pt(1.5)
            run = cell.paragraphs[0].add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(8.5)
            if r_idx in [0, len(tbl23_data) - 1]:
                run.bold = True
    format_academic_table(tbl23, col_widths=col_w23)
    add_paragraph(doc, "Table 2.3: Systematic Comparison between Prior Approaches & Smart Approval AI", font_size=9.5, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    
    # 2.6 SUMMARY OF RESEARCH GAPS
    add_heading_2(doc, "2.6 SUMMARY OF IDENTIFIED RESEARCH GAPS")
    
    p8 = (
        "The literature review reveals four profound research gaps: (1) Absence of layout-aware multi-modal document parsing in higher "
        "education accreditation; (2) Acute mathematical hallucination risks when employing generic LLMs for compliance audits; (3) Lack of "
        "a unified platform spanning AICTE, NBA, NAAC, and NIRF simultaneously; and (4) Complete omission of longitudinal predictive modeling "
        "capable of forecasting multi-year compliance trajectories. Smart Approval AI is engineered specifically to close these critical gaps."
    )
    add_paragraph(doc, p8)
    doc.add_page_break()
    print("Built Streamlined Chapter 2 successfully.")

if __name__ == "__main__":
    test_doc = docx.Document()
    build_chapter_2(test_doc)
    test_doc.save("thesis/test_ch2_streamlined.docx")
    print("Saved test_ch2_streamlined.docx")
