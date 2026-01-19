
import ollama

def ask_ai(prompt):
    try:
        if not prompt.strip():
            return "Sorry, that was an empty question 😅."

        response = ollama.chat(model='phi3', messages=[
            {"role": "user", "content": prompt}
        ])
        return response['message']['content'].strip()
    except Exception as e:
        return f"[Ollama Error]: {e}"
