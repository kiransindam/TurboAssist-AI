"""Run inference on new data."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd
from src.predictor import Predictor
from src.feature_engineering import engineer_features


def main():
    # Sample new engine data
    new_data = pd.DataFrame({
        "engine_id": [999] * 3,
        "cycle": [1, 2, 3],
        "temperature": [510, 520, 535],
        "pressure": [1980, 1960, 1940],
        "vibration": [2.6, 2.8, 3.1],
        "rpm": [9900, 9850, 9800],
        "oil_pressure": [59, 58, 57],
    })
    
    # Engineer features
    new_data_eng = engineer_features(new_data)
    X = new_data_eng.drop(columns=["engine_id", "cycle", "RUL"], errors="ignore")
    
    # Predict
    predictor = Predictor("xgboost")
    preds, lower, upper = predictor.predict_with_confidence(X)
    
    print("\n🔮 Predictions for Engine #999:")
    print("-" * 60)
    for i, (cycle, pred) in enumerate(zip(new_data["cycle"], preds)):
        ci = f"[{lower[i]:.1f}, {upper[i]:.1f}]" if lower is not None else "N/A"
        print(f"Cycle {cycle}: RUL = {pred:.1f} cycles  (95% CI: {ci})")


if __name__ == "__main__":
    main()
