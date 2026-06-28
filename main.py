import streamlit as st
from database.db_manager import DatabaseManager

st.set_page_config(
    page_title="Grand Vista Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

db = DatabaseManager()

st.title("🏨 Grand Vista Hotel")
st.markdown("### Management Dashboard")

stats = db.get_dashboard_stats()

col1, col2, col3, col4 = st.columns(4)
col1.metric("🛏️ Total Rooms", stats["total_rooms"])
col2.metric("✅ Available Rooms", stats["available_rooms"])
col3.metric("📅 Active Bookings", stats["active_bookings"])
col4.metric("💰 Total Revenue", f"${stats['today_revenue']:,.2f}")
