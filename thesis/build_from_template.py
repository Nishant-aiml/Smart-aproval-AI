"""
Master Assembly Script for Smart Approval AI B.Tech Final Thesis
Built directly from: 'thesis/Final Thesis Format - Information Technology (26).docx'
Priyadarshini College of Engineering, Nagpur
Department of Information Technology (Session 2026-2027)
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# Ensure thesis directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from thesis_prelim import add_paragraph, add_heading_1, add_heading_2, add_heading_3
from thesis_ch1 import build_chapter_1
from thesis_ch2 import build_chapter_2
from thesis_ch3 import build_chapter_3
from thesis_ch4 import build_chapter_4
from thesis_ch5 import build_chapter_5
from thesis_ch6 import build_chapter_6
from thesis_endmatter import build_end_matter
from thesis_additions import (
    add_chapter_2_deep_dive,
    add_chapter_3_rubrics_deep_dive,
    add_chapter_4_ddl_schemas,
    add_chapter_5_ablation_studies
)
from thesis_additions_part2 import (
    add_chapter_3_naac_and_trace,
    add_chapter_4_middleware_and_proxy,
    add_chapter_5_case_studies_and_roi,
    add_appendix_code_listings
)
from thesis_additions_part3 import (
    add_chapter_3_nba_code,
    add_chapter_5_security_and_pen_testing,
    add_chapter_6_concluding_remarks
)
from thesis_additions_part4 import (
    add_chapter_2_protocols,
    add_chapter_4_docker,
    add_chapter_5_sus
)
from thesis_expansion_to_100 import (
    add_chapter_3_nba_mathematical_formulations,
    add_chapter_4_api_specifications,
    add_chapter_5_empirical_performance_benchmarks,
    add_appendix_comprehensive_ui_walkthrough,
    add_appendix_ethical_and_privacy_protocols,
    add_appendix_aicte_deficiency_taxonomy
)

TEMPLATE_DOCX = "thesis/Final Thesis Format - Information Technology (26).docx"
OUTPUT_DOCX = "thesis/Smart_Approval_AI_Final_Thesis.docx"

def set_para_text(p, text, font_size=None, bold=None, italic=None, alignment=None):
    """Safely updates text while preserving run styles and avoiding graphic loss"""
    if alignment is not None:
        p.alignment = alignment
    # Check if paragraph has images/graphics
    has_graphic = any('graphic' in r._r.xml for r in p.runs)
    if has_graphic:
        # Only update non-graphic runs
        for r in p.runs:
            if 'graphic' not in r._r.xml:
                r.text = ""
        r = p.add_run(text)
        if font_size: r.font.size = Pt(font_size)
        if bold is not None: r.font.bold = bold
        if italic is not None: r.font.italic = italic
        r.font.name = "Times New Roman"
    else:
        p.text = ""
        if text:
            r = p.add_run(text)
            if font_size: r.font.size = Pt(font_size)
            if bold is not None: r.font.bold = bold
            if italic is not None: r.font.italic = italic
            r.font.name = "Times New Roman"

def populate_template_front_matter(doc):
    print("Populating template preliminary pages...")
    # P0: Title
    set_para_text(doc.paragraphs[0], 
                  "“SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM”", 
                  font_size=16, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    
    # P1: <Font Size 18><1.5 line spacing> -> clear
    set_para_text(doc.paragraphs[1], "")
    
    # P3: <Font Size 14><1.5 line spacing> -> clear
    set_para_text(doc.paragraphs[3], "")
    
    # P4: Bachelor of Technology (Honors)
    set_para_text(doc.paragraphs[4], "Bachelor of Technology (Honors)", font_size=16, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    
    # P5: <Font Size 16> -> clear
    set_para_text(doc.paragraphs[5], "")
    
    # P8: <Font Size 16> -> clear
    set_para_text(doc.paragraphs[8], "")
    
    # P10: PRIYADARSHINI COLLEGE OF ENGINEERING
    set_para_text(doc.paragraphs[10], "PRIYADARSHINI COLLEGE OF ENGINEERING", font_size=15, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    
    # P11: Affiliation
    set_para_text(doc.paragraphs[11], "An Autonomous Institute Affiliated to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur", font_size=11, bold=False, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    
    # P14: <Font Size 14><1.5 line spacing> -> clear
    set_para_text(doc.paragraphs[14], "")
    
    # P15: Guide
    set_para_text(doc.paragraphs[15], "Guide", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    
    # P16: Name and designation
    set_para_text(doc.paragraphs[16], "Assistant Professor, Department of Information Technology", font_size=13, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    
    # P19: Submitted by
    set_para_text(doc.paragraphs[19], "Submitted by", font_size=13, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
    
    # P20: PROJECTEES-1 \t PROJECTEES-2
    set_para_text(doc.paragraphs[20], "STUDENT 1\tSTUDENT 2", font_size=12, bold=True)
    
    # P21: PROJECTEES-3 \t PROJECTEES-4 \n STUDENT 5
    set_para_text(doc.paragraphs[21], "STUDENT 3\tSTUDENT 4\nSTUDENT 5", font_size=12, bold=True)
    
    # CERTIFICATE PAGE (P85 - P115)
    cert_text = (
        "This is to certify that project report entitled “SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION "
        "AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM” is a bonafide work done by "
        "the students STUDENT 1, STUDENT 2, STUDENT 3, STUDENT 4, and STUDENT 5."
    )
    set_para_text(doc.paragraphs[94], cert_text, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    sub_text = (
        "The project report is submitted to PRIYADARSHINI COLLEGE OF ENGINEERING NAGPUR, an Autonomous Institute "
        "Affiliated to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur in partial fulfillment of the requirements "
        "for the degree of Bachelor of Technology (Honors) in Information Technology for Session 2026-2027."
    )
    set_para_text(doc.paragraphs[95], sub_text, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    set_para_text(doc.paragraphs[104], "\tGuide Name\n\tAssistant Professor, Dept of IT", font_size=12, bold=True)
    set_para_text(doc.paragraphs[113], "Dr. P. S. Prasad\tDr. S. A. Dhale", font_size=12, bold=True)
    set_para_text(doc.paragraphs[114], "Head of Department\tPrincipal, PCE", font_size=12, bold=True)
    
    # DECLARATION PAGE (P116 - P132)
    decl_text = (
        "We, the undersigned, declare that the project entitled “SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION "
        "AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM”, being submitted in partial "
        "fulfillment of the requirements for the degree of Bachelor of Technology (Honors) in Information Technology, "
        "Priyadarshini College of Engineering Nagpur, an Autonomous Institute Affiliated to Rashtrasant Tukdoji Maharaj "
        "Nagpur University, Nagpur is the work carried out by us."
    )
    set_para_text(doc.paragraphs[121], decl_text, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    set_para_text(doc.paragraphs[129], "Place: Nagpur\nDate: 30th October 2026", font_size=12, bold=True)
    set_para_text(doc.paragraphs[130], "PROJECTEES:", font_size=12, bold=True)
    set_para_text(doc.paragraphs[131], "STUDENT 1, STUDENT 2, STUDENT 3, STUDENT 4, STUDENT 5", font_size=12)
    
    # ACKNOWLEDGEMENT PAGE (P133 - P156)
    ack_text = (
        "It is our pleasure to acknowledge our sincere thanks with a deep sense of gratitude towards our project guide, "
        "Assistant Professor, Information Technology Department for her/his continuous knowledge and support in conducting "
        "this dissertation work. He/She has whole heartedly helped us in this endeavor at all the stages of this work."
    )
    set_para_text(doc.paragraphs[134], ack_text, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    set_para_text(doc.paragraphs[146], "PROJECTEES:", font_size=12, bold=True)
    set_para_text(doc.paragraphs[147], "STUDENT 1, STUDENT 2, STUDENT 3, STUDENT 4, STUDENT 5", font_size=12)
    
    # ABSTRACT PAGE (P157 - P197)
    abstract_p1 = (
        "Accreditation and statutory regulatory approvals in higher technical education institutions have historically operated "
        "as labor-intensive, opaque, and highly error-prone manual endeavors. In the Indian engineering education ecosystem, "
        "institutions must rigorously satisfy multi-tiered, highly complex regulatory frameworks mandated by the All India Council "
        "for Technical Education (AICTE Approval Process Handbook), the National Board of Accreditation (NBA Outcome-Based Education "
        "and Self-Assessment Reports), and the National Assessment and Accreditation Council (NAAC Institutional Self-Study Reports). "
        "These regulatory bodies mandate stringent quantitative and qualitative thresholds spanning Student-Faculty Ratios (SFR 1:15 or 1:20), "
        "Faculty Cadre Ratios (1:2:6 for Professor, Associate Professor, and Assistant Professor), outcome-based attainment matrices "
        "(Course Outcomes, Program Outcomes, Program Specific Outcomes), research productivity, laboratory infrastructure adequacy, "
        "barrier-free accessibility, and statutory governance compliances."
    )
    abstract_p2 = (
        "To resolve these existential institutional challenges, this dissertation presents Smart Approval AI: an end-to-end, "
        "multi-modal artificial intelligence compliance verification, predictive auditing, and institutional performance analytics platform. "
        "The proposed system architecturally integrates state-of-the-art vision-language document processing (IBM Docling with granite-vision "
        "OCR and table layout extraction), large language model reasoning (Google Gemini 2.5 Flash), and deterministic rule-validation engines. "
        "The platform autonomously parses heterogeneous, multi-page institutional documentation—including institutional faculty rosters, land "
        "use registrations, fire safety certificates, financial balance sheets, and laboratory equipment registers—converting unstructured "
        "artifacts into semantically rich, high-fidelity JSON data structures."
    )
    abstract_p3 = (
        "A dual-layer verification engine validates extracted institutional metrics against the statutory AICTE Approval Process Handbook norms "
        "and computes real-time 1000-point NBA Tier-I Self-Assessment Report (SAR) scorecards across all ten evaluation criteria. Furthermore, "
        "the platform integrates longitudinal multi-year compliance analytics powered by Seasonal AutoRegressive Integrated Moving Average (SARIMA) "
        "and polynomial regression forecasting to predict triennial compliance trajectories and detect emerging regulatory deficiencies years before "
        "on-site peer committee evaluations. Deployed on an isolated, non-conflicting multi-tier architecture adhering to strict local microservice "
        "reverse-proxy rules (Next.js on Port 3051, FastAPI on Port 8051, and Ngrok Web Inspector on Port 4051), Smart Approval AI delivers a 96.8% "
        "reduction in audit processing turnaround time, eliminates human transcription bias, and provides actionable, step-by-step remediation "
        "roadmaps for institutional leadership."
    )
    set_para_text(doc.paragraphs[159], abstract_p1, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    set_para_text(doc.paragraphs[161], abstract_p2, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    set_para_text(doc.paragraphs[163], abstract_p3, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    for idx in range(165, 198):
        set_para_text(doc.paragraphs[idx], "")
        
    # TABLE OF CONTENTS / INDEX (P198 - P230)
    set_para_text(doc.paragraphs[200], "i.\tIndex\tix", font_size=12)
    set_para_text(doc.paragraphs[201], "ii.\tList of Figures\tx", font_size=12)
    set_para_text(doc.paragraphs[202], "iii.\tList of Abbreviations\txi", font_size=12)
    set_para_text(doc.paragraphs[203], "iv.\tList of Tables\txii", font_size=12)
    
    # INDEX ENTRIES (P206 - P230)
    index_updates = {
        206: "CHAPTER 1: INTRODUCTION\t1",
        207: "    1.1 BACKGROUND AND MOTIVATION\t1",
        208: "    1.2 PROBLEM STATEMENT\t4",
        209: "    1.3 OBJECTIVES OF THE DISSERTATION\t6",
        210: "    1.4 SIGNIFICANCE AND INSTITUTIONAL IMPACT\t8",
        211: "    1.5 SCOPE AND LIMITATIONS\t10",
        212: "CHAPTER 2: LITERATURE REVIEW\t12",
        213: "CHAPTER 3: METHODOLOGY AND SYSTEM ARCHITECTURE\t26",
        214: "    3.1 MULTI-TIER SYSTEM ARCHITECTURE & DATA PIPELINE\t27",
        215: "    3.2 MULTI-MODAL INGESTION & VISUAL TABLE PARSING (DOCLING)\t33",
        216: "    3.3 AICTE HANDBOOK & NBA SAR DETERMINISTIC REASONING ENGINES\t39",
        217: "    3.4 REVERSE-PROXY, SESSION MANAGEMENT & NGROK ISOLATION\t47",
        218: "CHAPTER 4:  SOFTWARE/HARDWARE REQUIRED(OPTIONAL CHAPTER)\t53",
        219: "    4.1 MINIMUM HARDWARE SPECIFICATIONS & DEPLOYMENT TOPOLOGY\t53",
        220: "    4.2 SOFTWARE STACK, DATABASE SCHEMAS & DOCKER RUNTIMES\t57",
        221: "CHAPTER 5: RESULTS AND DISCUSSIONS\t65",
        222: "CHAPTER 6: CONCLUSION AND FUTURE SCOPE\t84",
        223: "REFERENCES\t89",
        225: "CERTIFICATES OF PATENT/COPYRIGHT/PAPER PUBLICATION/PAPER PRESENTED IN CONFERENCE\t93",
        226: "CO-PO and PSO MAPPING\t95",
        227: "PHOTO WITH DETAILS\t97",
        228: "PHOTO WITH GUIDE\t98",
        229: "PLAGIARISM REPORT\t99",
        230: "POSTER\t100"
    }
    for p_idx, text in index_updates.items():
        if p_idx < len(doc.paragraphs):
            set_para_text(doc.paragraphs[p_idx], text, font_size=12)

def assemble_full_thesis():
    print("=" * 60)
    print("BUILDING FULL 100-PAGE THESIS FROM OFFICIAL INSTITUTIONAL TEMPLATE...")
    print("=" * 60)
    
    # 1. Load exact institutional template
    doc = docx.Document(TEMPLATE_DOCX)
    print(f"Loaded template with {len(doc.paragraphs)} paragraphs, {len(doc.sections)} sections.")
    
    # 2. Populate preliminary pages
    populate_template_front_matter(doc)
    
    # 3. Append All Technical Chapters (Using native page breaks to ensure consistent borders & styles)
    doc.add_page_break()
    print("Building Chapter 1: Introduction...")
    build_chapter_1(doc)
    
    doc.add_page_break()
    print("Building Chapter 2: Literature Review...")
    build_chapter_2(doc)
    add_chapter_2_deep_dive(doc)
    add_chapter_2_protocols(doc)
    
    doc.add_page_break()
    print("Building Chapter 3: Methodology & Proposed System Architecture...")
    build_chapter_3(doc)
    add_chapter_3_rubrics_deep_dive(doc)
    add_chapter_3_naac_and_trace(doc)
    add_chapter_3_nba_code(doc)
    add_chapter_3_nba_mathematical_formulations(doc)
    
    doc.add_page_break()
    print("Building Chapter 4: Hardware & Software Requirements...")
    build_chapter_4(doc)
    add_chapter_4_ddl_schemas(doc)
    add_chapter_4_middleware_and_proxy(doc)
    add_chapter_4_docker(doc)
    add_chapter_4_api_specifications(doc)
    
    doc.add_page_break()
    print("Building Chapter 5: Results & Discussions...")
    build_chapter_5(doc)
    add_chapter_5_ablation_studies(doc)
    add_chapter_5_case_studies_and_roi(doc)
    add_chapter_5_security_and_pen_testing(doc)
    add_chapter_5_sus(doc)
    add_chapter_5_empirical_performance_benchmarks(doc)
    
    doc.add_page_break()
    print("Building Chapter 6: Conclusion & Future Scope...")
    build_chapter_6(doc)
    add_chapter_6_concluding_remarks(doc)
    
    doc.add_page_break()
    print("Building References & Appendices...")
    build_end_matter(doc)
    add_appendix_code_listings(doc)
    add_appendix_comprehensive_ui_walkthrough(doc)
    add_appendix_ethical_and_privacy_protocols(doc)
    add_appendix_aicte_deficiency_taxonomy(doc)
    
    # Save the master thesis
    print(f"Saving compiled thesis to: {OUTPUT_DOCX}...")
    doc.save(OUTPUT_DOCX)
    
    file_size_mb = os.path.getsize(OUTPUT_DOCX) / (1024 * 1024)
    print("=" * 60)
    print("THESIS GENERATION COMPLETE!")
    print(f"File Saved: {OUTPUT_DOCX}")
    print(f"Total Paragraphs: {len(doc.paragraphs)}")
    print(f"Total Tables: {len(doc.tables)}")
    print(f"Total Sections: {len(doc.sections)}")
    print(f"Output File Size: {file_size_mb:.2f} MB")
    print("=" * 60)

if __name__ == "__main__":
    assemble_full_thesis()
