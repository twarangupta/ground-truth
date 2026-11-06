"""Database helpers. Phase 0 only needs a reachability check."""

import psycopg


def check_database(database_url: str, timeout_seconds: int = 2) -> bool:
    """Return True if Postgres accepts a connection and answers a trivial query."""
    try:
        with psycopg.connect(database_url, connect_timeout=timeout_seconds) as conn:
            conn.execute("SELECT 1")
    except psycopg.Error:
        return False
    return True
