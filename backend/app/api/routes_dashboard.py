from fastapi import APIRouter
from app.database import transactions_col

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_stats():
    if transactions_col is None:
        return {"error": "Database not available", "stats": _mock_stats()}
        
    total = transactions_col.count_documents({})
    high = transactions_col.count_documents({"prediction.risk_level": "HIGH"})
    medium = transactions_col.count_documents({"prediction.risk_level": "MEDIUM"})
    low = transactions_col.count_documents({"prediction.risk_level": "LOW"})
    
    # Calculate average risk score
    pipeline = [
        {"$group": {"_id": None, "avg_score": {"$avg": "$prediction.risk_score"}}}
    ]
    avg_score_res = list(transactions_col.aggregate(pipeline))
    avg_score = avg_score_res[0]["avg_score"] if avg_score_res else 0
    
    # Recent high risk
    recent_high = list(transactions_col.find({"prediction.risk_level": "HIGH"}).sort("transaction_time", -1).limit(5))
    for r in recent_high:
        r["_id"] = str(r["_id"])
        
    return {
        "stats": {
            "total_transactions": total,
            "high_risk": high,
            "medium_risk": medium,
            "low_risk": low,
            "average_risk_score": round(avg_score, 1)
        },
        "recent_high_risk": recent_high
    }

def _mock_stats():
    return {
        "total_transactions": 0,
        "high_risk": 0,
        "medium_risk": 0,
        "low_risk": 0,
        "average_risk_score": 0
    }
