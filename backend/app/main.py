from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_predict, routes_transactions, routes_dashboard, routes_review, routes_model, routes_upload

app = FastAPI(
    title="AI Risk Manager API",
    description="Intelligent Payment Fraud Detection and Risk Assessment System",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_predict.router, prefix="/api", tags=["Predict"])
app.include_router(routes_transactions.router, prefix="/api", tags=["Transactions"])
app.include_router(routes_dashboard.router, prefix="/api", tags=["Dashboard"])
app.include_router(routes_review.router, prefix="/api", tags=["Review"])
app.include_router(routes_model.router, prefix="/api", tags=["Model"])
app.include_router(routes_upload.router, prefix="/api", tags=["Upload"])

@app.get("/")
def read_root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "ai-risk-manager"}

