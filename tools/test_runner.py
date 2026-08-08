import os
from tools.code_runner import run_npm, run_python, run_command

def run_frontend_build(project_dir: str) -> dict:
    """Run npm install and npm run build in the frontend directory."""
    frontend_dir = os.path.join(project_dir, "frontend")
    
    install_res = run_npm("install", frontend_dir)
    if install_res["exit_code"] != 0:
        return {"status": "FAIL", "stage": "install", "error": install_res["stderr"]}
        
    build_res = run_npm("run build", frontend_dir)
    if build_res["exit_code"] != 0:
        return {"status": "FAIL", "stage": "build", "error": build_res["stderr"]}
        
    return {"status": "PASS", "details": build_res["stdout"]}

def run_backend_tests(project_dir: str) -> dict:
    """Run basic python syntax/import check for backend."""
    backend_dir = os.path.join(project_dir, "backend")
    
    # Just a simple check to see if main.py can be compiled
    check_res = run_python("-m py_compile main.py", backend_dir)
    if check_res["exit_code"] != 0:
        return {"status": "FAIL", "error": check_res["stderr"]}
        
    return {"status": "PASS", "details": "Syntax check passed."}

def run_basic_api_tests(project_dir: str) -> dict:
    """Run a simple script to ping the FastAPI server."""
    # This requires the server to be running, or we can just check if pytest passes.
    # For simplicity in V1, we'll assume there's a test file or we just rely on pytest if it exists.
    backend_dir = os.path.join(project_dir, "backend")
    
    # Check if pytest is available and run it
    test_res = run_command("pytest", backend_dir)
    
    if test_res["exit_code"] != 0:
        # If pytest fails or isn't found, we return FAIL
        return {"status": "FAIL", "error": test_res["stderr"] or test_res["stdout"]}
        
    return {"status": "PASS", "details": test_res["stdout"]}
