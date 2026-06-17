from pathlib import Path

# Project root folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data folders
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REFERENCE_DATA_DIR = DATA_DIR / "reference"

# Model folder
MODELS_DIR = PROJECT_ROOT / "models"

# Random seed for reproducibility
RANDOM_SEED = 42

# Number of synthetic household records to generate
N_HOUSEHOLDS = 1500