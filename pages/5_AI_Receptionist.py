import streamlit as st
import os
from ai.gemini_receptionist import GeminiReceptionist
from database.db_manager import DatabaseManager

st.set_page_config(page_title="AI Receptionist", page_icon="🤖", layout="wide")
db = DatabaseManager()

st.title("🤖 Aria — AI Receptionist")
st.caption("Ask Aria anything about rooms, bookings, or hotel policies.")

# Initialize AI and chat history
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

if not api_key:
    st.warning("Please configure your GEMINI_API_KEY in the app settings/secrets to chat with Aria.")
    st.stop()

if "aria" not in st.session_state:
    st.session_state.aria = GeminiReceptionist(api_key)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Hello! I am Aria, your receptionist at Grand Vista Hotel. How can I help you today?"}]

# Display chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
if prompt := st.chat_input("Ask Aria..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    stats = db.get_dashboard_stats()
    context = f"Available Rooms: {stats['available_rooms']}, Active Bookings: {stats['active_bookings']}"

    with st.chat_message("assistant"):
        with st.spinner("Aria is typing..."):
            response = st.session_state.aria.chat(prompt, context)
            st.write(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = [{"role": "assistant", "content": "Hello! I am Aria, your receptionist at Grand Vista Hotel. How can I help you today?"}]
    st.session_state.aria.reset_conversation()
    st.rerun()
