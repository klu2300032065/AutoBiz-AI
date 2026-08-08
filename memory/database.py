import json
import os

class Database:
    def __init__(self, db_path="memory/db.json"):
        self.db_path = db_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump({}, f)

    def save_research(self, topic: str, data: dict):
        with open(self.db_path, "r") as f:
            db = json.load(f)
        db[topic] = data
        with open(self.db_path, "w") as f:
            json.dump(db, f, indent=4)

    def get_research(self, topic: str):
        with open(self.db_path, "r") as f:
            db = json.load(f)
        return db.get(topic)
