import joblib
import pandas as pd
import shap

# -------------------- Load Model --------------------

model = joblib.load("C:\\React Native\\CKD_BACKEND\\ml_models\\ckd_xgb_model.pkl")
features = joblib.load("C:\\React Native\\CKD_BACKEND\\ml_models\\selected_features.pkl")

explainer = shap.TreeExplainer(model)

# -------------------- Medical Functions --------------------

def calculate_egfr(age, serum_creatinine, sex):
    if sex.lower() == "male":
        egfr = 141 * min(serum_creatinine / 0.9, 1)**(-0.411) * \
               max(serum_creatinine / 0.9, 1)**(-1.209) * (0.993**age)
    else:
        egfr = 144 * min(serum_creatinine / 0.7, 1)**(-0.329) * \
               max(serum_creatinine / 0.7, 1)**(-1.209) * (0.993**age)
    return round(egfr, 2)

def get_ckd_stage(egfr, albumin):
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

# -------------------- User Input --------------------

print("\n--- Enter Patient Data ---")

patient = {
    "age": int(input("Age: ")),
    "sex": input("Sex (male/female): "),
    "sg": float(input("Specific Gravity: ")),
    "al": float(input("Albumin: ")),
    "bgr": float(input("Blood Glucose: ")),
    "sc": float(input("Serum Creatinine: ")),
    "sod": float(input("Sodium: ")),
    "hemo": float(input("Hemoglobin: ")),
    "pcv": float(input("Packed Cell Volume: ")),
    "rc": float(input("Red Blood Cell Count: ")),
    "htn": int(input("Hypertension (1=yes, 0=no): ")),
    "dm": int(input("Diabetes (1=yes, 0=no): "))
}

# -------------------- Prediction --------------------

ml_input = pd.DataFrame([patient])[features]

prediction = model.predict(ml_input)[0]
probability = model.predict_proba(ml_input)[0][1]

print("\n--- CKD Diagnosis ---")
print("CKD:", "Yes" if prediction == 1 else "No")
print("Risk Probability:", round(probability, 3))

# -------------------- SHAP Explanation --------------------

shap_values = explainer.shap_values(ml_input)

print("\nTop factors influencing decision:")
impacts = list(zip(features, shap_values[0]))
impacts.sort(key=lambda x: abs(x[1]), reverse=True)

for feat, val in impacts[:5]:
    effect = "increased" if val > 0 else "reduced"
    print(f"- {feat} {effect} CKD risk")

# -------------------- Clinical Staging --------------------

if prediction == 1:
    egfr = calculate_egfr(patient["age"], patient["sc"], patient["sex"])
    stage = get_ckd_stage(egfr, patient["al"])

    print("\n--- Clinical Assessment ---")
    print("eGFR:", egfr)
    print("CKD Stage:", stage)

print("\n✔ Evaluation Complete")
