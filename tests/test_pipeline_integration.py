"""End-to-end test: runs ingestion -> transformation -> warehouse ->
analytics -> validation in sequence, exactly like a real run, but
against a temp directory instead of the real data/ folder.

Every path constant (RAW_DATA_PATH, TRUSTED_DATA_PATH, etc.) is
computed once in config/paths.py from PROJECT_ROOT and imported by
value (`from credit_pipeline.config import X`) into each module that
uses it. That means each module holds its own bound copy of the
constant, so redirecting the pipeline to a temp directory means
patching each module's copy individually ("patch where it's used, not
where it's defined"). This is exactly the kind of friction the roadmap
flags for a future phase (env-var-driven config instead of a path
hardcoded from __file__).
"""

import credit_pipeline.analytics.load_analytics as load_analytics_module
import credit_pipeline.ingestion.load_raw as load_raw_module
import credit_pipeline.transformation.load_trusted as load_trusted_module
import credit_pipeline.warehouse.database as database_module
import credit_pipeline.warehouse.load_warehouse as load_warehouse_module
import credit_pipeline.warehouse.loader as loader_module
import pytest
from credit_pipeline.analytics.validator import AnalyticsValidator


@pytest.fixture
def isolated_pipeline_paths(tmp_path, monkeypatch, raw_df):
    raw_dir = tmp_path / "raw"
    trusted_dir = tmp_path / "trusted"
    warehouse_dir = tmp_path / "warehouse"
    raw_dir.mkdir()
    trusted_dir.mkdir()
    warehouse_dir.mkdir()

    raw_csv_path = raw_dir / "german_credit_data.csv"
    raw_parquet_path = trusted_dir / "german_credit.parquet"
    trusted_parquet_path = trusted_dir / "german_credit_trusted.parquet"
    warehouse_db_path = warehouse_dir / "credit.duckdb"

    raw_df.to_csv(raw_csv_path, index=False)

    monkeypatch.setattr(load_raw_module, "RAW_DATA_PATH", raw_csv_path)
    monkeypatch.setattr(load_raw_module, "RAW_PARQUET_PATH", raw_parquet_path)

    monkeypatch.setattr(load_trusted_module, "RAW_PARQUET_PATH", raw_parquet_path)
    monkeypatch.setattr(load_trusted_module, "TRUSTED_DATA_PATH", trusted_parquet_path)

    monkeypatch.setattr(loader_module, "TRUSTED_DATA_PATH", trusted_parquet_path)

    monkeypatch.setattr(database_module, "WAREHOUSE_DB_PATH", warehouse_db_path)

    return {
        "raw_csv_path": raw_csv_path,
        "raw_parquet_path": raw_parquet_path,
        "trusted_parquet_path": trusted_parquet_path,
        "warehouse_db_path": warehouse_db_path,
    }


def test_full_pipeline_runs_end_to_end(isolated_pipeline_paths):
    paths = isolated_pipeline_paths

    load_raw_module.main()
    assert paths["raw_parquet_path"].exists(), (
        "ingestion should write the raw parquet that the transformation "
        "stage reads next"
    )

    load_trusted_module.main()
    assert paths["trusted_parquet_path"].exists()

    load_warehouse_module.main()
    assert paths["warehouse_db_path"].exists()

    load_analytics_module.main()

    AnalyticsValidator().validate()
