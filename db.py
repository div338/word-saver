import os
import sqlite3
from contextlib import contextmanager

from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS travel_samples (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fetched_at TEXT NOT NULL,
    travel_time_seconds INTEGER NOT NULL,
    traffic_delay_seconds INTEGER NOT NULL,
    length_meters INTEGER NOT NULL
);
"""


@contextmanager
def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute(SCHEMA)
        conn.commit()


def insert_sample(fetched_at, travel_time_seconds, traffic_delay_seconds, length_meters):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO travel_samples (fetched_at, travel_time_seconds, traffic_delay_seconds, length_meters) "
            "VALUES (?, ?, ?, ?)",
            (fetched_at, travel_time_seconds, traffic_delay_seconds, length_meters),
        )
        conn.commit()


def fetch_all_samples():
    with get_conn() as conn:
        cursor = conn.execute(
            "SELECT fetched_at, travel_time_seconds, traffic_delay_seconds, length_meters "
            "FROM travel_samples ORDER BY fetched_at"
        )
        return cursor.fetchall()
