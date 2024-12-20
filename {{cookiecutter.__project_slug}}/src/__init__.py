"""Source code."""

import sys
from pathlib import Path


src_path = Path(__file__).parent
if src_path not in sys.path:
    sys.path.insert(1, str(src_path))
