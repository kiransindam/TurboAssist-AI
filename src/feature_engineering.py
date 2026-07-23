"""Feature engineering for time-series sensor data."""
import pandas as pd
import numpy as np
from src.config import WINDOW_SIZE, ROLLING_STATS


def add_rolling_features(df: pd.DataFrame, group_col: str = "engine_id") -> pd.DataFrame:
    """Add rolling window statistics per engine."""
    sensor_cols = ["temperature", "pressure", "vibration", "rpm", "oil_pressure"]
    result_dfs = []
    
    for engine_id, group in df.groupby(group_col):
        group = group.sort_values("cycle").copy()
        
        for col in sensor_cols:
            for stat in ROLLING_STATS:
                rolling = group[col].rolling(window=WINDOW_SIZE, min_periods=1)
                new_col = f"{col}_rolling_{stat}"
                if stat == "mean":
                    group[new_col] = rolling.mean()
                elif stat == "std":
                    group[new_col] = rolling.std().fillna(0)
                elif stat == "min":
                    group[new_col] = rolling.min()
                elif stat == "max":
                    group[new_col] = rolling.max()
        
        result_dfs.append(group)
    
    return pd.concat(result_dfs, ignore_index=True)


def add_degradation_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived features capturing degradation patterns."""
    df = df.copy()
    # Interaction features
    df["temp_pressure_ratio"] = df["temperature"] / (df["pressure"] + 1e-6)
    df["vibration_rpm_ratio"] = df["vibration"] / (df["rpm"] + 1e-6)
    # Exponential moving average
    for col in ["temperature", "vibration"]:
        df[f"{col}_ema"] = df.groupby("engine_id")[col].transform(
            lambda x: x.ewm(span=5, min_periods=1).mean()
        )
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Full feature engineering pipeline."""
    df = add_rolling_features(df)
    df = add_degradation_features(df)
    # Drop NaN from rolling windows
    df = df.dropna()
    return df
