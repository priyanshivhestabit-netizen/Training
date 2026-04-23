import csv
import logging

logger = logging.getLogger(__name__)


class FileAgent:
    def read_csv(self, filepath):
        try:
            logger.info(f"Reading CSV: {filepath}")
            rows = []
            with open(filepath, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    rows.append(row)
            logger.info(f"Loaded {len(rows)} rows")
            return rows

        except Exception as e:
            logger.error(f"CSV read error: {e}")
            return []

    def read_txt(self, filepath):
        try:
            logger.info(f"Reading TXT: {filepath}")
            with open(filepath, "r") as f:
                return f.read()
        except Exception as e:
            logger.error(f"TXT read error: {e}")
            return ""

    def write_txt(self, filepath, content):
        try:
            logger.info(f"Writing TXT: {filepath}")
            with open(filepath, "w") as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"TXT write error: {e}")
            return False

    def write_csv(self, filepath, rows: list[dict]):
        try:
            logger.info(f"Writing CSV: {filepath}")
            if not rows:
                return False
            with open(filepath, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            return True
        except Exception as e:
            logger.error(f"CSV write error: {e}")
            return False