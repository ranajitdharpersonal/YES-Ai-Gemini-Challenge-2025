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
# database.py - check_db_exists function (Final Version)

def check_db_exists():
    """Checks if the necessary tables exist, creates them, and ensures a demo user exists."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Create Users Table (if not exists)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone() is None:
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP
                )
            """)

        # 2. Create Chat History Table (if not exists)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_history'")
        if cursor.fetchone() is None:
            cursor.execute("""
                CREATE TABLE chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            
        # 3. Create Permanent Demo User (The Fix for 'Sleep' Problem)
        # Only create if the email 'demo@yesai.com' does NOT exist
        cursor.execute("SELECT id FROM users WHERE email = 'demo@yesai.com'")
        if cursor.fetchone() is None:
            # Hash 'demopass' securely
            password_bytes = 'demopass'.encode('utf-8')
            password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                ('DemoUser', 'demo@yesai.com', password_hash, datetime.now())
            )
            print("Database: Permanent Demo User Created for Streamlit restarts.")
            
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database Error during check/creation: {e}")
    finally:
        conn.close()

# Note: The rest of your database.py file (get_db_connection, add_user, clear_history, etc.) 
# must remain exactly as it was provided in the previous step.

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
        conn.close()
        return False
    except Exception as e:
        print(f"Error adding user: {e}")
        conn.close()
        return False

def check_email_exists(email):
    """Checks if an email is already registered."""
    check_db_exists()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def check_user(email, password):
    """Checks user credentials for login."""
    check_db_exists()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        password_hash = user['password_hash'].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), password_hash):
            return user
    
    return None

def update_password(email, new_password):
    """Updates the user's password."""
    check_db_exists()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
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

# --- Chat History Functions (FULL IMPLEMENTATION) ---

def save_message(user_id, role, content):
    """Saves a message to the chat history."""
    check_db_exists() 
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chat_history (user_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, role, content, datetime.now())
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving message: {e}")
        return False

def load_history(user_id):
    """Loads all chat messages for a specific user."""
    check_db_exists() 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM chat_history WHERE user_id = ? ORDER BY id", (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history

def clear_history(user_id):
    """Deletes all chat messages for a specific user."""
    # Eitai sei missing function ja app.py call korchilo!
    check_db_exists() 
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error clearing history: {e}")
        return Falsev