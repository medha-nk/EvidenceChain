
import streamlit as st
from datetime import datetime
import sqlite3

from evidence import calculate_hash
from database import (
    create_table,
    save_evidence,
    get_all_evidence,
    get_evidence_by_id
)


st.set_page_config(
    page_title="EvidenceChain",
    page_icon="🔐",
    layout="wide"
)

create_table()

st.title("EvidenceChain")
st.caption("Digital Evidence | Integrity & Custody Records")

st.write(
    "Register digital evidence and maintain a record "
    "of its original SHA-256 fingerprint."
)

st.warning(
    "Educational prototype. Use sample files only. "
    "This application is not a secure evidence vault."
)

st.divider()

st.header("Register Evidence")

with st.form("evidence_form"):
    evidence_id = st.text_input("Evidence ID")
    description = st.text_input("Evidence Description")

    uploaded_file = st.file_uploader(
        "Choose an evidence file"
    )

    submitted = st.form_submit_button("Register Evidence")

if submitted:
    if not evidence_id.strip():
        st.error("Please enter an Evidence ID.")

    elif not description.strip():
        st.error("Please enter a description.")

    elif uploaded_file is None:
        st.error("Please upload a file.")

    else:
        file_bytes = uploaded_file.getvalue()
        file_hash = calculate_hash(file_bytes)

        registered_at = datetime.now().astimezone().strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        )

        try:
            save_evidence(
                evidence_id.strip(),
                description.strip(),
                uploaded_file.name,
                file_hash,
                registered_at
            )

            st.success("Evidence record saved successfully!")

            st.subheader("Registered Evidence")
            st.write("**Evidence ID:**", evidence_id.strip())
            st.write("**Filename:**", uploaded_file.name)
            st.write("**Registered at:**", registered_at)
            st.write("**SHA-256 fingerprint:**")
            st.code(file_hash)

        except sqlite3.IntegrityError:
            st.error(
                "This Evidence ID already exists. "
                "Please use a different ID."
            )

st.divider()

st.header("Evidence Register")

records = get_all_evidence()

if records:
    table_data = []

    for record in records:
        table_data.append({
            "Evidence ID": record[0],
            "Description": record[1],
            "Filename": record[2],
            "SHA-256": record[3],
            "Registered At": record[4]
        })

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No evidence records have been saved yet.")


st.divider()
st.header("Verify Evidence")

st.write(
    "Check whether a file matches the fingerprint "
    "stored when it was registered."
)

records = get_all_evidence()

if records:
    evidence_ids = [record[0] for record in records]

    selected_id = st.selectbox(
        "Select Evidence ID",
        evidence_ids
    )

    verification_file = st.file_uploader(
        "Upload the file to verify",
        key="verification_file"
    )

    if st.button("Verify Integrity"):
        if verification_file is None:
            st.error("Please upload a file to verify.")
        else:
            original_record = get_evidence_by_id(selected_id)

            original_hash = original_record[3]
            uploaded_bytes = verification_file.getvalue()
            current_hash = calculate_hash(uploaded_bytes)

            st.write("**Stored SHA-256 fingerprint:**")
            st.code(original_hash)

            st.write("**Current SHA-256 fingerprint:**")
            st.code(current_hash)

            if original_hash == current_hash:
                st.success(
                    "INTEGRITY CHECK PASSED — "
                    "The file matches the stored fingerprint."
                )
            else:
                st.error(
                    "INTEGRITY CHECK FAILED — "
                    "The file does not match the stored fingerprint."
                )
else:
    st.info("Register evidence before attempting verification.")

