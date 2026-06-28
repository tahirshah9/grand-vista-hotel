import customtkinter as ctk
from database.db_manager import DatabaseManager

class RoomsView(ctk.CTkFrame):
    def __init__(self, master, db_manager: DatabaseManager, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db_manager
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        title = ctk.CTkLabel(header_frame, text="Rooms Management", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(side="left")

        self.filter_var = ctk.StringVar(value="All")
        filters = ["All", "SingleRoom", "DoubleRoom", "DeluxeRoom", "Suite"]
        self.filter_menu = ctk.CTkOptionMenu(header_frame, values=filters, variable=self.filter_var, command=self.refresh)
        self.filter_menu.pack(side="right")

        # Scrollable Area for rooms
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.scroll_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.refresh()

    def refresh(self, *args):
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        rooms = self.db.get_all_rooms()
        filter_val = self.filter_var.get()
        if filter_val != "All":
            rooms = [r for r in rooms if r["type"] == filter_val]

        row = 0
        col = 0
        for room in rooms:
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=f"Room {room['room_number']}", font=ctk.CTkFont(weight="bold")).pack(pady=(10,0))
            ctk.CTkLabel(card, text=f"{room['type']} - Floor {room['floor']}").pack()
            ctk.CTkLabel(card, text=f"${room['price_per_night']:.2f}/night").pack()
            
            color = "green" if room["status"] == "available" else "red" if room["status"] == "occupied" else "orange"
            ctk.CTkLabel(card, text=room["status"].upper(), text_color=color).pack(pady=(0,5))
            
            # Status change option
            status_var = ctk.StringVar(value=room["status"])
            opt = ctk.CTkOptionMenu(card, values=["available", "occupied", "maintenance"], variable=status_var, 
                                    command=lambda v, r_id=room["id"]: self.change_status(r_id, v))
            opt.pack(pady=10, padx=10)

            col += 1
            if col > 3:
                col = 0
                row += 1

    def change_status(self, room_id, new_status):
        self.db.update_room_status(room_id, new_status)
        self.refresh()
