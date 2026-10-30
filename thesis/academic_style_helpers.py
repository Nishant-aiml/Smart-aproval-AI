"""
Academic Styling Helpers for Smart Approval AI B.Tech Dissertation
Priyadarshini College of Engineering, Nagpur
Provides professional mathematical equation formatting using native OMML,
IEEE table styling, code blocks, algorithm boxes, and figure captions.
"""

import os
import re
from xml.sax.saxutils import escape
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

NAVY_BLUE = "1A365D"
LIGHT_GRAY_BG = "F8FAFC"
BORDER_GRAY = "CBD5E1"
WHITE = RGBColor(255, 255, 255)
DARK_TEXT = RGBColor(15, 23, 42)

def latex_to_omml(latex):
    """
    Converts LaTeX math expression into Office Math Markup Language (OMML) string.
    Supports:
    - \\frac{num}{den} -> vertical stacked fraction
    - X_{sub} or X_i -> native subscript
    - X^{sup} or X^2 -> native superscript
    - \\sum_{sub}^{sup} -> native summation operator
    - Greek symbols, operators (\\cdot, \\times, \\pm)
    - Grouping brackets \\left( \\right)
    """
    s = latex.strip()
    s = s.replace(r'\%', '%').replace(r'\quad', '    ').replace(r'\_', '###US###')
    s = s.replace(r'\|', '||')
    s = s.replace(r'\overline{S}', 'S_bar').replace(r'\tilde{\Phi}', 'Phi~').replace(r'\tilde{\Theta}', 'Theta~')
    s = s.replace(r'\Phi', 'Phi').replace(r'\Theta', 'Theta').replace(r'\varepsilon', 'epsilon')
    
    M_NS = 'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
    
    def parse_expr(expr):
        tokens = []
        i = 0
        while i < len(expr):
            # Check for \frac{...}{...}
            if expr[i:].startswith(r'\frac'):
                num_start = expr.find('{', i)
                num_end = find_matching(expr, num_start)
                den_start = expr.find('{', num_end + 1)
                den_end = find_matching(expr, den_start)
                
                num_content = expr[num_start+1:num_end]
                den_content = expr[den_start+1:den_end]
                
                num_omml = parse_expr(num_content)
                den_omml = parse_expr(den_content)
                
                tokens.append(f'<m:f><m:num>{num_omml}</m:num><m:den>{den_omml}</m:den></m:f>')
                i = den_end + 1
                continue
                
            # Check for \text{...} optionally followed by _{sub} or ^{sup}
            if expr[i:].startswith(r'\text'):
                t_start = expr.find('{', i)
                t_end = find_matching(expr, t_start)
                text_val = escape(expr[t_start+1:t_end])
                i = t_end + 1
                
                # Check for subscript on \text
                if i < len(expr) and expr[i] == '_':
                    i += 1
                    if i < len(expr) and expr[i] == '{':
                        b_end = find_matching(expr, i)
                        sub_omml = parse_expr(expr[i+1:b_end])
                        i = b_end + 1
                    elif i < len(expr):
                        sub_omml = parse_expr(expr[i])
                        i += 1
                    tokens.append(f'<m:sSub><m:e><m:r><m:rPr><m:nor/></m:rPr><m:t>{text_val}</m:t></m:r></m:e><m:sub>{sub_omml}</m:sub></m:sSub>')
                    continue
                    
                # Check for superscript on \text
                if i < len(expr) and expr[i] == '^':
                    i += 1
                    if i < len(expr) and expr[i] == '{':
                        b_end = find_matching(expr, i)
                        sup_omml = parse_expr(expr[i+1:b_end])
                        i = b_end + 1
                    elif i < len(expr):
                        sup_omml = parse_expr(expr[i])
                        i += 1
                    tokens.append(f'<m:sSup><m:e><m:r><m:rPr><m:nor/></m:rPr><m:t>{text_val}</m:t></m:r></m:e><m:sup>{sup_omml}</m:sup></m:sSup>')
                    continue
                    
                tokens.append(f'<m:r><m:rPr><m:nor/></m:rPr><m:t>{text_val}</m:t></m:r>')
                continue
                
            # Check for \sum
            if expr[i:].startswith(r'\sum'):
                i += 4
                sub_omml = ''
                sup_omml = ''
                if i < len(expr) and expr[i] == '_':
                    i += 1
                    if i < len(expr) and expr[i] == '{':
                        b_end = find_matching(expr, i)
                        sub_omml = parse_expr(expr[i+1:b_end])
                        i = b_end + 1
                    elif i < len(expr):
                        sub_omml = parse_expr(expr[i])
                        i += 1
                if i < len(expr) and expr[i] == '^':
                    i += 1
                    if i < len(expr) and expr[i] == '{':
                        b_end = find_matching(expr, i)
                        sup_omml = parse_expr(expr[i+1:b_end])
                        i = b_end + 1
                    elif i < len(expr):
                        sup_omml = parse_expr(expr[i])
                        i += 1
                tokens.append(f'<m:nary><m:naryPr><m:chr m:val="\u2211"/></m:naryPr><m:sub>{sub_omml}</m:sub><m:sup>{sup_omml}</m:sup><m:e></m:e></m:nary>')
                continue
                
            # Check for subscripts X_{sub} or X_i
            sub_m = re.match(r'^([A-Za-z0-9\(\)]+)_(\{([^{}]+)\}|([A-Za-z0-9]))', expr[i:])
            if sub_m:
                base = escape(sub_m.group(1))
                sub_val = escape(sub_m.group(3) if sub_m.group(3) is not None else sub_m.group(4))
                tokens.append(f'<m:sSub><m:e><m:r><m:t>{base}</m:t></m:r></m:e><m:sub><m:r><m:t>{sub_val}</m:t></m:r></m:sub></m:sSub>')
                i += len(sub_m.group(0))
                continue
                
            # Check for superscripts X^{sup} or X^2
            sup_m = re.match(r'^([A-Za-z0-9\(\)]+)\^(\{([^{}]+)\}|([A-Za-z0-9]))', expr[i:])
            if sup_m:
                base = escape(sup_m.group(1))
                sup_val = escape(sup_m.group(3) if sup_m.group(3) is not None else sup_m.group(4))
                tokens.append(f'<m:sSup><m:e><m:r><m:t>{base}</m:t></m:r></m:e><m:sup><m:r><m:t>{sup_val}</m:t></m:r></m:sup></m:sSup>')
                i += len(sup_m.group(0))
                continue
                
            # Check for operators
            if expr[i:].startswith(r'\cdot'):
                tokens.append('<m:r><m:t> \u22c5 </m:t></m:r>')
                i += 5
                continue
            if expr[i:].startswith(r'\times'):
                tokens.append('<m:r><m:t> x </m:t></m:r>')
                i += 6
                continue
            if expr[i:].startswith(r'\pm'):
                tokens.append('<m:r><m:t> +/- </m:t></m:r>')
                i += 3
                continue
            if expr[i:].startswith(r'\left('):
                tokens.append('<m:r><m:t>(</m:t></m:r>')
                i += 6
                continue
            if expr[i:].startswith(r'\right)'):
                tokens.append('<m:r><m:t>)</m:t></m:r>')
                i += 7
                continue
            if expr[i:].startswith(r'\left['):
                tokens.append('<m:r><m:t>[</m:t></m:r>')
                i += 6
                continue
            if expr[i:].startswith(r'\right]'):
                tokens.append('<m:r><m:t>]</m:t></m:r>')
                i += 7
                continue
            if expr[i:].startswith(r'\cos'):
                tokens.append('<m:r><m:t>cos</m:t></m:r>')
                i += 4
                continue
            if expr[i:].startswith(r'\sin'):
                tokens.append('<m:r><m:t>sin</m:t></m:r>')
                i += 4
                continue
                
            # Plain char
            ch = expr[i]
            if ch not in '{}':
                tokens.append(f'<m:r><m:t>{escape(ch)}</m:t></m:r>')
            i += 1
            
        return "".join(tokens)

    def find_matching(s_expr, open_idx):
        depth = 0
        for idx in range(open_idx, len(s_expr)):
            if s_expr[idx] == '{':
                depth += 1
            elif s_expr[idx] == '}':
                depth -= 1
                if depth == 0:
                    return idx
        return len(s_expr) - 1

    inner = parse_expr(s)
    return f'<m:oMath {M_NS}>{inner}</m:oMath>'

