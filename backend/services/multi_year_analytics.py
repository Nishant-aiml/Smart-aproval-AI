"""
Multi-year analytics service.
Aggregates KPIs across multiple batches/years.
"""

import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from config.database import get_db, close_db, Batch, Block
from schemas.analytics import YearMetric, MetricTrend


CANONICAL_KPIS = {
    "fsr_score": "FSR Score", 
    "infrastructure_score": "Infrastructure Score", 
    "placement_index": "Placement Index", 
    "lab_compliance_index": "Lab Compliance Index", 
    "overall_score": "Overall Score"
}


def extract_year_from_batch(batch_id: str, blocks: List, batch=None) -> str:
    """
    Extract academic year from batch or batch blocks.
    Returns format like "2024-25" or "2023-24".
    """
    if batch and getattr(batch, 'academic_year', None):
        return batch.academic_year

    # Try querying batch from DB
    try:
        from config.database import get_db, close_db, Batch as DBBatch
        db = get_db()
        try:
            b = db.query(DBBatch).filter(DBBatch.id == batch_id).first()
            if b and b.academic_year:
                return b.academic_year
        finally:
            close_db(db)
    except Exception:
        pass

    # Try to find academic year in blocks
    for block in blocks:
        if block.data:
            year = _extract_year_from_data(block.data)
            if year:
                return year
    
    # Fallback: extract from batch_id (contains date)
    match = re.search(r'_(\d{4})(\d{2})(\d{2})_', batch_id)
    if match:
        return match.group(1)
    
    # Last resort: current year
    return str(datetime.now().year)


def _extract_year_from_data(data: Dict) -> Optional[str]:
    """Extract year from block data."""
    year_fields = ['academic_year', 'year', 'session', 'academic_session', 'approval_year', 'last_updated_year']
    
    for field in year_fields:
        if field in data and data[field]:
            val = str(data[field])
            # Extract 4-digit year or year range
            match = re.search(r'(\d{4})[-–]?(\d{2,4})?', val)
            if match:
                # If it's just a year number, format as academic year
                if field == 'year' or field == 'last_updated_year':
                    year_num = int(match.group(1))
                    if 2000 <= year_num <= 2100:
                        return f"{year_num}-{str(year_num + 1)[-2:]}"
                return val
    
    # Check for year in any field name containing "year"
    for key, val in data.items():
        if 'year' in key.lower() and val:
            val_str = str(val)
            match = re.search(r'(\d{4})[-–]?(\d{2,4})?', val_str)
            if match:
                year_num = int(match.group(1))
                if 2000 <= year_num <= 2100:
                    return f"{year_num}-{str(year_num + 1)[-2:]}"
    
    # Check nested data
    if isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, dict):
                result = _extract_year_from_data(val)
                if result:
                    return result
    
    return None


def normalize_year(year_str: str) -> int:
    """Convert year string to sortable integer (ending year of range)."""
    if not year_str:
        return datetime.now().year
    
    # Handle ranges like "2023-24" or "2023-2024"
    match = re.search(r'(\d{4})[-–](\d{2,4})', year_str)
    if match:
        end_year = match.group(2)
        if len(end_year) == 2:
            return 2000 + int(end_year)
        return int(end_year)
    
    # Single year
    match = re.search(r'(\d{4})', year_str)
    if match:
        return int(match.group(1))
    
    return datetime.now().year


def get_batch_kpis(batch_id: str) -> Dict[str, Optional[float]]:
    """Get KPIs for a batch from dashboard data."""
    from routers.dashboard import get_dashboard_data
    from fastapi import HTTPException
    
    try:
        dashboard = get_dashboard_data(batch_id)
        kpis = {}
        for key in CANONICAL_KPIS.keys():
            val = dashboard.kpis.get(key)
            if val is not None and isinstance(val, (int, float)) and val > 0:
                kpis[key] = float(val)
            else:
                kpis[key] = None
        return kpis
    except HTTPException:
        return {k: None for k in CANONICAL_KPIS.keys()}


