"""Generate cleaning reports."""
import pandas as pd
from pathlib import Path
from datetime import datetime


class CleaningReporter:
    """Generate data quality reports."""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.logs = []
    
    def log(self, stage: str, data: dict):
        """Log a cleaning stage."""
        self.logs.append({"stage": stage, "timestamp": datetime.now(), "data": data})
        print(f"   📋 Logged: {stage}")
    
    def generate_summary(self, df_before: pd.DataFrame, df_after: pd.DataFrame):
        """Generate before/after comparison report."""
        summary = {
            "original_rows": len(df_before),
            "cleaned_rows": len(df_after),
            "rows_removed": len(df_before) - len(df_after),
            "original_columns": len(df_before.columns),
            "cleaned_columns": len(df_after.columns),
            "missing_values_before": int(df_before.isnull().sum().sum()),
            "missing_values_after": int(df_after.isnull().sum().sum()),
            "duplicates_removed": len(df_before) - len(df_before.drop_duplicates()),
        }
        
        report_path = self.output_dir / f"cleaning_report_{datetime.now():%Y%m%d_%H%M%S}.txt"
        with open(report_path, "w") as f:
            f.write("=" * 60 + "\n")
            f.write("DATA CLEANING REPORT\n")
            f.write("=" * 60 + "\n\n")
            for k, v in summary.items():
                f.write(f"{k}: {v}\n")
            f.write("\n" + "=" * 60 + "\n")
            f.write("CLEANING LOG\n")
            f.write("=" * 60 + "\n")
            for log in self.logs:
                f.write(f"\n[{log['timestamp']}] {log['stage']}\n")
                f.write(f"{log['data']}\n")
        
        print(f"\n📄 Report saved to {report_path}")
        return summary
