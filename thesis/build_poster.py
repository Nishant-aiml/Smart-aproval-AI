"""
Smart Approval AI - Academic Research Project Poster Generator
Priyadarshini College of Engineering, Nagpur
Department of Information Technology

Generates:
1. Smart_Approval_AI_Poster.html (Self-contained, interactive, responsive HTML/CSS)
2. Smart_Approval_AI_Poster.png (High-resolution 300 DPI print-ready image)
3. Smart_Approval_AI_Poster.pdf (Vector-crisp printable PDF)
4. Updates thesis/extracted_assets/poster_smart_approval_ai.png for Appendix F
"""

import os
import base64
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_base64_image(path):
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(path)[1].lower()
    mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"

def build_poster_html():
    logo_b64 = get_base64_image(os.path.join(BASE_DIR, "extracted_assets", "image_2.jpeg"))
    arch_b64 = get_base64_image(os.path.join(BASE_DIR, "images", "fig_system_arch.png"))
    dash_b64 = get_base64_image(os.path.join(BASE_DIR, "images", "fig_dashboard.png"))
    aicte_b64 = get_base64_image(os.path.join(BASE_DIR, "images", "fig_aicte_eval.png"))
    nba_b64 = get_base64_image(os.path.join(BASE_DIR, "images", "fig_nba_sar.png"))
    analytics_b64 = get_base64_image(os.path.join(BASE_DIR, "images", "fig_analytics.png"))
    bench_b64 = get_base64_image(os.path.join(BASE_DIR, "images", "fig_benchmark_perf.png"))
    reports_b64 = get_base64_image(os.path.join(BASE_DIR, "images", "fig_reports.png"))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Smart Approval AI - Project Poster</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');

    @page {{
        size: 1400px 2060px;
        margin: 0;
    }}

    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}

    body {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: #f1f5f9;
        color: #1e293b;
        width: 1400px;
        height: 2060px;
        margin: 0 auto;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        -webkit-font-smoothing: antialiased;
    }}

    /* ---------------- HEADER BAR ---------------- */
    .header-bar {{
        background: #ffffff;
        padding: 16px 36px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 3px solid #2563eb;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }}

    .header-left {{
        display: flex;
        align-items: center;
        gap: 20px;
    }}

    .college-logo {{
        height: 82px;
        width: auto;
        object-fit: contain;
    }}

    .college-text {{
        text-align: left;
    }}

    .college-title {{
        font-size: 24px;
        font-weight: 900;
        letter-spacing: 0.5px;
        color: #1e3a8a;
        line-height: 1.2;
    }}

    .college-sub {{
        font-size: 13.5px;
        font-weight: 600;
        color: #475569;
        margin-top: 3px;
    }}

    .dept-title {{
        font-size: 15px;
        font-weight: 800;
        color: #0284c7;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-top: 3px;
    }}

    .header-right {{
        text-align: right;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 6px;
    }}

    .badge-accred {{
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #bfdbfe;
        color: #1d4ed8;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}

    .badge-session {{
        font-size: 12px;
        font-weight: 700;
        color: #64748b;
    }}

    /* ---------------- HERO TITLE BANNER ---------------- */
    .hero-banner {{
        background: linear-gradient(135deg, #07152d 0%, #0c2752 45%, #133e7c 100%);
        color: #ffffff;
        padding: 24px 36px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
        box-shadow: inset 0 -4px 12px rgba(0,0,0,0.3);
    }}

    .hero-banner::after {{
        content: "";
        position: absolute;
        top: -50px;
        right: -50px;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, rgba(0, 0, 0, 0) 70%);
        pointer-events: none;
    }}

    .hero-content {{
        display: flex;
        align-items: center;
        gap: 24px;
        z-index: 2;
    }}

    .hero-icon {{
        width: 76px;
        height: 76px;
        background: linear-gradient(135deg, #38bdf8 0%, #2563eb 100%);
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4), 0 0 0 2px rgba(255,255,255,0.2);
        flex-shrink: 0;
    }}

    .hero-icon svg {{
        width: 44px;
        height: 44px;
        fill: #ffffff;
    }}

    .hero-titles {{
        display: flex;
        flex-direction: column;
        gap: 4px;
    }}

    .project-name {{
        font-size: 40px;
        font-weight: 900;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
        line-height: 1.1;
    }}

    .project-name span {{
        color: #38bdf8;
    }}

    .project-tagline {{
        font-size: 15px;
        font-weight: 500;
        color: #bae6fd;
        max-width: 950px;
        line-height: 1.35;
    }}

    .hero-pills {{
        display: flex;
        gap: 10px;
        margin-top: 6px;
    }}

    .pill {{
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #f0fdf4;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 6px;
        letter-spacing: 0.3px;
    }}

    /* ---------------- THREE-COLUMN GRID ---------------- */
    .poster-grid {{
        flex: 1;
        display: grid;
        grid-template-columns: 420px 520px 420px;
        gap: 16px;
        padding: 16px 24px;
        background: #f1f5f9;
    }}

    .col {{
        display: flex;
        flex-direction: column;
        gap: 14px;
    }}

    /* ---------------- CARD SYSTEM ---------------- */
    .card {{
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }}

    .card-header {{
        background: #f8fafc;
        border-bottom: 1.5px solid #e2e8f0;
        padding: 9px 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .card-icon {{
        width: 24px;
        height: 24px;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        color: #2563eb;
        flex-shrink: 0;
    }}

    .card-title {{
        font-size: 13.5px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }}

    .card-body {{
        padding: 12px 14px;
        font-size: 11px;
        line-height: 1.45;
        color: #334155;
    }}

    /* ---------------- LISTS & BULLETS ---------------- */
    .feature-list {{
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 7px;
    }}

    .feature-item {{
        display: flex;
        align-items: flex-start;
        gap: 8px;
    }}

    .check-icon {{
        width: 15px;
        height: 15px;
        background: #10b981;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 9px;
        font-weight: 900;
        margin-top: 1px;
        flex-shrink: 0;
    }}

    .feature-text strong {{
        color: #0f172a;
        font-weight: 700;
    }}

    /* ---------------- OBJECTIVES NUMBERED LIST ---------------- */
    .obj-list {{
        display: flex;
        flex-direction: column;
        gap: 8px;
    }}

    .obj-item {{
        display: flex;
        align-items: flex-start;
        gap: 10px;
    }}

    .obj-num {{
        width: 20px;
        height: 20px;
        background: #2563eb;
        color: #ffffff;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        font-weight: 800;
        flex-shrink: 0;
        margin-top: 1px;
    }}

    .obj-desc strong {{
        color: #1e3a8a;
    }}

    /* ---------------- TABLE STYLING ---------------- */
    .tech-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 10.5px;
    }}

    .tech-table tr {{
        border-bottom: 1px solid #f1f5f9;
    }}

    .tech-table tr:last-child {{
        border-bottom: none;
    }}

    .tech-table td {{
        padding: 5px 6px;
    }}

    .tech-layer {{
        font-weight: 700;
        color: #1e40af;
        width: 28%;
        vertical-align: top;
    }}

    .tech-val {{
        color: #334155;
        font-family: 'JetBrains Mono', monospace;
        font-size: 9.5px;
    }}

    /* ---------------- IMAGE SHOWCASE BOXES ---------------- */
    .img-box {{
        background: #0f172a;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #cbd5e1;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        position: relative;
    }}

    .img-box img {{
        width: 100%;
        height: auto;
        display: block;
    }}

    .img-caption {{
        background: #f8fafc;
        border-top: 1px solid #e2e8f0;
        padding: 5px 8px;
        font-size: 9.5px;
        font-weight: 700;
        color: #475569;
        text-align: center;
    }}

    .side-by-side {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }}

    /* ---------------- METRIC BADGES ROW ---------------- */
    .metric-row {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-top: 6px;
    }}

    .metric-badge {{
        background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 7px 4px;
        text-align: center;
        display: flex;
        flex-direction: column;
        gap: 2px;
    }}

    .metric-val {{
        font-size: 16px;
        font-weight: 900;
        color: #1d4ed8;
        font-family: 'JetBrains Mono', monospace;
    }}

    .metric-lbl {{
        font-size: 8.5px;
        font-weight: 700;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }}

    /* ---------------- FOOTER BAR ---------------- */
    .footer-bar {{
        background: linear-gradient(135deg, #07152d 0%, #0c2752 45%, #133e7c 100%);
        color: #ffffff;
        padding: 16px 36px 14px 36px;
        border-top: 3px solid #38bdf8;
    }}

    .footer-top {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        margin-bottom: 12px;
    }}

    .footer-line {{
        height: 1px;
        background: rgba(255, 255, 255, 0.25);
        flex: 1;
    }}

    .footer-heading {{
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #7dd3fc;
    }}

    .members-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }}

    .member-card {{
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        padding: 8px 12px;
        text-align: center;
    }}

    .member-name {{
        font-size: 14px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 0.2px;
    }}

    .member-role {{
        font-size: 11px;
        font-weight: 600;
        color: #93c5fd;
        margin-top: 2px;
    }}

    .member-sub {{
        font-size: 10px;
        color: #cbd5e1;
        margin-top: 1px;
    }}

    .footer-sub {{
        margin-top: 10px;
        padding-top: 8px;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        text-align: center;
        font-size: 11px;
        color: #94a3b8;
        letter-spacing: 0.5px;
        font-weight: 600;
    }}
