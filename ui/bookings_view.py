import customtkinter as ctk
from tkinter import ttk, messagebox
from database.db_manager import DatabaseManager

class BookingsView(ctk.CTkFrame):
    def __init__(self, master, db_manager: DatabaseManager, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db_manager
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="New Booking", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.guest_var = ctk.StringVar()
        self.cb_guest = ctk.CTkComboBox(form_frame, variable=self.guest_var)
        self.cb_guest.grid(row=1, column=0, padx=10, pady=10)
        
        self.room_var = ctk.StringVar()
        self.cb_room = ctk.CTkComboBox(form_frame, variable=self.room_var)
        self.cb_room.grid(row=1, column=1, padx=10, pady=10)
        
        self.entry_check_in = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD")
        self.entry_check_in.grid(row=1, column=2, padx=10, pady=10)
        
        self.entry_check_out = ctk.CTkEntry(form_frame, placeholder_text="YYYY-MM-DD")
        self.entry_check_out.grid(row=1, column=3, padx=10, pady=10)
        
        btn_book = ctk.CTkButton(form_frame, text="Book Now", command=self.book_room)
        btn_book.grid(row=1, column=4, padx=10, pady=10)

        # Treeview
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=1, column=0, padx=20, pady=(0,20), sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        columns = ("id", "guest", "room", "check_in", "check_out", "status", "total")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("guest", text="Guest Name")
        self.tree.heading("room", text="Room No")
        self.tree.heading("check_in", text="Check In")
        self.tree.heading("check_out", text="Check Out")
        self.tree.heading("status", text="Status")
        self.tree.heading("total", text="Total ($)")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Action Buttons
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=2, column=0, padx=20, pady=10, sticky="e")
        ctk.CTkButton(action_frame, text="Generate Invoice", command=self.generate_invoice).pack(side="right", padx=10)
        ctk.CTkButton(action_frame, text="Cancel Booking", fg_color="red", hover_color="darkred", command=self.cancel_booking).pack(side="right")

        self.refresh()

    def book_room(self):
        guest_val = self.guest_var.get()
        room_val = self.room_var.get()
        check_in = self.entry_check_in.get()
        check_out = self.entry_check_out.get()
        
        if guest_val and room_val and check_in and check_out:
            guest_id = guest_val.split(" - ")[0]
            room_id = room_val.split(" - ")[0]
            try:
                self.db.save_reservation(guest_id, room_id, check_in, check_out)
                messagebox.showinfo("Success", "Booking created successfully!")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def cancel_booking(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            res_id = item["values"][0]
            self.db.delete_reservation(res_id)
            self.refresh()
            messagebox.showinfo("Success", "Booking cancelled.")

    def generate_invoice(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            res_id = item["values"][0]
            try:
                self.db.generate_invoice(res_id)
                messagebox.showinfo("Success", "Invoice generated! Check Invoices tab.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def refresh(self):
        guests = self.db.get_all_guests()
        self.cb_guest.configure(values=[f"{g['id']} - {g['name']}" for g in guests])
        
        rooms = [r for r in self.db.get_all_rooms() if r["status"] == "available"]
        self.cb_room.configure(values=[f"{r['id']} - Rm {r['room_number']}" for r in rooms])

        for item in self.tree.get_children():
            self.tree.delete(item)
            
        reservations = self.db.get_all_reservations()
        for r in reservations:
            self.tree.insert("", "end", values=(r["id"], r["guest_name"], r["room_number"], r["check_in"], r["check_out"], r["status"], f"{r['total_amount']:.2f}"))
