from aiogram import Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

from config import SUBSCRIPTION_PRICE, ADMIN_ID
from app.services.payments import create_charge
from app.services.alerts import create_alert
from app.services.calculator import position_size
from app.models import add_user, check_pro, get_all_users, set_pro

dp = Dispatcher()

# --- Главное меню ---
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💳 Купить PRO")],
        [KeyboardButton(text="📊 Статус")],
        [KeyboardButton(text="📩 Получить сигнал")],
        [KeyboardButton(text="📈 Калькулятор позиции")],
        [KeyboardButton(text="🔔 Создать алерт")],
    ],
    resize_keyboard=True
)


# --- Команда /start ---
@dp.message(Command("start"))
async def start(message: types.Message):
    add_user(message.from_user.id)
    await message.answer(
        "👋 Привет! Добро пожаловать в бота.\n\n"
        "Выбери действие в меню 👇",
        reply_markup=menu
    )


# --- Купить подписку ---
@dp.message(F.text == "💳 Купить PRO")
@dp.message(Command("buy"))
async def buy(message: types.Message):
    charge = await create_charge(
        "PRO Subscription",
        "Доступ к PRO на 30 дней",
        SUBSCRIPTION_PRICE
    )
    link = charge["data"]["hosted_url"]
    await message.answer(f"💳 Оплата подписки (10$ USDT TRC20): {link}")


# --- Проверить статус ---
@dp.message(F.text == "📊 Статус")
@dp.message(Command("status"))
async def status(message: types.Message):
    if check_pro(message.from_user.id):
        await message.answer("✅ У тебя активен PRO-доступ.")
    else:
        await message.answer("❌ У тебя нет активной подписки. Используй '💳 Купить PRO'.")


# --- Обновить меню ---
@dp.message(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer(
        "📍 Главное меню обновлено.\n\n"
        "Теперь выбери нужное действие 👇",
        reply_markup=menu
    )


# --- Получить сигнал (только PRO) ---
@dp.message(F.text == "📩 Получить сигнал")
@dp.message(Command("signal"))
async def signal(message: types.Message):
    if check_pro(message.from_user.id):
        await message.answer("📈 Сигнал дня: Покупай BTC при пробое $65,000 🚀")
    else:
        await message.answer("❌ Эта команда доступна только с PRO подпиской.")


# --- Калькулятор позиции ---
@dp.message(F.text == "📈 Калькулятор позиции")
@dp.message(Command("calc"))
async def calc(message: types.Message):
    try:
        # пример: /calc 1000 2 50
        _, deposit, risk_percent, stop_loss = message.text.split()
        deposit, risk_percent, stop_loss = float(deposit), float(risk_percent), float(stop_loss)
        size = position_size(deposit, risk_percent, stop_loss)
        await message.answer(f"📊 Размер позиции: {size:.2f} USDT")
    except Exception:
        await message.answer("❌ Использование: /calc <депозит> <риск %> <стоп>\nПример: /calc 1000 2 50")


# --- Создание алерта ---
@dp.message(F.text == "🔔 Создать алерт")
@dp.message(Command("alert"))
async def alert_cmd(message: types.Message):
    try:
        _, symbol, price = message.text.split()
        price = float(price)
        create_alert(message.from_user.id, symbol, price)
        await message.answer(f"🔔 Алерт создан: {symbol.upper()} при {price} USD")
    except Exception:
        await message.answer("❌ Использование: /alert <symbol> <price>\nПример: /alert btc 65000")


# --- Админ: список пользователей ---
@dp.message(Command("users"))
async def list_users(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ У тебя нет доступа к этой команде.")

    users = get_all_users()
    if not users:
        await message.answer("📭 В базе пока нет пользователей.")
        return

    text = "📋 Список пользователей:\n\n"
    for user_id, is_pro in users:
        status = "✅ PRO" if is_pro else "❌ FREE"
        text += f"👤 user_id: {user_id} | {status}\n"

    await message.answer(text)


# --- Админ: выдать PRO ---
@dp.message(Command("give_pro"))
async def give_pro(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ У тебя нет доступа.")

    try:
        _, user_id = message.text.split()
        user_id = int(user_id)
    except:
        return await message.answer("❌ Использование: /give_pro <user_id>")

    set_pro(user_id, True)  # даём PRO
    await message.answer(f"✅ Пользователю {user_id} выдан PRO-доступ")
