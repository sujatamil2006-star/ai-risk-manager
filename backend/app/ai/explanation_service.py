import json
from typing import Dict, Any
from app.config import settings

def generate_explanation(prediction_result: Dict[str, Any], transaction_data: Dict[str, Any]) -> str:
    """
    Generates a natural language explanation of the ML model's decision.
    Uses a mock explanation if no LLM API key is provided, ensuring the system 
    always functions even if the LLM is down.
    """
    
    # Extract key data points for the LLM
    context = {
        "risk_score": prediction_result["risk_score"],
        "risk_level": prediction_result["risk_level"],
        "fraud_probability": round(prediction_result["fraud_probability"] * 100, 1),
        "anomaly_status": prediction_result["anomaly_status"],
        "top_risk_factors": prediction_result["risk_factors"],
        "transaction_amount": transaction_data.get("transaction_amount"),
        "merchant_category": transaction_data.get("merchant_category")
    }
    
    if settings.LLM_PROVIDER == "mock" or not settings.LLM_API_KEY:
        return _mock_explanation(context)
        
    try:
        if settings.LLM_PROVIDER == "openai":
            import openai
            openai.api_key = settings.LLM_API_KEY
            # Make API Call...
            pass # Implement actual call when key is provided
        elif settings.LLM_PROVIDER == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=settings.LLM_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = _build_prompt(context)
            response = model.generate_content(prompt)
            return response.text
            
    except Exception as e:
        print(f"LLM API Error: {e}")
        return "AI explanation service unavailable. " + _mock_explanation(context)

def _build_prompt(context: dict) -> str:
    return f"""
    You are an AI assistant in a payment risk management system. Your job is to concisely explain 
    to a human analyst why a transaction received its specific risk score.
    
    DO NOT invent facts. DO NOT change the risk score or override the model.
    Use ONLY the following structured evidence:
    
    Data:
    Risk Score: {context['risk_score']}/100
    Risk Level: {context['risk_level']}
    Fraud Probability: {context['fraud_probability']}%
    Anomaly Status: {context['anomaly_status']}
    Top Risk Factors: {', '.join(context['top_risk_factors'])}
    Transaction Amount: {context['transaction_amount']}
    Merchant: {context['merchant_category']}
    
    Provide a concise (2-3 sentences), professional explanation summarizing why it was flagged, 
    and output a recommended action (Approve, Reject, or Manual Verification).
    """

def _mock_explanation(context: dict) -> str:
    factors_str = ', '.join([f.split(' (+')[0] for f in context['top_risk_factors']])
    
    if context['risk_level'] == 'HIGH':
        rec = "Manual verification is recommended."
        desc = f"Transaction flagged as high risk due to a fraud probability of {context['fraud_probability']}% and HIGH anomaly status."
    elif context['risk_level'] == 'MEDIUM':
        rec = "Investigate if user history is sparse."
        desc = f"Transaction shows moderate risk indicators."
    else:
        rec = "Approve."
        desc = "Transaction aligns with normal user behavior."
        
    return f"Model Explanation: {desc} Primary risk factors identified: {factors_str}. Recommendation: {rec}"
