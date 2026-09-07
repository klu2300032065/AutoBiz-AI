import pytest
from services.approval_manager import ApprovalManager
from services.task_manager import TaskManager
from services.agent_registry import AgentRegistry
from memory.business_memory import BusinessMemory

def test_approval_manager():
    memory = BusinessMemory()
    cycle_id = memory.get_active_cycle_id()
    manager = ApprovalManager()
    
    app_id = manager.request_approval(
        action="TEST_ACTION",
        description="Test approval request",
        risk_level="LOW",
        estimated_cost=10.0,
        cycle_id=cycle_id
    )
    assert app_id is not None

    pending = manager.get_pending_approvals(cycle_id=cycle_id)
    assert any(a.approval_id == app_id for a in pending)

    res = manager.approve(app_id)
    assert res is True

    pending_after = manager.get_pending_approvals(cycle_id=cycle_id)
    assert not any(a.approval_id == app_id for a in pending_after)

def test_task_manager():
    memory = BusinessMemory()
    cycle_id = memory.get_active_cycle_id()
    tm = TaskManager()

    task_id = tm.create_task("TEST_TASK", "Test task description", cycle_id=cycle_id)
    assert task_id is not None

    task = tm.get_next_runnable_task(cycle_id=cycle_id)
    assert task is not None

    tm.update_task_status(task_id, "RUNNING")
    updated_task = memory.get_task(task_id)
    assert updated_task.status == "RUNNING"

def test_agent_registry():
    registry = AgentRegistry()
    agents = registry.list_agents()
    assert "ResearchAgent" in agents
    assert "BuilderAgent" in agents
    assert "QAAgent" in agents
    assert "DeploymentAgent" in agents
    assert "MarketingSalesAnalyticsAgent" in agents
