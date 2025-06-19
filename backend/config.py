
import os
from typing import List

class Settings:
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-here-min-256-bits")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    # File Upload
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "/app/uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    
    # Chat
    CHAT_SIMULATION: bool = os.getenv("CHAT_SIMULATION", "true").lower() == "true"
    N8N_WEBHOOK_URL: str = os.getenv("N8N_WEBHOOK_URL", "")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
