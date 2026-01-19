import json
import os
import logging

PROFILE_PATH = "profile.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def get_profile():
    if os.path.exists(PROFILE_PATH):
        try:
            with open(PROFILE_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load profile: {e}")
            return {"name": "User"}
    return {"name": "User"}

def set_profile(name):
    try:
        with open(PROFILE_PATH, "w") as f:
            json.dump({"name": name}, f)
    except Exception as e:
        logging.error(f"Failed to save profile: {e}")
