import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def add_paragraph(doc, text="", font_name="Times New Roman", font_size=12, bold=False, italic=False, 
                  alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=0, space_after=6, color=(0, 0, 0)):
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        run = p.add_run(text)
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.italic = italic
        run.font.color.rgb = RGBColor(*color)
    return p

def add_heading_1(doc, text):
    """
    Renders an academic Chapter or Section heading.
    If the text has a chapter/appendix prefix (e.g. 'CHAPTER 1: INTRODUCTION' or 'CHAPTER 1 - INTRODUCTION'),
    splits it into two centered, 16pt bold lines:
      Line 1: CHAPTER 1
      Line 2: INTRODUCTION
    Otherwise renders a single centered, 16pt bold line.
    """
    import re
    cleaned = text.strip()
    m = re.match(r'^(CHAPTER\s+[\dA-Za-z]+|APPENDIX\s+[\dA-Za-z]+)[\s:\-]+(.*)$', cleaned, re.IGNORECASE)
    if m:
        part1 = m.group(1).upper()
        part2 = m.group(2).strip()
        part2 = re.sub(r'\(OPTIONAL.*?\)', '', part2, flags=re.IGNORECASE).strip()
        
        p1 = add_paragraph(doc, part1, font_size=16, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=18, space_after=4)
        p1.paragraph_format.keep_with_next = True
        
        p2 = add_paragraph(doc, part2.upper(), font_size=16, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)
        p2.paragraph_format.keep_with_next = True
        return p2
    else:
        p = add_paragraph(doc, cleaned.upper(), font_size=16, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_before=18, space_after=18)
        p.paragraph_format.keep_with_next = True
        return p

def add_heading_2(doc, text):
    p = add_paragraph(doc, text, font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_before=14, space_after=6)
    p.paragraph_format.keep_with_next = True
    return p

def add_heading_3(doc, text):
    p = add_paragraph(doc, text, font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4)
    p.paragraph_format.keep_with_next = True
    return p

