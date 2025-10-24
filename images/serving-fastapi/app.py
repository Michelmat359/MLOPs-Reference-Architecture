
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow.pyfunc
import numpy as np

app = FastAPI()

MODEL_URI = os.getenv("MODEL_URI", "models:/demo-model/Production")
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow-mlflow.mlops-system.svc.cluster.local:5000")

os.environ.setdefault("MLFLOW_TRACKING_URI", MLFLOW_TRACKING_URI)

class Input(BaseModel):
    features: list

@app.on_event("startup")
def load_model():
    global model
    try:
        model = mlflow.pyfunc.load_model(MODEL_URI)
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

@app.get("/healthz")
def healthz():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
def predict(payload: Input):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        arr = np.array(payload.features, dtype=float)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        preds = model.predict(arr)
        return {"predictions": preds.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
