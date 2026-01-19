
from modules.speech_module import speak, listen_async, play_wake_sound, get_greeting
from modules.intent_analyzer import get_action_from_command
from modules.dispatcher import execute_action
from modules.wakeword import wait_for_wake_word
from modules.selection_monitor import monitor_clipboard_for_selection
from modules.leo_dot import launch_dot
from modules.memory import Memory
from modules.brain import LeoBrain
import threading
import time


def run_assistant():

    speak("greeting sir , this is leo your pc")
    threading.Thread(target=monitor_clipboard_for_selection, daemon=True).start()
    # Start LeoBrain for continuous learning
    memory = Memory()
    brain = LeoBrain(memory)
    brain.start()

    while True:
        wait_for_wake_word()  
        play_wake_sound()
        speak("Yes sir?")
        print("🕒 Leo is listening for a command...")

        start_time = time.time()
        command = None

        while time.time() - start_time < 120: 
            command = listen_async()
            if command:
                break

        if not command:
            print("🕓 Timeout. No command heard. Leo will wait again.")
            continue

        print(f"[You said]: {command}")
        if "stop" in command.lower():
            speak("Goodbye!")
            break

        try:
            action_json = get_action_from_command(command) 
            print(f"[DEBUG] Parsed action: {action_json}")

            if action_json:
                execute_action(action_json)
            else:
                speak("Sorry, sir please repeat.")
        except Exception as e:
            print(f"[❌ Command Error]: {e}")
            speak("Something went wrong. Please try again.")

if __name__ == "__main__":
    threading.Thread(target=launch_dot, daemon=True).start()
    run_assistant()
    
