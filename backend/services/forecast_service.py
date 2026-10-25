"""
Forecast Engine - Statistical Model for Multi-Year Predictions
Requires minimum 3 years of real historical data
Provides confidence bands and explanations
"""

from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
import json
import math

logger = logging.getLogger(__name__)


def _get_val(obj: Any, key: str, default: Any = None) -> Any:
    """Helper to safely get a value from either a dict or an object attribute."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


class ForecastService:
    """
    Forecast service for KPI predictions
    Uses simple linear regression for explainability
    Requires minimum 3 years of historical data
    """
    
    def __init__(self):
        pass
    
    def forecast_kpi(
        self,
        historical_data: List[Any],  # [{year, value}, ...]
        forecast_years: int = 3,
        kpi_name: str = "overall_score"
    ) -> Dict[str, Any]:
        """
        Forecast KPI values for future years using linear regression.
        
        Args:
            historical_data: List of {year: int, value: float} dicts or objects
            forecast_years: Number of years to forecast ahead
            kpi_name: Name of KPI being forecasted
            
        Returns:
            {
                "has_forecast": bool,
                "can_forecast": bool,
                "insufficient_data": bool,
                "forecast": [{year, predicted_value, lower_bound, upper_bound}],
                "confidence_band": float,  # 0-1
                "explanation": str,
                "insufficient_data_reason": str (if can_forecast=False)
            }
        """
        # Ensure forecast_years is a valid positive integer
        try:
            forecast_years = int(forecast_years)
            if forecast_years <= 0:
                forecast_years = 3
        except (ValueError, TypeError):
            forecast_years = 3

        # Validate input list
        if not historical_data or len(historical_data) < 3:
            count = len(historical_data) if historical_data else 0
            return {
                "has_forecast": False,
                "can_forecast": False,
                "insufficient_data": True,
                "forecast": None,
                "confidence_band": 0.0,
                "explanation": None,
                "insufficient_data_reason": f"Insufficient data: {count} year(s) available, need at least 3 years for forecasting"
            }
        
        try:
            # Filter out None/null values safely supporting both dicts and objects
            valid_data = []
            for point in historical_data:
                val = _get_val(point, "value")
                yr = _get_val(point, "year")
                if val is not None and isinstance(val, (int, float)) and yr is not None:
                    try:
                        valid_data.append({"year": int(yr), "value": float(val)})
                    except (ValueError, TypeError):
                        continue
            
            if len(valid_data) < 3:
                return {
                    "has_forecast": False,
                    "can_forecast": False,
                    "insufficient_data": True,
                    "forecast": None,
                    "confidence_band": 0.0,
                    "explanation": None,
                    "insufficient_data_reason": f"Insufficient valid data: {len(valid_data)} valid point(s), need at least 3 for forecasting"
                }
            
            # Sort chronologically
            valid_data.sort(key=lambda p: p["year"])

            # Extract years and values
            years = [point["year"] for point in valid_data]
            values = [point["value"] for point in valid_data]
            
            # Calculate linear regression
            slope, intercept, r_squared = self._linear_regression(years, values)
            
            # Calculate confidence band (based on R² and data spread)
            confidence_band = min(0.95, max(0.5, r_squared))
            
            # Get last year
            last_year = max(years)
            
            # Generate forecast for next N years
            forecast_points = []
            for i in range(1, forecast_years + 1):
                forecast_year = last_year + i
                predicted_value = slope * forecast_year + intercept
                
                # Calculate confidence interval (standard error)
                std_error = self._calculate_standard_error(years, values, slope, intercept)
                margin = std_error * 1.96  # 95% confidence interval
                
                forecast_points.append({
                    "year": forecast_year,
                    "predicted_value": round(predicted_value, 2),
                    "lower_bound": round(max(0, predicted_value - margin), 2),
                    "upper_bound": round(min(100, predicted_value + margin), 2),
                    "confidence": round(confidence_band, 2)
                })
            
            # Generate explanation
            trend_direction = "increasing" if slope > 0.05 else "decreasing" if slope < -0.05 else "stable"
            explanation = (
                f"Forecast based on {len(valid_data)} years of historical data. "
                f"Trend shows {trend_direction} pattern (slope: {slope:.2f} per year). "
                f"Confidence: {confidence_band:.0%} (R² = {r_squared:.3f}). "
                f"Forecast range accounts for historical variability."
            )
            
            return {
                "has_forecast": True,
                "can_forecast": True,
                "insufficient_data": False,
                "forecast": forecast_points,
                "confidence_band": confidence_band,
                "explanation": explanation,
                "insufficient_data_reason": None,
                "model_info": {
                    "method": "linear_regression",
                    "slope": round(slope, 4),
                    "intercept": round(intercept, 4),
                    "r_squared": round(r_squared, 4),
                    "historical_points": len(valid_data)
                }
            }
            
        except Exception as e:
            logger.error(f"Forecast calculation error: {e}", exc_info=True)
            return {
                "has_forecast": False,
                "can_forecast": False,
                "insufficient_data": True,
                "forecast": None,
                "confidence_band": 0.0,
                "explanation": None,
                "insufficient_data_reason": f"Forecast calculation failed: {str(e)}"
            }
    
    def _linear_regression(self, x: List[int], y: List[float]) -> Tuple[float, float, float]:
        """
        Simple linear regression: y = mx + b
        Returns: (slope, intercept, r_squared)
        """
        n = len(x)
        if n < 2:
            return 0.0, 0.0, 0.0
        
        # Calculate means
        x_mean = sum(x) / n
        y_mean = sum(y) / n
        
        # Calculate slope and intercept
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0, y_mean, 0.0
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # Calculate R² (coefficient of determination)
        y_pred = [slope * x[i] + intercept for i in range(n)]
        ss_res = sum((y[i] - y_pred[i]) ** 2 for i in range(n))
        ss_tot = sum((y[i] - y_mean) ** 2 for i in range(n))
        
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        
        return slope, intercept, r_squared
    
    def _calculate_standard_error(self, x: List[int], y: List[float], slope: float, intercept: float) -> float:
        """Calculate standard error of regression"""
        n = len(x)
        if n <= 2:
            return 0.0
        
        y_pred = [slope * x[i] + intercept for i in range(n)]
        residuals = [y[i] - y_pred[i] for i in range(n)]
        
        # Sum of squared residuals
        ss_res = sum(r ** 2 for r in residuals)
        
        # Standard error
        std_error = math.sqrt(ss_res / (n - 2)) if n > 2 else 0.0
        
        return std_error
    
    def forecast_department_kpi(
        self,
        institution_name: str,
        department_name: str,
        kpi_name: str,
        historical_batches: List[Any]  # Batches (SQLAlchemy models or dicts) with same institution+department
    ) -> Dict[str, Any]:
        """
        Forecast KPI for a specific department based on historical batches.
        
        Args:
            institution_name: Institution name
            department_name: Department name
            kpi_name: KPI to forecast (e.g., "overall_score", "fsr_score")
            historical_batches: List of Batch objects or dicts with kpi_results and academic_year
            
        Returns:
            Forecast result with can_forecast and has_forecast flags
        """
        historical_data = []
        
        for batch in historical_batches:
            # Skip invalid batches
            is_inv = _get_val(batch, "is_invalid", 0)
            if is_inv == 1:
                continue
            
            # Extract academic year
            academic_year = _get_val(batch, "academic_year")
            if not academic_year:
                continue
            
            # Parse year (e.g., "2024-25" -> 2024, "2023" -> 2023)
            try:
                year_str = str(academic_year).split("-")[0].strip()
                year = int(year_str)
            except Exception:
                continue
            
            # Extract KPI value
            kpi_results = _get_val(batch, "kpi_results", {})
            if isinstance(kpi_results, str):
                try:
                    kpi_results = json.loads(kpi_results)
                except Exception:
                    kpi_results = {}
            if not isinstance(kpi_results, dict):
                kpi_results = {}
            
            kpi_value = None
            if isinstance(kpi_results.get(kpi_name), dict):
                kpi_value = kpi_results[kpi_name].get("value")
            elif kpi_name in kpi_results:
                kpi_value = kpi_results[kpi_name]
            
            # Fallback for overall_score directly from batch column
            if kpi_value is None and kpi_name == "overall_score":
                overall = _get_val(batch, "overall_score")
                if overall is not None:
                    kpi_value = overall

            if kpi_value is not None and isinstance(kpi_value, (int, float)):
                historical_data.append({
                    "year": year,
                    "value": float(kpi_value)
                })
        
        # Sort by year
        historical_data.sort(key=lambda x: x["year"])
        
        # Forecast
        return self.forecast_kpi(historical_data, forecast_years=3, kpi_name=kpi_name)
