# app/services/portfolio.py
import sqlite3
from datetime import datetime
from app.services.prices import get_price

DB_PATH = "db.sqlite"


def init_portfolio():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER,
        symbol TEXT,
        amount REAL,
        buy_price REAL,
        added_at TEXT
    )
    """)
    conn.commit()
    conn.close()


def add_asset(tg_id: int, symbol: str, amount: float, buy_price: float):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO portfolio (tg_id, symbol, amount, buy_price, added_at)
        VALUES (?, ?, ?, ?, ?)
    """, (tg_id, symbol.lower(), amount, buy_price, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()


def remove_asset(tg_id: int, symbol: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM portfolio WHERE tg_id=? AND symbol=?", (tg_id, symbol.lower()))
    conn.commit()
    conn.close()


def get_portfolio(tg_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT symbol, amount, buy_price FROM portfolio WHERE tg_id=?", (tg_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


async def portfolio_summary(tg_id: int):
    rows = get_portfolio(tg_id)
    if not rows:
        return "📭 У тебя нет активов в портфеле."

    text = "💼 Твой портфель:\n\n"
    total_invested = 0
    total_value = 0

    for symbol, amount, buy_price in rows:
        try:
            price = await get_price(symbol, "usd")
        except Exception:
            price = None

        invested = amount * buy_price
        total_invested += invested

        if price:
            current_value = amount * price
            total_value += current_value
            pnl = current_value - invested
            pnl_pct = (pnl / invested) * 100 if invested > 0 else 0
            text += (f"• {symbol.upper()} — {amount} шт.\n"
                     f"  Покупка: ${buy_price:.2f}\n"
                     f"  Сейчас: ${price:.2f}\n"
                     f"  PnL: {pnl:+.2f}$ ({pnl_pct:+.2f}%)\n\n")
        else:
            text += f"• {symbol.upper()} — {amount} шт. (❌ цена недоступна)\n\n"

    text += f"📊 Инвестировано: ${total_invested:.2f}\n"
    text += f"💰 Текущая стоимость: ${total_value:.2f}\n"
    pnl_total = total_value - total_invested
    text += f"🔎 Общий PnL: {pnl_total:+.2f}$"

    return text
