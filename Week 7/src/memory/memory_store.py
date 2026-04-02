import json
import os
from datetime import datetime
MEMORY_FILE = "CHAT-LOGS.json"
MAX_MEMORY = 5

class MemoryStore:
    def __init__(self):
        self.history = [] #in-memory list
        self._load()     #existing logs if any

    def add(self,role,content,endpoint="/ask"):
        entry = {
            "role" : role,
            "content" : content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "endpoint" : endpoint
        }
        self.history.append(entry)
        #keep only last MAX_MEMORY * 2 entries (for user and assistant pairs)
        if len(self.history) > MAX_MEMORY*2:
            self.history = self.history[-(MAX_MEMORY*2):]

        self._save()

    def get_context(self):
        if not self.history:
            return "No previous conversations."
        
        lines=[]
        for entry in self.history:
            role = entry["role"].upper()
            lines.append(f"{role}:{entry["content"][:200]}")

        return "\n".join(lines)
    
    def get_last_answer(self):
        for entry in reversed(self.history):
            if entry["role"] == "assistant":
                return entry["content"]
        return ""
    
    def clear(self):
        self.history=[]
        self._save()
        print("memory cleared")

    def _save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.history,f,indent=2)

    def _load(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE,"r") as f:
                    self.history = json.load(f)
                self.history = self.history[-(MAX_MEMORY * 2):]
            except Exception:
                self.history=[]

memory=MemoryStore()