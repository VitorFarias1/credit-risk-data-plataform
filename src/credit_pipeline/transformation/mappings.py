COLUMN_MAPPING = {
    "laufkont": "checking_account_status",
    "laufzeit": "loan_duration_months",
    "moral": "credit_history",
    "verw": "loan_purpose",
    "hoehe": "credit_amount",
    "sparkont": "savings_account",
    "beszeit": "employment_duration",
    "rate": "installment_rate",
    "famges": "personal_status_sex",
    "buerge": "guarantors",
    "wohnzeit": "residence_duration",
    "verm": "property",
    "alter": "age",
    "weitkred": "other_installment_plans",
    "wohn": "housing",
    "bishkred": "existing_credits",
    "beruf": "job",
    "pers": "people_liable",
    "telef": "telephone",
    "gastarb": "foreign_worker",
    "kredit": "credit_risk",
}


CREDIT_RISK_MAPPING = {
    1: "good",
    0: "bad",
}