def aggregate_multi_year_data(batch_ids: List[str]) -> Tuple[Dict[str, List[YearMetric]], List[str], str]:
    """
    Aggregate KPI data across multiple batches.
    Returns: (metrics_by_kpi, available_years, institution_name)
    """
    db = get_db()
    try:
        year_data: Dict[str, Dict[str, Optional[float]]] = {}  # year -> {kpi: value}
        institution_name = "Multiple Institutions"
        
        for bid in batch_ids:
            batch = db.query(Batch).filter(Batch.id == bid).first()
            if not batch or batch.status != "completed":
                continue
            
            blocks = db.query(Block).filter(Block.batch_id == bid).all()
            if not blocks:
                continue
            
            # Extract year
            year = extract_year_from_batch(bid, blocks, batch=batch)
            
            # Get KPIs
            kpis = get_batch_kpis(bid)
            
            # If year already exists, average the values
            if year in year_data:
                for k, v in kpis.items():
                    if v is not None and isinstance(v, (int, float)):
                        existing = year_data[year].get(k)
                        if existing is not None and isinstance(existing, (int, float)):
                            year_data[year][k] = (existing + v) / 2
                        else:
                            year_data[year][k] = v
            else:
                year_data[year] = kpis.copy() if kpis else {}
            
            # Try to get institution name
            if batch.institution_name:
                institution_name = batch.institution_name
            for block in blocks:
                if block.data:
                    for key in ['institution_name', 'name', 'institute_name']:
                        if key in block.data and block.data[key]:
                            institution_name = str(block.data[key])
                            break
        
        # Sort years
        sorted_years = sorted(year_data.keys(), key=normalize_year)
        
        # Build metrics dict - ensure years are in chronological order
        metrics: Dict[str, List[YearMetric]] = {}
        for kpi in CANONICAL_KPIS.keys():
            metrics[kpi] = []
            for year in sorted_years:
                value = year_data.get(year, {}).get(kpi)
                # Only add if value is not None and > 0
                if value is not None and isinstance(value, (int, float)) and value > 0:
                    metrics[kpi].append(YearMetric(year=year, value=float(value)))
        
        # Filter out metrics with insufficient data (< 3 years)
        filtered_metrics = {}
        for kpi, values in metrics.items():
            if len(values) >= 3:
                filtered_metrics[kpi] = values
        
        return filtered_metrics, sorted_years, institution_name
    finally:
        close_db(db)


def calculate_trend(values: List[YearMetric]) -> Tuple[str, Optional[float]]:
    """Calculate trend direction and average."""
    valid_values = [v.value for v in values if v.value is not None]
    
    if len(valid_values) < 2:
        return "stable", sum(valid_values) / len(valid_values) if valid_values else None
    
    avg = sum(valid_values) / len(valid_values)
    
    # Simple trend: compare first half to second half
    mid = len(valid_values) // 2
    first_half_avg = sum(valid_values[:mid]) / mid if mid > 0 else 0
    second_half_avg = sum(valid_values[mid:]) / (len(valid_values) - mid)
    
    if second_half_avg > first_half_avg * 1.05:
        return "up", avg
    elif second_half_avg < first_half_avg * 0.95:
        return "down", avg
    return "stable", avg


def build_trend_summary(metrics: Dict[str, List[YearMetric]]) -> Dict[str, MetricTrend]:
    """Build summary statistics for each metric."""
    summary = {}
    
    for kpi, values in metrics.items():
        valid_values = [v.value for v in values if v.value is not None]
        trend_dir, avg = calculate_trend(values)
        
        summary[kpi] = MetricTrend(
            metric_name=kpi,
            display_name=CANONICAL_KPIS.get(kpi, kpi),
            values=values,
            average=avg,
            min_value=min(valid_values) if valid_values else None,
            max_value=max(valid_values) if valid_values else None,
            trend_direction=trend_dir,
        )
    
    return summary


def find_best_worst_years(metrics: Dict[str, List[YearMetric]]) -> Tuple[Optional[str], Optional[str]]:
    """Find best and worst years based on overall score."""
    overall = metrics.get("overall_score", [])
    
    valid = [(v.year, v.value) for v in overall if v.value is not None]
    if not valid:
        return None, None
    
    best = max(valid, key=lambda x: x[1])
    worst = min(valid, key=lambda x: x[1])
    
    return best[0], worst[0]


def generate_insights(trend_summary: Dict[str, MetricTrend]) -> List[str]:
    """Generate textual insights from trend data."""
    insights = []
    
    for kpi, trend in trend_summary.items():
        if trend.trend_direction == "up":
            insights.append(f"📈 {trend.display_name} shows positive growth trend")
        elif trend.trend_direction == "down":
            insights.append(f"📉 {trend.display_name} shows declining trend - needs attention")
    
    # Overall insights
    overall = trend_summary.get("overall_score")
    if overall and overall.average:
        if overall.average >= 80:
            insights.append("✅ Overall performance is excellent across years")
        elif overall.average >= 60:
            insights.append("📊 Overall performance is good with room for improvement")
        else:
            insights.append("⚠️ Overall performance needs significant improvement")
    
    return insights
