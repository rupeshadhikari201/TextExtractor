import sqlite3

def init_db():
    """Initialize the SQLite database with auto-incrementing IDs."""
    conn = sqlite3.connect('text_storage.db', check_same_thread=False)
    c = conn.cursor()
    
    # Create table with auto-incrementing integer ID
    c.execute('''CREATE TABLE IF NOT EXISTS texts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  content TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    return conn

# Initialize the database
conn = init_db()