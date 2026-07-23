"""Model training pipeline with multiple algorithms."""
import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor
from src.config import MODEL_DIR, RANDOM_STATE


class ModelTrainer:
    """Train and save multiple regression models."""
    
    def __init__(self):
        self.models = {
            "ridge": Ridge(alpha=1.0, random_state=RANDOM_STATE),
            "random_forest": RandomForestRegressor(
                n_estimators=100, max_depth=10, random_state=RANDOM_STATE, n_jobs=-1
            ),
            "xgboost": XGBRegressor(
                n_estimators=200, max_depth=6, learning_rate=0.1,
                random_state=RANDOM_STATE, n_jobs=-1
            ),
        }
        self.trained_models = {}
    
    def train_all(self, X_train, y_train):
        """Train all models."""
        for name, model in self.models.items():
            print(f"Training {name}...")
            model.fit(X_train, y_train)
            self.trained_models[name] = model
        return self.trained_models
    
    def save_best(self, best_model_name: str):
        """Save the best model to disk."""
        model = self.trained_models[best_model_name]
        path = MODEL_DIR / f"{best_model_name}.joblib"
        joblib.dump(model, path)
        print(f"✅ Saved best model to {path}")
        return path
