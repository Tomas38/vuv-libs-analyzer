"""Streamlit entry point for the VUV Spectrometer Analyzer."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

from vuv_analyzer.core.config import default_config_path, load_config
from vuv_analyzer.core.export import export_array_to_csv, export_array_to_h5, export_array_to_json
from vuv_analyzer.core.loading import load_measurement_matrix
from vuv_analyzer.core.processing import build_wavelength_axis, calculate_statistics, extract_trace
from vuv_analyzer.ui.plots import create_figure, plot_spectrum


APP_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DATA_DIR = APP_ROOT / "sample-data"
DEFAULT_CONFIG = load_config(default_config_path())


st.set_page_config(page_title="VUV Spectrometer Analyzer", layout="wide")


def _available_sample_files() -> list[Path]:
    if not SAMPLE_DATA_DIR.exists():
        return []
    return sorted(path for path in SAMPLE_DATA_DIR.iterdir() if path.suffix.lower() == ".csv")


def _load_upload_to_tempfile(uploaded_file) -> Path:
    suffix = Path(uploaded_file.name).suffix or ".csv"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        return Path(temp_file.name)


def _to_dataframe(values: np.ndarray) -> pd.DataFrame:
    array = np.asarray(values)
    if array.ndim == 1:
        return pd.DataFrame({"value": array})
    return pd.DataFrame(array)


def _current_matrix() -> np.ndarray | None:
    return st.session_state.get("matrix")


st.title("VUV Spectrometer Analyzer")
st.caption("Fast browser-based workflow for loading, inspecting, and exporting spectroscopy data.")

sidebar = st.sidebar
sidebar.header("Data source")
use_hamamatsu_reader = sidebar.checkbox("Use Hamamatsu parser", value=True)
use_wavelength_axis = sidebar.checkbox("Show wavelength axis", value=True)

uploaded_file = sidebar.file_uploader("Upload measurement file", type=["csv", "txt"])
sample_files = _available_sample_files()
selected_sample = sidebar.selectbox(
    "Or choose a sample file",
    ["None", *[path.name for path in sample_files]],
)

source_path: Path | None = None
if uploaded_file is not None:
    source_path = _load_upload_to_tempfile(uploaded_file)
elif selected_sample != "None":
    source_path = SAMPLE_DATA_DIR / selected_sample

if source_path is not None:
    st.session_state["matrix"] = load_measurement_matrix(source_path, use_hamamatsu=use_hamamatsu_reader)
    st.session_state["source_name"] = source_path.name

matrix = _current_matrix()

if matrix is None:
    st.info("Upload a file or choose a sample to start.")
    st.stop()

source_name = st.session_state.get("source_name", "measurement")
config = DEFAULT_CONFIG

col_left, col_right = st.columns([1.1, 1.9], gap="large")

with col_left:
    st.subheader("Controls")
    st.write(f"Source: {source_name}")
    st.write(f"Shape: {tuple(matrix.shape)}")

    if matrix.ndim == 1:
        trace_orientation = "row"
        trace_index = 0
    else:
        trace_orientation = st.selectbox("Trace orientation", ["row", "column"])
        max_index = matrix.shape[0] - 1 if trace_orientation == "row" else matrix.shape[1] - 1
        trace_index = st.slider("Trace index", 0, max_index, 0)

    intensity_scale = st.number_input(
        "Intensity scale",
        min_value=0.0,
        value=float(config["data_conversion"].get("intensity_scale", 1.0)),
        step=0.1,
    )
    wavelength_start = st.number_input(
        "Wavelength start (nm)",
        value=120.0,
        step=1.0,
    )
    wavelength_end = st.number_input(
        "Wavelength end (nm)",
        value=220.0,
        step=1.0,
    )

    trace = extract_trace(matrix, trace_index=trace_index, orientation=trace_orientation)
    trace = trace * intensity_scale
    axis = build_wavelength_axis(len(trace), {"wavelength_axis": {"start_nm": wavelength_start, "end_nm": wavelength_end}}) if use_wavelength_axis else np.arange(len(trace))
    stats = calculate_statistics(trace)

    st.subheader("Statistics")
    st.metric("Mean", f"{stats['mean']:.4g}")
    st.metric("Std", f"{stats['std']:.4g}")
    st.metric("Min", f"{stats['min']:.4g}")
    st.metric("Max", f"{stats['max']:.4g}")

with col_right:
    st.subheader("Plot")
    figure = create_figure()
    plot_spectrum(figure, axis, trace, title=f"{source_name} - trace {trace_index}")
    st.pyplot(figure, clear_figure=True)

    st.subheader("Preview")
    preview = _to_dataframe(trace[: min(len(trace), 200)])
    st.dataframe(preview, use_container_width=True, height=220)

    st.subheader("Export")
    export_name = Path(source_name).stem
    csv_bytes = export_array_to_csv(trace, export_name)
    json_bytes = export_array_to_json(trace, export_name)
    h5_bytes = export_array_to_h5(trace, export_name)

    st.download_button("Download CSV", csv_bytes, file_name=f"{export_name}.csv", mime="text/csv")
    st.download_button("Download JSON", json_bytes, file_name=f"{export_name}.json", mime="application/json")
    st.download_button("Download H5", h5_bytes, file_name=f"{export_name}.h5", mime="application/x-hdf5")