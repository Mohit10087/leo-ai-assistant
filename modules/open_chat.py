import tkinter as tk
import asyncio
import logging
from modules.ai_engine import ask_ai

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def open_chat(self, _=None):
    if hasattr(self, "chat_win") and self.chat_win.winfo_exists():
        self.chat_win.lift()
        return

    self.chat_win = tk.Toplevel(self.root)
    self.chat_win.title("Leo Quick Chat")
    self.chat_win.geometry("300x220")
    self.chat_win.configure(bg="#1e1e2f")
    self.chat_win.resizable(False, False)

    response_area = tk.Text(self.chat_win, wrap=tk.WORD, height=6,
                            bg="#0f0f1a", fg="white", font=("Consolas", 10))
    response_area.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 4))
    response_area.config(state=tk.DISABLED)

    entry = tk.Entry(self.chat_win, bg="#222", fg="white", font=("Consolas", 10))
    entry.pack(fill=tk.X, padx=8, pady=(0, 4))
    entry.focus()

    def insert_response(text):
        response_area.config(state=tk.NORMAL)
        response_area.insert(tk.END, text)
        response_area.config(state=tk.DISABLED)
        response_area.see(tk.END)

    def send_query():
        user_text = entry.get()
        if not user_text.strip():
            return
        entry.delete(0, tk.END)
        insert_response(f"\n🧑 You: {user_text}\n")
        async def get_response():
            try:
                response = await ask_ai(user_text)
            except Exception as e:
                logging.error(f"[Chat Error]: {e}")
                response = f"[Error: {e}]"
            insert_response(f"🤖 Leo: {response}\n")
        asyncio.create_task(get_response())

    entry.bind("<Return>", lambda e: send_query())
