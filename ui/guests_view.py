import customtkinter as ctk
from tkinter import ttk
from database.db_manager import DatabaseManager

class GuestsView(ctk.CTkFrame):
    def __init__(self, master, db_manager: DatabaseManager, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db_manager
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        ctk.CTkLabel(form_frame, text="Register Guest", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_name = ctk.CTkEntry(form_frame, placeholder_text="Name")
        self.entry_name.grid(row=1, column=0, padx=10, pady=10)
        
        self.entry_email = ctk.CTkEntry(form_frame, placeholder_text="Email")
        self.entry_email.grid(row=1, column=1, padx=10, pady=10)
        
        self.entry_phone = ctk.CTkEntry(form_frame, placeholder_text="Phone")
        self.entry_phone.grid(row=1, column=2, padx=10, pady=10)
        
        self.entry_id = ctk.CTkEntry(form_frame, placeholder_text="ID Proof")
        self.entry_id.grid(row=1, column=3, padx=10, pady=10)
        
        btn_register = ctk.CTkButton(form_frame, text="Register", command=self.register_guest)
        btn_register.grid(row=1, column=4, padx=10, pady=10)

        # Treeview
        tree_frame = ctk.CTkFrame(self)
        tree_frame.grid(row=1, column=0, padx=20, pady=(0,20), sticky="nsew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        columns = ("id", "name", "email", "phone", "id_proof", "points")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree.heading("id", text="Guest ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("id_proof", text="ID Proof")
        self.tree.heading("points", text="Points")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Style treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", background="#565b5e", foreground="white", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        self.refresh()

    def register_guest(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        phone = self.entry_phone.get()
        id_proof = self.entry_id.get()
        
        if name and email and phone and id_proof:
            self.db.save_guest(name, email, phone, id_proof)
            self.entry_name.delete(0, 'end')
            self.entry_email.delete(0, 'end')
            self.entry_phone.delete(0, 'end')
            self.entry_id.delete(0, 'end')
            self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        guests = self.db.get_all_guests()
        for g in guests:
            self.tree.insert("", "end", values=(g["id"], g["name"], g["email"], g["phone"], g["id_proof"], g["loyalty_points"]))
