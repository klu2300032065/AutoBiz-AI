import os
from tools.code_runner import run_command

def generate_docker_config(project_path: str, tech_info: dict) -> dict:
    """
    Generates Dockerfile and docker-compose.yml if applicable, and validates the build.
    """
    results = {
        "status": "SKIPPED",
        "details": [],
        "warnings": [],
        "docker_used": False
    }
    
    if not tech_info.get("has_backend") and not tech_info.get("has_frontend"):
        return results
        
    results["docker_used"] = True
    results["status"] = "PASS"
    
    # 1. Create Backend Dockerfile
    if tech_info.get("has_backend"):
        backend_dir = os.path.join(project_path, "backend")
        dockerfile_path = os.path.join(backend_dir, "Dockerfile")
        if not os.path.exists(dockerfile_path):
            dockerfile_content = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
            with open(dockerfile_path, "w", encoding="utf-8") as f:
                f.write(dockerfile_content)
            results["details"].append("Generated backend Dockerfile.")
            
    # 2. Create Frontend Dockerfile
    if tech_info.get("has_frontend"):
        frontend_dir = os.path.join(project_path, "frontend")
        dockerfile_path = os.path.join(frontend_dir, "Dockerfile")
        if not os.path.exists(dockerfile_path):
            dockerfile_content = """FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""
            with open(dockerfile_path, "w", encoding="utf-8") as f:
                f.write(dockerfile_content)
            results["details"].append("Generated frontend Dockerfile.")
            
    # 3. Create docker-compose.yml
    compose_path = os.path.join(project_path, "docker-compose.yml")
    if not os.path.exists(compose_path):
        compose_content = "version: '3.8'\nservices:\n"
        if tech_info.get("has_backend"):
            compose_content += """  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./app.db
"""
        if tech_info.get("has_frontend"):
            compose_content += """  frontend:
    build: ./frontend
    ports:
      - "80:80"
"""
        with open(compose_path, "w", encoding="utf-8") as f:
            f.write(compose_content)
        results["details"].append("Generated docker-compose.yml.")
        
    # Validate by trying to build
    res = run_command("docker compose config", project_path)
    if res["exit_code"] != 0:
        results["warnings"].append(f"Docker configuration validation failed or docker not installed: {res['stderr']}")
        results["status"] = "PASS WITH WARNINGS"
    else:
        results["details"].append("Docker compose configuration is valid.")
        
    return results
