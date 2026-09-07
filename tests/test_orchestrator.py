import pytest
from agents.orchestrator import Orchestrator
from memory.business_memory import BusinessMemory

def test_orchestrator_determine_next_action():
    orchestrator = Orchestrator()
    memory = BusinessMemory()
    cycle_id = memory.get_active_cycle_id()

    action = orchestrator.determine_next_action()
    assert action in [
        "WAIT FOR APPROVAL",
        "RESEARCH_PRODUCT",
        "BUILD_PRODUCT",
        "RUN_QA",
        "PREPARE_DEPLOYMENT",
        "CREATE_MARKETING",
        "IDLE"
    ]
