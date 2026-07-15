from pathlib import Path

from credit_pipeline.warehouse.database import get_connection
from credit_pipeline.analytics.builder import AnalyticsBuilder


SQL_FOLDER = (
    Path(__file__).parent
    / "sql"
)


def main():

    print("Building Analytics Layer...")

    conn = get_connection()

    builder = AnalyticsBuilder(conn)

    for sql_file in sorted(SQL_FOLDER.glob("*.sql")):
        builder.execute_sql_file(sql_file)

    conn.close()

    print("Analytics Layer Completed.")


if __name__ == "__main__":
    main()