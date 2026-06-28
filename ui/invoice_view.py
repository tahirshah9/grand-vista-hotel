import customtkinter as ctk
from database.db_manager import DatabaseManager
import os

class InvoiceView(ctk.CTkFrame):
    def __init__(self, master, db_manager: DatabaseManager, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db_manager
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(self, text="Invoices", font=ctk.CTkFont(size=24, weight="bold"))
        header.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scroll_frame.grid_columnconfigure((0,1), weight=1)

        self.refresh()

    def refresh(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        invoices = self.db.get_all_invoices()
        
        row = 0
        col = 0
        for inv in invoices:
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=10)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(card, text="GRAND VISTA HOTEL", font=ctk.CTkFont(weight="bold")).pack(pady=(10,0))
            ctk.CTkLabel(card, text=f"Invoice ID: {inv['id']}").pack()
            ctk.CTkLabel(card, text=f"Guest: {inv['guest_name']}").pack()
            ctk.CTkLabel(card, text=f"Stay: {inv['check_in']} to {inv['check_out']}").pack()
            
            ctk.CTkLabel(card, text="-"*30).pack()
            ctk.CTkLabel(card, text=f"Subtotal: ${inv['subtotal']:.2f}").pack()
            ctk.CTkLabel(card, text=f"Tax (10%): ${inv['tax']:.2f}").pack()
            ctk.CTkLabel(card, text=f"TOTAL: ${inv['total']:.2f}", font=ctk.CTkFont(weight="bold"), text_color="blue").pack(pady=(5,10))
            
            ctk.CTkButton(card, text="Export .txt", command=lambda i=inv: self.export(i)).pack(pady=10)

            col += 1
            if col > 1:
                col = 0
                row += 1

    def export(self, inv):
        filename = f"{inv['id']}.txt"
        with open(filename, "w") as f:
            f.write("=" * 40 + "\n")
            f.write("   GRAND VISTA HOTEL - INVOICE\n")
            f.write("=" * 40 + "\n")
            f.write(f"Invoice ID : {inv['id']}\n")
            f.write(f"Guest      : {inv['guest_name']}\n")
            f.write(f"Check In   : {inv['check_in']}\n")
            f.write(f"Check Out  : {inv['check_out']}\n")
            f.write("-" * 40 + "\n")
            f.write(f"Subtotal   : ${inv['subtotal']:.2f}\n")
            f.write(f"Tax (10%)  : ${inv['tax']:.2f}\n")
            f.write("=" * 40 + "\n")
            f.write(f"TOTAL      : ${inv['total']:.2f}\n")
            f.write("=" * 40 + "\n")
        import tkinter.messagebox
        tkinter.messagebox.showinfo("Exported", f"Invoice saved to {os.path.abspath(filename)}")
