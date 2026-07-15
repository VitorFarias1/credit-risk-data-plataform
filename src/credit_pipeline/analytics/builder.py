from pathlib import Path

class AnalyticsBuilder:

    def __init__(self, connection):
        self.connection = connection

    def execute_sql_file(self, sql_path: Path):

        sql = sql_path.read_text()

        self.connection.execute(sql)

        print(f"Executed: {sql_path.name}")