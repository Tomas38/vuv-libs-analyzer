import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from vuv_analyzer.core.ham_reader import ham_read_file, ham_reader

st.title("VUV LIBS Map Analyzer")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    shots = st.number_input("Shots per spot", min_value=1, step=1)
with col2:
    grid_x = st.number_input("Grid X (spots)", min_value=1, value=10, step=1)
with col3:
    grid_y = st.number_input("Grid Y (spots)", min_value=1, value=10, step=1)
with col4:
    step_x = st.number_input("Step X (μm)", min_value=1.0, value=100.0)
with col5:
    step_y = st.number_input("Step Y (μm)", min_value=1.0, value=100.0)

st.write("Spots: ", grid_x * grid_y)
st.write("Spectra: ", grid_x * grid_y * shots)

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Choose a file with spectra to display")
    if uploaded_file is not None:
        ydatas = ham_read_file(uploaded_file)
    else:
        ydatas = ham_reader("sample-data/10us_30meas_05_Al_alloy_30mJ_Ar_1020mbar.csv")
with col2:
    uploaded_file_background = st.file_uploader("Choose a file for background subtraction")
    if uploaded_file_background is not None:
        ydatas_background = ham_read_file(uploaded_file_background)
    else:
        ydatas_background = ham_reader("sample-data/10us_30meas_05_Al_alloy_30mJ_Ar_1020mbar.csv")

if ydatas.size == 0:
    st.info("Upload a Hamamatsu file to display spectra.")
    st.stop()

xdata2 = np.arange(ydatas.shape[1])
spectra_df = pd.DataFrame(ydatas.T, columns=[f"spectrum_{i}" for i in range(ydatas.shape[0])])
spectra_df.insert(0, "x", xdata2)

# Initial spectrum to display
spec_id1 = 0

fig = go.Figure()
slider_steps = []
for index in range(ydatas.shape[0]):
    selected = index == spec_id1
    # selected is True/False
    fig.add_trace(
        go.Scatter(
            x=spectra_df["x"],
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

fig.update_layout(title="Title", xaxis_title="pixel no.", yaxis_title="intensity (counts)", uirevision="keep")
fig.update_layout(sliders=sliders)
st.plotly_chart(fig)

x_in_wavelength = st.toggle("Show x-axis in wavelength", value=True)

use_background_subtraction = st.toggle("Subtract background")

show_data_table = st.toggle("Show data table")
if show_data_table:
    st.write(spectra_df)
