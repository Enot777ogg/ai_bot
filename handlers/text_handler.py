from telegram import Update
from telegram.ext import ContextTypes
from utils.openai_client import ask_gpt
from db.models import User
from db.session import SessionLocal
from datetime import datetime

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    user_message = update.message.text

    db = SessionLocal()

    user = db.query(User).filter_by(telegram_id=user_id).first()

    if not user:
        user = User(telegram_id=user_id, name=user_name, memory="")
        db.add(user)
        db.commit()

        await update.message.reply_text(f"Привет, {user_name}! Я запомню тебя.")
    else:
        await update.message.reply_text(f"Снова привет, {user.name}!")

    # Добавим сообщение к памяти (упрощённо)
    new_memory = (user.memory or "") + f"\nUser: {user_message}"
    user.memory = new_memory[-1000:]  # ограничим длину памяти
    user.last_active = datetime.utcnow()
    db.commit()

    reply = ask_gpt(user_message, user.memory)
    await update.message.reply_text(reply)
