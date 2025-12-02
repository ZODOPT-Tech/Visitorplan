import bcrypt
from utils.aws_db import get_connection
import streamlit as st
from mysql.connector import Error as MySQLError

# --- Password Hashing Functions ---

def hash_password(pwd: str) -> str:
    """Hashes a plaintext password using bcrypt."""
    # bcrypt requires bytes, decode result back to string for storage
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    """Verifies a plaintext password against a hashed one."""
    try:
        # Checkpw handles the salt internally
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception as e:
        # Handle cases where the hash might be invalid/corrupt
        st.error(f"Password verification error: {e}")
        return False

# --- Admin Management Functions ---

def create_admin(name, email, password, company_name=None) -> bool:
    """
    Creates a new company (if needed) and a new admin user.
    Returns True on success, False on failure (e.g., duplicate email).
    """
    conn = get_connection()
    if conn is None:
        return False

    cur = conn.cursor()
    try:
        company_id = None
        
        if company_name:
            # 1. Create company if it doesn't exist
            cur.execute("INSERT IGNORE INTO companies (company_name) VALUES (%s)", (company_name,))
            conn.commit() 
            
            # 2. Get the company ID (either newly created or existing)
            cur.execute("SELECT id FROM companies WHERE company_name=%s", (company_name,))
            result = cur.fetchone()
            if result:
                company_id = result[0]
            else:
                st.error("Error: Could not retrieve company ID after insertion.")
                return False

        # 3. Insert new admin
        pw_hash = hash_password(password)
        cur.execute(
            "INSERT INTO admins (name, email, password_hash, company_id) VALUES (%s, %s, %s, %s)",
            (name, email, pw_hash, company_id)
        )
        conn.commit()
        return True
        
    except MySQLError as e:
        # Handle duplicate email (MySQL error 1062) or other database issues
        if e.errno == 1062: # Duplicate entry error code
            st.warning("Registration failed: This email address is already in use.")
        else:
            st.error(f"Database error during admin creation: {e}")
        conn.rollback() # Ensure atomicity of the operation
        return False
    finally:
        if cur:
            cur.close()


def get_admin_by_email(email):
    """Retrieves admin user data by email."""
    conn = get_connection()
    if conn is None:
        return None
        
    cur = conn.cursor(dictionary=True) # Returns results as a dictionary
    try:
        # Select specific, necessary columns
        cur.execute("SELECT id, name, email, password_hash, company_id FROM admins WHERE email=%s", (email,))
        row = cur.fetchone()
        return row
    except MySQLError as e:
        st.error(f"Database error while fetching admin: {e}")
        return None
    finally:
        if cur:
            cur.close()

def admin_login(email, password):
    """Attempts to log in an admin user. Returns admin dictionary without hash or None."""
    admin = get_admin_by_email(email)
    if not admin:
        return None # Email not found
        
    # Check password against stored hash
    if verify_password(password, admin["password_hash"]):
        # Remove hash before returning user data for security
        del admin["password_hash"]
        return admin
        
    return None # Password mismatch

def reset_admin_password(email, new_password) -> bool:
    """Hashes and updates an admin's password. Returns True on success."""
    conn = get_connection()
    if conn is None:
        return False
        
    cur = conn.cursor()
    try:
        pw_hash = hash_password(new_password)
        cur.execute("UPDATE admins SET password_hash=%s WHERE email=%s", (pw_hash, email))
        
        if cur.rowcount == 0:
            # No rows were affected (email not found)
            st.warning("Password reset failed: Admin email not found.")
            return False
            
        conn.commit()
        return True
        
    except MySQLError as e:
        st.error(f"Database error during password reset: {e}")
        conn.rollback()
        return False
    finally:
        if cur:
            cur.close()
