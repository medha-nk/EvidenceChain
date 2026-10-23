
import streamlit as st
from datetime import datetime
from evidence import calculate_hash


st.set_page_config(
    page_title="EvidenceChain",
    page_icon="🔐"
)

st.title("🔐 EvidenceChain")
st.subheader("Digital Evidence Chain of Custody")

st.write(
    "Register digital evidence and generate a SHA-256 "
    "fingerprint for future integrity checks."
)

st.warning(
    "Use sample files only. This prototype does not yet "
    "store records permanently or provide a secure evidence vault."
)

st.markdown("## Register Evidence")

evidence_id = st.text_input("Evidence ID")
description = st.text_input("Evidence Description")

uploaded_file = st.file_uploader(
    "Choose an evidence file"
)

if st.button("Register Evidence"):
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

        st.success("Evidence fingerprint generated!")

        st.markdown("### Evidence Record")
        st.write("**Evidence ID:**", evidence_id)
        st.write("**Description:**", description)
        st.write("**Filename:**", uploaded_file.name)
        st.write("**Registration Time:**", registered_at)
        st.write("**SHA-256 Hash:**")

        st.code(file_hash, language="text")
