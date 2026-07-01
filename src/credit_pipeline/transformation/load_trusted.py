import pandas as pd

from credit_pipeline.config import (RAW_PARQUET_PATH, TRUSTED_DATA_PATH,)
from credit_pipeline.transformation.transformer import TrustedLayerTransformer

def load_dataset():
    return pd.read_parquet(
        RAW_PARQUET_PATH
    )

def save_dataset(df):
    df.to_parquet(
        TRUSTED_DATA_PATH,
        index=False,
    )

def main():
    print("Loading Trusted Layer...")

    df = load_dataset()
    transformer = TrustedLayerTransformer(df)
    trusted_df = transformer.transform()
    save_dataset(trusted_df)

    print("Trusted Layer Completed")

if __name__ == "__main__":
    main()