import streamlit as st
from database.db_manager import DatabaseManager

st.set_page_config(page_title="Invoices", page_icon="🧾", layout="wide")
db = DatabaseManager()

st.title("🧾 Invoices")

invoices = db.get_all_invoices()
if invoices:
    for inv in invoices:
        with st.expander(f"Invoice {inv['id']} — {inv['guest_name']}"):
            col1, col2 = st.columns(2)
            col1.write(f"**Check In:** {inv['check_in']}")
            col2.write(f"**Check Out:** {inv['check_out']}")
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("Subtotal", f"${inv['subtotal']:,.2f}")
            col2.metric("Tax (10%)", f"${inv['tax']:,.2f}")
            col3.metric("Total", f"${inv['total']:,.2f}")

            # Export as .txt
            invoice_text = f"""
GRAND VISTA HOTEL - INVOICE
============================
Invoice ID : {inv['id']}
Guest      : {inv['guest_name']}
Check In   : {inv['check_in']}
Check Out  : {inv['check_out']}
----------------------------
Subtotal   : ${inv['subtotal']:.2f}
Tax (10%)  : ${inv['tax']:.2f}
============================
TOTAL      : ${inv['total']:.2f}
============================
            """
            st.download_button(
                "📥 Export Invoice",
                data=invoice_text,
                file_name=f"{inv['id']}.txt",
                mime="text/plain",
                key=f"dl_{inv['id']}"
            )
else:
    st.info("No invoices yet. Generate one from the Bookings page.")
