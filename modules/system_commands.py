import os
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def open_app(app_name):
    try:
        if app_name == "chrome":
            os.system("start chrome")
        elif app_name == "notepad":
            os.system("start notepad")
        else:
            logging.warning(f"Unknown app requested: {app_name}")
    except Exception as e:
        logging.error(f"Failed to open app {app_name}: {e}")

def shutdown():
    try:
        os.system("shutdown /s /t 1")
    except Exception as e:
        logging.error(f"Shutdown failed: {e}")

def restart():
    try:
        os.system("shutdown /r /t 1")
    except Exception as e:
        logging.error(f"Restart failed: {e}")
