from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.analytics_service import AnalyticsService
from services.sales_service import SalesService
from services.marketing_service import MarketingService

app = FastAPI(title="MSA API", description="Marketing, Sales & Analytics API for AutoBiz AI")

class CampaignRequest(BaseModel):
    product_name: str
    product_desc: str

@app.get("/analytics/overview")
def get_analytics_overview(product_id: int):
    svc = AnalyticsService()
    return svc.get_overview(product_id)

@app.get("/analytics/sales")
def get_analytics_sales(product_id: int):
    svc = SalesService()
    return svc.calculate_metrics(product_id)

@app.get("/analytics/campaigns")
def get_analytics_campaigns(product_id: int):
    svc = AnalyticsService()
    return svc.get_campaign_performance(product_id)

@app.post("/marketing/campaigns")
def generate_campaign(req: CampaignRequest):
    svc = MarketingService()
    return svc.create_campaign(req.product_name, req.product_desc)

@app.get("/health")
def health_check():
    return {"status": "ok"}
