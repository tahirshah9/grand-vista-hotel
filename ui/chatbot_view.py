import customtkinter as ctk
from database.db_manager import DatabaseManager
from ai.gemini_receptionist import GeminiReceptionist
import threading

class ChatbotView(ctk.CTkFrame):
    def __init__(self, master, db_manager: DatabaseManager, ai: GeminiReceptionist, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db_manager
        self.ai = ai
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        ctk.CTkLabel(header, text="Aria - AI Receptionist", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="Clear Chat", fg_color="red", width=100, command=self.clear_chat).pack(side="right")

        # Chat display
        self.chat_display = ctk.CTkScrollableFrame(self)
        self.chat_display.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.chat_display.grid_columnconfigure(0, weight=1)
        
        # Input area
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.entry_msg = ctk.CTkEntry(input_frame, placeholder_text="Ask Aria something...")
        self.entry_msg.grid(row=0, column=0, sticky="ew", padx=(0,10))
        self.entry_msg.bind("<Return>", lambda e: self.send_message())
        
        self.btn_send = ctk.CTkButton(input_frame, text="Send", width=100, command=self.send_message)
        self.btn_send.grid(row=0, column=1)
        
        self.msg_row = 0
        self.add_message("Aria", "Hello! I am Aria. How can I assist you today?", "bot")

    def add_message(self, sender, text, type="bot"):
        color = "#1f538d" if type == "bot" else "#2b2b2b"
        align = "w" if type == "bot" else "e"
        
        msg_frame = ctk.CTkFrame(self.chat_display, fg_color=color, corner_radius=10)
        msg_frame.grid(row=self.msg_row, column=0, pady=5, padx=10, sticky=align)
        
        ctk.CTkLabel(msg_frame, text=text, wraplength=400, justify="left").pack(padx=15, pady=10)
        self.msg_row += 1
        self.chat_display._parent_canvas.yview_moveto(1.0)

    def send_message(self):
        msg = self.entry_msg.get().strip()
        if not msg: return
        
        self.entry_msg.delete(0, 'end')
        self.add_message("You", msg, "user")
        self.btn_send.configure(state="disabled")
        
        # Run AI request in thread to not freeze UI
        threading.Thread(target=self.fetch_ai_response, args=(msg,), daemon=True).start()

    def fetch_ai_response(self, msg):
        try:
            stats = self.db.get_dashboard_stats()
            context = f"{stats['available_rooms']} available rooms, {stats['active_bookings']} active bookings."
            response = self.ai.chat(msg, context)
            self.after(0, self.add_message, "Aria", response, "bot")
        finally:
            self.after(0, lambda: self.btn_send.configure(state="normal"))

    def clear_chat(self):
        self.ai.reset_conversation()
        for widget in self.chat_display.winfo_children():
            widget.destroy()
        self.msg_row = 0
        self.add_message("Aria", "Chat cleared. How can I help you?", "bot")

    def refresh(self):
        pass # No need to refresh chat on tab switch
