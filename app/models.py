import sqlite3
from datetime import datetime, UTC


def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str) -> None:
    conn = get_connection(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_text TEXT NOT NULL,
            severity TEXT NOT NULL,
            confidence REAL NOT NULL DEFAULT 0,
            suggestion TEXT NOT NULL,
            line_results TEXT NOT NULL DEFAULT '',
            evidence_path TEXT NOT NULL DEFAULT '',
            timestamp TEXT NOT NULL
        )
        """
    )
    # Upgrade older databases without dropping user data.
    _add_column_if_missing(conn, "reports", "confidence", "REAL NOT NULL DEFAULT 0")
    _add_column_if_missing(conn, "reports", "line_results", "TEXT NOT NULL DEFAULT ''")
    _add_column_if_missing(conn, "reports", "evidence_path", "TEXT NOT NULL DEFAULT ''")
    conn.commit()
    conn.close()


def _add_column_if_missing(
    conn: sqlite3.Connection, table_name: str, column_name: str, definition: str
) -> None:
    columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    existing_names = {column["name"] for column in columns}
    if column_name not in existing_names:
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")


def save_report(
    db_path: str,
    chat_text: str,
    severity: str,
    confidence: float,
    suggestion: str,
    line_results: str,
    evidence_path: str,
) -> None:
    conn = get_connection(db_path)
    conn.execute(
        """
        INSERT INTO reports (chat_text, severity, confidence, suggestion, line_results, evidence_path, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            chat_text,
            severity,
            confidence,
            suggestion,
            line_results,
            evidence_path,
            datetime.now(UTC).isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def get_reports(db_path: str, severity_filter: str | None = None) -> list[sqlite3.Row]:
    conn = get_connection(db_path)
    if severity_filter and severity_filter != "All":
        rows = conn.execute(
            "SELECT * FROM reports WHERE severity = ? ORDER BY id DESC",
            (severity_filter,),
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM reports ORDER BY id DESC").fetchall()
    conn.close()
    return rows
