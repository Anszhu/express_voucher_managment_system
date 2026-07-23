import streamlit as st
import plotly.graph_objects as go
from api import dashboard_stats, list_vouchers
from components.ui import pie_chart, bar_chart, line_chart, metric_card

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

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

st.title("📈 Analytics Dashboard")
st.markdown('<p style="color: #64748b; margin-top: -0.75rem;">Deep insights into expense voucher data</p>', unsafe_allow_html=True)

with st.spinner("Loading analytics data..."):
    stats = dashboard_stats()
    all_vouchers = list_vouchers({"limit": 200})

by_status = stats.get("byStatus", [])
recent = stats.get("recent", [])
total_approved = float(stats.get("totalApprovedAmount", 0))

# Compute derived stats
status_counts = {}
status_amounts = {}
department_totals = {}
category_totals = {}

vouchers_list = all_vouchers.get("items", [])
for v in vouchers_list:
    s = v.get("status", "UNKNOWN")
    status_counts[s] = status_counts.get(s, 0) + 1
    amt = float(v.get("amount", 0))
    status_amounts[s] = status_amounts.get(s, 0) + amt
    
    dept = v.get("department", "Unknown")
    department_totals[dept] = department_totals.get(dept, 0) + amt
    
    cat = v.get("category", "Unknown")
    category_totals[cat] = category_totals.get(cat, 0) + amt

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Vouchers", sum(status_counts.values()), help="All vouchers in system")
with col2: st.metric("Total Approved Amount", f"${total_approved:,.2f}", help="Sum of approved voucher amounts")
with col3: st.metric("Pending Approval", status_counts.get("PENDING_APPROVAL", 0), help="Awaiting director review")
with col4: st.metric("Rejected", status_counts.get("REJECTED", 0), help="Vouchers not approved")

st.divider()

# Charts row
col1, col2 = st.columns(2)

with col1:
    if status_counts:
        fig = pie_chart(list(status_counts.keys()), list(status_counts.values()), "Voucher Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available.")

with col2:
    if department_totals:
        sorted_depts = sorted(department_totals.items(), key=lambda x: x[1], reverse=True)
        fig = bar_chart([d[0] for d in sorted_depts], [d[1] for d in sorted_depts], "Expenses by Department", color="#6366F1")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available.")

st.divider()

col3, col4 = st.columns(2)

with col3:
    if category_totals:
        sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:10]
        fig = bar_chart([c[0] for c in sorted_cats], [c[1] for c in sorted_cats], "Top 10 Categories by Amount", color="#f59e0b")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available.")

with col4:
    if status_amounts:
        fig = pie_chart(list(status_amounts.keys()), list(status_amounts.values()), "Amount by Status")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available.")

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

# Approval time trends
st.divider()
st.subheader("Approval Trends")
st.caption("Monthly submission and approval patterns")

monthly_data = {}
for v in vouchers_list:
    if v.get("submittedAt"):
        month = str(v["submittedAt"])[:7]
        if month not in monthly_data:
            monthly_data[month] = {"submitted": 0, "approved": 0, "rejected": 0}
        monthly_data[month]["submitted"] += 1
        if v.get("status") == "APPROVED":
            monthly_data[month]["approved"] += 1
        elif v.get("status") == "REJECTED":
            monthly_data[month]["rejected"] += 1

if monthly_data:
    sorted_months = sorted(monthly_data.keys())
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sorted_months, y=[monthly_data[m]["submitted"] for m in sorted_months], mode="lines+markers", name="Submitted", line=dict(color="#6366F1", width=2), marker=dict(color="#6366F1", size=6)))
    fig.add_trace(go.Scatter(x=sorted_months, y=[monthly_data[m]["approved"] for m in sorted_months], mode="lines+markers", name="Approved", line=dict(color="#10b981", width=2), marker=dict(color="#10b981", size=6)))
    fig.update_layout(
        title="Monthly Submission & Approval Trends",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        legend=dict(font=dict(color="#94a3b8")),
        xaxis=dict(gridcolor="rgba(99,102,241,0.05)"),
        yaxis=dict(gridcolor="rgba(99,102,241,0.05)"),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Insufficient data for approval trends.")
