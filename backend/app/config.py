import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Risk Manager"
    VERSION: str = "1.0.0"
    
    # MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = "ai_risk_manager"
    
    # Risk Thresholds
    LOW_RISK_MAX: int = int(os.getenv("LOW_RISK_MAX", 30))
    MEDIUM_RISK_MAX: int = int(os.getenv("MEDIUM_RISK_MAX", 70))
    
    # Risk Engine Weights
    WEIGHT_FRAUD_PROB: float = float(os.getenv("WEIGHT_FRAUD_PROB", 0.6))
    WEIGHT_ANOMALY: float = float(os.getenv("WEIGHT_ANOMALY", 0.2))
    WEIGHT_BEHAVIORAL: float = float(os.getenv("WEIGHT_BEHAVIORAL", 0.2))
    
    # LLM API
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mock") # "mock", "gemini", "openai"
    
    class Config:
        env_file = ".env"

settings = Settings()
