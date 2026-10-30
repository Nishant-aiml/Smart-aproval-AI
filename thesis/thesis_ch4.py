import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from thesis_prelim import add_paragraph, add_heading_1, add_heading_2, add_heading_3

def build_chapter_4(doc):
    add_heading_1(doc, "CHAPTER 4: SOFTWARE/HARDWARE REQUIRED (OPTIONAL CHAPTER)")
    
    # 4.1 HARDWARE SPECIFICATIONS
    add_heading_2(doc, "4.1 HARDWARE REQUIREMENTS AND DEPLOYMENT INFRASTRUCTURE")
    
    p1 = (
        "The computational architecture of Smart Approval AI is deliberately engineered for resource efficiency, enabling it to execute seamlessly "
        "across standard academic workstations, dedicated campus servers, and modern containerized cloud platforms. Because compute-heavy multimodal "
        "large language model inference is offloaded asynchronously to Google Gemini 2.5 Flash cloud infrastructure via high-speed API connections, the "
        "local institutional host primarily requires sufficient memory and processor throughput to execute Docling visual layout parsing, PyMuPDF "
        "vector extraction, SQLite/PostgreSQL transactional queries, and Next.js server-side rendering (SSR)."
    )
    add_paragraph(doc, p1)
    
    p2 = (
        "Table 4.1 delineates the minimum and recommended hardware specifications for single-workstation development environments and high-capacity "
        "institutional enterprise servers:"
    )
    add_paragraph(doc, p2)
    
    # Table 4.1: Hardware Specs
    add_paragraph(doc, "Table 4.1: Recommended Hardware Specifications for Local Workstation & Institutional Campus Server", font_size=11, bold=True, italic=True, space_after=4)
    tbl_hw = doc.add_table(rows=6, cols=3)
    tbl_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    hw_specs = [
        ("Hardware Component", "Minimum Developer Workstation", "Recommended Enterprise Campus Server"),
        ("Central Processing Unit (CPU)", "Intel Core i5 / AMD Ryzen 5 (4 Cores, 2.5 GHz+)", "Intel Xeon E5 / AMD EPYC (8+ Cores, 3.2 GHz+)"),
        ("System Memory (RAM)", "8 GB DDR4 RAM", "32 GB DDR4 / DDR5 ECC RAM"),
        ("Primary Disk Storage", "256 GB NVMe M.2 Solid State Drive (SSD)", "1 TB Enterprise NVMe SSD in RAID-1 Configuration"),
        ("Network Interface Card (NIC)", "100 Mbps Ethernet / 802.11ac Wi-Fi", "1 Gbps Full-Duplex Redundant Gigabit Ethernet"),
        ("Display / Client Terminal", "1920 × 1080 (Full HD) 60 Hz Resolution", "Dual 1920 × 1080 Full HD Monitors for Auditor Scrutiny"),
    ]
    for r_idx, row in enumerate(hw_specs):
        for c_idx, val in enumerate(row):
            cell = tbl_hw.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(10)
            if r_idx == 0:
                run.font.bold = True
                
    # 4.2 SOFTWARE TECHNOLOGY STACK
    add_heading_2(doc, "4.2 SOFTWARE TECHNOLOGY STACK AND DEPENDENCIES")
    
    p3 = (
        "The software architecture leverages an enterprise-grade open-source technology stack, selected for high concurrency, type safety, modularity, "
        "and long-term community support. Table 4.2 provides an exhaustive inventory of all core software dependencies across the full-stack architecture:"
    )
    add_paragraph(doc, p3)
    
    # Table 4.2: Software stack
    add_paragraph(doc, "Table 4.2: Comprehensive Software Technology Stack, Versions, and Functional Responsibilities", font_size=11, bold=True, italic=True, space_after=4)
    tbl_sw = doc.add_table(rows=11, cols=4)
    tbl_sw.alignment = WD_TABLE_ALIGNMENT.CENTER
    sw_data = [
        ("Layer", "Technology / Library", "Version", "Functional Role in Smart Approval AI"),
        ("Backend Web Core", "FastAPI / Starlette", "0.104.1", "Asynchronous REST API framework, dependency injection, routing"),
        ("ASGI Server", "Uvicorn", "0.24.0", "High-performance Lightning-fast ASGI web server worker"),
        ("Language Runtime", "Python", "3.11 / 3.12", "Underlying programming language runtime and type system"),
        ("Data Validation", "Pydantic v2", "2.14.1", "Strict data contract enforcement, JSON Schema generation"),
        ("Database ORM", "SQLAlchemy", "2.0.44", "Relational database mapping, connection pooling, schema migrations"),
        ("Frontend Web Core", "Next.js 14 (App Router)", "14.2.33", "Server-Side Rendering (SSR), React 18, relative API rewrites"),
        ("UI Styling & Icons", "Tailwind CSS + Lucide", "3.4.1", "Modern utility-first responsive styling and SVG iconography"),
        ("Cognitive AI Engine", "Google Gemini 2.5 Flash", "v0.8.6 SDK", "Multimodal regulatory reasoning, table parsing, structured JSON"),
        ("Document Deep Parser", "Docling + PyMuPDF", "2.14 / 2.0", "Layout segmentation, bounding box detection, table grid recovery"),
        ("Network Tunneling", "Ngrok", "v3.18", "Single-tunnel reverse-proxy external port exposure (:4051/:3051)"),
    ]
    for r_idx, row in enumerate(sw_data):
        for c_idx, val in enumerate(row):
            cell = tbl_sw.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                
    # 4.3 DATABASE SCHEMA AND ER DESIGN
    add_heading_2(doc, "4.3 DATABASE SCHEMA DESIGN AND ENTITY-RELATIONSHIP ARCHITECTURE")
    
    p4 = (
        "Persistent data storage is orchestrated through a normalized relational database schema engineered with strict referential integrity, "
        "foreign key constraints, and performance indexes. The database accommodates both high-frequency batch document ingestions and complex "
        "longitudinal queries spanning multiple academic years."
    )
    add_paragraph(doc, p4)
    
    p5 = (
        "Figure 4.1 illustrates the comprehensive Entity-Relationship (ER) Schema Diagram, detailing the core tables: `Institutions`, `Batches`, "
        "`Documents`, `KPI_Metrics`, `NBA_Criteria_Eval`, `Compliance_Audits`, and `Users`."
    )
    add_paragraph(doc, p5)
    
    # Embed Figure 4.1: ER Diagram
    p_fig41 = doc.add_paragraph()
    p_fig41.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fig41.paragraph_format.space_before = Pt(8)
    p_fig41.paragraph_format.space_after = Pt(4)
    er_img_path = "thesis/images/fig_er_diagram.png"
    if os.path.exists(er_img_path):
        p_fig41.add_run().add_picture(er_img_path, width=Inches(6.0))
    add_paragraph(doc, "Figure 4.1: Comprehensive Entity-Relationship (ER) Schema Diagram of Database", font_size=10, italic=True, alignment=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    
    p6 = (
        "Table 4.3 details the data dictionary for the primary relational entities, specifying field names, data types, nullability, and relational constraints:"
    )
    add_paragraph(doc, p6)
    
    # Table 4.3: Data Dictionary
    add_paragraph(doc, "Table 4.3: Relational Database Schema Data Dictionary and Integrity Constraints", font_size=11, bold=True, italic=True, space_after=4)
    tbl_dd = doc.add_table(rows=8, cols=5)
    tbl_dd.alignment = WD_TABLE_ALIGNMENT.CENTER
    dd_data = [
        ("Table Name", "Column Name", "Data Type", "Constraints", "Description"),
        ("Institutions", "id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique surrogate key for engineering college"),
        ("Institutions", "aicte_permanent_id", "VARCHAR(64)", "UNIQUE, NOT NULL", "Statutory AICTE permanent institute identifier"),
        ("Batches", "id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique identifier for uploaded audit batch"),
        ("Batches", "academic_year", "VARCHAR(16)", "NOT NULL, INDEXED", "Academic session string (e.g. '2026-2027')"),
        ("KPI_Metrics", "metric_name", "VARCHAR(128)", "NOT NULL, INDEXED", "Codified regulatory indicator (e.g. 'SFR', 'FCP')"),
        ("KPI_Metrics", "compliance_status", "VARCHAR(32)", "NOT NULL", "Verdict: 'COMPLIANT', 'DEFICIENT', 'EXCELLENT'"),
        ("Compliance_Audits", "digital_signature", "VARCHAR(255)", "NOT NULL", "Cryptographic SHA-256 verification token"),
    ]
    for r_idx, row in enumerate(dd_data):
        for c_idx, val in enumerate(row):
            cell = tbl_dd.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                
    # 4.4 API SPECIFICATIONS
    add_heading_2(doc, "4.4 API SPECIFICATIONS AND CLIENT-SERVER ARCHITECTURE")
    
    p7 = (
        "Communication between the Next.js presentation tier and the FastAPI computation tier is mediated through a strictly typed RESTful API. "
        "Table 4.4 details the primary endpoint contracts, supported HTTP verbs, payload formats, and authentication modes:"
    )
    add_paragraph(doc, p7)
    
    # Table 4.4: API Specs
    add_paragraph(doc, "Table 4.4: Primary RESTful API Endpoint Contracts, Payloads, and Authentication Modes", font_size=11, bold=True, italic=True, space_after=4)
    tbl_api = doc.add_table(rows=8, cols=5)
    tbl_api.alignment = WD_TABLE_ALIGNMENT.CENTER
    api_data = [
        ("Endpoint Route", "HTTP Verb", "Authentication", "Request Payload", "Response Object"),
        ("/api/upload", "POST", "Bearer JWT", "multipart/form-data (PDF file)", "JSON: batch_id, file_hash, parsing_status"),
        ("/api/batches", "GET", "Bearer JWT", "Query: limit, offset, status", "JSON: Array of BatchSummary objects"),
        ("/api/evaluate/aicte", "POST", "Bearer JWT", "JSON: batch_id, aicte_norm_year", "JSON: AICTEComplianceReport with deficiencies"),
        ("/api/evaluate/nba", "POST", "Bearer JWT", "JSON: batch_id, tier_type", "JSON: NBACriteriaBreakdown with 1000-pt score"),
        ("/api/analytics/trends", "GET", "Bearer JWT", "Query: institution_id, years_range", "JSON: LongitudinalSeries for 48 indicators"),
        ("/api/forecast", "POST", "Bearer JWT", "JSON: metric_name, horizon_years", "JSON: PointForecast, confidence_interval_95"),
        ("/api/reports/download", "GET", "Bearer JWT", "Query: batch_id, format (pdf/docx)", "Binary Stream: Cryptographically signed report"),
    ]
    for r_idx, row in enumerate(api_data):
        for c_idx, val in enumerate(row):
            cell = tbl_api.cell(r_idx, c_idx)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(val)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                
    doc.add_page_break()
    print("Built Chapter 4 successfully.")

if __name__ == "__main__":
    test_doc = docx.Document()
    build_chapter_4(test_doc)
    test_doc.save("thesis/test_ch4_out.docx")
    print("Saved test_ch4_out.docx")
