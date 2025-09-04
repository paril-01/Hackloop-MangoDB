"""Mark alembic revision as applied by inserting into alembic_version table."""
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / 'replika.db'
rev = '0002_initial'

conn = sqlite3.connect(str(DB))
cur = conn.cursor()
try:
    cur.execute('CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32) NOT NULL)')
    cur.execute('DELETE FROM alembic_version')
    cur.execute('INSERT INTO alembic_version (version_num) VALUES (?)', (rev,))
    conn.commit()
    print('Inserted alembic version', rev)
finally:
    conn.close()
