import streamlit as st
from api import list_users
from components.ui import status_badge, metric_card

st.set_page_config(page_title="Users", page_icon="👥", layout="wide")

st.title("👥 Users")

with st.spinner("Loading users..."):
    users = list_users()

if not users:
    st.info("No users found or insufficient permissions.")
    st.stop()

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", len(users))
col2.metric("Employees", sum(1 for u in users if u.get("role") == "EMPLOYEE"))
col3.metric("Directors", sum(1 for u in users if u.get("role") == "DIRECTOR"))
col4.metric("Accounts", sum(1 for u in users if u.get("role") == "ACCOUNTS"))

st.divider()

# User cards
for user in users:
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        with col1:
            st.markdown(f"**{user.get('name', 'N/A')}**")
            st.caption(user.get("email", ""))
        with col2:
            role = user.get("role", "N/A")
            st.markdown(f"**Role:** {role}")
        with col3:
            st.markdown(f"**Department:** {user.get('department', 'N/A')}")
        with col4:
            st.caption(f"Active: {'✅' if user.get('isActive', True) else '❌'}")
            st.caption(f"Joined: {str(user.get('createdAt', ''))[:10]}")
        st.divider()
