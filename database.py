from dbm import sqlite3
import os
import logging
import psycopg2  # Use mysql.connector for MySQL
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
from backend.models import CVEEntry
from flask_sqlalchemy import SQLAlchemy


def init_db():
    """Initialize the database with the required table schema."""
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS cve_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cve_id TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        published_date TEXT NOT NULL,
        severity TEXT NOT NULL
    );
    """)
    db.commit()
    
def init_db(app):
    db.init_app(app) # type: ignore

def get_db():
    """Establish a database connection."""
    db = sqlite3.connect("cve_database.db")
    db.row_factory = sqlite3.Row
    return db



# Database Configuration
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "cve_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),  # 3306 for MySQL
}

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_db_connection():
    """Establish and return a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logging.info("Database connection successful")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return None


def create_cve_table():
    """Creates the CVE table if it does not exist."""
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cve_data (
            id SERIAL PRIMARY KEY,
            cve_id TEXT UNIQUE NOT NULL,
            description TEXT,
            published_date TIMESTAMP,
            last_modified_date TIMESTAMP,
            cvss_score REAL,
            severity TEXT
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("CVE table created successfully.")


def insert_cve_data(cve_id, description, published_date, last_modified_date, cvss_score, severity):
    """Inserts a CVE record into the database, ignoring duplicates."""
    conn = get_db_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO cve_data (cve_id, description, published_date, last_modified_date, cvss_score, severity)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (cve_id) DO NOTHING;
        """, (cve_id, description, published_date, last_modified_date, cvss_score, severity))
        
        conn.commit()
        logging.info(f"CVE {cve_id} inserted successfully.")
        return True
    except Exception as e:
        logging.error(f"Error inserting CVE {cve_id}: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def fetch_cve_by_id(cve_id):
    """Fetch a specific CVE record by its ID."""
    conn = get_db_connection()
    if not conn:
        return None

    cursor = conn.cursor(cursor_factory=DictCursor)
    
    cursor.execute("SELECT * FROM cve_data WHERE cve_id = %s", (cve_id,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return dict(result) if result else None


def fetch_cves_by_year(year):
    """Fetch all CVEs for a specific year."""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor(cursor_factory=DictCursor)
    
    cursor.execute("SELECT * FROM cve_data WHERE EXTRACT(YEAR FROM published_date) = %s", (year,))
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return [dict(row) for row in results]


def fetch_cves_by_score(min_score, max_score):
    """Fetch CVEs within a specific CVSS score range."""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor(cursor_factory=DictCursor)
    
    cursor.execute("SELECT * FROM cve_data WHERE cvss_score BETWEEN %s AND %s", (min_score, max_score))
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return [dict(row) for row in results]


def fetch_recent_cves(days):
    """Fetch CVEs modified in the last 'N' days."""
    conn = get_db_connection()
    if not conn:
        return []

    cursor = conn.cursor(cursor_factory=DictCursor)
    
    cursor.execute("""
        SELECT * FROM cve_data 
        WHERE last_modified_date >= NOW() - INTERVAL '%s days'
    """, (days,))
    
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return [dict(row) for row in results]


if __name__ == "__main__":
    create_cve_table()  # Create the table when running this file
