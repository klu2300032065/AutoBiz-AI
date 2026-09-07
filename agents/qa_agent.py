import os
import json
import ollama
from tools.project_inspector import inspect_project
from tools.dependency_checker import check_dependencies
from tools.code_checker import run_static_checks
from tools.test_runner import run_frontend_build
from tools.api_tester import test_backend_api
from tools.file_manager import _ensure_safe_path, sanitize_project_name, get_project_path

from models.task import Task

class QAAgent:
    def __init__(self):
        self.model = "llama3.2"

    def run(self, task_or_input) -> dict:
        if isinstance(task_or_input, Task):
            task_id = task_or_input.task_id
            input_data = task_or_input.input_data
        else:
            task_id = 0
            input_data = str(task_or_input)

        if not input_data:
            return {"status": "error", "agent": "QAAgent", "task_id": task_id, "result": None, "errors": "No input_data provided"}
            
        project_name = sanitize_project_name(input_data)
        project_path = get_project_path(project_name)
        if not os.path.exists(project_path):
            return {
                "status": "error",
                "agent": "QAAgent",
                "task_id": task_id,
                "result": None,
                "artifacts": [],
                "errors": [f"Error: Project directory {project_path} not found."]
            }
            
        print(f"Inspecting project: {project_name}...")
        tech_info = inspect_project(project_path)
        
        print("Installing dependencies...")
        dep_results = check_dependencies(project_path, tech_info)
        
        print("Running static checks...")
        static_results = run_static_checks(project_path, tech_info)
        
        print("Running frontend build...")
        if tech_info.get("has_frontend"):
            frontend_res = run_frontend_build(project_path)
        else:
            frontend_res = {"status": "SKIPPED", "details": ""}
            
        print("Testing backend API...")
        if tech_info.get("has_backend"):
            api_res = test_backend_api(project_path)
        else:
            api_res = {"status": "SKIPPED", "details": ""}
            
        # Compile initial issues
        issues = []
        if tech_info["structure_issues"]:
            for issue in tech_info["structure_issues"]:
                issues.append({"severity": "HIGH", "desc": issue, "category": "STRUCTURE"})
                
        for k, v in dep_results.items():
            if v["status"] == "FAIL":
                issues.append({"severity": "CRITICAL", "desc": f"Dependency install failed: {v['details'][:200]}", "category": "DEPENDENCIES"})
                
        for k, v in static_results.items():
            if v["status"] == "FAIL":
                issues.append({"severity": "HIGH", "desc": f"Static check failed: {v['error'][:200]}", "category": "CODE", "raw_error": v['error']})
                
        if frontend_res["status"] == "FAIL":
            issues.append({"severity": "CRITICAL", "desc": f"Frontend build failed: {frontend_res['error'][:200]}", "category": "FRONTEND", "raw_error": frontend_res['error']})
            
        if api_res["status"] == "FAIL":
            issues.append({"severity": "CRITICAL", "desc": f"API test failed: {'; '.join(api_res['errors'])[:200]}", "category": "BACKEND", "raw_error": str(api_res['errors'])})
            
        auto_fixes_applied = []
        
        # Auto-fix loop for CODE, FRONTEND, BACKEND issues
        for issue in list(issues):
            if "raw_error" in issue:
                fix_attempt = self.attempt_autofix(project_path, issue["raw_error"])
                if fix_attempt.get("fixed"):
                    auto_fixes_applied.append(fix_attempt["description"])
                    # Remove from current issues
                    issues.remove(issue)
                elif fix_attempt.get("requires_human"):
                    issue["suggested_fix"] = "Human approval required."
        
        # Determine overall status
        status = "PASS"
        if len(issues) > 0:
            status = "PASS WITH WARNINGS"
                
        report = self.generate_report(project_name, tech_info, dep_results, frontend_res, static_results, api_res, issues, auto_fixes_applied, status)
        
        return {
            "status": "success" if status != "FAIL" else "error",
            "agent": "QAAgent",
            "task_id": task_id,
            "result": report,
            "artifacts": [],
            "errors": issues
        }
        
    def attempt_autofix(self, project_path: str, raw_error: str) -> dict:
        prompt = f"""
        An error occurred during testing:
        {raw_error}
        
        If this is a simple syntax error, missing import, or basic configuration issue, provide a fix.
        If it requires architectural changes or complex logic, do not fix it.
        
        Return ONLY valid JSON with this structure:
        {{
            "is_safe": true_or_false,
            "requires_human": true_or_false,
            "file_relative_path": "e.g. backend/main.py",
            "search_text": "exact text to replace",
            "replace_text": "new text",
            "explanation": "what was fixed"
        }}
        """
        try:
            response = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
            raw_response = response["message"]["content"].strip()
            
            # Find the JSON object block
            import re
            match = re.search(r"\{.*\}", raw_response, re.DOTALL)
            if match:
                raw_response = match.group(0)
            
            fix_plan = json.loads(raw_response)
            
            if fix_plan.get("is_safe") and fix_plan.get("file_relative_path"):
                target_file = os.path.join(project_path, fix_plan["file_relative_path"])
                target_file = _ensure_safe_path(target_file)
                if os.path.exists(target_file):
                    with open(target_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    search_text = fix_plan.get("search_text", "")
                    if search_text and search_text in content:
                        new_content = content.replace(search_text, fix_plan.get("replace_text", ""))
                        with open(target_file, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        return {"fixed": True, "description": fix_plan.get("explanation", "Applied fix.")}
            
            if fix_plan.get("requires_human"):
                return {"fixed": False, "requires_human": True}
                
        except Exception as e:
            print(f"Auto-fix error: {e}")
            pass
            
        return {"fixed": False}

    def generate_report(self, project_name, tech_info, dep_results, frontend_res, static_results, api_res, issues, auto_fixes, status) -> str:
        report = f"""
QA REPORT
=========

Project: {project_name}

Status:
{status}

STRUCTURE
---------
{'FAIL' if len(tech_info['structure_issues']) > 0 else 'PASS'}

DEPENDENCIES
------------
{'FAIL' if any(v['status']=='FAIL' for v in dep_results.values()) else 'PASS'}

FRONTEND
--------
{frontend_res['status']}

BACKEND
-------
{static_results.get('backend', {}).get('status', 'SKIPPED')}

DATABASE
--------
SKIPPED (No dedicated DB test implemented yet)

API
---
{api_res['status']}

SECURITY
--------
SKIPPED (No automated security scan implemented yet)

ISSUES FOUND
------------
"""
        if not issues:
            report += "None\n"
        else:
            for issue in issues:
                report += f"\n[{issue['severity']}]\n"
                report += f"Description: {issue['desc']}\n"
                if "suggested_fix" in issue:
                    report += f"Suggested fix: {issue['suggested_fix']}\n"
                    
        report += "\nAUTO-FIXES\n----------\n"
        if not auto_fixes:
            report += "None\n"
        else:
            for fix in auto_fixes:
                report += f"- {fix}\n"
                
        report += "\nREMAINING ISSUES\n----------------\n"
        report += f"{len(issues)} unresolved issues.\n"
        
        report += "\nFINAL RECOMMENDATION\n--------------------\n"
        if status == "PASS":
            report += "READY FOR DEPLOYMENT\n"
        else:
            report += "NOT READY FOR DEPLOYMENT\n"
            
        return report
