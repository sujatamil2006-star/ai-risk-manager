import pytest
from app.ml.risk_engine import calculate_risk_score

def test_calculate_risk_score_low():
    fraud_prob = 0.05
    anomaly_score = False
    
    result = calculate_risk_score(fraud_prob, anomaly_score, 0, 0, 0.5)
    score = result["risk_score"]
    status = result["risk_level"]
    
    assert 0 <= score <= 100
    assert status == "LOW"

def test_calculate_risk_score_high():
    fraud_prob = 0.85
    anomaly_score = True
    
    result = calculate_risk_score(fraud_prob, anomaly_score, 1, 1, 15.0)
    score = result["risk_score"]
    status = result["risk_level"]
    
    assert score >= 80
    assert status == "HIGH"

def test_calculate_risk_score_medium():
    fraud_prob = 0.40
    anomaly_score = False
    
    result = calculate_risk_score(fraud_prob, anomaly_score, 1, 0, 2.0)
    score = result["risk_score"]
    status = result["risk_level"]
    
    assert 40 <= score <= 79
    assert status == "MEDIUM"
