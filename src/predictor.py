"""Model inference / prediction."""
import joblib
import pandas as pd
import numpy as np
from src.config import MODEL_DIR


class Predictor:
    """Load model and make predictions."""
    
    def __init__(self, model_name: str = "xgboost"):
        model_path = MODEL_DIR / f"{model_name}.joblib"
        self.model = joblib.load(model_path)
        self.model_name = model_name
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict RUL for input features."""
        return self.model.predict(X)
    
    def predict_with_confidence(self, X: pd.DataFrame):
        """Predict with confidence interval (using tree-based variance)."""
        predictions = self.predict(X)
        
        # For tree ensembles, use individual tree predictions for CI
        if hasattr(self.model, "estimators_"):
            tree_preds = np.array([
                tree.predict(X) for tree in self.model.estimators_
            ])
            mean_pred = tree_preds.mean(axis=0)
            std_pred = tree_preds.std(axis=0)
            lower = mean_pred - 1.96 * std_pred
            upper = mean_pred + 1.96 * std_pred
            return mean_pred, lower, upper
        
        return predictions, None, None
