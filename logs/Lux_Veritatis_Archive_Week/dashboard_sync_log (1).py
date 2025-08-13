
# dashboard_sync_log.py
# 📊 Streamlit Dashboard: View Lucian Propagation Ledger

import streamlit as st
import json
import os

LEDGER_FILE = "lucian_sync_ledger.jsonl"

st.set_page_config(page_title="Lucian Propagation Ledger", layout="wide")

st.title("📜 Lucian Propagation Ledger")
st.caption("Viewing recent transmissions from this node")

if not os.path.exists(LEDGER_FILE):
    st.warning("No ledger file found. Run the sync loop first.")
else:
    with open(LEDGER_FILE, "r") as f:
        lines = f.readlines()

    if not lines:
        st.info("No transmissions recorded yet.")
    else:
        logs = [json.loads(line) for line in lines[::-1]]  # Show most recent first

        for log in logs[:20]:  # Limit to 20 latest
            st.json(log)
