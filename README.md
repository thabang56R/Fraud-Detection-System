# 🛡️ FinShield Fraud Detection Platform  

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Python](https://img.shields.io/badge/typescript-frontend-maroon?logo=typescript)
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

## 🌐 OVERVIEW  

FinShield demonstrates how modern fintech fraud detection systems combine multiple intelligence layers instead of relying on a single model.  

The platform includes:  
- 🧠 Supervised fraud classification for known fraud patterns  
- 🕵️ Anomaly detection for unusual or unseen behavior  
- 📏 Rules‑based scoring for transparent business logic  
- ⚖️ Hybrid scoring for final risk decisions  
- 📡 FastAPI endpoints for real‑time fraud scoring  
- 📊 Monitoring, audit logging, and MLflow experiment tracking  
- 🎨 Responsive React + Bootstrap frontend  

💎 Designed as a **portfolio‑grade fintech ML system** with a practical UI for scoring transactions and reviewing model output.  

---

## 🎯 WHAT THE SYSTEM DOES  

Given a transaction, FinShield can:  
- 🧠 Detect fraud using learned patterns  
- 🕵️ Identify suspicious unknown behavior  
- 📏 Apply configurable fraud rules  
- ⚖️ Combine rules, model probability, and anomaly scores  
- ✅ Approve, ⚠️ Review, or ⛔ Block a transaction  
- 🔍 Explain why a decision was made  
- 📑 Display model metadata and monitoring reports  

---

## 🏗️ ARCHITECTURE  

Raw Transaction Data  
        │  
        ▼  
Data Validation + Cleaning  
        │  
        ▼  
Batch Feature Engineering  
        │  
        ├── 👤 Customer Behavior Features  
        ├── ⚡ Velocity Features  
        ├── 🏪 Merchant Risk Features  
        ├── ⏰ Time Features  
        └── 🌍 Geo / Device Features  
        │  
        ▼  
Training Pipelines  
        │  
        ├── 📉 Logistic Regression Baseline  
        ├── 🚀 XGBoost Supervised Model  
        └── 🕵️ Isolation Forest Anomaly Model  
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
        ├── 📏 Rules Engine  
        ├── 🧠 Supervised Model Inference  
        └── 🕵️ Anomaly Detection Inference  
        │  
        ▼  
⚖️ Hybrid Fraud Scoring Engine  
        │  
        ▼  
Decision Output → ✅ Approve | ⚠️ Review | ⛔ Block  
        │  
        ▼  
Operational Layer → 📡 FastAPI | 🧾 Audit Logs | 📊 Monitoring | 📈 MLflow  
        │  
        ▼  
🎨 React Frontend  

---

## 🎨 FRONTEND  

Built with:  
- ⚛️ React  
- ⚡ Vite  
- 📜 JavaScript + JSX  
- 🎨 Bootstrap CSS  

Screens:  
1. 🖥️ **Overview** → Platform status, model info, quick links  
2. 🎛️ **Scoring Console** → Enter transaction, choose engine, review score + reasons  
3. 📊 **Monitoring** → Drift signals + backend monitoring output  
4. 📑 **Model Registry** → Metadata for supervised + anomaly models  

---

## 🧪 FRAUD INTELLIGENCE LAYERS  

1. 📈 **Feature Engineering**  
   - ⏰ Transaction hour, weekend, night flags  
   - ⚡ Customer velocity  
   - 💰 Rolling spend behavior  
   - 📊 Amount deviation  
   - 🏪 Merchant fraud rate  
   - 📱 New device indicator  
   - 🌍 Foreign transaction flag  

2. 📏 **Rules Engine**  
   - 💸 High transaction amount  
   - 📱 New device + large spend  
   - 🔁 Rapid repeat activity  
   - 🏪 Merchant fraud hotspot  
   - 🌍 Foreign high‑value transaction  

3. 🧠 **Supervised Learning**  
   - 📉 Logistic Regression baseline  
   - 🚀 XGBoost classifier  

4. 🕵️ **Anomaly Detection**  
   - 🌐 Isolation Forest  

5. ⚖️ **Hybrid Risk Scoring**
    
final_score =
0.30 * rules_score
+ 0.45 * model_probability
+ 0.25 * anomaly_score

  
---

## 🚦 DECISION SYSTEM  

| 📊 Score Range | 🛡️ Decision |
|----------------|-------------|
| 0–39           | ✅ Approve |
| 40–69          | ⚠️ Review |
| 70–100         | ⛔ Block |

---

## 📡 API ENDPOINTS  

- 🔹 GET `/`  
- 🔹 GET `/health`  
- 🔹 GET `/model/info`  
- 🔹 GET `/monitoring/report`  
- 🔹 POST `/score/hybrid`  
- 🔹 POST `/score/rules`  
- 🔹 POST `/score/model`  
- 🔹 POST `/score/anomaly`  
- 🔹 POST `/rules/evaluate`  
- 🔹 POST `/features/realtime`  

---

## ⚙️ BACKEND SETUP  

```bash
pip install -e .[dev]
pytest
python pipelines/training_pipeline.py
python -m uvicorn apps.api.main:app --reload

👉 Open: http://127.0.0.1:8000/doc

---

🎨 FRONTEND SETUP

npm install
npm run dev

👉 Default API: http://127.0.0.1:8000
---

📦 PROJECT OUTPUTS
📈 MLflow runs → mlruns/

🧾 Audit logs → logs/

📉 Drift reports → reports/

📂 Model files → models/artifacts

---

🧪 TESTING
✔ Unit tests
✔ Integration tests
✔ API tests

Run all

pytest

---

🔑 KEY FEATURES
🛡️ Hybrid fraud detection

🔍 Explainable decisions

⚡ Real‑time scoring API

🧠 Supervised ML

🕵️ Anomaly detection

📏 Configurable rules engine

📊 Monitoring + audit logging

📈 MLflow experiment tracking

🐳 Docker + CI/CD

🎨 Responsive React frontend

---

🛠️ TECHNOLOGIES
Backend: 🐍 Python • ⚡ FastAPI • 📊 Scikit‑Learn • 🚀 XGBoost • 📈 MLflow • 🧪 Pytest • 🐳 Docker
Frontend: ⚛️ React • ⚡ Vite • 📜 JSX • 🎨 Bootstrap

---

👨‍💻 AUTHOR
Thabang Rakeng

---

⭐ FINAL NOTE
FinShield showcases how engineering + ML + rules + anomaly detection + monitoring + frontend UX combine into a modern fraud detection platform.

If you found this useful, ⭐ the repo and help it shine! ✨

