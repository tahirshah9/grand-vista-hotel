import { GoogleGenAI } from "@google/genai";
import dbManager from "./db.js";

const apiKey = process.env.GEMINI_API_KEY;
const ai = new GoogleGenAI({ apiKey });

let conversationHistory: any[] = [];

export async function chatWithAria(userMessage: string) {
  if (!apiKey) {
    return "API Key not configured. Please add GEMINI_API_KEY in the Secrets panel.";
  }

  // Get current hotel context
  const availableRooms = dbManager.getAllRooms().filter((r: any) => r.status === 'available');
  const activeBookings = dbManager.getAllReservations().filter((r: any) => r.status === 'confirmed');

  const contextStr = `
    Current Hotel Context:
    - Available Rooms: ${availableRooms.length}
    - Active Bookings: ${activeBookings.length}
  `;

  const systemPrompt = `
    You are Aria, a professional, polite, and helpful hotel receptionist at Grand Vista Hotel.
    You assist staff and guests with room availability and bookings.
    Keep your answers concise and professional.
    ${contextStr}
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: [
        { role: "user", parts: [{ text: systemPrompt }] },
        { role: "model", parts: [{ text: "Understood. I am Aria, ready to assist." }] },
        ...conversationHistory,
        { role: "user", parts: [{ text: userMessage }] }
      ]
    });

    const text = response.text || "I'm sorry, I couldn't process that.";
    
    // Save to history
    conversationHistory.push({ role: "user", parts: [{ text: userMessage }] });
    conversationHistory.push({ role: "model", parts: [{ text }] });

    return text;
  } catch (error) {
    console.error("Gemini API Error:", error);
    return "I'm sorry, I'm having trouble connecting to my systems right now. (API Error)";
  }
}

export function resetConversation() {
  conversationHistory = [];
}
