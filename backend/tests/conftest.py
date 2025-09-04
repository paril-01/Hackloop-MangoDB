import sys
from pathlib import Path

# Ensure tests can import the backend package when running from the repo root
# Insert repository root (one level above 'backend') so `import backend` resolves
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