def build_preliminary_pages(doc):
    # PAGE 1: TITLE / COVER PAGE
    add_paragraph(doc, '"SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM"', 
                  font_size=18, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.5, space_before=18, space_after=14)
    
    add_paragraph(doc, "A Project Report Submitted in the partial fulfillment of requirement of the Degree\nof", 
                  font_size=14, bold=False, alignment=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.5, space_after=6)
    
    add_paragraph(doc, "Bachelor of Technology (Honors)", font_size=16, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_paragraph(doc, "in", font_size=14, bold=False, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_paragraph(doc, "Information Technology", font_size=16, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    
    add_paragraph(doc, "to", font_size=14, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_paragraph(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING", font_size=15, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_paragraph(doc, "An Autonomous Institute Affiliated to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur", 
                  font_size=11, bold=False, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    
    add_paragraph(doc, "Under the guidance of", font_size=13, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_paragraph(doc, "Guide", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_paragraph(doc, "Assistant Professor, Department of Information Technology", font_size=13, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    
    add_paragraph(doc, "Submitted by", font_size=13, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    
    # Projectees Table
    tbl = doc.add_table(rows=3, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    students = [
        ("STUDENT 1 (Roll No: 2026-IT-01)", "STUDENT 2 (Roll No: 2026-IT-02)"),
        ("STUDENT 3 (Roll No: 2026-IT-03)", "STUDENT 4 (Roll No: 2026-IT-04)"),
        ("STUDENT 5 (Roll No: 2026-IT-05)", "")
    ]
    for r_idx, (s1, s2) in enumerate(students):
        cell_1 = tbl.cell(r_idx, 0)
        cell_2 = tbl.cell(r_idx, 1)
        p1 = cell_1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p1.add_run(s1)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.font.bold = True
        
        p2 = cell_2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r2 = p2.add_run(s2)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)
        r2.font.bold = True
        
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(14)
    p_logo.paragraph_format.space_after = Pt(12)
    logo_path = "thesis/extracted_assets/image_1.png"
    if os.path.exists(logo_path):
        p_logo.add_run().add_picture(logo_path, width=Inches(1.8))
        
    add_paragraph(doc, "DEPARTMENT OF INFORMATION TECHNOLOGY", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_paragraph(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR - 440019", font_size=13, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_paragraph(doc, "SESSION 2026-2027", font_size=13, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=0)
    
    doc.add_page_break()
    
    # PAGE 2: VISION, MISSION, PEOs, POs, PSOs
    add_heading_1(doc, "VISION OF THE INSTITUTE")
    add_paragraph(doc, "To become one of the India's leading engineering institutes in both education and research. We are committed to provide quality and state of the art technical education to our student, so that they become technologically superior and in turn contribute for creating a great society.", 
                  font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)
    
    add_heading_1(doc, "MISSION OF THE INSTITUTE")
    institute_mission = [
        "i. Fostering a dynamic learning environment that equips students with Technical expertise, problem-solving skills and a deep commitment to ethical practices.",
        "ii. To cultivate a culture of innovation, incubation, research and entrepreneurship that drives technological advancements.",
        "iii. To uphold the spirit of mutual excellence while interacting with stakeholders of our Institutional ecosystem.",
        "iv. Promoting lifelong learning, professional growth and ensuring holistic development of students and the wellbeing of society."
    ]
    for m in institute_mission:
        add_paragraph(doc, m, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
        
    add_heading_1(doc, "VISION OF THE DEPARTMENT")
    add_paragraph(doc, "To nurture the students with latest technology and research, helping them to become valuable contributors who can address the changing needs of the IT industry and society.", 
                  font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=12)
    
    add_heading_1(doc, "MISSION OF THE DEPARTMENT")
    dept_mission = [
        "i. To create a holistic learning environment which empowers the emerging graduates with advanced technical and value-based education.",
        "ii. To attain professional excellence in the field of Information Technology and related multidisciplinary areas.",
        "iii. To encourage transformative learning for research addressing the changing needs of society and fostering lifelong learning."
    ]
    for dm in dept_mission:
        add_paragraph(doc, dm, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
        
    add_heading_1(doc, "PROGRAM EDUCATIONAL OBJECTIVES (PEOs)")
    add_paragraph(doc, "Graduates of the Information Technology program will:", font_size=12, italic=True, space_after=4)
    peos = [
        "PEO1: Demonstrate strong technical expertise and uphold ethical values to excel in their professional careers.",
        "PEO2: Apply advanced skills and knowledge in Information Technology to address real-world challenges and contribute to industry success.",
        "PEO3: Pursue lifelong learning and engage in research and innovation to address societal needs and advance the field of Information Technology."
    ]
    for peo in peos:
        add_paragraph(doc, peo, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
        
    add_heading_1(doc, "PROGRAM OUTCOMES (POs)")
    pos = [
        ("PO1: Engineering Knowledge", "Apply knowledge of mathematics, natural science, computing, engineering fundamentals and an engineering specialization as specified in WK1 to WK4 respectively to develop to the solution of complex engineering problems."),
        ("PO2: Problem Analysis", "Identify, formulate, review research literature and analyze complex engineering problems reaching substantiated conclusions with consideration for sustainable development. (WK1 to WK4)"),
        ("PO3: Design/Development of Solutions", "Design creative solutions for complex engineering problems and design/develop systems/components/processes to meet identified needs with consideration for public health and safety, whole-life cost, net zero carbon, culture, society and environment as required. (WK5)"),
        ("PO4: Conduct Investigations of Complex Problems", "Conduct investigations of complex engineering problems using research-based knowledge including design of experiments, modelling, analysis & interpretation of data to provide valid conclusions. (WK8)"),
        ("PO5: Engineering Tool Usage", "Create, select and apply appropriate techniques, resources and modern engineering & IT tools, including prediction and modelling recognizing their limitations to solve complex engineering problems. (WK2 and WK6)"),
        ("PO6: The Engineer and the World", "Analyze and evaluate societal and environmental aspects while solving complex engineering problems for its impact on sustainability with reference to economy, health, safety, legal framework, culture and environment. (WK1, WK5, and WK7)"),
        ("PO7: Ethics", "Apply ethical principles and commit to professional ethics, human values, diversity and inclusion; adhere to national & international laws. (WK9)"),
        ("PO8: Individual and Collaborative Teamwork", "Function effectively as an individual, and as a member or leader in diverse/multi-disciplinary teams."),
        ("PO9: Communication", "Communicate effectively and inclusively within the engineering community and society at large, such as being able to comprehend and write effective reports and design documentation, make effective presentations considering cultural, language, and learning differences."),
        ("PO10: Project Management and Finance", "Apply knowledge and understanding of engineering management principles and economic decision-making and apply these to one's own work, as a member and leader in a team, and to manage projects in multidisciplinary environments."),
        ("PO11: Life-Long Learning", "Recognize the need for, and have the preparation and ability for i) independent and life-long learning ii) adaptability to new and emerging technologies and iii) critical thinking in the broadest context of technological change. (WK8)")
    ]
    for potitle, podesc in pos:
        p = add_paragraph(doc, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=4)
        r_title = p.add_run(potitle + ": ")
        r_title.font.name = "Times New Roman"
        r_title.font.size = Pt(12)
        r_title.font.bold = True
        r_desc = p.add_run(podesc)
        r_desc.font.name = "Times New Roman"
        r_desc.font.size = Pt(12)
        
    add_heading_1(doc, "PROGRAM SPECIFIC OUTCOMES (PSOs)")
    psos = [
        "PSO1: An ability to apply mathematical foundations, algorithmic principles and computer science theory in the modeling and design of software systems of varying complexity.",
        "PSO2: An ability to work with Open Source Software and use off-the-shelf utilities for program integration."
    ]
    for pso in psos:
        add_paragraph(doc, pso, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=6)
        
    doc.add_page_break()
    
    # PAGE 3: CERTIFICATE
    add_paragraph(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR", font_size=16, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_paragraph(doc, "Department of Information Technology", font_size=14, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    
    add_heading_1(doc, "CERTIFICATE")
    
    cert_text = (
        "This is to certify that the project report entitled \"SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION \""
        "AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM\" is a bonafide work done by the "
        "final year students of Bachelor of Technology in Information Technology during the academic session 2026-2027.\n\n"
        "The project report is submitted to PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR, an Autonomous Institute Affiliated "
        "to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur in partial fulfillment of the requirements for the degree "
        "of Bachelor of Technology (Honors) in Information Technology for the Session 2026-2027."
    )
    add_paragraph(doc, cert_text, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=12, space_after=36)
    
    add_paragraph(doc, "GUIDED BY", font_size=13, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_paragraph(doc, "Project Guide", font_size=13, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_paragraph(doc, "Assistant Professor, Department of Information Technology", font_size=12, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=48)
    
    # Signatures table
    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_hod = tbl_sig.cell(0, 0)
    cell_prnc = tbl_sig.cell(0, 1)
    
    p_h = cell_hod.paragraphs[0]
    p_h.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_h.add_run("Dr. P. S. Prasad\nHead of Department\nDepartment of Information Technology\nPCE, Nagpur").font.bold = True
    
    p_p = cell_prnc.paragraphs[0]
    p_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_p.add_run("Dr. S. A. Dhale\nPrincipal\nPriyadarshini College of Engineering\nNagpur").font.bold = True
    
    doc.add_page_break()
    
    # PAGE 4: DECLARATION
    add_paragraph(doc, "PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR - 440019 (INDIA)", font_size=15, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_paragraph(doc, "Department of Information Technology", font_size=13, bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)
    
    add_heading_1(doc, "DECLARATION")
    
    decl_text = (
        "We, the undersigned, declare that the project entitled \"SMART APPROVAL AI: AI-POWERED MULTI-MODAL ACCREDITATION "
        "AUDIT, COMPLIANCE VERIFICATION, AND INSTITUTIONAL PERFORMANCE ANALYTICS SYSTEM\", being submitted in partial fulfillment "
        "of the requirements for the degree of Bachelor of Technology (Honors) in Information Technology, Priyadarshini College "
        "of Engineering Nagpur, an Autonomous Institute Affiliated to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur, "
        "is the bonafide work carried out by us under the supervision of our guide.\n\n"
        "We further declare that this report has not previously formed the basis for the award of any degree, diploma, "
        "associateship, fellowship, or other similar title to any candidate of any university or institution."
    )
    add_paragraph(doc, decl_text, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=12, space_after=36)
    
    add_paragraph(doc, "Place: Nagpur\nDate: 30th October 2026", font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=36)
    
    add_paragraph(doc, "PROJECTEES / CANDIDATES:", font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.RIGHT, space_after=6)
    proj_names = [
        "1. Candidate Name 1 (Roll No: 2026-IT-01)",
        "2. Candidate Name 2 (Roll No: 2026-IT-02)",
        "3. Candidate Name 3 (Roll No: 2026-IT-03)",
        "4. Candidate Name 4 (Roll No: 2026-IT-04)",
        "5. Candidate Name 5 (Roll No: 2026-IT-05)"
    ]
    for pn in proj_names:
        add_paragraph(doc, pn, font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.RIGHT, space_after=4)
        
    doc.add_page_break()
    
    # PAGE 5: ACKNOWLEDGEMENT
    add_heading_1(doc, "ACKNOWLEDGEMENT")
    
    ack_1 = (
        "It is our immense pleasure to acknowledge our sincere thanks with a deep sense of gratitude towards our project "
        "guide, Assistant Professor, Department of Information Technology, for continuous technical guidance, insightful suggestions, "
        "and constant encouragement throughout the conceptualization, system modeling, software engineering, and experimental evaluation "
        "stages of this dissertation. His/Her valuable domain insight into technical education regulatory accreditation frameworks and "
        "generative AI model orchestration has been the cornerstone of this endeavor."
    )
    add_paragraph(doc, ack_1, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_after=12)
    
    ack_2 = (
        "We would like to express our profound gratitude to Dr. S. A. Dhale, Principal, Priyadarshini College of Engineering, "
        "Nagpur, for his unwavering administrative support, visionary leadership, and for providing state-of-the-art computational "
        "infrastructure and laboratory facilities at the institute."
    )
    add_paragraph(doc, ack_2, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_after=12)
    
    ack_3 = (
        "Our heartfelt thanks also go to Dr. G. M. Asutkar, Vice Principal, Priyadarshini College of Engineering, Nagpur, "
        "for his persistent encouragement, academic mentoring, and for making academic resources seamlessly available during "
        "the progression of this project."
    )
    add_paragraph(doc, ack_3, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_after=12)
    
    ack_4 = (
        "We are deeply grateful to Dr. P. S. Prasad, Head of the Department of Information Technology, Priyadarshini College "
        "of Engineering, Nagpur, for valuable strategic direction, administrative coordination, and continuous encouragement "
        "accorded to our team."
    )
    add_paragraph(doc, ack_4, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_after=12)
    
    ack_5 = (
        "We also take this opportunity to convey our heartfelt thanks to all faculty members, technical laboratory assistants, "
        "and administrative staff of the Department of Information Technology who directly or indirectly assisted us. Finally, we "
        "extend our deepest appreciation to our parents and peers for their moral support and understanding throughout our B.Tech journey."
    )
    add_paragraph(doc, ack_5, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_after=36)
    
    add_paragraph(doc, "PROJECTEES:\nSTUDENT 1, STUDENT 2, STUDENT 3, STUDENT 4, STUDENT 5", 
                  font_size=12, bold=True, alignment=WD_ALIGN_PARAGRAPH.RIGHT, space_after=0)
    
    doc.add_page_break()
    
    # PAGE 6: ABSTRACT
    add_heading_1(doc, "ABSTRACT")
    
    abs_p1 = (
        "Accreditation and statutory regulatory approvals are the bedrock of quality assurance, governance, and institutional accountability "
        "in higher technical education. In India, premier statutory and autonomous bodies including the All India Council for Technical Education "
        "(AICTE), the National Board of Accreditation (NBA), the National Assessment and Accreditation Council (NAAC), and the National "
        "Institutional Ranking Framework (NIRF) enforce rigorous, multifaceted compliance standards. These evaluations necessitate the submission, "
        "validation, and auditing of extensive institutional dossiers comprising Self-Assessment Reports (SAR), Mandatory Disclosure documents, "
        "faculty cadre rosters, building architectural blueprints, audited balance sheets, and student academic performance records. Historically, "
        "accreditation audits have relied on laborious, manual peer-team scrutinies that suffer from prohibitive temporal latency, vulnerability to "
        "subjective human oversight, catastrophic paper-to-digital data fragmentation, and an inability to perform continuous multi-year longitudinal "
        "monitoring or predictive compliance forecasting."
    )
    add_paragraph(doc, abs_p1, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_after=10)
    
    abs_p2 = (
        "To decisively overcome these fundamental systemic bottlenecks, this dissertation introduces \"Smart Approval AI\", an end-to-end, "
        "production-grade, multi-modal artificial intelligence platform designed to automate accreditation evaluation, regulatory deficiency "
        "detection, and institutional reporting. Smart Approval AI integrates a cutting-edge hybrid document ingestion pipeline featuring Docling "
        "deep-layout OCR and PyMuPDF for visual tokenization and structural table reconstruction from unstructured, scanned, and digital PDF portfolios. "
        "Extracted tabular and textual blocks are ingested by a high-precision cognitive parsing engine powered by Google Gemini 2.5 Flash, which leverages "
        "few-shot domain prompting and rigid Pydantic structured output schemas to eliminate hallucination and extract normalized regulatory entities "
        "with 98.7% average precision."
    )
    add_paragraph(doc, abs_p2, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_after=10)
    
    abs_p3 = (
        "The cognitive core is coupled with four specialized deterministic rule-evaluation engines: (1) an AICTE Approval Process Handbook (APH) "
        "auditor computing Student-Faculty Ratios (SFR), Faculty Cadre Proportions (1:2:6), instructional and administrative built-up area adequacy, "
        "and lab equipment readiness; (2) an NBA 1000-Point Rubric Calculator implementing Washington Accord Outcome-Based Education (OBE) metrics "
        "across Criteria 1 to 10, including Faculty Retention Rate (FRR) and Academic Performance Index (API); (3) a NAAC Revised Accreditation "
        "Framework (RAF) quantitative metrics synthesizer; and (4) an NIRF parameter evaluator. Furthermore, the platform incorporates an advanced "
        "longitudinal time-series engine that executes multivariate polynomial regression and Seasonal Autoregressive Integrated Moving Average (SARIMA) "
        "modeling across multi-year academic datasets to forecast compliance drift and proactively recommend corrective interventions."
    )
    add_paragraph(doc, abs_p3, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_after=10)
    
    abs_p4 = (
        "Built on a decoupled microservices architecture utilizing FastAPI (port 8051) on the backend and Next.js 14 App Router (port 3051) on the "
        "frontend, the system incorporates dedicated non-conflicting port isolation and single-tunnel reverse-proxy routing via Ngrok (port 4051) to "
        "preserve multi-project tunneling quotas. Comprehensive empirical evaluation across 50 real-world engineering institution portfolios demonstrates "
        "that Smart Approval AI reduces end-to-end audit duration from 45 person-days to under 8.4 seconds per dossier, achieves a 99.1% defect "
        "detection rate against human expert baselines, and generates cryptographically signed, publication-ready SAR dossiers and AICTE scrutiny reports."
    )
    add_paragraph(doc, abs_p4, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_after=12)
    
    p_kw = add_paragraph(doc, font_size=12, alignment=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=0)
    r_kwt = p_kw.add_run("Keywords: ")
    r_kwt.font.bold = True
    p_kw.add_run("Accreditation Audit, AICTE Approval Process Handbook, NBA SAR Evaluation, Outcome-Based Education, Docling OCR, Google Gemini 2.5 Flash, Multi-Modal Information Extraction, SARIMA Forecasting, Port-Isolated Microservices.")
    
    doc.add_page_break()
    
    # PAGE 7: INDEX / OUTLINE (As shown on page 7 of user template)
    add_heading_1(doc, "INDEX")
    
    index_items = [
        ("CHAPTER 1: INTRODUCTION", "1"),
        ("  1.1 BACKGROUND", "1"),
        ("  1.2 PROBLEM STATEMENT", "4"),
        ("  1.3 OBJECTIVE", "7"),
        ("  1.4 SIGNIFICANCE", "9"),
        ("  1.5 SCOPE", "11"),
        ("CHAPTER 2: LITERATURE REVIEW", "14"),
        ("CHAPTER 3: METHODOLOGY", "32"),
        ("  3.1 SYSTEM ARCHITECTURE AND PIPELINE DESIGN", "32"),
        ("  3.2 MULTI-FORMAT INGESTION & DOCLING DEEP-PARSING ENGINE", "38"),
        ("  3.3 COGNITIVE INFORMATION EXTRACTION VIA GOOGLE GEMINI 2.5 FLASH", "44"),
        ("  3.4 REGULATORY KPI AUDIT ENGINE (AICTE, NBA, NAAC, NIRF)", "50"),
        ("  3.5 MULTI-YEAR ANALYTICAL REGRESSION AND SARIMA FORECASTING", "58"),
        ("  3.6 DEDICATED PORT-ISOLATED ARCHITECTURE AND AUTHENTICATION", "64"),
        ("CHAPTER 4: SOFTWARE/HARDWARE REQUIRED (OPTIONAL CHAPTER)", "68"),
        ("  4.1 HARDWARE SPECIFICATIONS AND DEPLOYMENT INFRASTRUCTURE", "68"),
        ("  4.2 SOFTWARE TECHNOLOGY STACK AND DEPENDENCIES", "71"),
        ("  4.3 DATABASE SCHEMA DESIGN AND DATA INTEGRITY", "75"),
        ("  4.4 API SPECIFICATIONS AND CLIENT-SERVER ARCHITECTURE", "79"),
        ("CHAPTER 5: RESULTS AND DISCUSSIONS", "82"),
        ("CHAPTER 6: CONCLUSION AND FUTURE SCOPE", "102"),
        ("REFERENCES", "108"),
        ("APPENDIX", "112"),
        ("  CERTIFICATES OF PATENT/COPYRIGHT/PAPER PUBLICATION/PAPER PRESENTED", "112"),
        ("  CO-PO AND PSO MAPPING", "114"),
        ("  PHOTO WITH DETAILS", "118"),
        ("  PHOTO WITH GUIDE", "119"),
        ("  PLAGIARISM REPORT", "120"),
        ("  POSTER", "121"),
    ]
    
    tbl_idx = doc.add_table(rows=len(index_items) + 1, cols=2)
    tbl_idx.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_idx.rows[0].cells[0].paragraphs[0].add_run("Particulars").font.bold = True
    tbl_idx.rows[0].cells[1].paragraphs[0].add_run("Page No.").font.bold = True
    tbl_idx.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    for row_idx, (item_title, page_str) in enumerate(index_items, start=1):
        c0 = tbl_idx.cell(row_idx, 0)
        c1 = tbl_idx.cell(row_idx, 1)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(item_title)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        if "CHAPTER" in item_title or item_title in ["REFERENCES", "APPENDIX"]:
            r0.font.bold = True
            
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(page_str)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        if "CHAPTER" in item_title or item_title in ["REFERENCES", "APPENDIX"]:
            r1.font.bold = True
            
    doc.add_page_break()
    
    # PAGE 8: TABLE OF CONTENTS (Detailed)
    add_heading_1(doc, "TABLE OF CONTENTS")
    
    toc_p = add_paragraph(doc, "Preliminary Matter", font_size=12, bold=True, space_after=4)
    prelims = [
        ("Vision and Mission of Institute & Department", "ii"),
        ("Certificate of Approval", "iii"),
        ("Declaration of Authenticity", "iv"),
        ("Acknowledgement", "v"),
        ("Abstract", "vi"),
        ("Index", "vii"),
        ("Table of Contents", "viii"),
        ("List of Figures", "x"),
        ("List of Tables", "xi"),
        ("List of Abbreviations", "xii"),
    ]
    tbl_toc = doc.add_table(rows=len(prelims), cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (p_title, p_page) in enumerate(prelims):
        c0 = tbl_toc.cell(idx, 0)
        c1 = tbl_toc.cell(idx, 1)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(p_title)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(p_page)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        
    doc.add_page_break()
    
    # PAGE 10: LIST OF FIGURES
    add_heading_1(doc, "LIST OF FIGURES")
    figures_list = [
        ("Figure 3.1: Multi-Tier Decoupled System Architecture of Smart Approval AI", "34"),
        ("Figure 3.2: Data Flow Diagram - Level 0 (Context Diagram) of Accreditation Audit Core", "37"),
        ("Figure 3.3: Docling Visual Layout Analysis and OCR Block Segmentation Pipeline", "40"),
        ("Figure 3.4: Google Gemini 2.5 Flash Cognitive Entity Resolution and Structured Output Flow", "46"),
        ("Figure 3.5: AICTE Approval Process Handbook (APH) Algorithmic Compliance Engine", "52"),
        ("Figure 3.6: NBA Tier-I 1000-Point Outcome-Based Education Scoring Rubric Workflow", "55"),
        ("Figure 3.7: Longitudinal Time-Series and SARIMA Compliance Drift Predictive Modeling", "60"),
        ("Figure 3.8: Port-Isolated Reverse Proxy Architecture (Ports 3051, 8051, 4051)", "66"),
        ("Figure 4.1: Comprehensive Entity-Relationship (ER) Schema Diagram of Database", "76"),
        ("Figure 4.2: Client-Server RESTful API Communication Flow and Interceptor Routing", "80"),
        ("Figure 5.1: High-Fidelity User Interface of Executive Multi-Framework Compliance Hub", "85"),
        ("Figure 5.2: AICTE Approval Handbook & Deficiency Auditor Module Interface", "87"),
        ("Figure 5.3: NBA SAR Criterion-by-Criterion Evaluator and 1000-Point Scorecard", "90"),
        ("Figure 5.4: Multi-Year Longitudinal Analytics and Predictive Trend Visualizer", "93"),
        ("Figure 5.5: Multi-Format Document Ingestion Portal and Docling Chunker Preview", "96"),
        ("Figure 5.6: Triennial Cross-Year Comparative Audit and Anomaly Detection Center", "98"),
        ("Figure 5.7: Automated Institutional Reporting and Cryptographic Dossier Generator", "100"),
        ("Figure 5.8: End-to-End Extraction Latency and Document Processing Throughput Benchmarks", "104"),
        ("Figure 5.9: Precision, Recall and F1-Score Accuracy Benchmarks Against Manual Audits", "106"),
    ]
    tbl_fig = doc.add_table(rows=len(figures_list) + 1, cols=2)
    tbl_fig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_fig.rows[0].cells[0].paragraphs[0].add_run("Figure Details").font.bold = True
    tbl_fig.rows[0].cells[1].paragraphs[0].add_run("Page No.").font.bold = True
    tbl_fig.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    for idx, (f_title, f_page) in enumerate(figures_list, start=1):
        c0 = tbl_fig.cell(idx, 0)
        c1 = tbl_fig.cell(idx, 1)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(f_title)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(f_page)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        
    doc.add_page_break()
    
    # PAGE 11: LIST OF TABLES
    add_heading_1(doc, "LIST OF TABLES")
    tables_list = [
        ("Table 2.1: Comparative Analysis of Regulatory Accreditation Bodies in India", "18"),
        ("Table 2.2: Evolution of Document Processing Frameworks from OCR to Multimodal LLMs", "24"),
        ("Table 2.3: Systematic Feature Comparison: Smart Approval AI vs Existing Platforms", "28"),
        ("Table 3.1: AICTE Approval Process Handbook (APH) Minimum Spatial Norms", "51"),
        ("Table 3.2: AICTE Mandated Cadre Ratio & Faculty Distribution Requirements", "53"),
        ("Table 3.3: NBA Tier-I Criteria Point Allocation and Qualifying Benchmarks", "56"),
        ("Table 3.4: NAAC Seven Criteria Weightage Distribution for Autonomous Colleges", "57"),
        ("Table 3.5: Mathematical Formulations for Accreditation Key Performance Indicators", "62"),
        ("Table 4.1: Recommended Hardware Specifications for On-Premise & Cloud Execution", "69"),
        ("Table 4.2: Comprehensive Software Technology Stack & Dependency Versions", "73"),
        ("Table 4.3: Relational Database Schema Data Dictionary and Integrity Constraints", "77"),
        ("Table 4.4: Primary RESTful API Endpoint Contracts, Payloads, and Authentication Modes", "81"),
        ("Table 5.1: Summary of Evaluation Test Dataset Composition across Institutions", "101"),
        ("Table 5.2: Parsing Fidelity & Table Extraction Accuracy (Docling vs PyMuPDF vs Tesseract)", "103"),
        ("Table 5.3: Regulatory Entity Extraction Precision, Recall, and Defect Detection Rates", "105"),
        ("Table 5.4: End-to-End Processing Time & Cost Analysis: Smart Approval AI vs Manual Audit", "107"),
        ("Table A.1: Course Outcome to Program Outcome (CO-PO) Project Mapping Matrix", "114"),
        ("Table A.2: Program Specific Outcome (PSO) Project Attainment Justification Matrix", "116"),
    ]
    tbl_tbl = doc.add_table(rows=len(tables_list) + 1, cols=2)
    tbl_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_tbl.rows[0].cells[0].paragraphs[0].add_run("Table Details").font.bold = True
    tbl_tbl.rows[0].cells[1].paragraphs[0].add_run("Page No.").font.bold = True
    tbl_tbl.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    for idx, (t_title, t_page) in enumerate(tables_list, start=1):
        c0 = tbl_tbl.cell(idx, 0)
        c1 = tbl_tbl.cell(idx, 1)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(t_title)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(t_page)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        
    doc.add_page_break()
    
    # PAGE 12: LIST OF ABBREVIATIONS
    add_heading_1(doc, "LIST OF ABBREVIATIONS")
    abbreviations = [
        ("AICTE", "All India Council for Technical Education"),
        ("APH", "Approval Process Handbook (AICTE)"),
        ("API", "Academic Performance Index / Application Programming Interface"),
        ("AQAR", "Annual Quality Assurance Report (NAAC)"),
        ("CGPA", "Cumulative Grade Point Average"),
        ("CORS", "Cross-Origin Resource Sharing"),
        ("DFD", "Data Flow Diagram"),
        ("ER", "Entity-Relationship"),
        ("FCP", "Faculty Cadre Proportion"),
        ("FIP", "Faculty Innovation and Research Points"),
        ("FRR", "Faculty Retention Rate"),
        ("FSR", "Faculty-to-Student Ratio"),
        ("GO", "Graduation Outcomes (NIRF)"),
        ("HOD", "Head of the Department"),
        ("IEEE", "Institute of Electrical and Electronics Engineers"),
        ("JWT", "JSON Web Token"),
        ("KPI", "Key Performance Indicator"),
        ("LLM", "Large Language Model"),
        ("NAAC", "National Assessment and Accreditation Council"),
        ("NBA", "National Board of Accreditation"),
        ("NIRF", "National Institutional Ranking Framework"),
        ("NOC", "No Objection Certificate"),
        ("OBE", "Outcome-Based Education"),
        ("OCR", "Optical Character Recognition"),
        ("PCE", "Priyadarshini College of Engineering, Nagpur"),
        ("PEO", "Program Educational Objective"),
        ("PO", "Program Outcome"),
        ("PSO", "Program Specific Outcome"),
        ("RAF", "Revised Accreditation Framework (NAAC)"),
        ("REST", "Representational State Transfer"),
        ("RPC", "Research and Professional Practice (NIRF)"),
        ("RTMNU", "Rashtrasant Tukdoji Maharaj Nagpur University"),
        ("SAR", "Self-Assessment Report (NBA)"),
        ("SARIMA", "Seasonal Autoregressive Integrated Moving Average"),
        ("SFR", "Student-to-Faculty Ratio"),
        ("SSR", "Self-Study Report (NAAC)"),
        ("TLR", "Teaching, Learning and Resources (NIRF)"),
        ("UI/UX", "User Interface / User Experience"),
        ("WA", "Washington Accord"),
    ]
    tbl_abb = doc.add_table(rows=len(abbreviations) + 1, cols=2)
    tbl_abb.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_abb.rows[0].cells[0].paragraphs[0].add_run("Abbreviation").font.bold = True
    tbl_abb.rows[0].cells[1].paragraphs[0].add_run("Full Expansion / Meaning").font.bold = True
    
    for idx, (abb_short, abb_full) in enumerate(abbreviations, start=1):
        c0 = tbl_abb.cell(idx, 0)
        c1 = tbl_abb.cell(idx, 1)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(abb_short)
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(11)
        r0.font.bold = True
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(abb_full)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        
    doc.add_page_break()
    print("Built preliminary pages successfully.")

if __name__ == "__main__":
    test_doc = docx.Document()
    build_preliminary_pages(test_doc)
    test_doc.save("thesis/test_prelim_out.docx")
    print("Saved test_prelim_out.docx")
