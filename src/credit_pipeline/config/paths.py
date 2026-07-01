from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"
TRUSTED_DIR = DATA_DIR / "trusted"
ANALYTICS_DIR = DATA_DIR / "analytics"
WAREHOUSE_DIR = DATA_DIR / "warehouse"

DOCS_DIR = PROJECT_ROOT / "docs"

TESTS_DIR = PROJECT_ROOT / "tests"

RAW_DATA_PATH = RAW_DIR / "german_credit_data.csv"

RAW_PARQUET_PATH = TRUSTED_DIR / "german_credit.parquet"

TRUSTED_DATA_PATH = TRUSTED_DIR / "german_credit_trusted.parquet"

WAREHOUSE_DB_PATH = WAREHOUSE_DIR / "credit.duckdb"