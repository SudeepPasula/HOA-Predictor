from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from feature_extractor import get_features_from_point
import joblib
import pandas as pd
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables and Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro-latest",
    generation_config={"temperature": 0.7}
)

app = FastAPI()

# Load model
model = joblib.load("hoa_model.pkl")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "HOA Prediction Backend is running!"}

@app.get("/features")
def get_features(lat: float, lon: float):
    return get_features_from_point(lat, lon)

def ask_gemini_for_hoa_probability(features: dict):
    prompt = f"""
    A residential property has the following attributes:
    - Legal acreage: {features.get('legalAcreage')}
    - Year built: {features.get('imprvActualYearBuilt')}
    - Improvement value: {features.get('improvementValue')}
    - Compactness: {features.get('compactness')}
    - Property type: {features.get('propType')}
    - City: {features.get('situs_city')}
    - Sidewalk present: {"Yes" if features.get("has_sidewalk") else "No"}

    Based on these, estimate the likelihood (as a percentage from 0 to 100) that this property belongs to a Homeowners Association (HOA).

    Only respond with a number.
    """

    try:
        response = gemini_model.generate_content([prompt])
        print("🤖 Gemini raw response:", response.text)
        return float(response.text.strip().split()[0])
    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return None

@app.get("/predict")
def predict(lat: float, lon: float):
    features = get_features_from_point(lat, lon)

    if "error" in features:
        return {"error": features["error"]}

    # Predict with Gemini only
    gemini_prob = ask_gemini_for_hoa_probability(features)

    return {
        "hoa_probability": round(gemini_prob, 2) if gemini_prob is not None else "Unavailable",
        "features_used": features
    }