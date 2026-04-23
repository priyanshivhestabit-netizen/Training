import sqlite3

DB_PATH = "src/data/database/enterprise.db"


def get_schema(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema_text = ""

    for (table_name,) in tables:
        schema_text += f"Table: {table_name}\n"

        # Get columns for this table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        for col in columns:
            col_name = col[1]
            col_type = col[2]
            schema_text += f"  - {col_name} ({col_type})\n"

        schema_text += "\n"

    conn.close()
    return schema_text


def get_sample_rows(db_path=DB_PATH, n=2):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    samples = ""
    for (table_name,) in tables:
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {n};")
        rows = cursor.fetchall()
        samples += f"Sample from {table_name}: {rows}\n"

    conn.close()
    return samples


if __name__ == "__main__":
    print("=== SCHEMA ===")
    print(get_schema())
    print("=== SAMPLES ===")
    print(get_sample_rows())