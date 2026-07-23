import streamlit as st
import plotly.graph_objects as go
from typing import List, Tuple, Optional

def metric_card(label: str, value, delta: Optional[str] = None, help_text: Optional[str] = None):
    """Display a styled metric card."""
    st.markdown(f"""
        <div style="
            padding: 1.2rem;
            background: var(--background-color);
            border-radius: 10px;
            border: 1px solid rgba(128, 128, 128, 0.2);
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
        ">
            <div style="font-size: 0.85rem; color: #888; margin-bottom: 0.4rem;">{label}</div>
            <div style="font-size: 1.8rem; font-weight: 700;">{value}</div>
            {f'<div style="font-size: 0.85rem; color: #4CAF50; margin-top: 0.2rem;">{delta}</div>' if delta else ''}
        </div>
    """, unsafe_allow_html=True)
    if help_text:
        st.caption(help_text)

def status_badge(status: str) -> str:
    """Return HTML for a status badge."""
    colors = {
        "DRAFT": "#9E9E9E",
        "SUBMITTED": "#2196F3",
        "PENDING_APPROVAL": "#FF9800",
        "APPROVED": "#4CAF50",
        "REJECTED": "#F44336",
    }
    color = colors.get(status.upper(), "#9E9E9E")
    return f'<span style="background: {color}20; color: {color}; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">{status}</span>'

def render_table(data: List[dict], columns: List[str], column_map: Optional[dict] = None):
    """Render a styled data table."""
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
                row[col] = val
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
    """Create a styled pie chart."""
    colors = ["#4CAF50", "#FF9800", "#2196F3", "#F44336", "#9E9E9E"]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors[:len(labels)])])
    fig.update_layout(
        title=title,
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#888",
    )
    return fig

def bar_chart(x: List[str], y: List[float], title: str = "", color: str = "#4CAF50") -> go.Figure:
    """Create a styled bar chart."""
    fig = go.Figure(data=[go.Bar(x=x, y=y, marker_color=color)])
    fig.update_layout(
        title=title,
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#888",
        xaxis_tickangle=-45,
    )
    return fig

def line_chart(x: List[str], y: List[float], title: str = "", color: str = "#2196F3") -> go.Figure:
    """Create a styled line chart."""
    fig = go.Figure(data=[go.Scatter(x=x, y=y, mode="lines+markers", marker_color=color, line_color=color)])
    fig.update_layout(
        title=title,
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#888",
    )
    return fig

def confirm_dialog(key: str, title: str, message: str) -> bool:
    """Show a confirmation dialog."""
    with st.popover(title, use_container_width=True):
        st.warning(message)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm", key=f"confirm_{key}", type="primary"):
                return True
        with col2:
            if st.button("❌ Cancel", key=f"cancel_{key}"):
                return False
    return False
