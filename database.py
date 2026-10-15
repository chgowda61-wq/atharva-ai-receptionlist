import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "receptionist.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_id TEXT UNIQUE NOT NULL,
            language TEXT DEFAULT 'en',
            status TEXT DEFAULT 'active',
            started_at TEXT DEFAULT CURRENT_TIMESTAMP,
            ended_at TEXT
        );

        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_id TEXT NOT NULL,
            speaker TEXT NOT NULL,
            text TEXT NOT NULL,
            ts TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (call_id) REFERENCES calls(call_id)
        );

        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_id TEXT NOT NULL,
            request_type TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (call_id) REFERENCES calls(call_id)
        );

        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_id TEXT,
            doctor TEXT,
            slot TEXT,
            status TEXT DEFAULT 'pending'
        );

        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_id TEXT,
            item TEXT,
            date TEXT,
            price REAL
        );

        CREATE TABLE IF NOT EXISTS escalations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_id TEXT,
            reason TEXT,
            handled_by TEXT
        );

        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            language TEXT DEFAULT 'en'
        );
        """)


def create_call(call_id, language="en"):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO calls (call_id, language) VALUES (?, ?)",
            (call_id, language)
        )


def save_turn(call_id, speaker, text):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO transcripts (call_id, speaker, text)
               VALUES (?, ?, ?)""",
            (call_id, speaker, text)
        )


def save_request(call_id, request_type, description):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO requests
               (call_id, request_type, description)
               VALUES (?, ?, ?)""",
            (call_id, request_type, description)
        )


def end_call(call_id):
    with get_conn() as conn:
        conn.execute(
            """UPDATE calls SET status = 'completed',
               ended_at = CURRENT_TIMESTAMP WHERE call_id = ?""",
            (call_id,)
        )


def get_calls():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM calls ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_transcripts(call_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM transcripts WHERE call_id = ? ORDER BY id",
            (call_id,)
        ).fetchall()
        return [dict(row) for row in rows]


def get_requests(call_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM requests WHERE call_id = ? ORDER BY id",
            (call_id,)
        ).fetchall()
        return [dict(row) for row in rows]
    