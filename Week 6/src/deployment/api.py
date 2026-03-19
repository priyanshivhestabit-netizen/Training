from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, create_model
import pickle, uuid, csv, os, json
from datetime import datetime
from typing import Any

app = FastAPI(title="Churn Predictor API", version="1.0")

MODEL_PATH = os.getenv("MODEL_PATH", "src/models/best_model.pkl")
LOG_FILE   = "src/logs/prediction_logs.csv"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Load the exact feature list used during training
with open("src/features/feature_list.json") as f:
    FEATURE_NAMES = json.load(f)

# Dynamically build the Pydantic model with all required fields
field_definitions = {name: (float, ...) for name in FEATURE_NAMES}
ChurnFeatures = create_model("ChurnFeatures", **field_definitions)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["request_id","timestamp","features","prediction","probability"])

@app.post("/predict")
def predict(data: ChurnFeatures):
    request_id = str(uuid.uuid4())

    # Build feature vector in the exact order the model expects
    features = [[data.dict()[name] for name in FEATURE_NAMES]]

    try:
        prediction  = int(model.predict(features)[0])
        probability = float(model.predict_proba(features)[0][1])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    with open(LOG_FILE, "a", newline="") as f:
        csv.writer(f).writerow([
            request_id, datetime.utcnow().isoformat(),
            data.dict(), prediction, round(probability, 4)
        ])

    return {
        "request_id":       request_id,
        "churn_prediction": prediction,
        "churn_probability": round(probability, 4),
        "model_version":    "1.0"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/features")
def get_features():
    """Returns the list of features the model expects."""
    return {"features": FEATURE_NAMES, "count": len(FEATURE_NAMES)}