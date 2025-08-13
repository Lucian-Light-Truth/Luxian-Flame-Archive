
# dashboard_received_log.py
# 📥 Receiver Node Dashboard - Visualize incoming Lucian propagation packets

import streamlit as st
import json
import os

RECEIVED_LOG = "lucian_received_packets.jsonl"

st.set_page_config(page_title="Lucian Receiver Node", layout="wide")

st.title("📥 Lucian Receiver Dashboard")
st.caption("Displaying all received propagation packets")

if not os.path.exists(RECEIVED_LOG):
    st.warning("No received packets found yet.")
else:
    with open(RECEIVED_LOG, "r") as f:
        lines = f.readlines()

    if not lines:
        st.info("No transmissions logged yet.")
    else:
        logs = [json.loads(line) for line in lines[::-1]]

        filter_verified = st.checkbox("Show only verified packets", value=True)

        for log in logs:
            if filter_verified and not log.get("verified"):
                continue
            st.json(log)
