import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set seed for reproducibility
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
random.seed(RANDOM_STATE)

NUM_USERS = 1000
NUM_TRANSACTIONS = 50000
FRAUD_RATE = 0.03 # 3% fraud

def generate_synthetic_data(num_users=NUM_USERS, num_transactions=NUM_TRANSACTIONS):
    print(f"Generating {num_transactions} transactions for {num_users} users...")
    
    # User profiles
    users = []
    locations = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"]
    devices = ["Android", "iOS", "Windows", "Mac"]
    
    for i in range(num_users):
        user_id = f"USER{i+1:04d}"
        base_amount = np.random.lognormal(mean=np.log(1000), sigma=1.0)
        base_amount = max(50, min(base_amount, 50000)) # clip between 50 and 50k
        home_location = random.choice(locations)
        primary_device = random.choice(devices)
        users.append({
            "user_id": user_id,
            "mean_amount": base_amount,
            "home_location": home_location,
            "primary_device": primary_device
        })
        
    user_df = pd.DataFrame(users)
    
    transactions = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(num_transactions):
        user = random.choice(users)
        
        is_fraud = np.random.random() < FRAUD_RATE
        
        # Date & Time
        days_offset = np.random.randint(0, 365)
        
        if is_fraud:
            # Fraudulent transactions often happen at odd hours (1 AM to 5 AM)
            if np.random.random() < 0.6:
                hour = np.random.randint(1, 6)
            else:
                hour = np.random.randint(0, 24)
            
            # Higher amounts for fraud
            amount = user['mean_amount'] * np.random.uniform(2.5, 10.0)
            
            # Different location
            location = random.choice([loc for loc in locations if loc != user['home_location']]) if np.random.random() < 0.8 else user['home_location']
            
            # Different device
            device = random.choice([dev for dev in devices if dev != user['primary_device']]) if np.random.random() < 0.7 else user['primary_device']
            
        else:
            # Normal transactions mostly during day
            hour = int(np.random.normal(14, 4))
            hour = max(0, min(23, hour))
            
            # Amount around user's mean
            amount = np.random.normal(user['mean_amount'], user['mean_amount'] * 0.3)
            amount = max(10, amount) # Minimum amount 10
            
            location = user['home_location'] if np.random.random() < 0.9 else random.choice(locations)
            device = user['primary_device'] if np.random.random() < 0.95 else random.choice(devices)
            
        txn_time = start_date + timedelta(days=days_offset, hours=hour, minutes=np.random.randint(0, 60))
        
        merchant_categories = ['Retail', 'Travel', 'Food', 'Entertainment', 'Electronics', 'Utilities']
        payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking']
        
        transactions.append({
            "transaction_id": f"TXN{i+1:06d}",
            "user_id": user['user_id'],
            "transaction_amount": round(amount, 2),
            "transaction_time": txn_time.strftime("%Y-%m-%d %H:%M:%S"),
            "location": location,
            "device": device,
            "merchant_category": random.choice(merchant_categories),
            "payment_method": random.choice(payment_methods),
            "is_fraud": int(is_fraud)
        })
        
    df = pd.DataFrame(transactions)
    df = df.sort_values('transaction_time').reset_index(drop=True)
    
    # Save raw data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, '..', '..', 'data', 'raw')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'synthetic_transactions.csv')
    df.to_csv(output_path, index=False)
    print(f"Dataset generated and saved to {output_path}")
    print("Fraud distribution:")
    print(df['is_fraud'].value_counts(normalize=True))

if __name__ == "__main__":
    generate_synthetic_data()
