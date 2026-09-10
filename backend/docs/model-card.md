# Model Card

## Model Purpose
FinShield uses three fraud intelligence layers:
- rules engine
- supervised fraud classifier
- anomaly detector

## Models Implemented
- Logistic Regression baseline
- XGBoost primary classifier
- Isolation Forest anomaly detector
- Hybrid weighted scoring engine

## Input Features
- transaction amount
- time features
- customer velocity features
- customer behavior features
- merchant risk features
- geo/device features

## Outputs

### Supervised model
- fraud probability
- binary fraud prediction

### Anomaly model
- raw anomaly score
- normalized anomaly score
- anomaly review recommendation

### Hybrid engine
- rule score
- fraud probability
- anomaly score
- final weighted score
- final decision
- top reasons

## Limitations
- trained on a very small demo dataset
- hybrid weights are manually configured
- thresholds are not yet cost-optimized
- no drift monitoring yet

## Next Improvements
- cost-based threshold tuning
- calibration
- MLflow tracking
- feature drift monitoring
- production audit logging