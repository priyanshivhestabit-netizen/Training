import sqlite3
import logging

logger = logging.getLogger(__name__)


class DBAgent:
    def __init__(self, db_path):
        self.db_path = db_path

    def setup(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_sales INTEGER,
                    average_sales REAL,
                    best_month TEXT,
                    max_sales INTEGER,
                    total_customers INTEGER,
                    llm_insights TEXT
                )
            """)
            conn.commit()
            conn.close()
            logger.info("DB setup complete")
        except Exception as e:
            logger.error(f"DB setup error: {e}")

    def insert_report(self, insights: dict, llm_insights: str = ""):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO reports(total_sales, average_sales, best_month, max_sales, total_customers, llm_insights)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                insights.get("total_sales"),
                insights.get("average_sales"),
                insights.get("best_month"),
                insights.get("max_sales"),
                insights.get("total_customers"),
                llm_insights
            ))
            conn.commit()
            conn.close()
            logger.info("Report inserted into DB")
        except Exception as e:
            logger.error(f"DB insert error: {e}")

    def query(self, sql: str):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            conn.close()
            return rows
        except Exception as e:
            logger.error(f"DB query error: {e}")
            return []