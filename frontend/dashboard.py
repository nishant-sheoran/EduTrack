import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# --- Page Config ---
st.set_page_config(
    page_title="Teacher Dashboard - EduTrack",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom Styles ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.6rem;
        font-weight: 800;
        color: #fff;
        text-align: center;
        padding: 1.2rem 0 2rem 0;
        margin-bottom: 0.5rem;
    }
    [data-theme="dark"] .main-header {
        color: #fff;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #fff;
        display: flex;
        align-items: center;
        margin-bottom: 0.7rem;
    }
    [data-theme="dark"] .section-header {
        color: #fff;
    }
    .metric-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 0.2rem;
    }
    [data-theme="dark"] .metric-title {
        color: #bbb;
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 700;
        color: #00e676;
        margin-bottom: 0.1rem;
    }
    .metric-delta-pos {
        font-size: 1rem;
        font-weight: 500;
        color: #00bfae;
    }
    .metric-delta-neg {
        font-size: 1rem;
        font-weight: 500;
        color: #ff1744;
    }
    .metric-caption {
        font-size: 0.95rem;
        color: #999;
        margin-bottom: 0.5rem;
    }
    [data-theme="dark"] .metric-caption {
        color: #bbb;
    }
</style>
""", unsafe_allow_html=True)

# --- Main Header ---
st.markdown('<div class="main-header">EduTrack Teacher Dashboard</div>', unsafe_allow_html=True)

# --- Teacher Inputs ---
col_strength, col_subject = st.columns([1, 2])
with col_strength:
    total_strength = st.number_input("Total Class Strength", min_value=1, max_value=1000, value=30, step=1)
with col_subject:
    subject_name = st.text_input("Subject Being Taught", value="Mathematics")

# --- Generate Sample Data ---
@st.cache_data
def generate_sample_data():
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    engagement_data = pd.DataFrame({
        'Date': dates,
        'Engagement_Score': [random.uniform(60, 95) for _ in range(len(dates))],
        'Attendance': [random.uniform(80, 98) for _ in range(len(dates))]
    })
    topics = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Literature']
    topic_data = pd.DataFrame({
        'Topic': topics,
        'Engagement_Score': [random.uniform(70, 95) for _ in range(len(topics))],
        'Dissociation_Rate': [random.uniform(5, 25) for _ in range(len(topics))]
    })
    return engagement_data, topic_data

engagement_data, topic_data = generate_sample_data()

# --- KPIs Section ---
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.markdown('<div class="section-header"><img src="https://raw.githubusercontent.com/feathericons/feather/master/icons/bar-chart-2.svg" width="26" style="margin-right: 10px;">Attendance Summary</div>', unsafe_allow_html=True)
    st.metric(label="Overall Attendance", value="92.5%", delta="+2.3%")
    st.caption("Based on last 30 days")
with kpi2:
    st.markdown('<div class="section-header"><img src="https://raw.githubusercontent.com/feathericons/feather/master/icons/activity.svg" width="26" style="margin-right: 10px;">Engagement Summary</div>', unsafe_allow_html=True)
    st.metric(label="Average Engagement", value="87.2%", delta="-1.8%")
    st.caption("Real-time tracking")
with kpi3:
    st.markdown('<div class="section-header"><img src="https://raw.githubusercontent.com/feathericons/feather/master/icons/clock.svg" width="26" style="margin-right: 10px;">Latest Session</div>', unsafe_allow_html=True)
    st.metric(label="Session Duration", value="45 min", delta="+5 min")
    st.caption("Current session")

# --- Analytics & Insights ---
st.markdown('<hr style="border: none; height: 32px; background: transparent;">', unsafe_allow_html=True)
st.markdown('<div style="width:100%;height:100%;background:rgba(0,0,0,0.04);border-radius:1.2rem;padding:1.5rem 0 0.5rem 0;margin-bottom:1.5rem;">', unsafe_allow_html=True)
st.markdown('<div class="section-header"><img src="https://raw.githubusercontent.com/feathericons/feather/master/icons/trending-up.svg" width="26" style="margin-right: 10px;">Analytics & Insights</div>', unsafe_allow_html=True)
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.markdown('<div class="metric-title" style="margin-bottom:0.3rem;">Engagement Timeline</div>', unsafe_allow_html=True)
    fig_engagement = px.line(
        engagement_data, 
        x='Date', 
        y='Engagement_Score',
        title=None,
        color_discrete_sequence=['#667eea']
    )
    fig_engagement.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#222'),
        xaxis=dict(gridcolor='#e0e0e0'),
        yaxis=dict(gridcolor='#e0e0e0')
    )
    st.plotly_chart(fig_engagement, use_container_width=True)
with chart_col2:
    st.markdown('<div class="metric-title" style="margin-bottom:0.3rem;">Topic Engagement Analytics</div>', unsafe_allow_html=True)
    fig_topics = px.bar(
        topic_data,
        x='Topic',
        y='Dissociation_Rate',
        title=None,
        color='Engagement_Score',
        color_continuous_scale='RdYlGn_r'
    )
    fig_topics.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#222'),
        xaxis=dict(gridcolor='#e0e0e0'),
        yaxis=dict(gridcolor='#e0e0e0')
    )
    st.plotly_chart(fig_topics, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Media & Documents ---
st.markdown('<hr style="border: none; height: 32px; background: transparent;">', unsafe_allow_html=True)
st.markdown('<div style="width:100%;height:100%;background:rgba(0,0,0,0.04);border-radius:1.2rem;padding:1.5rem 0 0.5rem 0;margin-bottom:1.5rem;">', unsafe_allow_html=True)
st.markdown('<div class="section-header"><img src="https://raw.githubusercontent.com/feathericons/feather/master/icons/video.svg" width="26" style="margin-right: 10px;">Media & Documents</div>', unsafe_allow_html=True)
media_col1, media_col2 = st.columns(2)
with media_col1:
    st.markdown('<div class="metric-title">Latest Video Session</div>', unsafe_allow_html=True)
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    st.video(video_url)
    st.markdown('<div class="metric-title" style="margin-top:0.5rem;">Session Details</div>', unsafe_allow_html=True)
    st.markdown(f"<ul style='margin:0 0 0 1.2rem; padding:0; color:#444; font-size:1rem;'>"
                f"<li><b>Date:</b> {datetime.now().strftime('%B %d, %Y')}</li>"
                f"<li><b>Duration:</b> 45 minutes</li>"
                f"<li><b>Students Present:</b> 28/30</li>"
                f"<li><b>Topics Covered:</b> Advanced Calculus, Linear Algebra</li>"
                f"</ul>", unsafe_allow_html=True)
with media_col2:
    st.markdown('<div class="metric-title">Generated Transcripts</div>', unsafe_allow_html=True)
    transcripts = [
        {"name": "Calculus_Lecture_01.pdf", "date": "2024-01-15", "size": "2.3 MB"},
        {"name": "Linear_Algebra_Session_02.pdf", "date": "2024-01-12", "size": "1.8 MB"},
        {"name": "Differential_Equations_Class.pdf", "date": "2024-01-10", "size": "3.1 MB"},
        {"name": "Vector_Calculus_Review.pdf", "date": "2024-01-08", "size": "2.7 MB"}
    ]
    for transcript in transcripts:
        col_a, col_b, col_c = st.columns([2.5, 1.5, 0.7])
        with col_a:
            st.markdown(f'<span style="font-size:1.05rem; color:#fff;">📄 {transcript["name"]}</span>', unsafe_allow_html=True)
        with col_b:
            st.markdown(f'<span style="color:#bbb;">{transcript["date"]}</span>', unsafe_allow_html=True)
        with col_c:
            st.download_button(
                label="⬇️",
                data=b"Sample PDF content",  # Placeholder
                file_name=transcript['name'],
                mime="application/pdf",
                key=f"download_{transcript['name']}"
            )
st.markdown('</div>', unsafe_allow_html=True)

# --- Configuration & System Health ---
st.markdown('<hr style="border: none; height: 32px; background: transparent;">', unsafe_allow_html=True)
st.markdown('<div style="width:100%;height:100%;background:rgba(0,0,0,0.04);border-radius:1.2rem;padding:1.5rem 0 0.5rem 0;margin-bottom:1.5rem;">', unsafe_allow_html=True)
st.markdown('<div class="section-header"><img src="https://raw.githubusercontent.com/feathericons/feather/master/icons/settings.svg" width="26" style="margin-right: 10px;">Configuration & System</div>', unsafe_allow_html=True)
config_col, sys_col = st.columns(2)
with config_col:
    st.markdown('<div class="metric-title">Configuration Panel</div>', unsafe_allow_html=True)
    video_quality = st.selectbox(
        "Video Quality",
        ["720p", "1080p", "4K"],
        index=1,
        help="Select the preferred video quality for recordings"
    )
    animation_style = st.selectbox(
        "Animation Style",
        ["Smooth", "Fast", "Minimal"],
        index=0,
        help="Choose the animation style for UI transitions"
    )
    sensitivity_threshold = st.slider(
        "Engagement Sensitivity Threshold",
        min_value=0.1,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Adjust the sensitivity for engagement detection"
    )
    auto_save_freq = st.selectbox(
        "Auto-save Frequency",
        ["Every 5 minutes", "Every 10 minutes", "Every 15 minutes", "Manual only"],
        index=1
    )
    if st.button("Save Configuration", type="primary"):
        st.success("Configuration saved successfully!")
with sys_col:
    st.markdown('<div class="metric-title">System Health</div>', unsafe_allow_html=True)
    api_status = random.choice([True, False])
    if api_status:
        st.success("API Connection: Active")
    else:
        st.error("API Connection: Failed")
    disk_usage = random.uniform(60, 85)
    if disk_usage < 70:
        st.success(f"Disk Usage: {disk_usage:.1f}%")
    elif disk_usage < 85:
        st.warning(f"Disk Usage: {disk_usage:.1f}%")
    else:
        st.error(f"Disk Usage: {disk_usage:.1f}%")
    memory_usage = random.uniform(40, 75)
    st.info(f"Memory Usage: {memory_usage:.1f}%")
    st.markdown('<div class="metric-title" style="margin-top:0.7rem;">Recent System Messages</div>', unsafe_allow_html=True)
    system_messages = [
        "Session recording completed successfully",
        "High CPU usage detected during video processing",
        "Transcript generation completed",
        "Backup scheduled for tonight at 2:00 AM"
    ]
    for message in system_messages:
        st.markdown(f"<li style='color:#444; font-size:1rem; margin-left:1.2rem;'>{message}</li>", unsafe_allow_html=True)
    if st.button("🔄 Refresh System Status"):
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #888888; padding: 1rem;'>
        <p>EduTrack Teacher Dashboard | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """,
    unsafe_allow_html=True
) 