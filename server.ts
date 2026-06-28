import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import dbManager from "./src/server/db.js";
import { chatWithAria, resetConversation } from "./src/server/ai.js";

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // --- API Routes ---

  app.get("/api/dashboard", (req, res) => {
    try {
      const stats = dbManager.getDashboardStats();
      res.json(stats);
    } catch (error) {
      res.status(500).json({ error: String(error) });
    }
  });

  app.get("/api/rooms", (req, res) => {
    try {
      const rooms = dbManager.getAllRooms();
      res.json(rooms);
    } catch (error) {
      res.status(500).json({ error: String(error) });
    }
  });

  app.put("/api/rooms/:id/status", (req, res) => {
    try {
      const { id } = req.params;
      const { status } = req.body;
      dbManager.updateRoomStatus(id, status);
      res.json({ success: true });
    } catch (error) {
      res.status(500).json({ error: String(error) });
    }
  });

  app.get("/api/guests", (req, res) => {
    try {
      const guests = dbManager.getAllGuests();
      res.json(guests);
    } catch (error) {
      res.status(500).json({ error: String(error) });
    }
  });

  app.post("/api/guests", (req, res) => {
    try {
      const { name, email, phone, id_proof } = req.body;
      const guestId = dbManager.saveGuest({ name, email, phone, id_proof });
      res.json({ success: true, guestId });
    } catch (error) {
      res.status(500).json({ error: String(error) });
    }
  });

  app.get("/api/reservations", (req, res) => {
    try {
      const reservations = dbManager.getAllReservations();
      res.json(reservations);
    } catch (error) {
      res.status(500).json({ error: String(error) });
    }
  });

  app.post("/api/reservations", (req, res) => {
    try {
      const { guest_id, room_id, check_in, check_out } = req.body;
      const reservationId = dbManager.saveReservation({ guest_id, room_id, check_in, check_out });
      res.json({ success: true, reservationId });
    } catch (error) {
      res.status(500).json({ error: String(error) });
    }
  });

  app.delete("/api/reservations/:id", (req, res) => {
    try {
      const { id } = req.params;
      dbManager.deleteReservation(id);
      res.json({ success: true });
    } catch (error) {
      res.status(500).json({ error: String(error) });
    }
  });

  app.get("/api/invoices", (req, res) => {
    try {
      const invoices = dbManager.getAllInvoices();
      res.json(invoices);
    } catch (error) {
      res.status(500).json({ error: String(error) });
    }
  });

  app.post("/api/invoices/:reservationId", (req, res) => {
    try {
      const { reservationId } = req.params;
      const invoiceId = dbManager.generateInvoice(reservationId);
      res.json({ success: true, invoiceId });
    } catch (error) {
      res.status(500).json({ error: String(error) });
    }
  });

  // Chat API
  app.post("/api/chat", async (req, res) => {
    try {
      const { message } = req.body;
      const response = await chatWithAria(message);
      res.json({ response });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Failed to communicate with AI Receptionist." });
    }
  });

  app.post("/api/chat/reset", (req, res) => {
    resetConversation();
    res.json({ success: true });
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