</style>
</head>
<body>

    <!-- ==================== HEADER BAR ==================== -->
    <header class="header-bar">
        <div class="header-left">
            <img src="{logo_b64}" alt="Priyadarshini College of Engineering Logo" class="college-logo">
            <div class="college-text">
                <div class="college-title">PRIYADARSHINI COLLEGE OF ENGINEERING</div>
                <div class="college-sub">(An Autonomous Institute Affiliated to Rashtrasant Tukdoji Maharaj Nagpur University, Nagpur)</div>
                <div class="dept-title">DEPARTMENT OF INFORMATION TECHNOLOGY</div>
            </div>
        </div>
        <div class="header-right">
            <div class="badge-accred">★ NAAC A+ & NBA ACCREDITED INSTITUTE ★</div>
            <div class="badge-session">B.Tech Honors Capstone Project | Session 2026-2027</div>
        </div>
    </header>

    <!-- ==================== HERO TITLE BANNER ==================== -->
    <section class="hero-banner">
        <div class="hero-content">
            <div class="hero-icon">
                <svg viewBox="0 0 24 24">
                    <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
                </svg>
            </div>
            <div class="hero-titles">
                <div class="project-name">Smart Approval <span>AI</span></div>
                <div class="project-tagline">
                    An End-to-End, Multi-Modal AI System for Statutory Higher Education Accreditation Auditing, Regulatory Compliance Verification, and Longitudinal Institutional Performance Analytics
                </div>
                <div class="hero-pills">
                    <span class="pill">AICTE APH 2024-2027</span>
                    <span class="pill">NBA Tier-I 1000-Point SAR</span>
                    <span class="pill">NAAC SSR & NIRF</span>
                    <span class="pill">IBM Docling Layout OCR</span>
                    <span class="pill">Gemini 2.5 Flash</span>
                    <span class="pill">SARIMA Forecasting</span>
                </div>
            </div>
        </div>
    </section>

    <!-- ==================== THREE-COLUMN GRID ==================== -->
    <main class="poster-grid">

        <!-- ==================== COLUMN 1 (FOUNDATION & ARCHITECTURE) ==================== -->
        <div class="col">
            <!-- 1. Introduction -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">💡</div>
                    <div class="card-title">1. Introduction</div>
                </div>
                <div class="card-body">
                    Smart Approval AI is an autonomous, multi-modal cognitive auditing and compliance verification platform engineered for Indian engineering institutions. It replaces episodic, 45-day paper-heavy accreditation scrutinies with real-time, deterministic verification across <strong>AICTE</strong>, <strong>NBA Tier-I SAR</strong>, <strong>NAAC SSR</strong>, and <strong>NIRF</strong> frameworks.
                </div>
            </div>

            <!-- 2. Key Features -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">⚙️</div>
                    <div class="card-title">Key Features</div>
                </div>
                <div class="card-body">
                    <ul class="feature-list">
                        <li class="feature-item">
                            <span class="check-icon">✓</span>
                            <span class="feature-text"><strong>Multi-Modal Layout Ingestion:</strong> Docling OCR parsing complex tables, multi-column layouts & scanned scans.</span>
                        </li>
                        <li class="feature-item">
                            <span class="check-icon">✓</span>
                            <span class="feature-text"><strong>Zero-Hallucination Extraction:</strong> Gemini 2.5 Flash strictly bounded by Pydantic v2 schemas for verified entity parsing.</span>
                        </li>
                        <li class="feature-item">
                            <span class="check-icon">✓</span>
                            <span class="feature-text"><strong>Deterministic AICTE Verification:</strong> Automated check of 1:2:6 Cadre Ratios, SFR (1:15/1:20), and area norms.</span>
                        </li>
                        <li class="feature-item">
                            <span class="check-icon">✓</span>
                            <span class="feature-text"><strong>NBA Tier-I 1000-Pt SAR Engine:</strong> Automated rubrics across all 10 criteria aligned with the Washington Accord.</span>
                        </li>
                        <li class="feature-item">
                            <span class="check-icon">✓</span>
                            <span class="feature-text"><strong>Predictive Analytics (SARIMA):</strong> Longitudinal time-series forecasting detecting anomalies 12-24 months early.</span>
                        </li>
                        <li class="feature-item">
                            <span class="check-icon">✓</span>
                            <span class="feature-text"><strong>Tamper-Proof Dossier Synthesis:</strong> One-click generation of PDF/Excel audit reports with SHA-256 digital seals.</span>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- 3. System Architecture Diagram -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🏗️</div>
                    <div class="card-title">System Architecture</div>
                </div>
                <div class="card-body" style="padding: 8px;">
                    <div class="img-box">
                        <img src="{arch_b64}" alt="Smart Approval AI System Architecture Diagram">
                        <div class="img-caption">Figure 1: Decoupled Multi-Modal Microservices Pipeline</div>
                    </div>
                </div>
            </div>

            <!-- 4. Tech Stack -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🥞</div>
                    <div class="card-title">Technology Stack</div>
                </div>
                <div class="card-body" style="padding: 8px 12px;">
                    <table class="tech-table">
                        <tr>
                            <td class="tech-layer">Frontend</td>
                            <td class="tech-val">Next.js 14, React 19, Tailwind CSS, Lucide (Port 3051)</td>
                        </tr>
                        <tr>
                            <td class="tech-layer">Backend API</td>
                            <td class="tech-val">FastAPI, Python 3.11, Uvicorn, Pydantic v2 (Port 8051)</td>
                        </tr>
                        <tr>
                            <td class="tech-layer">OCR & Layout</td>
                            <td class="tech-val">IBM Docling (granite-vision), PyMuPDF v1.25</td>
                        </tr>
                        <tr>
                            <td class="tech-layer">Cognitive LLM</td>
                            <td class="tech-val">Google Gemini 2.5 Flash (Cloud API)</td>
                        </tr>
                        <tr>
                            <td class="tech-layer">Forecasting</td>
                            <td class="tech-val">SARIMA, Polynomial Regression, Statsmodels, SciPy</td>
                        </tr>
                        <tr>
                            <td class="tech-layer">Database</td>
                            <td class="tech-val">SQLAlchemy Core, SQLite3 / PostgreSQL</td>
                        </tr>
                        <tr>
                            <td class="tech-layer">Deployment</td>
                            <td class="tech-val">Single-Tunnel Reverse Proxy, Ngrok Inspector (4051)</td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>

        <!-- ==================== COLUMN 2 (LIVE SYSTEM & PERFORMANCE) ==================== -->
        <div class="col">
            <!-- 1. Live Dashboard -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🖥️</div>
                    <div class="card-title">Live Platform Dashboard</div>
                </div>
                <div class="card-body" style="padding: 8px;">
                    <div class="img-box">
                        <img src="{dash_b64}" alt="Smart Approval AI Interactive Dashboard">
                        <div class="img-caption">Figure 2: Real-Time Compliance Overview, Deficit Breakdown & Multi-Department Scorecards</div>
                    </div>
                </div>
            </div>

            <!-- 2. AICTE & NBA SAR Evaluation Engines -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">⚖️</div>
                    <div class="card-title">Regulatory Verification Engines</div>
                </div>
                <div class="card-body" style="padding: 8px;">
                    <div class="side-by-side">
                        <div class="img-box">
                            <img src="{aicte_b64}" alt="AICTE Compliance Verification Module">
                            <div class="img-caption">Figure 3(a): AICTE Cadre & SFR Audit</div>
                        </div>
                        <div class="img-box">
                            <img src="{nba_b64}" alt="NBA Tier-I SAR Evaluation Module">
                            <div class="img-caption">Figure 3(b): NBA Tier-I 1000-Pt SAR Scorecard</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. Longitudinal Predictive Analytics -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">📈</div>
                    <div class="card-title">Longitudinal SARIMA Forecasting</div>
                </div>
                <div class="card-body" style="padding: 8px;">
                    <div class="img-box">
                        <img src="{analytics_b64}" alt="Longitudinal Predictive Analytics Module">
                        <div class="img-caption">Figure 4: 5-Year Compliance Trajectory Modeling & Anomaly Early Warning System</div>
                    </div>
                </div>
            </div>

            <!-- 4. Performance Benchmarks -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">📊</div>
                    <div class="card-title">Empirical Benchmark Evaluation</div>
                </div>
                <div class="card-body" style="padding: 8px 10px;">
                    <div class="img-box">
                        <img src="{bench_b64}" alt="Benchmark Performance & Accuracy Chart">
                        <div class="img-caption">Figure 5: Evaluation Across 50 Engineering Colleges (14,250 Pages)</div>
                    </div>
                    <div class="metric-row">
                        <div class="metric-badge">
                            <span class="metric-val">96.8%</span>
                            <span class="metric-lbl">Turnaround Reduction</span>
                        </div>
                        <div class="metric-badge">
                            <span class="metric-val">99.1%</span>
                            <span class="metric-lbl">Defect Detection</span>
                        </div>
                        <div class="metric-badge">
                            <span class="metric-val">0.0%</span>
                            <span class="metric-lbl">Math Hallucination</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ==================== COLUMN 3 (PROBLEM, OBJECTIVES & SCOPE) ==================== -->
        <div class="col">
            <!-- 1. Problem Statement -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🎯</div>
                    <div class="card-title">Problem Statement</div>
                </div>
                <div class="card-body">
                    Higher education accreditation in India requires navigating multi-tiered, opaque mandates across AICTE, NBA, NAAC, and NIRF. Manual scrutiny of 1,000+ page institutional portfolios takes <strong>45 person-days</strong>, introduces cognitive bias, causes mathematical discrepancies in SFR and cadre ratios, and results in catastrophic eleventh-hour approval rejections.
                </div>
            </div>

            <!-- 2. Objectives -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🎯</div>
                    <div class="card-title">Project Objectives</div>
                </div>
                <div class="card-body">
                    <div class="obj-list">
                        <div class="obj-item">
                            <div class="obj-num">1</div>
                            <div class="obj-desc"><strong>Autonomous Layout Parsing:</strong> Extract tables, stamps, and nested hierarchies from scanned PDFs with 98%+ cell fidelity.</div>
                        </div>
                        <div class="obj-item">
                            <div class="obj-num">2</div>
                            <div class="obj-desc"><strong>Deterministic Compliance:</strong> Eliminate LLM arithmetic errors via programmatic AICTE, NBA, and NAAC verification.</div>
                        </div>
                        <div class="obj-item">
                            <div class="obj-num">3</div>
                            <div class="obj-desc"><strong>Outcome-Based Evaluation:</strong> Real-time 1000-point SAR rubric computation tied to Washington Accord CO-PO metrics.</div>
                        </div>
                        <div class="obj-item">
                            <div class="obj-num">4</div>
                            <div class="obj-desc"><strong>Predictive Forecasting:</strong> SARIMA time-series alerting leadership to faculty attrition and deficits 2 years in advance.</div>
                        </div>
                        <div class="obj-item">
                            <div class="obj-num">5</div>
                            <div class="obj-desc"><strong>Port-Isolated Architecture:</strong> Single-tunnel reverse-proxy preventing port collisions across concurrent web servers.</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. Automated Reporting -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">📑</div>
                    <div class="card-title">Automated Institutional Reports</div>
                </div>
                <div class="card-body" style="padding: 8px;">
                    <div class="img-box">
                        <img src="{reports_b64}" alt="Automated Audit Report Generation">
                        <div class="img-caption">Figure 6: One-Click PDF/Word SAR Synthesis with SHA-256 Tamper Seals</div>
                    </div>
                </div>
            </div>

            <!-- 4. Future Scope -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🚀</div>
                    <div class="card-title">Future Research Scope</div>
                </div>
                <div class="card-body">
                    <ul class="feature-list">
                        <li class="feature-item">
                            <span class="check-icon" style="background: #0284c7;">→</span>
                            <span class="feature-text"><strong>Drone & Satellite Campus Auditing:</strong> Autonomous verification of land acreage and building footprints via aerial GIS.</span>
                        </li>
                        <li class="feature-item">
                            <span class="check-icon" style="background: #0284c7;">→</span>
                            <span class="feature-text"><strong>Voice-Enabled Evaluator Agent:</strong> Real-time conversational RAG agent assisting visiting peer inspection committees.</span>
                        </li>
                        <li class="feature-item">
                            <span class="check-icon" style="background: #0284c7;">→</span>
                            <span class="feature-text"><strong>Blockchain Credential Anchoring:</strong> Immutable ledger registration for student transcripts and faculty publications.</span>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- 5. Conclusion -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">🏁</div>
                    <div class="card-title">Conclusion</div>
                </div>
                <div class="card-body">
                    Smart Approval AI demonstrates that combining decoupled vision-language OCR with deterministic statutory rules transforms higher education accreditation from an episodic, panic-driven bureaucratic hurdle into an ongoing instrument of institutional quality, transparency, and global excellence.
                </div>
            </div>
        </div>

    </main>

    <!-- ==================== FOOTER BAR ==================== -->
    <footer class="footer-bar">
        <div class="footer-top">
            <div class="footer-line"></div>
            <div class="footer-heading">SUBMITTED BY & ACADEMIC GUIDANCE</div>
            <div class="footer-line"></div>
        </div>
        <div class="members-grid">
            <div class="member-card">
                <div class="member-name">Nishant Datta</div>
                <div class="member-role">Student Projectee</div>
                <div class="member-sub">B.Tech (Information Technology)</div>
            </div>
            <div class="member-card">
                <div class="member-name">Nazish Khan</div>
                <div class="member-role">Student Projectee</div>
                <div class="member-sub">B.Tech (Information Technology)</div>
            </div>
            <div class="member-card">
                <div class="member-name">Dr. Archana Potnurwar</div>
                <div class="member-role">Project Guide</div>
                <div class="member-sub">Associate Professor, Dept. of IT</div>
            </div>
            <div class="member-card">
                <div class="member-name">Ms. Lalita Charpe</div>
                <div class="member-role">Project Co-Guide</div>
                <div class="member-sub">Assistant Professor, Dept. of IT</div>
            </div>
        </div>
        <div class="footer-sub">
            DEPARTMENT OF INFORMATION TECHNOLOGY &bull; PRIYADARSHINI COLLEGE OF ENGINEERING, NAGPUR &bull; SESSION 2026-2027
        </div>
    </footer>

