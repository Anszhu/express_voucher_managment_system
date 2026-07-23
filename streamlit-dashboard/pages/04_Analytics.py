import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from api import dashboard_stats, list_vouchers
from components.ui import pie_chart, bar_chart, line_chart, metric_card

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

st.title("📈 Analytics Dashboard")

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
col1.metric("Total Vouchers", sum(status_counts.values()))
col2.metric("Total Approved Amount", f"${total_approved:,.2f}")
col3.metric("Pending Approval", status_counts.get("PENDING_APPROVAL", 0))
col4.metric("Rejected", status_counts.get("REJECTED", 0))

st.divider()

# Charts row
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Status distribution pie chart
    if status_counts:
        labels = list(status_counts.keys())
        values = list(status_counts.values())
        fig = pie_chart(labels, values, "Voucher Status Distribution")
        st.plotly_chart(fig, use_container_width=True)

with chart_col2:
    # Department expenses bar chart
    if department_totals:
        sorted_depts = sorted(department_totals.items(), key=lambda x: x[1], reverse=True)
        depts = [d[0] for d in sorted_depts]
        amounts = [d[1] for d in sorted_depts]
        fig = bar_chart(depts, amounts, "Expenses by Department", color="#FF9800")
        st.plotly_chart(fig, use_container_width=True)

st.divider()

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    # Category breakdown
    if category_totals:
        sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        cats = [c[0] for c in sorted_cats[:10]]
        amts = [c[1] for c in sorted_cats[:10]]
        fig = bar_chart(cats, amts, "Top 10 Categories by Amount", color="#2196F3")
        st.plotly_chart(fig, use_container_width=True)

with chart_col4:
    # Status amounts
    if status_amounts:
        labels = list(status_amounts.keys())
        values = list(status_amounts.values())
        fig = pie_chart(labels, values, "Amount by Status")
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

# Approval time trends (if we have data)
st.divider()
st.subheader("Approval Trends")
st.caption("Monthly approval trends based on submitted/approved voucher dates")

# Group by month for trends
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
    submitted_counts = [monthly_data[m]["submitted"] for m in sorted_months]
    approved_counts = [monthly_data[m]["approved"] for m in sorted_months]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sorted_months, y=submitted_counts, mode="lines+markers", name="Submitted", line_color="#2196F3"))
    fig.add_trace(go.Scatter(x=sorted_months, y=approved_counts, mode="lines+markers", name="Approved", line_color="#4CAF50"))
    fig.update_layout(
        title="Monthly Submission & Approval Trends",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Insufficient data for approval trends.")
