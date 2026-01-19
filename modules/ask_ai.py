import ollama

def ask_ai(prompt):
    try:
        response = ollama.chat(model='phi3', messages=[
            {"role": "user", "content": prompt}
        ])
        return response['message']['content']
    except Exception as e:
        print(f"[Ollama Error]: {e}")
        return ""