def add_equation(doc, eq_text, eq_number=""):
    """
    Renders an academic numbered equation using native Office Math Markup Language (OMML):
    - Borderless 2-column layout:
        Column 0 (5.5 in): Centered native OMML equation (<m:oMath>)
        Column 1 (1.0 in): Right-aligned equation number '(X.Y)' (Times New Roman, 11pt, Bold)
    """
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl._is_custom_block = True
    
    # Remove table borders
    tblPr = tbl._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>'
        f'<w:insideH w:val="none"/><w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)
    
    # Column 0: Equation cell
    c0 = tbl.cell(0, 0)
    c0.width = Inches(5.5)
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(4)
    p0.paragraph_format.space_after = Pt(4)
    
    try:
        omml_str = latex_to_omml(eq_text)
        omml_xml = parse_xml(omml_str)
        p0._p.append(omml_xml)
    except Exception as e:
        # Fallback to styled run if unexpected syntax
        r = p0.add_run(eq_text)
        r.font.name = "Cambria Math"
        r.font.size = Pt(11)
        r.font.italic = True
        r.font.color.rgb = DARK_TEXT
        
    # Column 1: Equation Number cell
    c1 = tbl.cell(0, 1)
    c1.width = Inches(1.0)
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_before = Pt(4)
    p1.paragraph_format.space_after = Pt(4)
    if eq_number:
        r1 = p1.add_run(f"({eq_number})")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = RGBColor(71, 85, 105)
        
    return tbl

