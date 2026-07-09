import duckdb

from credit_pipeline.config import WAREHOUSE_DB_PATH

def get_connection():
    WAREHOUSE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    return duckdb.connect(str(WAREHOUSE_DB_PATH))