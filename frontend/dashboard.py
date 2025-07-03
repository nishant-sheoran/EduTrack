import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import random
import plotly.express as px
import plotly.graph_objects as go

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
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #fff;
        display: flex;
        align-items: center;
        margin-bottom: 0.7rem;
    }
    .metric-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #fff;
        margin-bottom: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Main Header ---
st.markdown('<div class="main-header">EduTrack Teacher Dashboard</div>', unsafe_allow_html=True)

# --- Debug Toggle ---
debug = st.sidebar.checkbox("Show debug info (for backend engineers)")

# --- Teacher Inputs ---
col_strength, col_subject = st.columns([1, 2])
with col_strength:
    total_strength = st.number_input("Total Class Strength", min_value=1, max_value=1000, value=30, step=1)
with col_subject:
    subject_name = st.text_input("Subject Being Taught", value="Mathematics")

# --- API Helper with Error Handling ---
def fetch_api(url, description, params=None):
    try:
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code == 200:
            try:
                return resp.json()
            except Exception as e:
                st.error(f"{description}: Invalid JSON response.")
                if debug:
                    st.exception(e)
        else:
            st.error(f"{description}: Backend returned status {resp.status_code}")
            if debug:
                st.text(resp.text)
    except requests.exceptions.Timeout:
        st.error(f"{description}: Request timed out.")
    except requests.exceptions.ConnectionError:
        st.error(f"{description}: Could not connect to backend.")
    except Exception as e:
        st.error(f"{description}: Unexpected error.")
        if debug:
            st.exception(e)
    return None

# --- Real-time Attendance & Engagement ---
st.markdown('<div class="section-header"><img src="https://raw.githubusercontent.com/feathericons/feather/master/icons/bar-chart-2.svg" width="26" style="margin-right: 10px;"> Real-time Attendance & Engagement</div>', unsafe_allow_html=True)

realtime_data = fetch_api(
    url="http://localhost:8000/api/classroom/realtime",
    description="Real-time Attendance & Engagement",
    params={"subject": subject_name}
)

engagement_df = None

if realtime_data:
    present_ids = realtime_data.get('present_ids', [])
    engagement = realtime_data.get('engagement', [])
    emotions = realtime_data.get('emotions', [])
    attendance_pct = len(present_ids) / total_strength * 100 if total_strength else 0
    engaged_count = sum(1 for e in engagement if e['engagement'] == 'Engaged')
    engagement_pct = engaged_count / len(present_ids) * 100 if present_ids else 0
    engagement_df = pd.DataFrame(engagement)

    kpi1, kpi2 = st.columns(2)
    with kpi1:
        st.metric('Attendance', f'{attendance_pct:.1f}%')
    with kpi2:
        st.metric('Engagement', f'{engagement_pct:.1f}%')

    # --- Engagement Gauge ---
    st.markdown("### 🧭 Engagement Level Gauge")
    gauge_fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = engagement_pct,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Engagement %"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#00e676"},
            'steps': [
                {'range': [0, 50], 'color': '#ff1744'},
                {'range': [50, 100], 'color': '#00bfae'}
            ]
        }
    ))
    st.plotly_chart(gauge_fig, use_container_width=True)

    # --- Emotion Bar Chart ---
    if emotions:
        st.markdown("### 😊 Emotion Distribution")
        emotion_df = pd.DataFrame(emotions)
        fig_emotions = px.bar(emotion_df, x='emotion', y='count', color='emotion', title='Student Emotions')
        st.plotly_chart(fig_emotions, use_container_width=True)

    # --- Live Table ---
    st.markdown("### 🧾 Live Engagement Table")
    st.dataframe(engagement_df)
else:
    st.info("Waiting for real-time data from backend...")

# --- Resources: Transcripts & Remedial Videos ---
st.markdown('<div class="section-header"><img src="https://raw.githubusercontent.com/feathericons/feather/master/icons/video.svg" width="26" style="margin-right: 10px;"> Media & Documents</div>', unsafe_allow_html=True)

resources = fetch_api(
    url="http://localhost:8000/api/classroom/resources",
    description="Transcripts & Remedial Videos",
    params={"subject": subject_name}
) or {"transcripts": [], "remedial_videos": []}

media_col1, media_col2 = st.columns(2)
with media_col1:
    st.markdown('<div class="metric-title">Transcripts</div>', unsafe_allow_html=True)
    for t in resources.get('transcripts', []):
        try:
            file_bytes = requests.get(t['url'], timeout=5).content
            st.download_button(label=f'⬇️ {t["name"]}', data=file_bytes, file_name=t['name'])
        except Exception as e:
            st.warning(f"Could not download {t['name']}")
            if debug:
                st.exception(e)
with media_col2:
    st.markdown('<div class="metric-title">Remedial Videos</div>', unsafe_allow_html=True)
    for v in resources.get('remedial_videos', []):
        try:
            file_bytes = requests.get(v['url'], timeout=5).content
            st.download_button(label=f'⬇️ {v["topic"]} Video', data=file_bytes, file_name=f'{v["topic"]}.mp4')
        except Exception as e:
            st.warning(f"Could not download {v['topic']} video")
            if debug:
                st.exception(e)

# --- System Health Simulation ---
st.markdown('<div class="section-header"><img src="https://raw.githubusercontent.com/feathericons/feather/master/icons/settings.svg" width="26" style="margin-right: 10px;"> System Health</div>', unsafe_allow_html=True)
sys_col1, sys_col2 = st.columns(2)
with sys_col1:
    api_status = random.choice([True, False])
    if api_status:
        st.success("API Connection: Active")
    else:
        st.error("API Connection: Failed")
with sys_col2:
    disk_usage = random.uniform(60, 85)
    if disk_usage < 70:
        st.success(f"Disk Usage: {disk_usage:.1f}%")
    elif disk_usage < 85:
        st.warning(f"Disk Usage: {disk_usage:.1f}%")
    else:
        st.error(f"Disk Usage: {disk_usage:.1f}%")
    memory_usage = random.uniform(40, 75)
    st.info(f"Memory Usage: {memory_usage:.1f}%")
    system_messages = [
        "Session recording completed successfully",
        "Transcript generation completed",
        "High CPU usage detected during video processing",
        "Backup scheduled for tonight at 2:00 AM"
    ]
    for msg in system_messages:
        st.markdown(f"- {msg}")
    if st.button("🔄 Refresh System Status"):
        st.rerun()

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