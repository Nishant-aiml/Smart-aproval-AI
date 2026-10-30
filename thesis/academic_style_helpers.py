"""
Academic Styling Helpers for Smart Approval AI B.Tech Dissertation
Priyadarshini College of Engineering, Nagpur
Provides professional mathematical equation formatting, IEEE table styling,
code blocks, and figure captions.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

NAVY_BLUE = "1A365D"
LIGHT_GRAY_BG = "F8FAFC"
BORDER_GRAY = "CBD5E1"
WHITE = RGBColor(255, 255, 255)
DARK_TEXT = RGBColor(15, 23, 42)

def add_equation(doc, eq_text, eq_number=""):
    """
    Renders an academic numbered equation with:
    - Centered mathematical notation (Cambria Math, 11pt, Italic)
    - Right-aligned equation number (Times New Roman, 11pt, Bold)
    - Clean paragraph spacing
    """
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    
    # Configure tab stops: 3.25 inches center, 6.5 inches right
    p.paragraph_format.tab_stops.add_tab_stop(Inches(3.25), WD_TAB_ALIGNMENT.CENTER)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT)
    
    # Add Equation
    r_eq = p.add_run(f"\t{eq_text}")
    r_eq.font.name = "Cambria Math"
    r_eq.font.size = Pt(11)
    r_eq.font.italic = True
    r_eq.font.color.rgb = DARK_TEXT
    
    # Add Equation Number
    if eq_number:
        r_num = p.add_run(f"\t({eq_number})")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(11)
        r_num.font.bold = True
        r_num.font.color.rgb = RGBColor(71, 85, 105)
    return p

def format_academic_table(tbl, col_widths=None):
    """
    Applies IEEE / Springer academic styling to a docx table:
    - Navy Blue header row with white bold text
    - Subtle alternating row shading
    - Clean cell padding and borders
    - Repeated header row on page split
    - cantSplit on rows
    """
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Apply column widths if provided
    if col_widths:
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                if idx < len(row.cells):
                    row.cells[idx].width = Inches(width)
                    
    # Format Header Row (Row 0)
    hdr_row = tbl.rows[0]
    # Set cantSplit and tblHeader
    trPr = hdr_row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    
    for cell in hdr_row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        # Navy blue fill
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{NAVY_BLUE}"/>'))
        # Internal margins / padding
        tcPr.append(parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>'))
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(10)
                r.font.bold = True
                r.font.color.rgb = WHITE
                
    # Format Data Rows (Row 1 onwards)
    for r_idx, row in enumerate(tbl.rows[1:], start=1):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        # Alternate row background
        is_even = (r_idx % 2 == 0)
        bg_color = LIGHT_GRAY_BG if is_even else "FFFFFF"
        
        for c_idx, cell in enumerate(row.cells):
            tcPr = cell._tc.get_or_add_tcPr()
            if bg_color != "FFFFFF":
                tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>'))
            tcPr.append(parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="100" w:type="dxa"/><w:bottom w:w="100" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar>'))
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.5)
                    
    # Subtle clean borders across table
    tblPr = tbl._tbl.tblPr
    borders_xml = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{NAVY_BLUE}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{NAVY_BLUE}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{BORDER_GRAY}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders_xml)

def add_styled_figure(doc, img_path, caption_text, width_inches=5.8):
    """Adds a centered high-resolution figure with professional academic caption"""
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(30, 41, 59)
    else:
        p_err = doc.add_paragraph(f"[Image Missing: {img_path}]")
        p_err.alignment = WD_ALIGN_PARAGRAPH.CENTER
