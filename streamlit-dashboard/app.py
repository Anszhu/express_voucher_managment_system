import streamlit as st
from config import APP_NAME, APP_ICON
from api import login, logout, get_me

st.set_page_config(
    page_title=APP_NAME,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

def check_auth():
    if "user" not in st.session_state:
        st.session_state["user"] = None
        st.session_state["access_token"] = None
        st.session_state["refresh_token"] = None

def show_login():
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 2rem;
            background: var(--background-color);
            border-radius: 12px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.12);
        }
        .login-title {
            text-align: center;
            margin-bottom: 2rem;
            font-size: 1.8rem;
            font-weight: 700;
        }
        .login-subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div class="login-container">
                <div class="login-title">{APP_ICON} {APP_NAME}</div>
                <div class="login-subtitle">Sign in to access the admin dashboard</div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email", key="login_email")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")

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
            <div style="text-align: center; margin-top: 2rem; color: #666; font-size: 0.9rem;">
                <p><strong>Demo Credentials:</strong></p>
                <p>Employee: employee@example.com / ChangeMe123!</p>
                <p>Director: director@example.com / ChangeMe123!</p>
                <p>Accounts: accounts@example.com / ChangeMe123!</p>
            </div>
        """, unsafe_allow_html=True)

def main_app():
    user = st.session_state.get("user", {})
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### {APP_ICON} {APP_NAME}")
        st.markdown("---")
        
        if user:
            st.markdown(f"**👤 {user.get('name', 'User')}**")
            st.markdown(f"<small>{user.get('email', '')}</small>", unsafe_allow_html=True)
            st.markdown(f"<small>Role: **{user.get('role', 'N/A')}**</small>", unsafe_allow_html=True)
            st.markdown(f"<small>Department: {user.get('department', 'N/A')}</small>", unsafe_allow_html=True)
            st.markdown("---")

        st.page_link("app.py", label="Dashboard", icon="📊")
        st.page_link("pages/01_Vouchers.py", label="Vouchers", icon="📋")
        st.page_link("pages/02_Create_Voucher.py", label="Create Voucher", icon="➕")
        st.page_link("pages/03_Users.py", label="Users", icon="👥")
        st.page_link("pages/04_Analytics.py", label="Analytics", icon="📈")
        st.page_link("pages/05_Health.py", label="API Health", icon="🔌")
        
        st.markdown("---")
        if st.button("🚪 Sign Out", use_container_width=True):
            logout()
            st.rerun()

    # Main content area - Dashboard
    st.title("📊 Dashboard")
    
    from api import dashboard_stats, list_vouchers, list_users
    from components.ui import metric_card, pie_chart, bar_chart
    
    with st.spinner("Loading dashboard data..."):
        stats = dashboard_stats()
        vouchers_data = list_vouchers({"limit": 5})
        users = list_users()
    
    by_status = stats.get("byStatus", [])
    recent = stats.get("recent", [])
    total_approved = float(stats.get("totalApprovedAmount", 0))
    
    # Compute status counts
    status_map = {}
    for s in by_status:
        status_map[s["status"]] = s["_count"]["_all"]
    
    total_vouchers = sum(status_map.values())
    pending = status_map.get("PENDING_APPROVAL", 0)
    approved = status_map.get("APPROVED", 0)
    rejected = status_map.get("REJECTED", 0)
    drafts = status_map.get("DRAFT", 0)
    
    # Metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Vouchers", total_vouchers)
    col2.metric("Pending Approval", pending)
    col3.metric("Approved", approved)
    col4.metric("Rejected", rejected)
    col5.metric("Total Users", len(users))
    
    st.divider()
    
    # Charts row
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        if status_map:
            labels = list(status_map.keys())
            values = list(status_map.values())
            fig = pie_chart(labels, values, "Voucher Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with chart_col2:
        # Department breakdown from recent vouchers
        dept_amounts = {}
        for v in vouchers_data.get("items", []):
            dept = v.get("department", "Unknown")
            amt = float(v.get("amount", 0))
            dept_amounts[dept] = dept_amounts.get(dept, 0) + amt
        if dept_amounts:
            sorted_depts = sorted(dept_amounts.items(), key=lambda x: x[1], reverse=True)
            fig = bar_chart([d[0] for d in sorted_depts], [d[1] for d in sorted_depts], "Expenses by Department", color="#FF9800")
            st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Recent activity
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
    
    # Total approved amount
    st.metric("Total Approved Amount", f"${total_approved:,.2f}")

def main():
    check_auth()

    # Apply dark mode if set
    if "dark_mode" not in st.session_state:
        st.session_state["dark_mode"] = True

    if not st.session_state.get("access_token"):
        show_login()
    else:
        # Verify token is still valid
        user = get_me()
        if user:
            st.session_state["user"] = user
            main_app()
        else:
            show_login()

if __name__ == "__main__":
    main()
