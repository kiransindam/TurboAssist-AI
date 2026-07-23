"""Data transformation utilities."""
import pandas as pd
import numpy as np


class DataTransformer:
    """Apply common data transformations."""
    
    @staticmethod
    def coerce_numeric(df: pd.DataFrame, columns: list) -> pd.DataFrame:
        """Convert columns to numeric, replacing invalid values with NaN."""
        df = df.copy()
        for col in columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    
    @staticmethod
    def normalize_categories(df: pd.DataFrame, column: str, 
                            mapping: dict) -> pd.DataFrame:
        """Normalize categorical values."""
        df = df.copy()
        df[column] = df[column].astype(str).str.strip().str.lower()
        df[column] = df[column].replace(mapping)
        return df
    
    @staticmethod
    def fill_missing(df: pd.DataFrame, strategy: str = "median",
                    columns: list = None) -> pd.DataFrame:
        """Fill missing values using specified strategy."""
        df = df.copy()
        cols = columns or df.select_dtypes(include="number").columns
        
        for col in cols:
            if strategy == "median":
                df[col] = df[col].fillna(df[col].median())
            elif strategy == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif strategy == "forward":
                df[col] = df[col].ffill()
            elif strategy == "interpolate":
                df[col] = df[col].interpolate(method="linear")
        return df
    
    @staticmethod
    def handle_timestamps(df: pd.DataFrame, column: str = "timestamp") -> pd.DataFrame:
        """Parse and validate timestamp column."""
        df = df.copy()
        df[column] = pd.to_datetime(df[column], errors="coerce")
        return df
    
    @staticmethod
    def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
        """Add derived columns."""
        df = df.copy()
        if "temperature" in df.columns and "pressure" in df.columns:
            df["temp_pressure_ratio"] = df["temperature"] / (df["pressure"] + 1e-6)
        if "vibration" in df.columns and "rpm" in df.columns:
            df["vibration_per_rpm"] = df["vibration"] / (df["rpm"] + 1e-6)
        return df
