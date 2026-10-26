
import streamlit as st
from database import get_all_evidence, get_custody_log

# ---------------- DATA ----------------

records = get_all_evidence()
events = get_custody_log()

# ---------------- PAGE STYLE ----------------

st.markdown("""
<style>
    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .ec-eyebrow {
        color: #55D6BE;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        margin-bottom: 0.5rem;
    }

    .ec-subtitle {
        color: #9BAAB7;
        font-size: 0.92rem;
        line-height: 1.6;
        margin-top: -0.4rem;
        margin-bottom: 1.8rem;
    }

    .ec-metric {
        background: #121B23;
        border: 1px solid #293642;
        border-radius: 6px;
        padding: 1.15rem 1.25rem;
        min-height: 115px;
    }

    .ec-metric-label {
        color: #9BAAB7;
        font-size: 0.72rem;
        font-weight: 650;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.65rem;
    }

    .ec-metric-value {
        color: #E6EDF3;
        font-size: 1.8rem;
        font-weight: 650;
        line-height: 1.2;
    }

    .ec-section-label {
        color: #55D6BE;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        margin-bottom: 0.35rem;
    }

    .ec-system-note {
        background: #121B23;
        border-left: 3px solid #55D6BE;
        padding: 0.9rem 1rem;
        border-radius: 3px;
        color: #B5C2CD;
        font-size: 0.84rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
    '<div class="ec-eyebrow">WORKSPACE / OVERVIEW</div>',
    unsafe_allow_html=True,
)

st.title("Overview")

st.markdown(
    '<div class="ec-subtitle">'
    'Review registered evidence, monitor recorded activity, '
    'and access the integrity workflow.'
    '</div>',
    unsafe_allow_html=True,
)

# ---------------- METRICS ----------------

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown(f"""
        <div class="ec-metric">
            <div class="ec-metric-label">Registered evidence</div>
            <div class="ec-metric-value">{len(records):02d}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="ec-metric">
            <div class="ec-metric-label">Custody events</div>
            <div class="ec-metric-value">{len(events):02d}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="ec-metric">
            <div class="ec-metric-label">Fingerprint algorithm</div>
            <div class="ec-metric-value">SHA-256</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# ---------------- RECENT ACTIVITY ----------------

st.markdown(
    '<div class="ec-section-label">ACTIVITY LOG</div>',
    unsafe_allow_html=True,
)

st.subheader("Recent activity")

if events:
    recent_events = []

    for event in events[:8]:
        recent_events.append({
            "Evidence ID": event[1],
            "Action": event[2],
            "Details": event[3],
            "Timestamp": event[4],
        })

    st.dataframe(
        recent_events,
        use_container_width=True,
        hide_index=True,
        height=350,
    )
else:
    st.info("No activity has been recorded yet.")

st.write("")
st.divider()

# ---------------- SYSTEM NOTE ----------------

st.markdown(
    '<div class="ec-section-label">SYSTEM INFORMATION</div>',
    unsafe_allow_html=True,
)

st.markdown("""
    <div class="ec-system-note">
        <strong>EvidenceChain — Educational prototype</strong><br>
        Evidence metadata and custody events are stored in a local
        SQLite database. SHA-256 fingerprints support file-integrity
        comparisons; the application does not provide a tamper-proof
        evidence vault or independently authenticated audit trail.
    </div>
""", unsafe_allow_html=True)
