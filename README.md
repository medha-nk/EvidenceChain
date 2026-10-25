# EvidenceChain

**A Python-based digital evidence integrity and chain-of-custody tracker.**

EvidenceChain is an educational digital forensics project built with Python and Streamlit. It provides a structured workspace for registering digital evidence, generating SHA-256 fingerprints, checking file integrity, and maintaining a chronological record of evidence-related events.

The project explores how file hashing, persistent storage, and audit logging can support digital evidence management workflows.

## Features

### Evidence Registration
- Register digital evidence with a unique Evidence ID and description.
- Record the uploaded filename and registration timestamp.
- Calculate and store the file's SHA-256 fingerprint.
- Persist evidence records using SQLite.
- Reject duplicate Evidence IDs.

### Integrity Verification
- Select a previously registered evidence item.
- Upload a file for comparison against its stored SHA-256 fingerprint.
- Display the original and current fingerprints.
- Report whether the fingerprints match.
- Record successful and failed verification attempts in the custody log.

### Chain of Custody
- Record evidence registration and integrity verification events.
- Store the associated Evidence ID, action, event details, and timestamp.
- Review events in a chronological table.
- Filter the log by Evidence ID.

### Workspace Interface
- Navigate between the overview and evidence workspace.
- View summary counts for registered evidence and recorded events.
- Search the evidence register.
- Review evidence records and recent activity.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| SQLite | Persistent evidence records and custody events |
| `hashlib` | SHA-256 fingerprint generation |
| Git and GitHub | Version control and source-code hosting |

## Getting Started

### Prerequisites

- Python installed on your system
- Git
- Visual Studio Code or another code editor

### 1. Clone the repository

```bash
git clone https://github.com/medha-nk/EvidenceChain.git
cd EvidenceChain
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the virtual environment's Python executable directly instead.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run main.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`, where the application can be opened in a browser.

## Project Structure

```text
EvidenceChain/
├── .streamlit/
│   └── config.toml
├── pages/
│   └── overview.py
├── app.py
├── database.py
├── evidence.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

| File | Responsibility |
|---|---|
| `main.py` | Application entry point and navigation |
| `app.py` | Evidence registration, integrity verification, and custody history |
| `pages/overview.py` | Overview dashboard and recent activity |
| `evidence.py` | SHA-256 fingerprint calculation |
| `database.py` | SQLite table creation and database operations |
| `.streamlit/config.toml` | Application theme configuration |
| `requirements.txt` | Python dependencies |

## How It Works

### 1. Registration

A user supplies an Evidence ID, a description, and a file. EvidenceChain calculates the file's SHA-256 fingerprint and saves the associated metadata and fingerprint in the SQLite database.

### 2. Verification

A user selects a registered evidence item and uploads a file to check. EvidenceChain calculates the uploaded file's SHA-256 fingerprint and compares it with the stored fingerprint.

- **Match:** the uploaded file's contents match the stored fingerprint.
- **Mismatch:** the uploaded file's contents do not match the stored fingerprint.

### 3. Custody Logging

EvidenceChain records registration and verification events with timestamps. These events can be reviewed in the Chain of Custody workspace.

## Important Limitations

EvidenceChain is an **educational prototype**, not a secure evidence vault or a validated forensic tool.

- Uploaded files are not stored as a secure evidence archive; the application stores their metadata and fingerprints.
- A matching fingerprint indicates that the uploaded file matches the stored fingerprint. It does not establish who created the file or prove its full history.
- The custody log is stored in the same SQLite database as the evidence records. It is not independently authenticated or protected against tampering.
- Evidence registration and custody-event logging are separate database operations, so a failure between them could leave an incomplete record.
- The application does not currently implement user authentication, role-based permissions, secure evidence acquisition, or independently verified timestamps.
- Only use harmless sample files for testing. Do not upload confidential, personal, or real investigative evidence.

These limitations are important considerations for any future development toward a more robust evidence-management system.

## Future Improvements

- Strengthen custody-log integrity and tamper detection.
- Add automated tests for hashing, registration, and verification.
- Improve evidence search and filtering.
- Add exportable evidence reports.
- Introduce stronger validation, error handling, and transaction management.
- Explore authentication, permissions, and secure evidence storage.
- Refine the interface around forensic investigation workflows.

## Learning Objectives

This project provides practical experience with:

- Python application development
- Cryptographic hashing and file integrity
- Relational database operations using SQLite
- Event logging and timestamps
- Building interactive interfaces with Streamlit
- Version control with Git and GitHub

## Disclaimer

EvidenceChain is developed for learning and demonstration purposes. It should not be relied upon as the sole means of preserving, validating, or presenting digital evidence in legal proceedings or real investigations.

## Repository

[https://github.com/medha-nk/EvidenceChain](https://github.com/medha-nk/EvidenceChain)
