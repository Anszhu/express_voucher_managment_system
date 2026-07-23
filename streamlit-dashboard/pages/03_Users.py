import streamlit as st
from api import list_users
from components.ui import status_badge, metric_card

st.set_page_config(page_title="Users", page_icon="👥", layout="wide")

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
    hr { border-color: rgba(99,102,241,0.15); margin: 1.5rem 0; }
    .stSubheader { color: #f1f5f9; font-weight: 600; font-size: 1.15rem; }
    </style>
""", unsafe_allow_html=True)

st.title("👥 Users")
st.markdown('<p style="color: #64748b; margin-top: -0.75rem;">Manage system users and roles</p>', unsafe_allow_html=True)

with st.spinner("Loading users..."):
    users = list_users()

if not users:
    st.info("No users found or insufficient permissions.")
    st.stop()

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Users", len(users), help="All registered users")
with col2: st.metric("Employees", sum(1 for u in users if u.get("role") == "EMPLOYEE"), help="Employee role users")
with col3: st.metric("Directors", sum(1 for u in users if u.get("role") == "DIRECTOR"), help="Director role users")
with col4: st.metric("Accounts", sum(1 for u in users if u.get("role") == "ACCOUNTS"), help="Accounts role users")

st.divider()

# User cards
for user in users:
    st.markdown(f"""
        <div style="background: #14141f; border: 1px solid rgba(99,102,241,0.1); border-radius: 10px; padding: 1.25rem; margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
                <div>
                    <strong style="color: #f1f5f9; font-size: 0.95rem;">{user.get('name', 'N/A')}</strong>
                    <div style="color: #64748b; font-size: 0.8rem; margin-top: 0.2rem;">{user.get('email', '')}</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: #818CF8; font-size: 0.85rem; font-weight: 600;">{user.get('role', 'N/A')}</div>
                    <div style="color: #64748b; font-size: 0.8rem; margin-top: 0.2rem;">{user.get('department', 'N/A')}</div>
                </div>
            </div>
            <div style="display: flex; gap: 1.5rem; margin-top: 0.75rem; color: #64748b; font-size: 0.8rem;">
                <span>Active: {'✅' if user.get('isActive', True) else '❌'}</span>
                <span>Joined: {str(user.get('createdAt', ''))[:10]}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
