"""File loading helpers."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from vuv_analyzer.core.ham_reader import ham_reader


def is_hamamatsu_file(filepath: str | Path) -> bool:
    path = Path(filepath)
    with path.open("r", encoding="utf-8", errors="ignore") as file_handle:
        for _ in range(60):
            line = file_handle.readline()
            if not line:
                break
            if line.strip() == "[MEAS_DATA]":
                return True
    return False


def load_csv_matrix(filepath: str | Path) -> np.ndarray:
    dataframe = pd.read_csv(filepath)
    numeric = dataframe.select_dtypes(include=["number"])
    if numeric.empty:
        return dataframe.apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
    return numeric.to_numpy(dtype=float)


def load_hamamatsu_matrix(filepath: str | Path) -> np.ndarray:
    return ham_reader(str(filepath))


def load_measurement_matrix(filepath: str | Path, use_hamamatsu: bool = True) -> np.ndarray:
    path = Path(filepath)
    if use_hamamatsu and is_hamamatsu_file(path):
        return load_hamamatsu_matrix(path)
    return load_csv_matrix(path)