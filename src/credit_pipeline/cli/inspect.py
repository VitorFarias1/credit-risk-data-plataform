from credit_pipeline.warehouse.database import get_connection


def main():
    conn = get_connection()

    print("\n=== TABLES ===")
    print(conn.sql("SHOW ALL TABLES").fetchdf())

    print("\n=== SAMPLE ===")
    print(conn.sql("""
        SELECT *
        FROM trusted.credit
        LIMIT 5
    """).fetchdf())

    print("\n=== ROW COUNT ===")
    print(conn.sql("""
        SELECT COUNT(*) AS total
        FROM trusted.credit
    """).fetchdf())

    conn.close()


if __name__ == "__main__":
    main()