from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from db.models import User
from db.session import SessionLocal

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        ["📋 Профиль", "🧠 Память"],
        ["🌍 Изменить город", "🗑 Сброс памяти"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я AI-ассистент 🤖\nВыбери действие:", reply_markup=main_menu)

async def handle_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    user_id = update.effective_user.id
    db = SessionLocal()
    user = db.query(User).filter_by(telegram_id=user_id).first()

    if choice == "📋 Профиль":
        city = user.city if user.city else "не указан"
        await update.message.reply_text(f"👤 Имя: {user.name}\n🌍 Город: {city}")

    elif choice == "🧠 Память":
        memory = user.memory[-500:] if user.memory else "Память пуста"
        await update.message.reply_text(f"🧠 Память:\n{memory}")

    elif choice == "🌍 Изменить город":
        await update.message.reply_text("Введите новый город:")
        context.user_data["change_city"] = True

    elif choice == "🗑 Сброс памяти":
        user.memory = ""
        db.commit()
        await update.message.reply_text("🗑 Память очищена.")

    else:
        await update.message.reply_text("Неизвестная команда.")