def format_academic_table(tbl, col_widths=None):
    """
    Applies IEEE / Springer academic styling to a docx table:
    - Navy Blue header row with white bold text
    - Subtle alternating row shading
    - Clean cell padding and borders
    - Repeated header row on page split
    - cantSplit on rows
    """
    # Skip if custom algorithm, equation or code block
    if getattr(tbl, '_is_custom_block', False):
        return

    # Check if table is a borderless layout table (used for signatures / prelims)
    tblPr = tbl._tbl.tblPr
    tblBorders = tblPr.find(docx.oxml.ns.qn('w:tblBorders'))
    if tblBorders is not None:
        top_b = tblBorders.find(docx.oxml.ns.qn('w:top'))
        if top_b is not None and top_b.get(docx.oxml.ns.qn('w:val')) == 'none':
            return  # Skip borderless layout tables!

    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Apply column widths if provided
    if col_widths:
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                if idx < len(row.cells):
                    row.cells[idx].width = Inches(width)
                    
    # Format Header Row (Row 0)
    hdr_row = tbl.rows[0]
    trPr = hdr_row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    
    for cell in hdr_row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{NAVY_BLUE}"/>'))
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

def add_styled_figure(doc, img_path, caption_text, width_inches=5.4):
    """Adds a centered figure with keep_with_next to keep image and caption together"""
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(3)
        p_img.paragraph_format.keep_with_next = True
        p_img.add_run().add_picture(img_path, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(30, 41, 59)
    else:
        p_err = doc.add_paragraph(f"[Image Missing: {img_path}]")
        p_err.alignment = WD_ALIGN_PARAGRAPH.CENTER

def add_styled_algorithm(doc, alg_number, title, input_desc, output_desc, steps):
    """
    Renders an IEEE standard Algorithm box with:
    - Formal top/bottom 1.5pt rules (Navy Blue)
    - Algorithm number and title in header bar
    - Formatted Input and Output declarations
    - Monospace pseudocode with line numbers and standard ASCII operators (<-)
    """
    tbl = doc.add_table(rows=3, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl._is_custom_block = True
    
    # Apply IEEE top/bottom borders and subtle inside horizontal dividers
    tblPr = tbl._tbl.tblPr
    borders_xml = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="12" w:space="0" w:color="1A365D"/>'
        f'<w:bottom w:val="single" w:sz="12" w:space="0" w:color="1A365D"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders_xml)
    
    # Row 0: Title Header
    c0 = tbl.cell(0, 0)
    c0.width = Inches(6.5)
    trPr0 = tbl.rows[0]._tr.get_or_add_trPr()
    trPr0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    tcPr0 = c0._tc.get_or_add_tcPr()
    tcPr0.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>'))
    tcPr0.append(parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:left w:w="160" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tcMar>'))
    p0 = c0.paragraphs[0]
    p0.paragraph_format.keep_with_next = True
    p0.paragraph_format.space_before = Pt(4)
    p0.paragraph_format.space_after = Pt(4)
    r0 = p0.add_run(f"Algorithm {alg_number}: {title}")
    r0.font.name = "Times New Roman"
    r0.font.size = Pt(11)
    r0.font.bold = True
    r0.font.color.rgb = RGBColor(26, 54, 93)
    
    # Row 1: Input and Output
    c1 = tbl.cell(1, 0)
    c1.width = Inches(6.5)
    trPr1 = tbl.rows[1]._tr.get_or_add_trPr()
    trPr1.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    tcPr1 = c1._tc.get_or_add_tcPr()
    tcPr1.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>'))
    tcPr1.append(parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="100" w:type="dxa"/><w:bottom w:w="100" w:type="dxa"/><w:left w:w="160" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tcMar>'))
    p1 = c1.paragraphs[0]
    p1.paragraph_format.keep_with_next = True
    p1.paragraph_format.line_spacing = 1.25
    p1.paragraph_format.space_before = Pt(3)
    p1.paragraph_format.space_after = Pt(3)
    r_in = p1.add_run("Input: ")
    r_in.font.name = "Times New Roman"
    r_in.font.size = Pt(10)
    r_in.font.bold = True
    r_in.font.color.rgb = RGBColor(15, 23, 42)
    
    r_in_text = p1.add_run(f"{input_desc}\n")
    r_in_text.font.name = "Times New Roman"
    r_in_text.font.size = Pt(10)
    
    r_out = p1.add_run("Output: ")
    r_out.font.name = "Times New Roman"
    r_out.font.size = Pt(10)
    r_out.font.bold = True
    r_out.font.color.rgb = RGBColor(15, 23, 42)
    
    r_out_text = p1.add_run(output_desc)
    r_out_text.font.name = "Times New Roman"
    r_out_text.font.size = Pt(10)
    
    # Row 2: Algorithm Steps
    c2 = tbl.cell(2, 0)
    c2.width = Inches(6.5)
    trPr2 = tbl.rows[2]._tr.get_or_add_trPr()
    trPr2.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    tcPr2 = c2._tc.get_or_add_tcPr()
    tcPr2.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="FFFFFF"/>'))
    tcPr2.append(parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:left w:w="160" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tcMar>'))
    
    KEYWORDS = {"for", "each", "in", "do:", "if", "then:", "else", "else if", "end", "return", "Initialize", "empty"}
    for idx, (line_no, step_text) in enumerate(steps):
        # Sanitize arrows to <-
        clean_step = step_text.replace('\u2190', '<-').replace('<-', '<-')
        p_step = c2.paragraphs[0] if idx == 0 else c2.add_paragraph()
        if idx < len(steps) - 1:
            p_step.paragraph_format.keep_with_next = True
        p_step.paragraph_format.line_spacing = 1.15
        p_step.paragraph_format.space_before = Pt(1)
        p_step.paragraph_format.space_after = Pt(1)
        
        # Line number
        r_num = p_step.add_run(f"{line_no:>3s}:  ")
        r_num.font.name = "Consolas"
        r_num.font.size = Pt(9)
        r_num.font.bold = True
        r_num.font.color.rgb = RGBColor(100, 116, 139)
        
        # Indentation & tokens
        tokens = clean_step.split(" ")
        for t in tokens:
            r_t = p_step.add_run(t + " ")
            r_t.font.name = "Consolas"
            r_t.font.size = Pt(9)
            if t in KEYWORDS:
                r_t.font.bold = True
                r_t.font.color.rgb = RGBColor(26, 54, 93)
            else:
                r_t.font.color.rgb = RGBColor(15, 23, 42)
                
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(8)
    return tbl

def add_styled_code_listing(doc, listing_label, caption, code_str):
    """
    Renders an IEEE standard Code Listing with:
    - Bold caption header above the block
    - Container box with a 3pt navy left accent bar and light gray background
    - Monospace Consolas typography with clean line spacing
    """
    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.keep_with_next = True
    p_cap.paragraph_format.space_before = Pt(10)
    p_cap.paragraph_format.space_after = Pt(4)
    r_lbl = p_cap.add_run(f"Listing {listing_label}: ")
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(10.5)
    r_lbl.font.bold = True
    r_lbl.font.color.rgb = RGBColor(26, 54, 93)
    
    r_cap = p_cap.add_run(caption)
    r_cap.font.name = "Times New Roman"
    r_cap.font.size = Pt(10.5)
    r_cap.font.bold = True
    r_cap.font.color.rgb = RGBColor(15, 23, 42)
    
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl._is_custom_block = True
    
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    
    tblPr = tbl._tbl.tblPr
    borders_xml = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1A365D"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:insideH w:val="none"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders_xml)
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>'))
    tcPr.append(parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:left w:w="160" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tcMar>'))
    
    clean_code = code_str.replace('\u2190', '<-').replace('<-', '<-').replace('\u20b9', 'Rs. ')
    lines = clean_code.strip().split("\n")
    for idx, l in enumerate(lines):
        p_l = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p_l.paragraph_format.line_spacing = 1.15
        p_l.paragraph_format.space_before = Pt(0.5)
        p_l.paragraph_format.space_after = Pt(0.5)
        
        r_l = p_l.add_run(l)
        r_l.font.name = "Consolas"
        r_l.font.size = Pt(8.5)
        r_l.font.color.rgb = RGBColor(15, 23, 42)
        
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(10)
    return tbl
