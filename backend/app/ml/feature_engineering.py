import pandas as pd
import numpy as np

def create_features(df: pd.DataFrame, is_training: bool = True, historical_stats: dict = None) -> tuple:
    """
    Creates behavioral and temporal features.
    To prevent data leakage, historical_stats must be pre-calculated from training data ONLY,
    or calculated on-the-fly during training.
    """
    df = df.copy()
    
    # Temporal features
    df['transaction_hour'] = df['transaction_time'].dt.hour
    df['transaction_day_of_week'] = df['transaction_time'].dt.dayofweek
    
    # Calculate historical stats if training
    if is_training:
        historical_stats = {}
        # Calculate mean amount per user
        user_means = df.groupby('user_id')['transaction_amount'].mean().to_dict()
        historical_stats['user_means'] = user_means
        
        # Calculate known locations per user
        user_locations = df.groupby('user_id')['location'].apply(set).to_dict()
        historical_stats['user_locations'] = user_locations
        
        # Calculate known devices per user
        user_devices = df.groupby('user_id')['device'].apply(set).to_dict()
        historical_stats['user_devices'] = user_devices
        
    # Apply historical stats
    user_means = historical_stats.get('user_means', {})
    user_locations = historical_stats.get('user_locations', {})
    user_devices = historical_stats.get('user_devices', {})
    
    # Default mean for unknown users: global mean (or just 1000)
    global_mean = np.mean(list(user_means.values())) if user_means else 1000
    
    df['user_avg_amount'] = df['user_id'].map(user_means).fillna(global_mean)
    df['amount_deviation'] = df['transaction_amount'] / (df['user_avg_amount'] + 1e-5)
    
    # Behavioral features
    def is_new_location(row):
        known = user_locations.get(row['user_id'], set())
        return 0 if row['location'] in known else 1

    def is_new_device(row):
        known = user_devices.get(row['user_id'], set())
        return 0 if row['device'] in known else 1
        
    df['new_location'] = df.apply(is_new_location, axis=1)
    df['new_device'] = df.apply(is_new_device, axis=1)
    
    # One-hot encoding for categorical (using pd.get_dummies for simplicity, but in prod use OneHotEncoder)
    # We will use scikit-learn OneHotEncoder in the training pipeline to ensure consistent columns.
    
    return df, historical_stats
