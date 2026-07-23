import streamlit as st
import pandas as pd
from api import list_vouchers, get_voucher, delete_voucher, submit_voucher, approve_voucher, reject_voucher, update_voucher
from components.ui import status_badge, metric_card, render_table

st.set_page_config(page_title="Vouchers", page_icon="📋", layout="wide")

# ── Premium CSS injection ────────────────────────────────────────────
st.markdown("""
    <style>
    .stApp { background: #0a0a0f; }
    .main .block-container { padding: 2rem 2.5rem; max-width: 1400px; }
    div[data-testid="metric-container"] {
        background: #14141f; border: 1px solid rgba(99,102,241,0.1);
        border-radius: 10px; padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 24px rgba(0,0,0,0.12);
    }
    div[data-testid="metric-container"] label {
        color: #94a3b8; font-size: 0.8rem; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        color: #f1f5f9; font-size: 1.75rem; font-weight: 700;
        letter-spacing: -0.02em;
    }
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        border: none !important; border-radius: 10px !important;
        padding: 0.6rem 1.5rem; font-weight: 600;
        letter-spacing: 0.02em; transition: opacity 0.15s ease;
    }
    .stButton button[kind="primary"]:hover { opacity: 0.9; }
    hr { border-color: rgba(99,102,241,0.15); margin: 1.5rem 0; }
    .stSubheader { color: #f1f5f9; font-weight: 600; font-size: 1.15rem; }
    </style>
""", unsafe_allow_html=True)

st.title("📋 Vouchers")
st.markdown('<p style="color: #64748b; margin-top: -0.75rem;">Manage and track expense vouchers</p>', unsafe_allow_html=True)

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
    search = st.text_input("Search", placeholder="Search by title, number, or owner...")
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
    with col1: st.metric("Total Vouchers", total, help="All vouchers in current view")
    with col2: st.metric("Total Amount", f"${total_amount:,.2f}", help="Sum of all voucher amounts")
    with col3: st.metric("Page", f"{pagination.get('page', 1)} of {pagination.get('pages', 1)}", help="Current page")
    with col4: st.metric("Total Records", pagination.get("total", 0), help="Total matching records")

if not vouchers:
    st.info("No vouchers found. Create one from the sidebar!")
    st.stop()

# Voucher cards
for v in vouchers:
    with st.container():
        st.markdown(f"""
            <div style="background: #14141f; border: 1px solid rgba(99,102,241,0.1); border-radius: 10px; padding: 1.25rem; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
                    <div>
                        <strong style="color: #f1f5f9; font-size: 0.95rem;">{v.get('voucherNumber', 'N/A')}</strong>
                        <span style="color: #94a3b8; margin: 0 0.5rem;">—</span>
                        <span style="color: #e2e8f0;">{v.get('expenseTitle', 'Untitled')}</span>
                        <div style="color: #64748b; font-size: 0.8rem; margin-top: 0.25rem;">
                            Owner: {v.get('owner', {}).get('name', 'N/A')} · Dept: {v.get('department', 'N/A')} · Cat: {v.get('category', 'N/A')}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #f1f5f9; font-size: 1.1rem; font-weight: 700;">${float(v.get('amount', 0)):,.2f}</div>
                        <div style="margin-top: 0.25rem;">{status_badge(v.get("status", "DRAFT"))}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        view_key = f"view_{v['id']}"
        edit_key = f"edit_{v['id']}"
        delete_key = f"delete_{v['id']}"
        submit_key = f"submit_{v['id']}"
        approve_key = f"approve_{v['id']}"
        reject_key = f"reject_{v['id']}"
        
        action_cols = st.columns(6)
        with action_cols[0]:
            if st.button("View", key=view_key, help="View details"):
                with st.expander(f"Details — {v.get('voucherNumber', '')}", expanded=True):
                    st.json(v)
        
        if v.get("status") == "DRAFT":
            with action_cols[1]:
                if st.button("Edit", key=edit_key, help="Edit voucher"):
                    st.session_state["edit_voucher"] = v["id"]
                    st.rerun()
            with action_cols[2]:
                if st.button("Delete", key=delete_key, help="Delete voucher"):
                    if delete_voucher(v["id"]):
                        st.success("Voucher deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete voucher.")
        
        if v.get("status") in ("DRAFT", "REJECTED"):
            with action_cols[3]:
                if st.button("Submit", key=submit_key, help="Submit for approval"):
                    result = submit_voucher(v["id"])
                    if result:
                        st.success("Voucher submitted for approval!")
                        st.rerun()
                    else:
                        st.error("Failed to submit.")
        
        if v.get("status") == "PENDING_APPROVAL":
            with action_cols[4]:
                if st.button("Approve", key=approve_key, help="Approve voucher"):
                    result = approve_voucher(v["id"])
                    if result:
                        st.success("Voucher approved!")
                        st.rerun()
                    else:
                        st.error("Failed to approve.")
            with action_cols[5]:
                if st.button("Reject", key=reject_key, help="Reject voucher"):
                    reason = st.text_input("Rejection reason:", key=f"reason_{v['id']}")
                    if reason and st.button("Confirm Reject", key=f"confirm_reject_{v['id']}"):
                        result = reject_voucher(v["id"], reason)
                        if result:
                            st.success("Voucher rejected.")
                            st.rerun()
                        else:
                            st.error("Failed to reject.")
        
        st.divider()
