from fastapi import APIRouter
import json
import os

router = APIRouter()

@router.get("/model/metrics")
def get_model_metrics():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    metadata_path = os.path.join(current_dir, '..', '..', '..', 'models', 'model_metadata.json')
    
    try:
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        return metadata
    except FileNotFoundError:
        return {"error": "Model metadata not found. Please train the model first."}
