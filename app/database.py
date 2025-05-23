# app/database.py

import sqlite3
import os
from datetime import datetime

DB_DIR  = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
DB_PATH = os.path.join(DB_DIR, "chatbot_logs_v2.db")

def create_table():
    """
    Create the 'logs' table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            question TEXT NOT NULL,
            context TEXT,
            answer TEXT NOT NULL,
            response_time REAL,
            confidence_score REAL,
            bleu REAL,
            rouge REAL,
            evaluation_score REAL
        )
    """)
    conn.commit()
    conn.close()

def reset_table():
    """
    Drop the old 'logs' table (if any) and recreate it fresh.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS logs")
    conn.commit()
    conn.close()
    # Now recreate with the correct schema
    create_table()

def log_qa_interaction(
    question: str,
    answer: str,
    response_time: float,
    evaluation_score: float = None,
    context: str = None,
    confidence_score: float = None,
    bleu_score: float = None,
    rouge_score: float = None,
):
    """
    Append a new interaction to the 'logs' table.
    """
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    timestamp = datetime.utcnow().isoformat()

    cur.execute("""
        INSERT INTO logs
          (timestamp, question, context, answer,
           response_time, confidence_score,
           bleu, rouge, evaluation_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        question,
        context,
        answer,
        response_time,
        confidence_score,
        bleu_score,
        rouge_score,
        evaluation_score
    ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # For manual testing: reset + create fresh logs table
    reset_table()
    print("✅ 'logs' table has been reset.")
