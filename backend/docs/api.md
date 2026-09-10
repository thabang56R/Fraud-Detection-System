# API

## Endpoints

### GET /
Returns basic service metadata.

### GET /health
Returns health status for the API.

### GET /model/info
Returns supervised and anomaly model metadata.

### GET /monitoring/report
Generates and returns a simple monitoring/drift report.

### POST /features/realtime
Generates realtime fraud features from a live transaction payload using historical transaction data.

### POST /rules/evaluate
Evaluates configured fraud rules against the engineered transaction features.

### POST /score/rules
Runs the rule-based fraud scoring engine and returns:
- rule score
- triggered rules
- decision
- top reasons

### POST /score/model
Runs the supervised fraud model and returns:
- fraud probability
- predicted label
- model threshold

### POST /score/anomaly
Runs the anomaly detection model and returns:
- raw anomaly score
- normalized anomaly score
- anomaly label
- review recommendation

### POST /score/hybrid
Runs the hybrid fraud engine and returns:
- rule score
- fraud probability
- anomaly score
- final weighted score
- final decision
- reasons