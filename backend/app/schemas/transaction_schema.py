from pydantic import BaseModel, Field
from typing import Optional

class TransactionInput(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction ID")
    user_id: str = Field(..., description="User ID")
    transaction_amount: float = Field(..., description="Amount of transaction")
    transaction_time: str = Field(..., description="Timestamp (YYYY-MM-DD HH:MM:SS)")
    location: str = Field(..., description="City or region")
    device: str = Field(..., description="Device used (e.g. Android, iOS)")
    merchant_category: str = Field(..., description="Category of merchant")
    payment_method: str = Field(..., description="Method of payment")

class PredictionResponse(BaseModel):
    transaction_id: str
    fraud_probability: float
    anomaly_status: str
    risk_score: int
    risk_level: str
    risk_factors: list[str]
    mitigating_factors: list[str]
    ai_explanation: str
