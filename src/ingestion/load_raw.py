import pandas as pd

from config import RAW_DATA_PATH, TRUSTED_DATA_PATH
from quality import DataQualityReporter
from validator import DataValidator


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_PATH)


def save_as_parquet(df: pd.DataFrame) -> None:
    df.to_parquet(
        TRUSTED_DATA_PATH,
        index=False,
    )


def main() -> None:
    print("Starting ingestion pipeline...")

    df = load_dataset()

    validator = DataValidator(df, RAW_DATA_PATH)
    validator.validate()

    quality = DataQualityReporter(df)
    report = quality.generate_report()
    quality.print_report(report)

    save_as_parquet(df)

    print("Pipeline finished successfully.")


if __name__ == "__main__":
    main()