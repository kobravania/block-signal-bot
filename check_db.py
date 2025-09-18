import sqlite3
from datetime import datetime

DB_PATH = "db.sqlite"

def show_users():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT tg_id, is_pro, until FROM users")
    users = cur.fetchall()
    conn.close()

    if not users:
        print("📭 В базе пока нет пользователей.")
        return

    print("📋 Пользователи в базе:\n")
    for tg_id, is_pro, until in users:
        status = "✅ PRO" if is_pro else "❌ FREE"
        if is_pro and until:
            try:
                until_dt = datetime.fromisoformat(until)
                status += f" (до {until_dt.strftime('%Y-%m-%d %H:%M')})"
            except Exception:
                pass
        print(f"👤 {tg_id} | {status}")

if __name__ == "__main__":
    show_users()
