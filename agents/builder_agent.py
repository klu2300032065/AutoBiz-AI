import ollama
import os
import re
from tools.file_manager import create_directory, create_file, WORKSPACE_DIR
from tools.test_runner import run_frontend_build, run_backend_tests, run_basic_api_tests
from tools.code_runner import run_command

class BuilderAgent:
    def run(self, product_spec: str) -> str:
        # Step 1: Analyze requirements & Step 2: Create build specification
        analysis_prompt = f"""
        Given the following product specification:
        {product_spec}
        
        Create a comprehensive build plan for a React+Vite frontend and a FastAPI+SQLite backend.
        Return the files using EXACTLY this format for each file:

        ---FILE: path/to/file.ext---
        file content here
        ---END_FILE---

        Do NOT use markdown code blocks around the file content. Just the raw text.

        Required files to generate:
        1. backend/main.py (FastAPI app)
        2. backend/requirements.txt (fastapi, uvicorn, pytest)
        3. frontend/package.json (Vite react app)
        4. frontend/index.html
        5. frontend/vite.config.js
        6. frontend/src/main.jsx
        7. frontend/src/App.jsx
        """
        
        print("Generating architecture and code... (this may take a while)")
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": analysis_prompt}]
        )
        
        raw_response = response["message"]["content"]
        print(f"--- RAW LLM OUTPUT ---\n{raw_response}\n----------------------")
        
        project_name = "student-expense-tracker"
        project_dir = os.path.join(WORKSPACE_DIR, project_name)
        
        # Step 4: Create project directory
        create_directory(project_dir)
        create_directory(os.path.join(project_dir, "frontend"))
        create_directory(os.path.join(project_dir, "backend"))
        
        files_created = []
        
        # Parse files using regex
        pattern = r"---FILE:\s*(.+?)---\n(.*?)(?=\n---END_FILE---|\n---FILE:|$)"
        matches = re.finditer(pattern, raw_response, re.DOTALL)
        
        for match in matches:
            file_path = match.group(1).strip()
            file_content = match.group(2).strip()
            full_path = os.path.join(project_dir, file_path)
            create_file(full_path, file_content)
            files_created.append(file_path)
                
        # Step 10: Install backend dependencies
        print("Installing dependencies...")
        backend_dir = os.path.join(project_dir, "backend")
        run_command("pip install -r requirements.txt", backend_dir)
        
        # Step 11, 12: Run Tests
        print("Running tests...")
        frontend_res = run_frontend_build(project_dir)
        backend_res = run_backend_tests(project_dir)
        api_res = run_basic_api_tests(project_dir)
        
        # Step 13, 14: Fix straightforward errors
        errors_fixed = "None (Auto-fix disabled for V1 safety)"
        
        # Step 15: Return final build report
        report = f"""
==================================================
BUILD REPORT
==================================================

PROJECT
-------
Name: {project_name}

LOCATION:
{project_dir}

TECH STACK:
React + Vite (Frontend)
FastAPI + SQLite (Backend)

FEATURES
--------
- Automatically derived from specification

FILES CREATED
-------------
{chr(10).join(files_created)}

TEST RESULTS
------------
Frontend Build: {frontend_res['status']} 
Backend Syntax: {backend_res['status']}
Backend Tests: {api_res['status']}

ERRORS FIXED
------------
{errors_fixed}

REMAINING ISSUES
----------------
Frontend Error: {frontend_res.get('error', 'None')}
Backend Error: {backend_res.get('error', 'None')}
API Test Error: {api_res.get('error', 'None')}

RUN COMMAND
-----------
Frontend: cd {os.path.join(project_dir, 'frontend')} && npm run dev
Backend: cd {os.path.join(project_dir, 'backend')} && uvicorn main:app --reload
"""
        return report
