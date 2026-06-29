import io
import csv
from os import PathLike

import numpy as np


def _read_hamamatsu_stream(
    csv_file,
    marker: str = "[MEAS_DATA]",
    skip_lines_after_marker: int = 1,
    skip_first_n_cols: int = 6,
):
    for _, line in enumerate(csv_file):
        if line.strip() == marker:
            break
    else:
        raise ValueError(f"Marker '{marker}' not found in file")

    for _ in range(int(skip_lines_after_marker)):
        next(csv_file, None)

    csv_reader = csv.reader(csv_file, delimiter=",")
    data_rows = []
    pixel_ids = []

    for row in csv_reader:
        if not any((field or "").strip() for field in row):
            break

        pixel_ids.append(int(float(row[0].strip())))

        tail = row[skip_first_n_cols:]

        converted = []
        for v in tail:
            v = v.strip()
            if v == "":
                converted.append(-1)   # or raise error
            else:
                converted.append(int(v))

        data_rows.append(converted)

    max_cols = max(len(r) for r in data_rows)

    array = np.zeros((len(data_rows), max_cols), dtype=np.int64)

    for i, row in enumerate(data_rows):
        array[i, :len(row)] = np.array(row, dtype=np.int64)

    return np.array(pixel_ids, dtype=np.int64), array.transpose()


def ham_read_file(
    file_obj,
    marker: str = "[MEAS_DATA]",
    skip_lines_after_marker: int = 1,
    skip_first_n_cols: int = 6,
) -> tuple[np.ndarray, np.ndarray]:
    """Read Hamamatsu-style data from a file path or file-like object."""

    if isinstance(file_obj, (str, bytes, PathLike)):
        with open(file_obj, "r", encoding="utf-8") as csv_file:
            return _read_hamamatsu_stream(
                csv_file,
                marker=marker,
                skip_lines_after_marker=skip_lines_after_marker,
                skip_first_n_cols=skip_first_n_cols,
            )

    if hasattr(file_obj, "seek"):
        file_obj.seek(0)

    raw_data = file_obj.read()
    if isinstance(raw_data, bytes):
        text_stream = io.StringIO(raw_data.decode("utf-8"))
    else:
        text_stream = io.StringIO(raw_data)

    return _read_hamamatsu_stream(
        text_stream,
        marker=marker,
        skip_lines_after_marker=skip_lines_after_marker,
        skip_first_n_cols=skip_first_n_cols,
    )


def ham_reader(
    filename: str,
    marker: str = "[MEAS_DATA]",
    skip_lines_after_marker: int = 1,
    skip_first_n_cols: int = 6,
) -> tuple[np.ndarray, np.ndarray]:
    """Read a Hamamatsu-style CSV-like file and return measurement data."""

    return ham_read_file(
        filename,
        marker=marker,
        skip_lines_after_marker=skip_lines_after_marker,
        skip_first_n_cols=skip_first_n_cols,
    )
