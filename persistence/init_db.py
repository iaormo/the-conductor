#!/usr/bin/env python3
"""init_db.py — Initialize the-conductor audit database."""
from severity_logger import init_db
from pathlib import Path

db_path = Path(__file__).parent / "audit.db"
init_db(db_path)
print(f"Database initialized: {db_path}")
