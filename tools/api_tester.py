import os
import subprocess
import time
import urllib.request
import urllib.error

def test_backend_api(project_path: str) -> dict:
    """
    Starts the FastAPI server, pings standard endpoints, and returns the results.
    """
    backend_dir = os.path.join(project_path, "backend")
    main_py = os.path.join(backend_dir, "main.py")
    
    if not os.path.exists(main_py):
        return {"status": "SKIPPED", "details": "No backend main.py found to test."}
        
    results = {
        "status": "PASS",
        "details": "",
        "errors": []
    }
    
    import sys
    # Start the server
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for startup
        time.sleep(3)
        
        # Check if process crashed immediately
        if process.poll() is not None:
            stderr = process.stderr.read().decode("utf-8")
            return {
                "status": "FAIL",
                "details": "Backend crashed immediately on startup.",
                "errors": [stderr]
            }
            
        # Test basic endpoints
        endpoints = ["/", "/docs"]
        for ep in endpoints:
            url = f"http://localhost:8000{ep}"
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status >= 400:
                        results["status"] = "FAIL"
                        results["errors"].append(f"Endpoint {ep} returned status {response.status}")
            except urllib.error.URLError as e:
                results["status"] = "FAIL"
                results["errors"].append(f"Endpoint {ep} failed: {str(e)}")
            except Exception as e:
                results["status"] = "FAIL"
                results["errors"].append(f"Endpoint {ep} error: {str(e)}")
                
    except Exception as e:
        return {
            "status": "FAIL",
            "details": "Failed to start backend process.",
            "errors": [str(e)]
        }
    finally:
        # Terminate server
        try:
            process.terminate()
            process.wait(timeout=5)
        except Exception:
            process.kill()
            
    if not results["errors"]:
        results["details"] = "Backend API successfully started and responded to basic ping."
        
    return results
