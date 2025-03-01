import sqlite3

def connect_db():
    """Establish connection to SQLite database and return connection and cursor."""
    conn = sqlite3.connect("cve_database.db")
    cursor = conn.cursor()
    return conn, cursor

def remove_duplicates():
    """Remove duplicate CVE entries while keeping the latest record."""
    conn, cursor = connect_db()

    try:
        # Ensure the table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cve_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cve_id TEXT UNIQUE NOT NULL,
                description TEXT,
                severity TEXT,
                published_date TEXT
            )
        """)
        conn.commit()

        # Identify and delete duplicate CVEs, keeping the most recent one
        cursor.execute("""
            DELETE FROM cve_records
            WHERE id NOT IN (
                SELECT MIN(id) 
                FROM cve_records 
                GROUP BY cve_id
            )
        """)

        # Commit changes and close connection
        conn.commit()
        print("✅ Duplicate CVE records removed successfully!")

    except sqlite3.Error as e:
        print(f"❌ Error: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    remove_duplicates()
