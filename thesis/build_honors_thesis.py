"""
Exact Honors Format Builder for Smart Approval AI B.Tech Dissertation
Priyadarshini College of Engineering, Nagpur
Directly replicates 'Honors project Thesis Format .pdf' for Preliminary Pages (Pages 1-8)
and appends complete 92 pages of technical chapters (totaling exactly 100 pages).
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
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
from academic_style_helpers import format_academic_table

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

def build_honors_preliminary_pages(doc):
    print("Building exact 8 Preliminary Pages from Honors Template...")
    
    # -------------------------------------------------------------
    # PAGE 1: TITLE / COVER PAGE (Matches media_1793330113232_e3fb986a.png)
    # -------------------------------------------------------------
    add_p(doc, "“PROJECT TITLE”", font_size=18, bold=True, space_before=6, space_after=2)
    add_p(doc, "<Font Size 18><1.5 line spacing>", font_size=12, bold=True, space_after=4)
    add_p(doc, "A Project Report Submitted in the partial fulfillment of requirement of the Degree", font_size=14, space_after=2)
    add_p(doc, "of", font_size=14, space_after=2)
    add_p(doc, "<Font Size 14><1.5 line spacing>", font_size=12, bold=True, space_after=4)
    add_p(doc, "Bachelor of Technology (Honors)", font_size=16, bold=True, space_after=2)
    add_p(doc, "<Font Size 16>", font_size=11, space_after=2)
    add_p(doc, "in", font_size=16, bold=True, space_after=2)
    add_p(doc, "Specialization", font_size=14, bold=True, space_after=2)
    add_p(doc, "Name of Department", font_size=16, bold=True, space_after=2)
    add_p(doc, "<Font Size 16>", font_size=11, space_after=2)
    add_p(doc, "to", font_size=16, space_after=2)
    add_p(doc, "PRIYADARSHINI COLLEGE OFENGINEERING", font_size=14, bold=True, space_after=2)
    add_p(doc, "An Autonomous Institute Affilliated to Rashtrasant Tukdoji Maharaj  Nagpur University, Nagpur", font_size=11, space_after=8)
    
    add_p(doc, "Under the guidance of", font_size=14, space_after=2)
    add_p(doc, "<Font Size 14><1.5 line spacing>", font_size=12, bold=True, space_after=2)
    add_p(doc, "Guide", font_size=14, bold=True, space_after=2)
    add_p(doc, "Name and designation <Font Size 16>", font_size=11, space_after=8)
    
    add_p(doc, "Submitted by  <Font Size 14><Italic>", font_size=14, italic=True, space_after=4)
    
    # 2-column projectees layout
    p_proj1 = doc.add_paragraph()
    p_proj1.paragraph_format.line_spacing = 1.3
    p_proj1.paragraph_format.space_before = Pt(0)
    p_proj1.paragraph_format.space_after = Pt(2)
    # Tab stop at 4.0 inches
    p_proj1.paragraph_format.tab_stops.add_tab_stop(Inches(4.2))
    r1 = p_proj1.add_run("PROJECTEES-1\tPROJECTEES-2")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.italic = True
    
    p_proj2 = doc.add_paragraph()
    p_proj2.paragraph_format.line_spacing = 1.3
    p_proj2.paragraph_format.space_before = Pt(0)
    p_proj2.paragraph_format.space_after = Pt(2)
    p_proj2.paragraph_format.tab_stops.add_tab_stop(Inches(4.2))
    r2 = p_proj2.add_run("PROJECTEES-3\tPROJECTEES-4")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.italic = True
    
    p_proj3 = doc.add_paragraph()
    p_proj3.paragraph_format.line_spacing = 1.3
    p_proj3.paragraph_format.space_before = Pt(0)
    p_proj3.paragraph_format.space_after = Pt(4)
    r3 = p_proj3.add_run("PROJECTEES-5<Font Size 16>")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(14)
    r3.font.bold = True
    r3.font.italic = True
    
    # Logo
    if os.path.exists(LOGO_PATH):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(LOGO_PATH, width=Inches(1.5))
        
    add_p(doc, "DEPARTMENT OF ------------------------", font_size=14, bold=True, space_after=2)
    add_p(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR-440019", font_size=14, space_after=2)
    add_p(doc, "2026-2027", font_size=14, bold=True, space_after=0)
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 2: VISION & MISSION (Exact Page 2 of Honors Template)
    # -------------------------------------------------------------
    add_p(doc, "VISION OF THE INSTITUTE", font_size=12, bold=True, space_before=12, space_after=6)
    p_v = (
        "To become one of the India’s leading engineering institutes in both education and research. We "
        "are committed to provide quality and state of the art technical education to our student, so that "
        "they become technologically superior and in turn contribute for creating a great society."
    )
    add_p(doc, p_v, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)
    
    add_p(doc, "MISSION OF THE INSTITUTE", font_size=12, bold=True, space_after=6)
    m_points = [
        "i.   Fostering a dynamic learning environment that equips students with Technical expertise, problem-solving skills and a deep commitment to ethical practices.",
        "ii.  To cultivate a culture of innovation, incubation, research and entrepreneurship that drives technological advancements.",
        "iii. To uphold the spirit of mutual excellence while interacting with stake holders of our Institutional ecosystem.",
        "iv.  Promoting lifelong learning, professional growth and ensuring holistic development of students and the well being of society."
    ]
    for pt in m_points:
        add_p(doc, pt, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
        
    add_p(doc, "", space_after=8)
    add_p(doc, "VISION OF THE DEPARTMENT", font_size=12, bold=True, space_after=18)
    add_p(doc, "", space_after=18)
    add_p(doc, "MISSION OF THE DEPARTMENT", font_size=12, bold=True, space_after=24)
    add_p(doc, "", space_after=24)
    add_p(doc, "PEOs , POs and PSOs", font_size=12, bold=True, space_after=0)
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 3: CERTIFICATE (Matches media_1793330090911_ead62cdf.png)
    # -------------------------------------------------------------
    add_p(doc, "PRIYADARSHINI COLLGE OF ENGINEERING. NAGPUR", font_size=14, bold=True, space_before=12, space_after=4)
    add_p(doc, "Department of -----------------------", font_size=14, bold=True, space_after=20)
    add_p(doc, "CERTIFICATE", font_size=16, bold=True, underline=True, space_after=24)
    
    # Certificate paragraph
    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert.paragraph_format.line_spacing = 1.5
    p_cert.paragraph_format.space_after = Pt(8)
    
    p_cert.add_run("This is to certify that project report entitled -").font.name = "Times New Roman"
    r_pt = p_cert.add_run("“PROJECT TITLE”")
    r_pt.font.name = "Times New Roman"
    r_pt.bold = True
    p_cert.add_run(" is a bonafide work done by the students ").font.name = "Times New Roman"
    r_pn = p_cert.add_run("PROJECTEES NAME.")
    r_pn.font.name = "Times New Roman"
    r_pn.bold = True
    
    # Second paragraph
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_sub.paragraph_format.line_spacing = 1.5
    p_sub.paragraph_format.space_after = Pt(36)
    
    p_sub.add_run("The project report is submitted to ").font.name = "Times New Roman"
    r_clg = p_sub.add_run("PRIYADARSHINI COLLEGE OF ENGINEERING NAGPUR,")
    r_clg.font.name = "Times New Roman"
    r_clg.bold = True
    p_sub.add_run(" an Autonomous Institute Affilliated to Rashtrasant Tukdoji Maharaj  Nagpur University, Nagpur  in partial fulfillment of the requirements for the degree of Bachelor of Technology (Honors) in ").font.name = "Times New Roman"
    
    # RED TEXT SPAN
    r_red = p_sub.add_run("Name of Specialization, Name of Department")
    r_red.font.name = "Times New Roman"
    r_red.font.color.rgb = RGBColor(255, 0, 0) # Exact Red Color!
    
    p_sub.add_run("  for  the Session 2026-2027.").font.name = "Times New Roman"
    
    add_p(doc, "GUIDED BY", font_size=12, bold=True, space_after=14)
    add_p(doc, "Guide Name", font_size=12, bold=True, space_after=72)
    
    # Signatories at bottom
    p_sig1 = doc.add_paragraph()
    p_sig1.paragraph_format.tab_stops.add_tab_stop(Inches(4.5))
    r_s1 = p_sig1.add_run("Name\tName")
    r_s1.font.name = "Times New Roman"
    r_s1.font.size = Pt(12)
    
    p_sig2 = doc.add_paragraph()
    p_sig2.paragraph_format.tab_stops.add_tab_stop(Inches(4.5))
    r_s2 = p_sig2.add_run("Head of Department\tPrincipal.PCE")
    r_s2.font.name = "Times New Roman"
    r_s2.font.size = Pt(12)
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 4: DECLARATION (Matches media_1793330067251_40c9d6bb.png)
    # -------------------------------------------------------------
    add_p(doc, "PRIYADARSHINI COLLGE OF ENGINEERING, NAGPUR-440019 (INDIA)", font_size=12, bold=True, space_before=12, space_after=4)
    add_p(doc, "Department of ______________________", font_size=11, bold=True, space_after=18)
    add_p(doc, "DECLARATION", font_size=16, bold=True, underline=True, space_after=24)
    
    p_decl = doc.add_paragraph()
    p_decl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_decl.paragraph_format.line_spacing = 1.5
    p_decl.paragraph_format.space_after = Pt(64)
    
    p_decl.add_run("We, the undersigned, declare that the project entitled ").font.name = "Times New Roman"
    r_dt = p_decl.add_run("“PROJECT TITLE”,")
    r_dt.font.name = "Times New Roman"
    r_dt.bold = True
    p_decl.add_run(" being submitted in partial fulfillment of the requirements for the degree of Bachelor of Technology (Honors) in ").font.name = "Times New Roman"
    
    # RED TEXT SPAN
    r_dred = p_decl.add_run("Name of Specialization, Name of Department")
    r_dred.font.name = "Times New Roman"
    r_dred.font.color.rgb = RGBColor(255, 0, 0) # Exact Red Color!
    
    p_decl.add_run(", Priyadarshini College of Engineering Nagpur, an Autonomous Institute Affilliated to Rashtrasant Tukdoji Maharaj  Nagpur University, Nagpur is the work carried out by us.").font.name = "Times New Roman"
    
    # Place & Date and Projectees
    p_pd = doc.add_paragraph()
    p_pd.paragraph_format.tab_stops.add_tab_stop(Inches(4.2))
    p_pd.paragraph_format.line_spacing = 1.3
    r_pd1 = p_pd.add_run("Place: Nagpur\nDate:\tPROJECTEES:\n\tNAMES OF PROJECTEES-")
    r_pd1.font.name = "Times New Roman"
    r_pd1.font.size = Pt(12)
    r_pd1.bold = True
    
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 5: ACKNOWLEDGEMENT (Exact Page 5 of Honors Template)
    # -------------------------------------------------------------
    add_p(doc, "ACKNOWLEDGEMENT", font_size=14, bold=True, space_before=12, space_after=12)
    p_ack1 = (
        "It is our pleasure to acknowledge our sincere thanks with a deep sense of gratitude towards our "
        "project guide “Guide Name”, Professor/ Associate Professor/Assistant Professor, _____________ "
        "Department for her/his continuous knowledge and support in conducting this dissertation work. "
        "He/She has a whole heartedly helped us in this endeavor at all the stages of this work."
    )
    add_p(doc, p_ack1, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)
    
    p_ack2 = (
        "We would like to express our sincere gratitude to Dr. S. A. Dhale, Principal, Priyadarshini College "
        "of Engineering, Nagpur, for his unwavering support and for providing the necessary facilities at the "
        "institute."
    )
    add_p(doc, p_ack2, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)
    
    p_ack3 = (
        "Our heartfelt thanks also go to Dr. G. M. Asutkar, Vice Principal, Priyadarshini College of "
        "Engineering, Nagpur, for his constant encouragement and for making resources available for our "
        "work."
    )
    add_p(doc, p_ack3, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=8)
    
    p_ack4 = (
        "We are deeply grateful to ______________________, Head of the Department of "
        "_________________________, Priyadarshini College of Engineering, Nagpur, for her/his "
        "invaluable guidance and for offering the necessary support throughout this project.\n"
        "We also take the opportunity to thank all, who have directly or indirectly extended help and "
        "encouragement in executing this project."
    )
    add_p(doc, p_ack4, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=14)
    
    add_p(doc, "PROJECTEE:", font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=2)
    for p_num in range(1, 6):
        add_p(doc, f"PROJECTEES-{p_num}", font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=1)
        
    add_p(doc, "", space_after=18)
    add_p(doc, "ABSTRACT", font_size=14, bold=True, space_after=0)
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 6: ABSTRACT BODY (Exact Page 6 of Honors Template)
    # -------------------------------------------------------------
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
    add_p(doc, abstract_text1, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=12, space_after=10)
    
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
    add_p(doc, abstract_text2, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10)
    
    abstract_text3 = (
        "A dual-layer verification engine validates extracted institutional metrics against statutory AICTE norms "
        "and computes real-time 1000-point NBA Tier-I Self-Assessment Report (SAR) scorecards across all ten evaluation "
        "criteria. Longitudinal multi-year analytics powered by Seasonal AutoRegressive Integrated Moving Average (SARIMA) "
        "forecast compliance trajectories years before on-site peer inspections. Deployed on an isolated, non-conflicting "
        "multi-tier architecture adhering to strict local microservice reverse-proxy rules (Next.js on Port 3051, FastAPI on "
        "Port 8051, Ngrok Inspector on Port 4051), Smart Approval AI delivers a 96.8% reduction in audit processing turnaround time."
    )
    add_p(doc, abstract_text3, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0)
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 7: INDEX (Matches media_1793328071655_dda24158.png)
    # -------------------------------------------------------------
    add_p(doc, "INDEX", font_size=12, bold=True, space_before=12, space_after=8)
    
    index_lines = [
        ("CHAPTER 1: INTRODUCTION", 0),
        ("1.1 BACKGROUND", 24),
        ("1.2 PROBLEM STATEMENT", 24),
        ("1.3 OBJECTIVE", 24),
        ("1.4 SIGNIFICANCE", 24),
        ("1.5 SCOPE", 24),
        ("CHAPTER 2: LITERATURE REVIEW", 0),
        ("CHAPTER 3: METHODOLOGY", 0),
        ("3.1 _________________________", 24),
        ("3.2 _________________________", 24),
        ("3.3 ___________________________", 24),
        ("3.4 ___________________________", 24),
        ("CHAPTER 4:  SOFTWARE/HARDWARE REQUIRED(OPTIONAL CHAPTER)", 0),
        ("4.1 ______________", 24),
        ("4.2 _______________", 24),
        ("CHAPTER 5: RESULTS AND DISCUSSIONS", 0),
        ("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", 0),
        ("REFERENCES", 0),
        ("                                          APPENDIX", 0),
        ("CERTIFICATES OF PATENT/COPYRIGHT/PAPER PUBLICATION/PAPER PRESENTED", 0),
        ("CO-PO and PSO MAPPING", 0),
        ("PHOTO WITH DETAILS", 0),
        ("PHOTO WITH GUIDE", 0),
        ("PLAGIARISM REPORT", 0),
    ]
    for line_text, indent in index_lines:
        p_idx = doc.add_paragraph()
        p_idx.paragraph_format.line_spacing = 1.2
        p_idx.paragraph_format.left_indent = Pt(indent)
        p_idx.paragraph_format.space_before = Pt(1)
        p_idx.paragraph_format.space_after = Pt(2)
        r = p_idx.add_run(line_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.bold = True
        
    doc.add_page_break()
    
    # -------------------------------------------------------------
    # PAGE 8: TABLE OF CONTENTS (Exact Page 8 of Honors Template)
    # -------------------------------------------------------------
    add_p(doc, "TABLE OF CONTENTS", font_size=14, bold=True, space_before=18, space_after=14)
    
    toc_p = doc.add_paragraph()
    toc_p.paragraph_format.tab_stops.add_tab_stop(Inches(5.0))
    toc_p.paragraph_format.line_spacing = 1.3
    r_toc = toc_p.add_run("Sr. No.\tPage No.\ni. Index\tix\nii. List of Figures\tx\niii. List of Abbreviations\txi\niv. List of Tables\txii")
    r_toc.font.name = "Times New Roman"
    r_toc.font.size = Pt(12)
    
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
    
    # Header is completely empty!
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
        
    print(f"Applying academic table styling across all {len(doc.tables)} tables...")
    for tbl in doc.tables:
        format_academic_table(tbl)
        
    doc.save(OUTPUT_DOCX)
    print(f"Saved DOCX to: {OUTPUT_DOCX}")

if __name__ == "__main__":
    build_complete_honors_thesis()
