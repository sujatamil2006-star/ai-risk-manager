from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.transaction_schema import TransactionInput, PredictionResponse
from app.ml.prediction_pipeline import predict_transaction
from app.ai.explanation_service import generate_explanation
from app.database import transactions_col
from datetime import datetime

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
def predict_single_transaction(txn: TransactionInput):
    try:
        # Convert Pydantic model to dict
        txn_dict = txn.model_dump()
        
        # 1. Run ML Pipeline
        prediction = predict_transaction(txn_dict)
        
        # 2. Get AI Explanation
        explanation = generate_explanation(prediction, txn_dict)
        prediction['ai_explanation'] = explanation
        
        # 3. Save to DB
        if transactions_col is not None:
            doc = {**txn_dict, "prediction": prediction, "created_at": datetime.utcnow().isoformat()}
            transactions_col.update_one(
                {"transaction_id": txn_dict["transaction_id"]},
                {"$set": doc},
                upsert=True
            )
        
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
