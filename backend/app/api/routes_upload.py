from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io
from app.ml.prediction_pipeline import predict_transaction
from app.ai.explanation_service import generate_explanation
from app.database import transactions_col
from datetime import datetime
import logging

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
        
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        required_cols = ['transaction_id', 'user_id', 'transaction_amount', 'transaction_time', 'location', 'device', 'merchant_category', 'payment_method']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise HTTPException(status_code=400, detail=f"Missing required columns: {', '.join(missing)}")
            
        # Process each row
        results = []
        for _, row in df.iterrows():
            txn_dict = row.to_dict()
            # Ensure proper types
            txn_dict['transaction_amount'] = float(txn_dict['transaction_amount'])
            txn_dict['transaction_time'] = str(txn_dict['transaction_time'])
            
            try:
                # 1. Predict
                prediction = predict_transaction(txn_dict)
                # 2. Explain
                explanation = generate_explanation(prediction, txn_dict)
                prediction['ai_explanation'] = explanation
                
                # 3. Save to DB
                if transactions_col is not None:
                    doc = {**txn_dict, "prediction": prediction, "created_at": datetime.utcnow().isoformat()}
                    transactions_col.update_one(
                        {"transaction_id": txn_dict["transaction_id"]},
                        {"$set": doc},
                        upsert=True
                    )
                results.append(prediction)
            except Exception as row_e:
                logging.error(f"Error processing row {txn_dict.get('transaction_id')}: {row_e}")
                
        return {"message": f"Successfully processed {len(results)} transactions from CSV.", "count": len(results)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process CSV: {str(e)}")
