import datetime
from modules.speech_module import speak
from modules.user_profile import get_profile

def greet_user():
    hour = datetime.datetime.now().hour
    user = get_profile().get("name", "there")

    if hour < 12:
        greet = "Good morning"
    elif hour < 18:
        greet = "Good afternoon"
    else:
        greet = "Good evening"

    speak(f"{greet}, {user}. I'm Leo, ready to help.")
