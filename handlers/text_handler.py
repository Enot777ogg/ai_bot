from telegram import Update
from telegram.ext import ContextTypes
from db.session import SessionLocal
from db.models import User
from utils.openai_client import ask_gpt
from datetime import datetime

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    message = update.message.text
    db = SessionLocal()

    user = db.query(User).filter_by(telegram_id=user_id).first()
    if not user:
        user = User(telegram_id=user_id, name=user_name, memory="")
        db.add(user)
        db.commit()

    # Обработка смены города
    if context.user_data.get("change_city"):
        user.city = message
        db.commit()
        context.user_data["change_city"] = False
        await update.message.reply_text(f"🌍 Город обновлён на: {message}")
        return

    # Продолжение диалога с GPT
    user.memory = (user.memory or "") + f"\nUser: {message}"
    user.memory = user.memory[-1000:]
    user.last_active = datetime.utcnow()
    db.commit()

    reply = ask_gpt(message, user.memory)
    await update.message.reply_text(reply)
