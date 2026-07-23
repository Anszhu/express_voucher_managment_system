import streamlit as st
from config import APP_NAME, APP_ICON
from api import login, logout, get_me

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS injection ─────────────────────────────────────────────
def inject_global_css():
    st.markdown("""
        <style>
        /* === DESIGN TOKENS === */
        :root {
            --indigo: #6366F1;
            --indigo-light: #818CF8;
            --indigo-dark: #4F46E5;
            --slate-50: #f8fafc;
            --slate-100: #f1f5f9;
            --slate-200: #e2e8f0;
            --slate-300: #cbd5e1;
            --slate-400: #94a3b8;
            --slate-500: #64748b;
            --slate-600: #475569;
            --slate-700: #334155;
            --slate-800: #1e293b;
            --slate-900: #0f172a;
            --amber: #f59e0b;
            --green: #10b981;
            --red: #ef4444;
            --radius-sm: 6px;
            --radius: 10px;
            --radius-lg: 14px;
            --shadow: 0 2px 8px rgba(0,0,0,0.08);
            --shadow-lg: 0 4px 24px rgba(0,0,0,0.12);
        }

        /* Sidebar */
        .stSidebar {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
            border-right: 1px solid rgba(99,102,241,0.15);
        }
        .stSidebar .sidebar-content {
            padding: 1.5rem 1rem;
        }
        .stSidebar .stMarkdown h3 {
            color: #f1f5f9;
            font-weight: 700;
            font-size: 1.25rem;
            letter-spacing: -0.01em;
        }
        .stSidebar hr {
            border-color: rgba(99,102,241,0.2);
            margin: 1rem 0;
        }
        .stSidebar .stButton button {
            background: transparent;
            border: 1px solid rgba(99,102,241,0.3);
            color: #94a3b8;
            border-radius: var(--radius);
            transition: all 0.2s ease;
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }
        .stSidebar .stButton button:hover {
            background: rgba(99,102,241,0.1);
            border-color: var(--indigo);
            color: #f1f5f9;
        }
        .stSidebar .stLinkButton {
            margin-bottom: 4px;
        }
        .stSidebar .stLinkButton a {
            color: #94a3b8 !important;
            padding: 0.5rem 0.75rem;
            border-radius: var(--radius-sm);
            transition: all 0.15s ease;
            font-size: 0.9rem;
            text-decoration: none !important;
        }
        .stSidebar .stLinkButton a:hover {
            background: rgba(99,102,241,0.08);
            color: #f1f5f9 !important;
        }

        /* Main area */
        .stApp {
            background: #0a0a0f;
        }
        .main .block-container {
            padding: 2rem 2.5rem;
            max-width: 1400px;
        }

        /* Metric cards */
        div[data-testid="metric-container"] {
            background: #14141f;
            border: 1px solid rgba(99,102,241,0.1);
            border-radius: var(--radius);
            padding: 1.25rem;
            box-shadow: var(--shadow);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        div[data-testid="metric-container"] label {
            color: #94a3b8;
            font-size: 0.8rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        div[data-testid="metric-container"] div[data-testid="metric-value"] {
            color: #f1f5f9;
            font-size: 1.75rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        div[data-testid="metric-container"] div[data-testid="metric-delta"] {
            font-size: 0.8rem;
        }

        /* Data editor tables */
        div[data-testid="stDataEditor"] {
            border: 1px solid rgba(99,102,241,0.1);
            border-radius: var(--radius);
            overflow: hidden;
        }

        /* Dividers */
        hr {
            border-color: rgba(99,102,241,0.15);
            margin: 1.5rem 0;
        }

        /* Subheaders */
        .stSubheader {
            color: #f1f5f9;
            font-weight: 600;
            font-size: 1.15rem;
            margin-bottom: 0.5rem;
        }

        /* Login */
        .login-container {
            max-width: 420px;
            margin: 80px auto;
            padding: 2.5rem 2rem;
            background: #14141f;
            border-radius: var(--radius-lg);
            border: 1px solid rgba(99,102,241,0.15);
            box-shadow: var(--shadow-lg);
        }
        .login-title {
            text-align: center;
            margin-bottom: 0.5rem;
            font-size: 1.6rem;
            font-weight: 700;
            color: #f1f5f9;
        }
        .login-subtitle {
            text-align: center;
            color: #64748b;
            margin-bottom: 2rem;
            font-size: 0.9rem;
        }

        /* Buttons */
        .stButton button[kind="primary"] {
            background: linear-gradient(135deg, var(--indigo) 0%, var(--indigo-dark) 100%) !important;
            border: none !important;
            border-radius: var(--radius) !important;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            transition: opacity 0.15s ease;
        }
        .stButton button[kind="primary"]:hover {
            opacity: 0.9;
        }
        </style>
    """, unsafe_allow_html=True)

def check_auth():
    if "user" not in st.session_state:
        st.session_state["user"] = None
        st.session_state["access_token"] = None
        st.session_state["refresh_token"] = None

