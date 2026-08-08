import os
from tools.code_runner import run_python

def run_static_checks(project_path: str, tech_info: dict) -> dict:
    """
    Runs static code checks for syntax errors or basic validation.
    """
    results = {
        "frontend": {"status": "SKIPPED", "details": ""},
        "backend": {"status": "SKIPPED", "details": ""}
    }
    
    frontend_dir = os.path.join(project_path, "frontend")
    backend_dir = os.path.join(project_path, "backend")
    
    # Python syntax check
    if tech_info.get("has_backend") and "Python" in tech_info.get("backend_tech", []):
        main_py = os.path.join(backend_dir, "main.py")
        if os.path.exists(main_py):
            res = run_python("-m py_compile main.py", backend_dir)
            if res["exit_code"] != 0:
                results["backend"] = {
                    "status": "FAIL",
                    "error": res["stderr"] or res["stdout"],
                    "exit_code": res["exit_code"]
                }
            else:
                results["backend"] = {
                    "status": "PASS",
                    "details": "Syntax check passed.",
                    "exit_code": 0
                }
                
    # Frontend static checks (e.g. relying on Vite build in test_runner later)
    # If eslint is present in package.json, we could run it, but for simplicity we rely on the build step.
    
    return results
