install:
	pip install -e .[dev]

run-api:
	python -m uvicorn apps.api.main:app --reload

test:
	pytest

validate-data:
	python pipelines/data_validation.py

train:
	python pipelines/training_pipeline.py

evaluate:
	python pipelines/evaluation_pipeline.py

score:
	python pipelines/scoring_pipeline.py

monitor:
	python apps/monitoring/monitor.py

format:
	black .
	isort .

lint:
	ruff check .