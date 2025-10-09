# database.py

import sqlite3
import bcrypt
from datetime import datetime

DATABASE_NAME = "users.db"

# --- Database Connection ---
def get_db_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- Initialization Function ---
def check_db_exists():
    """Checks if the 'users' table exists and creates it if it doesn't."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone() is None:
            # Table does not exist, so create it
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP
                )
            """)
            conn.commit()
            print("Database: 'users' table created successfully.")
        
    except sqlite3.Error as e:
        print(f"Database Error during check/creation: {e}")
    finally:
        conn.close()

# --- User Management Functions ---

def add_user(username, email, password):
    """Adds a new user to the database."""
    check_db_exists() # Ensure table exists before inserting
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hash the password
        password_bytes = password.encode('utf-8')
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, datetime.now())
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Email or username already exists
        conn.close()
        return False
    except Exception as e:
        print(f"Error adding user: {e}")
        conn.close()
        return False

def check_email_exists(email):
    """Checks if an email is already registered."""
    check_db_exists() # Ensure table exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def check_user(email, password):
    """Checks user credentials for login."""
    check_db_exists() # Ensure table exists
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check by email first
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        # Verify the password
        password_hash = user['password_hash'].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), password_hash):
            return user
    
    return None

def update_password(email, new_password):
    """Updates the user's password."""
    check_db_exists() # Ensure table exists
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hash the new password
        password_bytes = new_password.encode('utf-8')
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute(
            "UPDATE users SET password_hash = ?, created_at = ? WHERE email = ?",
            (password_hash, datetime.now(), email)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False

# NOTE: You must call check_db_exists() once at the start of your app
# or rely on it being called before any other DB operation.