import sqlite3
import sys
import os

db_path = os.path.join(os.path.dirname(__file__), "sqlite_app.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

try:
    c.execute("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'member'")
    print("Added role column to users.")
except Exception as e:
    print("Column might already exist:", e)

c.execute("UPDATE users SET role = 'admin'")
conn.commit()
print("Updated all users to admin.")
conn.close()
