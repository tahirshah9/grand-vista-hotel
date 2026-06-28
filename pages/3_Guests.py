import streamlit as st
from database.db_manager import DatabaseManager
from utils.helpers import validate_email, validate_phone

st.set_page_config(page_title="Guests", page_icon="👤", layout="wide")
db = DatabaseManager()

st.title("👤 Guest Management")

# Register Guest
st.subheader("Register New Guest")
with st.form("guest_form"):
    col1, col2 = st.columns(2)
    name = col1.text_input("Full Name")
    email = col2.text_input("Email")
    phone = col1.text_input("Phone")
    id_proof = col2.text_input("ID Proof")
    submitted = st.form_submit_button("Register Guest")

    if submitted:
        if not validate_email(email):
            st.error("Invalid email address!")
        elif not validate_phone(phone):
            st.error("Invalid phone number!")
        else:
            try:
                db.save_guest(name, email, phone, id_proof)
                st.success(f"Guest {name} registered successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Guest Table
st.subheader("All Guests")
search = st.text_input("Search by name or email")
guests = db.get_all_guests()
if search:
    guests = [g for g in guests if search.lower() in g["name"].lower() or search.lower() in g["email"].lower()]

if guests:
    import pandas as pd
    df = pd.DataFrame(guests)[["id", "name", "email", "phone", "id_proof", "loyalty_points"]]
    df.columns = ["ID", "Name", "Email", "Phone", "ID Proof", "Loyalty Points"]
    st.dataframe(df, use_container_width=True)
else:
    st.info("No guests found.")
