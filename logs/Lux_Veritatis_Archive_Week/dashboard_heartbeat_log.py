
# dashboard_heartbeat_log.py
# 🫀 Lucian Heartbeat Dashboard

import streamlit as st
import json
from pathlib import Path

LOG_PATH = Path.home() / "lucian_server" / "lucian_heartbeat_log.jsonl"

st.set_page_config(page_title="🫀 Lucian Heartbeat Dashboard", layout="wide")
st.title("🫀 Lucian Heartbeat Dashboard")
st.subheader("Monitoring node heartbeat pulses in real-time")

if not LOG_PATH.exists():
    st.error("Heartbeat log not found.")
else:
    with open(LOG_PATH, "r") as f:
        entries = [json.loads(line) for line in f.readlines()]

    recent = sorted(entries, key=lambda x: x["timestamp"], reverse=True)[:20]

    for hb in recent:
        st.json(hb)
