import sqlite3
from threading import RLock
from uuid import UUID

# The shared connection keeps data alive until the process exits.
db = sqlite3.connect(":memory:", check_same_thread=False)
db.row_factory = sqlite3.Row
_lock = RLock()

db.execute("""
    CREATE TABLE tickets (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'open'
    )
""")


def create_ticket(ticket_id: UUID, title: str, description: str) -> dict:
    with _lock, db:
        db.execute(
            "INSERT INTO tickets (id, title, description, status) VALUES (?, ?, ?, ?)",
            (str(ticket_id), title, description, "open"),
        )
        row = db.execute(
            "SELECT * FROM tickets WHERE id = ?", (str(ticket_id),)
        ).fetchone()
        return dict(row)


def list_tickets() -> list[dict]:
    with _lock:
        rows = db.execute("SELECT * FROM tickets ORDER BY rowid").fetchall()
        return [dict(row) for row in rows]


def get_ticket(ticket_id: UUID) -> dict | None:
    with _lock:
        row = db.execute(
            "SELECT * FROM tickets WHERE id = ?", (str(ticket_id),)
        ).fetchone()
        return dict(row) if row is not None else None
