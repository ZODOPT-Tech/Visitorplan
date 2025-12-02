# utils/aws_db.py
import boto3
import mysql.connector
from botocore.exceptions import ClientError
import streamlit as st

# Secret ARN
SECRET_ARN = "arn:aws:secretsmanager:ap-south-1:034362058776:secret:Wheelbrand-zM6npS"
AWS_REGION = "ap-south-1"

def parse_kv_string(secret_str: str):
    creds = {}
    for line in secret_str.splitlines():
        if not line.strip():
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
def get_db_credentials():
    """
    Get DB credentials from AWS Secrets Manager.
    Supports key=value pair string returns.
    """
    try:
        client = boto3.client("secretsmanager", region_name=AWS_REGION)
        resp = client.get_secret_value(SecretId=SECRET_ARN)
        secret = resp.get("SecretString", "")
        # try JSON -> else parse key=value
        import json
        try:
            parsed = json.loads(secret)
            # accept multiple common keys
            host = parsed.get("host") or parsed.get("DB_HOST") or parsed.get("HOST")
            user = parsed.get("username") or parsed.get("user") or parsed.get("DB_USER")
            password = parsed.get("password") or parsed.get("DB_PASSWORD")
            database = parsed.get("database") or parsed.get("dbname") or parsed.get("DB_NAME")
            return {"host": host, "user": user, "password": password, "database": database}
        except Exception:
            return {
                "host": parse_kv_string(secret).get("host") or parse_kv_string(secret).get("DB_HOST"),
                "user": parse_kv_string(secret).get("username") or parse_kv_string(secret).get("DB_USER"),
                "password": parse_kv_string(secret).get("password") or parse_kv_string(secret).get("DB_PASSWORD"),
                "database": parse_kv_string(secret).get("database") or parse_kv_string(secret).get("DB_NAME"),
            }
    except ClientError as e:
        st.error(f"Secrets Manager error: {e}")
        st.stop()

@st.cache_resource(ttl=None)
def get_connection():
    creds = get_db_credentials()
    if not creds or not all([creds.get("host"), creds.get("user"), creds.get("password"), creds.get("database")]):
        st.error("DB credentials missing or incomplete. Check Secrets Manager format.")
        st.stop()
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
        st.error(f"MySQL connection error: {e}")
        st.stop()

def init_db():
    """Idempotent creation of required tables."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(255) NOT NULL UNIQUE,
        api_key VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """)
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
    cur.execute("""
    CREATE TABLE IF NOT EXISTS visitor_identity (
        id INT AUTO_INCREMENT PRIMARY KEY,
        visitor_id INT,
        id_type VARCHAR(100),
        id_number VARCHAR(255),
        id_image LONGBLOB,
        visitor_photo LONGBLOB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(visitor_id) REFERENCES visitors(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)
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
        photo_blob LONGBLOB,
        signature_blob LONGBLOB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(visitor_id) REFERENCES visitors(id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)
    conn.commit()
    cur.close()
