import time
import pyperclip
import logging
import asyncio
from modules.speech_module import speak
from modules.intent_analyzer import get_action_from_command
from modules.dispatcher import execute_action

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

last_clipboard = ""

def monitor_clipboard_for_selection():
    global last_clipboard
    while True:
        try:
            text = pyperclip.paste()
            if text != last_clipboard and len(text.split()) > 1:
                last_clipboard = text
                speak("sir, a text is in clipboard Should I translate or process it?")
                async def process_clipboard():
                    try:
                        action_json = await get_action_from_command(f"Process this text: {text}")
                        if action_json:
                            execute_action(action_json)
                    except Exception as e:
                        logging.error(f"Clipboard AI error: {e}")
                asyncio.create_task(process_clipboard())
        except Exception as e:
            logging.error(f"Clipboard monitor error: {e}")
        time.sleep(3)
