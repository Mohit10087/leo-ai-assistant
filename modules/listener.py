import threading
import asyncio
import logging
from modules.speech_module import listen_async, speak
from modules.ai_engine import ask_ai

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def listen_for_wakeword():
    def _listen():
        while True:
            command = listen_async()
            if "leo" in (command or "").lower():
                speak("Yes, I'm listening.")
                query = listen_async()
                if query:
                    try:
                        reply = asyncio.run(ask_ai(query))
                        speak(reply)
                    except Exception as e:
                        logging.error(f"[AI Error]: {e}")
                        speak("Sorry, I had trouble processing your request.")
    threading.Thread(target=_listen, daemon=True).start()
