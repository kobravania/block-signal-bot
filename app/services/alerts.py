import sqlite3
from typing import List, Tuple

DB_PATH = "database.db"

def create_alert(user_id: int, symbol: str, target_price: float):
    """Создать новый алерт"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            symbol TEXT NOT NULL,
            target_price REAL NOT NULL
        )
    """)
    cur.execute(
        "INSERT INTO alerts (user_id, symbol, target_price) VALUES (?, ?, ?)",
        (user_id, symbol.lower(), target_price)
    )
    conn.commit()
    conn.close()

def get_alerts() -> List[Tuple[int, int, str, float]]:
    """Получить все алерты"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, symbol, target_price FROM alerts")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_alert(alert_id: int):
    """Удалить алерт после срабатывания"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM alerts WHERE id = ?", (alert_id,))
    conn.commit()
    conn.close()
