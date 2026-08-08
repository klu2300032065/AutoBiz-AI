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

    def execute_task(self, task: Task, input_data: str = None) -> TaskResult:
        agent = None
        if task.type == "RESEARCH_PRODUCT":
            agent = self.agents["RESEARCH"]
            # ResearchAgent takes goal as string
            try:
                res = agent.run(input_data)
                return TaskResult(status="success", result=res)
            except Exception as e:
                return TaskResult(status="error", result=None, errors=str(e))
                
        elif task.type == "BUILD_PRODUCT":
            agent = self.agents["BUILDER"]
            # BuilderAgent takes spec string
            try:
                res = agent.run(input_data)
                return TaskResult(status="success", result=res)
            except Exception as e:
                return TaskResult(status="error", result=None, errors=str(e))
                
        elif task.type == "RUN_QA":
            agent = self.agents["QA"]
            # QAAgent takes project_name
            try:
                res = agent.run(input_data)
                is_success = "PASS" in res
                return TaskResult(status="success" if is_success else "error", result=res, errors=res if not is_success else None)
            except Exception as e:
                return TaskResult(status="error", result=None, errors=str(e))
                
        elif task.type == "PREPARE_DEPLOYMENT":
            agent = self.agents["DEPLOYMENT"]
            try:
                res = agent.run(input_data)
                return TaskResult(status="success", result=res)
            except Exception as e:
                return TaskResult(status="error", result=None, errors=str(e))
                
        elif task.type == "CREATE_MARKETING" or task.type == "ANALYZE_PERFORMANCE":
            agent = self.agents["MARKETING_SALES_ANALYTICS"]
            try:
                res = agent.run(input_data)
                return TaskResult(status="success", result=res)
            except Exception as e:
                return TaskResult(status="error", result=None, errors=str(e))
        else:
            return TaskResult(status="error", result=None, errors=f"Unknown task type: {task.type}")
