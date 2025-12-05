import sqlite3
import os

# Railway: persistência apenas dentro de /data
DB_PATH = "/data/reminders.db"

def connect():
    # Garante que a pasta /data existe
    os.makedirs("/data", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                remind_at TEXT
            )
        """)

def save_reminder(user_id, text, remind_at):
    with connect() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO reminders (user_id, text, remind_at) VALUES (?, ?, ?)",
            (user_id, text, remind_at)
        )
        con.commit()
        return cur.lastrowid

def list_reminders(user_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute(
            "SELECT id, text, remind_at FROM reminders WHERE user_id = ?",
            (user_id,)
        )
        return cur.fetchall()

def delete_reminder(reminder_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        con.commit()
        return cur.rowcount > 0
