import os
import sqlite3

def get_db_connection():
    db_path = 'menu.db'
    if os.environ.get('RENDER'):
        db_path = '/tmp/menu.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conne)
