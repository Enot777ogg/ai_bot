import os
from pydub import AudioSegment
import speech_recognition as sr
from gtts import gTTS

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

def convert_ogg_to_wav(ogg_path: str, wav_path: str):
    audio = AudioSegment.from_ogg(ogg_path)
    audio.export(wav_path, format="wav")

def speech_to_text(wav_path: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio, language="ru-RU")

def text_to_speech(text: str, output_path: str):
    tts = gTTS(text, lang='ru')
    tts.save(output_path)
