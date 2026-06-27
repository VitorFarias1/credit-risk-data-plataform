from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "german_credit_data.csv"
)

TRUSTED_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "trusted"
    / "german_credit.parquet"
)