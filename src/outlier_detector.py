"""Outlier detection using multiple methods."""
import numpy as np
import pandas as pd


class OutlierDetector:
    """Detect outliers using IQR and Z-score methods."""
    
    def __init__(self, z_threshold: float = 3.0, iqr_multiplier: float = 1.5):
        self.z_threshold = z_threshold
        self.iqr_multiplier = iqr_multiplier
    
    def detect_iqr(self, series: pd.Series) -> pd.Series:
        """Detect outliers using IQR method."""
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - self.iqr_multiplier * IQR
        upper = Q3 + self.iqr_multiplier * IQR
        return (series < lower) | (series > upper)
    
    def detect_zscore(self, series: pd.Series) -> pd.Series:
        """Detect outliers using Z-score method."""
        mean = series.mean()
        std = series.std()
        z_scores = np.abs((series - mean) / std)
        return z_scores > self.z_threshold
    
    def detect_combined(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Flag outliers using both methods."""
        df = df.copy()
        for col in columns:
            if col not in df.columns:
                continue
            iqr_outliers = self.detect_iqr(df[col].dropna())
            z_outliers = self.detect_zscore(df[col].dropna())
            
            # Mark as outlier if flagged by either method
            df[f"{col}_outlier"] = False
            df.loc[iqr_outliers.index, f"{col}_outlier"] = iqr_outliers
            df.loc[z_outliers.index, f"{col}_outlier"] |= z_outliers
        
        return df
