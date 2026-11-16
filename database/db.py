
import sqlite3
from pathlib import Path

# Find the database file relative to this Python file
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "products.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    schema_path = BASE_DIR / "schema.sql"

    with get_db_connection() as conn:
        schema = schema_path.read_text()
        conn.executescript(schema)
