# utils/auth.py
import bcrypt
from utils.aws_db import get_connection
import streamlit as st

def hash_password(pwd: str) -> str:
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False

def create_admin(name, email, password, company_name=None):
    conn = get_connection()
    cur = conn.cursor()
    # create company if provided
    company_id = None
    if company_name:
        cur.execute("INSERT IGNORE INTO companies (company_name) VALUES (%s)", (company_name,))
        conn.commit()
        cur.execute("SELECT id FROM companies WHERE company_name=%s", (company_name,))
        company_id = cur.fetchone()[0]
    pw_hash = hash_password(password)
    cur.execute("INSERT INTO admins (name, email, password_hash, company_id) VALUES (%s,%s,%s,%s)",
                (name, email, pw_hash, company_id))
    conn.commit()
    cur.close()
    return True

def get_admin_by_email(email):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM admins WHERE email=%s", (email,))
    row = cur.fetchone()
    cur.close()
    return row

def admin_login(email, password):
    admin = get_admin_by_email(email)
    if not admin:
        return None
    if verify_password(password, admin["password_hash"]):
        return admin
    return None

def reset_admin_password(email, new_password):
    conn = get_connection()
    cur = conn.cursor()
    pw_hash = hash_password(new_password)
    cur.execute("UPDATE admins SET password_hash=%s WHERE email=%s", (pw_hash, email))
    conn.commit()
    cur.close()
    return True
