"""Run alembic migrations (upgrade head) and then seed the database."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run_migrations():
    # Run alembic upgrade head
    cmd = [sys.executable, '-m', 'alembic', 'upgrade', 'head']
    print('Running:', ' '.join(cmd))
    subprocess.check_call(cmd, cwd=str(ROOT))

def run_seed():
    cmd = [sys.executable, str(ROOT / 'scripts' / 'seed_db.py')]
    print('Seeding with:', ' '.join(cmd))
    subprocess.check_call(cmd)

if __name__ == '__main__':
    run_migrations()
    run_seed()
