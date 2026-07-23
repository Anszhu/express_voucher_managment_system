import streamlit as st
import plotly.graph_objects as go
from typing import List, Optional

def metric_card(label: str, value, delta: Optional[str] = None, help_text: Optional[str] = None):
    """Display a styled metric card with premium design."""
    delta_color = "#10b981" if delta and not delta.startswith("-") else "#ef4444"
    st.markdown(f"""
        <div style="
            padding: 1.25rem;
            background: #14141f;
            border-radius: 10px;
            border: 1px solid rgba(99,102,241,0.1);
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        ">
            <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 500;">{label}</div>
            <div style="font-size: 1.75rem; font-weight: 700; color: #f1f5f9; letter-spacing: -0.02em;">{value}</div>
            {f'<div style="font-size: 0.8rem; color: {delta_color}; margin-top: 0.25rem; font-weight: 500;">{delta}</div>' if delta else ''}
        </div>
    """, unsafe_allow_html=True)
    if help_text:
        st.caption(help_text)

def status_badge(status: str) -> str:
    """Return HTML for a premium status badge."""
    colors = {
        "DRAFT": "#94a3b8",
        "SUBMITTED": "#6366F1",
        "PENDING_APPROVAL": "#f59e0b",
        "APPROVED": "#10b981",
        "REJECTED": "#ef4444",
    }
    color = colors.get(status.upper(), "#94a3b8")
    return f'<span style="background: {color}15; color: {color}; padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.02em; border: 1px solid {color}30;">{status.replace("_", " ").title()}</span>'

def render_table(data: List[dict], columns: List[str], column_map: Optional[dict] = None):
    """Render a styled data table with premium look."""
    if not data:
        st.info("No data available.")
        return
    
    df_data = []
    for item in data:
        row = {}
        for col in columns:
            key = column_map.get(col, col) if column_map else col
            val = item.get(key, "")
            if key == "status":
                row[col] = status_badge(val)
            elif key == "amount":
                try:
                    row[col] = f"${float(val):,.2f}"
                except:
                    row[col] = val
            else:
                row[col] = val
        df_data.append(row)
    
    st.data_editor(
        df_data,
        column_config={col: st.column_config.TextColumn(col, width="medium") for col in columns},
        hide_index=True,
        use_container_width=True,
        disabled=True,
    )

def pie_chart(labels: List[str], values: List[float], title: str = "") -> go.Figure:
    """Create a styled pie chart with premium palette."""
    colors = ["#6366F1", "#f59e0b", "#10b981", "#ef4444", "#94a3b8"]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors[:len(labels)], textfont_color="#f1f5f9")])
    fig.update_layout(
        title=dict(text=title, font=dict(color="#f1f5f9", size=14)),
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        legend=dict(font=dict(color="#94a3b8")),
    )
    return fig

def bar_chart(x: List[str], y: List[float], title: str = "", color: str = "#6366F1") -> go.Figure:
    """Create a styled bar chart with premium look."""
    fig = go.Figure(data=[go.Bar(x=x, y=y, marker_color=color, marker_line_color=color, marker_line_width=0)])
    fig.update_layout(
        title=dict(text=title, font=dict(color="#f1f5f9", size=14)),
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        xaxis=dict(tickangle=-45, gridcolor="rgba(99,102,241,0.05)"),
        yaxis=dict(gridcolor="rgba(99,102,241,0.05)"),
    )
    return fig

def line_chart(x: List[str], y: List[float], title: str = "", color: str = "#6366F1") -> go.Figure:
    """Create a styled line chart with premium look."""
    fig = go.Figure(data=[go.Scatter(x=x, y=y, mode="lines+markers", marker=dict(color=color, size=6), line=dict(color=color, width=2))])
    fig.update_layout(
        title=dict(text=title, font=dict(color="#f1f5f9", size=14)),
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8"),
        xaxis=dict(gridcolor="rgba(99,102,241,0.05)"),
        yaxis=dict(gridcolor="rgba(99,102,241,0.05)"),
    )
    return fig

def confirm_dialog(key: str, title: str, message: str) -> bool:
    """Show a premium confirmation dialog."""
    with st.popover(title, use_container_width=True):
        st.warning(message)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirm", key=f"confirm_{key}", type="primary", use_container_width=True):
                return True
        with col2:
            if st.button("Cancel", key=f"cancel_{key}", use_container_width=True):
                return False
    return False
