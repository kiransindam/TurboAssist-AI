"""Generate intentionally dirty sensor data for cleaning demo."""
import numpy as np
import pandas as pd
from pathlib import Path


def generate_dirty_data(n_records: int = 1000) -> pd.DataFrame:
    """Generate sensor data with various quality issues."""
    np.random.seed(42)
    
    data = {
        "engine_id": np.random.randint(1, 51, n_records),
        "timestamp": pd.date_range("2024-01-01", periods=n_records, freq="H"),
        "temperature": np.random.normal(550, 30, n_records),
        "pressure": np.random.normal(1800, 100, n_records),
        "vibration": np.random.normal(3.5, 0.8, n_records),
        "rpm": np.random.normal(9500, 300, n_records),
        "status": np.random.choice(["normal", "warning", "critical"], n_records, p=[0.8, 0.15, 0.05]),
    }
    df = pd.DataFrame(data)
    
    # Inject various data quality issues
    # 1. Missing values (5-10%)
    for col in ["temperature", "pressure", "vibration"]:
        mask = np.random.rand(n_records) < 0.07
        df.loc[mask, col] = np.nan
    
    # 2. Duplicates (3%)
    dup_idx = np.random.choice(df.index, size=int(n_records * 0.03), replace=False)
    df = pd.concat([df, df.iloc[dup_idx]], ignore_index=True)
    
    # 3. Outliers (2%)
    outlier_idx = np.random.choice(df.index, size=int(len(df) * 0.02), replace=False)
    df.loc[outlier_idx, "temperature"] = np.random.choice([-100, 2000, 5000], len(outlier_idx))
    
    # 4. Invalid categorical values
    invalid_idx = np.random.choice(df.index, size=10, replace=False)
    df.loc[invalid_idx, "status"] = np.random.choice(["unknown", "ERROR", "", "Normal "], 10)
    
    # 5. Type issues (string in numeric)
    df.loc[5, "rpm"] = "9500 rpm"
    df.loc[15, "temperature"] = "N/A"
    
    # 6. Negative values in impossible fields
    df.loc[20:25, "vibration"] = -5.0
    
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    output_path = Path(__file__).parent / "dirty_sensor_data.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} dirty records → {output_path}")
    return df


if __name__ == "__main__":
    generate_dirty_data()
