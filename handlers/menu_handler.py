from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from db.models import User
from db.session import SessionLocal

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        ["📋 Профиль", "🧠 Память"],
        ["🌍 Изменить город", "🗑 Сброс памяти"],
        ["🖼 Установить аватар"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я AI-ассистент 🤖", reply_markup=main_menu)

async def handle_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    user_id = update.effective_user.id
    db = SessionLocal()
    user = db.query(User).filter_by(telegram_id=user_id).first()

    if not user:
        await update.message.reply_text("Пользователь не найден. Напиши что-нибудь для начала.")
        return

    if choice == "📋 Профиль":
        msg = (
            f"👤 Имя: {user.name}\n"
            f"🌍 Город: {user.city or 'не указан'}\n"
            f"⭐ Уровень: {user.level}\n"
            f"📈 Опыт: {user.xp} XP"
        )
        if user.avatar_url:
            await update.message.reply_photo(photo=user.avatar_url, caption=msg)
        else:
            await update.message.reply_text(msg)

    elif choice == "🧠 Память":
        memory = user.memory[-500:] if user.memory else "Память пуста"
        await update.message.reply_text(f"🧠\n{memory}")

    elif choice == "🌍 Изменить город":
        await update.message.reply_text("Введи новый город:")
        context.user_data["change_city"] = True

    elif choice == "🖼 Установить аватар":
        if user.level < 5:
            await update.message.reply_text("🔒 Доступно только с 5 уровня.")
        else:
            await update.message.reply_text("Отправь ссылку на изображение (jpg/png):")
            context.user_data["change_avatar"] = True

    elif choice == "🗑 Сброс памяти":
        user.memory = ""
        db.commit()
        await update.message.reply_text("🗑 Память очищена.")
