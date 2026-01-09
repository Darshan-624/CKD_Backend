# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, prediction

app = FastAPI(
    title="CKD Prediction API",
    description="Backend for Capstone Project Review 2 - CKD Self Assessment App",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Register the Auth Router
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Register the Prediction Router
app.include_router(prediction.router, prefix="/api", tags=["Prediction"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "CKD API is running"}