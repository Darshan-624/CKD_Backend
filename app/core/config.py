import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SECRET_KEY: str
    EXPIRATION_TIME_SECONDS: int = 3600 # Default to 1 hour if not set

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()