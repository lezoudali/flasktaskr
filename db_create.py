import sqlite3
from config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as conn:

    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE tasks (
                   task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   due_date TEXT NOT NULL,
                   priority INTEGER NOT NULL,
                   status INTEGER NOT NULL)""")
