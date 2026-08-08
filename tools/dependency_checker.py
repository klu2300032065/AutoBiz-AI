import os
from tools.code_runner import run_npm, run_command

def check_dependencies(project_path: str, tech_info: dict) -> dict:
    """
    Installs dependencies for the detected tech stacks.
    """
    results = {
        "frontend": {"status": "SKIPPED", "details": ""},
        "backend": {"status": "SKIPPED", "details": ""}
    }
    
    frontend_dir = os.path.join(project_path, "frontend")
    backend_dir = os.path.join(project_path, "backend")
    
    if tech_info.get("has_frontend") and "npm" in tech_info.get("frontend_tech", []):
        res = run_npm("install", frontend_dir)
        results["frontend"] = {
            "status": "PASS" if res["exit_code"] == 0 else "FAIL",
            "details": res["stderr"] if res["exit_code"] != 0 else res["stdout"],
            "exit_code": res["exit_code"]
        }
        
    import sys
    if tech_info.get("has_backend") and "pip" in tech_info.get("backend_tech", []):
        # Determine appropriate python/pip command
        # Use simple python -m pip to ensure we use the current env or just pip
        res = run_command(f"{sys.executable} -m pip install -r requirements.txt", backend_dir)
        results["backend"] = {
            "status": "PASS" if res["exit_code"] == 0 else "FAIL",
            "details": res["stderr"] if res["exit_code"] != 0 else res["stdout"],
            "exit_code": res["exit_code"]
        }
        
    return results
