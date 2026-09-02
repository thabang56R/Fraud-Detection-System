from fastapi import FastAPI
from pydantic import BaseModel

from apps.monitoring.monitor import run_monitoring
from features.realtime_features import build_realtime_features
from src.common.config import settings
from src.common.paths import RAW_DATA_DIR
from src.data.ingestion import basic_cleaning, read_csv_data
from src.models.anomaly_inference import FraudAnomalyService
from src.models.inference import FraudModelService
from src.monitoring.model_registry import load_anomaly_metadata, load_model_metadata
from src.scoring.hybrid_engine import HybridFraudScoringEngine
from src.scoring.risk_engine import FraudRiskEngine

app = FastAPI(
    title="FinShield Fraud Detection API",
    version="0.7.0",
    description="Production-style fraud detection platform for fintech",
)


def get_risk_engine() -> FraudRiskEngine:
    return FraudRiskEngine()


def get_model_service() -> FraudModelService:
    return FraudModelService()


def get_anomaly_service() -> FraudAnomalyService:
    return FraudAnomalyService()


def get_hybrid_engine() -> HybridFraudScoringEngine:
    return HybridFraudScoringEngine()


class TransactionPayload(BaseModel):
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: float
    currency: str
    country: str
    device_type: str
    ip_address: str
    timestamp: str


@app.get("/")
def root():
    return {
        "message": "FinShield Fraud Detection API is running",
        "environment": settings.app_env,
        "version": "0.7.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "finshield-api",
        "environment": settings.app_env,
    }


@app.get("/model/info")
def get_model_info():
    return {
        "supervised_model_metadata": load_model_metadata(),
        "anomaly_model_metadata": load_anomaly_metadata(),
    }


@app.get("/monitoring/report")
def get_monitoring_report():
    return run_monitoring()


@app.post("/features/realtime")
def preview_realtime_features(payload: TransactionPayload):
    history_df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    history_df = basic_cleaning(history_df)

    features = build_realtime_features(
        payload=payload.model_dump(),
        customer_history=history_df,
        merchant_history=history_df,
    )

    return {
        "message": "Realtime features generated successfully",
        "features": features,
    }


@app.post("/rules/evaluate")
def evaluate_rules(payload: TransactionPayload):
    history_df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    history_df = basic_cleaning(history_df)

    features = build_realtime_features(
        payload=payload.model_dump(),
        customer_history=history_df,
        merchant_history=history_df,
    )

    rules_result = get_risk_engine().rules_engine.evaluate(features)

    return {
        "message": "Rules evaluated successfully",
        "features": features,
        "rules_result": rules_result,
    }


@app.post("/score/rules")
def score_with_rules(payload: TransactionPayload):
    history_df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    history_df = basic_cleaning(history_df)

    features = build_realtime_features(
        payload=payload.model_dump(),
        customer_history=history_df,
        merchant_history=history_df,
    )

    result = get_risk_engine().score(features)

    return {
        "message": "Rule-based fraud score generated successfully",
        "result": result,
    }


@app.post("/score/model")
def score_with_model(payload: TransactionPayload):
    history_df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    history_df = basic_cleaning(history_df)

    features = build_realtime_features(
        payload=payload.model_dump(),
        customer_history=history_df,
        merchant_history=history_df,
    )

    result = get_model_service().predict(features)

    return {
        "message": "Supervised model fraud score generated successfully",
        "features": features,
        "result": result,
    }


@app.post("/score/anomaly")
def score_with_anomaly(payload: TransactionPayload):
    history_df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    history_df = basic_cleaning(history_df)

    features = build_realtime_features(
        payload=payload.model_dump(),
        customer_history=history_df,
        merchant_history=history_df,
    )

    result = get_anomaly_service().predict(features)

    return {
        "message": "Anomaly score generated successfully",
        "features": features,
        "result": result,
    }


@app.post("/score/hybrid")
def score_with_hybrid(payload: TransactionPayload):
    history_df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    history_df = basic_cleaning(history_df)

    features = build_realtime_features(
        payload=payload.model_dump(),
        customer_history=history_df,
        merchant_history=history_df,
    )

    result = get_hybrid_engine().score(features)

    return {
        "message": "Hybrid fraud score generated successfully",
        "features": features,
        "result": result,
    }