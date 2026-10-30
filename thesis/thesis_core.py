"""
Smart Approval AI - Full Thesis Document Generator
Institution: Priyadarshini College of Engineering, Nagpur
Department of Information Technology (Session 2026-2027)
Degree: Bachelor of Technology (Honors) in Information Technology
Target Length: ~100 Pages in IEEE / PCE Institutional Format
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

OUTPUT_PATH = "thesis/Smart_Approval_AI_Final_Thesis.docx"

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def add_page_border(section):
    border_xml = parse_xml(
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
        f'<w:top w:val="single" w:color="000000" w:sz="18" w:space="24"/>'
        f'<w:left w:val="single" w:color="000000" w:sz="18" w:space="24"/>'
        f'<w:bottom w:val="single" w:color="000000" w:sz="18" w:space="24"/>'
        f'<w:right w:val="single" w:color="000000" w:sz="18" w:space="24"/>'
        f'</w:pgBorders>'
    )
    section._sectPr.append(border_xml)

def add_page_number_to_run(run):
    fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>')
    fldChar3 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def add_header_footer(section, is_front_matter=False, roman_numeral=None):
    add_page_border(section)
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.text = ""
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)
    if is_front_matter:
        if roman_numeral:
            run.text = roman_numeral
    else:
        add_page_number_to_run(run)

print("Thesis generator core loaded successfully.")
