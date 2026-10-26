
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
    st.markdown(
        '<div class="ec-eyebrow">EVIDENCE MANAGEMENT / INTAKE</div>',
        unsafe_allow_html=True,
    )

    st.title("Register evidence")

    st.markdown(
        '<div class="ec-subtitle">'
        'Create an evidence record and calculate its original '
        'SHA-256 fingerprint.'
        '</div>',
        unsafe_allow_html=True,
    )

    form_col, info_col = st.columns([1.5, 1], gap="large")

    with form_col:
        st.markdown("### Evidence details")

        with st.form("evidence_form", clear_on_submit=True):
            evidence_id = st.text_input(
                "Evidence ID",
                placeholder="e.g. EV-006",
                help="Enter a unique identifier for this evidence item.",
            )

            description = st.text_input(
                "Description",
                placeholder="Briefly describe the evidence",
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
                file_hash = calculate_hash(uploaded_file.getvalue())

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

                    st.session_state["registration_receipt"] = {
                        "evidence_id": clean_id,
                        "description": description.strip(),
                        "filename": uploaded_file.name,
                        "registered_at": registered_at,
                        "hash": file_hash,
                    }

                    st.success(
                        f"Evidence {clean_id} registered successfully."
                    )

                except sqlite3.IntegrityError:
                    st.error(
                        "That Evidence ID already exists. "
                        "Choose a different ID."
                    )

                except Exception as exc:
                    st.error(
                        "Registration failed. Check the terminal "
                        "for details."
                    )
                    print(f"Evidence registration error: {exc}")

    with info_col:
        st.markdown("""
        <div class="ec-panel">
            <div class="ec-panel-label">REGISTRATION PROTOCOL</div>
            <div class="ec-panel-value">SHA-256</div>
            <div class="ec-panel-note">
                A fingerprint is calculated from the uploaded file's
                contents and stored alongside its evidence metadata.
            </div>
            <hr>
            <div class="ec-panel-label">RECORD INCLUDES</div>
            <div class="ec-panel-note">
                Evidence ID<br>
                Description and filename<br>
                Original SHA-256 fingerprint<br>
                Registration timestamp
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.caption(
            "The prototype stores metadata and fingerprints, "
            "not the uploaded file itself."
        )

    receipt = st.session_state.get("registration_receipt")

    if receipt:
        st.divider()

        st.markdown(
            '<div class="ec-section-label">LATEST REGISTRATION</div>',
            unsafe_allow_html=True,
        )

        st.subheader("Registration receipt")

        receipt_col, hash_col = st.columns([1, 1], gap="large")

        with receipt_col:
            st.write("**Evidence ID**")
            st.write(receipt["evidence_id"])

            st.write("**Description**")
            st.write(receipt["description"])

            st.write("**Filename**")
            st.write(receipt["filename"])

            st.write("**Registered at**")
            st.write(receipt["registered_at"])

        with hash_col:
            st.write("**Original SHA-256 fingerprint**")
            st.code(receipt["hash"], language=None)

# --------------------------------------------------
# TAB 2: EVIDENCE REGISTER
# --------------------------------------------------

with register_view_tab:
    st.markdown(
        '<div class="ec-eyebrow">EVIDENCE MANAGEMENT / INVENTORY</div>',
        unsafe_allow_html=True,
    )

    st.title("Evidence register")

    st.markdown(
        '<div class="ec-subtitle">'
        'Search, inspect, and review registered evidence records.'
        '</div>',
        unsafe_allow_html=True,
    )

    records = get_all_evidence()

    if records:
        # Search controls
        search_col, count_col = st.columns([3, 1])

        with search_col:
            search_term = st.text_input(
                "Search inventory",
                placeholder="Evidence ID, description, or filename",
                key="evidence_search",
            )

        filtered_records = [
            record for record in records
            if search_term.strip().lower() in " ".join(
                str(value) for value in record[:3]
            ).lower()
        ]

        with count_col:
            st.markdown(
                '<div class="ec-panel-label">MATCHING RECORDS</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="ec-panel-value">'
                f'{len(filtered_records):02d}'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.write("")

        if filtered_records:
            table_data = []

            for record in filtered_records:
                table_data.append({
                    "Evidence ID": record[0],
                    "Description": record[1],
                    "Filename": record[2],
                    "Registered At": record[4],
                })

            st.dataframe(
                table_data,
                use_container_width=True,
                hide_index=True,
                height=350,
                column_config={
                    "Evidence ID": st.column_config.TextColumn(
                        "Evidence ID",
                        width="small",
                    ),
                    "Description": st.column_config.TextColumn(
                        "Description",
                        width="large",
                    ),
                    "Filename": st.column_config.TextColumn(
                        "Filename",
                        width="medium",
                    ),
                    "Registered At": st.column_config.TextColumn(
                        "Registered at",
                        width="medium",
                    ),
                },
            )

            st.divider()

            st.markdown(
                '<div class="ec-section-label">RECORD DETAILS</div>',
                unsafe_allow_html=True,
            )

            selected_id = st.selectbox(
                "Inspect evidence record",
                [record[0] for record in filtered_records],
                key="inspect_evidence_id",
            )

            selected_record = next(
                record for record in filtered_records
                if record[0] == selected_id
            )

            detail_col, hash_col = st.columns([1, 1], gap="large")

            with detail_col:
                st.markdown("#### Evidence metadata")

                st.write("**Evidence ID**")
                st.write(selected_record[0])

                st.write("**Description**")
                st.write(selected_record[1])

                st.write("**Filename**")
                st.write(selected_record[2])

                st.write("**Registered at**")
                st.write(selected_record[4])

            with hash_col:
                st.markdown("#### Original fingerprint")
                st.caption("SHA-256")

                st.code(
                    selected_record[3],
                    language=None,
                )

                st.caption(
                    "This fingerprint represents the file contents "
                    "at registration time."
                )

        else:
            st.info("No records match your search.")

    else:
        st.info(
            "No evidence has been registered yet. "
            "Use Register Evidence to create your first record."
        )

# --------------------------------------------------
# TAB 3: VERIFY INTEGRITY
# --------------------------------------------------

with verify_tab:
    st.markdown(
        '<div class="ec-eyebrow">EVIDENCE ANALYSIS / INTEGRITY CHECK</div>',
        unsafe_allow_html=True,
    )

    st.title("Verify integrity")

    st.markdown(
        '<div class="ec-subtitle">'
        'Compare a submitted file against its registered SHA-256 '
        'fingerprint to check whether the file contents match.'
        '</div>',
        unsafe_allow_html=True,
    )

    records = get_all_evidence()

    if records:
        evidence_by_id = {record[0]: record for record in records}

        select_col, info_col = st.columns([1.5, 1], gap="large")

        with select_col:
            selected_id = st.selectbox(
                "Select evidence record",
                list(evidence_by_id.keys()),
                key="verify_evidence_id",
            )

            selected_record = evidence_by_id[selected_id]

            st.markdown("### Selected evidence")

            st.write(f"**Evidence ID:** {selected_record[0]}")
            st.write(f"**Description:** {selected_record[1]}")
            st.write(f"**Registered filename:** {selected_record[2]}")

        with info_col:
            st.markdown("""
            <div class="ec-panel">
                <div class="ec-panel-label">VERIFICATION METHOD</div>
                <div class="ec-panel-value">SHA-256</div>
                <div class="ec-panel-note">
                    The uploaded file is hashed and compared with the
                    original fingerprint stored during registration.
                </div>
                <hr>
                <div class="ec-panel-label">INTERPRETATION</div>
                <div class="ec-panel-note">
                    MATCH — file contents have the same fingerprint.<br><br>
                    MISMATCH — file contents have a different fingerprint.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        st.markdown(
            '<div class="ec-section-label">NEW FILE SAMPLE</div>',
            unsafe_allow_html=True,
        )

        verification_file = st.file_uploader(
            "Upload the file to verify",
            help="Upload the original file or a file you want to compare.",
            key="integrity_verification_file",
        )

        if st.button(
            "Run integrity check",
            type="primary",
            use_container_width=False,
        ):
            if verification_file is None:
                st.error("Upload a file before running verification.")

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
                        result_label = "PASS"
                        result_colour = "#55D6BE"
                        result_message = (
                            "The uploaded file matches the original "
                            "registered fingerprint."
                        )
                        action = "Integrity Verified"
                        details = (
                            "PASS — SHA-256 fingerprints matched."
                        )
                    else:
                        result_label = "FAIL"
                        result_colour = "#FF7373"
                        result_message = (
                            "The uploaded file does not match the "
                            "original registered fingerprint."
                        )
                        action = "Integrity Verification Failed"
                        details = (
                            "FAIL — SHA-256 fingerprints did not match."
                        )

                    log_custody_event(
                        selected_id,
                        action,
                        details,
                        verification_time,
                    )

                    st.session_state["verification_result"] = {
                        "evidence_id": selected_id,
                        "filename": verification_file.name,
                        "result": result_label,
                        "colour": result_colour,
                        "message": result_message,
                        "stored_hash": original_hash,
                        "current_hash": current_hash,
                        "timestamp": verification_time,
                    }

        result = st.session_state.get("verification_result")

        if result and result["evidence_id"] == selected_id:
            st.divider()

            st.markdown(
                '<div class="ec-section-label">VERIFICATION REPORT</div>',
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div style="
                    background:#121B23;
                    border:1px solid #293642;
                    border-left:4px solid {result['colour']};
                    border-radius:6px;
                    padding:1.25rem;
                    margin:0.5rem 0 1.25rem 0;
                ">
                    <div style="
                        color:{result['colour']};
                        font-size:1.35rem;
                        font-weight:750;
                        letter-spacing:0.08em;
                    ">{result['result']}</div>
                    <div style="
                        color:#E6EDF3;
                        margin-top:0.4rem;
                    ">{result['message']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            hash_col1, hash_col2 = st.columns(2, gap="large")

            with hash_col1:
                st.markdown("#### Original fingerprint")
                st.code(result["stored_hash"], language=None)

            with hash_col2:
                st.markdown("#### Uploaded file fingerprint")
                st.code(result["current_hash"], language=None)

            st.caption(
                f"File checked: {result['filename']} · "
                f"Recorded at: {result['timestamp']}"
            )

            st.caption(
                "A matching hash indicates matching file contents; "
                "it does not independently establish the file's "
                "origin or the authenticity of its chain of custody."
            )

    else:
        st.info("Register evidence before running an integrity check.")

# --------------------------------------------------
# TAB 4: CHAIN OF CUSTODY
# --------------------------------------------------

# --------------------------------------------------
# TAB 4: CHAIN OF CUSTODY
# --------------------------------------------------

with custody_tab:
    st.markdown(
        '<div class="ec-eyebrow">AUDIT HISTORY / CUSTODY RECORDS</div>',
        unsafe_allow_html=True,
    )

    st.title("Chain of custody")

    st.markdown(
        '<div class="ec-subtitle">'
        'Review recorded evidence events and inspect the history '
        'associated with an individual evidence item.'
        '</div>',
        unsafe_allow_html=True,
    )

    events = get_custody_log()

    if events:
        evidence_ids = sorted(set(event[1] for event in events))

        filter_col, count_col = st.columns([2, 1])

        with filter_col:
            selected_filter = st.selectbox(
                "Filter by Evidence ID",
                ["All evidence"] + evidence_ids,
                key="custody_evidence_filter",
            )

        if selected_filter == "All evidence":
            filtered_events = events
        else:
            filtered_events = [
                event for event in events
                if event[1] == selected_filter
            ]

        with count_col:
            st.markdown(
                '<div class="ec-panel-label">MATCHING EVENTS</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="ec-panel-value">'
                f'{len(filtered_events):02d}'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.write("")
        st.divider()

        st.markdown(
            '<div class="ec-section-label">RECORDED EVENTS</div>',
            unsafe_allow_html=True,
        )

        st.subheader("Event history")

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
                    "Details",
                    width="large",
                ),
                "Timestamp": st.column_config.TextColumn(
                    "Timestamp",
                    width="medium",
                ),
            },
        )

        st.divider()

        st.markdown(
            '<div class="ec-section-label">EVENT DETAILS</div>',
            unsafe_allow_html=True,
        )

        selected_event_index = st.selectbox(
            "Inspect event",
            range(len(filtered_events)),
            format_func=lambda index: (
                f"Log #{filtered_events[index][0]} · "
                f"{filtered_events[index][1]} · "
                f"{filtered_events[index][2]}"
            ),
            key="inspect_custody_event",
        )

        selected_event = filtered_events[selected_event_index]

        detail_col, time_col = st.columns([2, 1], gap="large")

        with detail_col:
            st.markdown("#### Event information")

            st.write(f"**Log ID:** {selected_event[0]}")
            st.write(f"**Evidence ID:** {selected_event[1]}")
            st.write(f"**Action:** {selected_event[2]}")

            st.write("**Details**")
            st.write(selected_event[3])

        with time_col:
            st.markdown("#### Recorded timestamp")
            st.write(selected_event[4])

        st.caption(
            "Events are displayed from the application's SQLite "
            "custody log. This log is not independently authenticated "
            "or protected against modification."
        )

    else:
        st.info(
            "No custody events have been recorded yet. "
            "Register evidence or run an integrity check to create events."
        )


st.divider()

st.markdown(
    '<div class="ec-footnote">'
    'EVIDENCECHAIN &nbsp; / &nbsp; EDUCATIONAL PROTOTYPE &nbsp; / '
    '&nbsp; SHA-256 INTEGRITY CHECKS'
    '</div>',
    unsafe_allow_html=True,
)
