import os
import joblib
import json
import pandas as pd
import shap
from typing import Dict, Any

from app.ml.feature_engineering import create_features
from app.ml.risk_engine import calculate_risk_score
from app.ml.explainability import get_shap_explanations

# Global model variables
xgb_model = None
iso_forest = None
preprocessor = None
historical_stats = None
explainer = None
feature_names = None

def load_models():
    global xgb_model, iso_forest, preprocessor, historical_stats, explainer, feature_names
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(current_dir, '..', '..', '..', 'models')
    
    xgb_model = joblib.load(os.path.join(models_dir, 'xgboost_fraud_model.pkl'))
    iso_forest = joblib.load(os.path.join(models_dir, 'isolation_forest.pkl'))
    preprocessor = joblib.load(os.path.join(models_dir, 'preprocessor.pkl'))
    
    with open(os.path.join(models_dir, 'historical_stats.json'), 'r') as f:
        historical_stats = json.load(f)
        
    with open(os.path.join(models_dir, 'model_metadata.json'), 'r') as f:
        metadata = json.load(f)
        feature_names = metadata['features']
        
    explainer = shap.TreeExplainer(xgb_model)

def predict_transaction(txn_data: Dict[str, Any]) -> Dict[str, Any]:
    if xgb_model is None:
        load_models()
        
    # 1. Convert to DataFrame
    df_raw = pd.DataFrame([txn_data])
    
    # 2. Ensure datetime
    df_raw['transaction_time'] = pd.to_datetime(df_raw['transaction_time'])
    
    # 3. Feature Engineering
    df_feat, _ = create_features(df_raw, is_training=False, historical_stats=historical_stats)
    
    # Store behavioral flags for risk engine
    new_device = df_feat['new_device'].iloc[0]
    new_location = df_feat['new_location'].iloc[0]
    amount_deviation = df_feat['amount_deviation'].iloc[0]
    
    # Drop columns not used by model
    cols_to_drop = ['transaction_id', 'user_id', 'transaction_time', 'location', 'device']
    df_model = df_feat.drop(columns=[c for c in cols_to_drop if c in df_feat.columns])
    
    # 4. Preprocess
    X_processed = preprocessor.transform(df_model)
    
    # 5. Predict Fraud Probability
    fraud_prob = float(xgb_model.predict_proba(X_processed)[0, 1])
    
    # 6. Predict Anomaly (-1 is anomaly, 1 is normal in IsolationForest)
    anomaly_pred = iso_forest.predict(X_processed)[0]
    is_anomaly = anomaly_pred == -1
    
    # 7. Calculate Risk Score
    risk_results = calculate_risk_score(fraud_prob, is_anomaly, new_device, new_location, amount_deviation)
    
    # 8. SHAP Explanations
    shap_explanations = get_shap_explanations(explainer, X_processed, feature_names)
    
    return {
        "transaction_id": txn_data.get("transaction_id", "UNKNOWN"),
        "fraud_probability": fraud_prob,
        "anomaly_status": "HIGH" if is_anomaly else "LOW",
        "risk_score": risk_results["risk_score"],
        "risk_level": risk_results["risk_level"],
        "risk_factors": shap_explanations["top_risk_factors"],
        "mitigating_factors": shap_explanations["top_mitigating_factors"]
    }
