import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LIB_DIR = PROJECT_ROOT / "lib"

for path in [PROJECT_ROOT, LIB_DIR]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))