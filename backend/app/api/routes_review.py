from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import reviews_col
from datetime import datetime

router = APIRouter()

class ReviewInput(BaseModel):
    transaction_id: str
    decision: str # APPROVE, REJECT, INVESTIGATE
    comment: str
    analyst_id: str

@router.post("/review")
def submit_review(review: ReviewInput):
    if reviews_col is None:
        raise HTTPException(status_code=500, detail="Database not available")
        
    doc = review.model_dump()
    doc["timestamp"] = datetime.utcnow().isoformat()
    
    reviews_col.update_one(
        {"transaction_id": review.transaction_id},
        {"$set": doc},
        upsert=True
    )
    
    return {"message": "Review submitted successfully"}
