
import streamlit as st
from datetime import datetime
import sqlite3

from evidence import calculate_hash
from database import (
    create_table,
    save_evidence,
    get_all_evidence,
    get_evidence_by_id,
    log_custody_event,
    get_custody_log,
)

# --------------------------------------------------
# PAGE SETUP
# main.py controls the application-wide page config.
# --------------------------------------------------

create_table()

# --------------------------------------------------
# VISUAL DESIGN
# --------------------------------------------------

st.markdown("""
<style>
    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    h1, h2, h3 {
        letter-spacing: -0.035em;
    }

    h1 {
        font-weight: 650;
    }

    h2, h3 {
        font-weight: 550;
    }

    .ec-eyebrow {
        color: #55D6BE;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .ec-subtitle {
        color: #9BAAB7;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-top: -0.4rem;
        margin-bottom: 1.5rem;
    }

    .ec-panel {
        background: #121B23;
        border: 1px solid #293642;
        border-radius: 6px;
        padding: 1.15rem 1.25rem;
        margin: 0.5rem 0 1rem 0;
    }

    .ec-panel-label {
        color: #9BAAB7;
        font-size: 0.72rem;
        font-weight: 650;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
    }

    .ec-panel-value {
        color: #E6EDF3;
        font-size: 1.65rem;
        font-weight: 650;
        line-height: 1.3;
    }

    .ec-panel-note {
        color: #9BAAB7;
        font-size: 0.8rem;
        margin-top: 0.35rem;
    }

    .ec-status {
        display: inline-block;
        padding: 0.3rem 0.55rem;
        border-radius: 3px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }

    .ec-status-pass {
        background: #12382F;
        color: #72E2C5;
        border: 1px solid #246653;
    }

    .ec-status-fail {
        background: #3B2025;
        color: #FF9B9B;
        border: 1px solid #71343B;
    }

    div[data-testid="stTabs"] button {
        font-weight: 550;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #55D6BE;
    }

    div[data-testid="stForm"] {
        border: 1px solid #293642;
        border-radius: 6px;
        padding: 1.25rem;
        background: #0D141B;
    }

    div[data-testid="stFileUploader"] {
        border-radius: 4px;
    }

    code {
        overflow-wrap: anywhere;
    }

    hr {
        border-color: #293642;
    }

    .ec-footnote {
        color: #8495A4;
        font-size: 0.78rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="ec-eyebrow">DIGITAL FORENSICS / EVIDENCE MANAGEMENT</div>',
    unsafe_allow_html=True,
)

st.title("Evidence workspace")

st.markdown(
    '<div class="ec-subtitle">'
    'Register digital evidence, validate file integrity, '
    'and review recorded custody events.'
    '</div>',
    unsafe_allow_html=True,
)

st.warning(
    "Educational prototype. Use sample files only. "
    "This application is not a secure evidence vault."
)

records = get_all_evidence()
all_events = get_custody_log()

# --------------------------------------------------
# SUMMARY STRIP
# --------------------------------------------------

summary_a, summary_b, summary_c = st.columns(3)

with summary_a:
    st.markdown(
        f"""
        <div class="ec-panel">
            <div class="ec-panel-label">Registered evidence</div>
            <div class="ec-panel-value">{len(records):02d}</div>
            <div class="ec-panel-note">Stored evidence records</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with summary_b:
    st.markdown(
        f"""
        <div class="ec-panel">
            <div class="ec-panel-label">Custody events</div>
            <div class="ec-panel-value">{len(all_events):02d}</div>
            <div class="ec-panel-note">Recorded application events</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with summary_c:
    st.markdown(
        """
        <div class="ec-panel">
            <div class="ec-panel-label">Hash algorithm</div>
            <div class="ec-panel-value">SHA-256</div>
            <div class="ec-panel-note">File fingerprint comparison</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# --------------------------------------------------
# WORKSPACE TABS
# --------------------------------------------------

register_tab, register_view_tab, verify_tab, custody_tab = st.tabs([
    "Register Evidence",
    "Evidence Register",
    "Verify Integrity",
    "Chain of Custody",
])

# --------------------------------------------------
# TAB 1: REGISTER EVIDENCE
# --------------------------------------------------

with register_tab:
    st.subheader("Register new evidence")
    st.caption(
        "Create a record and calculate the file's original SHA-256 fingerprint."
    )

    with st.form("evidence_form", clear_on_submit=True):
        evidence_id = st.text_input(
            "Evidence ID",
            placeholder="e.g. EV-005",
            help="Use a unique identifier for each evidence item.",
        )

        description = st.text_input(
            "Evidence description",
            placeholder="Briefly describe the item",
        )

        uploaded_file = st.file_uploader(
            "Evidence file",
            help="Use a harmless sample file for this prototype.",
        )

        submitted = st.form_submit_button(
            "Register evidence",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not evidence_id.strip():
            st.error("Enter an Evidence ID.")
        elif not description.strip():
            st.error("Enter an evidence description.")
        elif uploaded_file is None:
            st.error("Choose a file before registering.")
        else:
            clean_id = evidence_id.strip()
            file_bytes = uploaded_file.getvalue()
            file_hash = calculate_hash(file_bytes)

            registered_at = datetime.now().astimezone().strftime(
                "%Y-%m-%d %H:%M:%S %Z"
            )

            try:
                save_evidence(
                    clean_id,
                    description.strip(),
                    uploaded_file.name,
                    file_hash,
                    registered_at,
                )

                log_custody_event(
                    clean_id,
                    "Evidence Registered",
                    f"File: {uploaded_file.name}; SHA-256: {file_hash}",
                    registered_at,
                )

                st.success(f"Evidence {clean_id} registered successfully.")

                st.markdown("#### Registration receipt")
                receipt_a, receipt_b = st.columns(2)

                with receipt_a:
                    st.write("**Evidence ID**")
                    st.write(clean_id)
                    st.write("**Filename**")
                    st.write(uploaded_file.name)

                with receipt_b:
                    st.write("**Registered at**")
                    st.write(registered_at)
                    st.write("**Fingerprint algorithm**")
                    st.write("SHA-256")

                st.write("**Original SHA-256 fingerprint**")
                st.code(file_hash, language=None)

            except sqlite3.IntegrityError:
                st.error(
                    "That Evidence ID already exists. "
                    "Choose a different ID."
                )

            except Exception as exc:
                st.error(
                    "The operation encountered an error. "
                    "Check the terminal for details."
                )
                print(f"Evidence registration error: {exc}")

# --------------------------------------------------
# TAB 2: EVIDENCE REGISTER
# --------------------------------------------------

with register_view_tab:
    st.subheader("Evidence register")
    st.caption(
        "Review saved records and their original fingerprints."
    )

    records = get_all_evidence()

    if records:
        search_term = st.text_input(
            "Search evidence",
            placeholder="Search ID, description, or filename",
            key="evidence_search",
        )

        filtered_records = [
            record for record in records
            if search_term.strip().lower() in " ".join(
                str(value) for value in record[:3]
            ).lower()
        ]

        st.caption(
            f"Showing {len(filtered_records)} of {len(records)} records"
        )

        if filtered_records:
            table_data = []

            for record in filtered_records:
                table_data.append({
                    "Evidence ID": record[0],
                    "Description": record[1],
                    "Filename": record[2],
                    "SHA-256": record[3],
                    "Registered At": record[4],
                })

            st.dataframe(
                table_data,
                use_container_width=True,
                hide_index=True,
                height=380,
                column_config={
                    "Evidence ID": st.column_config.TextColumn(
                        "Evidence ID",
                        width="small",
                    ),
                    "Description": st.column_config.TextColumn(
                        "Description",
                        width="medium",
                    ),
                    "Filename": st.column_config.TextColumn(
                        "Filename",
                        width="medium",
                    ),
                    "SHA-256": st.column_config.TextColumn(
                        "SHA-256 fingerprint",
                        width="large",
                    ),
                    "Registered At": st.column_config.TextColumn(
                        "Registered at",
                        width="medium",
                    ),
                },
            )
        else:
            st.info("No records match that search.")

    else:
        st.info("No evidence has been registered yet.")

# --------------------------------------------------
# TAB 3: VERIFY INTEGRITY
# --------------------------------------------------

with verify_tab:
    st.subheader("Verify file integrity")
    st.caption(
        "Compare a file's current SHA-256 fingerprint "
        "with the fingerprint saved at registration."
    )

    records = get_all_evidence()

    if records:
        evidence_by_id = {record[0]: record for record in records}
        evidence_ids = list(evidence_by_id.keys())

        selected_id = st.selectbox(
            "Evidence record",
            evidence_ids,
            key="verification_evidence_id",
        )

        selected_record = evidence_by_id[selected_id]

        st.markdown(
            f"""
            <div class="ec-panel">
                <div class="ec-panel-label">Selected evidence</div>
                <div class="ec-panel-value">{selected_record[0]}</div>
                <div class="ec-panel-note">
                    {selected_record[2]} &nbsp; | &nbsp;
                    Registered {selected_record[4]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        verification_file = st.file_uploader(
            "File to verify",
            key="verification_file",
        )

        if st.button(
            "Run integrity check",
            type="primary",
            use_container_width=True,
        ):
            if verification_file is None:
                st.error("Upload the file you want to verify.")
            else:
                original_record = get_evidence_by_id(selected_id)

                if original_record is None:
                    st.error("The selected evidence record could not be found.")
                else:
                    original_hash = original_record[3]
                    current_hash = calculate_hash(
                        verification_file.getvalue()
                    )

                    verification_time = datetime.now().astimezone().strftime(
                        "%Y-%m-%d %H:%M:%S %Z"
                    )

                    matches = original_hash == current_hash

                    if matches:
                        log_custody_event(
                            selected_id,
                            "Integrity Verified",
                            "PASS — SHA-256 fingerprints matched.",
                            verification_time,
                        )
                    else:
                        log_custody_event(
                            selected_id,
                            "Integrity Verification Failed",
                            "FAIL — SHA-256 fingerprints did not match.",
                            verification_time,
                        )

                    st.divider()
                    st.subheader("Verification result")

                    if matches:
                        st.markdown(
                            '<span class="ec-status ec-status-pass">'
                            'INTEGRITY CHECK PASSED</span>',
                            unsafe_allow_html=True,
                        )
                        st.write(
                            "The uploaded file matches the stored fingerprint."
                        )
                    else:
                        st.markdown(
                            '<span class="ec-status ec-status-fail">'
                            'INTEGRITY CHECK FAILED</span>',
                            unsafe_allow_html=True,
                        )
                        st.write(
                            "The uploaded file does not match the stored fingerprint."
                        )

                    st.write("**Stored SHA-256 fingerprint**")
                    st.code(original_hash, language=None)

                    st.write("**Current SHA-256 fingerprint**")
                    st.code(current_hash, language=None)

                    st.caption(
                        f"Verification recorded at {verification_time}"
                    )

                    #st.rerun()

    else:
        st.info("Register evidence before running an integrity check.")

# --------------------------------------------------
# TAB 4: CHAIN OF CUSTODY
# --------------------------------------------------

with custody_tab:
    st.subheader("Chain of custody")
    st.caption(
        "Review registration and integrity verification events."
    )

    all_events = get_custody_log()

    if all_events:
        evidence_ids_in_log = sorted(
            {event[1] for event in all_events}
        )

        selected_filter = st.selectbox(
            "Filter by evidence ID",
            ["All evidence"] + evidence_ids_in_log,
            key="custody_filter",
        )

        if selected_filter == "All evidence":
            filtered_events = all_events
        else:
            filtered_events = [
                event for event in all_events
                if event[1] == selected_filter
            ]

        st.caption(f"{len(filtered_events)} recorded events")

        event_data = []

        for event in filtered_events:
            event_data.append({
                "Log ID": event[0],
                "Evidence ID": event[1],
                "Action": event[2],
                "Details": event[3],
                "Timestamp": event[4],
            })

        st.dataframe(
            event_data,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_config={
                "Log ID": st.column_config.NumberColumn(
                    "Log ID",
                    width="small",
                    format="%d",
                ),
                "Evidence ID": st.column_config.TextColumn(
                    "Evidence ID",
                    width="small",
                ),
                "Action": st.column_config.TextColumn(
                    "Action",
                    width="medium",
                ),
                "Details": st.column_config.TextColumn(
                    "Event details",
                    width="large",
                ),
                "Timestamp": st.column_config.TextColumn(
                    "Timestamp",
                    width="medium",
                ),
            },
        )

        st.markdown(
            '<div class="ec-footnote">'
            'This log records events generated by the application. '
            'It is not a tamper-proof or independently authenticated audit trail.'
            '</div>',
            unsafe_allow_html=True,
        )

    else:
        st.info(
            "No custody events recorded yet. "
            "Register evidence to begin the activity history."
        )

st.divider()

st.markdown(
    '<div class="ec-footnote">'
    'EVIDENCECHAIN &nbsp; / &nbsp; EDUCATIONAL PROTOTYPE &nbsp; / '
    '&nbsp; SHA-256 INTEGRITY CHECKS'
    '</div>',
    unsafe_allow_html=True,
)
