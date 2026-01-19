import json
import re
from ai_engine import ask_ai  # Assumes async is handled or not needed
import webbrowser
import requests

# --- UTILITY ---

def extract_json(text):
    """
    Extract JSON object from AI's possibly formatted or code-block wrapped response.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*({.*?})\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError as e:
                print("[DEBUG] Clean JSON parse error:", e)
    print("[DEBUG] No valid JSON found in AI response.")
    return None

def is_url_reachable(url):
    """
    Optionally check if the website is reachable.
    """
    try:
        r = requests.head(url, allow_redirects=True, timeout=2)
        return r.status_code < 400
    except:
        return False

# --- MAIN COMMAND INTERPRETATION ---

def get_action_from_command(command):
    prompt = f"""
You are an AI assistant named Leo. Interpret the user's command and return the action as JSON.

Supported actions:
- open_website: with a realistic URL like "https://www.youtube.com"
- edit_file: with file_path and changes
- fill_form: with website_url and field_data
- answer_question: with answer_text
- run_code: with code_snippet and language
- system_control: like shutdown, volume_up, etc.
- translate: with input_text and target_language
- summarize: with input_text

Command: "{command}"

Respond ONLY with JSON like:
{{
  "action": "open_website",
  "data": {{
    "url": "https://www.youtube.com"
  }}
}}
"""

    try:
        response = ask_ai(prompt)
        print("[DEBUG] Raw AI response:", response)
        return extract_json(response)
    except Exception as e:
        print("[ERROR] Failed to get AI action:", e)
        return None

# --- OPTIONAL: ACTION HANDLING (call this after parsing)

def handle_action(parsed):
    if not parsed:
        print("[Leo 🗣️]: Sorry, I couldn't understand that.")
        return

    action = parsed.get("action")
    data = parsed.get("data", {})

    if action == "open_website":
        url = data.get("url")
        if url and is_url_reachable(url):
            print(f"[Leo 🗣️]: Opening {url}")
            webbrowser.open(url)
        else:
            print("[Leo 🗣️]: That website seems unreachable.")
    else:
        print(f"[Leo 🗣️]: I understood action '{action}', but I don't know how to do that yet.")
