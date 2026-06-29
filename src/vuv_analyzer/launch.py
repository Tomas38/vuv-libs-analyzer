import subprocess
from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parent


def main():
    app = BASE_DIR / "app.py"

    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app)
    ])