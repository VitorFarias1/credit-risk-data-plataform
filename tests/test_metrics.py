import pandas as pd

from credit_pipeline.analytics.metrics import AnalyticsMetrics


class TestAnalyticsMetrics:
    """AnalyticsMetrics isn't called anywhere in the current pipeline --
    the analytics layer is built with SQL instead (see analytics/sql/).
    It looks like an earlier, pandas-only approach that was superseded.
    Tested here for correctness in case it gets wired in later; worth
    deciding whether to keep it, wire it in, or remove it as dead code.
    """

    def test_metrics_on_trusted_data(self, trusted_df):
        metrics = AnalyticsMetrics(trusted_df)

        assert metrics.total_customers() == len(trusted_df)
        assert (
            metrics.good_customers() + metrics.bad_customers()
            == len(trusted_df)
        )
        assert 0 <= metrics.default_rate() <= 100
        assert metrics.average_credit_amount() > 0
        assert 18 <= metrics.average_age() <= 100

    def test_default_rate_is_zero_for_empty_dataframe(self):
        empty_df = pd.DataFrame({"credit_risk": pd.Series(dtype="object")})
        metrics = AnalyticsMetrics(empty_df)

        assert metrics.default_rate() == 0
