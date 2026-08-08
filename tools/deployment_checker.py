from agents.qa_agent import QAAgent

def verify_qa_status(project_name: str) -> dict:
    """
    Runs the QA Agent to verify the project status.
    Returns PASS, PASS WITH WARNINGS, or FAIL.
    """
    qa = QAAgent()
    report = qa.run(project_name)
    
    status = "FAIL"
    if "Status:\nPASS\n" in report or "Status:\nPASS\r\n" in report or "Status:\nPASS" in report.split("STRUCTURE")[0]:
        status = "PASS"
    elif "PASS WITH WARNINGS" in report.split("STRUCTURE")[0]:
        status = "PASS WITH WARNINGS"
        
    return {
        "status": status,
        "qa_report": report
    }
