"""Exploratory Data Analysis utilities."""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def generate_eda_report(df: pd.DataFrame, output_dir: Path):
    """Generate EDA visualizations and statistics."""
    output_dir.mkdir(exist_ok=True)
    
    # 1. Basic statistics
    stats = df.describe()
    stats.to_csv(output_dir / "statistics.csv")
    
    # 2. Missing values
    missing = df.isnull().sum()
    missing.to_csv(output_dir / "missing_values.csv")
    
    # 3. Correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.select_dtypes(include="number").corr(), annot=True, cmap="coolwarm")
    plt.title("Feature Correlation")
    plt.tight_layout()
    plt.savefig(output_dir / "correlation_heatmap.png", dpi=100)
    plt.close()
    
    # 4. RUL distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df["RUL"], bins=50, kde=True)
    plt.title("RUL Distribution")
    plt.xlabel("Remaining Useful Life (cycles)")
    plt.savefig(output_dir / "rul_distribution.png", dpi=100)
    plt.close()
    
    # 5. Sensor trends over cycles
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    sensors = ["temperature", "pressure", "vibration", "rpm"]
    for ax, sensor in zip(axes.flatten(), sensors):
        sample = df[df["engine_id"] == 1]
        ax.plot(sample["cycle"], sample[sensor])
        ax.set_title(f"{sensor.capitalize()} vs Cycle")
        ax.set_xlabel("Cycle")
    plt.tight_layout()
    plt.savefig(output_dir / "sensor_trends.png", dpi=100)
    plt.close()
    
    print(f"✅ EDA report saved to {output_dir}")
    return stats
