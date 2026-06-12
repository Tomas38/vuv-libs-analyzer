"""Console launcher for the Streamlit app."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    completed = subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())