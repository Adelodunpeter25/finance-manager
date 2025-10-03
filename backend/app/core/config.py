from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Finance Manager API"
    VERSION: str = "1.0.0"
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    DATABASE_URL: str
    
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    
    REDIS_URL: str = "redis://127.0.0.1:6379/1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
