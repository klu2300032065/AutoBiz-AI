import os
import time
import subprocess
import urllib.request
import urllib.error
import sys

def run_health_check(project_path: str, tech_info: dict) -> dict:
    """
    Checks for a /health endpoint in FastAPI, injects it if missing, and tests it.
    """
    results = {
        "status": "SKIPPED",
        "details": [],
        "errors": []
    }
    
    if not tech_info.get("has_backend") or "FastAPI" not in tech_info.get("backend_tech", []):
        return results
        
    results["status"] = "PASS"
    backend_dir = os.path.join(project_path, "backend")
    main_py = os.path.join(backend_dir, "main.py")
    
    if not os.path.exists(main_py):
        results["status"] = "FAIL"
        results["errors"].append("Backend main.py not found.")
        return results
        
    # Check if /health exists
    with open(main_py, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "@app.get(\"/health\")" not in content and "@app.get('/health')" not in content:
        # Inject health endpoint
        health_code = """
@app.get("/health")
def health_check():
    return {"status": "ok"}
"""
        with open(main_py, "a", encoding="utf-8") as f:
            f.write(health_code)
        results["details"].append("Injected /health endpoint into main.py.")
    else:
        results["details"].append("/health endpoint already exists.")
        
    # Ping the health endpoint
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)
        
        url = "http://localhost:8000/health"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                results["details"].append("Health check passed (HTTP 200).")
            else:
                results["status"] = "FAIL"
                results["errors"].append(f"Health check failed with status {response.status}")
    except Exception as e:
        results["status"] = "FAIL"
        results["errors"].append(f"Failed to hit /health endpoint: {e}")
    finally:
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
            
    return results
