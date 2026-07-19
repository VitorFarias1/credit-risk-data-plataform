import credit_pipeline.cli.inspect as inspect_module


def test_main_runs_without_error(duckdb_with_trusted_data, monkeypatch, capsys):
    """Regression test: inspect.py used to query a table named
    `trusted_credit`, which never existed (the real table is
    `trusted.credit`, schema `trusted` + table `credit`). This runs the
    CLI's real main() end-to-end against an in-memory database and
    checks it completes and prints the expected sections.
    """
    monkeypatch.setattr(
        "credit_pipeline.cli.inspect.get_connection",
        lambda: duckdb_with_trusted_data,
    )

    inspect_module.main()

    output = capsys.readouterr().out
    assert "TABLES" in output
    assert "SAMPLE" in output
    assert "ROW COUNT" in output
