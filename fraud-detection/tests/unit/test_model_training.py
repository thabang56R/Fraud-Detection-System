from pipelines.training_pipeline import run_training_pipeline
from src.common.paths import MODEL_ARTIFACTS_DIR


def test_training_pipeline_saves_artifacts():
    metadata = run_training_pipeline()

    assert "supervised_metadata" in metadata
    assert "anomaly_metadata" in metadata

    assert (MODEL_ARTIFACTS_DIR / "logistic_regression_model.joblib").exists()
    assert (MODEL_ARTIFACTS_DIR / "xgboost_model.joblib").exists()
    assert (MODEL_ARTIFACTS_DIR / "isolation_forest_model.joblib").exists()
    assert (MODEL_ARTIFACTS_DIR / "model_metadata.json").exists()
    assert (MODEL_ARTIFACTS_DIR / "anomaly_metadata.json").exists()