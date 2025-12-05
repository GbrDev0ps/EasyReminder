import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect("reminders.db")

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
        cur.execute("SELECT * FROM reminders WHERE user_id = ?", (user_id,))
        return cur.fetchall()

def delete_reminder(reminder_id):
    with connect() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
        con.commit()
        return cur.rowcount > 0
