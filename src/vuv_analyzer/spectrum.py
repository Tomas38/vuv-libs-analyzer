from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from vuv_analyzer.core.ham_reader import ham_read_file, ham_reader
from vuv_analyzer.core.pix2wav import pix2wav


BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(layout="wide")

uploaded_file = st.file_uploader("Choose a file with spectra to display")
if uploaded_file is not None:
    xdata, ydatas = ham_read_file(uploaded_file)
else:
    xdata, ydatas = ham_reader(BASE_DIR / "sample-data" / "10us_30meas_05_Al_alloy_30mJ_Ar_1020mbar.csv")

if ydatas.size == 0:
    st.info("Upload a Hamamatsu file to display spectra.")
    st.stop()

wav_on = st.toggle("X-axis in wavelength", value=True)
use_background_subtraction = st.toggle("Subtract background")


dark_id, dark_y, dark_y_std = np.loadtxt(BASE_DIR / "config" / "dark_frame_default.csv", delimiter=",", skiprows=1, unpack=True)

xdata2 = xdata
if use_background_subtraction is True:
    ydatas = ydatas - dark_y

spectra_df = pd.DataFrame(ydatas.T, columns=[f"spectrum_{i}" for i in range(ydatas.shape[0])])
spectra_df.insert(0, "x", xdata2)
spectra_df.insert(0, "wavelength", pix2wav(xdata2))


if wav_on:
    xaxis_to_show = "wavelength"
else:
    xaxis_to_show = "x"

# Initial spectrum to display
spec_id1 = 0

fig = go.Figure()
slider_steps = []
for index in range(ydatas.shape[0]):
    selected = index == spec_id1
    # selected is True/False
    fig.add_trace(
        go.Scatter(
            x=spectra_df[xaxis_to_show],
            y=spectra_df[f"spectrum_{index}"],
            mode="lines",
            name=f"spectrum_{index}",
            line={"width": 1},
            visible=selected,
        )
    )

# Create steps for the slider
for index in range(ydatas.shape[0]):
    visibility = [trace_index == index for trace_index in range(ydatas.shape[0])]
    # looks like [True, False, False, ...] for the selected trace and [False, True, False, ...] for the next one etc.
    slider_steps.append(
        {
            "method": "update",
            "args": [{"visible": visibility}, {"title": f"Spectrum {index}"}],
            "label": str(index),
        }
    )

# Create and add slider inside the plotly figure
sliders = [dict(
    active=spec_id1,
    currentvalue={"prefix": "Spectrum: "},
    pad={"t": 30},
    steps=slider_steps
)]

if wav_on:
    fig.update_layout(xaxis_title="Wavelength (nm)")
else:
    fig.update_layout(xaxis_title="Pixel No.")
fig.update_layout(title="Loaded spectra", yaxis_title="intensity (counts)", uirevision="keep")
fig.update_layout(sliders=sliders)
st.plotly_chart(fig)

show_data_table = st.toggle("Show data table")
if show_data_table:
    st.write(spectra_df)
