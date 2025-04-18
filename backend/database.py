import sqlite3
from datetime import datetime
from typing import List, Optional
import os

DATABASE_NAME = "creative_assistant.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DATABASE_NAME)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_db_and_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS creations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                content_type TEXT NOT NULL,
                generated_text TEXT,
                timestamp DATETIME NOT NULL
            )
        """)
        conn.commit()
        print("Base de datos y tabla 'creations' aseguradas.")
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")
    finally:
        if conn:
            conn.close()

def add_creation(prompt: str, content_type: str, generated_text: Optional[str] = None) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()
    timestamp = datetime.now()
    try:
        cursor.execute(
            "INSERT INTO creations (prompt, content_type, generated_text, timestamp) VALUES (?, ?, ?, ?)",
            (prompt, content_type, generated_text, timestamp)
        )
        conn.commit()
        creation_id = cursor.lastrowid
        print(f"Creación añadida con ID: {creation_id}")
        return creation_id
    except sqlite3.Error as e:
        print(f"Error al añadir creación: {e}")
        conn.rollback()
        return -1
    finally:
        conn.close()

def get_all_creations() -> List[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, prompt, content_type, generated_text, timestamp FROM creations ORDER BY timestamp DESC")
        creations = cursor.fetchall()
        return [dict(row) for row in creations]
    except sqlite3.Error as e:
        print(f"Error al obtener creaciones: {e}")
        return []
    finally:
        conn.close()
