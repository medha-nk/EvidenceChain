
import streamlit as st

st.set_page_config(
    page_title="EvidenceChain",
    page_icon=":material/shield:",
    layout="wide"
)

# ---------------- THEME STATE ----------------

if "ec_theme" not in st.session_state:
    st.session_state.ec_theme = "Dark"

# ---------------- SHARED THEME ----------------

if st.session_state.ec_theme == "Dark":
    bg = "#0A0F14"
    sidebar_bg = "#0D141B"
    panel_bg = "#121B23"
    text = "#E6EDF3"
    muted = "#9BAAB7"
    border = "#293642"
    accent = "#55D6BE"
    input_bg = "#121B23"
else:
    bg = "#F5F7FA"
    sidebar_bg = "#FFFFFF"
    panel_bg = "#FFFFFF"
    text = "#243447"
    muted = "#64748B"
    border = "#DCE3EB"
    accent = "#315B85"
    input_bg = "#FFFFFF"

st.markdown(f"""
<style>
    /* Main workspace */
    .stApp {{
        background-color: {bg};
        color: {text};
    }}

    .block-container {{
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border};
    }}

    section[data-testid="stSidebar"] > div {{
        padding-top: 1.5rem;
    }}

    /* General text */
    h1, h2, h3, h4, p, label {{
        color: {text};
    }}

    [data-testid="stMarkdownContainer"] {{
        color: {text};
    }}

    .ec-eyebrow,
    .ec-section-label {{
        color: {accent} !important;
    }}

    .ec-subtitle,
    .ec-muted,
    .ec-panel-note {{
        color: {muted} !important;
    }}

    /* Custom panels */
    .ec-metric,
    .ec-panel {{
        background-color: {panel_bg} !important;
        border: 1px solid {border} !important;
    }}

    .ec-metric-label,
    .ec-panel-label {{
        color: {muted} !important;
    }}

    .ec-metric-value,
    .ec-panel-value {{
        color: {text} !important;
    }}

    /* Metric widgets */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {{
        color: {text} !important;
    }}

    /* Text inputs and text areas */
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border-color: {border} !important;
    }}

    div[data-testid="stTextInput"] input::placeholder,
    div[data-testid="stTextArea"] textarea::placeholder {{
        color: {muted} !important;
        opacity: 1 !important;
    }}

    /* Select boxes */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
        background-color: {input_bg} !important;
        color: {text} !important;
        border-color: {border} !important;
    }}

    /* Radio buttons and checkboxes */
    div[data-testid="stRadio"] label,
    div[data-testid="stCheckbox"] label {{
        color: {text} !important;
    }}

    /* Tables: outer container only.
       Streamlit's data grid has its own internal theme. */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {{
        border: 1px solid {border};
        border-radius: 6px;
        overflow: hidden;
    }}

    /* File uploader */
    [data-testid="stFileUploader"] {{
        background-color: {panel_bg};
        border: 1px solid {border};
        border-radius: 6px;
        padding: 0.5rem;
    }}

    /* Buttons */
    div[data-testid="stButton"] button,
    div[data-testid="stFormSubmitButton"] button {{
        border-radius: 6px;
        border-color: {border};
    }}

    div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stFormSubmitButton"] button[kind="primary"] {{
        background-color: {accent} !important;
        color: {bg} !important;
        border-color: {accent} !important;
    }}

    /* Alerts */
    [data-testid="stAlert"] {{
        border-radius: 6px;
    }}

    /* Dividers */
    hr {{
        border-color: {border} !important;
    }}

    /* Sidebar branding */
    section[data-testid="stSidebar"] .ec-brand {{
        color: {text} !important;
    }}

    /* Fingerprint/code blocks */
    [data-testid="stCode"] {{
        border: 1px solid {border};
        border-radius: 6px;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("""
        <div class="ec-brand" style="font-size:1.35rem;font-weight:750;">
            EvidenceChain
        </div>
        <div style="
            font-size:0.68rem;
            letter-spacing:0.12em;
            color:#8293A3;
            margin-top:4px;
        ">
            DIGITAL FORENSICS WORKSPACE
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.caption("APPEARANCE")

    st.radio(
        "Choose theme",
        ["Dark", "Light"],
        horizontal=True,
        key="ec_theme",
        label_visibility="collapsed",
    )

    st.divider()

    st.caption("ENVIRONMENT")
    st.write("Educational prototype")

    st.caption("INTEGRITY ENGINE")
    st.write("SHA-256 fingerprinting")

# ---------------- NAVIGATION ----------------

overview_page = st.Page(
    "pages/overview.py",
    title="Overview",
    icon=":material/dashboard:",
    default=True
)

evidence_page = st.Page(
    "app.py",
    title="Evidence Register",
    icon=":material/folder_open:"
)

pg = st.navigation(
    [overview_page, evidence_page],
    position="sidebar"
)

pg.run()
