import fitz
import sys
import os

TEMPLATE_PDF = "thesis/Honors project Thesis Format .pdf"
TEMP_PDF = "thesis/temp_word.pdf"
FINAL_PDF = "thesis/Smart_Approval_AI_Final_Thesis.pdf"

def build_pdf():
    # 1. Open template
    tpl = fitz.open(TEMPLATE_PDF)
    print(f"Honors Template has {len(tpl)} pages.")
    
    # 2. Open converted Word doc PDF
    content = fitz.open(TEMP_PDF)
    print(f"Word generated PDF has {len(content)} pages.")
    
    # Find where Chapter 1 starts in content PDF
    ch1_idx = 8 # default 0-indexed page 8 (which is page 9)
    for i in range(len(content)):
        txt = content[i].get_text()
        if "CHAPTER 1: INTRODUCTION" in txt:
            ch1_idx = i
            print(f"Chapter 1 found on 0-indexed page {ch1_idx} (Page {ch1_idx + 1})")
            break
            
    # 3. Create merged master PDF
    out_pdf = fitz.open()
    
    # Insert exact 8 pages of template
    out_pdf.insert_pdf(tpl, from_page=0, to_page=len(tpl)-1)
    print(f"Inserted {len(tpl)} template pages.")
    
    # Insert technical chapters from ch1_idx to end
    out_pdf.insert_pdf(content, from_page=ch1_idx, to_page=len(content)-1)
    print(f"Inserted technical chapters from page {ch1_idx+1} to {len(content)}.")
    
    print(f"Total merged pages: {len(out_pdf)}")
    out_pdf.save(FINAL_PDF)
    print(f"Saved master PDF to: {FINAL_PDF}")

if __name__ == "__main__":
    build_pdf()
