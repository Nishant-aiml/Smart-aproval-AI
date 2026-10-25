"""
Report generation router - SQLite version
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Optional
from schemas.reports import ReportGenerateRequest, ReportGenerateResponse
from services.report_generator import ReportGenerator
from config.database import get_db, Batch, close_db
from config.settings import settings
from middleware.auth_middleware import get_current_user
from datetime import datetime
import os

router = APIRouter()
report_generator = ReportGenerator()

@router.post("/generate", response_model=ReportGenerateResponse)
def generate_report(
    request: ReportGenerateRequest,
    user: Optional[dict] = Depends(get_current_user)
):
    """
    Generate PDF report for a batch.
    PLATFORM MODEL: Only real batches - no demo mode.
    Includes evidence summary, scores, compliance, gaps, recommendations.
    """
    db = get_db()
    
    try:
        batch = db.query(Batch).filter(Batch.id == request.batch_id).first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")

        
        # PLATFORM MODEL: Enforce user access control (skip for system batches)
        is_system_batch = getattr(batch, 'data_source', 'user') == 'system'
        if user and not is_system_batch:
            user_id = user.get("uid")
            role = user.get("role", "department")
            
            if role != "institution":
                department_id = user.get("department_id")
                if department_id:
                    if batch.department_id != department_id:
                        raise HTTPException(status_code=403, detail="Access denied")
                elif user_id:
                    if batch.user_id != user_id:
                        raise HTTPException(status_code=403, detail="Access denied")
        
        # INVALID BATCH ENFORCEMENT
        if batch.is_invalid == 1:
            raise HTTPException(
                status_code=400,
                detail="Cannot generate report for invalid batch"
            )
        
        if batch.status != "completed":
            raise HTTPException(status_code=400, detail="Batch processing not completed")
        
        # Generate report
        report_path = report_generator.generate_report(
            request.batch_id,
            include_evidence=request.include_evidence if hasattr(request, 'include_evidence') else True,
            include_trends=request.include_trends if hasattr(request, 'include_trends') else False,
            report_type=request.report_type if hasattr(request, 'report_type') else "full",
        )
        
        download_url = f"/api/reports/download/{request.batch_id}"
        
        return ReportGenerateResponse(
            batch_id=request.batch_id,
            report_path=report_path,
            download_url=download_url,
            generated_at=datetime.utcnow().isoformat()
        )
    finally:
        close_db(db)

@router.get("/download/{batch_id}")
def download_report(
    batch_id: str,
    user: Optional[dict] = Depends(get_current_user)
):
    """Download generated report - supports demo batches with sample reports"""
    
    # DEMO MODE: Return sample report for demo batches
    if batch_id.startswith("demo-"):
        # Generate a simple demo HTML report
        demo_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AICTE Accreditation Report - Demo</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #0D9488; border-bottom: 3px solid #0D9488; padding-bottom: 10px; }}
        h2 {{ color: #374151; margin-top: 30px; }}
        .score-card {{ background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%); padding: 20px; border-radius: 12px; margin: 20px 0; }}
        .score {{ font-size: 48px; font-weight: bold; color: #0D9488; }}
        .label {{ color: #6B7280; font-size: 14px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0; }}
        .kpi-item {{ background: white; padding: 15px; border-radius: 8px; border: 1px solid #E5E7EB; }}
        .kpi-name {{ font-weight: 600; color: #374151; }}
        .kpi-value {{ font-size: 24px; font-weight: bold; color: #0D9488; }}
        .compliance {{ background: #FEF3C7; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #F59E0B; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #E5E7EB; color: #9CA3AF; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>🎓 AICTE Accreditation Report</h1>
    <p><strong>Batch ID:</strong> {batch_id}</p>
    <p><strong>Institution:</strong> {"IIT Delhi - CSE Department" if "2024" in batch_id else "NIT Trichy - ECE Department"}</p>
    <p><strong>Generated:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
    
    <div class="score-card">
        <div class="label">OVERALL ACCREDITATION SCORE</div>
        <div class="score">84.5 / 100</div>
        <p>✅ Recommended for Accreditation</p>
    </div>
    
    <h2>📊 KPI Summary</h2>
    <div class="kpi-grid">
        <div class="kpi-item">
            <div class="kpi-name">Faculty-Student Ratio (FSR)</div>
            <div class="kpi-value">78.5</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-name">Infrastructure Score</div>
            <div class="kpi-value">82.3</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-name">Placement Index</div>
            <div class="kpi-value">92.1</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-name">Lab Compliance</div>
            <div class="kpi-value">88.7</div>
        </div>
    </div>
    
    <h2>⚠️ Compliance Issues</h2>
    <div class="compliance">
        <strong>Minor Issues (2 found):</strong>
        <ul>
            <li>Library book count slightly below AICTE norms</li>
            <li>Faculty qualification documentation incomplete</li>
        </ul>
    </div>
    
    <h2>✅ Strengths</h2>
    <ul>
        <li>Excellent placement record (92% placement rate)</li>
        <li>Strong industry partnerships</li>
        <li>Well-equipped laboratories</li>
        <li>Research output above national average</li>
    </ul>
    
    <h2>📈 Recommendations</h2>
    <ul>
        <li>Increase library resources to meet AICTE norms</li>
        <li>Complete faculty qualification documentation</li>
        <li>Consider infrastructure expansion for growing intake</li>
    </ul>
    
    <div class="footer">
        <p>This is a demo report generated by Smart Approval AI.</p>
        <p>Powered by Google Gemini AI & Firebase Authentication</p>
    </div>
</body>
</html>
        """
        
        # Save demo report temporarily
        demo_report_path = os.path.join(settings.REPORTS_DIR, f"report_{batch_id}.html")
        os.makedirs(settings.REPORTS_DIR, exist_ok=True)
        with open(demo_report_path, 'w') as f:
            f.write(demo_html)
        
        return FileResponse(
            demo_report_path,
            media_type="text/html",
            filename=f"report_{batch_id}.html"
        )
    
    db = get_db()
    
    try:
        batch = db.query(Batch).filter(Batch.id == batch_id).first()
        if not batch:
            raise HTTPException(status_code=404, detail="Batch not found")
        
        # PLATFORM MODEL: Enforce user access control (skip for system batches)
        is_system_batch = getattr(batch, 'data_source', 'user') == 'system'
        if user and not is_system_batch:
            user_id = user.get("uid")
            role = user.get("role", "department")
            
            if role != "institution":
                department_id = user.get("department_id")
                if department_id:
                    if batch.department_id != department_id:
                        raise HTTPException(status_code=403, detail="Access denied")
                elif user_id:
                    if batch.user_id != user_id:
                        raise HTTPException(status_code=403, detail="Access denied")
        
        # Find report file - check for both PDF and HTML (WeasyPrint fallback)
        report_filename_pdf = f"report_{batch_id}.pdf"
        report_filename_html = f"report_{batch_id}.html"
        reports_dir = getattr(settings, 'REPORTS_DIR', 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        report_path_pdf = os.path.join(reports_dir, report_filename_pdf)
        report_path_html = os.path.join(reports_dir, report_filename_html)
        
        # Try PDF first, then HTML
        if os.path.exists(report_path_pdf):
            return FileResponse(
                report_path_pdf,
                media_type="application/pdf",
                filename=report_filename_pdf
            )
        elif os.path.exists(report_path_html):
            return FileResponse(
                report_path_html,
                media_type="text/html",
                filename=report_filename_html
            )
        else:
            raise HTTPException(status_code=404, detail="Report not generated. Please generate it first.")
    finally:
        close_db(db)
