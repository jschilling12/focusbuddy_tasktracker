from pydoc import resolve
import sqlite3
import os
from pathlib import Path
from typing import Optional

def connect_db(db_path: Optional[str] = None):

    if db_path is None:
        db_path = os.environ.get(
            "DATABASE_NAME"
            str((Path(__file__).parent.parent / "time_tracking.db").resolve()),
        )
    return sqlite3.connect(db_path)

def init_db():
    with connect_db()as conn:
        cursor = conn.cursor()
        
        #Time Tracking Table
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS time_tracking (
                       id INTEGER PRIMARY KEY,
                       app_name TEXT,
                       date INTEGER, 
                       time_tracked INTEGER DEFAULT 0)
                       UNIQUE(app_name, date)
                       ''')
        


    