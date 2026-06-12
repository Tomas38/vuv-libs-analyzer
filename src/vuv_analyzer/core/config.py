"""Configuration helpers."""

from __future__ import annotations

import json
from pathlib import Path


def default_config_path() -> Path:
    return Path(__file__).resolve().parents[3] / "config" / "default_config.json"


def load_config(config_path: str | Path) -> dict:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def save_config(config: dict, config_path: str | Path) -> None:
    path = Path(config_path)
    with path.open("w", encoding="utf-8") as file_handle:
        json.dump(config, file_handle, indent=2)


def update_config(config: dict, key: str, value) -> dict:
    config[key] = value
    return config