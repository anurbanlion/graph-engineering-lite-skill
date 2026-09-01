import sys
from pathlib import Path

# Add scripts/ to sys.path so `from lib.x import y` works.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
