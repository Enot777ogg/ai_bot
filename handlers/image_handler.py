from telegram import Update
from telegram.ext import ContextTypes
from utils.image_utils import encode_image_to_base64
from config import OPENAI_API_KEY
import openai
import os

openai.api_key = OPENAI_API_KEY

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]  # самое большое качество
    file = await photo.get_file()
    img_path = "temp_image.png"
    await file.download_to_drive(img_path)

    try:
        base64_image = encode_image_to_base64(img_path)

        response = openai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Что на этом изображении?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1000,
        )

        result = response.choices[0].message.content
        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")
