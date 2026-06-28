import customtkinter as ctk
from database.db_manager import DatabaseManager

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, db_manager: DatabaseManager, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db_manager
        
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=4, padx=20, pady=(20, 10), sticky="w")

        # Stats Cards
        self.card_frame_1 = ctk.CTkFrame(self, corner_radius=10)
        self.card_frame_1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.card_frame_2 = ctk.CTkFrame(self, corner_radius=10)
        self.card_frame_2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.card_frame_3 = ctk.CTkFrame(self, corner_radius=10)
        self.card_frame_3.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.card_frame_4 = ctk.CTkFrame(self, corner_radius=10)
        self.card_frame_4.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        self.lbl_total_rooms = ctk.CTkLabel(self.card_frame_1, text="Total Rooms\n0", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_total_rooms.pack(expand=True, pady=20)
        
        self.lbl_available = ctk.CTkLabel(self.card_frame_2, text="Available\n0", font=ctk.CTkFont(size=18, weight="bold"), text_color="green")
        self.lbl_available.pack(expand=True, pady=20)
        
        self.lbl_bookings = ctk.CTkLabel(self.card_frame_3, text="Active Bookings\n0", font=ctk.CTkFont(size=18, weight="bold"), text_color="orange")
        self.lbl_bookings.pack(expand=True, pady=20)
        
        self.lbl_revenue = ctk.CTkLabel(self.card_frame_4, text="Revenue\n$0.00", font=ctk.CTkFont(size=18, weight="bold"), text_color="blue")
        self.lbl_revenue.pack(expand=True, pady=20)

        self.refresh()

    def refresh(self):
        stats = self.db.get_dashboard_stats()
        self.lbl_total_rooms.configure(text=f"Total Rooms\n{stats['total_rooms']}")
        self.lbl_available.configure(text=f"Available\n{stats['available_rooms']}")
        self.lbl_bookings.configure(text=f"Active Bookings\n{stats['active_bookings']}")
        self.lbl_revenue.configure(text=f"Revenue\n${stats['today_revenue']:.2f}")
