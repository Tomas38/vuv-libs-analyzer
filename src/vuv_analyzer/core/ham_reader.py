import csv

import numpy as np


def ham_reader(
    filename: str,
    marker: str = "[MEAS_DATA]",
    skip_lines_after_marker: int = 1,
    skip_first_n_cols: int = 6,
) -> np.ndarray:
    """Read a Hamamatsu-style CSV-like file and return measurement data."""

    with open(filename, "r", encoding="utf-8") as csv_file:
        for _, line in enumerate(csv_file):
            if line.strip() == marker:
                break
        else:
            raise ValueError(f"Marker '{marker}' not found in file: {filename}")

        for _ in range(int(skip_lines_after_marker)):
            next(csv_file, None)

        csv_reader = csv.reader(csv_file, delimiter=",")
        data_rows = []
        for row in csv_reader:
            if not any((field or "").strip() for field in row):
                break

            tail = row[skip_first_n_cols:]
            if not tail:
                data_rows.append([])
                continue

            converted = []
            for value in tail:
                stripped = value.strip()
                if stripped == "":
                    converted.append(np.nan)
                    continue
                try:
                    converted.append(float(stripped))
                except ValueError:
                    converted.append(np.nan)
            data_rows.append(converted)

        if not data_rows:
            return np.empty((0, 0), dtype=float)

        max_cols = max(len(row) for row in data_rows)
        if max_cols == 0:
            return np.empty((len(data_rows), 0), dtype=float)

        array = np.full((len(data_rows), max_cols), np.nan, dtype=float)
        for row_index, row in enumerate(data_rows):
            array[row_index, : len(row)] = row

        return array.transpose()