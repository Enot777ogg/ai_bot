from telegram import Update
from telegram.ext import ContextTypes
from utils.audio_utils import convert_ogg_to_wav, speech_to_text, text_to_speech
from utils.openai_client import ask_gpt
import os

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    ogg_path = "temp_audio/input.ogg"
    wav_path = "temp_audio/input.wav"
    mp3_path = "temp_audio/output.mp3"

    await file.download_to_drive(ogg_path)

    try:
        convert_ogg_to_wav(ogg_path, wav_path)
        text = speech_to_text(wav_path)
        await update.message.reply_text(f"📥 Распознано: {text}")

        reply = ask_gpt(text)
        await update.message.reply_text(reply)

        text_to_speech(reply, mp3_path)
        with open(mp3_path, 'rb') as audio:
            await update.message.reply_voice(audio)

    except Exception as e:
        await update.message.reply_text(f"Ошибка при обработке аудио: {e}")

