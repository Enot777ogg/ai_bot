from telegram import Update
from telegram.ext import ContextTypes
from db.session import SessionLocal
from db.models import User
from utils.openai_client import ask_gpt
from utils.level_system import calculate_level
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
        context.user_data["change_city"] = False
        db.commit()
        await update.message.reply_text(f"🌍 Город обновлён на: {message}")
        return

    # Обработка аватара
    if context.user_data.get("change_avatar"):
        if message.startswith("http"):
            user.avatar_url = message
            db.commit()
            context.user_data["change_avatar"] = False
            await update.message.reply_text("✅ Аватар установлен!")
        else:
            await update.message.reply_text("❌ Это не ссылка. Попробуй ещё.")
        return

    # Память и XP
    user.memory = (user.memory or "") + f"\nUser: {message}"
    user.memory = user.memory[-1000:]
    user.last_active = datetime.utcnow()
    user.xp += 100
    new_level = calculate_level(user.xp)
    if new_level > user.level:
        user.level = new_level
        await update.message.reply_text(f"🎉 Поздравляю! Ты достиг {new_level} уровня!")
    db.commit()

    reply = ask_gpt(message, user.memory)
    await update.message.reply_text(reply)
