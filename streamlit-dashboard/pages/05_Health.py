import streamlit as st
import json
from datetime import datetime
from api import health_check, dashboard_stats, list_vouchers

st.set_page_config(page_title="API Health", page_icon="🔌", layout="wide")

st.title("🔌 API Health Status")

# Auto-refresh
auto_refresh = st.checkbox("Auto-refresh (every 10s)", value=False)
if auto_refresh:
    st.rerun()

with st.spinner("Checking API health..."):
    health = health_check()

# Health status card
status_color = "🟢" if health.get("status") == "ok" else "🔴" if health.get("status") == "error" else "⚪"
status_text = health.get("status", "unknown").upper()

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"""
        <div style="
            padding: 2rem;
            background: var(--background-color);
            border-radius: 12px;
            border: 2px solid {'#4CAF50' if health.get('status') == 'ok' else '#F44336'};
            text-align: center;
        ">
            <div style="font-size: 3rem;">{status_color}</div>
            <div style="font-size: 1.5rem; font-weight: 700; margin-top: 0.5rem;">{status_text}</div>
            <div style="font-size: 0.85rem; color: #888; margin-top: 0.5rem;">
                Last checked: {datetime.now().strftime('%H:%M:%S')}
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if health.get("status") != "unreachable":
        st.json({
            "status": health.get("status"),
            "environment": health.get("environment"),
            "version": health.get("version"),
            "uptime": f"{health.get('uptimeSeconds', 0):.2f}s",
            "timestamp": health.get("timestamp"),
            "requestId": health.get("requestId"),
        })
    else:
        st.error("""
            ## API Unreachable
            
            The Express backend does not appear to be running.
            
            **Please start the backend:**
            
```bash
            cd backend
            npm run dev
            
```
            
            Expected API URL: http://localhost:4000
        """)

st.divider()

# API endpoints status
st.subheader("API Endpoints")

endpoints = [
    ("GET /api/v1/auth/login", "Authentication"),
    ("POST /api/v1/auth/refresh", "Token Refresh"),
    ("GET /api/v1/auth/me", "Current User"),
    ("GET /api/v1/vouchers", "List Vouchers"),
    ("POST /api/v1/vouchers", "Create Voucher"),
    ("GET /api/v1/vouchers/dashboard", "Dashboard Stats"),
    ("GET /api/v1/users", "List Users"),
    ("GET /api-docs", "Swagger Documentation"),
    ("GET /health", "Health Check"),
    ("GET /live", "Liveness Probe"),
    ("GET /ready", "Readiness Probe"),
    ("GET /metrics", "Prometheus Metrics"),
]

endpoint_data = []
for endpoint, desc in endpoints:
    endpoint_data.append({
        "Endpoint": endpoint,
        "Description": desc,
        "Status": "✅ Available" if health.get("status") != "unreachable" else "❌ Unavailable",
    })

st.data_editor(endpoint_data, hide_index=True, use_container_width=True, disabled=True)

st.divider()

# Quick stats if API is reachable
if health.get("status") != "unreachable":
    st.subheader("Quick System Stats")
    col1, col2, col3 = st.columns(3)
    
    try:
        vouchers_data = list_vouchers({"limit": 1})
        total_vouchers = vouchers_data.get("pagination", {}).get("total", 0)
        col1.metric("Total Vouchers", total_vouchers)
    except:
        col1.metric("Total Vouchers", "N/A")
    
    try:
        from api import list_users
        users_data = list_users()
        col2.metric("Users", len(users_data) if users_data else "N/A")
    except:
        col2.metric("Users", "N/A")
    
    try:
        stats = dashboard_stats()
        total_approved = float(stats.get("totalApprovedAmount", 0))
        col3.metric("Approved Amount", f"${total_approved:,.2f}" if total_approved else "$0")
    except:
        col3.metric("Approved Amount", "N/A")
