# HOA Predictor 🏘️

An AI-powered web application to predict the likelihood that a property is part of a Homeowners Association (HOA) — using geospatial features, machine learning, and Gemini AI.

---

## 🚀 Features
- 📍 Interactive map (Leaflet.js)
- 🧠 Machine Learning model predicts HOA likelihood based on parcel data
- 🔎 Geospatial feature extraction (acreage, year built, improvement value, compactness)
- 🛣️ Sidewalk detection using OpenStreetMap (OSM)
- 🤖 Gemini AI integration for final probability refinement
- 🌎 Click anywhere or search an address to get instant HOA predictions

---

## 🛠️ Technology Stack
- Frontend: React.js (Vite) + Leaflet.js
- Backend: FastAPI (Python)
- AI Model: Google Gemini 1.5 Pro
- Data: GeoJSON parcel data, OSM sidewalks

---

## 📦 How to Run Locally

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
