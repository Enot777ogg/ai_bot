import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers.menu_handler import start, handle_menu_choice
from handlers.text_handler import handle_text
from db.session import init_db
from dotenv import load_dotenv
load_dotenv()

# Загрузи токен
BOT_TOKEN = os.getenv("BOT_TOKEN")  # добавь в .env или в Termux вручную
init_db()

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_menu_choice))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()
