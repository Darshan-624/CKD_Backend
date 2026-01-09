from fastapi import APIRouter, HTTPException, Depends, status
from app.db.supabase import supabase
from app.models.prediction import PredictionRequest, PredictionResponse
from app.core.auth_dependency import get_current_user
from app.services.prediction_service import make_prediction

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse, summary="Make CKD Prediction")
async def predict_ckd(
    request: PredictionRequest,
    current_user = Depends(get_current_user)
):
    """
    Create a health record, make CKD prediction, and store results.
    Requires authentication.
    """
    try:
        user_id = current_user.id
        
        # Fetch user profile to get age, gender, hypertension, diabetes
        profile_response = supabase.table("profiles").select("*").eq("id", user_id).execute()
        
        if not profile_response.data or len(profile_response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )
        
        profile = profile_response.data[0]
        
        # Create health record entry
        health_record_data = {
            "user_id": user_id,
            "specific_gravity": request.specific_gravity,
            "albumin": request.albumin,
            "blood_glucose": request.blood_glucose_random,
            "serum_creatinine": request.serum_creatinine,
            "sodium": request.sodium,
            "hemoglobin": request.hemoglobin,
            "packed_cell_volume": request.packed_cell_volume,
            "red_blood_cell_count": request.red_blood_cell_count
        }
        
        health_record_response = supabase.table("health_records").insert(health_record_data).execute()
        
        if not health_record_response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create health record"
            )
        
        record_id = health_record_response.data[0]["id"]
        
        # Prepare data for ML model prediction
        patient_data = {
            "age": request.age,
            "sex": request.sex,
            "sg": request.specific_gravity,
            "al": request.albumin,
            "bgr": request.blood_glucose_random,
            "sc": request.serum_creatinine,
            "sod": request.sodium,
            "hemo": request.hemoglobin,
            "pcv": request.packed_cell_volume,
            "rc": request.red_blood_cell_count,
            "htn": request.hypertension,
            "dm": request.diabetes_mellitus
        }
        
        # Make prediction
        prediction_result = make_prediction(patient_data)
        
        # Store prediction in database
        prediction_data = {
            "record_id": record_id,
            "user_id": user_id,
            "ckd_prediction": prediction_result["ckd_diagnosis"],
            "risk_probability": prediction_result["risk_probability"],
            "ckd_stage": prediction_result["ckd_stage"],
            "egfr_value": prediction_result["egfr"],
            "top_factors": prediction_result["top_factors"]
        }
        
        prediction_response = supabase.table("predictions").insert(prediction_data).execute()
        
        if not prediction_response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store prediction"
            )
        
        # Return prediction response
        return PredictionResponse(
            ckd_diagnosis=prediction_result["ckd_diagnosis"],
            risk_probability=prediction_result["risk_probability"],
            top_factors=prediction_result["top_factors"],
            egfr=prediction_result["egfr"] if prediction_result["egfr"] else 0.0,
            ckd_stage=prediction_result["ckd_stage"] if prediction_result["ckd_stage"] else "N/A"
        )
    
    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid input data: {str(ve)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )