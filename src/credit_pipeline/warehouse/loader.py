import duckdb

from credit_pipeline.config import TRUSTED_DATA_PATH


class WarehouseLoader:

    def __init__(self, connection):
        self.connection = connection

    def create_schemas(self):
        self.connection.execute("CREATE SCHEMA IF NOT EXISTS raw")
        self.connection.execute("CREATE SCHEMA IF NOT EXISTS trusted")
        self.connection.execute("CREATE SCHEMA IF NOT EXISTS analytics")

    def load_trusted_table(self):
        self.connection.execute(
            """
            CREATE OR REPLACE TABLE trusted.credit AS

            SELECT *

            FROM read_parquet(?)
            """,
            [str(TRUSTED_DATA_PATH)]
        )