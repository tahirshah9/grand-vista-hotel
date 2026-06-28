import customtkinter as ctk
from database.db_manager import DatabaseManager
from ai.gemini_receptionist import GeminiReceptionist
from ui.dashboard_view import DashboardView
from ui.rooms_view import RoomsView
from ui.bookings_view import BookingsView
from ui.guests_view import GuestsView
from ui.invoice_view import InvoiceView
from ui.chatbot_view import ChatbotView
from datetime import datetime

class HotelApp(ctk.CTk):
    def __init__(self, ai_api_key: str):
        super().__init__()
        
        self.title("Grand Vista Hotel Booking System")
        self.geometry("1100x700")
        
        self.db = DatabaseManager()
        self.ai = GeminiReceptionist(ai_api_key)
        
        # Grid layout (1 row, 2 columns)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Grand Vista\nHotel", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=lambda: self.select_frame("Dashboard"))
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_rooms = ctk.CTkButton(self.sidebar_frame, text="Rooms", command=lambda: self.select_frame("Rooms"))
        self.btn_rooms.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_bookings = ctk.CTkButton(self.sidebar_frame, text="Bookings", command=lambda: self.select_frame("Bookings"))
        self.btn_bookings.grid(row=3, column=0, padx=20, pady=10)
        
        self.btn_guests = ctk.CTkButton(self.sidebar_frame, text="Guests", command=lambda: self.select_frame("Guests"))
        self.btn_guests.grid(row=4, column=0, padx=20, pady=10)
        
        self.btn_invoices = ctk.CTkButton(self.sidebar_frame, text="Invoices", command=lambda: self.select_frame("Invoices"))
        self.btn_invoices.grid(row=5, column=0, padx=20, pady=10)
        
        self.btn_ai = ctk.CTkButton(self.sidebar_frame, text="AI Receptionist", command=lambda: self.select_frame("AI Receptionist"))
        self.btn_ai.grid(row=6, column=0, padx=20, pady=10)
        
        self.theme_switch = ctk.CTkSwitch(self.sidebar_frame, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.grid(row=8, column=0, padx=20, pady=20)
        self.theme_switch.select()

        # Main View Area
        self.main_view = ctk.CTkFrame(self, fg_color="transparent")
        self.main_view.grid(row=0, column=1, sticky="nsew")
        self.main_view.grid_rowconfigure(1, weight=1)
        self.main_view.grid_columnconfigure(0, weight=1)
        
        # Top bar with clock
        self.top_bar = ctk.CTkFrame(self.main_view, height=50)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,0))
        
        self.clock_label = ctk.CTkLabel(self.top_bar, text="", font=ctk.CTkFont(size=14))
        self.clock_label.pack(side="right", padx=20, pady=10)
        self.update_clock()
        
        # Container for views
        self.view_container = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.view_container.grid(row=1, column=0, sticky="nsew")
        self.view_container.grid_rowconfigure(0, weight=1)
        self.view_container.grid_columnconfigure(0, weight=1)
        
        # Initialize views
        self.views = {
            "Dashboard": DashboardView(self.view_container, self.db),
            "Rooms": RoomsView(self.view_container, self.db),
            "Bookings": BookingsView(self.view_container, self.db),
            "Guests": GuestsView(self.view_container, self.db),
            "Invoices": InvoiceView(self.view_container, self.db),
            "AI Receptionist": ChatbotView(self.view_container, self.db, self.ai)
        }
        
        self.current_view = None
        self.select_frame("Dashboard")

    def select_frame(self, name):
        if self.current_view:
            self.current_view.grid_forget()
        
        self.current_view = self.views[name]
        self.current_view.grid(row=0, column=0, sticky="nsew")
        if hasattr(self.current_view, 'refresh'):
            self.current_view.refresh()

    def toggle_theme(self):
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def update_clock(self):
        now = datetime.now().strftime("%A, %b %d %Y | %I:%M:%S %p")
        self.clock_label.configure(text=now)
        self.after(1000, self.update_clock)
