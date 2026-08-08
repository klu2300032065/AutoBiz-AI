import os
from tools.project_inspector import inspect_project
from tools.deployment_checker import verify_qa_status
from tools.environment_checker import check_environment
from tools.docker_manager import generate_docker_config
from tools.health_checker import run_health_check

class DeploymentAgent:
    def __init__(self):
        pass

    def run(self, project_name: str) -> str:
        project_path = os.path.join(os.getcwd(), "workspace", "generated_projects", project_name)
        if not os.path.exists(project_path):
            return f"Error: Project directory {project_path} not found."
            
        print(f"Deploying {project_name}...")
        
        # 1. Verify QA Status
        print("Checking QA Status...")
        qa_status = verify_qa_status(project_name)
        if qa_status["status"] == "FAIL":
            return "Deployment blocked because QA has failed."
            
        # 2. Inspect project
        print("Inspecting Project...")
        tech_info = inspect_project(project_path)
        
        # 3. Check environment
        print("Checking Environment Configurations...")
        env_res = check_environment(project_path, tech_info)
        
        # 4. Generate Docker configuration
        print("Checking Docker Configuration...")
        docker_res = generate_docker_config(project_path, tech_info)
        
        # 5. Run health check
        print("Running Health Check...")
        health_res = run_health_check(project_path, tech_info)
        
        # 6. Generate deployment report
        report = self.generate_report(
            project_name, 
            qa_status["status"], 
            env_res, 
            docker_res, 
            health_res
        )
        
        # 7. Ask for human approval
        print("\n" + report)
        print("\nDEPLOYMENT READY")
        print("Project:", project_name)
        print("Environment: Production")
        print("QA:", qa_status["status"])
        print("Health Check:", health_res["status"])
        print("Deployment target: Local / Docker")
        
        # The assignment says "Wait for human approval before actual deployment."
        # Because we can't truly pause for interactive input without blocking the test suite, 
        # we will prompt via input() but default to skipping actual deployment.
        approval = input("\nDo you want to deploy this project? (y/n): ").strip().lower()
        if approval == 'y':
            return "\nDeployment process initiated (Simulation only). Success!"
        else:
            return "\nDeployment aborted by user."

    def generate_report(self, project_name, qa_status, env_res, docker_res, health_res) -> str:
        report = f"""
DEPLOYMENT REPORT
=================

Project: {project_name}

QA Status: {qa_status}

Environment Status: {env_res['status']}

Docker Status: {docker_res['status']}

Health Check: {health_res['status']}

Deployment Target: Local / Docker

Deployment Status: PENDING HUMAN APPROVAL

BLOCKERS:
"""
        blockers = []
        if env_res['status'] == 'FAIL': blockers.extend(env_res.get('errors', []))
        if docker_res['status'] == 'FAIL': blockers.extend(docker_res.get('errors', []))
        if health_res['status'] == 'FAIL': blockers.extend(health_res.get('errors', []))
        
        if not blockers:
            report += "None\n"
        else:
            for b in blockers:
                report += f"- {b}\n"
                
        report += "\nWARNINGS:\n"
        warnings = []
        warnings.extend(env_res.get('warnings', []))
        warnings.extend(docker_res.get('warnings', []))
        
        if not warnings:
            report += "None\n"
        else:
            for w in warnings:
                report += f"- {w}\n"
                
        report += "\nNEXT ACTION:\n"
        if blockers:
            report += "Resolve blockers before deployment.\n"
        else:
            report += "Awaiting human approval to deploy.\n"
            
        return report
