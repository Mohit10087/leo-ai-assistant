from vosk import Model, KaldiRecognizer
import pyaudio
import json
import time
import logging

WAKE_WORD = "leo"
COOLDOWN_SECONDS = 3  # Prevent repeated false triggers

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Load Vosk model once
try:
    model = Model("modules/vosk_model")
    rec = KaldiRecognizer(model, 16000)
except Exception as e:
    logging.error(f"Failed to load Vosk model: {e}")
    raise

# Set up microphone stream
try:
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8000
    )
    stream.start_stream()
except Exception as e:
    logging.error(f"Failed to initialize microphone stream: {e}")
    raise

def wait_for_wake_word():
    logging.info(f"🔎 Waiting for wake word '{WAKE_WORD.capitalize()}' (offline)...")
    last_trigger_time = 0
    while True:
        try:
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                try:
                    result = json.loads(rec.Result())
                    text = result.get("text", "").lower()
                    if WAKE_WORD in text:
                        now = time.time()
                        if now - last_trigger_time > COOLDOWN_SECONDS:
                            last_trigger_time = now
                            return
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            logging.error(f"Wakeword detection error: {e}")
            time.sleep(1)
