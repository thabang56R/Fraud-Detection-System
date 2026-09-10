from apps.monitoring.monitor import run_monitoring


def test_run_monitoring_returns_report():
    result = run_monitoring()

    assert "report" in result
    assert "report_path" in result
    assert "numeric_feature_drift" in result["report"]