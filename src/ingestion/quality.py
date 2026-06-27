import pandas as pd

class DataQualityReporter:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def generate_report(self) -> dict:
        return {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "missing_values": int(self.df.isnull().sum().sum()),
            "duplicated_rows": int(self.df.duplicated().sum()),
            "memory_usage_mb": round(
                self.df.memory_usage(deep=True).sum() / 1024 * 2, 2
            ),
        }

    @staticmethod
    def print_report(report: dict) -> None:
        print("\n========== DATA QUALITY REPORT ==========")

        for key, value in report.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

        print("=========================================\n")