import sqlite3
from app.database import init_db, DB_NAME

init_db()

conn = sqlite3.connect(DB_NAME)

cursor = conn.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""")

tables = cursor.fetchall()

print("Tablas creadas:")
for table in tables:
    print(table[0])

conn.close()