def show_login():
    inject_global_css()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class="login-container">
                <div class="login-title">{APP_ICON} {APP_NAME}</div>
                <div class="login-subtitle">Sign in to manage expense vouchers</div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="you@company.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")
            submitted = st.form_submit_button("Sign in", use_container_width=True, type="primary")

            if submitted:
                if not email or not password:
                    st.error("Please enter both email and password")
                else:
                    with st.spinner("Authenticating..."):
                        result = login(email, password)
                        if result:
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password. Please try again.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <div style="text-align: center; margin-top: 1.5rem; padding: 1rem; background: #14141f; border-radius: 10px; border: 1px solid rgba(99,102,241,0.1); max-width: 420px; margin-left: auto; margin-right: auto;">
                <p style="color: #64748b; font-size: 0.8rem; margin-bottom: 0.5rem; font-weight: 600;">DEMO CREDENTIALS</p>
                <p style="color: #94a3b8; font-size: 0.8rem; margin: 0.1rem 0;"><span style="color: #818CF8;">employee@example.com</span> / ChangeMe123!</p>
                <p style="color: #94a3b8; font-size: 0.8rem; margin: 0.1rem 0;"><span style="color: #818CF8;">director@example.com</span> / ChangeMe123!</p>
                <p style="color: #94a3b8; font-size: 0.8rem; margin: 0.1rem 0;"><span style="color: #818CF8;">accounts@example.com</span> / ChangeMe123!</p>
            </div>
        """, unsafe_allow_html=True)

def main_app():
    inject_global_css()
    user = st.session_state.get("user", {})
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### {APP_ICON} {APP_NAME}")
        st.markdown("---")
        
        if user:
            st.markdown(f"""
                <div style="padding: 0.75rem; background: rgba(99,102,241,0.06); border-radius: var(--radius-sm); margin-bottom: 1rem;">
                    <div style="font-weight: 600; color: #f1f5f9; font-size: 0.9rem;">👤 {user.get('name', 'User')}</div>
                    <div style="color: #64748b; font-size: 0.8rem;">{user.get('email', '')}</div>
                    <div style="color: #818CF8; font-size: 0.75rem; margin-top: 0.25rem;">{user.get('role', 'N/A')} · {user.get('department', 'N/A')}</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown("---")

        st.page_link("app.py", label="Dashboard", icon="📊")
        st.page_link("pages/01_Vouchers.py", label="Vouchers", icon="📋")
        st.page_link("pages/02_Create_Voucher.py", label="Create Voucher", icon="➕")
        st.page_link("pages/03_Users.py", label="Users", icon="👥")
        st.page_link("pages/04_Analytics.py", label="Analytics", icon="📈")
        st.page_link("pages/05_Health.py", label="API Health", icon="🔌")
        
        st.markdown("---")
        if st.button("Sign Out", use_container_width=True):
            logout()
            st.rerun()

    # Main content area - Dashboard
    st.title("📊 Overview")
    st.markdown('<p style="color: #64748b; margin-top: -0.75rem;">Real-time expense voucher analytics</p>', unsafe_allow_html=True)
    
    from api import dashboard_stats, list_vouchers, list_users
    from components.ui import metric_card, pie_chart, bar_chart
    
    with st.spinner("Loading dashboard data..."):
        stats = dashboard_stats()
        vouchers_data = list_vouchers({"limit": 5})
        users = list_users()
    
    by_status = stats.get("byStatus", [])
    recent = stats.get("recent", [])
    total_approved = float(stats.get("totalApprovedAmount", 0))
    
    status_map = {}
    for s in by_status:
        status_map[s["status"]] = s["_count"]["_all"]
    
    total_vouchers = sum(status_map.values())
    pending = status_map.get("PENDING_APPROVAL", 0)
    approved = status_map.get("APPROVED", 0)
    rejected = status_map.get("REJECTED", 0)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Total Vouchers", total_vouchers, delta="12%", help="All vouchers created")
    with col2: st.metric("Pending Approval", pending, delta="33%", help="Awaiting director approval")
    with col3: st.metric("Approved", approved, delta="5%", help="Successfully approved")
    with col4: st.metric("Rejected", rejected, delta="-8%", help="Rejected vouchers")
    with col5: st.metric("Users", len(users), help="Active system users")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if status_map:
            labels = list(status_map.keys())
            values = list(status_map.values())
            fig = pie_chart(labels, values, "Voucher Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No voucher data available.")
    
    with col2:
        dept_amounts = {}
        for v in vouchers_data.get("items", []):
            dept = v.get("department", "Unknown")
            amt = float(v.get("amount", 0))
            dept_amounts[dept] = dept_amounts.get(dept, 0) + amt
        if dept_amounts:
            sorted_depts = sorted(dept_amounts.items(), key=lambda x: x[1], reverse=True)
            fig = bar_chart(
                [d[0] for d in sorted_depts],
                [d[1] for d in sorted_depts],
                "Expenses by Department",
                color="#6366F1"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No expense data available.")
    
    st.divider()
    
    st.subheader("Recent Activity")
    if recent:
        activity_data = []
        for v in recent:
            activity_data.append({
                "Voucher": v.get("voucherNumber", "N/A"),
                "Title": v.get("expenseTitle", ""),
                "Status": v.get("status", ""),
                "Amount": f"${float(v.get('amount', 0)):,.2f}",
                "Updated": str(v.get("updatedAt", ""))[:16],
                "Owner": v.get("owner", {}).get("name", ""),
            })
        st.data_editor(activity_data, hide_index=True, use_container_width=True, disabled=True)
    else:
        st.info("No recent activity.")
    
    st.metric("Total Approved Amount", f"${total_approved:,.2f}")

def main():
    check_auth()
    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = True
    if not st.session_state.get("access_token"):
        show_login()
    else:
        user = get_me()
        if user:
            st.session_state["user"] = user
            main_app()
        else:
            show_login()

if __name__ == "__main__":
    main()
