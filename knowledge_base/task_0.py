# PHOENIX CORE - DNA MODULE (task_0)
import json, os
class CoreMemory:
    def __init__(self, file="core_memory.json"):
        self.file = file
        self.data = self._load()
    def _load(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f: return json.load(f)
        return {"capabilities": ["foundation_v0"]}
    def save(self):
        with open(self.file, 'w') as f: json.dump(self.data, f)
if __name__ == "__main__":
    mem = CoreMemory(); mem.save()
    print("Core Initialized.")
