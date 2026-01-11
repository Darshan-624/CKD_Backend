# app/models/prediction.py
from pydantic import BaseModel, EmailStr, Field
from typing import List

class PredictionRequest(BaseModel):
    age: int
    sex: str
    specific_gravity: float
    albumin: float
    blood_glucose_random: float
    serum_creatinine: float
    sodium: float
    hemoglobin: float
    packed_cell_volume: float
    red_blood_cell_count: float
    hypertension: int     # 1 or 0
    diabetes_mellitus: int # 1 or 0

class PredictionResponse(BaseModel):
    ckd_diagnosis: str  # "Yes" or "No"
    risk_probability: float
    top_factors: List[str]
    egfr: float
    ckd_stage: str
   
   
    # sugar: float
    # pus_cell: str         # "normal" or "abnormal"
    # pus_cell_clumps: str  # "present" or "notpresent"
    # bacteria: str         # "present" or "notpresent"
    # blood_urea: float
    # red_blood_cells: str  # "normal" or "abnormal"
    # potassium: float
    # white_blood_cell_count: float
    # coronary_artery_disease: int # 1 or 0
    # appetite: str         # "good" or "poor"
    # pedal_edema: str      # "yes" or "no"
    # anemia: str           # "yes" or "no"

class PredictionHistoryItem(BaseModel):
    id: str
    created_at: str
    ckd_prediction: str
    risk_probability: float
    ckd_stage: str
    egfr_value: float
    top_factors: List[str]

class PredictionHistoryResponse(BaseModel):
    predictions: List[PredictionHistoryItem]
