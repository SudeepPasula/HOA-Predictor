import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report
import joblib

# Load enriched sample
df = pd.read_csv("hoa_training_sampled.csv")

# Features and label
X = df.drop(columns=["hoa_label"])
y = df["hoa_label"]

# Define feature types
numeric_features = [
    "legalAcreage",
    "imprvActualYearBuilt",
    "improvementValue",
    "compactness",
    "has_sidewalk"
]
categorical_features = ["propType", "situs_city"]

# Preprocessing pipeline
preprocessor = ColumnTransformer([
    ("num", "passthrough", numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
])

# Full model pipeline using XGBoost
model = make_pipeline(preprocessor, XGBClassifier(n_estimators=100, learning_rate=0.1, use_label_encoder=False, eval_metric='logloss', random_state=42))

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("\n🎯 Model Evaluation:")
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "hoa_model.pkl")
print("\n✅ XGBoost model saved as hoa_model.pkl")
