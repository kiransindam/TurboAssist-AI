"""Model evaluation metrics and reporting."""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_model(y_true, y_pred, model_name: str) -> dict:
    """Compute evaluation metrics."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    # Score-based metric (common in predictive maintenance)
    score = _compute_score(y_true, y_pred)
    
    return {
        "model": model_name,
        "MAE": round(mae, 3),
        "RMSE": round(rmse, 3),
        "R2": round(r2, 4),
        "Score": round(score, 2),
    }


def _compute_score(y_true, y_pred) -> float:
    """Asymmetric score penalizing late predictions more than early ones."""
    errors = y_pred - y_true
    score = np.sum(np.where(errors < 0, np.exp(-errors / 13) - 1,
                            np.exp(errors / 10) - 1))
    return score


def compare_models(results: list) -> pd.DataFrame:
    """Compare all models and rank by score."""
    df = pd.DataFrame(results).sort_values("Score")
    print("\n=== Model Comparison ===")
    print(df.to_string(index=False))
    return df
