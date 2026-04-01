import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS categories(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS quizzes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
category_id INTEGER,
quiz_name TEXT
)
""")

conn.commit()
conn.close()

print("Tables created")