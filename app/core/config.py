import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "Imóvel Gestão API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database Settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:admin123@postgres:5432/imovel_gestao"
    )

    # Database Pool Settings
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 3600

    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # CORS Settings - URLs permitidas para acessar a API
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5173",
        # Produção
        "https://imobly.onrender.com",  # Frontend
        "https://auth-api-3zxk.onrender.com",  # Auth-API
        "https://backend-non0.onrender.com",  # Backend (self)
    ]

    # File Upload Settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx"}

    # Redis Settings (desabilitado - não sendo usado)
    # REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignorar variáveis extras do Docker


settings = Settings()
