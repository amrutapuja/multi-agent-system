import sqlite3
from datetime import datetime
import os

DB_PATH = "memory/agent_memory.db"

def init_memory():
    os.makedirs("memory", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            stage TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_to_memory(record: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO memory_log (timestamp, stage, content)
        VALUES (?, ?, ?)
    ''', (
        datetime.utcnow().isoformat(),
        record.get("stage", "unknown"),
        str(record)
    ))
    conn.commit()
    conn.close()

def get_memory_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM memory_log ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
