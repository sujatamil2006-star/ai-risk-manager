from pymongo import MongoClient
from app.config import settings
import logging
import json
import os

class JSONCollection:
    def __init__(self, filename):
        self.filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', filename)
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)
                
    def _load(self):
        with open(self.filename, 'r') as f:
            return json.load(f)
            
    def _save(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

    def update_one(self, filter_dict, update_dict, upsert=False):
        data = self._load()
        tx_id = filter_dict.get("transaction_id")
        
        # Check if exists
        for i, doc in enumerate(data):
            if doc.get("transaction_id") == tx_id:
                # Update
                if "$set" in update_dict:
                    data[i].update(update_dict["$set"])
                self._save(data)
                return
                
        if upsert and "$set" in update_dict:
            new_doc = update_dict["$set"]
            new_doc["_id"] = str(len(data))
            data.append(new_doc)
            self._save(data)
            
    def find(self, query=None):
        data = self._load()
        if not query:
            return MockCursor(data)
            
        filtered = []
        for doc in data:
            match = True
            for k, v in query.items():
                # basic nested query support for prediction.risk_level
                if k == "prediction.risk_level":
                    if doc.get("prediction", {}).get("risk_level") != v:
                        match = False
                        break
                elif doc.get(k) != v:
                    match = False
                    break
            if match:
                filtered.append(doc)
        return MockCursor(filtered)
        
    def find_one(self, query):
        cursor = self.find(query)
        res = cursor.data
        return res[0] if res else None
        
    def count_documents(self, query):
        return len(self.find(query).data)
        
    def aggregate(self, pipeline):
        # only mock average score for dashboard
        data = self.find().data
        if not data: return []
        total = sum(d.get("prediction", {}).get("risk_score", 0) for d in data)
        return [{"avg_score": total / len(data)}]

class MockCursor:
    def __init__(self, data):
        self.data = data
    def sort(self, key, direction):
        if key == "transaction_time":
            self.data.sort(key=lambda x: x.get(key, ""), reverse=(direction == -1))
        return self
    def skip(self, num):
        self.data = self.data[num:]
        return self
    def limit(self, num):
        self.data = self.data[:num]
        return self
    def __iter__(self):
        return iter(self.data)

try:
    client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=2000)
    client.admin.command('ping') # Force connection check
    db = client[settings.DATABASE_NAME]
    
    # Collections
    transactions_col = db["transactions"]
    reviews_col = db["analyst_reviews"]
    
    # Ensure indexes
    transactions_col.create_index("transaction_id", unique=True)
    transactions_col.create_index("transaction_time")
    transactions_col.create_index("risk_level")
    
    logging.info("Connected to MongoDB.")
    
except Exception as e:
    logging.warning(f"Could not connect to MongoDB: {e}. Falling back to local JSON files.")
    transactions_col = JSONCollection("transactions_db.json")
    reviews_col = JSONCollection("reviews_db.json")

def get_db():
    return None
