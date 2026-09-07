import pytest
from models.approval import Approval
from services.approval_manager import ApprovalManager
from memory.business_memory import BusinessMemory

def test_approval_cost_distinction():
    app = Approval(
        approval_id=1,
        action="DEPLOY_PRODUCT",
        description="Approve deployment to production.",
        risk_level="HIGH",
        estimated_cost=50.0,
        actual_cost=0.0,
        demo_cost=50.0,
        deployment_mode="LOCAL/DEMO"
    )
    assert app.estimated_cost == 50.0
    assert app.actual_cost == 0.0
    assert app.demo_cost == 50.0
    assert app.deployment_mode == "LOCAL/DEMO"
    assert app.actual_cost != app.estimated_cost

def test_local_demo_actual_cost_is_zero():
    manager = ApprovalManager()
    memory = BusinessMemory()
    c_id = memory.create_new_cycle().cycle_id
    
    app_id = manager.request_approval(
        action="DEPLOY_PRODUCT",
        description="Approve deployment to production.",
        risk_level="HIGH",
        estimated_cost=50.0,
        actual_cost=100.0,  # Try passing non-zero actual cost for LOCAL/DEMO
        demo_cost=50.0,
        deployment_mode="LOCAL/DEMO",
        cycle_id=c_id
    )
    
    retrieved = memory.get_approval(app_id)
    assert retrieved.deployment_mode == "LOCAL/DEMO"
    assert retrieved.actual_cost == 0.0  # Must be forced to 0 for LOCAL/DEMO
    assert retrieved.estimated_cost == 50.0

def test_cycle_5_cost_reporting(capsys):
    memory = BusinessMemory()
    c_id = 5
    cycle_approvals = memory.get_approvals_for_cycle(cycle_id=c_id)
    deploy_app = next((a for a in cycle_approvals if a.action == "DEPLOY_PRODUCT"), None)
    
    assert deploy_app is not None
    assert deploy_app.estimated_cost == 50.0
    assert deploy_app.actual_cost == 0.0
    assert deploy_app.deployment_mode == "LOCAL/DEMO"
