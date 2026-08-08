from pydantic import BaseModel
from typing import List, Optional

class ProductSpec(BaseModel):
    product: str
    problem: str
    target_customers: str
    required_features: List[str]
    suggested_technology: str

class BuildPlan(BaseModel):
    requirements: List[str]
    features: List[str]
    pages: List[str]
    api_endpoints: List[str]
    database_schema: List[str]
    components: List[str]
    project_structure: List[str]
