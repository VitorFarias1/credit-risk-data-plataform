import pandas as pd

from credit_pipeline.transformation.mappings import CREDIT_RISK_MAPPING
from credit_pipeline.transformation.mappings import COLUMN_MAPPING

class TrustedLayerTransformer:
    def __init__(self, dataFrame: pd.DataFrame):
        self.df = dataFrame.copy()

    def transform(self) -> pd.DataFrame:
        self._rename_columns()
        self._transform_credit_risk()
        self._convert_data_types()
        self._create_age_group()

    def _rename_columns(self):
        self.df.rename(
            columns=COLUMN_MAPPING,
            inplace=True
        )
    
    def _transform_credit_risk(self):
        self.df["credit_risk"] = (
            self.df["credit_risk"]
            .map(CREDIT_RISK_MAPPING)
        )

    def _convert_data_types(self):
        categorical_columns = [
            "checking_account_status",
            "loan_duration_months",
            "credit_history",
            "loan_purpose",
            "credit_amount",
            "savings_account",
            "employment_duration",
            "installment_rate",
            "personal_status_sex",
            "guarantors",
            "residence_duration",
            "property",
            "age",
            "other_installment_plans",
            "housing",
            "existing_credits",
            "job",
            "people_liable",
            "telephone",
            "foreign_worker",
            "credit_risk",
        ]

        for column in categorical_columns:
            self.df[column] = (
                self.df[column]
                .astype("category")
            )

    def _create_age_group(self):
        self.df["age_group"] = pd.cut(
            self.df["age"],
            bins=[18,25,35,50,100],
    labels=["18-25", "26-35", "36-50", "50+",],
        )