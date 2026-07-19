import pytest
import yaml

from credit_pipeline.analytics.builder import AnalyticsBuilder
from credit_pipeline.analytics.load_analytics import SQL_FOLDER
from credit_pipeline.analytics.validator import AnalyticsValidator

CONTRACTS_FOLDER = SQL_FOLDER.parent / "contracts"

TABLE_NAMES = [
    "loan_purpose_summary",
    "risk_by_age",
    "housing_summary",
    "employment_summary",
]

def _duckdb_type_satisfies_contract(actual_type: str, contract_type: str) -> bool:
    """Loosely checks a DuckDB column type against a contract's declared
    type. Returns True for unrecognized contract types (nothing to check
    against).
    """
    if contract_type in ("category", "string"):
        
        return actual_type == "VARCHAR" or actual_type.startswith("ENUM(") or actual_type == "BIGINT"
    if contract_type == "integer":
        return actual_type in {"BIGINT", "INTEGER", "HUGEINT"}
    if contract_type == "double":
        return actual_type in {"DOUBLE", "FLOAT"}
    return True


@pytest.fixture
def analytics_built(duckdb_with_trusted_data):
    """Runs every real SQL file in analytics/sql against the connection
    and returns it, with all analytics tables built.
    """
    connection = duckdb_with_trusted_data
    builder = AnalyticsBuilder(connection)

    for sql_file in sorted(SQL_FOLDER.glob("*.sql")):
        builder.execute_sql_file(sql_file)

    return connection


class TestSQLFilesAreNotEmpty:
    """Regression test: employment_summary.sql and housing_summary.sql
    used to be empty files. DuckDB silently executes an empty string as
    a no-op, so AnalyticsBuilder reported "Executed" without creating
    the table, and the failure only surfaced later, in validation.
    """

    @pytest.mark.parametrize("table_name", TABLE_NAMES)
    def test_sql_file_has_content(self, table_name):
        sql_path = SQL_FOLDER / f"{table_name}.sql"

        assert sql_path.exists(), f"missing SQL file for {table_name}"
        assert sql_path.read_text().strip(), (
            f"{table_name}.sql is empty -- it would silently create no table"
        )


class TestAnalyticsTables:
    @pytest.mark.parametrize("table_name", TABLE_NAMES)
    def test_table_is_created_with_rows(self, analytics_built, table_name):
        row_count = analytics_built.execute(
            f"SELECT COUNT(*) FROM analytics.{table_name}"
        ).fetchone()[0]

        assert row_count > 0

    @pytest.mark.parametrize("table_name", TABLE_NAMES)
    def test_table_columns_match_its_contract(self, analytics_built, table_name):
        contract = yaml.safe_load(
            (CONTRACTS_FOLDER / f"{table_name}.yml").read_text()
        )
        expected_columns = [column["name"] for column in contract["columns"]]

        described = analytics_built.execute(
            f"DESCRIBE analytics.{table_name}"
        ).fetchall()
        actual_columns = [row[0] for row in described]
        actual_types = {row[0]: row[1] for row in described}

        assert actual_columns == expected_columns, (
            f"{table_name}: table columns {actual_columns} do not match "
            f"contract columns {expected_columns}"
        )

        for column in contract["columns"]:
            actual_type = actual_types[column["name"]]
            assert _duckdb_type_satisfies_contract(actual_type, column["type"]), (
                f"{table_name}.{column['name']}: contract says "
                f"'{column['type']}', table has DuckDB type '{actual_type}'"
            )

    def test_customers_equals_good_plus_bad(self, analytics_built):
        for table_name in ["loan_purpose_summary", "housing_summary", "employment_summary"]:
            mismatched = analytics_built.execute(f"""
                SELECT COUNT(*)
                FROM analytics.{table_name}
                WHERE customers <> good_customers + bad_customers
            """).fetchone()[0]

            assert mismatched == 0, f"{table_name} has inconsistent totals"

    def test_default_rate_is_within_bounds(self, analytics_built):
        for table_name in TABLE_NAMES:
            invalid = analytics_built.execute(f"""
                SELECT COUNT(*)
                FROM analytics.{table_name}
                WHERE default_rate < 0 OR default_rate > 100
            """).fetchone()[0]

            assert invalid == 0, f"{table_name} has an out-of-range default_rate"


class TestAnalyticsValidator:
    """Exercises the real AnalyticsValidator class, redirecting its
    connection to our in-memory test database via monkeypatch (it
    normally opens the real on-disk DuckDB file through get_connection()).
    """

    def test_validate_passes_on_healthy_data(self, analytics_built, monkeypatch):
        monkeypatch.setattr(
            "credit_pipeline.analytics.validator.get_connection",
            lambda: analytics_built,
        )

        AnalyticsValidator().validate()  

    def test_validate_catches_inconsistent_customer_totals(
        self, analytics_built, monkeypatch
    ):
        analytics_built.execute("""
            UPDATE analytics.loan_purpose_summary
            SET customers = customers + 1
        """)

        monkeypatch.setattr(
            "credit_pipeline.analytics.validator.get_connection",
            lambda: analytics_built,
        )

        with pytest.raises(ValueError):
            AnalyticsValidator().validate()

    def test_validate_catches_out_of_range_default_rate(
        self, analytics_built, monkeypatch
    ):
        analytics_built.execute("""
            UPDATE analytics.risk_by_age
            SET default_rate = 150
        """)

        monkeypatch.setattr(
            "credit_pipeline.analytics.validator.get_connection",
            lambda: analytics_built,
        )

        with pytest.raises(ValueError):
            AnalyticsValidator().validate()
