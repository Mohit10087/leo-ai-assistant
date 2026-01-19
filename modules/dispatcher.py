import os
import webbrowser
import subprocess
import pyautogui
from modules.speech_module import speak

def execute_action(action_json):
    try:
        action = action_json["action"]
        data = action_json["data"]
    except:
        speak("Sorry, I couldn't understand that.")
        return

    if action == "open_website":
        url = data.get("url")
        if url:
            speak(f"Opening {url}")
            webbrowser.open(url)

    elif action == "system_control":
        cmd = data.get("command")
        if cmd:
            speak("Executing system command.")
            os.system(cmd)

    elif action == "answer_question":
        answer = data.get("answer_text")
        if answer:
            speak(answer)

    elif action == "edit_file":
        file_path = data.get("file_path")
        changes = data.get("changes")
        if file_path and changes:
            try:
                with open(file_path, 'a') as f:
                    f.write("\n" + changes)
                speak("File updated successfully.")
            except:
                speak("I couldn't edit the file.")

    elif action == "fill_form":
        fields = data.get("field_data", {})
        speak("Starting form fill.")
        for key, value in fields.items():
            pyautogui.typewrite(value)
            pyautogui.press('tab')

    elif action == "run_code":
        code = data.get("code_snippet")
        lang = data.get("language")
        if code and lang == "python":
            try:
                exec(code, {})
                speak("Code executed.")
            except Exception as e:
                speak(f"Code failed: {e}")
    else:
        speak("Sorry, I don't know how to do that yet.")
