import sqlite3
from typing import List, Dict, Any
from utils.helpers import generate_id, RoomNotAvailableError, InvalidDateError
from datetime import datetime

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        self.conn = sqlite3.connect("hotel.db", check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self._seed_rooms()

    def _create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id TEXT PRIMARY KEY,
            room_number TEXT UNIQUE,
            type TEXT,
            floor INTEGER,
            status TEXT,
            price_per_night REAL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            id_proof TEXT,
            loyalty_points INTEGER DEFAULT 0
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id TEXT PRIMARY KEY,
            guest_id TEXT,
            room_id TEXT,
            check_in TEXT,
            check_out TEXT,
            status TEXT,
            total_amount REAL,
            FOREIGN KEY(guest_id) REFERENCES guests(id),
            FOREIGN KEY(room_id) REFERENCES rooms(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id TEXT PRIMARY KEY,
            reservation_id TEXT UNIQUE,
            subtotal REAL,
            tax REAL,
            total REAL,
            FOREIGN KEY(reservation_id) REFERENCES reservations(id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id TEXT PRIMARY KEY,
            invoice_id TEXT,
            method TEXT,
            amount REAL,
            status TEXT,
            receipt TEXT,
            FOREIGN KEY(invoice_id) REFERENCES invoices(id)
        )
        """)
        self.conn.commit()

    def _seed_rooms(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM rooms")
        count = cursor.fetchone()["count"]

        if count == 0:
            room_types = [
                {"type": "SingleRoom", "price": 100},
                {"type": "DoubleRoom", "price": 150},
                {"type": "DeluxeRoom", "price": 250},
                {"type": "Suite", "price": 500}
            ]
            
            room_counter = 1
            for r_type in room_types:
                for i in range(5):
                    floor = (room_counter - 1) // 5 + 1
                    room_num = f"{floor}0{(room_counter - 1) % 5 + 1}"
                    actual_price = r_type["price"]
                    if r_type["type"] == "Suite":
                        actual_price *= 1.2
                    elif r_type["type"] == "DeluxeRoom":
                        actual_price *= 1.15
                    elif r_type["type"] == "DoubleRoom":
                        actual_price *= 1.05
                        
                    room_id = f"rm_{room_counter}"
                    cursor.execute("""
                    INSERT INTO rooms (id, room_number, type, floor, status, price_per_night)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (room_id, room_num, r_type["type"], floor, "available", actual_price))
                    room_counter += 1
            self.conn.commit()

    def get_dashboard_stats(self) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM rooms")
        total_rooms = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) as count FROM rooms WHERE status = 'available'")
        available_rooms = cursor.fetchone()["count"]

        cursor.execute("SELECT COUNT(*) as count FROM reservations WHERE status = 'confirmed'")
        active_bookings = cursor.fetchone()["count"]

        cursor.execute("SELECT SUM(total) as sum FROM invoices")
        today_revenue = cursor.fetchone()["sum"] or 0.0

        return {
            "total_rooms": total_rooms,
            "available_rooms": available_rooms,
            "active_bookings": active_bookings,
            "today_revenue": today_revenue,
            "occupied_rooms": total_rooms - available_rooms,
            "total_revenue": today_revenue
        }

    def get_all_rooms(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM rooms")
        return [dict(row) for row in cursor.fetchall()]

    def update_room_status(self, room_id: str, status: str):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE rooms SET status = ? WHERE id = ?", (status, room_id))
        self.conn.commit()

    def get_all_guests(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM guests")
        return [dict(row) for row in cursor.fetchall()]

    def save_guest(self, name: str, email: str, phone: str, id_proof: str) -> str:
        guest_id = generate_id("guest")
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO guests (id, name, email, phone, id_proof)
        VALUES (?, ?, ?, ?, ?)
        """, (guest_id, name, email, phone, id_proof))
        self.conn.commit()
        return guest_id

    def get_all_reservations(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT r.*, g.name as guest_name, rm.room_number 
        FROM reservations r
        JOIN guests g ON r.guest_id = g.id
        JOIN rooms rm ON r.room_id = rm.id
        ORDER BY r.check_in DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

    def get_reservation_by_id(self, reservation_id: str) -> Dict[str, Any]:
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT r.*, g.name as guest_name, rm.room_number 
        FROM reservations r
        JOIN guests g ON r.guest_id = g.id
        JOIN rooms rm ON r.room_id = rm.id
        WHERE r.id = ?
        """, (reservation_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def save_reservation(self, guest_id: str, room_id: str, check_in: str, check_out: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
        room = cursor.fetchone()
        if not room or room["status"] != "available":
            raise RoomNotAvailableError("Room is not available")

        ci_date = datetime.strptime(check_in, "%Y-%m-%d")
        co_date = datetime.strptime(check_out, "%Y-%m-%d")
        nights = (co_date - ci_date).days
        if nights <= 0:
            raise InvalidDateError("Check-out must be after check-in")

        total_amount = nights * room["price_per_night"]
        res_id = generate_id("res")

        cursor.execute("""
        INSERT INTO reservations (id, guest_id, room_id, check_in, check_out, status, total_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (res_id, guest_id, room_id, check_in, check_out, "confirmed", total_amount))
        
        cursor.execute("UPDATE rooms SET status = 'occupied' WHERE id = ?", (room_id,))
        self.conn.commit()
        return res_id

    def delete_reservation(self, reservation_id: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT room_id FROM reservations WHERE id = ?", (reservation_id,))
        res = cursor.fetchone()
        if res:
            cursor.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
            cursor.execute("UPDATE rooms SET status = 'available' WHERE id = ?", (res["room_id"],))
            self.conn.commit()

    def get_all_invoices(self) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT i.*, r.check_in, r.check_out, g.name as guest_name 
        FROM invoices i
        JOIN reservations r ON i.reservation_id = r.id
        JOIN guests g ON r.guest_id = g.id
        """)
        return [dict(row) for row in cursor.fetchall()]

    def generate_invoice(self, reservation_id: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM invoices WHERE reservation_id = ?", (reservation_id,))
        existing = cursor.fetchone()
        if existing:
            return existing["id"]

        cursor.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,))
        res = cursor.fetchone()
        if not res:
            raise ValueError("Reservation not found")

        subtotal = res["total_amount"]
        tax = subtotal * 0.10
        total = subtotal + tax
        inv_id = generate_id("inv")

        cursor.execute("""
        INSERT INTO invoices (id, reservation_id, subtotal, tax, total)
        VALUES (?, ?, ?, ?, ?)
        """, (inv_id, reservation_id, subtotal, tax, total))
        self.conn.commit()
        return inv_id
