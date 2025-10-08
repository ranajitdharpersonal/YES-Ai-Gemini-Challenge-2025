import sqlite3
import bcrypt

DATABASE_NAME = "users.db"

def get_db_connection():
    """Database connection toiri kore ebong return kore."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# --- (baki shob function jemon chilo temon-i ache) ---
# ...
# ...
# ... (add_user, check_user, etc.)
def initialize_database():
    """Database'e dorkari table gulo toiri kore."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # User table with password as BLOB
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    conn.commit()
    conn.close()
    print("Database tables created successfully.")

def add_user(username, email, password):
    """Notun user'ke database-e add kore."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Password'ke secure vabe hash kora hocche (eta already bytes return kore)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user(email, password):
    """User'er email o password check kore."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    
    # Ekhon user['password'] already bytes, tai ar kono change dorkar nei
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return user
    return None

def save_message(user_id, role, content):
    """Chat message'ke database-e save kore."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, role, content) VALUES (?, ?, ?)", 
                   (user_id, role, content))
    conn.commit()
    conn.close()

def load_history(user_id):
    """Ekjon user'er purono chat history load kore."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT role, content FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC", (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history

def clear_history(user_id):
    """Ekjon user'er shob chat history database theke delete kore dey."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    print(f"Chat history cleared for user_id: {user_id}")
    return True

# --- NOTUN FUNCTION ADD KORA HOLO ---

def check_email_exists(email):
    """Check kore je kono email aage thekei registered ache kina."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user_exists = cursor.fetchone()
    conn.close()
    return user_exists is not None

def update_password(email, new_password):
    """Ekjon user'er password database-e update kore."""
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, email))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()

