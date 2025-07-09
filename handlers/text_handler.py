from telegram import Update
from telegram.ext import ContextTypes
from utils.openai_client import ask_gpt

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = ask_gpt(user_message)
    await update.message.reply_text(reply)

