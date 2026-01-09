# app/models/auth.py
from pydantic import BaseModel, EmailStr, Field

class UserSignup(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    name: str
    contact: str
    age: int
    gender: str          # "male" or "female"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserVerify(BaseModel):
    email: EmailStr
    token: str          # The 6-digit code or token from the email
    type: str = "signup" # Default to 'signup', but could be 'recovery' for password reset