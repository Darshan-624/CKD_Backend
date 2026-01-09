import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    EXPIRATION_TIME_SECONDS: int = 3600 # Default to 1 hour if not set


settings = Settings()