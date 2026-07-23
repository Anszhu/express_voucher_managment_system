import streamlit as st
from datetime import datetime
from api import health_check, dashboard_stats, list_vouchers

st.set_page_config(page_title="API Health", page_icon="🔌", layout="wide")

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
    .stCodeBlock { background: #14141f !important; border: 1px solid rgba(99,102,241,0.1) !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🔌 API Health Status")
st.markdown('<p style="color: #64748b; margin-top: -0.75rem;">Monitor backend API availability and performance</p>', unsafe_allow_html=True)

# Auto-refresh
auto_refresh = st.checkbox("Auto-refresh (every 10s)", value=False)
if auto_refresh:
    st.rerun()

with st.spinner("Checking API health..."):
    health = health_check()

# Health status card
status_color = "🟢" if health.get("status") == "ok" else "🔴" if health.get("status") == "error" else "⚪"
status_text = health.get("status", "unknown").upper()
border_color = "#10b981" if health.get("status") == "ok" else "#ef4444"

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"""
        <div style="
            padding: 2rem;
            background: #14141f;
            border-radius: 14px;
            border: 2px solid {border_color};
            text-align: center;
        ">
            <div style="font-size: 3rem;">{status_color}</div>
            <div style="font-size: 1.5rem; font-weight: 700; margin-top: 0.5rem; color: #f1f5f9;">{status_text}</div>
            <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">
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
        st.error("API Unreachable - The Express backend does not appear to be running. Please start the backend with `cd backend && npm run dev`.")

st.divider()

# API endpoints status
st.subheader("API Endpoints")
st.caption("All available API endpoints and their current availability")

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
        with col1: st.metric("Total Vouchers", total_vouchers, help="All vouchers in the system")
    except:
        with col1: st.metric("Total Vouchers", "N/A")
    
    try:
        from api import list_users
        users_data = list_users()
        with col2: st.metric("Users", len(users_data) if users_data else "N/A", help="Registered system users")
    except:
        with col2: st.metric("Users", "N/A")
    
    try:
        stats = dashboard_stats()
        total_approved = float(stats.get("totalApprovedAmount", 0))
        with col3: st.metric("Approved Amount", f"${total_approved:,.2f}" if total_approved else "$0", help="Total approved voucher amount")
    except:
        with col3: st.metric("Approved Amount", "N/A")
