import shap
import numpy as np

# We'll use a globally initialized explainer in the prediction pipeline
def get_shap_explanations(explainer, X_processed, feature_names):
    """
    Computes SHAP values for the given processed transaction.
    Returns the top risk factors (positive shap values) and mitigating factors (negative shap values).
    """
    shap_values = explainer.shap_values(X_processed)
    
    # For a single prediction
    if len(shap_values.shape) == 1:
        sv = shap_values
    else:
        sv = shap_values[0]
        
    factors = []
    for i, val in enumerate(sv):
        if val != 0:
            factors.append({
                "feature": feature_names[i],
                "contribution": float(val)
            })
            
    # Sort by absolute contribution descending
    factors.sort(key=lambda x: abs(x["contribution"]), reverse=True)
    
    # Format into human-readable strings for top factors
    top_positive = []
    top_negative = []
    
    for f in factors:
        feat = f["feature"]
        val = f["contribution"]
        
        # Friendly names mappings
        if feat == "transaction_amount": name = "Transaction Amount"
        elif feat == "amount_deviation": name = "Deviation from User Average Amount"
        elif feat == "new_device": name = "New/Unrecognized Device"
        elif feat == "new_location": name = "New/Unrecognized Location"
        elif feat == "transaction_hour": name = "Transaction Time"
        elif "cat__merchant_category_" in feat: name = f"Merchant Category: {feat.split('_')[-1]}"
        elif "cat__payment_method_" in feat: name = f"Payment Method: {feat.split('_')[-1]}"
        else: name = feat
        
        if val > 0:
            top_positive.append(f"{name} (+{val:.2f})")
        else:
            top_negative.append(f"{name} ({val:.2f})")
            
    return {
        "top_risk_factors": top_positive[:3],
        "top_mitigating_factors": top_negative[:3]
    }
