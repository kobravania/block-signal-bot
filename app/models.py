import sqlite3
from datetime import datetime, timedelta

DB_PATH = "db.sqlite"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # --- Пользователи ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        tg_id INTEGER UNIQUE,
        is_pro INTEGER DEFAULT 0,
        until TEXT
    )
    """)

    # --- Портфель ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY,
        tg_id INTEGER,
        symbol TEXT,
        amount REAL,
        avg_price REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# ===========================
# Пользователи
# ===========================

def add_user(tg_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (tg_id) VALUES (?)", (tg_id,))
    conn.commit()
    conn.close()

def activate_pro(tg_id: int, days: int = 30):
    until = (datetime.utcnow() + timedelta(days=days)).isoformat()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_pro=1, until=? WHERE tg_id=?", (until, tg_id))
    conn.commit()
    conn.close()

def check_pro(tg_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT is_pro, until FROM users WHERE tg_id=?", (tg_id,))
    row = cur.fetchone()
    conn.close()
    if row and row[0] == 1:
        until = datetime.fromisoformat(row[1])
        return datetime.utcnow() < until
    return False

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT tg_id, is_pro FROM users")
    users = cur.fetchall()
    conn.close()
    return users

def set_pro(tg_id: int, is_pro: bool, days: int = 30):
    """Выдаёт или снимает PRO"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if is_pro:
        until = (datetime.utcnow() + timedelta(days=days)).isoformat()
        cur.execute("UPDATE users SET is_pro=1, until=? WHERE tg_id=?", (until, tg_id))
    else:
        cur.execute("UPDATE users SET is_pro=0, until=NULL WHERE tg_id=?", (tg_id,))
    conn.commit()
    conn.close()

# ===========================
# Портфель
# ===========================

def add_trade(tg_id: int, symbol: str, amount: float, avg_price: float):
    """Добавить сделку в портфель"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO portfolio (tg_id, symbol, amount, avg_price) VALUES (?, ?, ?, ?)",
        (tg_id, symbol.lower(), amount, avg_price)
    )
    conn.commit()
    conn.close()

def get_portfolio(tg_id: int):
    """Получить все позиции пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT symbol, amount, avg_price FROM portfolio WHERE tg_id=?", (tg_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def clear_portfolio(tg_id: int):
    """Очистить портфель пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM portfolio WHERE tg_id=?", (tg_id,))
    conn.commit()
    conn.close()
