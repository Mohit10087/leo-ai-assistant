import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import json
import math 
import asyncio
from modules.ai_engine import ask_ai

SETTINGS_FILE = os.path.join(os.path.expanduser("~"), ".leo_dot_settings.json")


def create_rounded_image(path, size=(60, 60)):
    img = Image.open(path).convert("RGBA").resize(size)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    img.putalpha(mask)
    return ImageTk.PhotoImage(img)


class LeoDot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='white')
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.geometry(self.load_position())

        self.angle = 0
        self.fade_in_alpha = 0.0
        self.fade_in()

        self.color1 = "#00f5ff"
        self.color2 = "#f500ff"

        self.menu_buttons = []
        self.menu_visible = False

        self.menu_config = [
            {"icon": "🎤 Listen", "action": self.say_hi},
            {"icon": "💬 Chatbot", "action": self.open_chatbot},
            {"icon": "❌ Exit", "action": self.hide_radial_menu},
        ]

        self.create_icon()
        self.animate_ring()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def create_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "leo_face.png")
        icon_path = os.path.abspath(icon_path)

        if os.path.exists(icon_path):
            self.tk_img = create_rounded_image(icon_path)
        else:
            img = Image.new("RGBA", (60, 60), "blue")
            draw = ImageDraw.Draw(img)
            draw.ellipse((0, 0, 60, 60), fill="blue")
            self.tk_img = ImageTk.PhotoImage(img)

        self.canvas = tk.Canvas(self.root, width=80, height=80, bg="white", bd=0, highlightthickness=0)
        self.canvas.pack()

        self.icon_obj = self.canvas.create_image(40, 40, image=self.tk_img)
        self.rings = []
        for i in range(36):
            angle = math.radians(i * 10)
            x = 40 + 30 * math.cos(angle)
            y = 40 + 30 * math.sin(angle)
            dot = self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=self.color1, outline="")
            self.rings.append(dot)

        self.canvas.bind("<Button-1>", self.toggle_menu)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<Enter>", self.on_hover)
        self.canvas.bind("<Leave>", self.on_leave)

    def toggle_menu(self, _=None):
        if self.menu_visible:
            self.hide_radial_menu()
        else:
            self.root.after(10, self.show_radial_menu)

    def show_radial_menu(self):
        self.menu_buttons = []

        self.root.update_idletasks()
        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        center_x = root_x + 40
        center_y = root_y + 40
        radius = 100

        start_angle = 0    
        arc_span = 90         

        total_buttons = len(self.menu_config)
        angle_step = arc_span / (total_buttons - 1) if total_buttons > 1 else 0

        for i, item in enumerate(self.menu_config):
            label = item["icon"]
            cmd = item["action"]

            angle_deg = start_angle + i * angle_step
            angle_rad = math.radians(angle_deg)

            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)

            btn = tk.Toplevel(self.root)
            btn.overrideredirect(True)
            btn.attributes("-topmost", True)

            button_widget = tk.Button(
                btn,
                text=label,
                command=lambda c=cmd, b=btn: [c(), self.hide_radial_menu()],
                font=("Consolas", 10),
                bg="#1e1e2f",
                fg="lime",
                bd=0,
                relief="solid",
                highlightthickness=1,
                highlightbackground="#00f5ff",
                activebackground="#444",
                activeforeground="white"
            )
            button_widget.pack(ipadx=10, ipady=5)
            btn.geometry(f"+{int(x - 25)}+{int(y - 25)}")
            self.menu_buttons.append(btn)

        self.menu_visible = True

    def hide_radial_menu(self):
        for btn in self.menu_buttons:
            btn.destroy()
        self.menu_buttons.clear()
        self.menu_visible = False

    def drag(self, e):
        x = e.x_root - 40
        y = e.y_root - 40
        self.root.geometry(f"+{x}+{y}")
        self.save_position(f"{x}+{y}")

    def animate_ring(self):
        for i, dot in enumerate(self.rings):
            ratio = (math.sin(math.radians(self.angle + i * 10)) + 1) / 2
            r1, g1, b1 = self.hex_to_rgb(self.color1)
            r2, g2, b2 = self.hex_to_rgb(self.color2)
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.itemconfig(dot, fill=color)
        self.angle = (self.angle + 5) % 360
        self.root.after(50, self.animate_ring)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def fade_in(self):
        if self.fade_in_alpha < 1.0:
            self.fade_in_alpha += 0.05
            self.root.attributes("-alpha", self.fade_in_alpha)
            self.root.after(40, self.fade_in)

    def on_hover(self, _):
        for dot in self.rings:
            self.canvas.itemconfig(dot, outline="#ffffff", width=1)

    def on_leave(self, _):
        for dot in self.rings:
            self.canvas.itemconfig(dot, outline="", width=0)

    def say_hi(self):
        try:
            from modules.speech_module import speak
            speak("Yes, how can I help you?")
        except:
            print("Speech module not found or failed.")

    def open_chatbot(self):
        chat_win = tk.Toplevel(self.root)
        chat_win.title("Leo Chatbot")
        chat_win.geometry("350x320")
        chat_win.configure(bg="#1e1e2f")
        chat_win.resizable(False, False)

        response_area = tk.Text(chat_win, wrap=tk.WORD, height=10,
                                bg="#0f0f1a", fg="white", font=("Consolas", 10))
        response_area.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 4))
        response_area.config(state=tk.DISABLED)

        entry = tk.Entry(chat_win, bg="#222", fg="white", font=("Consolas", 10))
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
            insert_response("🤖 Leo is typing...\n")
            async def get_response():
                try:
                    response = await ask_ai(user_text)
                except Exception as e:
                    response = f"[Error: {e}]"
                # Remove 'Leo is typing...' and insert real response
                response_area.config(state=tk.NORMAL)
                content = response_area.get("1.0", tk.END)
                content = content.replace("🤖 Leo is typing...\n", "")
                response_area.delete("1.0", tk.END)
                response_area.insert(tk.END, content)
                response_area.insert(tk.END, f"🤖 Leo: {response}\n")
                response_area.config(state=tk.DISABLED)
                response_area.see(tk.END)
            asyncio.create_task(get_response())

        entry.bind("<Return>", lambda e: send_query())

    def save_position(self, pos_str):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"position": pos_str}, f)

    def load_position(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                return f"80x80+{data['position']}"
        return "80x80+100+100"

    def on_close(self):
        self.save_position(self.root.geometry().split('+')[1] + '+' + self.root.geometry().split('+')[2])
        self.root.destroy()


def launch_dot():
    LeoDot()


if __name__ == "__main__":
    launch_dot()
