
from db import get_db_connection, init_db

init_db()

conn = get_db_connection()

tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("Database connected successfully!")
print("Tables in database:")

for table in tables:
    print("-", table["name"])

conn.close()

