import pytest
import os
import sqlite3
from memory.business_memory import BusinessMemory
from models.business_state import BusinessState
from models.task import Task
from models.approval import Approval

@pytest.fixture
def memory():
    return BusinessMemory()

def test_get_active_cycle_id(memory):
    cycle_id = memory.get_active_cycle_id()
    assert isinstance(cycle_id, int)
    assert cycle_id >= 1

def test_set_and_get_objective(memory):
    cycle_id = memory.get_active_cycle_id()
    test_obj = "Test business objective for automation"
    memory.set_objective(test_obj, cycle_id=cycle_id)
    retrieved = memory.get_objective(cycle_id=cycle_id)
    assert retrieved == test_obj

def test_get_and_update_business_state(memory):
    cycle_id = memory.get_active_cycle_id()
    state = memory.get_business_state(cycle_id=cycle_id)
    assert state.cycle_id == cycle_id

    state.product = "Test Product"
    state.stage = "RESEARCH_COMPLETED"
    memory.update_business_state(state)

    updated_state = memory.get_business_state(cycle_id=cycle_id)
    assert updated_state.product == "Test Product"
    assert updated_state.stage == "RESEARCH_COMPLETED"

def test_create_and_get_task(memory):
    cycle_id = memory.get_active_cycle_id()
    task = Task(
        task_id=None,
        type="RESEARCH_PRODUCT",
        description="Research automated testing idea",
        status="PENDING",
        priority=1,
        created_at="2026-08-13T10:00:00",
        updated_at="2026-08-13T10:00:00",
        dependencies=[],
        assigned_agent="ResearchAgent",
        input_data="Automated testing",
        result=None,
        cycle_id=cycle_id
    )
    task_id = memory.create_task(task)
    assert task_id is not None

    retrieved_task = memory.get_task(task_id)
    assert retrieved_task is not None
    assert retrieved_task.type == "RESEARCH_PRODUCT"
    assert retrieved_task.cycle_id == cycle_id

def test_create_and_get_pending_approvals(memory):
    cycle_id = memory.get_active_cycle_id()
    approval = Approval(
        approval_id=None,
        action="APPROVE_PRODUCT",
        description="Approve test product build",
        risk_level="MEDIUM",
        estimated_cost=0.0,
        status="PENDING",
        requested_at="2026-08-13T10:00:00",
        cycle_id=cycle_id
    )
    app_id = memory.create_approval(approval)
    assert app_id is not None

    pending = memory.get_pending_approvals(cycle_id=cycle_id)
    assert any(a.approval_id == app_id for a in pending)

    memory.update_approval(app_id, "APPROVED")
    pending_after = memory.get_pending_approvals(cycle_id=cycle_id)
    assert not any(a.approval_id == app_id for a in pending_after)
