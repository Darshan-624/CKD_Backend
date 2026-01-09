from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.db.supabase import supabase
from app.models.auth import UserSignup, UserLogin, UserVerify

router = APIRouter()

@router.post("/signup", summary="Register a new Patient with Medical History")
def signup(user: UserSignup):
    try:
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })

        if not auth_response.user or not auth_response.user.id:
            raise HTTPException(status_code=400, detail="Signup failed in Supabase Auth")

        user_id = auth_response.user.id

        profile_data = {
            "id": user_id,
            "name": user.name,
            "contact": user.contact,
            "age": user.age,
            "gender": user.gender,
            "hypertension": 0,
            "diabetes": 0
        }

        # Insert into database
        data = supabase.table("profiles").insert(profile_data).execute()

        return {
            "message": "User registered successfully",
            "user_id": user_id,
            "profile": profile_data
        }

    except Exception as e:
        error_msg = str(e)
        if "User already registered" in error_msg:
            raise HTTPException(status_code=400, detail="Email already registered")
        raise HTTPException(status_code=400, detail=f"Registration error: {error_msg}")

@router.post("/login", summary="Login Patient")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": form_data.username,  # OAuth2 uses 'username', but we treat it as email
            "password": form_data.password
        })

        if not auth_response.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            "access_token": auth_response.session.access_token,
            "token_type": "bearer",
            "user": {
                "id": auth_response.user.id,
                "email": auth_response.user.email
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")
    
@router.post("/verify", summary="Verify Email with Token/OTP")
def verify_user(data: UserVerify):
    """
    Verifies the user's email using the token (OTP) sent by Supabase.
    """
    try:
        # verify_otp verifies the token and, if valid, confirms the user.
        # It also returns a session (access_token), effectively logging them in.
        res = supabase.auth.verify_otp({
            "email": data.email,
            "token": data.token,
            "type": data.type
        })

        if not res.user:
            raise HTTPException(status_code=400, detail="Verification failed")

        return {
            "message": "Email verified successfully",
            "access_token": res.session.access_token if res.session else None,
            "user": {
                "id": res.user.id,
                "email": res.user.email
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Verification Error: {str(e)}")