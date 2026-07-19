import pandas as pd

from credit_pipeline.transformation.mappings import COLUMN_MAPPING
from credit_pipeline.transformation.transformer import TrustedLayerTransformer

NUMERIC_COLUMNS = {"age", "credit_amount", "loan_duration_months"}

CATEGORICAL_COLUMNS = {
    "checking_account_status",
    "credit_history",
    "loan_purpose",
    "savings_account",
    "employment_duration",
    "installment_rate",
    "personal_status_sex",
    "guarantors",
    "residence_duration",
    "property",
    "other_installment_plans",
    "housing",
    "existing_credits",
    "job",
    "people_liable",
    "telephone",
    "foreign_worker",
    "credit_risk",
}


class TestTrustedLayerTransformer:
    def test_renames_all_columns(self, raw_df):
        trusted = TrustedLayerTransformer(raw_df).transform()

        expected_names = set(COLUMN_MAPPING.values()) | {"age_group"}
        assert expected_names.issubset(set(trusted.columns))
        
        assert not set(COLUMN_MAPPING.keys()) & set(trusted.columns)

    def test_credit_risk_is_mapped_to_good_bad_labels(self, raw_df):
        trusted = TrustedLayerTransformer(raw_df).transform()

        assert set(trusted["credit_risk"].unique()) <= {"good", "bad"}

    def test_age_group_has_no_nulls_and_expected_labels(self, raw_df):
        trusted = TrustedLayerTransformer(raw_df).transform()

        assert trusted["age_group"].isnull().sum() == 0
        assert set(trusted["age_group"].cat.categories) == {
            "18-25", "26-35", "36-50", "50+",
        }

    def test_continuous_columns_stay_numeric(self, raw_df):
        """Regression test.

        age, credit_amount and loan_duration_months were previously
        cast to `category`, even though they're aggregated with
        AVG/MIN/MAX in the analytics SQL layer.
        """
        trusted = TrustedLayerTransformer(raw_df).transform()

        for column in NUMERIC_COLUMNS:
            assert pd.api.types.is_numeric_dtype(trusted[column]), (
                f"{column} should stay numeric, got {trusted[column].dtype}"
            )

    def test_coded_columns_become_category(self, raw_df):
        trusted = TrustedLayerTransformer(raw_df).transform()

        for column in CATEGORICAL_COLUMNS:
            assert isinstance(trusted[column].dtype, pd.CategoricalDtype), (
                f"{column} should be category, got {trusted[column].dtype}"
            )

    def test_does_not_mutate_the_input_dataframe(self, raw_df):
        """The transformer should work on its own copy, not the caller's
        DataFrame -- otherwise re-running a pipeline stage in the same
        process (e.g. in a notebook or an Airflow task retry) could see
        already-transformed data on the second pass."""
        original_columns = list(raw_df.columns)

        TrustedLayerTransformer(raw_df).transform()

        assert list(raw_df.columns) == original_columns
