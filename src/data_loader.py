"""Data loading and splitting utilities."""
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.config import DATA_DIR, TEST_SIZE, RANDOM_STATE, TARGET_COLUMN


def load_data(file_name: str = "sensor_data.csv") -> pd.DataFrame:
    """Load sensor data from CSV."""
    file_path = DATA_DIR / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    return pd.read_csv(file_path)


def split_data(df: pd.DataFrame):
    """Split data into train/test sets."""
    X = df.drop(columns=[TARGET_COLUMN, "engine_id", "cycle"])
    y = df[TARGET_COLUMN]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    return X_train, X_test, y_train, y_test
