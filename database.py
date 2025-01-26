from dotenv import load_dotenv
load_dotenv()  

import psycopg2
import os
from urllib.parse import urlparse

def init_db():
   
    connection_string = os.getenv("DATABASE_URL")
    
    if not connection_string:
        raise ValueError("DATABASE_URL environment variable is not set.")
    
    # Parse the connection string
    parsed = urlparse(connection_string)
    
    # Connect to the database with SSL
    conn = psycopg2.connect(
        dbname=parsed.path[1:],  # Remove the leading '/'
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port,
        sslmode="require"  # Enable SSL
    )
    
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS texts
                 (id SERIAL PRIMARY KEY, 
                  content TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    return conn

# Initialize the database
conn = init_db()