</body>
</html>
"""
    return html

def main():
    print("Building high-resolution academic poster for Smart Approval AI...")
    html_content = build_poster_html()
    
    html_path = os.path.join(BASE_DIR, "Smart_Approval_AI_Poster.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"1. Saved interactive self-contained HTML poster: {html_path}")

    # Render via Chrome headless
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    browser = None
    for p in chrome_paths:
        if os.path.exists(p):
            browser = p
            break

    if not browser:
        print("Error: Chrome/Edge executable not found for rendering.")
        return

    png_path = os.path.join(BASE_DIR, "Smart_Approval_AI_Poster.png")
    pdf_path = os.path.join(BASE_DIR, "Smart_Approval_AI_Poster.pdf")
    file_url = "file:///" + html_path.replace("\\", "/")

    # Render PNG (1400x2060 window size, scaled for crisp 300 DPI viewing)
    print(f"Rendering high-resolution PNG using {os.path.basename(browser)}...")
    cmd_png = [
        browser,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--screenshot={png_path}",
        "--window-size=1400,2060",
        "--force-device-scale-factor=2",
        file_url
    ]
    res_png = subprocess.run(cmd_png, capture_output=True, text=True)
    if os.path.exists(png_path):
        print(f"2. Rendered ultra-high-resolution PNG poster: {png_path} ({os.path.getsize(png_path):,} bytes)")

    # Render PDF (Print-ready)
    print(f"Rendering printable PDF using {os.path.basename(browser)}...")
    cmd_pdf = [
        browser,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        file_url
    ]
    res_pdf = subprocess.run(cmd_pdf, capture_output=True, text=True)
    if os.path.exists(pdf_path):
        print(f"3. Rendered vector PDF poster: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")

    # Also update the asset used in Appendix F
    appendix_asset_path = os.path.join(BASE_DIR, "extracted_assets", "poster_smart_approval_ai.png")
    if os.path.exists(png_path):
        from PIL import Image
        im = Image.open(png_path)
        # Convert to optimal size for Word document embedding while maintaining crisp detail
        im_appendix = im.resize((1200, int(1200 * im.height / im.width)), Image.Resampling.LANCZOS)
        im_appendix.save(appendix_asset_path, quality=95)
        print(f"4. Updated Appendix F poster asset in: {appendix_asset_path}")

    print("\nPoster generation complete!")

if __name__ == "__main__":
    main()
