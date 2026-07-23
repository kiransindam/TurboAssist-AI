"""Generate synthetic turbomachinery sensor data for training."""
import numpy as np
import pandas as pd
from pathlib import Path


def generate_sensor_data(n_engines: int = 100, seq_length: int = 100) -> pd.DataFrame:
    """
    Generate synthetic sensor data simulating turbomachinery degradation.
    
    Features simulate: temperature, pressure, vibration, RPM, oil pressure
    RUL (Remaining Useful Life) decreases as engine degrades.
    """
    np.random.seed(42)
    records = []
    
    for engine_id in range(1, n_engines + 1):
        # Random lifespan for this engine
        lifespan = np.random.randint(seq_length // 2, seq_length * 2)
        
        for cycle in range(1, lifespan + 1):
            # Degradation factor (0 to 1)
            degradation = cycle / lifespan
            
            # Sensor readings with degradation trend + noise
            temperature = 500 + (150 * degradation) + np.random.normal(0, 10)
            pressure = 2000 - (400 * degradation) + np.random.normal(0, 30)
            vibration = 2.5 + (5.0 * degradation) + np.random.normal(0, 0.3)
            rpm = 10000 - (1500 * degradation) + np.random.normal(0, 100)
            oil_pressure = 60 - (20 * degradation) + np.random.normal(0, 2)
            
            # RUL = remaining cycles
            rul = lifespan - cycle
            
            records.append({
                "engine_id": engine_id,
                "cycle": cycle,
                "temperature": round(temperature, 2),
                "pressure": round(pressure, 2),
                "vibration": round(vibration, 2),
                "rpm": round(rpm, 2),
                "oil_pressure": round(oil_pressure, 2),
                "RUL": rul,
            })
    
    return pd.DataFrame(records)


if __name__ == "__main__":
    df = generate_sensor_data(n_engines=100, seq_length=100)
    output_path = Path(__file__).parent / "sensor_data.csv"
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {len(df)} records for {df['engine_id'].nunique()} engines")
    print(f"Saved to: {output_path}")
