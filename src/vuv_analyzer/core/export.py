"""Export helpers."""

from __future__ import annotations

import io
import json

import h5py
import numpy as np


def export_array_to_csv(data, name: str = "data") -> bytes:
    buffer = io.StringIO()
    np.savetxt(buffer, np.asarray(data), delimiter=",", fmt="%.10g")
    return buffer.getvalue().encode("utf-8")


def export_array_to_json(data, name: str = "data") -> bytes:
    payload = {
        "name": name,
        "values": np.asarray(data).tolist(),
    }
    return json.dumps(payload, indent=2).encode("utf-8")


def export_array_to_h5(data, name: str = "data", dataset_name: str = "data", compression: str = "gzip") -> bytes:
    buffer = io.BytesIO()
    with h5py.File(buffer, "w") as file_handle:
        file_handle.create_dataset(dataset_name, data=np.asarray(data), compression=compression)
        file_handle.attrs["name"] = name
    return buffer.getvalue()