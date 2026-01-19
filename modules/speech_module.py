import os
import asyncio
import edge_tts
import playsound
import speech_recognition as sr
import tempfile
import re
from datetime import datetime
import pyaudio

VOICE_NAME = "en-US-AriaNeural"  


def clean_text(text):
    return re.sub(r'[^\w\s.,!?]', '', text).strip()


def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"


async def speak_async(text):
    temp_path = os.path.join(tempfile.gettempdir(), "leo_speak.mp3")
    try:
        if os.path.exists(temp_path):
            os.remove(temp_path)
    except Exception as e:
        print(f"[File Cleanup Error]: {e}")
        return
    try:
        communicate = edge_tts.Communicate(text, voice=VOICE_NAME)
        await communicate.save(temp_path)
        playsound.playsound(temp_path)
    except Exception as e:
        print(f"[Edge TTS Error]: {e}")


def speak(text):
    cleaned = clean_text(text)
    if not cleaned:
        print("[Leo says]: (Empty or invalid text — skipping TTS)")
        return
    print(f"[Leo 🗣️]: {cleaned}")
    try:
        asyncio.run(speak_async(cleaned))
    except Exception as e:
        print(f"[Async Error]: {e}")


def get_rnnoise_mic():
    try:
        mic_list = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mic_list):
            if "OBS" in name or "Virtual" in name:
                print(f"✅ RNNoise mic detected: {name}")
                return i
    except Exception as e:
        print(f"❌ Error checking mics: {e}")
    print("❌ RNNoise (OBS Virtual) mic not found. Using default mic.")
    return None

def listen_async():
    recognizer = sr.Recognizer()
    mic_index = get_rnnoise_mic()

    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("🕒 Leo is listening for a command...")
            recognizer.adjust_for_ambient_noise(source)
            print(f"🎤 Listening ({'RNNoise' if mic_index is not None else 'default'})...")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"[Heard]: {text}")
            return text
    except sr.WaitTimeoutError:
        print("⏱️ Timeout: No speech detected.")
    except sr.UnknownValueError:
        print("❓ Could not understand audio.")
    except sr.RequestError as e:
        print(f"🔌 Request Error: {e}")
    except Exception as e:
        print(f"🎙️ Mic Error: {e}")
    return ""


def play_wake_sound():
    path = os.path.join(os.path.dirname(__file__), "wake.mp3")
    if os.path.exists(path):
        playsound.playsound(path)
    else:
        print("🔔 Wake sound not found.")
