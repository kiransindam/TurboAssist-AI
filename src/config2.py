"""Configuration for ML pipeline."""
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

# Model parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2
TARGET_COLUMN = "RUL"

# Feature engineering
WINDOW_SIZE = 10
ROLLING_STATS = ["mean", "std", "min", "max"]
