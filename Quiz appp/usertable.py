import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# ❌ पुराना table delete
cur.execute("DROP TABLE IF EXISTS users")

# ✅ नया सही table
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    mobile TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()
conn.close()

print("✅ Table recreated with mobile column")