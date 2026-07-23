"""Main data cleaning orchestrator."""
import pandas as pd
from src.validators import DataValidator
from src.outlier_detector import OutlierDetector
from src.transformers import DataTransformer
from src.reporter import CleaningReporter


class DataCleaner:
    """Orchestrate the full data cleaning pipeline."""
    
    def __init__(self):
        self.validator = DataValidator()
        self.outlier_detector = OutlierDetector()
        self.transformer = DataTransformer()
        self.reporter = CleaningReporter()
        self.numeric_cols = ["temperature", "pressure", "vibration", "rpm"]
    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Run the complete cleaning pipeline."""
        print(f"\n🔧 Starting cleaning pipeline on {len(df)} records...")
        
        # Step 1: Pre-clean validation
        pre_validation = self.validator.full_validation(df)
        self.reporter.log("Pre-clean validation", pre_validation)
        
        # Step 2: Remove exact duplicates
        before = len(df)
        df = df.drop_duplicates()
        print(f"   ✓ Removed {before - len(df)} duplicates")
        
        # Step 3: Coerce numeric types
        df = self.transformer.coerce_numeric(df, self.numeric_cols)
        print(f"   ✓ Coerced numeric columns")
        
        # Step 4: Handle timestamps
        df = self.transformer.handle_timestamps(df)
        print(f"   ✓ Parsed timestamps")
        
        # Step 5: Normalize categories
        status_mapping = {
            "normal": "normal", "warning": "warning", "critical": "critical",
            "unknown": "normal", "error": "critical", "": "normal",
        }
        df = self.transformer.normalize_categories(df, "status", status_mapping)
        print(f"   ✓ Normalized categorical values")
        
        # Step 6: Detect and handle outliers
        df = self.outlier_detector.detect_combined(df, self.numeric_cols)
        outlier_cols = [f"{c}_outlier" for c in self.numeric_cols]
        outlier_mask = df[outlier_cols].any(axis=1)
        n_outliers = outlier_mask.sum()
        df.loc[outlier_mask, self.numeric_cols] = np.nan
        print(f"   ✓ Flagged and nullified {n_outliers} outliers")
        
        # Step 7: Fill missing values (per engine, forward fill then median)
        df = df.sort_values(["engine_id", "timestamp"])
        df = df.groupby("engine_id", group_keys=False).apply(
            lambda g: self.transformer.fill_missing(g, strategy="interpolate",
                                                   columns=self.numeric_cols)
        )
        df = self.transformer.fill_missing(df, strategy="median",
                                          columns=self.numeric_cols)
        print(f"   ✓ Filled missing values")
        
        # Step 8: Add derived features
        df = self.transformer.add_derived_features(df)
        print(f"   ✓ Added derived features")
        
        # Step 9: Drop outlier flag columns
        df = df.drop(columns=outlier_cols, errors="ignore")
        
        # Step 10: Reset index
        df = df.reset_index(drop=True)
        
        # Post-clean validation
        post_validation = self.validator.full_validation(df)
        self.reporter.log("Post-clean validation", post_validation)
        
        print(f"\n✅ Cleaning complete! Final dataset: {len(df)} records")
        return df
