"""
Health database layer — SQLite at ~/.openclaw/workspace/health/health.sqlite
"""
import sqlite3
import os
import json
import time
from datetime import datetime, date
from typing import Optional, List, Dict, Any

DB_PATH = os.path.expanduser("~/.openclaw/workspace/health/health.sqlite")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS checkins (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            date            TEXT NOT NULL UNIQUE,   -- YYYY-MM-DD
            timestamp       INTEGER NOT NULL,        -- unix epoch
            energy          INTEGER,                 -- 1-10
            pain_areas      TEXT,                    -- free text, comma-separated
            food            TEXT,                    -- what JT ate
            exercise        TEXT,                    -- description or "none"
            sleep_quality   INTEGER,                 -- 1-10 (last night)
            notes           TEXT,                    -- anything extra
            raw_response    TEXT                     -- original reply for debugging
        );

        CREATE TABLE IF NOT EXISTS weekly_reports (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            week_start  TEXT NOT NULL UNIQUE,        -- YYYY-MM-DD (Monday)
            generated   INTEGER NOT NULL,
            report_text TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def save_checkin(
    checkin_date: str,         # YYYY-MM-DD
    energy: Optional[int],
    pain_areas: Optional[str],
    food: Optional[str],
    exercise: Optional[str],
    sleep_quality: Optional[int],
    notes: Optional[str] = None,
    raw_response: Optional[str] = None,
) -> int:
    """Insert or replace a check-in. Returns the row id."""
    conn = get_conn()
    cur = conn.execute("""
        INSERT INTO checkins
            (date, timestamp, energy, pain_areas, food, exercise, sleep_quality, notes, raw_response)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            timestamp     = excluded.timestamp,
            energy        = excluded.energy,
            pain_areas    = excluded.pain_areas,
            food          = excluded.food,
            exercise      = excluded.exercise,
            sleep_quality = excluded.sleep_quality,
            notes         = excluded.notes,
            raw_response  = excluded.raw_response
    """, (
        checkin_date,
        int(time.time()),
        energy, pain_areas, food, exercise, sleep_quality, notes, raw_response
    ))
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id


def get_recent_checkins(days: int = 7) -> List[Dict[str, Any]]:
    """Return the most recent N days of check-ins, most recent first."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM checkins
        ORDER BY date DESC
        LIMIT ?
    """, (days,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_checkin(checkin_date: str) -> Optional[Dict[str, Any]]:
    conn = get_conn()
    row = conn.execute("SELECT * FROM checkins WHERE date = ?", (checkin_date,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_checkins() -> List[Dict[str, Any]]:
    conn = get_conn()
    rows = conn.execute("SELECT * FROM checkins ORDER BY date DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
