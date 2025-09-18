import asyncio
import threading
import uvicorn

from aiogram import Bot
from app.config import TELEGRAM_TOKEN
from app.bot import dp
from app.models import init_db
from app.webhook import app
from app.services.alerts_worker import check_alerts  # фоновый воркер

bot = Bot(token=TELEGRAM_TOKEN)

async def main():
    """Запуск Telegram-бота и фоновых задач"""
    init_db()  # ⚡ создаём все таблицы (users + portfolio)
    print("🚀 Bot started")

    # фоновая проверка алертов
    asyncio.create_task(check_alerts(bot))

    # запуск Telegram бота
    await dp.start_polling(bot)

def run_webhook():
    """Запуск FastAPI вебхука в отдельном потоке"""
    print("🌐 Webhook server started on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    # поднимаем вебхук в отдельном потоке
    threading.Thread(target=run_webhook, daemon=True).start()

    # запускаем бота (основной цикл)
    asyncio.run(main())
