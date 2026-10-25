"""
Year-Wise KPI Processing Service.
Parses historical year data from blocks and calculates KPIs per year.
"""

import re
import math
from typing import Dict, List, Any, Optional, Tuple
from statistics import stdev, mean


# Regex patterns for year detection
YEAR_PATTERNS = [
    r'\b(19\d{2}|20\d{2})\b',  # Full year: 2023, 2024
    r'\b(19\d{2}|20\d{2})[-–](19\d{2}|20\d{2})\b',  # Range: 2023-2024
    r'\b(19\d{2}|20\d{2})[-–](\d{2})\b',  # Short range: 2023-24
]


def parse_year(value: str) -> Optional[int]:
    """Parse a year from a string, handling various formats."""
    if not value:
        return None
    
    value = str(value).strip()
    
    # Try short range format first: 2023-24 -> 2024
    match = re.search(r'(19\d{2}|20\d{2})[-–](\d{2})\b', value)
    if match:
        base_year = int(match.group(1))
        suffix = int(match.group(2))
        century = base_year // 100
        return century * 100 + suffix
    
    # Try full range: 2023-2024 -> 2024
    match = re.search(r'(19\d{2}|20\d{2})[-–](19\d{2}|20\d{2})\b', value)
    if match:
        return int(match.group(2))
    
    # Try single year
    match = re.search(r'\b(19\d{2}|20\d{2})\b', value)
    if match:
        return int(match.group(1))
    
    return None


def extract_years_from_block(block_data: Dict) -> Dict[int, Dict[str, Any]]:
    """
    Extract year-wise data from a block.
    Returns: {year: {field: value, ...}, ...}
    """
    year_data: Dict[int, Dict[str, Any]] = {}
    
    if not block_data or not isinstance(block_data, dict):
        return year_data
    
    # Check for explicit year fields
    for key, value in block_data.items():
        if key in ['parsed_year', 'academic_year', 'last_updated_year', 'year']:
            year = parse_year(str(value))
            if year:
                if year not in year_data:
                    year_data[year] = {}
                # Add all other fields to this year
                for k, v in block_data.items():
                    if k not in ['parsed_year', 'academic_year', 'year'] and v is not None:
                        year_data[year][k] = v
    
    # Check for yearly arrays (e.g., placements_by_year, faculty_by_year)
    for key, value in block_data.items():
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    year_val = item.get('year') or item.get('academic_year')
                    year = parse_year(str(year_val)) if year_val else None
                    if year:
                        if year not in year_data:
                            year_data[year] = {}
                        for k, v in item.items():
                            if k != 'year' and k != 'academic_year' and v is not None:
                                year_data[year][k] = v
    
    return year_data


def calculate_fsr_for_year(year_data: Dict[str, Any]) -> Optional[float]:
    """Calculate FSR score for a single year's data."""
    faculty = None
    students = None
    
    # Try different field names
    for key in ['total_faculty', 'faculty_count', 'faculty_count_num', 'total_faculty_num']:
        if key in year_data and year_data[key] is not None:
            try:
                faculty = float(year_data[key])
                break
            except:
                pass
    
    for key in ['total_students', 'student_count', 'student_count_num', 'total_intake', 'admitted_students']:
        if key in year_data and year_data[key] is not None:
            try:
                students = float(year_data[key])
                break
            except:
                pass
    
    # Aggregate UG + PG if total missing
    if students is None:
        ug = year_data.get('ug_students') or year_data.get('ug_enrollment')
        pg = year_data.get('pg_students') or year_data.get('pg_enrollment')
        if ug is not None or pg is not None:
            try:
                students = float(ug or 0) + float(pg or 0)
            except:
                pass
    
    if faculty is None or students is None or faculty <= 0:
        return None
    
    ratio = students / faculty
    ideal_ratio = 15.0
    
    if ratio <= ideal_ratio:
        return 100.0
    else:
        return max(0, min(100, (ideal_ratio / ratio) * 100))


