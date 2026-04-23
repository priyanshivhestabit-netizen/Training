import sqlite3
import logging

logger = logging.getLogger(__name__)


class LongTermMemory:
    def __init__(self, db_path):
        self.db_path = db_path

    def setup(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
            logger.info("Long-term memory DB ready")
        except Exception as e:
            logger.error(f"DB setup error: {e}")

    def store(self, text: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("INSERT INTO memories(text) VALUES (?)", (text,))
            conn.commit()
            conn.close()
            logger.info(f"Stored to long-term memory: {text[:60]}")
        except Exception as e:
            logger.error(f"Store memory error: {e}")

    def fetch_all(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("SELECT text FROM memories ORDER BY created_at DESC")
            rows = cur.fetchall()
            conn.close()
            return [r[0] for r in rows]
        except Exception as e:
            logger.error(f"Fetch memory error: {e}")
            return []