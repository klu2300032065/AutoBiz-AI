from agents.qa_agent import QAAgent

def verify_qa_status(project_name: str) -> dict:
    """
    Runs the QA Agent to verify the project status.
    Returns PASS, PASS WITH WARNINGS, or FAIL.
    """
    qa = QAAgent()
    qa_res = qa.run(project_name)
    
    if isinstance(qa_res, dict):
        report = qa_res.get("result", "") or ""
        agent_status = qa_res.get("status")
    else:
        report = str(qa_res)
        agent_status = "error" if "error" in report.lower() else "success"
        
    status = "FAIL"
    report_upper = report.upper()
    if "STATUS:\nPASS" in report_upper or "READY FOR DEPLOYMENT" in report_upper or agent_status == "success":
        if "PASS WITH WARNINGS" in report_upper:
            status = "PASS WITH WARNINGS"
        else:
            status = "PASS"
        
    return {
        "status": status,
        "qa_report": report
    }
