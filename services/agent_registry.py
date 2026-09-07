from agents.research_agent import ResearchAgent
from agents.builder_agent import BuilderAgent
from agents.qa_agent import QAAgent
from agents.deployment_agent import DeploymentAgent
from agents.marketing_sales_analytics_agent import MarketingSalesAnalyticsAgent
from models.task import Task
from models.task_result import TaskResult

class AgentRegistry:
    def __init__(self):
        self.agents = {
            "RESEARCH": ResearchAgent(),
            "BUILDER": BuilderAgent(),
            "QA": QAAgent(),
            "DEPLOYMENT": DeploymentAgent(),
            "MARKETING_SALES_ANALYTICS": MarketingSalesAnalyticsAgent()
        }

    def execute_task(self, task: Task) -> dict:
        agent = None
        if task.type == "RESEARCH_PRODUCT":
            agent = self.agents["RESEARCH"]
        elif task.type in ["BUILD_PRODUCT", "BUILD_PRODUCT"]:
            agent = self.agents["BUILDER"]
        elif task.type == "RUN_QA":
            agent = self.agents["QA"]
        elif task.type == "PREPARE_DEPLOYMENT":
            agent = self.agents["DEPLOYMENT"]
        elif task.type in ["CREATE_MARKETING", "ANALYZE_PERFORMANCE"]:
            agent = self.agents["MARKETING_SALES_ANALYTICS"]
        else:
            return {"status": "error", "agent": "Registry", "task_id": task.task_id, "result": None, "errors": f"Unknown task type: {task.type}"}
            
        try:
            return agent.run(task)
        except Exception as e:
            return {"status": "error", "agent": agent.__class__.__name__, "task_id": task.task_id, "result": None, "errors": str(e)}

    def list_agents(self) -> list:
        return [agent.__class__.__name__ for agent in self.agents.values()]
