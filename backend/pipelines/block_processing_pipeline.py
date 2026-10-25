"""
Block-Based Processing Pipeline - Docling + One-Shot Extraction
New optimized pipeline: PDF → Docling → OCR fallback → One-shot extraction → Quality → Metrics
"""

import logging
import uuid
import re
from typing import Dict, Any, List
from datetime import datetime

# Helper to strip emojis for Windows console/file compatibility
def strip_emojis(text: str) -> str:
    """Remove emoji characters that Windows charmap can't encode."""
    return re.sub(r'[\U00010000-\U0010ffff]', '', text)
from config.database import (
    get_db,
    Batch,
    Block,
    File,
    ComplianceFlag,
    ApprovalClassification,
    ApprovalRequiredDocument,
    close_db,
)
from services.docling_service import DoclingService
from services.ocr_service import OCRService
from services.one_shot_extraction import OneShotExtractionService
from services.block_quality import BlockQualityService
from services.block_sufficiency import BlockSufficiencyService
from services.kpi import KPIService
from services.compliance import ComplianceService
from services.trends import TrendService
from services.approval_classifier import classify_approval, calculate_readiness_score, get_required_documents, normalize_classification
from services.postprocess_mapping import (
    normalize_student_block,
    normalize_infrastructure_block,
    normalize_placement_block,
    fill_missing_from_evidence,
)
from config.information_blocks import get_information_blocks
from utils.id_generator import generate_block_id
import json

logger = logging.getLogger(__name__)

