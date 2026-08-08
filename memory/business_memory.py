import sqlite3
import os
import json
from datetime import datetime
from models.task import Task
from models.approval import Approval
from models.business_state import BusinessState

DB_PATH = os.path.join(os.getcwd(), "ceo_memory.db")

class BusinessMemory:
    def __init__(self):
        self._init_db()
        
    def _get_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_db()
        c = conn.cursor()
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS business_state (
                id INTEGER PRIMARY KEY,
                state_data TEXT
            )
        """)
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                description TEXT,
                status TEXT,
                priority INTEGER,
                created_at TEXT,
                updated_at TEXT,
                dependencies TEXT,
                assigned_agent TEXT,
                result TEXT
            )
        """)
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                approval_id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                description TEXT,
                risk_level TEXT,
                estimated_cost REAL,
                status TEXT,
                requested_at TEXT
            )
        """)
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS objective (
                id INTEGER PRIMARY KEY,
                objective_text TEXT
            )
        """)
        
        conn.commit()
        conn.close()

    def get_objective(self) -> str:
        conn = self._get_db()
        c = conn.cursor()
        c.execute("SELECT objective_text FROM objective WHERE id=1")
        row = c.fetchone()
        conn.close()
        return row['objective_text'] if row else None

    def set_objective(self, obj: str):
        conn = self._get_db()
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO objective (id, objective_text) VALUES (1, ?)", (obj,))
        conn.commit()
        conn.close()

    def get_business_state(self) -> BusinessState:
        conn = self._get_db()
        c = conn.cursor()
        c.execute("SELECT state_data FROM business_state WHERE id=1")
        row = c.fetchone()
        conn.close()
        if row:
            data = json.loads(row['state_data'])
            return BusinessState(**data)
        return BusinessState()

    def update_business_state(self, state: BusinessState):
        conn = self._get_db()
        c = conn.cursor()
        data = json.dumps(state.__dict__)
        c.execute("INSERT OR REPLACE INTO business_state (id, state_data) VALUES (1, ?)", (data,))
        conn.commit()
        conn.close()

    def create_task(self, task: Task) -> int:
        conn = self._get_db()
        c = conn.cursor()
        deps = json.dumps(task.dependencies)
        c.execute("""
            INSERT INTO tasks (type, description, status, priority, created_at, updated_at, dependencies, assigned_agent, result)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (task.type, task.description, task.status, task.priority, task.created_at, task.updated_at, deps, task.assigned_agent, task.result))
        task_id = c.lastrowid
        conn.commit()
        conn.close()
        return task_id

    def update_task(self, task: Task):
        conn = self._get_db()
        c = conn.cursor()
        deps = json.dumps(task.dependencies)
        c.execute("""
            UPDATE tasks SET status=?, updated_at=?, assigned_agent=?, result=? WHERE task_id=?
        """, (task.status, datetime.now().isoformat(), task.assigned_agent, task.result, task.task_id))
        conn.commit()
        conn.close()

    def get_task(self, task_id: int) -> Task:
        conn = self._get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,))
        row = c.fetchone()
        conn.close()
        if row:
            deps = json.loads(row['dependencies'])
            return Task(
                task_id=row['task_id'],
                type=row['type'],
                description=row['description'],
                status=row['status'],
                priority=row['priority'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                dependencies=deps,
                assigned_agent=row['assigned_agent'],
                result=row['result']
            )
        return None

    def get_all_tasks(self) -> list[Task]:
        conn = self._get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM tasks ORDER BY created_at ASC")
        rows = c.fetchall()
        conn.close()
        tasks = []
        for row in rows:
            deps = json.loads(row['dependencies'])
            tasks.append(Task(
                task_id=row['task_id'],
                type=row['type'],
                description=row['description'],
                status=row['status'],
                priority=row['priority'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                dependencies=deps,
                assigned_agent=row['assigned_agent'],
                result=row['result']
            ))
        return tasks

    def create_approval(self, approval: Approval) -> int:
        conn = self._get_db()
        c = conn.cursor()
        c.execute("""
            INSERT INTO approvals (action, description, risk_level, estimated_cost, status, requested_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (approval.action, approval.description, approval.risk_level, approval.estimated_cost, approval.status, approval.requested_at))
        app_id = c.lastrowid
        conn.commit()
        conn.close()
        return app_id

    def update_approval(self, approval_id: int, status: str):
        conn = self._get_db()
        c = conn.cursor()
        c.execute("UPDATE approvals SET status=? WHERE approval_id=?", (status, approval_id))
        conn.commit()
        conn.close()

    def get_approval(self, approval_id: int) -> Approval:
        conn = self._get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM approvals WHERE approval_id=?", (approval_id,))
        row = c.fetchone()
        conn.close()
        if row:
            return Approval(
                approval_id=row['approval_id'],
                action=row['action'],
                description=row['description'],
                risk_level=row['risk_level'],
                estimated_cost=row['estimated_cost'],
                status=row['status'],
                requested_at=row['requested_at']
            )
        return None

    def get_pending_approvals(self) -> list[Approval]:
        conn = self._get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM approvals WHERE status='PENDING'")
        rows = c.fetchall()
        conn.close()
        apps = []
        for row in rows:
            apps.append(Approval(
                approval_id=row['approval_id'],
                action=row['action'],
                description=row['description'],
                risk_level=row['risk_level'],
                estimated_cost=row['estimated_cost'],
                status=row['status'],
                requested_at=row['requested_at']
            ))
        return apps
