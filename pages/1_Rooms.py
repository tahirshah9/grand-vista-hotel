import streamlit as st
from database.db_manager import DatabaseManager

st.set_page_config(page_title="Rooms", page_icon="🛏️", layout="wide")
db = DatabaseManager()

st.title("🛏️ Room Management")

# Filter
room_type = st.selectbox("Filter by Type", ["All", "SingleRoom", "DoubleRoom", "DeluxeRoom", "Suite"])
rooms = db.get_all_rooms()
if room_type != "All":
    rooms = [r for r in rooms if r["type"] == room_type]

# Display rooms as cards in a grid
cols = st.columns(4)
for i, room in enumerate(rooms):
    with cols[i % 4]:
        status_color = "🟢" if room["status"] == "available" else "🔴" if room["status"] == "occupied" else "🟠"
        st.markdown(f"""
        **Room {room['room_number']}**
        {status_color} {room['status'].capitalize()}
        Type: {room['type']}
        Floor: {room['floor']}
        Price: ${room['price_per_night']}/night
        """)
        new_status = st.selectbox(
            "Change Status",
            ["available", "occupied", "maintenance"],
            index=["available", "occupied", "maintenance"].index(room["status"]),
            key=f"status_{room['id']}"
        )
        if st.button("Update", key=f"btn_{room['id']}"):
            db.update_room_status(room["id"], new_status)
            st.rerun()
