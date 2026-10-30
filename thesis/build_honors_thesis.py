"""
Exact Honors Format Builder for Smart Approval AI B.Tech Dissertation
Priyadarshini College of Engineering, Nagpur
Department of Information Technology
Populates all exact project, student, and guide details:
- Project: Smart Approval AI
- Students: Nishant Datta & Nazish Khan
- Guide: Dr. Archana Potnurwar (Associate Professor)
- Co-Guide: Ms. Lalita Charpe (Assistant Professor)
- HOD: Dr. P. S. Prasad (Head of Department)
- Principal: Dr. S. A. Dhale (Principal, PCE)
- Vice Principal: Dr. G. M. Asutkar
- Academic Session: 2026-2027
Directly builds the exact 8 Preliminary Pages and appends all technical chapters.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Ensure thesis directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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
from academic_style_helpers import format_academic_table, add_equation

OUTPUT_DOCX = "thesis/Smart_Approval_AI_Final_Thesis.docx"
FINAL_PDF = "thesis/Smart_Approval_AI_Final_Thesis.pdf"
LOGO_PATH = "thesis/extracted_assets/image_1.png"

def add_p(doc, text="", font_size=12, bold=False, italic=False, underline=False,
          alignment=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.5, space_before=0, space_after=4, color=(0, 0, 0)):
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.underline = underline
        run.font.color.rgb = RGBColor(*color)
    return p

def apply_page_border(sect):
    border_xml = parse_xml(
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
        f'<w:top w:val="single" w:color="000000" w:sz="18" w:space="24"/>'
        f'<w:left w:val="single" w:color="000000" w:sz="18" w:space="24"/>'
        f'<w:bottom w:val="single" w:color="000000" w:sz="18" w:space="24"/>'
        f'<w:right w:val="single" w:color="000000" w:sz="18" w:space="24"/>'
        f'</w:pgBorders>'
    )
    sect._sectPr.append(border_xml)

def add_borderless_table(doc, rows, cols, col_widths=None):
    tbl = doc.add_table(rows=rows, cols=cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = tbl._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="none"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)
    if col_widths:
        for row in tbl.rows:
            for i, w in enumerate(col_widths):
                if i < len(row.cells):
                    row.cells[i].width = Inches(w)
    return tbl

def set_cell(cell, text="", font_size=12, bold=False, italic=False, alignment=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15, space_before=0, space_after=2):
    p = cell.paragraphs[0]
    p.alignment = alignment
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.italic = italic
    return p

def build_honors_preliminary_pages(doc):
    print("Building exact 8 Preliminary Pages with Full Project, Student & Guide Details...")
    
    # -------------------------------------------------------------
    # PAGE 1: TITLE / COVER PAGE
    # -------------------------------------------------------------
    add_p(doc, "“SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM”",
          font_size=15, bold=True, space_before=0, space_after=6, line_spacing=1.3)
    
    add_p(doc, "A Project Report Submitted in partial fulfillment of the requirements for the Degree of",
          font_size=12, space_after=3, line_spacing=1.2)
    add_p(doc, "Bachelor of Technology (Honors)", font_size=15, bold=True, space_after=2)
    add_p(doc, "in", font_size=12, space_after=2)
    add_p(doc, "Information Technology", font_size=15, bold=True, space_after=2)
    add_p(doc, "Department of Information Technology", font_size=13, bold=True, space_after=3)
    add_p(doc, "to", font_size=12, space_after=2)
    add_p(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING", font_size=14, bold=True, space_after=2)
    add_p(doc, "An Autonomous Institute Affiliated to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur",
          font_size=10, space_after=8)
    
    add_p(doc, "Under the guidance of", font_size=12, bold=True, space_after=3)
    tbl_guide_cover = add_borderless_table(doc, 1, 2, [3.2, 3.2])
    
    # Left: Co-Guide
    c_left = tbl_guide_cover.cell(0, 0)
    set_cell(c_left, "Ms. Lalita Charpe", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_cg1 = c_left.add_paragraph()
    p_cg1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cg1.paragraph_format.line_spacing = 1.1
    p_cg1.paragraph_format.space_after = Pt(1)
    r_cg1 = p_cg1.add_run("Co-Guide\nAssistant Professor\nDepartment of Information Technology")
    r_cg1.font.name = "Times New Roman"
    r_cg1.font.size = Pt(10)
    
    # Right: Guide
    c_right = tbl_guide_cover.cell(0, 1)
    set_cell(c_right, "Dr. Archana Potnurwar", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_g1 = c_right.add_paragraph()
    p_g1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_g1.paragraph_format.line_spacing = 1.1
    p_g1.paragraph_format.space_after = Pt(1)
    r_g1 = p_g1.add_run("Guide\nAssociate Professor\nDepartment of Information Technology")
    r_g1.font.name = "Times New Roman"
    r_g1.font.size = Pt(10)
    
    add_p(doc, "Submitted by", font_size=12, italic=True, space_before=4, space_after=2)
    tbl_students_cover = add_borderless_table(doc, 1, 2, [3.2, 3.2])
    c_s1 = tbl_students_cover.cell(0, 0)
    set_cell(c_s1, "Nishant Datta", font_size=12.5, bold=True, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    c_s2 = tbl_students_cover.cell(0, 1)
    set_cell(c_s2, "Nazish Khan", font_size=12.5, bold=True, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    
    # Logo
    if os.path.exists(LOGO_PATH):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(LOGO_PATH, width=Inches(1.2))
        
    add_p(doc, "DEPARTMENT OF INFORMATION TECHNOLOGY", font_size=12.5, bold=True, space_after=2)
    add_p(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR-440019", font_size=12.5, bold=True, space_after=2)
    add_p(doc, "2026-2027", font_size=12.5, bold=True, space_after=0)
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 2: VISION & MISSION
    # -------------------------------------------------------------
    add_p(doc, "VISION OF THE INSTITUTE", font_size=12, bold=True, space_before=2, space_after=3)
    p_v = (
        "To become one of India’s leading engineering institutes in both education and research. We "
        "are committed to provide quality and state-of-the-art technical education to our students, so that "
        "they become technologically superior and in turn contribute to creating a great society."
    )
    add_p(doc, p_v, font_size=10.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.15)
    
    add_p(doc, "MISSION OF THE INSTITUTE", font_size=12, bold=True, space_after=3)
    m_points = [
        "i.   Fostering a dynamic learning environment that equips students with technical expertise, problem-solving skills, and a deep commitment to ethical practices.",
        "ii.  To cultivate a culture of innovation, incubation, research, and entrepreneurship that drives technological advancements.",
        "iii. To uphold the spirit of mutual excellence while interacting with stakeholders of our institutional ecosystem.",
        "iv.  Promoting lifelong learning, professional growth, and ensuring the holistic development of students and the well-being of society."
    ]
    for pt in m_points:
        add_p(doc, pt, font_size=10.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2, line_spacing=1.15)
        
    add_p(doc, "VISION OF THE DEPARTMENT", font_size=12, bold=True, space_before=4, space_after=3)
    dept_v = (
        "To nurture students with the latest technology and research, helping them to become valuable "
        "contributors who can address the changing needs of the IT industry and society."
    )
    add_p(doc, dept_v, font_size=10.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.15)
    
    add_p(doc, "MISSION OF THE DEPARTMENT", font_size=12, bold=True, space_after=3)
    dept_m_points = [
        "i.   To create a holistic learning environment that empowers emerging graduates with advanced technical and value-based education.",
        "ii.  To attain professional excellence in the field of Information Technology and allied multidisciplinary areas.",
        "iii. To encourage transformative learning for research addressing the changing needs of society and fostering lifelong learning."
    ]
    for pt in dept_m_points:
        add_p(doc, pt, font_size=10.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2, line_spacing=1.15)
        
    add_p(doc, "PROGRAM EDUCATIONAL OBJECTIVES (PEOs), POs & PSOs", font_size=11.5, bold=True, space_before=4, space_after=3)
    peo_text = (
        "• PEO1 (Technical Expertise & Leadership): Demonstrate strong technical competencies and professional ethics in Information Technology.\n"
        "• PEO2 (Industry-Ready Innovation): Apply advanced computing paradigms to address real-world challenges and regulatory compliance.\n"
        "• PEO3 (Lifelong Learning & Research): Engage in continuous skill acquisition, research contributions, and societal development.\n"
        "• POs (PO1 to PO11): Engineering Knowledge, Problem Analysis, Design/Development, Complex Investigations, Modern Tool Usage, Engineer & Society, Ethics, Teamwork, Communication, Project Management, and Lifelong Learning.\n"
        "• PSOs: (PSO1) Algorithmic modeling and software architectures; (PSO2) Open-source system integration and automated microservices."
    )
    add_p(doc, peo_text, font_size=9.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0, line_spacing=1.15)
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 3: CERTIFICATE
    # -------------------------------------------------------------
    add_p(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR", font_size=14, bold=True, space_before=6, space_after=3)
    add_p(doc, "Department of Information Technology", font_size=13, bold=True, space_after=14)
    add_p(doc, "CERTIFICATE", font_size=16, bold=True, underline=True, space_after=18)
    
    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert.paragraph_format.line_spacing = 1.35
    p_cert.paragraph_format.space_after = Pt(10)
    p_cert.add_run("This is to certify that project report entitled ")
    r_pt = p_cert.add_run("“SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM”")
    r_pt.bold = True
    p_cert.add_run(" is a bonafide work done by the students ")
    r_pn = p_cert.add_run("Nishant Datta and Nazish Khan.")
    r_pn.bold = True
    for r in p_cert.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11.5)
        
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_sub.paragraph_format.line_spacing = 1.35
    p_sub.paragraph_format.space_after = Pt(24)
    p_sub.add_run("The project report is submitted to ")
    r_clg = p_sub.add_run("PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR,")
    r_clg.bold = True
    p_sub.add_run(" an Autonomous Institute Affiliated to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur in partial fulfillment of the requirements for the degree of ")
    r_deg = p_sub.add_run("Bachelor of Technology (Honors) in Information Technology")
    r_deg.bold = True
    p_sub.add_run(" for the Session 2026-2027.")
    for r in p_sub.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11.5)
        
    add_p(doc, "GUIDED BY", font_size=12, bold=True, space_after=12)
    tbl_guides = add_borderless_table(doc, 1, 2, [3.2, 3.2])
    
    # Left: Co-Guide
    c_cg = tbl_guides.cell(0, 0)
    set_cell(c_cg, "Ms. Lalita Charpe", font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_cg = c_cg.add_paragraph()
    p_cg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cg.paragraph_format.line_spacing = 1.15
    r_cg = p_cg.add_run("Co-Guide\nAssistant Professor\nDepartment of Information Technology")
    r_cg.font.name = "Times New Roman"
    r_cg.font.size = Pt(10.5)
    
    # Right: Guide
    c_g = tbl_guides.cell(0, 1)
    set_cell(c_g, "Dr. Archana Potnurwar", font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_g = c_g.add_paragraph()
    p_g.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_g.paragraph_format.line_spacing = 1.15
    r_g = p_g.add_run("Guide\nAssociate Professor\nDepartment of Information Technology")
    r_g.font.name = "Times New Roman"
    r_g.font.size = Pt(10.5)
    
    add_p(doc, "", space_after=32)
    
    # Signatories at bottom
    tbl_sig = add_borderless_table(doc, 1, 2, [3.2, 3.2])
    c_hod = tbl_sig.cell(0, 0)
    set_cell(c_hod, "Dr. P. S. Prasad", font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_hod = c_hod.add_paragraph()
    p_hod.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hod.paragraph_format.line_spacing = 1.15
    r_hod = p_hod.add_run("Head of Department\nDepartment of Information Technology")
    r_hod.font.name = "Times New Roman"
    r_hod.font.size = Pt(10.5)
    
    c_pce = tbl_sig.cell(0, 1)
    set_cell(c_pce, "Dr. S. A. Dhale", font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_pce = c_pce.add_paragraph()
    p_pce.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pce.paragraph_format.line_spacing = 1.15
    r_pce = p_pce.add_run("Principal\nPriyadarshini College of Engineering")
    r_pce.font.name = "Times New Roman"
    r_pce.font.size = Pt(10.5)
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 4: DECLARATION
    # -------------------------------------------------------------
    add_p(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR-440019 (INDIA)", font_size=13, bold=True, space_before=6, space_after=3)
    add_p(doc, "Department of Information Technology", font_size=12, bold=True, space_after=16)
    add_p(doc, "DECLARATION", font_size=16, bold=True, underline=True, space_after=22)
    
    p_decl = doc.add_paragraph()
    p_decl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_decl.paragraph_format.line_spacing = 1.4
    p_decl.paragraph_format.space_after = Pt(44)
    p_decl.add_run("We, the undersigned, declare that the project entitled ")
    r_dt = p_decl.add_run("“SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM”,")
    r_dt.bold = True
    p_decl.add_run(" being submitted in partial fulfillment of the requirements for the degree of ")
    r_ddeg = p_decl.add_run("Bachelor of Technology (Honors) in Information Technology")
    r_ddeg.bold = True
    p_decl.add_run(", Priyadarshini College of Engineering Nagpur, an Autonomous Institute Affiliated to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur is the work carried out by us.")
    for r in p_decl.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
        
    tbl_decl_sig = add_borderless_table(doc, 1, 2, [3.2, 3.2])
    c_pd = tbl_decl_sig.cell(0, 0)
    set_cell(c_pd, "Place: Nagpur\nDate: 30th October 2026", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.3)
    
    c_ps = tbl_decl_sig.cell(0, 1)
    set_cell(c_ps, "PROJECTEES:\n1. Nishant Datta\n2. Nazish Khan", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.3)
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 5: ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    add_p(doc, "ACKNOWLEDGEMENT", font_size=15, bold=True, space_before=6, space_after=10)
    p_ack1 = (
        "It is our pleasure to acknowledge our sincere thanks with a deep sense of gratitude towards our "
        "project guide Dr. Archana Potnurwar, Associate Professor, and co-guide Ms. Lalita Charpe, Assistant "
        "Professor, Department of Information Technology, for their continuous knowledge, insightful guidance, "
        "and untiring support in conducting this dissertation work. They have wholeheartedly helped us in "
        "this endeavor across every stage of research and implementation."
    )
    add_p(doc, p_ack1, font_size=11, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    
    p_ack2 = (
        "We would like to express our sincere gratitude to Dr. S. A. Dhale, Principal, Priyadarshini College "
        "of Engineering, Nagpur, for his unwavering support and for providing state-of-the-art infrastructural "
        "and computing facilities at the institute."
    )
    add_p(doc, p_ack2, font_size=11, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    
    p_ack3 = (
        "Our heartfelt thanks also go to Dr. G. M. Asutkar, Vice Principal, Priyadarshini College of "
        "Engineering, Nagpur, for his constant encouragement and for making vital institutional resources "
        "available for our project."
    )
    add_p(doc, p_ack3, font_size=11, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    
    p_ack4 = (
        "We are deeply grateful to Dr. P. S. Prasad, Head of the Department of Information Technology, "
        "Priyadarshini College of Engineering, Nagpur, for his invaluable guidance, inspiring vision, and "
        "for offering necessary department-level support throughout this project.\n"
        "We also take this opportunity to thank all faculty members, laboratory staff, and peers who have "
        "directly or indirectly extended their help, advice, and encouragement in executing this project."
    )
    add_p(doc, p_ack4, font_size=11, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=14, line_spacing=1.2)
    
    p_ack_sig = doc.add_paragraph()
    p_ack_sig.paragraph_format.line_spacing = 1.25
    p_ack_sig.paragraph_format.space_before = Pt(8)
    p_ack_sig.paragraph_format.space_after = Pt(0)
    r_as = p_ack_sig.add_run("PROJECTEES:\n1. Nishant Datta\n2. Nazish Khan")
    r_as.font.name = "Times New Roman"
    r_as.font.size = Pt(11.5)
    r_as.font.bold = True
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 6: ABSTRACT
    # -------------------------------------------------------------
    add_p(doc, "ABSTRACT", font_size=15, bold=True, space_before=6, space_after=10)
    abstract_text1 = (
        "Accreditation and statutory regulatory approvals in higher technical education institutions have "
        "historically operated as labor-intensive, opaque, and highly error-prone manual endeavors. In the "
        "Indian engineering education ecosystem, institutions must rigorously satisfy multi-tiered, highly "
        "complex regulatory frameworks mandated by the All India Council for Technical Education (AICTE "
        "Approval Process Handbook), the National Board of Accreditation (NBA Outcome-Based Education "
        "and Self-Assessment Reports), and the National Assessment and Accreditation Council (NAAC "
        "Institutional Self-Study Reports). These regulatory bodies mandate stringent quantitative and "
        "qualitative thresholds spanning Student-Faculty Ratios (SFR 1:15 or 1:20), Faculty Cadre Ratios "
        "(1:2:6 for Professor, Associate Professor, and Assistant Professor), outcome-based attainment "
        "matrices (Course Outcomes, Program Outcomes, Program Specific Outcomes), research productivity, "
        "laboratory infrastructure adequacy, barrier-free accessibility, and statutory governance compliances."
    )
    add_p(doc, abstract_text1, font_size=11, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    
    abstract_text2 = (
        "To resolve these existential institutional challenges, this dissertation presents Smart Approval AI: an "
        "end-to-end, multi-modal artificial intelligence compliance verification, predictive auditing, and "
        "institutional performance analytics platform. The proposed system architecturally integrates state-of-"
        "the-art vision-language document processing (IBM Docling with granite-vision OCR and table layout "
        "extraction), large language model reasoning (Google Gemini 2.5 Flash), and deterministic rule-"
        "validation engines. The platform autonomously parses heterogeneous, multi-page institutional "
        "documentation—including institutional faculty rosters, land use registrations, fire safety certificates, "
        "financial balance sheets, and laboratory equipment registers—converting unstructured artifacts into "
        "semantically rich, high-fidelity JSON data structures."
    )
    add_p(doc, abstract_text2, font_size=11, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.2)
    
    abstract_text3 = (
        "A dual-layer verification engine validates extracted institutional metrics against statutory AICTE norms "
        "and computes real-time 1000-point NBA Tier-I Self-Assessment Report (SAR) scorecards across all ten evaluation "
        "criteria. Longitudinal multi-year analytics powered by Seasonal AutoRegressive Integrated Moving Average (SARIMA) "
        "forecast compliance trajectories years before on-site peer inspections. Deployed on an isolated, non-conflicting "
        "multi-tier architecture adhering to strict local microservice reverse-proxy rules (Next.js on Port 3051, FastAPI on "
        "Port 8051, Ngrok Inspector on Port 4051), Smart Approval AI delivers a 96.8% reduction in audit processing turnaround time."
    )
    add_p(doc, abstract_text3, font_size=11, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.2)
    
    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(6)
    p_kw.paragraph_format.space_after = Pt(0)
    r_kw_label = p_kw.add_run("Keywords: ")
    r_kw_label.font.name = "Times New Roman"
    r_kw_label.font.size = Pt(10.5)
    r_kw_label.font.bold = True
    r_kw_val = p_kw.add_run("Higher Education Accreditation, AICTE Statutory Compliance, NBA Tier-I SAR Evaluation, NAAC SSR Analytics, Vision-Language Models, IBM Docling OCR, Automated Audit Verification, Microservice Architecture.")
    r_kw_val.font.name = "Times New Roman"
    r_kw_val.font.size = Pt(10.5)
    r_kw_val.font.italic = True
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 7: INDEX
    # -------------------------------------------------------------
    add_p(doc, "INDEX", font_size=14, bold=True, space_before=4, space_after=6)
    
    index_lines = [
        ("CHAPTER 1: INTRODUCTION", 0, "1"),
        ("1.1 BACKGROUND AND MOTIVATION", 20, "1"),
        ("1.2 PROBLEM STATEMENT", 20, "3"),
        ("1.3 OBJECTIVES OF THE STUDY", 20, "5"),
        ("1.4 SIGNIFICANCE AND INNOVATION", 20, "7"),
        ("1.5 SCOPE AND DELIMITATIONS", 20, "9"),
        ("CHAPTER 2: LITERATURE REVIEW", 0, "11"),
        ("2.1 STATUTORY REGULATORY FRAMEWORKS IN TECHNICAL EDUCATION", 20, "11"),
        ("2.2 LIMITATIONS OF TRADITIONAL MANUAL AUDIT METHODOLOGIES", 20, "14"),
        ("2.3 DOCUMENT AI AND VISION-LANGUAGE MULTI-MODAL REASONING", 20, "17"),
        ("2.4 OUTCOME-BASED EDUCATION (OBE) & ACCREDITATION MODELS", 20, "20"),
        ("2.5 COMPARATIVE TAXONOMY OF EXISTING PLATFORMS", 20, "24"),
        ("CHAPTER 3: METHODOLOGY", 0, "28"),
        ("3.1 SYSTEM ARCHITECTURE & DATA FLOW DESIGN", 20, "28"),
        ("3.2 MULTI-MODAL DOCUMENT PARSING (IBM DOCLING OCR)", 20, "31"),
        ("3.3 AICTE STATUTORY REGULATORY VERIFICATION ENGINE", 20, "34"),
        ("3.4 NBA TIER-I 1000-POINT SAR EVALUATION ENGINE", 20, "38"),
        ("3.5 NAAC MULTI-CRITERIA INSTITUTIONAL ASSESSMENT", 20, "42"),
        ("3.6 LONGITUDINAL AUDIT FORECASTING (SARIMA)", 20, "46"),
        ("CHAPTER 4: SOFTWARE/HARDWARE REQUIREMENTS", 0, "50"),
        ("4.1 HARDWARE ARCHITECTURE & COMPUTE INFRASTRUCTURE", 20, "50"),
        ("4.2 SOFTWARE TECHNOLOGY STACK & MICROSERVICES", 20, "53"),
        ("4.3 RELATIONAL DATABASE SCHEMAS & DDL SPECIFICATIONS", 20, "56"),
        ("4.4 MICROSERVICE REVERSE PROXY & PORT ISOLATION FRAMEWORK", 20, "60"),
        ("CHAPTER 5: RESULTS AND DISCUSSIONS", 0, "64"),
        ("5.1 DOCUMENT INGESTION & TABLE EXTRACTION BENCHMARKS", 20, "64"),
        ("5.2 STATUTORY RULE ENGINE VERIFICATION ACCURACY", 20, "68"),
        ("5.3 NBA TIER-I SAR EVALUATION VALIDATION", 20, "72"),
        ("5.4 PREDICTIVE AUDIT FORECASTING ACCURACY", 20, "76"),
        ("5.5 SYSTEM USABILITY SCALE (SUS) & USER EXPERIENCE", 20, "80"),
        ("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", 0, "84"),
        ("6.1 CONCLUDING REMARKS", 20, "84"),
        ("6.2 FUTURE RESEARCH & DEVELOPMENT DIRECTIONS", 20, "86"),
        ("REFERENCES", 0, "88"),
        ("APPENDIX", 0, "92"),
        ("Appendix A: Code Listings & Core Engine Implementations", 20, "92"),
        ("Appendix B: Complete UI Walkthrough & Architectural Artifacts", 20, "95"),
        ("Appendix C: Ethical Governance & Data Privacy Protocols", 20, "97"),
        ("Appendix D: AICTE Regulatory Deficiency Taxonomy", 20, "99"),
        ("CO-PO and PSO Mapping Matrices", 0, "100"),
        ("Photo with Details & Guided Verification", 0, "101"),
        ("Plagiarism Analysis Report", 0, "102"),
    ]
    
    for line_text, indent, pg in index_lines:
        p_idx = doc.add_paragraph()
        p_idx.paragraph_format.line_spacing = 1.15
        p_idx.paragraph_format.left_indent = Pt(indent)
        p_idx.paragraph_format.space_before = Pt(0.5)
        p_idx.paragraph_format.space_after = Pt(1.5)
        p_idx.paragraph_format.tab_stops.add_tab_stop(Inches(6.4), WD_TAB_ALIGNMENT.RIGHT)
        
        r = p_idx.add_run(line_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        if indent == 0:
            r.bold = True
            
        r_tab = p_idx.add_run(f"\t{pg}")
        r_tab.font.name = "Times New Roman"
        r_tab.font.size = Pt(10)
        if indent == 0:
            r_tab.bold = True
            
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 8: TABLE OF CONTENTS
    # -------------------------------------------------------------
    add_p(doc, "TABLE OF CONTENTS", font_size=14, bold=True, space_before=8, space_after=12)
    
    toc_entries = [
        ("Sr. No.", "Content Title", "Page No."),
        ("i.", "Index", "vii"),
        ("ii.", "List of Figures", "x"),
        ("iii.", "List of Abbreviations", "xi"),
        ("iv.", "List of Tables", "xii"),
        ("1.", "Chapter 1: Introduction", "1"),
        ("2.", "Chapter 2: Literature Review", "11"),
        ("3.", "Chapter 3: Methodology", "28"),
        ("4.", "Chapter 4: Software / Hardware Required", "50"),
        ("5.", "Chapter 5: Results and Discussions", "64"),
        ("6.", "Chapter 6: Conclusion and Future Scope", "84"),
        ("7.", "References", "88"),
        ("8.", "Appendices (A through D & Official Reports)", "92"),
    ]
    
    tbl_toc = doc.add_table(rows=len(toc_entries), cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w = [1.0, 4.2, 1.2]
    
    for r_idx, (sr, title, pg) in enumerate(toc_entries):
        for c_idx, val in enumerate([sr, title, pg]):
            cell = tbl_toc.cell(r_idx, c_idx)
            cell.width = Inches(col_w[c_idx])
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_idx == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.bold = True
                
    doc.add_page_break()

def build_complete_honors_thesis():
    print("=" * 60)
    print("ASSEMBLING COMPLETE DISSERTATION IN STRICT HONORS FORMAT...")
    print("=" * 60)
    
    doc = docx.Document()
    
    # Configure base style
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)
    
    sect = doc.sections[0]
    sect.top_margin = Inches(0.8)
    sect.bottom_margin = Inches(0.8)
    sect.left_margin = Inches(1.0)
    sect.right_margin = Inches(0.8)
    apply_page_border(sect)
    
    # Header is completely empty
    h = sect.header
    for p in h.paragraphs:
        p.text = ""
        
    # Build 8 exact preliminary pages
    build_honors_preliminary_pages(doc)
    
    # Append All 6 Technical Chapters + Additions
    print("Appending Chapter 1: Introduction...")
    build_chapter_1(doc)
    doc.add_page_break()
    
    print("Appending Chapter 2: Literature Review...")
    build_chapter_2(doc)
    add_chapter_2_deep_dive(doc)
    add_chapter_2_protocols(doc)
    doc.add_page_break()
    
    print("Appending Chapter 3: Methodology...")
    build_chapter_3(doc)
    add_chapter_3_rubrics_deep_dive(doc)
    add_chapter_3_naac_and_trace(doc)
    add_chapter_3_nba_code(doc)
    add_chapter_3_nba_mathematical_formulations(doc)
    doc.add_page_break()
    
    print("Appending Chapter 4: Hardware & Software Requirements...")
    build_chapter_4(doc)
    add_chapter_4_ddl_schemas(doc)
    add_chapter_4_middleware_and_proxy(doc)
    add_chapter_4_docker(doc)
    add_chapter_4_api_specifications(doc)
    doc.add_page_break()
    
    print("Appending Chapter 5: Results & Discussions...")
    build_chapter_5(doc)
    add_chapter_5_ablation_studies(doc)
    add_chapter_5_case_studies_and_roi(doc)
    add_chapter_5_security_and_pen_testing(doc)
    add_chapter_5_sus(doc)
    add_chapter_5_empirical_performance_benchmarks(doc)
    doc.add_page_break()
    
    print("Appending Chapter 6: Conclusion & Future Scope...")
    build_chapter_6(doc)
    add_chapter_6_concluding_remarks(doc)
    doc.add_page_break()
    
    print("Appending References & Appendices...")
    build_end_matter(doc)
    add_appendix_code_listings(doc)
    add_appendix_comprehensive_ui_walkthrough(doc)
    add_appendix_ethical_and_privacy_protocols(doc)
    add_appendix_aicte_deficiency_taxonomy(doc)
    
    # Ensure all sections have border
    for s in doc.sections:
        apply_page_border(s)
        
    print(f"Applying academic table styling across technical data tables...")
    for tbl in doc.tables:
        format_academic_table(tbl)
        
    doc.save(OUTPUT_DOCX)
    print(f"Saved DOCX to: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_complete_honors_thesis()
