from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Campaign:
    cycle_id: int
    product_name: str
    objective: str
    target_audience: str
    positioning: str
    compliance_disclaimer: str
    posting_schedule: List[str] = field(default_factory=list)

class CampaignBuilder:
    @staticmethod
    def generate_campaign(cycle_id: int, product_name: str) -> Campaign:
        prod_lower = (product_name or "").lower()
        is_healthcare = any(term in prod_lower for term in ["medical", "health", "clinic", "billing", "hipaa", "doctor"])

        if is_healthcare:
            objective = "Demonstrate operational efficiency gains for small medical clinic billing workflows using a modern automation prototype."
            target_audience = "Office managers, billing coordinators, and clinic administrative leads at small independent medical practices."
            positioning = "A lightweight workflow automation prototype that streamlines invoice tracking and claim matching without complex legacy software."
            disclaimer = (
                "COMPLIANCE NOTICE: Workflow automation prototype for demonstration purposes. "
                "Does NOT assert unverified HIPAA, HITECH, or FDA compliance certifications, nor guaranteed revenue or billing accuracy."
            )
            schedule = [
                "Day 1: Platform Overview (LinkedIn & Facebook)",
                "Day 3: Workflow Demo Simulation (Instagram)",
                "Day 5: Productivity Tip (X / Twitter)",
                "Day 7: Discussion & Feedback (Reddit r/healthit)",
                "Day 10: Case Study Prototype (LinkedIn)"
            ]
        else:
            objective = "Drive awareness and trial signups for logistics workflow automation."
            target_audience = "Logistics directors and accounts payable leads at 3PL and freight forwarding firms."
            positioning = "Automated freight bill line-item matching against purchase orders."
            disclaimer = "B2B SaaS operational software."
            schedule = [
                "Day 1: Feature Launch (LinkedIn)",
                "Day 3: Product Demo (Instagram)",
                "Day 5: AP Tips (X)",
                "Day 7: Discussion (Reddit)"
            ]

        return Campaign(
            cycle_id=cycle_id,
            product_name=product_name,
            objective=objective,
            target_audience=target_audience,
            positioning=positioning,
            compliance_disclaimer=disclaimer,
            posting_schedule=schedule
        )
