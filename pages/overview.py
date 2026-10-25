
import streamlit as st
from database import get_all_evidence, get_custody_log

st.title("EvidenceChain")
st.caption("DIGITAL FORENSICS  /  EVIDENCE MANAGEMENT")

st.divider()

st.header("Overview")
st.write(
    "Monitor registered evidence, review recent activity, "
    "and access integrity records."
)

records = get_all_evidence()
events = get_custody_log()

total_evidence = len(records)
total_events = len(events)

col1, col2 = st.columns(2)

with col1:
    st.metric("Registered Evidence", total_evidence)

with col2:
    st.metric("Recorded Events", total_events)

st.divider()

st.subheader("Recent Activity")

if events:
    recent_events = []

    for event in events[:5]:
        recent_events.append({
            "Evidence ID": event[1],
            "Action": event[2],
            "Timestamp": event[4]
        })

    st.dataframe(
        recent_events,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No activity has been recorded yet.")

st.divider()

st.subheader("Workspace")
st.write(
    "Use the navigation menu to access your evidence "
    "register and custody records."
)
