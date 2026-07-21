import pandas as pd
import pytest

from credit_pipeline.ingestion.quality import DataQualityReporter
from credit_pipeline.ingestion.validator import DataValidator


class TestDataValidator:
    def test_raises_if_file_does_not_exist(self, tmp_path, raw_df):
        missing_path = tmp_path / "does_not_exist.csv"
        validator = DataValidator(raw_df, missing_path)

        with pytest.raises(FileNotFoundError):
            validator.validate()

    def test_raises_if_dataframe_is_empty(self, raw_csv_file):
        empty_df = pd.DataFrame()
        validator = DataValidator(empty_df, raw_csv_file)

        with pytest.raises(ValueError):
            validator.validate()

    def test_raises_if_dataframe_has_no_columns(self, raw_csv_file):
        no_columns_df = pd.DataFrame(index=[0, 1, 2])
        validator = DataValidator(no_columns_df, raw_csv_file)

        with pytest.raises(ValueError):
            validator.validate()

    def test_passes_for_a_valid_dataframe(self, raw_csv_file, raw_df):
        validator = DataValidator(raw_df, raw_csv_file)

        validator.validate() 

class TestDataQualityReporter:
    def test_report_counts_match_the_dataframe(self, raw_df):
        report = DataQualityReporter(raw_df).generate_report()

        assert report["rows"] == len(raw_df)
        assert report["columns"] == len(raw_df.columns)
        assert report["missing_values"] == int(raw_df.isnull().sum().sum())
        assert report["duplicated_rows"] == int(raw_df.duplicated().sum())

    def test_detects_missing_values(self, raw_df):
        df_with_na = raw_df.copy()
        df_with_na.loc[0, "alter"] = None

        report = DataQualityReporter(df_with_na).generate_report()

        assert report["missing_values"] == 1

    def test_detects_duplicated_rows(self, raw_df):
        df_with_duplicate = pd.concat(
            [raw_df, raw_df.iloc[[0]]], ignore_index=True
        )

        report = DataQualityReporter(df_with_duplicate).generate_report()

        assert report["duplicated_rows"] == 1

    def test_memory_usage_mb_is_plausible(self, raw_df):
        """Regression test.

        memory_usage_mb used to be computed as
        `bytes / 1024 * 2` instead of `bytes / 1024 ** 2`, which
        overstated memory usage by roughly three orders of magnitude
        (a ~100KB synthetic dataset was reported as ~60MB).
        """
        report = DataQualityReporter(raw_df).generate_report()

        expected_mb = raw_df.memory_usage(deep=True).sum() / (1024 ** 2)

        assert report["memory_usage_mb"] == pytest.approx(expected_mb, abs=0.01)
    
        assert report["memory_usage_mb"] < 1
