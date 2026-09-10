from __future__ import annotations

import json

import joblib
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split

from features.batch_features import build_batch_features
from src.common.config import get_base_config, load_yaml_config
from src.common.logger import logger
from src.common.paths import MODEL_ARTIFACTS_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR
from src.data.ingestion import basic_cleaning, read_csv_data, validate_required_columns
from src.models.anomaly import train_anomaly_model
from src.models.evaluate import evaluate_classifier
from src.models.preprocessing import get_feature_columns
from src.models.train import train_models


def run_training_pipeline() -> dict:
    logger.info("Training pipeline started")

    base_config = get_base_config()
    config = load_yaml_config("model.yaml")

    target_col = config["model"]["target"]
    random_state = int(config["model"]["random_state"])
    test_size = float(config["model"]["test_size"])
    threshold = float(config["training"]["probability_threshold"])
    anomaly_review_threshold = float(config["anomaly"]["review_threshold"])

    mlflow_tracking_uri = base_config["experiment"]["mlflow_tracking_uri"]
    mlflow_experiment_name = base_config["experiment"]["mlflow_experiment_name"]

    mlflow.set_tracking_uri(mlflow_tracking_uri)
    mlflow.set_experiment(mlflow_experiment_name)

    raw_file_path = RAW_DATA_DIR / "transactions_sample.csv"
    processed_file_path = PROCESSED_DATA_DIR / "transactions_features.csv"

    df = read_csv_data(str(raw_file_path))
    validate_required_columns(df)
    df = basic_cleaning(df)

    features_df = build_batch_features(df)
    features_df.to_csv(processed_file_path, index=False)

    feature_config = get_feature_columns()
    selected_features = feature_config["numeric"] + feature_config["categorical"]

    X = features_df[selected_features].copy()
    y = features_df[target_col].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        shuffle=False,
        random_state=random_state,
    )

    with mlflow.start_run(run_name="finshield_training_run"):
        mlflow.log_param("target_column", target_col)
        mlflow.log_param("test_size", test_size)
        mlflow.log_param("random_state", random_state)
        mlflow.log_param("threshold", threshold)
        mlflow.log_param("anomaly_review_threshold", anomaly_review_threshold)
        mlflow.log_param("baseline_model", config["training"]["baseline_model"])
        mlflow.log_param("primary_model", config["training"]["primary_model"])
        mlflow.log_param("anomaly_model", config["training"]["anomaly_model"])

        trained = train_models(X_train=X_train, y_train=y_train, random_state=random_state)

        baseline_metrics = evaluate_classifier(trained.baseline_pipeline, X_test, y_test, threshold=threshold)
        primary_metrics = evaluate_classifier(trained.primary_pipeline, X_test, y_test, threshold=threshold)

        for metric_name, metric_value in baseline_metrics.items():
            if isinstance(metric_value, (int, float)):
                mlflow.log_metric(f"baseline_{metric_name}", metric_value)

        for metric_name, metric_value in primary_metrics.items():
            if isinstance(metric_value, (int, float)):
                mlflow.log_metric(f"primary_{metric_name}", metric_value)

        joblib.dump(trained.baseline_pipeline, MODEL_ARTIFACTS_DIR / "logistic_regression_model.joblib")
        joblib.dump(trained.primary_pipeline, MODEL_ARTIFACTS_DIR / "xgboost_model.joblib")

        anomaly_trained = train_anomaly_model(X_train=X_train, random_state=random_state)
        joblib.dump(anomaly_trained.pipeline, MODEL_ARTIFACTS_DIR / "isolation_forest_model.joblib")

        raw_train_scores = anomaly_trained.pipeline.named_steps["model"].score_samples(
            anomaly_trained.pipeline.named_steps["preprocessor"].transform(X_train)
        )

        anomaly_metadata = {
            "model_name": config["training"]["anomaly_model"],
            "review_threshold": anomaly_review_threshold,
            "raw_score_min": float(raw_train_scores.min()),
            "raw_score_max": float(raw_train_scores.max()),
            "feature_columns": selected_features,
        }

        with open(MODEL_ARTIFACTS_DIR / "anomaly_metadata.json", "w", encoding="utf-8") as f:
            json.dump(anomaly_metadata, f, indent=2)

        metadata = {
            "baseline_model": config["training"]["baseline_model"],
            "primary_model": config["training"]["primary_model"],
            "anomaly_model": config["training"]["anomaly_model"],
            "target": target_col,
            "threshold": threshold,
            "feature_columns": selected_features,
            "baseline_metrics": baseline_metrics,
            "primary_metrics": primary_metrics,
        }

        with open(MODEL_ARTIFACTS_DIR / "model_metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        mlflow.log_artifact(str(MODEL_ARTIFACTS_DIR / "model_metadata.json"))
        mlflow.log_artifact(str(MODEL_ARTIFACTS_DIR / "anomaly_metadata.json"))
        mlflow.log_artifact(str(processed_file_path))

    logger.info(f"Saved processed training features to: {processed_file_path}")
    logger.info(f"Saved model artifacts to: {MODEL_ARTIFACTS_DIR}")
    logger.info("Training pipeline completed")

    return {
        "supervised_metadata": metadata,
        "anomaly_metadata": anomaly_metadata,
    }


if __name__ == "__main__":
    result = run_training_pipeline()
    print(json.dumps(result, indent=2))