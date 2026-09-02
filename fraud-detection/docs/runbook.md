# Runbook

## Local setup
1. Install dependencies
2. Run tests
3. Train models
4. Run scoring pipeline
5. Start API
6. Generate monitoring report

## Commands

### Install
`pip install -e .[dev]`

### Tests
`pytest`

### Train models
`python pipelines/training_pipeline.py`

### Evaluate metadata
`python pipelines/evaluation_pipeline.py`

### Score sample payload
`python pipelines/scoring_pipeline.py`

### Start API
`python -m uvicorn apps.api.main:app --reload`

### Generate monitoring report
`python apps/monitoring/monitor.py`

## Operational endpoints

### Health
`GET /health`

### Model metadata
`GET /model/info`

### Monitoring report
`GET /monitoring/report`

### Hybrid scoring
`POST /score/hybrid`

## Artifacts
- `models/artifacts/`
- `logs/`
- `reports/`
- `mlruns/`
