
# dashboard_echo_log.py
# 📡 Lucian Echo Dashboard

import streamlit as st
import json
from pathlib import Path

LOG_PATH = Path.home() / "lucian_server" / "lucian_echo_log.jsonl"

st.set_page_config(page_title="📡 Lucian Echo Dashboard", layout="wide")
st.title("📡 Lucian Echo Dashboard")
st.subheader("Displaying all node echo confirmations")

if not LOG_PATH.exists():
    st.error("Echo log not found.")
else:
    with open(LOG_PATH, "r") as f:
        entries = [json.loads(line) for line in f.readlines()]

    for entry in entries:
        st.json(entry)