def calculate_infrastructure_for_year(year_data: Dict[str, Any]) -> Optional[float]:
    """Calculate Infrastructure score for a single year's data."""
    score = 0.0
    weights_used = 0.0
    
    components = [
        ('built_up_area', 'built_up_area_num', 0.40, 10000),  # sqm
        ('classrooms', 'number_of_classrooms', 0.25, 30),
        ('library_area', 'library_area_num', 0.15, 500),
        ('lab_area', 'total_lab_area', 0.10, 1000),
        ('digital_resources', None, 0.10, 1),
    ]
    
    for field1, field2, weight, norm in components:
        value = year_data.get(field1) or year_data.get(f"{field1}_num")
        if value is None and field2:
            value = year_data.get(field2)
        
        if value is not None:
            try:
                numeric_val = float(value)
                component_score = min(100, (numeric_val / norm) * 100)
                score += component_score * weight
                weights_used += weight
            except:
                pass
    
    if weights_used == 0:
        return None
    
    # Normalize by weights used
    return min(100, score / weights_used * sum(w for _, _, w, _ in components))


def calculate_placement_for_year(year_data: Dict[str, Any]) -> Optional[float]:
    """Calculate Placement score for a single year's data."""
    placement_rate = year_data.get('placement_rate') or year_data.get('placement_rate_num')
    
    # Calculate from placed/eligible if missing
    if placement_rate is None:
        placed = year_data.get('placed_students') or year_data.get('students_placed')
        eligible = year_data.get('eligible_students') or year_data.get('students_eligible')
        if placed is not None and eligible is not None:
            try:
                placement_rate = (float(placed) / float(eligible)) * 100
            except:
                pass
    
    if placement_rate is None:
        return None
    
    try:
        rate = float(placement_rate)
        return min(100, rate)
    except:
        return None


def calculate_lab_for_year(year_data: Dict[str, Any]) -> Optional[float]:
    """Calculate Lab Compliance score for a single year's data."""
    score = 0.0
    components_found = 0
    
    lab_fields = [
        ('computer_labs', 5),
        ('science_labs', 4),
        ('engineering_labs', 6),
        ('lab_count', 10),
    ]
    
    for field, norm in lab_fields:
        value = year_data.get(field) or year_data.get(f"{field}_num")
        if value is not None:
            try:
                numeric_val = float(value)
                score += min(100, (numeric_val / norm) * 100)
                components_found += 1
            except:
                pass
    
    if components_found == 0:
        return None
    
    return score / components_found


def calculate_kpis_for_year(year_data: Dict[str, Any]) -> Dict[str, Optional[float]]:
    """Calculate all KPIs for a single year's data."""
    fsr = calculate_fsr_for_year(year_data)
    infra = calculate_infrastructure_for_year(year_data)
    placement = calculate_placement_for_year(year_data)
    lab = calculate_lab_for_year(year_data)
    
    # Filter out exactly 0 values - treat as invalid/missing
    if fsr is not None and fsr == 0:
        fsr = None
    if infra is not None and infra == 0:
        infra = None
    if placement is not None and placement == 0:
        placement = None
    if lab is not None and lab == 0:
        lab = None
    
    # Calculate overall only if we have at least 2 valid KPIs
    valid_kpis = [(kpi, weight) for kpi, weight in [
        (fsr, 0.25), (infra, 0.25), (placement, 0.30), (lab, 0.20)
    ] if kpi is not None and kpi > 0]  # Only include KPIs > 0
    
    overall = None
    if len(valid_kpis) >= 2:
        total_weight = sum(w for _, w in valid_kpis)
        overall = sum(v * w for v, w in valid_kpis) / total_weight
    
    return {
        'fsr_score': fsr,
        'infrastructure_score': infra,
        'placement_index': placement,
        'lab_compliance_index': lab,
        'overall_score': overall,
    }


def calculate_slope(values: List[float], years: List[int]) -> float:
    """Calculate trend slope (change per year)."""
    if len(values) < 2:
        return 0.0
    
    n = len(years)
    if n < 2:
        return 0.0
    
    return (values[-1] - values[0]) / (years[-1] - years[0]) if years[-1] != years[0] else 0.0


def calculate_volatility(values: List[float]) -> float:
    """Calculate volatility (standard deviation)."""
    if len(values) < 2:
        return 0.0
    return stdev(values)


