"""Main entry point for data cleaning."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from data.generate_dirty_data import generate_dirty_data
from src.cleaner import DataCleaner
from src.reporter import CleaningReporter


def main():
    # Generate dirty data if not exists
    data_path = Path("data/dirty_sensor_data.csv")
    if not data_path.exists():
        print("📊 Generating dirty sensor data...")
        generate_dirty_data()
    
    # Load dirty data
    print("\n📥 Loading dirty data...")
    df_dirty = pd.read_csv(data_path)
    print(f"   Original: {len(df_dirty)} records")
    print(f"   Missing values: {df_dirty.isnull().sum().sum()}")
    
    # Clean
    cleaner = DataCleaner()
    df_clean = cleaner.clean(df_dirty)
    
    # Generate report
    reporter = cleaner.reporter
    summary = reporter.generate_summary(df_dirty, df_clean)
    
    # Save cleaned data
    output_path = Path("data/clean_sensor_data.csv")
    df_clean.to_csv(output_path, index=False)
    print(f"\n💾 Cleaned data saved to {output_path}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("CLEANING SUMMARY")
    print("=" * 60)
    for k, v in summary.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
