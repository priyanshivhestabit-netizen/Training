# Fixed version for Day 5
from collections import deque


class SessionMemory:
    def __init__(self, limit=10):
        self.memory = deque(maxlen=limit)

    def add(self, role: str, message: str):
        self.memory.append({"role": role, "content": message})

    def get_all(self):
        return list(self.memory)

    def format_for_prompt(self):
        return "\n".join([f"{m['role'].upper()}: {m['content']}" for m in self.memory])