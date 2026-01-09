# app/services/prediction_service.py
import joblib
import pandas as pd
import shap
import os
from pathlib import Path

# Get the base directory (CKD_BACKEND)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load model and features
MODEL_PATH = BASE_DIR / "ml_models" / "ckd_xgb_model.pkl"
FEATURES_PATH = BASE_DIR / "ml_models" / "selected_features.pkl"

model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURES_PATH)
explainer = shap.TreeExplainer(model)

def calculate_egfr(age: int, serum_creatinine: float, sex: str) -> float:
    """
    Calculate eGFR using CKD-EPI equation
    """
    if sex.lower() == "male":
        egfr = 141 * min(serum_creatinine / 0.9, 1)**(-0.411) * \
               max(serum_creatinine / 0.9, 1)**(-1.209) * (0.993**age)
    else:
        egfr = 144 * min(serum_creatinine / 0.7, 1)**(-0.329) * \
               max(serum_creatinine / 0.7, 1)**(-1.209) * (0.993**age)
    return round(egfr, 2)

def get_ckd_stage(egfr: float, albumin: float) -> str:
    """
    Determine CKD stage based on eGFR and albumin levels
    """
    if egfr >= 90 and albumin > 0:
        return "Stage 1"
    elif 60 <= egfr < 90 and albumin > 0:
        return "Stage 2"
    elif 45 <= egfr < 60:
        return "Stage 3a"
    elif 30 <= egfr < 45:
        return "Stage 3b"
    elif 15 <= egfr < 30:
        return "Stage 4"
    else:
        return "Stage 5"

def make_prediction(patient_data: dict) -> dict:
    """
    Make CKD prediction and return detailed results
    """
    # Prepare ML input
    ml_input = pd.DataFrame([patient_data])[features]
    
    # Make prediction
    prediction = int(model.predict(ml_input)[0])
    probability = float(model.predict_proba(ml_input)[0][1])
    
    # Get SHAP values for feature importance
    shap_values = explainer.shap_values(ml_input)
    impacts = list(zip(features, shap_values[0]))
    impacts.sort(key=lambda x: abs(x[1]), reverse=True)
    
    # Format top factors
    top_factors = []
    for feat, val in impacts[:5]:
        effect = "increased" if float(val) > 0 else "reduced"
        top_factors.append(f"{feat} {effect} CKD risk")
    
    # Calculate eGFR and stage if CKD is predicted
    egfr = None
    ckd_stage = None
    
    if prediction == 1:
        egfr = calculate_egfr(
            patient_data["age"], 
            patient_data["sc"], 
            patient_data["sex"]
        )
        ckd_stage = get_ckd_stage(egfr, patient_data["al"])
    
    return {
        "ckd_diagnosis": "Yes" if prediction == 1 else "No",
        "risk_probability": round(probability, 3),
        "top_factors": top_factors,
        "egfr": egfr,
        "ckd_stage": ckd_stage
    }
