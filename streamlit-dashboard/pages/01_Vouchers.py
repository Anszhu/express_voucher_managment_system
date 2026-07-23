import streamlit as st
import pandas as pd
from api import list_vouchers, get_voucher, delete_voucher, submit_voucher, approve_voucher, reject_voucher, update_voucher
from components.ui import status_badge, metric_card, render_table

st.set_page_config(page_title="Vouchers", page_icon="📋", layout="wide")

st.title("📋 Vouchers")

# Action handling from session state
if "edit_voucher" in st.session_state:
    voucher_id = st.session_state.pop("edit_voucher")
    voucher = get_voucher(voucher_id)
    if voucher:
        st.info(f"Editing voucher: {voucher.get('voucherNumber', voucher_id)}")
        with st.form("edit_voucher_form"):
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Expense Title", value=voucher.get("expenseTitle", ""))
                category = st.text_input("Category", value=voucher.get("category", ""))
                department = st.text_input("Department", value=voucher.get("department", ""))
            with col2:
                amount = st.number_input("Amount", min_value=0.01, max_value=999999999.0, value=float(voucher.get("amount", 0)))
                expense_date = st.date_input("Expense Date", value=pd.to_datetime(voucher.get("expenseDate", "today")).date())
                description = st.text_area("Description", value=voucher.get("description", ""))
            
            submitted = st.form_submit_button("Update Voucher", type="primary")
            if submitted:
                data = {
                    "expenseTitle": title,
                    "category": category,
                    "department": department,
                    "amount": amount,
                    "expenseDate": expense_date.isoformat(),
                    "description": description,
                }
                result = update_voucher(voucher_id, data)
                if result:
                    st.success("Voucher updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update voucher.")
        st.divider()
        if st.button("← Back to vouchers"):
            st.rerun()
        st.stop()

# Search and filter
col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col1:
    search = st.text_input("🔍 Search", placeholder="Search by title, number, or owner...")
with col2:
    status_filter = st.selectbox("Status", ["All", "DRAFT", "SUBMITTED", "PENDING_APPROVAL", "APPROVED", "REJECTED"])
with col3:
    department_filter = st.text_input("Department", placeholder="Filter by dept")
with col4:
    category_filter = st.text_input("Category", placeholder="Filter by category")

params = {"limit": 50}
if search:
    params["search"] = search
if status_filter != "All":
    params["status"] = status_filter
if department_filter:
    params["department"] = department_filter
if category_filter:
    params["category"] = category_filter

with st.spinner("Loading vouchers..."):
    data = list_vouchers(params)

vouchers = data.get("items", [])
pagination = data.get("pagination", {})

# Summary stats
if vouchers:
    total = len(vouchers)
    total_amount = sum(float(v.get("amount", 0)) for v in vouchers)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Vouchers", total)
    col2.metric("Total Amount", f"${total_amount:,.2f}")
    col3.metric("Page", f"{pagination.get('page', 1)} of {pagination.get('pages', 1)}")
    col4.metric("Total Records", pagination.get("total", 0))

if not vouchers:
    st.info("No vouchers found. Create one from the sidebar!")
    st.stop()

# Voucher cards
for v in vouchers:
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 2])
        with col1:
            st.markdown(f"**{v.get('voucherNumber', 'N/A')}** — {v.get('expenseTitle', 'Untitled')}")
            st.caption(f"Owner: {v.get('owner', {}).get('name', 'N/A')} | Dept: {v.get('department', 'N/A')}")
        with col2:
            st.markdown(f"**${float(v.get('amount', 0)):,.2f}**")
            st.caption(f"Category: {v.get('category', 'N/A')}")
        with col3:
            st.markdown(status_badge(v.get("status", "DRAFT")), unsafe_allow_html=True)
            st.caption(f"Date: {v.get('expenseDate', 'N/A')[:10] if v.get('expenseDate') else 'N/A'}")
        with col4:
            st.markdown(f"**${float(v.get('amount', 0)):,.2f}**")
        with col5:
            view_key = f"view_{v['id']}"
            edit_key = f"edit_{v['id']}"
            delete_key = f"delete_{v['id']}"
            submit_key = f"submit_{v['id']}"
            approve_key = f"approve_{v['id']}"
            reject_key = f"reject_{v['id']}"
            
            action_cols = st.columns(4)
            with action_cols[0]:
                if st.button("👁️", key=view_key, help="View details"):
                    with st.expander(f"Details — {v.get('voucherNumber', '')}", expanded=True):
                        st.json(v)
            
            if v.get("status") == "DRAFT":
                with action_cols[1]:
                    if st.button("✏️", key=edit_key, help="Edit"):
                        st.session_state["edit_voucher"] = v["id"]
                        st.rerun()
                with action_cols[2]:
                    if st.button("🗑️", key=delete_key, help="Delete"):
                        if delete_voucher(v["id"]):
                            st.success("Voucher deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete voucher.")
            
            if v.get("status") in ("DRAFT", "REJECTED"):
                with action_cols[3]:
                    if st.button("📤", key=submit_key, help="Submit for approval"):
                        result = submit_voucher(v["id"])
                        if result:
                            st.success("Voucher submitted for approval!")
                            st.rerun()
                        else:
                            st.error("Failed to submit.")
            
            if v.get("status") == "PENDING_APPROVAL":
                with action_cols[1]:
                    if st.button("✅", key=approve_key, help="Approve"):
                        result = approve_voucher(v["id"])
                        if result:
                            st.success("Voucher approved!")
                            st.rerun()
                        else:
                            st.error("Failed to approve.")
                with action_cols[2]:
                    if st.button("❌", key=reject_key, help="Reject"):
                        reason = st.text_input("Rejection reason:", key=f"reason_{v['id']}")
                        if reason and st.button("Confirm Reject", key=f"confirm_reject_{v['id']}"):
                            result = reject_voucher(v["id"], reason)
                            if result:
                                st.success("Voucher rejected.")
                                st.rerun()
                            else:
                                st.error("Failed to reject.")
        
        st.divider()
