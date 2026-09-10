# 🛡️ FinShield Fraud Detection Platform

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green?logo=fastapi)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange?logo=scikitlearn)
![XGBoost](https://img.shields.io/badge/XGBoost-Classifier-red)
![MLflow](https://img.shields.io/badge/MLflow-Experiment%20Tracking-blue)
![Pytest](https://img.shields.io/badge/Pytest-Tested-success?logo=pytest)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-black?logo=githubactions)
![Status](https://img.shields.io/badge/Status-Production--Style%20Learning%20Project-purple)

> 🚀 A production-style fraud detection platform for fintech use cases, built with **Python**, **FastAPI**, **machine learning**, **rules engines**, **anomaly detection**, and **MLOps**.

---

## ✨ Vision

FinShield is designed to simulate how **modern fintech fraud detection systems** are built in real-world environments.

Instead of training a single notebook model, this project combines:

- 🧠 **supervised fraud classification** for known fraud patterns
- 🕵️ **anomaly detection** for unknown suspicious behavior
- 📏 **rules-based scoring** for interpretable business logic
- ⚖️ **hybrid scoring** for final risk decisions
- 📡 **FastAPI endpoints** for real-time fraud scoring
- 📊 **monitoring, audit logging, and MLflow tracking** for operational credibility

The goal is to make this repo feel like a **serious portfolio-grade fintech ML system** rather than a simple beginner project.

---

## 🧩 Project Description

Fraud detection in fintech is not solved with one model alone.

Real systems usually combine:

- historical behavior analysis
- merchant and device intelligence
- hand-crafted fraud rules
- probabilistic models
- anomaly scoring
- explainable decisioning
- monitoring and audit trails

FinShield follows that same pattern.

It ingests transaction history, builds fraud features, trains supervised and unsupervised models, evaluates rules, combines all signals into a final score, and exposes the results through a real-time API.

---

## 🎯 What This Project Solves

FinShield helps answer questions like:

- Is this transaction suspicious based on past behavior?
- Does it break known fraud rules?
- Does it look abnormal compared to normal activity?
- Should it be **approved**, **reviewed**, or **blocked**?
- Why did the system make that decision?

---

## 🏗️ Architecture

```text
Raw Transaction Data
        │
        ▼
Data Validation + Cleaning
        │
        ▼
Batch Feature Engineering
        │
        ├── Customer Behavior Features
        ├── Velocity Features
        ├── Merchant Risk Features
        ├── Time Features
        └── Geo / Device Features
        │
        ▼
Training Pipelines
        │
        ├── Logistic Regression Baseline
        ├── XGBoost Supervised Model
        └── Isolation Forest Anomaly Model
        │
        ▼
Saved Model Artifacts
        │
        ▼
Realtime Feature Builder
        │
        ▼
Fraud Intelligence Layers
        │
        ├── Rules Engine
        ├── Supervised Model Inference
        └── Anomaly Detection Inference
        │
        ▼
Hybrid Fraud Scoring Engine
        │
        ▼
Decision Output
        ├── Approve ✅
        ├── Review ⚠️
        └── Block ⛔
        │
        ▼
Operational Layer
        ├── FastAPI Endpoints
        ├── Audit Logs
        ├── Monitoring Reports
        └── MLflow Experiment Tracking
```

## 🧠 Core Fraud Detection Concepts Used

### 📈 1. Feature Engineering
Fraud models are only as good as the features they consume.

This project engineers rich behavioral and contextual features such as:

- ⏰ Transaction time features (hour, weekend, night flags)
- ⚡ Customer transaction velocity (1d, 7d, 30d)
- 💰 Rolling spend behavior
- 📊 Amount deviation from customer history
- 🏪 Merchant historical fraud rate
- 📱 New device indicator
- 🌍 Foreign transaction flag

---

### 📏 2. Rules Engine
Rules provide fast, interpretable fraud logic based on domain knowledge.

Example rules include:

- 💸 High transaction amount
- 📱 New device + large spend
- 🔁 Rapid repeat activity
- 🏪 Merchant fraud hotspot
- 🌍 Foreign high-value transaction

📌 Rules are stored in **YAML configuration** and can be modified without changing code.

---

### 🧠 3. Supervised Learning
The supervised model learns from labeled fraud data and predicts fraud probability.

**Implemented models:**
- Logistic Regression (baseline)
- XGBoost (primary classifier)

---

### 🕵️ 4. Anomaly Detection
The anomaly model detects unusual or unseen patterns without relying on labels.

**Implemented model:**
- Isolation Forest

---

### ⚖️ 5. Hybrid Risk Scoring
The final fraud score combines multiple intelligence layers:

- 📏 Rule-based score
- 🧠 Supervised model probability
- 🕵️ Anomaly score

This reflects how real-world fraud systems blend rules and machine learning.

---

### 📡 6. Real-Time Scoring
Transactions are scored in real time using FastAPI endpoints.

- ⚡ Low-latency inference
- 🔄 On-the-fly feature generation
- 🌐 API-based decisioning

---

### 📊 7. Monitoring and Auditability
The platform includes production-style observability features:

- 📈 MLflow experiment tracking
- 🧾 Prediction audit logs
- 📉 Drift report generation
- 📦 Model metadata storage

---

## 🔥 Key Features

- ✅ Production-style Python project structure  
- ✅ Configurable fraud rules engine (YAML-driven)  
- ✅ Supervised fraud model training (Logistic + XGBoost)  
- ✅ Anomaly detection pipeline (Isolation Forest)  
- ✅ Hybrid risk scoring engine  
- ✅ FastAPI real-time serving layer  
- ✅ Model metadata endpoint  
- ✅ Monitoring and drift reporting  
- ✅ Audit logging for predictions  
- ✅ MLflow experiment tracking  
- ✅ Unit, integration, and API tests  
- ✅ Docker + GitHub Actions CI  

🗂️ Project Structure
```
finshield-fraud-detection-platform/
├── apps/
│   ├── api/
│   │   └── main.py
│   ├── monitoring/
│   │   └── monitor.py
│   └── training/
│       └── train.py
│
├── configs/
│   ├── base.yaml
│   ├── features.yaml
│   ├── model.yaml
│   └── rules.yaml
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── samples/
│
├── docs/
│   ├── api.md
│   ├── architecture.md
│   ├── model-card.md
│   └── runbook.md
│
├── features/
│   ├── batch_features.py
│   └── realtime_features.py
│
├── models/
│   ├── anomaly/
│   ├── supervised/
│   └── artifacts/
│
├── pipelines/
│   ├── data_validation.py
│   ├── training_pipeline.py
│   ├── scoring_pipeline.py
│   └── evaluation_pipeline.py
│
├── src/
│   ├── common/
│   ├── data/
│   ├── models/
│   ├── monitoring/
│   ├── rules/
│   └── scoring/
│
├── tests/
│   ├── api/
│   ├── integration/
│   └── unit/
│
├── logs/
├── reports/
├── mlruns/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md

<<<<<<< HEAD
=======
---
🧪 Fraud Intelligence Layers
🟦 Rules Engine
>>>>>>> 566900bbc01cb6b576161df73e6773a282de7e7e


# 🎯 What This System Does

<<<<<<< HEAD
Given a transaction, FinShield can:
=======
high_amount
foreign_high_amount
rapid_repeat_activity
merchant_fraud_hotspot
new_device_high_amount

---

🟩 Supervised Model
>>>>>>> 566900bbc01cb6b576161df73e6773a282de7e7e

* detect fraud using learned patterns 🧠
* detect suspicious unknown behavior 🕵️
* apply business fraud rules 📏
* combine everything into a **final decision** ⚖️
* explain **why** the decision was made 🔍

---

# 🧪 Live Demo (Add Screenshots Here)

### 🔹 Swagger API

👉 `http://127.0.0.1:8000/docs`

<<<<<<< HEAD
📸 Add screenshot here:
=======
Isolation Forest

🟥 Hybrid Engine
>>>>>>> 566900bbc01cb6b576161df73e6773a282de7e7e

```
/docs/screenshots/swagger-ui.png
```

---

### 🔹 Hybrid Fraud Scoring Example

📥 Input:

```json
{
  "amount": 12000,
  "country": "ZA",
  "device_type": "desktop"
}
```

📤 Output:

```json
{
  "final_score": 84.55,
  "decision": "block",
  "top_reasons": [
    "high_amount",
    "merchant_fraud_hotspot",
    "high_model_probability"
  ]
}
```

---

# 🧠 How It Works (Simple Flow)

```text
Transaction → Features → Rules + ML + Anomaly → Hybrid Score → Decision
```

---

# 🏗️ Architecture (Real Industry Pattern)

```text
Raw Data
   ↓
Feature Engineering
   ↓
├── Rules Engine
├── ML Model (XGBoost)
└── Anomaly Model (Isolation Forest)
   ↓
Hybrid Scoring Engine
   ↓
Decision (Approve / Review / Block)
   ↓
API + Monitoring + Logs
```

---

# 🧠 Core Concepts Demonstrated

## 📈 Feature Engineering

* Behavioral features (spend patterns)
* Velocity features (transaction frequency)
* Risk features (merchant fraud rate)
* Context features (time, geo, device)

---

## 📏 Rules Engine

* YAML-configurable
* Explainable decisions
* Instant fraud detection layer

---

## 🧠 Machine Learning

* Logistic Regression (baseline)
* XGBoost (primary)

---

## 🕵️ Anomaly Detection

* Isolation Forest
* Detects unknown fraud patterns

---

## ⚖️ Hybrid Scoring (REAL SYSTEM DESIGN)

```text
final_score =
0.30 * rules
+ 0.45 * ML probability
+ 0.25 * anomaly score
```

---

## 📡 Real-Time API

* FastAPI-based scoring
* Production-style endpoints

---

## 📊 MLOps & Monitoring

* MLflow experiment tracking
* Audit logs (every prediction tracked)
* Drift reports
* Model metadata endpoints

---

# 🔥 Key Features

* Hybrid fraud detection system
* Explainable decisions
* Real-time scoring API
* ML + anomaly detection
* Monitoring + audit logging
* CI/CD pipeline
* Fully tested system




---

# 🚦 Decision System

| Score  | Decision  |
| ------ | --------- |
| 0–39   | ✅ Approve |
| 40–69  | ⚠️ Review |
| 70–100 | ⛔ Block   |

---

# 🚀 Quick Start (1-Minute Setup)

```bash
pip install -e .[dev]
pytest
python pipelines/training_pipeline.py
python -m uvicorn apps.api.main:app --reload
```

👉 Open:

```
http://127.0.0.1:8000/docs
```

---

# 📊 Outputs

| Type          | Location            |
| ------------- | ------------------- |
| MLflow runs   | `mlruns/`           |
| Audit logs    | `logs/`             |
| Drift reports | `reports/`          |
| Models        | `models/artifacts/` |

---

# 🧪 Testing

```bash
pytest
```

✔ Unit
✔ Integration
✔ API

---

# 🧑‍💻 Skills Demonstrated

This project shows ability in:

* Machine Learning Engineering
* Backend Development (FastAPI)
* Data Engineering (pipelines)
* MLOps (MLflow, monitoring)
* System Design
* Fraud Detection Domain

---

# 🛣️ Next Improvements (Production Path)

* Feature store (Feast)
* SHAP explainability
* Streaming fraud detection (Kafka)
* Dashboard (React)
* Cloud deployment (AWS/GCP)

---

# 👨‍💻 Author

**Thabang Rakeng**

---

# ⭐ Recruiter Note

This project is intentionally built to demonstrate:

✔ real-world ML system thinking
✔ production pipeline design
✔ hybrid decision systems
✔ clean architecture



---

# ⭐ Give It a Star

If this helped or impressed you, ⭐ the repo.














⭐ Final Note

FinShield is built to showcase what a modern fraud detection platform can look like when engineering, ML, and MLOps are combined thoughtfully.

If you found this useful, give the repo a ⭐
