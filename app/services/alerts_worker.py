import asyncio
from aiogram import Bot
from app.services.alerts import get_alerts, delete_alert
from app.services.prices import get_price

async def check_alerts(bot: Bot):
    """Фоновая задача для проверки алертов"""
    while True:
        alerts = get_alerts()
        for alert_id, user_id, symbol, target_price in alerts:
            current_price = await get_price(symbol, "usd")
            if current_price is None:
                continue

            if current_price >= target_price:
                try:
                    await bot.send_message(
                        user_id,
                        f"🔔 {symbol.upper()} достиг {current_price} USD (цель {target_price}) 🚀"
                    )
                except Exception as e:
                    print(f"[alerts_worker] Ошибка отправки пользователю {user_id}: {e}")
                delete_alert(alert_id)

        await asyncio.sleep(30)  # проверяем каждые 30 секунд
