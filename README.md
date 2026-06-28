# Grand Vista Hotel Booking System

A Python-based desktop application for hotel management, built using strict OOP principles, `customtkinter` for the UI, `sqlite3` for local persistence, and the `google-generativeai` SDK for an integrated AI receptionist.

## Features
- **Dashboard**: High-level overview of hotel stats.
- **Rooms Management**: View and update room status.
- **Bookings**: Manage reservations, check-in, and check-out.
- **Guests**: Register and search for guests.
- **Invoices**: Generate itemized invoices and export to `.txt`.
- **AI Receptionist**: Talk to Aria, an integrated AI assistant aware of real-time hotel context.

## Prerequisites
- Python 3.10+
- A Google Gemini API Key.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   Create a `.env` file in the root directory and add your key:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```
   (You can copy `.env.example` to `.env`)

3. **Run the App**:
   ```bash
   python main.py
   ```

**Note**: This is a desktop application utilizing tkinter. It requires a local display environment (X11/Wayland on Linux, or Windows/macOS window manager). It will not run properly in headless web container environments.
