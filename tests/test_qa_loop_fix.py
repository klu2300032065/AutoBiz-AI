import os
import pytest
from tools.file_manager import sanitize_project_name, get_project_path, WORKSPACE_DIR
from models.business_state import BusinessState
from memory.business_memory import BusinessMemory
from agents.orchestrator import Orchestrator

def test_path_sanitization_normal():
    assert sanitize_project_name("Medical Billing Automation") == "medical_billing_automation"
    assert sanitize_project_name("B2B Invoice Automation for Logistics") == "b2b_invoice_automation_for_logistics"
    assert sanitize_project_name("Student Expense Tracker") == "student_expense_tracker"

def test_path_sanitization_symbols_and_numbers():
    assert sanitize_project_name("1. Medical billing automation software for small medical practices") == "1_medical_billing_automation_software_for_small_medical_practices"

def test_path_sanitization_rejections():
    unsafe_inputs = [
        "../etc/passwd",
        "..\\Windows\\System32",
        "C:\\Users\\admin",
        "D:\\Project",
        "\\\\server\\share",
        "//server/share",
        "foo/bar",
        "foo\\bar",
        "project\0nullbyte"
    ]
    for unsafe in unsafe_inputs:
        with pytest.raises(ValueError):
            sanitize_project_name(unsafe)

def test_get_project_path_inside_workspace():
    path = get_project_path("Medical Billing Automation")
    assert os.path.isabs(path)
    assert os.path.normcase(path).startswith(os.path.normcase(WORKSPACE_DIR))
    assert os.path.basename(path) == "medical_billing_automation"

def test_builder_qa_path_contract():
    raw_spec = "1. Medical billing automation software for small medical practices"
    builder_path = get_project_path(raw_spec)
    qa_input = "Run QA on " + raw_spec
    qa_path = get_project_path(qa_input)
    assert builder_path == qa_path

def test_qa_max_retries_halting():
    memory = BusinessMemory()
    # Create isolated test cycle
    test_state = memory.create_new_cycle()
    c_id = test_state.cycle_id
    
    test_state.product = "Test Safety Product"
    test_state.stage = "BUILD_COMPLETED"
    test_state.build_status = "COMPLETED"
    test_state.qa = "FAIL"
    test_state.qa_retry_count = 0
    memory.update_business_state(test_state)
    
    orchestrator = Orchestrator()
    
    def complete_pending_tasks():
        tasks = memory.get_all_tasks(cycle_id=c_id)
        for t in tasks:
            if t.status == "PENDING":
                t.status = "COMPLETED"
                memory.update_task(t)
    
    # Attempt 1 -> retry count should become 1
    action1 = orchestrator.determine_next_action()
    s1 = memory.get_business_state(cycle_id=c_id)
    assert action1 == "BUILD_PRODUCT"
    assert s1.qa_retry_count == 1
    assert s1.qa is None
    complete_pending_tasks()
    
    # Simulate QA failure on attempt 1
    s1.qa = "FAIL"
    memory.update_business_state(s1)
    
    # Attempt 2 -> retry count should become 2
    action2 = orchestrator.determine_next_action()
    s2 = memory.get_business_state(cycle_id=c_id)
    assert action2 == "BUILD_PRODUCT"
    assert s2.qa_retry_count == 2
    complete_pending_tasks()
    
    # Simulate QA failure on attempt 2
    s2.qa = "FAIL"
    memory.update_business_state(s2)
    
    # Attempt 3 -> retry count should become 3
    action3 = orchestrator.determine_next_action()
    s3 = memory.get_business_state(cycle_id=c_id)
    assert action3 == "BUILD_PRODUCT"
    assert s3.qa_retry_count == 3
    complete_pending_tasks()
    
    # Simulate QA failure on attempt 3
    s3.qa = "FAIL"
    memory.update_business_state(s3)
    
    # Attempt 4 -> Max retries (3) reached -> Must halt with WAIT FOR APPROVAL & QA_FAILED_FINAL
    action4 = orchestrator.determine_next_action()
    s4 = memory.get_business_state(cycle_id=c_id)
    assert action4 == "WAIT FOR APPROVAL"
    assert s4.stage == "QA_FAILED_FINAL"
    
    # Attempt 5 -> Still halted, no new builds
    action5 = orchestrator.determine_next_action()
    assert action5 == "WAIT FOR APPROVAL"
