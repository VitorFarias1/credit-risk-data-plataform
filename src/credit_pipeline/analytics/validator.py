from credit_pipeline.warehouse.database import get_connection


class AnalyticsValidator:

    def __init__(self):
        self.connection = get_connection()

    def validate(self):

        print("Running Analytics Validation...")

        try:

            self.validate_tables()

            self.validate_customer_totals()

            self.validate_default_rates()

            self.validate_average_age()

            self.validate_nulls()

            print("Analytics validation completed.")

        finally:

            self.connection.close()

    def validate_tables(self):

        tables = [

            "loan_purpose_summary",

            "risk_by_age",

            "housing_summary",

            "employment_summary"

        ]

        for table in tables:

            result = self.connection.execute(f"""

                SELECT COUNT(*)

                FROM analytics.{table}

            """).fetchone()

            print(f"{table}: OK ({result[0]} rows)")

    def validate_customer_totals(self):

        tables = [

            "loan_purpose_summary",

            "housing_summary",

            "employment_summary"

        ]

        for table in tables:

            invalid = self.connection.execute(f"""

                SELECT COUNT(*)

                FROM analytics.{table}

                WHERE customers <> good_customers + bad_customers

            """).fetchone()[0]

            if invalid:

                raise ValueError(

                    f"{table} contains inconsistent totals."

                )

            print(f"{table}: customer totals OK")

    def validate_default_rates(self):

        tables = [

            "loan_purpose_summary",

            "housing_summary",

            "employment_summary",

            "risk_by_age"

        ]

        for table in tables:

            invalid = self.connection.execute(f"""

                SELECT COUNT(*)

                FROM analytics.{table}

                WHERE default_rate < 0
                OR default_rate > 100

            """).fetchone()[0]

            if invalid:

                raise ValueError(

                    f"{table} has invalid default_rate."

                )

            print(f"{table}: default_rate OK")

    def validate_average_age(self):

        invalid = self.connection.execute("""

            SELECT COUNT(*)

            FROM analytics.housing_summary

            WHERE average_age < 18

            OR average_age > 100

        """).fetchone()[0]

        if invalid:

            raise ValueError(
                "housing_summary has invalid average_age."
            )

        print("housing_summary: average_age OK")

    def validate_nulls(self):

        invalid = self.connection.execute("""

            SELECT COUNT(*)

            FROM analytics.loan_purpose_summary

            WHERE loan_purpose IS NULL

        """).fetchone()[0]

        if invalid:

            raise ValueError(
                "loan_purpose_summary contains null loan_purpose values."
            )

        print("loan_purpose_summary: nulls OK")


def main():
    AnalyticsValidator().validate()


if __name__ == "__main__":
    main()