# AI Risk Manager – Intelligent Payment Fraud Detection

## Problem Statement
Payment fraud is a multi-billion dollar problem. Distinguishing genuine transactions from fraudulent ones in real-time requires sophisticated AI architectures capable of analyzing behavior, time, and location without generating excessive false positives.

## Objectives
- Build a realistic FinTech ML pipeline.
- Accurately predict fraud probabilities using XGBoost.
- Identify novel anomalies using Isolation Forests.
- Provide human-readable AI explanations for risk scores using SHAP values.

## Features
- **Deterministic Risk Engine:** Combines ML probability, anomaly score, and behavioral features into a 0-100 risk score.
- **Explainable AI:** Uses SHAP to extract top risk and mitigating factors.
- **AI Summary Layer:** Generates concise explanations for human analysts.
- **Human-in-the-Loop:** Dashboard to Review, Approve, or Reject high-risk transactions.

## Architecture
- **Backend:** FastAPI, Python, MongoDB
- **Frontend:** React, Vite, TailwindCSS
- **ML Pipeline:** Scikit-learn, XGBoost, Isolation Forest, SHAP

## Installation & Running

### 1. Requirements
- Python 3.10+
- Node.js 18+
- MongoDB running on `mongodb://localhost:27017`

### 2. Generate Data & Train Models
```bash
cd ai-risk-manager/backend
pip install -r requirements.txt
python scripts/generate_data.py
python scripts/train_model.py
```

### 3. Run Backend
```bash
cd ai-risk-manager/backend
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 4. Run Frontend
```bash
cd ai-risk-manager/frontend
npm install
npm run dev
```

## Disclaimer
This project is an educational prototype and is not intended for real financial decision-making or production payment processing.
