import sqlite3


def create_table():
    connection = sqlite3.connect("evidencechain.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS evidence (
            evidence_id TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            registered_at TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS custody_log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            evidence_id TEXT NOT NULL,
            action TEXT NOT NULL,
            details TEXT NOT NULL,
            logged_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_evidence(evidence_id, description, filename,
                  file_hash, registered_at):
    connection = sqlite3.connect("evidencechain.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO evidence
        (evidence_id, description, filename, file_hash, registered_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        evidence_id,
        description,
        filename,
        file_hash,
        registered_at
    ))

    connection.commit()
    connection.close()


def get_all_evidence():
    connection = sqlite3.connect("evidencechain.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT evidence_id, description, filename,
               file_hash, registered_at
        FROM evidence
        ORDER BY registered_at DESC
    """)

    records = cursor.fetchall()
    connection.close()

    return records

def get_evidence_by_id(evidence_id):
    connection = sqlite3.connect("evidencechain.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT evidence_id, description, filename,
               file_hash, registered_at
        FROM evidence
        WHERE evidence_id = ?
    """, (evidence_id,))

    record = cursor.fetchone()
    connection.close()

    return record

def log_custody_event(evidence_id, action, details, logged_at):
    connection = sqlite3.connect("evidencechain.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO custody_log
        (evidence_id, action, details, logged_at)
        VALUES (?, ?, ?, ?)
    """, (evidence_id, action, details, logged_at))

    connection.commit()
    connection.close()


def get_custody_log(evidence_id=None):
    connection = sqlite3.connect("evidencechain.db")
    cursor = connection.cursor()

    if evidence_id:
        cursor.execute("""
            SELECT log_id, evidence_id, action, details, logged_at
            FROM custody_log
            WHERE evidence_id = ?
            ORDER BY log_id DESC
        """, (evidence_id,))
    else:
        cursor.execute("""
            SELECT log_id, evidence_id, action, details, logged_at
            FROM custody_log
            ORDER BY log_id DESC
        """)

    records = cursor.fetchall()
    connection.close()

    return records
