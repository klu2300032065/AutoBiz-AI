from pydantic import BaseModel
from typing import List, Optional

class Competitor(BaseModel):
    name: str
    features: List[str]
    pricing: str
    source: str

class PricingData(BaseModel):
    observed_market_prices: str
    source: str
    estimated_price_for_our_product: str

class OpportunityScore(BaseModel):
    problem_severity: int
    demand: int
    competition: int
    willingness_to_pay: int
    development_difficulty: int
    scalability: int
    final_score: int
    explanation: str

class ProductOpportunity(BaseModel):
    product: str
    problem: str
    target_customer: str
    real_market_evidence: str
    evidence_sources: List[str]
    competitors: List[Competitor]
    pricing: PricingData
    opportunity_score: OpportunityScore
    recommendation: str
    reason: str