def generate_insight(kpi_name: str, slope: float, volatility: float, values: List[float]) -> str:
    """Generate human-readable insight for a KPI trend."""
    if not values:
        return "No data available"
    
    avg = mean(values) if values else 0
    
    if slope > 3:
        trend = "📈 Strong Growth"
    elif slope > 0.5:
        trend = "↗️ Moderate Growth"
    elif slope < -3:
        trend = "📉 Significant Decline"
    elif slope < -0.5:
        trend = "↘️ Slight Decline"
    else:
        trend = "➡️ Stable"
    
    if volatility > 10:
        stability = "Highly Irregular"
    elif volatility > 5:
        stability = "Moderate Fluctuations"
    elif volatility < 2:
        stability = "Very Consistent"
    else:
        stability = "Fairly Stable"
    
    return f"{trend} ({slope:+.1f}/year), {stability} (±{volatility:.1f})"


def process_yearwise_kpis(blocks: List[Dict[str, Any]], mode: str = "aicte") -> Dict[str, Any]:
    """
    Main function: Process all blocks and return year-wise KPIs with trends.
    
    Returns:
    {
        "years_available": [2021, 2022, 2023, ...],
        "kpis_per_year": {
            2021: {"fsr_score": 85, ...},
            2022: {"fsr_score": 87, ...},
            ...
        },
        "trends": {
            "fsr_score": {"slope": 1.5, "volatility": 2.3, "insight": "..."},
            ...
        },
        "has_historical_data": true/false
    }
    """
    # Collect all year data from all blocks
    all_year_data: Dict[int, Dict[str, Any]] = {}
    
    for block in blocks:
        block_data = block.get('extracted_data') or block.get('data', {})
        if not block_data:
            continue
        
        year_data = extract_years_from_block(block_data)
        
        for year, data in year_data.items():
            if year not in all_year_data:
                all_year_data[year] = {}
            # Merge data, newer values override
            all_year_data[year].update(data)
    
    # Filter years with sufficient data (at least 2 meaningful numeric fields)
    valid_years = {}
    for year, data in all_year_data.items():
        numeric_count = sum(1 for v in data.values() if isinstance(v, (int, float)) and v > 0)
        if numeric_count >= 2:
            valid_years[year] = data
    
    if not valid_years:
        return {
            "years_available": [],
            "kpis_per_year": {},
            "trends": {},
            "has_historical_data": False,
        }
    
    # Calculate KPIs per year
    years_sorted = sorted(valid_years.keys())
    kpis_per_year = {}
    
    for year in years_sorted:
        kpis_per_year[year] = calculate_kpis_for_year(valid_years[year])
    
    # Calculate trends for each KPI
    kpi_names = ['fsr_score', 'infrastructure_score', 'placement_index', 'lab_compliance_index', 'overall_score']
    trends = {}
    
    for kpi_name in kpi_names:
        values = []
        years_with_data = []
        
        for year in years_sorted:
            val = kpis_per_year[year].get(kpi_name)
            # Filter out 0 values - treat as invalid
            if val is not None and val > 0:
                values.append(val)
                years_with_data.append(year)
        
        if len(values) >= 2:
            slope = calculate_slope(values, years_with_data)
            volatility = calculate_volatility(values)
            insight = generate_insight(kpi_name, slope, volatility, values)
            
            trends[kpi_name] = {
                "slope": round(slope, 2),
                "volatility": round(volatility, 2),
                "min": round(min(values), 2),
                "max": round(max(values), 2),
                "avg": round(mean(values), 2),
                "insight": insight,
                "data_points": len(values),
            }
        else:
            trends[kpi_name] = {
                "slope": 0,
                "volatility": 0,
                "insight": "Insufficient historical data",
                "data_points": len(values),
            }
    
    return {
        "years_available": years_sorted,
        "kpis_per_year": {str(k): v for k, v in kpis_per_year.items()},
        "trends": trends,
        "has_historical_data": len(years_sorted) >= 2,
    }


def get_trend_chart_data(kpis_per_year: Dict, kpi_name: str) -> List[Dict]:
    """
    Get chart-ready data for a specific KPI.
    Returns: [{"year": 2021, "value": 85}, ...]
    """
    chart_data = []
    for year_str, kpis in kpis_per_year.items():
        val = kpis.get(kpi_name)
        if val is not None:
            chart_data.append({
                "year": int(year_str),
                "value": round(val, 2),
            })
    return sorted(chart_data, key=lambda x: x["year"])
