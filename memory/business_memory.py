import sqlite3
import os
import json
from typing import Optional
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
                input_data TEXT,
                result TEXT,
                cycle_id INTEGER DEFAULT 1
            )
        """)
        try:
            c.execute("ALTER TABLE tasks ADD COLUMN cycle_id INTEGER DEFAULT 1")
        except Exception:
            pass
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                approval_id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT,
                description TEXT,
                risk_level TEXT,
                estimated_cost REAL,
                actual_cost REAL DEFAULT 0.0,
                demo_cost REAL DEFAULT 0.0,
                deployment_mode TEXT DEFAULT 'LOCAL/DEMO',
                status TEXT,
                requested_at TEXT,
                cycle_id INTEGER DEFAULT 1
            )
        """)
        try:
            c.execute("ALTER TABLE approvals ADD COLUMN cycle_id INTEGER DEFAULT 1")
        except Exception:
            pass
        try:
            c.execute("ALTER TABLE approvals ADD COLUMN actual_cost REAL DEFAULT 0.0")
        except Exception:
            pass
        try:
            c.execute("ALTER TABLE approvals ADD COLUMN demo_cost REAL DEFAULT 0.0")
        except Exception:
            pass
        try:
            c.execute("ALTER TABLE approvals ADD COLUMN deployment_mode TEXT DEFAULT 'LOCAL/DEMO'")
        except Exception:
            pass
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS objective (
                id INTEGER PRIMARY KEY,
                objective_text TEXT
            )
        """)
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS cycles (
                cycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT,
                stage TEXT,
                status TEXT,
                created_at TEXT,
                updated_at TEXT,
                revenue REAL DEFAULT 0.0,
                customers INTEGER DEFAULT 0
            )
        """)
        try:
            c.execute("ALTER TABLE cycles ADD COLUMN revenue REAL DEFAULT 0.0")
        except Exception:
            pass
        try:
            c.execute("ALTER TABLE cycles ADD COLUMN customers INTEGER DEFAULT 0")
        except Exception:
            pass
        
        # Ensure at least Cycle 1 exists
        c.execute("SELECT COUNT(*) as cnt FROM cycles")
        if c.fetchone()['cnt'] == 0:
            now = datetime.now().isoformat()
            c.execute("""
                INSERT INTO cycles (cycle_id, product, stage, status, created_at, updated_at, revenue, customers)
                VALUES (1, 'Student Expense Tracker', 'MARKETING_READY', 'LIVE', ?, ?, 0.0, 0)
            """, (now, now))
            
        conn.commit()
        conn.close()

    def get_active_cycle_id(self) -> int:
        conn = self._get_db()
        c = conn.cursor()
        c.execute("SELECT cycle_id FROM cycles WHERE status='ACTIVE' ORDER BY cycle_id DESC LIMIT 1")
        row = c.fetchone()
        conn.close()
        return row['cycle_id'] if row else 1

    def get_objective(self, cycle_id: Optional[int] = None) -> str:
        if cycle_id is None:
            cycle_id = self.get_active_cycle_id()
        conn = self._get_db()
        c = conn.cursor()
        c.execute("SELECT objective_text FROM objective WHERE id=?", (cycle_id,))
        row = c.fetchone()
        conn.close()
        return row['objective_text'] if row else None

    def set_objective(self, obj: str, cycle_id: Optional[int] = None):
        if cycle_id is None:
            cycle_id = self.get_active_cycle_id()
        conn = self._get_db()
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO objective (id, objective_text) VALUES (?, ?)", (cycle_id, obj))
        conn.commit()
        conn.close()

    def get_business_state(self, cycle_id: Optional[int] = None) -> BusinessState:
        if cycle_id is None:
            cycle_id = self.get_active_cycle_id()
        conn = self._get_db()
        c = conn.cursor()
        c.execute("SELECT state_data FROM business_state WHERE id=?", (cycle_id,))
        row = c.fetchone()
        conn.close()
        if row:
            data = json.loads(row['state_data'])
            return BusinessState(**data)
        return BusinessState(cycle_id=cycle_id, product=None, stage="NO_PRODUCT")

    def update_business_state(self, state: BusinessState):
        conn = self._get_db()
        c = conn.cursor()
        data = json.dumps(state.__dict__)
        c.execute("INSERT OR REPLACE INTO business_state (id, state_data) VALUES (?, ?)", (state.cycle_id, data))
        conn.commit()
        conn.close()
        try:
            self.sync_active_cycle(state)
        except Exception:
            pass

    def create_task(self, task: Task) -> int:
        conn = self._get_db()
        c = conn.cursor()
        deps = json.dumps(task.dependencies)
        cycle_id = getattr(task, 'cycle_id', 1) or self.get_active_cycle_id()
        c.execute("""
            INSERT INTO tasks (type, description, status, priority, created_at, updated_at, dependencies, assigned_agent, input_data, result, cycle_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (task.type, task.description, task.status, task.priority, task.created_at, task.updated_at, deps, task.assigned_agent, task.input_data, task.result, cycle_id))
        task_id = c.lastrowid
        conn.commit()
        conn.close()
        return task_id

    def update_task(self, task: Task):
        conn = self._get_db()
        c = conn.cursor()
        deps = json.dumps(task.dependencies)
        c.execute("""
            UPDATE tasks SET status=?, updated_at=?, assigned_agent=?, input_data=?, result=? WHERE task_id=?
        """, (task.status, datetime.now().isoformat(), task.assigned_agent, task.input_data, task.result, task.task_id))
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
            row_keys = row.keys()
            c_id = row['cycle_id'] if 'cycle_id' in row_keys else 1
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
                input_data=row['input_data'],
                result=row['result'],
                cycle_id=c_id
            )
        return None

    def get_all_tasks(self, cycle_id: Optional[int] = None) -> list[Task]:
        conn = self._get_db()
        c = conn.cursor()
        if cycle_id is not None:
            c.execute("SELECT * FROM tasks WHERE cycle_id=? ORDER BY created_at ASC", (cycle_id,))
        else:
            c.execute("SELECT * FROM tasks ORDER BY created_at ASC")
        rows = c.fetchall()
        conn.close()
        tasks = []
        for row in rows:
            deps = json.loads(row['dependencies'])
            row_keys = row.keys()
            c_id = row['cycle_id'] if 'cycle_id' in row_keys else 1
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
                input_data=row['input_data'],
                result=row['result'],
                cycle_id=c_id
            ))
        return tasks

    def create_approval(self, approval: Approval) -> int:
        conn = self._get_db()
        c = conn.cursor()
        cycle_id = getattr(approval, 'cycle_id', 1) or 1
        actual_cost = getattr(approval, 'actual_cost', 0.0) or 0.0
        demo_cost = getattr(approval, 'demo_cost', 0.0) or 0.0
        mode = getattr(approval, 'deployment_mode', 'LOCAL/DEMO') or 'LOCAL/DEMO'
        if mode == "LOCAL/DEMO":
            actual_cost = 0.0
        c.execute("""
            INSERT INTO approvals (action, description, risk_level, estimated_cost, actual_cost, demo_cost, deployment_mode, status, requested_at, cycle_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (approval.action, approval.description, approval.risk_level, approval.estimated_cost, actual_cost, demo_cost, mode, approval.status, approval.requested_at, cycle_id))
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
            keys = row.keys()
            mode = row['deployment_mode'] if 'deployment_mode' in keys and row['deployment_mode'] is not None else "LOCAL/DEMO"
            act_cost = row['actual_cost'] if 'actual_cost' in keys and row['actual_cost'] is not None else 0.0
            if mode == "LOCAL/DEMO":
                act_cost = 0.0
            return Approval(
                approval_id=row['approval_id'],
                action=row['action'],
                description=row['description'],
                risk_level=row['risk_level'],
                estimated_cost=row['estimated_cost'],
                actual_cost=act_cost,
                demo_cost=row['demo_cost'] if 'demo_cost' in keys and row['demo_cost'] is not None else 0.0,
                deployment_mode=mode,
                status=row['status'],
                requested_at=row['requested_at'],
                cycle_id=row['cycle_id'] if 'cycle_id' in keys else 1
            )
        return None

    def get_pending_approvals(self, cycle_id: Optional[int] = None) -> list[Approval]:
        conn = self._get_db()
        c = conn.cursor()
        if cycle_id is not None:
            c.execute("SELECT * FROM approvals WHERE status='PENDING' AND (cycle_id=? OR cycle_id IS NULL)", (cycle_id,))
        else:
            c.execute("SELECT * FROM approvals WHERE status='PENDING'")
        rows = c.fetchall()
        conn.close()
        apps = []
        for row in rows:
            keys = row.keys()
            mode = row['deployment_mode'] if 'deployment_mode' in keys and row['deployment_mode'] is not None else "LOCAL/DEMO"
            act_cost = row['actual_cost'] if 'actual_cost' in keys and row['actual_cost'] is not None else 0.0
            if mode == "LOCAL/DEMO":
                act_cost = 0.0
            apps.append(Approval(
                approval_id=row['approval_id'],
                action=row['action'],
                description=row['description'],
                risk_level=row['risk_level'],
                estimated_cost=row['estimated_cost'],
                actual_cost=act_cost,
                demo_cost=row['demo_cost'] if 'demo_cost' in keys and row['demo_cost'] is not None else 0.0,
                deployment_mode=mode,
                status=row['status'],
                requested_at=row['requested_at'],
                cycle_id=row['cycle_id'] if 'cycle_id' in keys else 1
            ))
        return apps

    def get_approvals_for_cycle(self, cycle_id: Optional[int] = None) -> list[Approval]:
        conn = self._get_db()
        c = conn.cursor()
        if cycle_id is not None:
            c.execute("SELECT * FROM approvals WHERE cycle_id=? ORDER BY approval_id ASC", (cycle_id,))
        else:
            c.execute("SELECT * FROM approvals ORDER BY approval_id ASC")
        rows = c.fetchall()
        conn.close()
        apps = []
        for row in rows:
            keys = row.keys()
            mode = row['deployment_mode'] if 'deployment_mode' in keys and row['deployment_mode'] is not None else "LOCAL/DEMO"
            act_cost = row['actual_cost'] if 'actual_cost' in keys and row['actual_cost'] is not None else 0.0
            if mode == "LOCAL/DEMO":
                act_cost = 0.0
            apps.append(Approval(
                approval_id=row['approval_id'],
                action=row['action'],
                description=row['description'],
                risk_level=row['risk_level'],
                estimated_cost=row['estimated_cost'],
                actual_cost=act_cost,
                demo_cost=row['demo_cost'] if 'demo_cost' in keys and row['demo_cost'] is not None else 0.0,
                deployment_mode=mode,
                status=row['status'],
                requested_at=row['requested_at'],
                cycle_id=row['cycle_id'] if 'cycle_id' in keys else 1
            ))
        return apps

    def get_all_cycles(self) -> list[dict]:
        conn = self._get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM cycles ORDER BY cycle_id ASC")
        rows = c.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def create_new_cycle(self) -> BusinessState:
        conn = self._get_db()
        c = conn.cursor()
        now = datetime.now().isoformat()
        
        # 1. Mark existing active cycles as COMPLETED/LIVE
        state = self.get_business_state()
        status_label = "LIVE" if state.deployment == "LIVE" or state.marketing == "LIVE" else "COMPLETED"
        c.execute("""
            UPDATE cycles SET status=?, stage=?, product=?, updated_at=? WHERE status='ACTIVE'
        """, (status_label, state.stage or "COMPLETED", state.product or "None", now))
        
        # 2. Insert new active cycle
        c.execute("""
            INSERT INTO cycles (product, stage, status, created_at, updated_at)
            VALUES (NULL, 'NO_PRODUCT', 'ACTIVE', ?, ?)
        """, (now, now))
        new_cycle_id = c.lastrowid
        conn.commit()
        conn.close()
        
        # 3. Create fresh active state for new cycle
        new_state = BusinessState(
            cycle_id=new_cycle_id,
            product=None,
            stage="NO_PRODUCT",
            qa=None,
            deployment=None,
            marketing=None,
            revenue=0.0,
            customers=0,
            build_status=None,
            research_results=None
        )
        self.update_business_state(new_state)
        self.set_objective("")
        return new_state

    def sync_active_cycle(self, state: BusinessState):
        conn = self._get_db()
        c = conn.cursor()
        now = datetime.now().isoformat()
        c.execute("""
            UPDATE cycles SET product=?, stage=?, revenue=?, customers=?, updated_at=? WHERE cycle_id=?
        """, (state.product, state.stage, getattr(state, 'revenue', 0.0) or 0.0, getattr(state, 'customers', 0) or 0, now, state.cycle_id))
        conn.commit()
        conn.close()
