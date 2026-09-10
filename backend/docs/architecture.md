# Architecture

FinShield is a production-style fraud detection platform designed for fintech fraud use cases.

## Section 7 Scope
- ingestion and cleaning
- offline feature engineering
- YAML-driven fraud rules
- supervised fraud model training
- anomaly model training
- hybrid score fusion
- MLflow experiment tracking
- model metadata endpoints
- monitoring report generation
- audit logging

## High-Level Flow

Raw Transactions  
→ Validation  
→ Cleaning  
→ Batch Feature Engineering  
→ Training Dataset  
→ Preprocessing Pipeline  
→ Logistic Regression Baseline  
→ XGBoost Classifier  
→ Isolation Forest  
→ MLflow Tracking  
→ Saved Artifacts  
→ Realtime Feature Builder  
→ Rules Engine + Model Inference + Anomaly Inference  
→ Hybrid Weighted Score  
→ Audit Log  
→ Monitoring Reports  
→ Fraud Scoring API

## Operational Assets
- `models/artifacts/`
- `logs/prediction_audit.jsonl`
- `reports/drift_report.json`
- `mlruns/`