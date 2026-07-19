"""Shared pytest fixtures for the credit_pipeline test suite.

The real german_credit_data.csv is intentionally not committed to the
repository (see README), so every test builds its own small synthetic
dataset with the same raw (German) column names and value ranges
instead of depending on a file that may not exist locally or in CI.
"""

import duckdb
import numpy as np
import pandas as pd
import pytest

from credit_pipeline.transformation.transformer import TrustedLayerTransformer
from credit_pipeline.warehouse.loader import WarehouseLoader

RANDOM_SEED = 42
N_ROWS = 200


def _make_raw_german_credit_df(n: int = N_ROWS) -> pd.DataFrame:
    """Builds a synthetic DataFrame shaped like the raw German Credit
    dataset: same (German) column names, same value ranges/codes.
    """
    rng = np.random.default_rng(RANDOM_SEED)

    return pd.DataFrame(
        {
            "laufkont": rng.integers(1, 5, n),
            "laufzeit": rng.integers(4, 72, n),
            "moral": rng.integers(0, 5, n),
            "verw": rng.integers(0, 11, n),
            "hoehe": rng.integers(250, 20000, n),
            "sparkont": rng.integers(1, 6, n),
            "beszeit": rng.integers(1, 6, n),
            "rate": rng.integers(1, 5, n),
            "famges": rng.integers(1, 5, n),
            "buerge": rng.integers(1, 4, n),
            "wohnzeit": rng.integers(1, 5, n),
            "verm": rng.integers(1, 5, n),
            "alter": rng.integers(19, 75, n),
            "weitkred": rng.integers(1, 4, n),
            "wohn": rng.integers(1, 4, n),
            "bishkred": rng.integers(1, 5, n),
            "beruf": rng.integers(1, 5, n),
            "pers": rng.integers(1, 3, n),
            "telef": rng.integers(1, 3, n),
            "gastarb": rng.integers(1, 3, n),
            "kredit": rng.integers(0, 2, n),
        }
    )


@pytest.fixture
def raw_df() -> pd.DataFrame:
    """A synthetic raw DataFrame, same shape as the real CSV once loaded."""
    return _make_raw_german_credit_df()


@pytest.fixture
def raw_csv_file(tmp_path, raw_df):
    """Writes `raw_df` to a temp CSV and returns its path."""
    csv_path = tmp_path / "german_credit_data.csv"
    raw_df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def trusted_df(raw_df) -> pd.DataFrame:
    """A trusted-layer DataFrame produced by the real transformer.

    Other layers (warehouse, analytics) are built on top of this, so
    their tests exercise the actual transformation logic instead of a
    hand-rolled approximation of it.
    """
    transformer = TrustedLayerTransformer(raw_df.copy())
    return transformer.transform()


@pytest.fixture
def duckdb_with_trusted_data(trusted_df):
    """An in-memory DuckDB connection with trusted.credit populated from
    synthetic data -- built the same way load_warehouse.py builds the
    real one, minus reading trusted parquet from disk.
    """
    connection = duckdb.connect(":memory:")

    loader = WarehouseLoader(connection)
    loader.create_schemas()

    connection.register("trusted_df_view", trusted_df)
    connection.execute(
        "CREATE TABLE trusted.credit AS SELECT * FROM trusted_df_view"
    )

    yield connection

    connection.close()
