from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from vuv_analyzer.core.ham_reader import ham_read_file, ham_reader
from vuv_analyzer.core.pix2wav import pix2wav


BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(layout="wide")

uploaded_file = st.file_uploader("Choose a file with dark frames")
if uploaded_file is not None:
    xdata, ydatas = ham_read_file(uploaded_file)
else:
    xdata, ydatas = ham_reader(BASE_DIR / "sample-data" / "10us_30meas_05_Al_alloy_30mJ_Ar_1020mbar.csv")

if ydatas.size == 0:
    st.info("Upload a Hamamatsu file to display spectra.")
    st.stop()

wav_on = st.toggle("X-axis in wavelength", value=True)

xdata2 = xdata
spectra_df = pd.DataFrame(ydatas.T, columns=[f"spectrum_{i}" for i in range(ydatas.shape[0])])
spectra_df.insert(0, "x", xdata2)
spectra_df.insert(0, "wavelength", pix2wav(xdata2))

ydatas_avg = np.mean(ydatas, axis=0)
ydatas_std = np.std(ydatas, axis=0)


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


fig2 = go.Figure()
fig2.add_trace(
    go.Scatter(
        x=spectra_df[xaxis_to_show],
        y=ydatas_avg + ydatas_std,
        mode="lines",
        name="Average Dark Frame + 1 std",
        line={"width": 0},
        visible=True,
        showlegend=False,
    )
)
fig2.add_trace(
    go.Scatter(
        x=spectra_df[xaxis_to_show],
        y=ydatas_avg - ydatas_std,
        mode="lines",
        name="Average Dark Frame - 1 std",
        line={"width": 0},
        visible=True,
        fill="tonexty",
        fillcolor="lightgray",
        showlegend=False,
    )
)
fig2.add_trace(
    go.Scatter(
        x=spectra_df[xaxis_to_show],
        y=ydatas_avg,
        mode="lines",
        line={"color": "black", "width": 2},
        visible=True,
    )
)

if wav_on:
    fig2.update_layout(xaxis_title="Wavelength (nm)")
else:
    fig2.update_layout(xaxis_title="Pixel No.")
fig2.update_layout(title="Average Dark Frame ± 1 std", yaxis_title="intensity (counts)", uirevision="keep")

st.plotly_chart(fig2)



override_default_dark_buttion = st.button("Overwrite Master Dark Frame", type="primary")

if override_default_dark_buttion:
    # Combine the arrays column-wise
    data = np.column_stack((xdata, ydatas_avg, ydatas_std))

    # Save to CSV
    np.savetxt(
        BASE_DIR / "config" / "dark_frame_default.csv",
        data,
        delimiter=",",
        header="x,y,std",
        comments="",
        fmt="%.10g"   # Adjust formatting as needed
    )