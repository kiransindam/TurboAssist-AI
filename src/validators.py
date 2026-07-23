"""Data validation rules."""
import pandas as pd
from typing import Dict, List


class DataValidator:
    """Validate data against business rules."""
    
    def __init__(self):
        self.rules = {
            "temperature": {"min": 100, "max": 1200, "unit": "celsius"},
            "pressure": {"min": 500, "max": 3000, "unit": "psi"},
            "vibration": {"min": 0, "max": 15, "unit": "mm/s"},
            "rpm": {"min": 0, "max": 15000, "unit": "rpm"},
        }
        self.valid_statuses = {"normal", "warning", "critical"}
    
    def validate_schema(self, df: pd.DataFrame) -> Dict:
        """Check required columns exist."""
        required = ["engine_id", "timestamp", "temperature", "pressure", 
                    "vibration", "rpm", "status"]
        missing = [c for c in required if c not in df.columns]
        return {"valid": len(missing) == 0, "missing_columns": missing}
    
    def validate_ranges(self, df: pd.DataFrame) -> Dict:
        """Check numeric values are within valid ranges."""
        violations = {}
        for col, rules in self.rules.items():
            if col not in df.columns:
                continue
            valid = df[col].dropna()
            out_of_range = valid[(valid < rules["min"]) | (valid > rules["max"])]
            violations[col] = {
                "count": len(out_of_range),
                "min_valid": rules["min"],
                "max_valid": rules["max"],
            }
        return violations
    
    def validate_categories(self, df: pd.DataFrame) -> Dict:
        """Check categorical values."""
        if "status" not in df.columns:
            return {}
        invalid = df[~df["status"].isin(self.valid_statuses)]["status"]
        return {
            "invalid_count": len(invalid),
            "invalid_values": invalid.value_counts().to_dict(),
        }
    
    def full_validation(self, df: pd.DataFrame) -> Dict:
        """Run all validations."""
        return {
            "schema": self.validate_schema(df),
            "ranges": self.validate_ranges(df),
            "categories": self.validate_categories(df),
            "row_count": len(df),
            "column_count": len(df.columns),
        }
