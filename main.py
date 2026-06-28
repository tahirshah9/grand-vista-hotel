import os
from dotenv import load_dotenv
from ui.app import HotelApp
import customtkinter as ctk

def main():
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found in environment variables.")
        api_key = "dummy_key_to_prevent_crash"
        
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = HotelApp(api_key)
    app.mainloop()

if __name__ == "__main__":
    main()
