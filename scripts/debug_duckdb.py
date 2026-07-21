from credit_pipeline.warehouse.database import get_connection

conn = get_connection()

print("Connected!")

print("\nSchemas:")
print(conn.execute("SELECT schema_name FROM information_schema.schemata").fetchdf())

print("\nTables:")
print(conn.execute("""
SELECT table_schema, table_name
FROM information_schema.tables
ORDER BY table_schema, table_name
""").fetchdf())

conn.close()