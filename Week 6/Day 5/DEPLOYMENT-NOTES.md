# Deployment Notes

## Overview
The Telco Churn Prediction model is deployed as a REST API using
FastAPI and Uvicorn, containerized with Docker.

---

## 1. Architecture
```
Client Request
      │
      ▼
POST /predict (FastAPI)
      │
      ▼
Input Validation (Pydantic)
      │
      ▼
Feature Ordering (feature_list.json)
      │
      ▼
Model Inference (best_model.pkl)
      │
      ▼
Prediction Logging (logs/predictions.csv)
      │
      ▼
JSON Response → Client
```

---

## 2. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict` | Returns churn prediction + probability |
| GET | `/health` | Health check |
| GET | `/features` | Lists all 30 expected features |
| GET | `/docs` | Swagger UI (auto-generated) |

### Sample Request
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "gender": 0, "SeniorCitizen": 1, "Partner": 0,
    "Dependents": 0, "tenure": 1, "PhoneService": 1,
    "MultipleLines": 0, "InternetService": 1,
    "OnlineSecurity": 0, "OnlineBackup": 0,
    "DeviceProtection": 0, "TechSupport": 0,
    "StreamingTV": 0, "StreamingMovies": 0,
    "Contract": 0, "PaperlessBilling": 1,
    "PaymentMethod": 2, "MonthlyCharges": 95.0,
    "TotalCharges": 95.0, "charges_per_month": 95.0,
    "is_long_tenure": 0, "is_high_monthly": 1,
    "tenure_sq": 1, "charges_log": 4.56,
    "monthly_log": 4.56, "tenure_x_monthly": 95.0,
    "contract_months": 1, "has_tech_support": 0,
    "has_online_security": 0, "num_services": 1
  }'
```

### Sample Response
```json
{
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "churn_prediction": 1,
  "churn_probability": 0.847,
  "model_version": "1.0"
}
```

---

## 4. Running the API

### Local Development
```bash
uvicorn src.deployment.api:app --reload
# Visit: http://127.0.0.1:8000/docs
```

### Docker
```bash
# Build
docker build -t churn -f src/deployment/Dockerfile .

# Run
docker run -p 8000:8000 churn

# Visit: http://127.0.0.1:8000/docs
```

---

## 5. Prediction Logging

All predictions are saved to `src/logs/predictions.csv`:

| Column | Description |
|--------|-------------|
| request_id | Unique UUID per request |
| timestamp | UTC time of prediction |
| features | Full input JSON |
| prediction | 0 = No Churn, 1 = Churn |
| probability | Churn probability (0.0 - 1.0) |


---

## 6. File Structure
```
src/
├── deployment/
│   ├── api.py              ← FastAPI application
│   └── Dockerfile          ← Container definition
├── models/
│   └── best_model.pkl      ← Trained XGBoost model
├── features/
│   └── feature_list.json   ← 30 feature names in order
├── logs/
│   └── predictions.csv     ← Prediction audit log
requirements.txt            ← Deployment dependencies (9 packages)
requirements-dev.txt        ← Full dev dependencies
.env.example                ← Environment variable template
```

---

## 7. Environment Variables (.env.example)
```
MODEL_PATH=models/best_model.pkl
LOG_FILE=logs/predictions.csv
API_VERSION=1.0
```

