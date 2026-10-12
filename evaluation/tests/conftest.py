"""
Pytest configuration ensuring local project root has absolute priority in sys.path.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Remove any other scratch directories from sys.path to prevent module collisions
for p in list(sys.path):
    if "ai-marketing-growth-os" in p:
        sys.path.remove(p)
