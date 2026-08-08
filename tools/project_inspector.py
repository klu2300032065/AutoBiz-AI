import os

def inspect_project(project_path: str) -> dict:
    """
    Inspects a generated project directory and detects its technologies.
    """
    info = {
        "has_frontend": False,
        "has_backend": False,
        "frontend_tech": [],
        "backend_tech": [],
        "database_tech": [],
        "structure_issues": []
    }
    
    frontend_dir = os.path.join(project_path, "frontend")
    backend_dir = os.path.join(project_path, "backend")
    
    # Check frontend
    if os.path.exists(frontend_dir):
        info["has_frontend"] = True
        
        # Detect package.json
        pkg_json = os.path.join(frontend_dir, "package.json")
        if os.path.exists(pkg_json):
            info["frontend_tech"].append("npm")
            try:
                with open(pkg_json, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '"react"' in content:
                        info["frontend_tech"].append("React")
                    if '"vite"' in content:
                        info["frontend_tech"].append("Vite")
            except Exception:
                pass
        else:
            info["structure_issues"].append("Frontend directory exists but package.json is missing.")
            
    # Check backend
    if os.path.exists(backend_dir):
        info["has_backend"] = True
        
        req_txt = os.path.join(backend_dir, "requirements.txt")
        if os.path.exists(req_txt):
            info["backend_tech"].append("pip")
            try:
                with open(req_txt, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'fastapi' in content.lower():
                        info["backend_tech"].append("FastAPI")
                    if 'pytest' in content.lower():
                        info["backend_tech"].append("pytest")
            except Exception:
                pass
        else:
            info["structure_issues"].append("Backend directory exists but requirements.txt is missing.")
            
        # Detect SQLite (look for .db or sqlite imports in main.py)
        main_py = os.path.join(backend_dir, "main.py")
        if os.path.exists(main_py):
            info["backend_tech"].append("Python")
            try:
                with open(main_py, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'sqlite3' in content or '.db' in content:
                        info["database_tech"].append("SQLite")
            except Exception:
                pass
        else:
            info["structure_issues"].append("Backend directory exists but main.py is missing.")
            
    if not info["has_frontend"] and not info["has_backend"]:
        info["structure_issues"].append("No frontend or backend directories found.")
        
    return info
