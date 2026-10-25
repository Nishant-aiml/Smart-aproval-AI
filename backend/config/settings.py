"""
Application configuration settings
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    # MongoDB (supports both MONGODB_URL and MONGODB_URI)
    MONGODB_URL: Optional[str] = None
    MONGODB_URI: Optional[str] = None  # Alternative name for compatibility
    MONGODB_DB_NAME: str = "smart_approval_ai"
    
    # AI Provider: 'gemini' (primary, fastest, free tier) or 'openai'
    AI_PROVIDER: str = os.environ.get("AI_PROVIDER", "glm")
    
    # GLM (Zhipu AI BigModel - Free Generous Tier)
    GLM_API_KEY: Optional[str] = os.environ.get("GLM_API_KEY")
    GLM_BASE_URL: str = os.environ.get("GLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
    GLM_MODEL: str = os.environ.get("GLM_MODEL", "GLM-4.7-Flash")
    GLM_MODEL_FALLBACK: str = os.environ.get("GLM_MODEL_FALLBACK", "GLM-4.7-Flash")
    
    # Google Gemini (PRIMARY - Free Tier, Cheapest & Fastest)
    GEMINI_API_KEY: Optional[str] = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    GEMINI_MODEL: str = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")  # Primary AI model - Gemini 1.5 Flash (free tier, fastest, cheapest)
    GEMINI_MODEL_FALLBACK: str = os.environ.get("GEMINI_MODEL_FALLBACK", "gemini-2.0-flash")  # Fast fallback
    
    # OpenAI (Fallback when Gemini unavailable)
    OPENAI_API_KEY: Optional[str] = os.environ.get("OPENAI_API_KEY")
    OPENAI_MODEL_PRIMARY: str = os.environ.get("OPENAI_MODEL_PRIMARY", "gpt-4o-mini")
    OPENAI_MODEL_FALLBACK: str = os.environ.get("OPENAI_MODEL_FALLBACK", "gpt-4o-mini")
    
    # Firebase
    FIREBASE_PROJECT_ID: Optional[str] = os.environ.get("FIREBASE_PROJECT_ID")
    FIREBASE_STORAGE_BUCKET: Optional[str] = None  # Firebase Storage bucket name
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None  # Path to service account JSON
    
    # Database
    DATABASE_URL: Optional[str] = None  # PostgreSQL connection string (Supabase) or SQLite fallback
    
    # Unstructured-IO
    UNSTRUCTURED_API_KEY: Optional[str] = None
    UNSTRUCTURED_LOCAL: bool = True
    
    # Storage
    UPLOAD_DIR: str = "storage/uploads"
    REPORTS_DIR: str = "storage/reports"
    EVIDENCE_DIR: str = "storage/evidence"
    # Maximum single file size (safety limit) - 50 MB
    MAX_FILE_SIZE: int = 50 * 1024 * 1024
    
    # Processing
    CLASSIFICATION_CONFIDENCE_THRESHOLD: float = 0.7
    EXTRACTION_RETRY_LIMIT: int = 3
    CHUNK_SIZE: int = 4000
    CHUNK_OVERLAP: int = 200
    
    # API Security
    API_TOKEN: Optional[str] = None
    
    class Config:
        # Try to find .env file, but don't require it
        env_file = ".env" if Path(".env").exists() else None
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Use MONGODB_URI if MONGODB_URL is not set
        if not self.MONGODB_URL and self.MONGODB_URI:
            self.MONGODB_URL = self.MONGODB_URI
        elif not self.MONGODB_URL:
            self.MONGODB_URL = "mongodb://localhost:27017/"

settings = Settings()
