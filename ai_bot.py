import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔑 Вставь свои ключи сюда
TELEGRAM_TOKEN = 'your_telegram_token_here'
OPENAI_API_KEY = 'your_openai_api_key_here'

openai.api_key = OPENAI_API_KEY

# 🤖 Обработка входящего текста
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Отправка запроса к OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # можно заменить на "gpt-4", если доступен
        messages=[
            {"role": "system", "content": "Ты умный помощник."},
            {"role": "user", "content": user_message}
        ]
    )

    bot_reply = response.choices[0].message.content
    await update.message.reply_text(bot_reply)

# Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я AI-ассистент. Задай мне вопрос!")

# 🧠 Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
