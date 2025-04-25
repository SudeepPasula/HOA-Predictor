from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

print("✅ Starting FastAPI app with model...")

try:
    model = joblib.load("hoa_model.pkl")
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Error loading model:", e)
    model = None

@app.get("/")
def root():
    return {"message": "Simple prediction app running."}

@app.get("/predict")
def predict(lat: float = 33.2785, lon: float = -96.9951):
    if model is None:
        return {"error": "Model failed to load."}

    # Example features, since we're skipping feature_extractor for now
    example_features = {
        "legalAcreage": 0.34,
        "imprvActualYearBuilt": 2005,
        "improvementValue": 150000,
        "propType": "R",
        "situs_city": "AUBREY",
        "compactness": 18.0
    }

    df = pd.DataFrame([example_features])
    prob = model.predict_proba(df)[0][1]

    return {
        "hoa_probability": round(prob * 100, 2),
        "features_used": example_features
    }
