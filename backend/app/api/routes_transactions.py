from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.database import transactions_col, reviews_col
from pydantic import BaseModel

router = APIRouter()

@router.get("/transactions")
def get_transactions(limit: int = 50, skip: int = 0, risk_level: str = None):
    if transactions_col is None:
        return {"error": "Database not available"}
        
    query = {}
    if risk_level:
        query["prediction.risk_level"] = risk_level
        
    cursor = transactions_col.find(query).sort("transaction_time", -1).skip(skip).limit(limit)
    
    results = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
        
    return results

@router.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str):
    if transactions_col is None:
        return {"error": "Database not available"}
        
    doc = transactions_col.find_one({"transaction_id": transaction_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    doc["_id"] = str(doc["_id"])
    
    # Fetch review if exists
    review = reviews_col.find_one({"transaction_id": transaction_id}) if reviews_col is not None else None
    if review:
        review["_id"] = str(review["_id"])
        doc["review"] = review
        
    return doc

class BatchUploadRequest(BaseModel):
    transactions: List[Dict[str, Any]]

@router.post("/transactions/batch")
def upload_batch(req: BatchUploadRequest):
    """
    Saves a batch of transactions (already predicted) to the DB.
    """
    if transactions_col is None:
        return {"error": "Database not available"}
        
    if not req.transactions:
        return {"message": "No transactions provided"}
        
    # Upsert to avoid duplicates
    count = 0
    for txn in req.transactions:
        transactions_col.update_one(
            {"transaction_id": txn["transaction_id"]},
            {"$set": txn},
            upsert=True
        )
        count += 1
        
    return {"message": f"Successfully processed {count} transactions"}
