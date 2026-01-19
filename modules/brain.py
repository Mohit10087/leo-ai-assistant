import threading
import time
import os
import glob
import pyperclip
from modules.memory import Memory
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

class LeoBrain:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.last_clipboard = ""
        self.last_files = set()
        self.running = False

    def monitor_clipboard(self):
        while self.running:
            try:
                text = pyperclip.paste()
                if text and text != self.last_clipboard:
                    self.last_clipboard = text
                    self.memory.set("last_clipboard", text)
                    logging.info(f"[Brain] Clipboard updated.")
            except Exception as e:
                logging.error(f"[Brain] Clipboard error: {e}")
            time.sleep(2)

    def monitor_files(self, watch_dirs=None):
        if watch_dirs is None:
            watch_dirs = [os.path.expanduser("~")]  # Home directory
        while self.running:
            try:
                files = set()
                for d in watch_dirs:
                    for f in glob.glob(os.path.join(d, "**"), recursive=True):
                        if os.path.isfile(f):
                            files.add(f)
                new_files = files - self.last_files
                if new_files:
                    self.memory.set("recent_files", list(new_files))
                    logging.info(f"[Brain] New files detected: {len(new_files)}")
                self.last_files = files
            except Exception as e:
                logging.error(f"[Brain] File monitor error: {e}")
            time.sleep(10)

    def monitor_activity(self):
        # Placeholder for more advanced activity monitoring (apps, browser, etc.)
        while self.running:
            # Could add more sensors here
            time.sleep(5)

    def analyze_user(self):
        # Analyze clipboard, files, and other data to learn about the user
        clipboard = self.memory.get("last_clipboard", "")
        files = self.memory.get("recent_files", [])
        # Example: update favorite file types
        ext_count = {}
        for f in files:
            ext = os.path.splitext(f)[1]
            ext_count[ext] = ext_count.get(ext, 0) + 1
        if ext_count:
            self.memory.set("favorite_file_types", ext_count)
        # Example: analyze clipboard for keywords
        if clipboard:
            keywords = [w for w in clipboard.split() if len(w) > 5]
            self.memory.set("recent_keywords", keywords)
        logging.info("[Brain] User analysis updated.")

    def start(self):
        self.running = True
        threading.Thread(target=self.monitor_clipboard, daemon=True).start()
        threading.Thread(target=self.monitor_files, daemon=True).start()
        threading.Thread(target=self.monitor_activity, daemon=True).start()
        threading.Thread(target=self.periodic_analysis, daemon=True).start()
        logging.info("[Brain] LeoBrain started.")

    def stop(self):
        self.running = False
        logging.info("[Brain] LeoBrain stopped.")

    def periodic_analysis(self):
        while self.running:
            self.analyze_user()
            time.sleep(30)

# Usage example (add to main.py):
# from modules.memory import Memory
# from modules.brain import LeoBrain
# memory = Memory()
# brain = LeoBrain(memory)
# brain.start()
