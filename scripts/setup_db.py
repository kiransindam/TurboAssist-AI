"""Setup SQLite database with schema and seed data."""
import sqlite3
from pathlib import Path


def setup_database():
    """Create and populate the maintenance database."""
    db_path = Path("data/maintenance.db")
    db_path.parent.mkdir(exist_ok=True)
    
    # Remove existing DB
    if db_path.exists():
        db_path.unlink()
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Read and execute SQL files in order
    sql_dir = Path("sql")
    sql_files = [
        "01_schema.sql",
        "02_seed_data.sql",
        "04_views.sql",
        "05_stored_procs.sql",
        "06_indexes.sql",
    ]
    
    for sql_file in sql_files:
        sql_path = sql_dir / sql_file
        if sql_path.exists():
            print(f"Executing {sql_file}...")
            with open(sql_path) as f:
                sql = f.read()
            cursor.executescript(sql)
    
    conn.commit()
    conn.close()
    print(f"✅ Database created at {db_path}")


if __name__ == "__main__":
    setup_database()
