import streamlit as st
from database.db_manager import DatabaseManager
from utils.helpers import RoomNotAvailableError, InvalidDateError

st.set_page_config(page_title="Bookings", page_icon="📅", layout="wide")
db = DatabaseManager()

st.title("📅 Bookings Management")

# New Booking Form
st.subheader("New Booking")
guests = db.get_all_guests()
rooms = [r for r in db.get_all_rooms() if r["status"] == "available"]

with st.form("booking_form"):
    guest_options = {g["name"]: g["id"] for g in guests}
    room_options = {f"Room {r['room_number']} ({r['type']}) - ${r['price_per_night']}/night": r["id"] for r in rooms}

    selected_guest = st.selectbox("Select Guest", list(guest_options.keys()))
    selected_room = st.selectbox("Select Room", list(room_options.keys()))
    col1, col2 = st.columns(2)
    check_in = col1.date_input("Check In")
    check_out = col2.date_input("Check Out")
    submitted = st.form_submit_button("Book Now")

    if submitted:
        try:
            db.save_reservation(
                guest_options[selected_guest],
                room_options[selected_room],
                str(check_in),
                str(check_out)
            )
            st.success("Booking confirmed!")
            st.rerun()
        except RoomNotAvailableError:
            st.error("Room is not available!")
        except InvalidDateError:
            st.error("Check-out must be after check-in!")

# Bookings Table
st.subheader("All Bookings")
reservations = db.get_all_reservations()
if reservations:
    for res in reservations:
        with st.expander(f"📋 {res['guest_name']} — Room {res['room_number']} — {res['status'].upper()}"):
            col1, col2, col3 = st.columns(3)
            col1.write(f"**Check In:** {res['check_in']}")
            col2.write(f"**Check Out:** {res['check_out']}")
            col3.write(f"**Total:** ${res['total_amount']:,.2f}")
            bcol1, bcol2 = st.columns(2)
            if bcol1.button("Generate Invoice", key=f"inv_{res['id']}"):
                db.generate_invoice(res["id"])
                st.success("Invoice generated! Go to Invoices page.")
            if bcol2.button("Cancel Booking", key=f"cancel_{res['id']}"):
                db.delete_reservation(res["id"])
                st.warning("Booking cancelled.")
                st.rerun()
else:
    st.info("No bookings yet.")
