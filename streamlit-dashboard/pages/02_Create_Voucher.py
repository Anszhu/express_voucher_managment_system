import streamlit as st
import pandas as pd
from api import create_voucher

st.set_page_config(page_title="Create Voucher", page_icon="➕", layout="wide")

# ── Premium CSS injection ────────────────────────────────────────────
st.markdown("""
    <style>
    .stApp { background: #0a0a0f; }
    .main .block-container { padding: 2rem 2.5rem; max-width: 800px; }
    div[data-testid="metric-container"] {
        background: #14141f; border: 1px solid rgba(99,102,241,0.1);
        border-radius: 10px; padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        border: none !important; border-radius: 10px !important;
        padding: 0.6rem 1.5rem; font-weight: 600;
        letter-spacing: 0.02em; transition: opacity 0.15s ease;
    }
    .stButton button[kind="primary"]:hover { opacity: 0.9; }
    hr { border-color: rgba(99,102,241,0.15); margin: 1.5rem 0; }
    .stForm { background: #14141f; padding: 2rem; border-radius: 14px; border: 1px solid rgba(99,102,241,0.1); }
    </style>
""", unsafe_allow_html=True)

st.title("➕ Create New Voucher")
st.markdown('<p style="color: #64748b; margin-top: -0.75rem;">Submit a new expense voucher for approval</p>', unsafe_allow_html=True)

with st.form("create_voucher_form"):
    col1, col2 = st.columns(2)
    with col1:
        expense_title = st.text_input("Expense Title *", placeholder="e.g. Office Supplies - Stationery")
        category = st.text_input("Category *", placeholder="e.g. Office Supplies")
        department = st.text_input("Department *", placeholder="e.g. Engineering")
        
    with col2:
        amount = st.number_input("Amount ($) *", min_value=0.01, max_value=999999999.0, step=10.0)
        expense_date = st.date_input("Expense Date *", value=pd.Timestamp.now())
        description = st.text_area("Description", placeholder="Optional description of the expense...")
    
    submitted = st.form_submit_button("Create Voucher", type="primary", use_container_width=True)
    
    if submitted:
        if not expense_title or not category or not department:
            st.error("Please fill in all required fields.")
        else:
            data = {
                "expenseTitle": expense_title,
                "category": category,
                "department": department,
                "amount": amount,
                "expenseDate": expense_date.isoformat(),
                "description": description,
            }
            with st.spinner("Creating voucher..."):
                result = create_voucher(data)
                if result:
                    st.success(f"Voucher {result.get('voucherNumber', '')} created successfully!")
                    st.json(result)
                else:
                    st.error("Failed to create voucher. Check your input and try again.")

st.markdown("---")
st.caption("* Required fields")
