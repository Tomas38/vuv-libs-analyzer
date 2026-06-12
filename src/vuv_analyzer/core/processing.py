"""Data processing helpers."""

from __future__ import annotations

import numpy as np


def build_wavelength_axis(pixel_count: int, config: dict) -> np.ndarray:
    axis_config = config.get("wavelength_axis", {})
    start_nm = float(axis_config.get("start_nm", 120.0))
    end_nm = float(axis_config.get("end_nm", 220.0))
    return np.linspace(start_nm, end_nm, pixel_count)


def extract_trace(data: np.ndarray, trace_index: int = 0, orientation: str = "row") -> np.ndarray:
    array = np.asarray(data)
    if array.ndim == 1:
        return array.astype(float)

    if orientation == "column":
        trace_index = max(0, min(trace_index, array.shape[1] - 1))
        return array[:, trace_index].astype(float)

    trace_index = max(0, min(trace_index, array.shape[0] - 1))
    return array[trace_index, :].astype(float)


def apply_conversion(data: np.ndarray, config: dict) -> np.ndarray:
    intensity_scale = float(config.get("data_conversion", {}).get("intensity_scale", 1.0))
    return np.asarray(data, dtype=float) * intensity_scale


def calculate_statistics(data: np.ndarray) -> dict:
    values = np.asarray(data, dtype=float)
    return {
        "mean": float(np.nanmean(values)),
        "std": float(np.nanstd(values)),
        "min": float(np.nanmin(values)),
        "max": float(np.nanmax(values)),
    }