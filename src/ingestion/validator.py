from pathlib import Path

import pandas as pd

class DataValidator:
    def __init__(self, dataframe: pd.DataFrame, source_path: Path):
        self.df = dataframe
        self.source_path = source_path

    def validate(self) -> None:
        self._validate_file_exists()
        self._validate_dataframe_not_empty()
        self._validate_has_columns()

    def _validate_file_exists(self) -> None:
        if not self.source_path.exists():
            raise FileNotFoundError(
                f"Input file not found: {self.source_path}"
            )
        
    def _validate_dataframe_not_empty(self) -> None:
        if self.df.empty:
            raise ValueError("The dataset is empty.")

    def _validate_has_columns(self) -> None:
        if self.df.columns.empty:
            raise ValueError("The dataset has no columns.")