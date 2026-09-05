from app.config import settings

def calculate_risk_score(fraud_prob: float, is_anomaly: bool, new_device: int, new_location: int, amount_deviation: float) -> dict:
    """
    Calculates the final risk score (0-100) using configurable weights.
    Returns the score and the computed risk level.
    """
    # 1. Fraud Probability Component (0-100)
    prob_score = fraud_prob * 100
    
    # 2. Anomaly Component (0 or 100)
    anomaly_score = 100 if is_anomaly else 0
    
    # 3. Behavioral Component (0-100)
    # We penalize new devices, new locations, and extreme amount deviations.
    behavioral_score = 0
    if new_device == 1:
        behavioral_score += 30
    if new_location == 1:
        behavioral_score += 30
        
    # Amount deviation penalty (e.g., if > 3x mean, add penalty up to 40)
    if amount_deviation > 3.0:
        penalty = min(40, (amount_deviation - 3.0) * 10)
        behavioral_score += penalty
        
    behavioral_score = min(100, behavioral_score)
    
    # Final Weighted Score
    final_score = (
        (prob_score * settings.WEIGHT_FRAUD_PROB) +
        (anomaly_score * settings.WEIGHT_ANOMALY) +
        (behavioral_score * settings.WEIGHT_BEHAVIORAL)
    )
    
    final_score = min(100, max(0, int(round(final_score))))
    
    if final_score <= settings.LOW_RISK_MAX:
        risk_level = "LOW"
    elif final_score <= settings.MEDIUM_RISK_MAX:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
        
    return {
        "risk_score": final_score,
        "risk_level": risk_level,
        "components": {
            "fraud_probability_contribution": round(prob_score * settings.WEIGHT_FRAUD_PROB, 2),
            "anomaly_contribution": round(anomaly_score * settings.WEIGHT_ANOMALY, 2),
            "behavioral_contribution": round(behavioral_score * settings.WEIGHT_BEHAVIORAL, 2)
        }
    }
