from memory.business_memory import BusinessMemory
from models.task import Task

class TaskManager:
    def __init__(self):
        self.memory = BusinessMemory()

    def create_task(self, type_str: str, description: str, dependencies: list[int] = None) -> int:
        if dependencies is None:
            dependencies = []
        task = Task(task_id=0, type=type_str, description=description, dependencies=dependencies)
        return self.memory.create_task(task)

    def can_run(self, task_id: int) -> bool:
        task = self.memory.get_task(task_id)
        if not task or task.status != "PENDING":
            return False
            
        for dep_id in task.dependencies:
            dep_task = self.memory.get_task(dep_id)
            if not dep_task or dep_task.status != "COMPLETED":
                return False
        return True

    def update_task_status(self, task_id: int, status: str, result: str = None, assigned_agent: str = None):
        task = self.memory.get_task(task_id)
        if task:
            task.status = status
            if result is not None:
                task.result = result
            if assigned_agent is not None:
                task.assigned_agent = assigned_agent
            self.memory.update_task(task)

    def get_next_runnable_task(self) -> Task:
        tasks = self.memory.get_all_tasks()
        for t in tasks:
            if self.can_run(t.task_id):
                return t
        return None
