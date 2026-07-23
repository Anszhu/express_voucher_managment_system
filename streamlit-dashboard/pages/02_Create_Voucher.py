import streamlit as st
import pandas as pd
from api import create_voucher

st.set_page_config(page_title="Create Voucher", page_icon="➕", layout="wide")

st.title("➕ Create New Voucher")

col1, col2 = st.columns(2)

with st.form("create_voucher_form"):
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
                    st.success(f"✅ Voucher {result.get('voucherNumber', '')} created successfully!")
                    st.json(result)
                else:
                    st.error("Failed to create voucher. Check your input and try again.")

st.markdown("---")
st.caption("* Required fields")
