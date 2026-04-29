"""
Application Settings & Configuration
Manages all environment variables and configuration using Pydantic
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from .env file
    All free-tier friendly configurations
    """
    
    # App Configuration
    APP_NAME: str = "VaidiQ Healthcare"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Server Configuration
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    RELOAD: bool = True
    
    # Database - PostgreSQL (Supabase)
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/vaidiq"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600
    DB_ECHO: bool = False
    
    # Database - MongoDB (Atlas)
    MONGODB_URL: str = "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true"
    MONGODB_DB_NAME: str = "vaidiq_healthcare"
    
    # Redis Cache (Upstash)
    REDIS_URL: str = "redis://default:password@upstash.io:port"
    REDIS_ENABLED: bool = True
    REDIS_TIMEOUT: int = 5
    
    # JWT Configuration
    SECRET_KEY: str = "your-super-secret-key-min-32-chars-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Security
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173", "*"]
    ALLOWED_HOSTS: list = ["localhost", "127.0.0.1", "*"]
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "backend/app/uploads"
    ALLOWED_EXTENSIONS: list = ["pdf", "jpg", "jpeg", "png", "doc", "docx"]
    
    # Email Configuration (Optional)
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_EMAIL: str = "your-email@gmail.com"
    SMTP_PASSWORD: str = "your-app-password"
    SEND_EMAILS: bool = False
    
    # AI/LLM Configuration
    GROQ_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    AI_MODEL: str = "groq"  # "groq" or "gemini"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 500
    
    # Twilio SMS (Optional)
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE: str = ""
    SEND_SMS: bool = False
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/vaidiq.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Used throughout the application
    """
    return Settings()


# Global settings instance
settings = get_settings()
