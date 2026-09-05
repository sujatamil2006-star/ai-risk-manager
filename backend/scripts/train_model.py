import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix
import xgboost as xgb

# Add backend directory to sys.path so we can import app modules
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, '..')
sys.path.append(backend_dir)

from app.ml.preprocessing import validate_data
from app.ml.feature_engineering import create_features

RANDOM_STATE = 42

def train():
    print("Loading data...")
    data_path = os.path.join(current_dir, '..', '..', 'data', 'raw', 'synthetic_transactions.csv')
    df = pd.read_csv(data_path)
    
    print("Validating data...")
    df = validate_data(df)
    
    print("Splitting data...")
    # Chronological or Stratified split. We'll use stratified for synthetic data.
    X = df.drop(columns=['is_fraud'])
    y = df['is_fraud']
    
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE)
    
    print("Feature Engineering...")
    # Generate features on train set, extract stats
    X_train, historical_stats = create_features(X_train_raw, is_training=True)
    # Apply stats to test set to prevent leakage
    X_test, _ = create_features(X_test_raw, is_training=False, historical_stats=historical_stats)
    
    # Define columns for pipeline
    numeric_features = ['transaction_amount', 'transaction_hour', 'transaction_day_of_week', 'user_avg_amount', 'amount_deviation']
    categorical_features = ['merchant_category', 'payment_method']
    passthrough_features = ['new_location', 'new_device'] # Already 0/1
    
    # We drop transaction_id, user_id, transaction_time, location, device from training
    cols_to_drop = ['transaction_id', 'user_id', 'transaction_time', 'location', 'device']
    X_train = X_train.drop(columns=cols_to_drop)
    X_test = X_test.drop(columns=cols_to_drop)
    
    print("Building preprocessing pipeline...")
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features),
            ('pass', 'passthrough', passthrough_features)
        ])
    
    # Fit and transform
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # Get feature names
    cat_encoder = preprocessor.named_transformers_['cat']
    cat_feature_names = cat_encoder.get_feature_names_out(categorical_features)
    feature_names = numeric_features + list(cat_feature_names) + passthrough_features
    
    print("Training XGBoost Classifier...")
    # Handle class imbalance
    scale_pos_weight = (len(y_train) - sum(y_train)) / sum(y_train)
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        random_state=RANDOM_STATE,
        eval_metric='logloss'
    )
    
    xgb_model.fit(X_train_processed, y_train)
    
    print("Evaluating XGBoost...")
    y_pred = xgb_model.predict(X_test_processed)
    y_prob = xgb_model.predict_proba(X_test_processed)[:, 1]
    
    metrics = {
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob),
        "pr_auc": average_precision_score(y_test, y_prob)
    }
    
    cm = confusion_matrix(y_test, y_pred)
    metrics["confusion_matrix"] = {
        "tn": int(cm[0, 0]),
        "fp": int(cm[0, 1]),
        "fn": int(cm[1, 0]),
        "tp": int(cm[1, 1])
    }
    
    print(classification_report(y_test, y_pred))
    
    print("Training Isolation Forest...")
    # Train IF only on normal transactions or whole training set? Usually whole training set is fine if contamination is set.
    iso_forest = IsolationForest(
        n_estimators=100, 
        contamination=0.03, 
        random_state=RANDOM_STATE
    )
    iso_forest.fit(X_train_processed)
    
    print("Saving models and metadata...")
    models_dir = os.path.join(current_dir, '..', '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(xgb_model, os.path.join(models_dir, 'xgboost_fraud_model.pkl'))
    joblib.dump(iso_forest, os.path.join(models_dir, 'isolation_forest.pkl'))
    joblib.dump(preprocessor, os.path.join(models_dir, 'preprocessor.pkl'))
    
    with open(os.path.join(models_dir, 'historical_stats.json'), 'w') as f:
        # Convert sets to list for JSON serialization if any sneaked in
        # We already used dicts in feature_engineering, but let's be safe
        def default_serialize(obj):
            if isinstance(obj, set): return list(obj)
            return obj
        json.dump(historical_stats, f, default=default_serialize)
        
    metadata = {
        "training_date": datetime.now().isoformat(),
        "dataset_size": len(df),
        "features": feature_names,
        "metrics": metrics,
        "model_version": "1.0",
        "random_state": RANDOM_STATE
    }
    
    with open(os.path.join(models_dir, 'model_metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=4)
        
    print("Training complete!")

if __name__ == "__main__":
    train()
