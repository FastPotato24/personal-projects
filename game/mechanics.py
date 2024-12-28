import json
import os

class Entity:
    def __init__(self, id, **kwargs):
        self.id = id
        self.data = {}
        self.process(self.id)
        self.data.update(kwargs)

        self.name = self.data["meta"].get("name", "Unknown")
        self.description = self.data["meta"].get("description", "No description available.")
        
        self.health = self.data["components"]["stats"].get("health", 0)
        self.max_health = self.data["components"]["stats"].get("max_health", 0)

    def process(self, id):
        if ":" in id:
            self.module, self.id = id.split(":")
        else:
            self.module = "main"
            self.id = id
        file_path = os.path.join(os.path.dirname(__file__), f"modules/{self.module}/entities/{self.id}.json")
        with open(file_path) as f:
            self.data = json.load(f)