class BlockProcessingPipeline:
    """Optimized block-based processing pipeline with Docling and one-shot extraction"""
    
    def __init__(self):
        self.docling = DoclingService()
        self.ocr = OCRService()
        self.one_shot_extraction = OneShotExtractionService()
        self.block_quality = BlockQualityService()
        self.block_sufficiency = BlockSufficiencyService()
        self.kpi = KPIService()
        self.compliance = ComplianceService()
        self.trends = TrendService()
    
    @staticmethod
    def _resolve_filepath(filepath: str) -> str:
        """Resolve filepath correctly whether running from project root or backend folder."""
        import os
        if not filepath:
            return filepath
        if os.path.exists(filepath):
            return filepath
        cand1 = os.path.join("backend", filepath)
        if os.path.exists(cand1):
            return cand1
        if filepath.startswith("backend/") or filepath.startswith("backend\\"):
            cand2 = filepath[8:]
            if os.path.exists(cand2):
                return cand2
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cand3 = os.path.join(base, filepath)
        if os.path.exists(cand3):
            return cand3
        return filepath

    def process_batch(self, batch_id: str) -> Dict[str, Any]:
        """
        Main pipeline orchestrator
        Flow: PDF → Docling → OCR fallback → One-shot extraction → Quality → Sufficiency → KPIs → Compliance → Trends
        """
        logger.info(f"🚀 Starting OPTIMIZED pipeline for batch {batch_id}")
        db = get_db()
        
        try:
            # Get batch
            batch = db.query(Batch).filter(Batch.id == batch_id).first()
            if not batch:
                raise ValueError(f"Batch {batch_id} not found")
            
            mode = batch.mode
            new_university = bool(batch.new_university) if batch.new_university else False
            
            # Clean up existing records from prior runs for idempotency
            try:
                db.query(ApprovalClassification).filter(ApprovalClassification.batch_id == batch_id).delete()
                db.query(Block).filter(Block.batch_id == batch_id).delete()
                db.query(ComplianceFlag).filter(ComplianceFlag.batch_id == batch_id).delete()
                db.query(ApprovalRequiredDocument).filter(ApprovalRequiredDocument.batch_id == batch_id).delete()
                db.commit()
            except Exception as e_clean:
                logger.warning(f"Cleanup of prior batch records warning: {e_clean}")
                db.rollback()

            # Get files
            files = db.query(File).filter(File.batch_id == batch_id).all()
            logger.info(f"📄 Found {len(files)} files to process")
            
            if len(files) == 0:
                logger.warning(f"⚠️  No files found for batch {batch_id}")
                batch.status = "completed"
                db.commit()
                return {"status": "completed", "batch_id": batch_id, "message": "No files to process"}
            
            # Stage 1: Docling Structured Parsing
            batch.status = "docling_parsing"
            db.commit()
            logger.info(f"🔄 Stage 1: Extracting using Docling...")
            
            all_texts: List[str] = []
            all_tables: List[str] = []
            all_sections: List[Dict[str, Any]] = []
            # Simple map of page_number -> concatenated text (for evidence page detection)
            # For Excel/CSV: page_number = sheet_index (1-based)
            page_map: Dict[int, str] = {}
            # Map of filename -> file_type for evidence page mapping
            file_type_map: Dict[str, str] = {}
            # CSV/Excel mapped blocks (bypass LLM extraction)
            csv_excel_blocks: Dict[str, Dict[str, Any]] = {}
            
            for file in files:
                try:
                    resolved_path = self._resolve_filepath(file.filepath)
                    # Determine file type and use appropriate parser
                    from services.document_parser import parse_document, detect_file_type
                    
                    file_type = detect_file_type(resolved_path)
                    file_type_map[file.filename] = file_type
                    logger.info(f"📁 Processing: {file.filename} (type: {file_type})")
                    
                    full_text = ""
                    tables = ""
                    sections = []
                    
                    if file_type in ['xlsx', 'xls', 'csv', 'docx']:
                        # Use document_parser for non-PDF files
                        parsed = parse_document(resolved_path)
                        full_text = parsed.get("text", "")
                        
                        # For CSV/Excel: Try direct block mapping (bypasses LLM for structured data)
                        if file_type in ['xlsx', 'xls', 'csv']:
                            from services.csv_block_mapper import map_file
                            mapped_blocks = map_file(resolved_path, file_type, mode)
                            
                            for mapped_block in mapped_blocks:
                                block_type = mapped_block.get("block_type")
                                if block_type:
                                    # Store mapped block (will be merged with LLM results later)
                                    csv_excel_blocks[block_type] = {
                                        "data": mapped_block.get("data", {}),
                                        "confidence": mapped_block.get("confidence", 0.95),
                                        "source": mapped_block.get("source", file_type),
                                        "file_path": resolved_path
                                    }
                                    logger.info(f"✅ Direct mapped {file_type.upper()} to {block_type} block (confidence: {mapped_block.get('confidence', 0.95):.2f})")
                        
                        # Convert table data to markdown format for LLM context (for other blocks)
                        parsed_tables = parsed.get("tables", [])
                        for table in parsed_tables:
                            if isinstance(table, dict) and "data" in table:
                                sheet_name = table.get("sheet", table.get("table_index", "Table"))
                                columns = table.get("columns", [])
                                table_data = table.get("data", [])
                                
                                # Create markdown table
                                tables += f"\n=== {sheet_name} ===\n"
                                if columns:
                                    # Header row
                                    tables += "| " + " | ".join(str(c) for c in columns) + " |\n"
                                    tables += "| " + " | ".join(["---"] * len(columns)) + " |\n"
                                    # Data rows (limit to 100 for token efficiency)
                                    for row in table_data[:100]:
                                        if isinstance(row, dict):
                                            row_values = [str(row.get(col, "")) for col in columns]
                                            tables += "| " + " | ".join(row_values) + " |\n"
                                        else:
                                            tables += str(row) + "\n"
                                else:
                                    # Fallback: just stringify rows
                                    for row in table_data[:100]:
                                        tables += str(row) + "\n"
                        
                        logger.info(f"✅ Parsed {file_type.upper()}: {file.filename} ({len(full_text)} chars, {len(parsed_tables)} tables)")
                    else:
                        # Use Docling for PDF files (existing flow)
                        docling_result = self.docling.parse_pdf_to_structured_text(resolved_path)
                        
                        full_text = docling_result.get("full_text", "")
                        tables = docling_result.get("tables_text", "")
                        sections = docling_result.get("sections", [])
                        
                        # Check if text extraction was successful (500 chars threshold for meaningful content)
                        docling_text_length = len(full_text.strip()) if full_text else 0
                        if docling_text_length < 500:
                            logger.warning(f"⚠️  Docling returned sparse text ({docling_text_length} chars) for {file.filename}, triggering OCR fallback...")
                            
                            # Update status to ocr_fallback
                            batch.status = "ocr_fallback"
                            db.commit()
                            
                            # Use OCR fallback for this file
                            try:
                                from pdf2image import convert_from_path
                                images = convert_from_path(resolved_path)
                                ocr_text_parts = []
                                
                                for page_num, image in enumerate(images, 1):
                                    import tempfile
                                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                                        image.save(tmp.name)
                                        ocr_text = self.ocr.ocr_page(tmp.name)
                                        if ocr_text:
                                            ocr_text_parts.append(f"[Page {page_num}]\n{ocr_text}")
                                        from pathlib import Path
                                        Path(tmp.name).unlink()
                                
                                full_text = "\n\n".join(ocr_text_parts)
                                logger.info(f"✅ OCR extracted {len(full_text)} characters from {file.filename}")
                            except Exception as ocr_error:
                                logger.error(f"❌ OCR fallback failed: {ocr_error}")
                                full_text = ""
                    
                    if full_text:
                        # Add document type header for LLM context
                        doc_type_header = f"DOCUMENT_TYPE: {file_type.upper()}"
                        all_texts.append(f"\n\n--- {file.filename} ({doc_type_header}) ---\n\n{full_text}")
                        if tables:
                            all_tables.append(tables)
                        if sections:
                            all_sections.extend(sections)

                        # Build basic page → text aggregation from sections
                        for section in sections or []:
                            page = section.get("page", 1)
                            text = " ".join(section.get("content", []))
                            if not text:
                                continue
                            existing = page_map.get(page, "")
                            page_map[page] = (existing + " " + text).strip()
                        
                        # For Excel/CSV: map sheet index to page_map
                        if file_type in ['xlsx', 'xls', 'csv']:
                            # parsed is already available from above
                            parsed_tables = parsed.get("tables", [])
                            for sheet_idx, table in enumerate(parsed_tables, 1):
                                if isinstance(table, dict) and "data" in table:
                                    sheet_name = table.get("sheet", f"Sheet{sheet_idx}")
                                    # Convert table to text for page mapping
                                    table_text = f"Sheet: {sheet_name}\n"
                                    columns = table.get("columns", [])
                                    for row in table.get("data", [])[:20]:  # First 20 rows for mapping
                                        if isinstance(row, dict):
                                            row_text = " ".join(str(row.get(col, "")) for col in columns)
                                            table_text += row_text + " "
                                    existing = page_map.get(sheet_idx, "")
                                    page_map[sheet_idx] = (existing + " " + table_text).strip()

                        logger.info(f"✅ Processed: {file.filename} ({len(full_text)} chars)")
                    else:
                        logger.warning(f"⚠️  No text extracted from {file.filename}")
                
                except Exception as e:
                    logger.error(f"❌ Docling parsing error for {file.filename}: {e}")
                    import traceback
                    logger.error(traceback.format_exc())
            
            # Combine all text, tables, and sections into a single full-context string
            combined_text = "\n\n".join(all_texts)
            combined_tables = "\n\n".join(all_tables)

            sections_text_parts: List[str] = []
            for section in all_sections:
                title = section.get("title", "")
                content = " ".join(section.get("content", []))
                if title or content:
                    sections_text_parts.append(f"[SECTION] {title}\n{content}")
            sections_text = "\n\n".join(sections_text_parts)
            
            if not combined_text or len(combined_text.strip()) < 50:
                logger.error("❌ No text extracted from any file")
                batch.status = "failed"
                db.commit()
                return {"status": "failed", "batch_id": batch_id, "message": "No text extracted"}
            
            # Build full_context_text for LLM:
            # doc text + tables + structured sections
            parts: List[str] = []
            if combined_text:
                parts.append(combined_text)
            if combined_tables:
                parts.append("## TABLES_MARKDOWN ##\n\n" + combined_tables)
            if sections_text:
                parts.append("## STRUCTURED_SECTIONS ##\n\n" + sections_text)

            # Join and normalize whitespace; keep relative ordering (do not cut middle content)
            full_context_text = "\n\n".join(parts)
            full_context_text = "\n".join(line.rstrip() for line in full_context_text.splitlines())

            # Approximate token safety: if extremely long, keep last ~250k chars (tail-heavy, but keeps structure)
            max_chars = 250_000
            if len(full_context_text) > max_chars:
                full_context_text = full_context_text[-max_chars:]

            logger.info(f"✅ Full context length for LLM: {len(full_context_text)} characters")
            
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # DOCUMENT VALIDATION - Quick text length check only (skip slow forgery detection)
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            # Only reject if completely empty
            if len(full_context_text) < 50:
                logger.error(f"❌ Document text too short: {len(full_context_text)} chars < 50")
                batch.status = "invalid"
                batch.errors = ["Document text too short - upload complete PDF"]
                db.commit()
                return {
                    "status": "invalid",
                    "batch_id": batch_id,
                    "message": "Document Invalid — Text too short. Upload authentic or complete PDF"
                }
            
            logger.info("✅ Document passed validation checks (quick mode)")
            
            # Stage 2: Approval classification
            batch.status = "classify_approval"
            db.commit()
            logger.info("🔄 Stage 2: Classifying approval type from content...")
            
            # Classify - this now ALWAYS returns a dict
            classification_raw = classify_approval(full_context_text)
            
            # Normalize to ensure it's a dict (defensive)
            classification_dict = normalize_classification(classification_raw)
            
            # Ensure classification_dict is valid
            if not isinstance(classification_dict, dict):
                logger.error(f"❌ Classification normalization failed, got: {type(classification_dict)}")
                classification_dict = {
                    "category": "unknown",
                    "subtype": "unknown",
                    "confidence": 0.0,
                    "signals": ["Classification normalization failed"]
                }
            
            # Extract values safely
            category = classification_dict.get("category", "unknown")
            subtype = classification_dict.get("subtype", "unknown")
            confidence = classification_dict.get("confidence", 0.0)
            signals = classification_dict.get("signals", [])
            
            if not isinstance(signals, list):
                signals = []
            
            # Store classification for later stages (as dict)
            classification_result = classification_dict
            
            # Store in batch as dict
            batch.approval_classification = classification_dict
            
            # Upsert database record
            existing_c = db.query(ApprovalClassification).filter(ApprovalClassification.id == f"classify_{batch_id}").first()
            if existing_c:
                existing_c.category = category
                existing_c.subtype = subtype
                existing_c.signals = signals
            else:
                classification_record = ApprovalClassification(
                    id=f"classify_{batch_id}",
                    batch_id=batch_id,
                    category=category,
                    subtype=subtype,
                    signals=signals,
                )
                db.add(classification_record)
            db.commit()
            logger.info(f"✅ Classification: {category}/{subtype} (confidence: {confidence:.2f})")
            
            # Stage 3: One-Shot AI Extraction
            batch.status = "one_shot_extraction"
            db.commit()
            logger.info(f"🔄 Stage 3: One-shot AI extraction for all 10 blocks...")
            
            # Write debug to file since print from thread may not be visible
            with open("debug_extraction.log", "a", encoding="utf-8") as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"BATCH: {batch_id}\n")
                f.write(f"CONTEXT LENGTH: {len(full_context_text)} chars\n")
                f.write(f"CONTEXT PREVIEW: {strip_emojis(full_context_text[:200])}...\n")
            
            # Wrap extraction in try-catch to prevent pipeline from hanging
            try:
                logger.info(f"Calling one_shot_extraction.extract_all_blocks...")
                extraction_result = self.one_shot_extraction.extract_all_blocks(full_context_text, mode, new_university)
                extracted_blocks = extraction_result.get("blocks", {})
                extraction_confidence = extraction_result.get("confidence", 0.0)
                logger.info(f"Extraction completed successfully")
            except Exception as extraction_error:
                import traceback
                error_trace = traceback.format_exc()
                logger.error(f"❌ Extraction failed: {extraction_error}")
                logger.error(f"Stack trace: {error_trace}")
                
                # Write error to debug log
                with open("debug_extraction.log", "a", encoding="utf-8") as f:
                    f.write(f"EXTRACTION ERROR: {extraction_error}\n")
                    f.write(f"STACK TRACE: {error_trace}\n")
                
                # Use empty blocks as fallback so pipeline can continue
                extracted_blocks = {}
                extraction_confidence = 0.0
                logger.warning("Using empty blocks as fallback, pipeline will continue")
            
            # Count non-empty blocks and write to file
            non_empty = sum(1 for d in extracted_blocks.values() if d and isinstance(d, dict) and len(d) > 0)
            with open("debug_extraction.log", "a", encoding="utf-8") as f:
                f.write(f"EXTRACTED: {len(extracted_blocks)} blocks, {non_empty} non-empty\n")
                f.write(f"BLOCK KEYS: {list(extracted_blocks.keys())}\n")
                for k, v in extracted_blocks.items():
                    field_count = len(v) if isinstance(v, dict) else 0
                    f.write(f"  {k}: {field_count} fields\n")
                f.write(f"CONFIDENCE: {extraction_confidence}\n")
                f.write(f"{'='*60}\n")
            
            logger.info(f"✅ Extracted {len(extracted_blocks)} blocks with confidence {extraction_confidence:.2f}")


            
            # Merge CSV/Excel mapped blocks with LLM extracted blocks
            # CSV/Excel blocks take precedence (higher confidence, structured data)
            for block_type, csv_block in csv_excel_blocks.items():
                csv_data = csv_block.get("data", {})
                csv_conf = csv_block.get("confidence", 0.95)
                
                if csv_data:
                    # If LLM also extracted this block, merge (prefer CSV values for numeric fields)
                    if block_type in extracted_blocks:
                        llm_data = extracted_blocks[block_type] or {}
                        # Merge: prefer CSV numeric values, keep LLM text fields
                        for key, value in csv_data.items():
                            if "_num" in key or isinstance(value, (int, float)):
                                # Prefer CSV numeric values
                                llm_data[key] = value
                            elif key not in llm_data or not llm_data[key]:
                                # Use CSV value if LLM doesn't have it
                                llm_data[key] = value
                        extracted_blocks[block_type] = llm_data
                        logger.info(f"✅ Merged CSV/Excel {block_type} with LLM extraction")
                    else:
                        # CSV/Excel block not found by LLM, add it directly
                        extracted_blocks[block_type] = csv_data
                        logger.info(f"✅ Added CSV/Excel {block_type} block (not found by LLM)")
            
            # Post-processing: parse numeric fields and year fields
            from utils.parse_numeric import parse_numeric
            from utils.parse_year import parse_year
            
            logger.info(f"🔄 Post-processing: Parsing numeric and year fields + block normalization...")
            for block_type, block_data in extracted_blocks.items():
                if not isinstance(block_data, dict):
                    continue
                
                # Parse numeric fields and add _num variants
                # Comprehensive list of all numeric fields that need parsing
                numeric_fields = [
                    # Faculty
                    "faculty_count", "total_faculty", "phd_count", "assistant_professor", "associate_professor", "professor",
                    # Students
                    "student_count", "total_students", "total_intake", "admitted_students", "ug_enrollment", "pg_enrollment",
                    "male_students", "female_students",
                    # Infrastructure - Area fields (will be converted to sqm)
                    "built_up_area", "area", "total_area", "campus_area", "building_area",
                    "library_area", "lab_area", "hostel_area",
                    # Infrastructure - Count fields
                    "classrooms", "classroom_count", "number_of_classrooms", "total_classrooms",
                    "labs", "lab_count", "number_of_labs", "total_labs", "laboratories",
                    "computers", "computer_count", "digital_resources", "digital_library_resources",
                    "hostel_capacity", "hostel_rooms",
                    # Placement
                    "students_placed", "placed_students", "total_placements", "placement_count",
                    "students_eligible", "eligible_students",
                    "placement_rate", "placement_percentage",
                    "average_package", "avg_package", "average_salary", "avg_salary",
                    "highest_package", "max_package", "highest_salary", "max_salary",
                    # Fees
                    "annual_fee", "tuition_fee", "hostel_fee", "transport_fee", "semester_fee",
                    # Research
                    "publications", "publication_count", "patents", "patent_count",
                    "funded_projects", "projects", "citations", "citation_count",
                    # Other
                    "fsr_value", "committee_count", "present_committees"
                ]
                
                for field in numeric_fields:
                    if field in block_data:
                        raw_value = block_data[field]
                        if raw_value is not None and raw_value != "":
                            # Use parse_numeric which handles unit conversion
                            parsed_num = parse_numeric(str(raw_value))
                            if parsed_num is not None:
                                # For area fields, ensure we store as _sqm_num if it's an area field
                                if any(area_term in field.lower() for area_term in ["area", "sqft", "sqm", "acre", "hectare"]):
                                    # Store as both the original field_num and built_up_area_sqm_num if it's the main area field
                                    block_data[f"{field}_num"] = parsed_num
                                    if field in ["built_up_area", "area", "total_area", "campus_area", "building_area"]:
                                        block_data["built_up_area_sqm_num"] = parsed_num
                                else:
                                    block_data[f"{field}_num"] = parsed_num
                
                # Also parse any field ending with _num that might be a string
                for key, value in list(block_data.items()):
                    if key.endswith("_num") and isinstance(value, str):
                        parsed = parse_numeric(value)
                        if parsed is not None:
                            block_data[key] = parsed
                
                # Parse year fields
                year_fields = ["last_updated_year", "academic_year"]
                for field in year_fields:
                    if field in block_data:
                        raw_value = block_data[field]
                        if raw_value is not None and raw_value != "":
                            parsed_year = parse_year(str(raw_value))
                            if parsed_year:
                                block_data["parsed_year"] = parsed_year

                # Block-type specific normalizations (additive)
                if block_type == "student_enrollment_information":
                    normalize_student_block(block_data)
                elif block_type == "infrastructure_information":
                    normalize_infrastructure_block(block_data)
                elif block_type == "placement_information":
                    normalize_placement_block(block_data)
                
                # Evidence-based backfill for obvious missing fields
                fill_missing_from_evidence(block_type, block_data)
            
            # Stage 3: Store blocks in SQLite
            batch.status = "storing_blocks"
            db.commit()
            logger.info(f"🔄 Stage 3: Storing blocks...")
            
            required_blocks = get_information_blocks(mode, new_university)  # Get mode-specific blocks (conditional for UGC)
            stored_blocks = []
            # Initialize block_payloads_for_approval as empty dict - will be populated during block storage
            block_payloads_for_approval: Dict[str, Dict[str, Any]] = {}
            
            for block_type in required_blocks:
                block_data = extracted_blocks.get(block_type, {}) or {}

                # Skip completely empty blocks so they don't count as "present"
                if not block_data or (isinstance(block_data, dict) and len(block_data.keys()) == 0):
                    logger.info(f"⚠️  Skipping empty block data for {block_type}")
                    continue
                        
                # Choose a representative non-null primitive field for evidence lookup
                search_value = None
                if isinstance(block_data, dict):
                    for field_name, value in block_data.items():
                        if isinstance(value, (str, int, float)) and value not in (None, "", 0):
                            search_value = str(value)
                            break

                evidence_snippet = self._find_evidence_snippet(search_value, full_context_text)
                # Determine source file type by checking which file's content contains the evidence snippet
                source_file_type = "pdf"  # Default
                if evidence_snippet:
                    for file in files:
                        file_type = file_type_map.get(file.filename, "pdf")
                        # Check if snippet appears in this file's content (simple heuristic)
                        if file_type in ['xlsx', 'xls', 'csv', 'docx']:
                            # For Excel/CSV, check if snippet contains sheet/table markers
                            if any(marker in evidence_snippet.lower() for marker in ['sheet', 'row', 'column']):
                                source_file_type = file_type
                                break
                evidence_page = self._find_evidence_page(evidence_snippet, all_sections, page_map, source_file_type)
                
                # Calculate confidence using dynamic formula
                # Get expected field count for this block type
                from config.information_blocks import get_block_fields
                expected_fields = get_block_fields(block_type, mode)
                total_fields = len(expected_fields) if expected_fields else len(block_data)
                
                # Count non-null fields
                filled_fields = sum(
                    1 for v in block_data.values() 
                    if v not in [None, "", []] and str(v).lower() not in ["none", "null", "n/a", "na"]
                )
                non_null_ratio = filled_fields / max(total_fields, 1)
                
                # Get LLM confidence, with fallback based on non_null_ratio
                llm_conf = extraction_confidence
                if llm_conf is None:
                    llm_conf = 0.65 if non_null_ratio >= 0.60 else 0.40
                else:
                    llm_conf = float(llm_conf)
                
                # Final confidence: 60% non_null_ratio + 40% LLM confidence
                confidence = 0.6 * non_null_ratio + 0.4 * llm_conf
                
                # Clamp to [0, 1]
                confidence = min(1.0, max(0.0, confidence))
                improved_confidence = confidence

                # Attach evidence snippet into block data for downstream enrichment/backfill.
                # Overwrite to ensure the richest snippet is used.
                if evidence_snippet:
                    block_data["evidence"] = {
                        "snippet": evidence_snippet,
                        "page": evidence_page
                    }

                # Evidence-based backfill for obvious missing fields (after evidence is attached)
                fill_missing_from_evidence(block_type, block_data)
                
                # Backfill missing year from academic_year_start to prevent unwanted outdated flags
                from services.postprocess_mapping import backfill_missing_year
                backfill_missing_year(block_data)

                # Create block record
                block_id = generate_block_id()
                block = Block(
                    id=block_id,
                    batch_id=batch_id,
                    block_type=block_type,
                    data=block_data if isinstance(block_data, dict) else {},
                    confidence=improved_confidence,
                    extraction_confidence=extraction_confidence,
                    evidence_snippet=evidence_snippet,
                    evidence_page=evidence_page,
                    source_doc=files[0].filename if files else "unknown.pdf",
                    is_outdated=0,
                    is_low_quality=0,
                    is_invalid=0
                )
                
                db.add(block)
                stored_blocks.append(block)
                block_payloads_for_approval[block_type] = {
                    "data": block_data if isinstance(block_data, dict) else {},
                    "confidence": improved_confidence,
                    "evidence_snippet": evidence_snippet,
                }
                logger.info(f"✅ Stored: {block_type} (confidence: {improved_confidence:.2f})")
            
            db.commit()
            
            # Stage 4: Quality Checks
            batch.status = "quality_check"
            db.commit()
            logger.info(f"🔄 Stage 4: Quality checking blocks...")
            
            for block in stored_blocks:
                try:
                    # Recalculate completeness after post-processing
                    block_data = block.data or {}
                    if not isinstance(block_data, dict):
                        block_data = {}
                    
                    # Get required fields for completeness calculation
                    from config.information_blocks import get_block_fields
                    block_fields = get_block_fields(block.block_type, mode)
                    required_fields = block_fields.get("required_fields", []) if block_fields else []
                    total_required = len(required_fields) if required_fields else len(block_data)
                    
                    non_null_required = 0
                    for field in (required_fields if required_fields else block_data.keys()):
                        value = block_data.get(field)
                        if value is not None and value != "" and value != "null" and str(value).lower() not in ["none", "n/a", "na"]:
                            non_null_required += 1
                    
                    completeness_pct = (non_null_required / total_required) * 100 if total_required > 0 else 0
                    
                    block_dict = {
                        "extracted_data": block_data,
                        "extraction_confidence": block.extraction_confidence,
                        "confidence": block.confidence,
                        "evidence": [{
                            "snippet": block.evidence_snippet or "",
                            "page": block.evidence_page
                        }],
                        "block_type": block.block_type
                    }
                    
                    # Check quality (no AI calls - fast rule-based checks)
                    quality_result = self.block_quality.check_block_quality(block_dict, mode)
                    invalid_result = self.block_quality.check_invalid(block_dict, mode)  # No AI client needed
                    
                    block.is_outdated = 1 if quality_result.get("is_outdated", False) else 0
                    block.is_low_quality = 1 if quality_result.get("is_low_quality", False) else 0
                    block.is_invalid = 1 if invalid_result.get("is_invalid", False) else 0
                    
                    db.commit()
                except Exception as e:
                    logger.error(f"❌ Quality check error for block {block.id}: {e}")
            
            # Stage 5: Sufficiency - SOFT FAIL
            batch.status = "sufficiency"
            db.commit()
            logger.info(f"🔄 Stage 5: Calculating sufficiency...")
            
            try:
                blocks = db.query(Block).filter(Block.batch_id == batch_id).all()
                block_list = [self._block_to_dict(b) for b in blocks]
                sufficiency_result = self.block_sufficiency.calculate_sufficiency(mode, block_list)
                
                batch.sufficiency_result = sufficiency_result
                db.commit()
                logger.info(f"✅ Sufficiency: {sufficiency_result.get('percentage', 0):.2f}%")
            except Exception as suff_error:
                logger.error(f"❌ Sufficiency calculation failed: {suff_error}. Using default.")
                import traceback
                logger.error(traceback.format_exc())
                # SOFT FAIL: Use default sufficiency instead of crashing
                sufficiency_result = {
                    "percentage": 0,
                    "present_count": 0,
                    "required_count": 10,
                    "missing_blocks": [],
                    "penalty_breakdown": {}
                }
                batch.sufficiency_result = sufficiency_result
                db.commit()
            
            # Stage 6: KPI Scoring
            batch.status = "kpi_scoring"
            db.commit()
            logger.info(f"🔄 Stage 6: Calculating KPIs...")
            
            blocks = db.query(Block).filter(Block.batch_id == batch_id).all()
            block_list = [self._block_to_dict(b) for b in blocks]
            kpi_results = self.kpi.calculate_kpis(mode, blocks=block_list)
            
            batch.kpi_results = kpi_results
            db.commit()
            logger.info(f"✅ KPIs calculated: {len(kpi_results)} metrics")
            
            # Stage 6.5: Mark invalid batches (PRODUCTION GUARD)
            # Check if overall_score is 0/None or sufficiency is 0
            overall_score = None
            if isinstance(kpi_results, dict):
                overall_score_data = kpi_results.get("overall_score") or kpi_results.get("aicte_overall_score") or kpi_results.get("ugc_overall_score")
                if isinstance(overall_score_data, dict):
                    overall_score = overall_score_data.get("value")
                elif isinstance(overall_score_data, (int, float)):
                    overall_score = overall_score_data
            
            sufficiency_pct = sufficiency_result.get("percentage", 0) if isinstance(sufficiency_result, dict) else 0
            
            if (overall_score is None or overall_score == 0) or sufficiency_pct == 0:
                batch.is_invalid = 1
                logger.warning(f"Batch {batch_id} marked invalid: overall_score={overall_score}, sufficiency={sufficiency_pct}%")
                db.commit()
            
            # Stage 6.6: NBA-specific validation (MANDATORY for NBA mode)
            if mode.lower() == "nba":
                logger.info("🔄 Stage 6.6: NBA-specific validation...")
                from services.production_guard import ProductionGuard
                
                nba_valid, nba_reason = ProductionGuard.validate_nba_batch(batch, stored_blocks)
                if not nba_valid:
                    batch.is_invalid = 1
                    logger.warning(f"NBA_INVALID_BATCH_REASON: {batch_id} - {nba_reason}")
                    db.commit()
                else:
                    logger.info("✅ NBA batch validation passed")
            
            # Stage 7: Compliance
            
            # Stage 7: Compliance
            batch.status = "compliance"
            db.commit()
            logger.info(f"🔄 Stage 7: Checking compliance...")
            
            blocks = db.query(Block).filter(Block.batch_id == batch_id).all()
            block_list = [self._block_to_dict(b) for b in blocks]
            compliance_results = self.compliance.check_compliance(mode, blocks=block_list)
            
            # Store compliance flags
            existing_flags_count = db.query(ComplianceFlag).filter(ComplianceFlag.batch_id == batch_id).count()
            for idx, flag in enumerate(compliance_results):
                flag_id = f"flag_{batch_id}_{existing_flags_count + idx}"
                compliance_flag = ComplianceFlag(
                    id=flag_id,
                    batch_id=batch_id,
                    severity=flag.get("severity", "medium"),
                    title=flag.get("title", "Compliance Issue"),
                    reason=flag.get("reason", ""),
                    recommendation=flag.get("recommendation")
                )
                db.add(compliance_flag)
            
            batch.compliance_results = compliance_results
            db.commit()
            logger.info(f"✅ Compliance checked: {len(compliance_results)} flags")
            
            # Stage 8: Approval readiness
            batch.status = "approval_readiness"
            db.commit()
            logger.info("🔄 Stage 8: Computing approval readiness...")

            try:
                # CRITICAL: Ensure classification_result exists and is a dict
                # If classification_result was never set or is None, get from batch
                if classification_result is None:
                    logger.warning("⚠️  classification_result is None, loading from batch")
                    classification_result = batch.approval_classification or {}
                
                # Normalize to ensure it's a dict
                if not isinstance(classification_result, dict):
                    logger.warning(f"⚠️  classification_result is not a dict: {type(classification_result)}, normalizing")
                    classification_result = normalize_classification(classification_result)
                
                # If still not a dict after normalization, use fallback
                if not isinstance(classification_result, dict):
                    logger.error(f"❌ classification_result normalization failed: {type(classification_result)}, using fallback")
                    classification_result = {
                        "category": mode,  # Use batch mode as fallback
                        "subtype": "unknown",
                        "confidence": 0.0,
                        "signals": []
                    }
                
                # Final validation - ensure required keys exist
                if "category" not in classification_result:
                    classification_result["category"] = mode
                if "subtype" not in classification_result:
                    classification_result["subtype"] = "unknown"
                if "signals" not in classification_result or not isinstance(classification_result["signals"], list):
                    classification_result["signals"] = []
                if "confidence" not in classification_result:
                    classification_result["confidence"] = 0.0
                
                # Build present docs list and extracted data
                # block_payloads_for_approval is Dict[str, Dict] where key is block_type
                # Ensure it's a dict (defensive check)
                if not isinstance(block_payloads_for_approval, dict):
                    logger.error(f"❌ block_payloads_for_approval is not a dict: {type(block_payloads_for_approval)}")
                    block_payloads_for_approval = {}
                
                present_docs = list(block_payloads_for_approval.keys())  # Use block types as document identifiers
                extracted_data = {}
                for block_type, block_payload in block_payloads_for_approval.items():
                    # Ensure block_payload is a dict (defensive check)
                    if not isinstance(block_payload, dict):
                        logger.warning(f"⚠️  block_payload for {block_type} is not a dict: {type(block_payload)}, skipping")
                        continue
                    
                    block_data = block_payload.get("data", {})
                    if block_data and isinstance(block_data, dict):
                        extracted_data.update(block_data)
                
                # Calculate readiness - classification_result is now always a dict
                # Wrap in try-catch to catch any errors
                try:
                    readiness_result = calculate_readiness_score(
                        classification_result, present_docs, extracted_data
                    )
                except Exception as calc_error:
                    logger.error(f"❌ Error in calculate_readiness_score: {calc_error}")
                    import traceback
                    logger.error(traceback.format_exc())
                    # Create safe default using dict access
                    cat = classification_result.get("category", mode) if isinstance(classification_result, dict) else mode
                    sub = classification_result.get("subtype", "unknown") if isinstance(classification_result, dict) else "unknown"
                    conf = classification_result.get("confidence", 0.0) if isinstance(classification_result, dict) else 0.0
                    sigs = classification_result.get("signals", []) if isinstance(classification_result, dict) else []
                    readiness_result = {
                        "readiness_score": 0.0,
                        "required_documents": 0,
                        "present_documents": 0,
                        "missing_documents": [],
                        "classification": {
                            "category": cat,
                            "subtype": sub,
                            "confidence": conf,
                            "signals": sigs if isinstance(sigs, list) else []
                        }
                    }
                
                # Ensure readiness_result is a dict
                if not isinstance(readiness_result, dict):
                    logger.error(f"❌ readiness_result is not a dict: {type(readiness_result)}, value: {readiness_result}")
                    # Use dict access, not getattr
                    cat_fallback = classification_result.get("category", mode) if isinstance(classification_result, dict) else mode
                    sub_fallback = classification_result.get("subtype", "unknown") if isinstance(classification_result, dict) else "unknown"
                    readiness_result = {
                        "readiness_score": 0.0,
                        "required_documents": 0,
                        "present_documents": 0,
                        "missing_documents": [],
                        "classification": {
                            "category": cat_fallback,
                            "subtype": sub_fallback,
                            "confidence": 0.0,
                            "signals": []
                        }
                    }
                
                batch.approval_readiness = readiness_result
                
                # Get required docs for storing - wrap in try-catch
                try:
                    # Safely get category and subtype from dict
                    cat = classification_result.get("category", mode) if isinstance(classification_result, dict) else mode
                    sub = classification_result.get("subtype", "unknown") if isinstance(classification_result, dict) else "unknown"
                    
                    if not isinstance(cat, str):
                        cat = str(cat) if cat else mode
                    if not isinstance(sub, str):
                        sub = str(sub) if sub else "unknown"
                    
                    required_docs = get_required_documents(cat, sub)
                    
                    # Ensure required_docs is a list of dicts
                    if not isinstance(required_docs, list):
                        logger.error(f"❌ required_docs is not a list: {type(required_docs)}")
                        required_docs = []
                    
                    # Filter to only dict items
                    required_docs = [d for d in required_docs if isinstance(d, dict)]
                    
                    # Store required document records
                    for doc_row in required_docs:
                        try:
                            # Ensure doc_row is a dict (should be filtered above, but be safe)
                            if not isinstance(doc_row, dict):
                                continue
                            
                            doc_name = doc_row.get("name", "")
                            if not doc_name or not isinstance(doc_name, str):
                                continue
                            
                            # Check if this document is present (flexible matching)
                            present_docs_lower = [str(pd).lower() for pd in present_docs if pd is not None]
                            doc_name_lower = str(doc_name).lower()
                            
                            is_present = any(
                                doc_name_lower in pd or pd in doc_name_lower or
                                any(kw in pd for kw in doc_name_lower.split()) or
                                any(kw in doc_name_lower for kw in pd.split("_"))
                                for pd in present_docs_lower
                            )
                            
                            req_doc = ApprovalRequiredDocument(
                                id=str(uuid.uuid4()),
                                batch_id=batch_id,
                                category=cat,
                                required_key=doc_name,
                                present=1 if is_present else 0,
                                confidence=0.8 if is_present else 0.0,
                                evidence="",
                            )
                            db.add(req_doc)
                        except Exception as doc_error:
                            logger.warning(f"⚠️  Error storing doc_row: {doc_error}, skipping")
                            continue
                    
                    db.commit()
                    
                    # Safely get readiness score info
                    score = readiness_result.get('readiness_score', 0) if isinstance(readiness_result, dict) else 0
                    missing_list = readiness_result.get('missing_documents', []) if isinstance(readiness_result, dict) else []
                    missing_count = len(missing_list) if isinstance(missing_list, list) else 0
                    
                    logger.info(
                        f"✅ Approval readiness score: {score} "
                        f"Missing: {missing_count}"
                    )
                except Exception as store_error:
                    logger.error(f"❌ Error storing required documents: {store_error}")
                    import traceback
                    logger.error(traceback.format_exc())
                    # Continue anyway - we already set batch.approval_readiness
                    db.commit()
            except Exception as e:
                logger.error(f"❌ Approval readiness error: {e}")
                import traceback
                logger.error(traceback.format_exc())
                # Set a default readiness result to prevent pipeline failure
                # Safely extract classification info from dict
                try:
                    if isinstance(classification_result, dict):
                        cat = classification_result.get("category", mode)
                        sub = classification_result.get("subtype", "unknown")
                        conf = classification_result.get("confidence", 0.0)
                        sigs = classification_result.get("signals", [])
                        if not isinstance(sigs, list):
                            sigs = []
                    else:
                        # Fallback if classification_result is not a dict
                        logger.warning(f"⚠️  classification_result is not a dict in exception handler: {type(classification_result)}")
                        # Try to normalize it
                        normalized = normalize_classification(classification_result)
                        if isinstance(normalized, dict):
                            cat = normalized.get("category", mode)
                            sub = normalized.get("subtype", "unknown")
                            conf = normalized.get("confidence", 0.0)
                            sigs = normalized.get("signals", [])
                        else:
                            cat = mode
                            sub = "unknown"
                            conf = 0.0
                            sigs = []
                except Exception as ce:
                    logger.error(f"❌ Error extracting classification info: {ce}")
                    cat = mode
                    sub = "unknown"
                    conf = 0.0
                    sigs = []
                
                batch.approval_readiness = {
                    "readiness_score": 0,
                    "required_documents": 0,
                    "present_documents": 0,
                    "missing_documents": [],
                    "classification": {
                        "category": cat,
                        "subtype": sub,
                        "confidence": conf,
                        "signals": sigs
                    }
                }
                db.commit()
                logger.warning("⚠️  Continuing pipeline with default readiness score")
            
            # Stage 9: Trends (from Docling tables only)
            batch.status = "trend_analysis"
            db.commit()
            logger.info(f"🔄 Stage 9: Extracting trends from Docling tables...")
            
            # Extract trends from tables
            trend_results = self.trends.extract_trends_from_docling_tables(files, combined_tables, mode)
            batch.trend_results = trend_results
            db.commit()
            logger.info(f"✅ Trends extracted")
            
            # Stage 10: Extract and store institution name from blocks
            logger.info("🔄 Stage 10: Extracting institution name from blocks...")
            institution_name = None
            
            # Search for institution name in extracted blocks
            # Priority order: institution_info block, then any block with institution_name field
            name_keys = ["institution_name", "institute_name", "college_name", "name", "university_name"]
            
            for block in stored_blocks:
                if institution_name:
                    break
                block_data = block.data or {}
                if not isinstance(block_data, dict):
                    continue
                    
                for key in name_keys:
                    if key in block_data and block_data[key]:
                        candidate = str(block_data[key]).strip()
                        # Validate it looks like an institution name (at least 3 chars, not generic)
                        if len(candidate) >= 3 and candidate.lower() not in ["null", "none", "n/a", "na", "unknown"]:
                            institution_name = candidate
                            logger.info(f"✅ Institution name extracted: {institution_name}")
                            break
            
            # Fallback 1: Extract from document text header
            if not institution_name and full_context_text:
                first_lines = [line.strip() for line in full_context_text[:1500].splitlines() if line.strip()]
                for line in first_lines:
                    line_clean = re.sub(r'^[-\[\]\d\.\s#*]+', '', line).strip()
                    if any(term in line_clean.lower() for term in ["university", "college", "institute", "academy", "vidyapeeth", "engineering", "technology", "polytechnic"]):
                        if len(line_clean) >= 5 and not any(term in line_clean.lower() for term in ["report", "document", "evaluation", "affiliated"]):
                            institution_name = line_clean
                            logger.info(f"✅ Institution name extracted from header text: {institution_name}")
                            break
                        elif any(term in line_clean.lower() for term in ["evaluation report", "report"]):
                            parts = re.split(r'[-–—:]', line_clean)
                            if len(parts) > 1 and any(term in parts[-1].lower() for term in ["university", "college", "institute"]):
                                institution_name = parts[-1].strip()
                                logger.info(f"✅ Institution name extracted from title: {institution_name}")
                                break

            # Fallback 2: Gemini fast extraction
            if not institution_name and full_context_text:
                try:
                    from ai.gemini_client import GeminiClient
                    gemini = GeminiClient()
                    if gemini.available:
                        prompt_name = f"Extract only the educational institution or university name from this document text. Return only the name without extra text:\n\n{full_context_text[:1200]}"
                        extracted_by_ai = gemini.generate_text(prompt=prompt_name, temperature=0.1)
                        if extracted_by_ai and len(extracted_by_ai.strip()) >= 3 and len(extracted_by_ai.strip()) < 100:
                            institution_name = extracted_by_ai.strip().replace('"', '')
                            logger.info(f"✅ Institution name extracted by Gemini: {institution_name}")
                except Exception as e_name:
                    logger.debug(f"AI institution name extraction failed: {e_name}")

            # Update batch with extracted institution name
            if institution_name:
                batch.institution_name = institution_name
                if len(stored_blocks) > 0:
                    batch.is_invalid = 0
            else:
                if len(stored_blocks) == 0:
                    batch.is_invalid = 1
                    logger.warning(f"⚠️  Batch {batch_id} marked invalid: Institution name not found and 0 blocks extracted")
                else:
                    batch.institution_name = f"Institution ({batch_id[-8:]})"
            
            db.commit()
            
            # Complete
            batch.status = "completed"
            db.commit()
            logger.info(f"✅ Pipeline completed for batch {batch_id}")
            
            return {
                "status": "completed",
                "batch_id": batch_id,
                "sufficiency": sufficiency_result,
                "kpis": kpi_results,
                "compliance": compliance_results,
                "trends": trend_results
            }
            
        except Exception as e:
            logger.error(f"❌ Pipeline error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            batch.status = "failed"
            db.commit()
            raise
        finally:
            close_db(db)
    
    def _find_evidence_snippet(self, search_value: Any, full_text: str) -> str:
        """
        Find the best evidence snippet by searching for a representative field value.
        Prefers exact match, falls back to fuzzy match if needed.
        Returns a small window of text around the *best* match.
        """
        if not full_text or not isinstance(full_text, str):
            return ""
        
        if not search_value:
            return ""
        
        text = full_text
        text_lower = text.lower()

        if isinstance(search_value, (str, int, float)):
            needle = str(search_value).strip()
            if not needle:
                return ""
        
            needle_lower = needle.lower()
            
            # Prefer exact match first
            if needle in text:
                idx = text.index(needle)
                start = max(0, idx - 100)
                end = min(len(text), idx + len(needle) + 200)
                return text[start:end].strip()
            
            # Fallback: case-insensitive match
            if needle_lower in text_lower:
                idx = text_lower.index(needle_lower)
                start = max(0, idx - 100)
                end = min(len(text), idx + len(needle) + 200)
                return text[start:end].strip()
            
            # Fallback: fuzzy match - find best snippet with longest context
            best_snippet = ""
            best_len = 0
            start_idx = 0
            # Scan all occurrences and prefer the one with the longest
            # surrounding context (simple heuristic for "best" match).
            while True:
                idx = text_lower.find(needle_lower, start_idx)
                if idx == -1:
                    break
                start = max(0, idx - 200)
                end = min(len(text), idx + 200)
                candidate = text[start:end].strip()
                if len(candidate) > best_len:
                    best_len = len(candidate)
                    best_snippet = candidate
                start_idx = idx + len(needle_lower)

            if best_snippet:
                return best_snippet

        # Fallback: return first 200 characters
        return text[:200].strip()
    
    def _find_evidence_page(self, snippet: str, sections: List[Dict], page_map: Dict[int, str], file_type: str = "pdf") -> int:
        """
        Find evidence page for a given snippet using multiple strategies:
        1. Direct match in page_map
        2. Fuzzy / partial match in page_map
        3. Nearest section header match
        4. Fallback to page 1 (or sheet 1 for Excel/CSV)
        
        For Excel/CSV: page_map keys are sheet indices (1-based)
        For PDF: page_map keys are page numbers (1-based)
        """
        if not snippet or not page_map:
            return 1

        snippet_clean = snippet.strip().lower()
        if not snippet_clean:
            return 1

        # 1. Direct substring match inside page text
        for page_num, text in page_map.items():
            try:
                if snippet_clean in (text or "").lower():
                    return page_num
            except Exception:
                continue

        # 2. Fuzzy partial match - use first 30 chars of snippet
        prefix_30 = snippet_clean[:30]
        if prefix_30:
            for page_num, text in page_map.items():
                try:
                    if prefix_30 in (text or "").lower():
                        return page_num
                except Exception:
                    continue

        # 3. Check nearest section header / text (only for PDF)
        if file_type == "pdf":
            prefix_20 = snippet_clean[:20]
            if prefix_20:
                for section in sections or []:
                    section_text = section.get("text") or " ".join(section.get("content", [])) or ""
                    if prefix_20 in section_text.lower():
                        return section.get("page", 1) or 1

        # 4. Final fallback
        # For Excel/CSV, return sheet 1; for PDF, return page 1
        return 1
    
    def _block_to_dict(self, block: Block) -> Dict[str, Any]:
        """Convert SQLite Block to dict"""
        return {
            "block_id": block.id,
            "batch_id": block.batch_id,
            "block_type": block.block_type,
            "extracted_data": block.data or {},
            "extraction_confidence": block.extraction_confidence,
            "confidence": block.confidence,
            "evidence": [{
                "snippet": block.evidence_snippet or "",
                "page": block.evidence_page
            }],
            "is_outdated": bool(block.is_outdated),
            "is_low_quality": bool(block.is_low_quality),
            "is_invalid": bool(block.is_invalid),
            "source_doc": block.source_doc
                }
