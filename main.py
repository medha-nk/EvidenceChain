
import streamlit as st

st.set_page_config(
    page_title="EvidenceChain",
    page_icon=":material/shield_lock:",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.markdown("## EvidenceChain")
    st.caption("DIGITAL FORENSICS WORKSPACE")
    st.divider()

overview_page = st.Page(
    "pages/overview.py",
    title="Overview",
    icon=":material/space_dashboard:",
    default=True
)

evidence_page = st.Page(
    "app.py",
    title="Evidence Register",
    icon=":material/folder_open:"
)

pg = st.navigation(
    {
        "WORKSPACE": [overview_page, evidence_page]
    },
    position="sidebar"
)

pg.run()
