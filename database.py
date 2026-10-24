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
