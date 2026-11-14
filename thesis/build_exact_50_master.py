"""
Master 50-Page Honors Thesis Compiler for Smart Approval AI
Priyadarshini College of Engineering, Nagpur
Department of Information Technology

Authors: Nishant Datta & Nazish Khan
Guide: Dr. Archana Potnurwar | Co-Guide: Ms. Lalita Charpe
HOD: Dr. P. S. Prasad | Principal: Dr. S. A. Dhale
Session: 2026-2027

Exact Target: 50 Physical Pages
- 10 Preliminary Pages (i to x)
- 40 Body Pages (1 to 40)
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from academic_style_helpers import format_academic_table

OUTPUT_DOCX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Smart_Approval_AI_Final_Thesis.docx")
OUTPUT_PDF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Smart_Approval_AI_Final_Thesis.pdf")
LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extracted_assets", "image_2.jpeg")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "extracted_assets")
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

def apply_page_border(section):
    sectPr = section._sectPr
    for existing in sectPr.findall(qn('w:pgBorders')):
        sectPr.remove(existing)
    borders_xml = parse_xml(
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
        f'<w:top w:val="single" w:sz="4" w:space="24" w:color="333333"/>'
        f'<w:left w:val="single" w:sz="4" w:space="24" w:color="333333"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="24" w:color="333333"/>'
        f'<w:right w:val="single" w:sz="4" w:space="24" w:color="333333"/>'
        f'</w:pgBorders>'
    )
    sectPr.append(borders_xml)

def add_p(doc, text="", font_size=12, bold=False, italic=False, underline=False,
          alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=3.0, line_spacing=1.18):
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(font_size)
        run.bold = bold
        run.italic = italic
        run.underline = underline
    return p

def add_h1(doc, text):
    import re
    cleaned = text.strip()
    m = re.match(r'^(CHAPTER\s+[\dA-Za-z]+|APPENDIX\s+[\dA-Za-z]+)[\s:\-]+(.*)$', cleaned, re.IGNORECASE)
    if m:
        part1 = m.group(1).upper()
        part2 = m.group(2).strip()
        part2 = re.sub(r'\(OPTIONAL.*?\)', '', part2, flags=re.IGNORECASE).strip()
        p1 = add_p(doc, part1, font_size=15, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=2)
        p1.paragraph_format.keep_with_next = True
        p2 = add_p(doc, part2.upper(), font_size=15, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=10)
        p2.paragraph_format.keep_with_next = True
        return p2
    else:
        p = add_p(doc, cleaned.upper(), font_size=15, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=8, space_after=10)
        p.paragraph_format.keep_with_next = True
        return p

def add_h2(doc, text):
    p = add_p(doc, text, font_size=13, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_before=8, space_after=3)
    p.paragraph_format.keep_with_next = True
    return p

def add_h3(doc, text):
    p = add_p(doc, text, font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=2)
    p.paragraph_format.keep_with_next = True
    return p

def add_borderless_table(doc, rows, cols, widths):
    tbl = doc.add_table(rows=rows, cols=cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = tbl._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/>'
        f'<w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)
    for r in tbl.rows:
        for idx, w in enumerate(widths):
            r.cells[idx].width = Inches(w)
    return tbl

def set_cell(cell, text, font_size=11, bold=False, italic=False, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=1, line_spacing=1.15):
    p = cell.paragraphs[0]
    p.alignment = alignment
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(font_size)
    run.bold = bold
    run.italic = italic
    return run

# Set up hooks in thesis_prelim so all chapter functions use compact formatting
import thesis_prelim
thesis_prelim.add_paragraph = add_p
thesis_prelim.add_heading_1 = add_h1
thesis_prelim.add_heading_2 = add_h2
thesis_prelim.add_heading_3 = add_h3

from thesis_ch1 import build_chapter_1
from thesis_ch2 import build_chapter_2
from thesis_ch3 import build_chapter_3
from thesis_ch4 import build_chapter_4
from thesis_ch5 import build_chapter_5
from thesis_ch6 import build_chapter_6
from thesis_endmatter import build_end_matter

def build_preliminary_pages(doc):
    """Generates the exact 10 preliminary pages matching university guidelines."""
    # -------------------------------------------------------------
    # PAGE 1: COVER PAGE
    # -------------------------------------------------------------
    add_p(doc, '"SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM"',
          font_size=15, bold=True, space_before=4, space_after=6, line_spacing=1.2)
    
    add_p(doc, "A Project Report Submitted in the partial fulfillment of requirement of the Degree of",
          font_size=11, italic=False, space_after=3, line_spacing=1.15)
    
    add_p(doc, "Bachelor of Technology (Honors)", font_size=13, bold=True, space_after=2)
    add_p(doc, "in", font_size=11, space_after=2)
    add_p(doc, "Information Technology", font_size=13, bold=True, space_after=2)
    add_p(doc, "Department of Information Technology", font_size=13, bold=True, space_after=2)
    add_p(doc, "to", font_size=11, space_after=2)
    add_p(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING", font_size=13.5, bold=True, space_after=2)
    add_p(doc, "An Autonomous Institute Affiliated to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur",
          font_size=10, italic=True, space_after=6)
    
    add_p(doc, "Under the guidance of", font_size=11, space_after=2)
    add_p(doc, "Guide", font_size=12, bold=True, space_after=1)
    
    tbl_guides_cover = add_borderless_table(doc, 1, 2, [3.2, 3.2])
    c_g1 = tbl_guides_cover.cell(0, 0)
    set_cell(c_g1, "Dr. Archana Potnurwar", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_g1_sub = c_g1.add_paragraph()
    p_g1_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_g1_sub = p_g1_sub.add_run("Associate Professor (Guide)\nDepartment of Information Technology")
    r_g1_sub.font.name = "Times New Roman"
    r_g1_sub.font.size = Pt(9.5)
    
    c_g2 = tbl_guides_cover.cell(0, 1)
    set_cell(c_g2, "Ms. Lalita Charpe", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_g2_sub = c_g2.add_paragraph()
    p_g2_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_g2_sub = p_g2_sub.add_run("Assistant Professor (Co-Guide)\nDepartment of Information Technology")
    r_g2_sub.font.name = "Times New Roman"
    r_g2_sub.font.size = Pt(9.5)
    
    add_p(doc, "Submitted by", font_size=11, italic=True, space_before=4, space_after=2)
    tbl_students_cover = add_borderless_table(doc, 1, 2, [3.2, 3.2])
    c_s1 = tbl_students_cover.cell(0, 0)
    set_cell(c_s1, "Nishant Datta", font_size=12, bold=True, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    c_s2 = tbl_students_cover.cell(0, 1)
    set_cell(c_s2, "Nazish Khan", font_size=12, bold=True, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    
    if os.path.exists(LOGO_PATH):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(3)
        p_img.paragraph_format.space_after = Pt(3)
        p_img.add_run().add_picture(LOGO_PATH, width=Inches(1.1))
        
    add_p(doc, "DEPARTMENT OF INFORMATION TECHNOLOGY", font_size=12, bold=True, space_after=2)
    add_p(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR-440019", font_size=12, bold=True, space_after=2)
    add_p(doc, "2026-2027", font_size=12, bold=True, space_after=0)
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 2: VISION & MISSION
    # -------------------------------------------------------------
    add_p(doc, "VISION OF THE INSTITUTE", font_size=11.5, bold=True, space_before=2, space_after=2)
    p_v = (
        "To become one of India's leading engineering institutes in both education and research. We "
        "are committed to provide quality and state-of-the-art technical education to our students, so that "
        "they become technologically superior and in turn contribute to creating a great society."
    )
    add_p(doc, p_v, font_size=10, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, line_spacing=1.15)
    
    add_p(doc, "MISSION OF THE INSTITUTE", font_size=11.5, bold=True, space_after=2)
    m_points = [
        "i.   Fostering a dynamic learning environment that equips students with technical expertise, problem-solving skills, and a deep commitment to ethical practices.",
        "ii.  To cultivate a culture of innovation, incubation, research, and entrepreneurship that drives technological advancements.",
        "iii. To uphold the spirit of mutual excellence while interacting with stakeholders of our institutional ecosystem.",
        "iv.  Promoting lifelong learning, professional growth, and ensuring the holistic development of students and the well-being of society."
    ]
    for pt in m_points:
        add_p(doc, pt, font_size=10, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2, line_spacing=1.15)
        
    add_p(doc, "VISION OF THE DEPARTMENT", font_size=11.5, bold=True, space_before=3, space_after=2)
    dept_v = (
        "To nurture students with the latest technology and research, helping them to become valuable "
        "contributors who can address the changing needs of the IT industry and society."
    )
    add_p(doc, dept_v, font_size=10, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4, line_spacing=1.15)
    
    add_p(doc, "MISSION OF THE DEPARTMENT", font_size=11.5, bold=True, space_after=2)
    dept_m_points = [
        "i.   To create a holistic learning environment that empowers emerging graduates with advanced technical and value-based education.",
        "ii.  To attain professional excellence in the field of Information Technology and allied multidisciplinary areas.",
        "iii. To encourage transformative learning for research addressing the changing needs of society and fostering lifelong learning."
    ]
    for pt in dept_m_points:
        add_p(doc, pt, font_size=10, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=2, line_spacing=1.15)
        
    add_p(doc, "PROGRAM EDUCATIONAL OBJECTIVES (PEOs), POs & PSOs", font_size=11, bold=True, space_before=3, space_after=2)
    peo_text = (
        "-  PEO1 (Technical Expertise): Demonstrate strong technical competencies and professional ethics in Information Technology.\n"
        "-  PEO2 (Innovation): Apply advanced computing paradigms to address real-world challenges and regulatory compliance.\n"
        "-  PEO3 (Lifelong Learning): Engage in continuous skill acquisition, research contributions, and societal development.\n"
        "-  POs (PO1 to PO11): Engineering Knowledge, Problem Analysis, Design, Modern Tool Usage, Society, Ethics, Teamwork, Communication, Project Management, and Lifelong Learning.\n"
        "-  PSOs: (PSO1) Algorithmic modeling and software architectures; (PSO2) Open-source system integration and automated microservices."
    )
    add_p(doc, peo_text, font_size=9, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0, line_spacing=1.15)
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 3: CERTIFICATE
    # -------------------------------------------------------------
    add_p(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR", font_size=13.5, bold=True, space_before=4, space_after=2)
    add_p(doc, "Department of Information Technology", font_size=12, bold=True, space_after=12)
    add_p(doc, "CERTIFICATE", font_size=15, bold=True, underline=True, space_after=14)
    
    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert.paragraph_format.line_spacing = 1.3
    p_cert.paragraph_format.space_after = Pt(8)
    p_cert.add_run("This is to certify that project report entitled ")
    r_pt = p_cert.add_run('"SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM"')
    r_pt.bold = True
    p_cert.add_run(" is a bonafide work done by the students ")
    r_pn = p_cert.add_run("Nishant Datta and Nazish Khan.")
    r_pn.bold = True
    for r in p_cert.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_sub.paragraph_format.line_spacing = 1.3
    p_sub.paragraph_format.space_after = Pt(20)
    p_sub.add_run("The project report is submitted to ")
    r_clg = p_sub.add_run("PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR,")
    r_clg.bold = True
    p_sub.add_run(" an Autonomous Institute Affiliated to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur in partial fulfillment of the requirements for the degree of ")
    r_deg = p_sub.add_run("Bachelor of Technology (Honors) in Information Technology")
    r_deg.bold = True
    p_sub.add_run(" for the Session 2026-2027.")
    for r in p_sub.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    add_p(doc, "GUIDED BY", font_size=11.5, bold=True, space_after=10)
    tbl_guides = add_borderless_table(doc, 1, 2, [3.2, 3.2])
    
    # Left: Guide
    c_g = tbl_guides.cell(0, 0)
    set_cell(c_g, "Dr. Archana Potnurwar", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_g = c_g.add_paragraph()
    p_g.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_g.paragraph_format.line_spacing = 1.15
    r_g = p_g.add_run("Guide\nAssociate Professor\nDepartment of Information Technology")
    r_g.font.name = "Times New Roman"
    r_g.font.size = Pt(10)
    
    # Right: Co-Guide
    c_cg = tbl_guides.cell(0, 1)
    set_cell(c_cg, "Ms. Lalita Charpe", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_cg = c_cg.add_paragraph()
    p_cg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cg.paragraph_format.line_spacing = 1.15
    r_cg = p_cg.add_run("Co-Guide\nAssistant Professor\nDepartment of Information Technology")
    r_cg.font.name = "Times New Roman"
    r_cg.font.size = Pt(10)
    
    add_p(doc, "", space_after=28)
    
    # Signatories at bottom
    tbl_sig = add_borderless_table(doc, 1, 2, [3.2, 3.2])
    c_hod = tbl_sig.cell(0, 0)
    set_cell(c_hod, "Dr. P. S. Prasad", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_hod = c_hod.add_paragraph()
    p_hod.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_hod.paragraph_format.line_spacing = 1.15
    r_hod = p_hod.add_run("Head of Department\nDepartment of Information Technology")
    r_hod.font.name = "Times New Roman"
    r_hod.font.size = Pt(10)
    
    c_pce = tbl_sig.cell(0, 1)
    set_cell(c_pce, "Dr. S. A. Dhale", font_size=11.5, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    p_pce = c_pce.add_paragraph()
    p_pce.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pce.paragraph_format.line_spacing = 1.15
    r_pce = p_pce.add_run("Principal\nPriyadarshini College of Engineering")
    r_pce.font.name = "Times New Roman"
    r_pce.font.size = Pt(10)
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 4: DECLARATION
    # -------------------------------------------------------------
    add_p(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR-440019 (INDIA)", font_size=12.5, bold=True, space_before=4, space_after=2)
    add_p(doc, "Department of Information Technology", font_size=11.5, bold=True, space_after=14)
    add_p(doc, "DECLARATION", font_size=15, bold=True, underline=True, space_after=18)
    
    p_decl = doc.add_paragraph()
    p_decl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_decl.paragraph_format.line_spacing = 1.35
    p_decl.paragraph_format.space_after = Pt(36)
    p_decl.add_run("We, the undersigned, declare that the project entitled ")
    r_dt = p_decl.add_run('"SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM",')
    r_dt.bold = True
    p_decl.add_run(" being submitted in partial fulfillment of the requirements for the degree of ")
    r_ddeg = p_decl.add_run("Bachelor of Technology (Honors) in Information Technology")
    r_ddeg.bold = True
    p_decl.add_run(", Priyadarshini College of Engineering Nagpur, an Autonomous Institute Affiliated to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur is the work carried out by us.")
    for r in p_decl.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11.5)
        
    tbl_decl_sig = add_borderless_table(doc, 1, 2, [3.2, 3.2])
    c_pd = tbl_decl_sig.cell(0, 0)
    set_cell(c_pd, "Place: Nagpur\nDate: 30th October 2026", font_size=11, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.3)
    
    c_ps = tbl_decl_sig.cell(0, 1)
    set_cell(c_ps, "PROJECTEES:\n1. Nishant Datta\n2. Nazish Khan", font_size=11, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.3)
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 5: ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    add_p(doc, "ACKNOWLEDGEMENT", font_size=14, bold=True, space_before=4, space_after=8)
    p_ack1 = (
        "It is our pleasure to acknowledge our sincere thanks with a deep sense of gratitude towards our "
        "project guide Dr. Archana Potnurwar, Associate Professor, and co-guide Ms. Lalita Charpe, Assistant "
        "Professor, Department of Information Technology, for their continuous knowledge, insightful guidance, "
        "and untiring support in conducting this dissertation work. They have wholeheartedly helped us in "
        "this endeavor across every stage of research and implementation."
    )
    add_p(doc, p_ack1, font_size=10.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.15)
    
    p_ack2 = (
        "We would like to express our sincere gratitude to Dr. S. A. Dhale, Principal, Priyadarshini College "
        "of Engineering, Nagpur, for his unwavering support and for providing state-of-the-art infrastructural "
        "and computing facilities at the institute."
    )
    add_p(doc, p_ack2, font_size=10.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.15)
    
    p_ack3 = (
        "We also extend our special gratitude towards Dr. G. M. Asutkar, Vice-Principal, for his constant "
        "encouragement, keen interest, and academic advice throughout our undergraduate journey."
    )
    add_p(doc, p_ack3, font_size=10.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.15)
    
    p_ack4 = (
        "We express our sincere thanks to Dr. P. S. Prasad, Head of the Department of Information Technology, "
        "Priyadarshini College of Engineering, Nagpur, for his invaluable guidance, inspiring vision, and "
        "for offering necessary department-level support throughout this project.\n"
        "We also take this opportunity to thank all faculty members, laboratory staff, and peers who have "
        "directly or indirectly extended their help, advice, and encouragement in executing this project."
    )
    add_p(doc, p_ack4, font_size=10.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10, line_spacing=1.15)
    
    p_ack_sig = doc.add_paragraph()
    p_ack_sig.paragraph_format.line_spacing = 1.2
    p_ack_sig.paragraph_format.space_before = Pt(6)
    p_ack_sig.paragraph_format.space_after = Pt(0)
    r_as = p_ack_sig.add_run("PROJECTEES:\n1. Nishant Datta\n2. Nazish Khan")
    r_as.font.name = "Times New Roman"
    r_as.font.size = Pt(11)
    r_as.font.bold = True
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 6: ABSTRACT
    # -------------------------------------------------------------
    add_p(doc, "ABSTRACT", font_size=14, bold=True, space_before=4, space_after=8)
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
    add_p(doc, abstract_text1, font_size=10.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.15)
    
    abstract_text2 = (
        "To resolve these existential institutional challenges, this dissertation presents Smart Approval AI: an "
        "end-to-end, multi-modal artificial intelligence compliance verification, predictive auditing, and "
        "institutional performance analytics platform. The proposed system architecturally integrates state-of-"
        "the-art vision-language document processing (IBM Docling with granite-vision OCR and table layout "
        "extraction), large language model reasoning (Google Gemini 2.5 Flash), and deterministic rule-"
        "validation engines. The platform autonomously parses heterogeneous, multi-page institutional "
        "documentation - including institutional faculty rosters, land use registrations, fire safety certificates, "
        "financial balance sheets, and laboratory equipment registers - converting unstructured artifacts into "
        "semantically rich, high-fidelity JSON data structures."
    )
    add_p(doc, abstract_text2, font_size=10.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6, line_spacing=1.15)
    
    abstract_text3 = (
        "A dual-layer verification engine validates extracted institutional metrics against statutory AICTE norms "
        "and computes real-time 1000-point NBA Tier-I Self-Assessment Report (SAR) scorecards across all ten evaluation "
        "criteria. Longitudinal multi-year analytics powered by Seasonal AutoRegressive Integrated Moving Average (SARIMA) "
        "forecast compliance trajectories years before on-site peer inspections. Deployed on an isolated, non-conflicting "
        "multi-tier architecture adhering to strict local microservice reverse-proxy rules (Next.js on Port 3051, FastAPI on "
        "Port 8051, Ngrok Inspector on Port 4051), Smart Approval AI delivers a 96.8% reduction in audit processing turnaround time."
    )
    add_p(doc, abstract_text3, font_size=10.5, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8, line_spacing=1.15)
    
    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(4)
    p_kw.paragraph_format.space_after = Pt(0)
    r_kw_label = p_kw.add_run("Keywords: ")
    r_kw_label.font.name = "Times New Roman"
    r_kw_label.font.size = Pt(10)
    r_kw_label.font.bold = True
    r_kw_val = p_kw.add_run("Higher Education Accreditation, AICTE Statutory Compliance, NBA Tier-I SAR Evaluation, NAAC SSR Analytics, Vision-Language Models, IBM Docling OCR, Automated Audit Verification, Microservice Architecture.")
    r_kw_val.font.name = "Times New Roman"
    r_kw_val.font.size = Pt(10)
    r_kw_val.font.italic = True
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 7: TABLE OF CONTENTS
    # -------------------------------------------------------------
    add_p(doc, "TABLE OF CONTENTS", font_size=14, bold=True, space_before=6, space_after=12)
    
    toc_entries = [
        ("Sr. No.", "Content Title", "Page No."),
        ("i.", "Index (Detailed Chapters and Sections)", "viii"),
        ("ii.", "List of Figures & List of Tables", "ix"),
        ("iii.", "List of Abbreviations", "x"),
        ("1.", "Chapter 1: Introduction", "1"),
        ("2.", "Chapter 2: Literature Review", "4"),
        ("3.", "Chapter 3: Methodology", "7"),
        ("4.", "Chapter 4: Software / Hardware Required", "17"),
        ("5.", "Chapter 5: Results and Discussions", "22"),
        ("6.", "Chapter 6: Conclusion and Future Scope", "29"),
        ("7.", "References", "32"),
        ("8.", "Appendices (A through F & Official Exhibits)", "34"),
    ]
    
    tbl_toc = doc.add_table(rows=len(toc_entries), cols=3)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_toc = [1.0, 4.2, 1.2]
    
    for r_idx, (sr, title, pg) in enumerate(toc_entries):
        for c_idx, val in enumerate([sr, title, pg]):
            cell = tbl_toc.cell(r_idx, c_idx)
            cell.width = Inches(col_w_toc[c_idx])
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.25
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_idx == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10.5)
            if r_idx == 0:
                run.bold = True
                
    format_academic_table(tbl_toc, col_widths=col_w_toc)
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 8: INDEX (EXACT MATCH TO USER PROMPT IMAGE)
    # -------------------------------------------------------------
    add_p(doc, "INDEX", font_size=14, bold=True, space_before=2, space_after=6)
    
    index_lines = [
        ("CHAPTER 1: INTRODUCTION", 0, "1"),
        ("1.1 BACKGROUND", 16, "1"),
        ("1.2 PROBLEM STATEMENT", 16, "1"),
        ("1.3 OBJECTIVE", 16, "2"),
        ("1.4 SIGNIFICANCE", 16, "2"),
        ("1.5 SCOPE", 16, "3"),
        ("CHAPTER 2: LITERATURE REVIEW", 0, "4"),
        ("CHAPTER 3: METHODOLOGY", 0, "7"),
        ("3.1 SYSTEM ARCHITECTURE & DATA FLOW DESIGN", 16, "7"),
        ("3.2 MULTI-MODAL DOCUMENT PARSING (IBM DOCLING OCR)", 16, "9"),
        ("3.3 AICTE STATUTORY REGULATORY VERIFICATION ENGINE", 16, "11"),
        ("3.4 NBA TIER-I 1000-POINT SAR EVALUATION ENGINE", 16, "13"),
        ("CHAPTER 4: SOFTWARE/HARDWARE REQUIRED(OPTIONAL CHAPTER)", 0, "17"),
        ("4.1 HARDWARE ARCHITECTURE & COMPUTE INFRASTRUCTURE", 16, "17"),
        ("4.2 SOFTWARE TECHNOLOGY STACK & MICROSERVICES", 16, "17"),
        ("CHAPTER 5: RESULTS AND DISCUSSIONS", 0, "22"),
        ("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", 0, "29"),
        ("REFERENCES", 0, "32"),
        ("APPENDIX", 0, "34"),
        ("CERTIFICATES OF PATENT/COPYRIGHT/PAPER PUBLICATION/PAPER PRESENTED", 16, "34"),
        ("CO-PO and PSO MAPPING", 16, "35"),
        ("PHOTO WITH DETAILS", 16, "36"),
        ("PHOTO WITH GUIDE", 16, "37"),
        ("PLAGIARISM REPORT", 16, "38"),
        ("POSTER", 16, "39"),
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
        r.font.size = Pt(9.5)
        if indent == 0:
            r.bold = True
            
        r_tab = p_idx.add_run(f"\t{pg}")
        r_tab.font.name = "Times New Roman"
        r_tab.font.size = Pt(9.5)
        if indent == 0:
            r_tab.bold = True
            
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 9: LIST OF FIGURES & LIST OF TABLES
    # -------------------------------------------------------------
    add_p(doc, "LIST OF FIGURES", font_size=13, bold=True, space_before=2, space_after=4)
    figures = [
        ("Figure 3.1: Multi-Tier Microservice Architecture of Smart Approval AI", "7"),
        ("Figure 3.2: Level-0 Data Flow Diagram (DFD) of Ingestion & Verification", "8"),
        ("Figure 4.1: Entity-Relationship Diagram of Institutional Compliance Schema", "19"),
        ("Figure 5.1: High-Fidelity Interface of Executive Multi-Framework Compliance Hub", "22"),
        ("Figure 5.2: AICTE Approval Handbook & Deficiency Auditor Module Interface", "23"),
        ("Figure 5.3: NBA SAR Criterion-by-Criterion Evaluator & 1000-Point Scorecard", "23"),
        ("Figure 5.4: Longitudinal Multi-Year Analytics & SARIMA Forecasting Interface", "24"),
        ("Figure 5.5: Operational Modules (Ingestion, Cross-Year Comparison & Dossier Export)", "24"),
        ("Figure 5.6: Empirical Benchmark Evaluation across Layout Precision & TSR Accuracy", "27"),
    ]
    for fig_t, fig_p in figures:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.line_spacing = 1.15
        p_f.paragraph_format.space_before = Pt(0.5)
        p_f.paragraph_format.space_after = Pt(1.5)
        p_f.paragraph_format.tab_stops.add_tab_stop(Inches(6.4), WD_TAB_ALIGNMENT.RIGHT)
        rf = p_f.add_run(fig_t)
        rf.font.name = "Times New Roman"
        rf.font.size = Pt(9)
        rp = p_f.add_run(f"\t{fig_p}")
        rp.font.name = "Times New Roman"
        rp.font.size = Pt(9)
        
    add_p(doc, "LIST OF TABLES", font_size=13, bold=True, space_before=8, space_after=4)
    tables = [
        ("Table 2.1: Comparative Analysis of Apex Higher Education Quality Frameworks", "4"),
        ("Table 2.2: Evolution of Document Understanding & OCR Methodologies", "5"),
        ("Table 2.3: Systematic Comparison between Prior Approaches & Smart Approval AI", "6"),
        ("Table 3.1: Statutory Instructional Space & Land Norms (AICTE APH 2024-2027)", "12"),
        ("Table 3.2: NBA Tier-I 1000-Point Evaluation Criteria & Point Allocation", "13"),
        ("Table 4.1: Compute Hardware Testbed & Production Specifications", "17"),
        ("Table 4.2: Enterprise Software Technology Stack & Dependency Matrix", "17"),
        ("Table 4.3: Core Relational Database Entities & Field Specifications", "19"),
        ("Table 4.4: Primary RESTful Microservice API Endpoints", "20"),
        ("Table 5.1: Multi-Format Evaluation Corpus Composition & Distribution", "25"),
        ("Table 5.2: Parsing & Information Extraction Performance across Formats", "26"),
        ("Table 5.3: Metric-Level Extraction & Deterministic Computation Accuracy", "26"),
        ("Table 5.4: Empirical Comparative Evaluation: Manual Audits vs. Smart Approval AI", "27"),
        ("Table B.1: 14-Column CO-PO & PSO Correlation Matrix", "35"),
    ]
    for tbl_t, tbl_p in tables:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.space_before = Pt(0.5)
        p_t.paragraph_format.space_after = Pt(1.5)
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.4), WD_TAB_ALIGNMENT.RIGHT)
        rt = p_t.add_run(tbl_t)
        rt.font.name = "Times New Roman"
        rt.font.size = Pt(9)
        rp = p_t.add_run(f"\t{tbl_p}")
        rp.font.name = "Times New Roman"
        rp.font.size = Pt(9)
        
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 10: LIST OF ABBREVIATIONS
    # -------------------------------------------------------------
    add_p(doc, "LIST OF ABBREVIATIONS", font_size=13.5, bold=True, space_before=4, space_after=8)
    abbrevs = [
        ("AICTE", "All India Council for Technical Education"),
        ("NBA", "National Board of Accreditation"),
        ("NAAC", "National Assessment and Accreditation Council"),
        ("NIRF", "National Institutional Ranking Framework"),
        ("SAR", "Self-Assessment Report"),
        ("OBE", "Outcome-Based Education"),
        ("CO / PO / PSO", "Course Outcome / Program Outcome / Specific Outcome"),
        ("PEO", "Program Educational Objective"),
        ("SFR / FSR", "Student-Faculty Ratio / Faculty-Student Ratio"),
        ("OCR / VLM", "Optical Character Recognition / Vision-Language Model"),
        ("SARIMA", "Seasonal AutoRegressive Integrated Moving Average"),
        ("SUS", "System Usability Scale"),
        ("API / REST", "Application Programming Interface / REST Architecture"),
        ("SHA-256", "Secure Hash Algorithm 256-bit Cryptographic Hash"),
        ("JSON", "JavaScript Object Notation"),
        ("CIE / SEE", "Continuous Internal Evaluation / Semester End Exam"),
        ("SSR / AQAR", "Self-Study Report / Annual Quality Assurance Report"),
        ("IQAC", "Internal Quality Assurance Cell"),
        ("APH", "Approval Process Handbook (AICTE)"),
        ("DSRM", "Design Science Research Methodology"),
    ]
    
    tbl_abbr = doc.add_table(rows=len(abbrevs) + 1, cols=2)
    tbl_abbr.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_abbr = [1.8, 4.6]
    tbl_abbr.cell(0, 0).paragraphs[0].add_run("Abbreviation").font.bold = True
    tbl_abbr.cell(0, 1).paragraphs[0].add_run("Expansion / Full Term").font.bold = True
    for c_i in [0, 1]:
        tbl_abbr.cell(0, c_i).paragraphs[0].runs[0].font.name = "Times New Roman"
        tbl_abbr.cell(0, c_i).paragraphs[0].runs[0].font.size = Pt(9.5)
        
    for r_idx, (abb, exp) in enumerate(abbrevs, start=1):
        c0 = tbl_abbr.cell(r_idx, 0)
        c1 = tbl_abbr.cell(r_idx, 1)
        c0.paragraphs[0].paragraph_format.space_before = Pt(1.5)
        c0.paragraphs[0].paragraph_format.space_after = Pt(1.5)
        c1.paragraphs[0].paragraph_format.space_before = Pt(1.5)
        c1.paragraphs[0].paragraph_format.space_after = Pt(1.5)
        r0 = c0.paragraphs[0].add_run(abb)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r1 = c1.paragraphs[0].add_run(exp)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9)
        
    format_academic_table(tbl_abbr, col_widths=col_w_abbr)
    doc.add_page_break()

def build_complete_50page_master():
    print("=" * 60)
    print("COMPILING MASTER 50-PAGE HONORS DISSERTATION...")
    print("=" * 60)
    
    doc = docx.Document()
    
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
    
    # Header is empty
    h = sect.header
    for p in h.paragraphs:
        p.text = ""
        
    # 1. Preliminary pages (10 pages)
    build_preliminary_pages(doc)
    
    # 2. Chapters (Each chapter has its own ending page break, so no duplicate breaks!)
    print("Appending Chapter 1: Introduction...")
    build_chapter_1(doc)
    
    print("Appending Chapter 2: Literature Review...")
    build_chapter_2(doc)
    
    print("Appending Chapter 3: Methodology...")
    build_chapter_3(doc)
    
    print("Appending Chapter 4: Hardware & Software Requirements...")
    build_chapter_4(doc)
    
    print("Appending Chapter 5: Results & Discussions...")
    build_chapter_5(doc)
    
    print("Appending Chapter 6: Conclusion & Future Scope...")
    build_chapter_6(doc)
    
    # 3. References & Appendices A through F
    print("Appending References & Appendices A through F...")
    build_end_matter(doc)
    
    # Optimize image widths
    print("Optimizing image widths...")
    for shape in doc.inline_shapes:
        if shape.width > Inches(4.8):
            shape.width = Inches(4.5)
            
    for s in doc.sections:
        apply_page_border(s)
        
    print("Applying academic table styling across all tables...")
    for tbl in doc.tables:
        format_academic_table(tbl)
        
    doc.save(OUTPUT_DOCX)
    print(f"Master DOCX saved successfully to: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_complete_50page_master()
