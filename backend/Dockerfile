FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY apps ./apps
COPY src ./src
COPY pipelines ./pipelines
COPY features ./features
COPY configs ./configs
COPY data ./data

RUN pip install --upgrade pip && pip install .

EXPOSE 8000

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]