"""SQLite persistence: songs, versions, and conversation history."""
import sqlite3
import json
from datetime import datetime
import config


def _conn():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS versions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        song_id INTEGER NOT NULL,
        version_num INTEGER NOT NULL,
        lyrics TEXT,
        style_prompt TEXT,
        suno_job_id TEXT,
        audio_path TEXT,
        status TEXT DEFAULT 'pending',
        is_final INTEGER DEFAULT 0,
        metadata TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (song_id) REFERENCES songs(id)
    );
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        song_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (song_id) REFERENCES songs(id)
    );
    """)
    conn.commit()
    conn.close()


# --- songs ---

def create_song(title: str) -> int:
    conn = _conn()
    cur = conn.execute(
        "INSERT INTO songs (title, created_at) VALUES (?, ?)",
        (title, datetime.utcnow().isoformat()),
    )
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid


def list_songs():
    conn = _conn()
    rows = conn.execute("SELECT * FROM songs ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_song(song_id: int):
    conn = _conn()
    row = conn.execute("SELECT * FROM songs WHERE id=?", (song_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# --- versions ---

def add_version(song_id, lyrics, style_prompt, suno_job_id=None, metadata=None):
    conn = _conn()
    version_num = conn.execute(
        "SELECT COALESCE(MAX(version_num), 0) + 1 FROM versions WHERE song_id=?",
        (song_id,),
    ).fetchone()[0]
    cur = conn.execute(
        """INSERT INTO versions
           (song_id, version_num, lyrics, style_prompt, suno_job_id, status, metadata, created_at)
           VALUES (?, ?, ?, ?, ?, 'submitted', ?, ?)""",
        (song_id, version_num, lyrics, style_prompt, suno_job_id,
         json.dumps(metadata or {}), datetime.utcnow().isoformat()),
    )
    conn.commit()
    vid = cur.lastrowid
    conn.close()
    return vid, version_num


def update_version(version_id: int, **fields):
    if not fields:
        return
    conn = _conn()
    cols = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE versions SET {cols} WHERE id=?",
                 (*fields.values(), version_id))
    conn.commit()
    conn.close()


def list_versions(song_id: int):
    conn = _conn()
    rows = conn.execute(
        "SELECT * FROM versions WHERE song_id=? ORDER BY version_num",
        (song_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_version(song_id: int, version_num: int):
    conn = _conn()
    row = conn.execute(
        "SELECT * FROM versions WHERE song_id=? AND version_num=?",
        (song_id, version_num),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def mark_final(song_id: int, version_num: int) -> bool:
    conn = _conn()
    v = conn.execute(
        "SELECT id FROM versions WHERE song_id=? AND version_num=?",
        (song_id, version_num),
    ).fetchone()
    if not v:
        conn.close()
        return False
    conn.execute("UPDATE versions SET is_final=0 WHERE song_id=?", (song_id,))
    conn.execute("UPDATE versions SET is_final=1 WHERE id=?", (v["id"],))
    conn.commit()
    conn.close()
    return True


# --- messages (conversation history per song) ---

def save_message(song_id: int, role: str, content):
    conn = _conn()
    conn.execute(
        "INSERT INTO messages (song_id, role, content, created_at) VALUES (?, ?, ?, ?)",
        (song_id, role, json.dumps(content), datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def load_messages(song_id: int):
    conn = _conn()
    rows = conn.execute(
        "SELECT role, content FROM messages WHERE song_id=? ORDER BY id",
        (song_id,),
    ).fetchall()
    conn.close()
    return [{"role": r["role"], "content": json.loads(r["content"])} for r in rows]