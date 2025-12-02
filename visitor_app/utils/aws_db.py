import boto3
import mysql.connector
from botocore.exceptions import ClientError
import streamlit as st
import json

# --- Configuration ---
# Secret ARN and AWS Region are environment-specific and should be treated as such
SECRET_ARN = "arn:aws:secretsmanager:ap-south-1:034362058776:secret:Wheelbrand-zM6npS"
AWS_REGION = "ap-south-1"


# --- Secrets Manager Helpers ---

def parse_kv_string(secret_str: str) -> dict:
    """Parses a multi-line key=value or key:value string into a dictionary."""
    creds = {}
    for line in secret_str.splitlines():
        line = line.strip()
        if not line:
            continue
            
        if "=" in line:
            k, v = line.split("=", 1)
        elif ":" in line:
            k, v = line.split(":", 1)
        else:
            continue
            
        creds[k.strip()] = v.strip()
    return creds

@st.cache_resource(ttl=3600)
def get_db_credentials() -> dict or None:
    """
    Retrieves and parses DB credentials from AWS Secrets Manager.
    Supports JSON or key=value string formats.
    """
    try:
        client = boto3.client("secretsmanager", region_name=AWS_REGION)
        resp = client.get_secret_value(SecretId=SECRET_ARN)
        secret = resp.get("SecretString", "")
        
        # Keys to check in the secret (prioritized)
        HOST_KEYS = ["host", "DB_HOST", "HOST"]
        USER_KEYS = ["username", "user", "DB_USER"]
        PASSWORD_KEYS = ["password", "DB_PASSWORD"]
        DATABASE_KEYS = ["database", "dbname", "DB_NAME"]

        def extract_creds(data: dict) -> dict:
            """Extracts common credential fields from a dictionary."""
            return {
                "host": next((data.get(k) for k in HOST_KEYS if data.get(k)), None),
                "user": next((data.get(k) for k in USER_KEYS if data.get(k)), None),
                "password": next((data.get(k) for k in PASSWORD_KEYS if data.get(k)), None),
                "database": next((data.get(k) for k in DATABASE_KEYS if data.get(k)), None),
            }

        # 1. Try JSON parsing
        try:
            parsed = json.loads(secret)
            return extract_creds(parsed)
        except json.JSONDecodeError:
            pass # Fall through to key=value parsing
            
        # 2. Try key=value parsing
        kv_parsed = parse_kv_string(secret)
        return extract_creds(kv_parsed)

    except ClientError as e:
        st.error(f"Secrets Manager error: Failed to retrieve secret {SECRET_ARN}. Details: {e}")
        st.stop()
        return None # Should be unreachable due to st.stop()


# --- Database Connection ---

@st.cache_resource(ttl=None)
def get_connection():
    """Establishes and caches a MySQL database connection."""
    creds = get_db_credentials()
    
    # Validation checks
    if not creds or not all(creds.get(k) for k in ["host", "user", "password", "database"]):
        st.error("DB credentials missing or incomplete. Check AWS Secrets Manager format.")
        st.stop()
        return None
        
    try:
        conn = mysql.connector.connect(
            host=creds["host"],
            user=creds["user"],
            password=creds["password"],
            database=creds["database"],
            autocommit=True,
            connection_timeout=10
        )
        return conn
    except mysql.connector.Error as e:
        st.error(f"MySQL connection error: Could not connect to the database. Details: {e}")
        st.stop()
        return None

# --- Database Initialization ---

def init_db():
    """Idempotent creation of required tables."""
    conn = get_connection()
    if conn is None:
        return # Cannot proceed without connection
        
    try:
        # Use a context manager for the cursor
        with conn.cursor() as cur:
            # Table definitions (kept as original, ensuring InnoDB engine and foreign keys)
            
            # 1. Companies Table
            cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL UNIQUE,
                api_key VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
            """)
            
            # 2. Admins Table
            cur.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255) UNIQUE,
                password_hash VARCHAR(255),
                company_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(company_id) REFERENCES companies(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
            """)
            
            # 3. Visitors Table
            cur.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(50),
                company_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(company_id) REFERENCES companies(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
            """)
            
            # 4. Visitor Identity Table (For ID documents and visitor photos)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS visitor_identity (
                id INT AUTO_INCREMENT PRIMARY KEY,
                visitor_id INT,
                id_type VARCHAR(100),
                id_number VARCHAR(255),
                id_image LONGBLOB,      -- Stores ID image data
                visitor_photo LONGBLOB, -- Stores live capture photo
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(visitor_id) REFERENCES visitors(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
            """)
            
            # 5. Visitor Details Table (Visit Information)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS visitor_details (
                id INT AUTO_INCREMENT PRIMARY KEY,
                visitor_id INT,
                visit_type VARCHAR(100),
                from_company VARCHAR(255),
                department VARCHAR(255),
                designation VARCHAR(255),
                organization_address TEXT,
                address_line1 VARCHAR(255),
                city VARCHAR(150),
                state VARCHAR(150),
                postal_code VARCHAR(50),
                country VARCHAR(100),
                gender VARCHAR(50),
                purpose TEXT,
                person_to_meet VARCHAR(255),
                belongings TEXT,
                photo_blob LONGBLOB,    -- Redundant if stored in visitor_identity, verify usage
                signature_blob LONGBLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(visitor_id) REFERENCES visitors(id) ON DELETE CASCADE
            ) ENGINE=InnoDB;
            """)
            
        # Commit changes after all DDL statements
        conn.commit()
        
    except mysql.connector.Error as e:
        # Catch and report errors during table creation (e.g., syntax errors)
        st.error(f"MySQL initialization error: Failed to create tables. Details: {e}")
        conn.rollback() # Ensure transaction is rolled back on error
