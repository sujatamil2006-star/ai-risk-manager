import pandas as pd
import numpy as np

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates and cleans the raw transaction dataframe.
    """
    initial_len = len(df)
    
    # 1. Missing values
    df = df.dropna(subset=['transaction_id', 'user_id', 'transaction_amount', 'transaction_time', 'is_fraud'])
    
    # 2. Duplicate rows
    df = df.drop_duplicates(subset=['transaction_id'])
    
    # 3. Invalid amounts (negative or zero)
    df = df[df['transaction_amount'] > 0]
    
    # 4. Incorrect data types
    df['transaction_time'] = pd.to_datetime(df['transaction_time'], errors='coerce')
    df = df.dropna(subset=['transaction_time'])
    
    df['is_fraud'] = df['is_fraud'].astype(int)
    
    dropped = initial_len - len(df)
    if dropped > 0:
        print(f"Validation dropped {dropped} invalid rows.")
        
    return df
