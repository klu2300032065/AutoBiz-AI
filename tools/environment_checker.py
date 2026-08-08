import os

def check_environment(project_path: str, tech_info: dict) -> dict:
    """
    Checks environment configurations and ensures no obvious hardcoded secrets.
    Generates .env.example.
    """
    results = {
        "status": "PASS",
        "details": [],
        "warnings": [],
        "created_env_example": False
    }
    
    env_example_path = os.path.join(project_path, ".env.example")
    
    # Check if .env.example exists, if not create one based on tech
    if not os.path.exists(env_example_path):
        env_content = ""
        if "FastAPI" in tech_info.get("backend_tech", []):
            env_content += "API_URL=http://localhost:8000\n"
            env_content += "SECRET_KEY=your-secret-key-here\n"
        if "SQLite" in tech_info.get("database_tech", []):
            env_content += "DATABASE_URL=sqlite:///./app.db\n"
            
        with open(env_example_path, "w", encoding="utf-8") as f:
            f.write(env_content)
        results["created_env_example"] = True
        results["details"].append("Created .env.example template.")
    else:
        results["details"].append(".env.example already exists.")
        
    # Check for obvious hardcoded secrets (very basic check)
    backend_main = os.path.join(project_path, "backend", "main.py")
    if os.path.exists(backend_main):
        with open(backend_main, "r", encoding="utf-8") as f:
            content = f.read()
            if "password=" in content.lower() or "secret_key=" in content.lower():
                results["warnings"].append("Possible hardcoded secret found in backend/main.py")
                results["status"] = "PASS WITH WARNINGS"
                
    return results
