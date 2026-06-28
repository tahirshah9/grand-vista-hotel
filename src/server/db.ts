import Database from 'better-sqlite3';
import path from 'path';
import fs from 'fs';

const dbPath = path.join(process.cwd(), 'hotel.db');
const db = new Database(dbPath);

db.pragma('journal_mode = WAL');

// Initialize database tables
db.exec(`
  CREATE TABLE IF NOT EXISTS rooms (
    id TEXT PRIMARY KEY,
    room_number TEXT UNIQUE,
    type TEXT,
    floor INTEGER,
    status TEXT,
    price_per_night REAL
  );

  CREATE TABLE IF NOT EXISTS guests (
    id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    id_proof TEXT,
    loyalty_points INTEGER DEFAULT 0
  );

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
  );

  CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY,
    reservation_id TEXT UNIQUE,
    subtotal REAL,
    tax REAL,
    total REAL,
    FOREIGN KEY(reservation_id) REFERENCES reservations(id)
  );
`);

// Seed data if empty
const countRooms = db.prepare('SELECT COUNT(*) as count FROM rooms').get() as { count: number };
if (countRooms.count === 0) {
  const insertRoom = db.prepare('INSERT INTO rooms (id, room_number, type, floor, status, price_per_night) VALUES (?, ?, ?, ?, ?, ?)');
  
  const roomTypes = [
    { type: 'SingleRoom', price: 100 },
    { type: 'DoubleRoom', price: 150 },
    { type: 'DeluxeRoom', price: 250 },
    { type: 'Suite', price: 500 }
  ];

  let roomCounter = 1;
  for (const type of roomTypes) {
    for (let i = 0; i < 5; i++) {
      const floor = Math.ceil(roomCounter / 5);
      const roomNumber = `${floor}0${(roomCounter % 5) || 5}`;
      // Suite adds 20%
      const actualPrice = type.type === 'Suite' ? type.price * 1.2 : type.price;
      insertRoom.run(`rm_${roomCounter}`, roomNumber, type.type, floor, 'available', actualPrice);
      roomCounter++;
    }
  }
}

class DatabaseManager {
  
  // Dashboard
  getDashboardStats() {
    const totalRooms = db.prepare('SELECT COUNT(*) as count FROM rooms').get() as { count: number };
    const availableRooms = db.prepare("SELECT COUNT(*) as count FROM rooms WHERE status = 'available'").get() as { count: number };
    const activeBookings = db.prepare("SELECT COUNT(*) as count FROM reservations WHERE status = 'confirmed'").get() as { count: number };
    
    // Today's revenue (sum of completed/confirmed invoices for simplicity)
    const todayRevenue = db.prepare("SELECT SUM(total) as sum FROM invoices").get() as { sum: number | null };

    return {
      totalRooms: totalRooms.count,
      availableRooms: availableRooms.count,
      activeBookings: activeBookings.count,
      todayRevenue: todayRevenue.sum || 0
    };
  }

  // Rooms
  getAllRooms() {
    return db.prepare('SELECT * FROM rooms').all();
  }

  updateRoomStatus(roomId: string, status: string) {
    db.prepare('UPDATE rooms SET status = ? WHERE id = ?').run(status, roomId);
  }

  // Guests
  getAllGuests() {
    return db.prepare('SELECT * FROM guests').all();
  }

  saveGuest(guest: { name: string, email: string, phone: string, id_proof: string }) {
    const id = `guest_${Date.now()}`;
    db.prepare('INSERT INTO guests (id, name, email, phone, id_proof, loyalty_points) VALUES (?, ?, ?, ?, ?, ?)').run(
      id, guest.name, guest.email, guest.phone, guest.id_proof, 0
    );
    return id;
  }

  // Reservations
  getAllReservations() {
    return db.prepare(`
      SELECT r.*, g.name as guest_name, rm.room_number 
      FROM reservations r
      JOIN guests g ON r.guest_id = g.id
      JOIN rooms rm ON r.room_id = rm.id
      ORDER BY r.check_in DESC
    `).all();
  }

  saveReservation(res: { guest_id: string, room_id: string, check_in: string, check_out: string }) {
    // Check room availability
    const room = db.prepare('SELECT * FROM rooms WHERE id = ?').get(res.room_id) as any;
    if (!room || room.status !== 'available') {
      throw new Error("RoomNotAvailableError");
    }

    // Calculate nights and total
    const checkInDate = new Date(res.check_in);
    const checkOutDate = new Date(res.check_out);
    const nights = Math.ceil((checkOutDate.getTime() - checkInDate.getTime()) / (1000 * 3600 * 24));
    
    if (nights <= 0) throw new Error("InvalidDateError");
    
    const totalAmount = nights * room.price_per_night;
    const id = `res_${Date.now()}`;

    // Use a transaction
    const transaction = db.transaction(() => {
      db.prepare('INSERT INTO reservations (id, guest_id, room_id, check_in, check_out, status, total_amount) VALUES (?, ?, ?, ?, ?, ?, ?)')
        .run(id, res.guest_id, res.room_id, res.check_in, res.check_out, 'confirmed', totalAmount);
      
      db.prepare("UPDATE rooms SET status = 'occupied' WHERE id = ?").run(res.room_id);
    });
    
    transaction();
    return id;
  }

  deleteReservation(id: string) {
    const res = db.prepare('SELECT room_id FROM reservations WHERE id = ?').get(id) as any;
    if (res) {
      const transaction = db.transaction(() => {
        db.prepare('DELETE FROM reservations WHERE id = ?').run(id);
        db.prepare("UPDATE rooms SET status = 'available' WHERE id = ?").run(res.room_id);
      });
      transaction();
    }
  }

  // Invoices
  getAllInvoices() {
    return db.prepare(`
      SELECT i.*, r.check_in, r.check_out, g.name as guest_name 
      FROM invoices i
      JOIN reservations r ON i.reservation_id = r.id
      JOIN guests g ON r.guest_id = g.id
    `).all();
  }

  generateInvoice(reservationId: string) {
    const existing = db.prepare('SELECT id FROM invoices WHERE reservation_id = ?').get(reservationId) as any;
    if (existing) return existing.id;

    const res = db.prepare('SELECT * FROM reservations WHERE id = ?').get(reservationId) as any;
    if (!res) throw new Error("Reservation not found");

    const subtotal = res.total_amount;
    const tax = subtotal * 0.10; // 10% tax
    const total = subtotal + tax;
    const id = `inv_${Date.now()}`;

    db.prepare('INSERT INTO invoices (id, reservation_id, subtotal, tax, total) VALUES (?, ?, ?, ?, ?)').run(
      id, reservationId, subtotal, tax, total
    );
    return id;
  }
}

export default new DatabaseManager();
