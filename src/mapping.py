import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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
        ydatas_background = np.zeros_like(ydatas)

if ydatas.size == 0:
    st.info("Upload a Hamamatsu file to display spectra.")
    st.stop()

use_background_subtraction = st.toggle("Subtract background")
show_dark_mean = st.toggle("Show dark mean spectrum")

ydatas_background_avg = np.mean(ydatas_background, axis=0)

if use_background_subtraction is True:
    ydatas = ydatas - ydatas_background_avg

xdata2 = np.arange(ydatas.shape[1])
spectra_df = pd.DataFrame(ydatas.T, columns=[f"spectrum_{i}" for i in range(ydatas.shape[0])])
spectra_df.insert(0, "x", xdata2)

if show_dark_mean:
    fig0 = go.Figure()
    fig0.add_trace(
        go.Scatter(x=spectra_df["x"], y=ydatas_background_avg, mode="lines", name="background average", line={"width": 1})
    )
    st.plotly_chart(fig0)

show_spectra = st.toggle("Show spectra")


rect_x_max = int(spectra_df["x"].max())
rect_width_default = 100
rect_x0_default = min(1780, max(0, rect_x_max - rect_width_default))
rect_x1_default = min(rect_x0_default + rect_width_default, rect_x_max)

rect_col1, rect_col2, rect_col3, rect_col4 = st.columns(4)
with rect_col1:
    rect_x0 = st.number_input(
        "x0",
        min_value=0,
        max_value=rect_x_max - 1,
        value=rect_x0_default,
        step=1,
    )
with rect_col2:
    rect_x1 = st.number_input(
        "x1",
        min_value=rect_x0 + 1,
        max_value=rect_x_max,
        value=max(rect_x1_default, rect_x0 + 1),
        step=1,
    )

# Initial spectrum to display
spec_id1 = 0

if show_spectra:
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

    fig.add_vrect(
        x0=rect_x0,
        x1=rect_x1,
        annotation_text="integration",
        annotation_position="top left",
        fillcolor="green",
        opacity=0.25,
        line_width=0,
    )

    fig.update_layout(title="Title", xaxis_title="pixel no.", yaxis_title="intensity (counts)", uirevision="keep")
    fig.update_layout(sliders=sliders)
    st.plotly_chart(fig)

x_in_wavelength = st.toggle("Show x-axis in wavelength", value=True)

show_data_table = st.toggle("Show data table")
if show_data_table:
    st.write(spectra_df)

#st.write(len(ydatas[0, :]))
#st.write(len(ydatas[:, 0]))
#st.write(np.shape(ydatas))

libs_map = np.zeros((grid_x, grid_y), dtype=float)
spectra_ids = np.zeros((grid_x, grid_y), dtype=int)

libs_map[4, 2] = 5.0

snake = st.toggle("Snake-like mapping", value=False)

try:
    for i in range(grid_x):
        for j in range(grid_y):
            if snake == False:
                index0 = i * shots + j * shots * grid_x
                spectra_ids[i, j] = index0
            if snake == True:
                index0 = 0
                if j % 2 == 0:
                    index0 = i * shots + j * shots * grid_x
                else:
                    index0 = (grid_x - i - 1) * shots + j * shots * grid_x
                spectra_ids[i, j] = index0
            indexes = np.arange(spectra_ids[i, j], shots)
            integ_vals = []
            for k in range(shots):
                integ_vals.append(np.sum(ydatas[spectra_ids[i, j] + k, rect_x0:rect_x1]))
            int_vals = np.array(integ_vals)
            libs_map[i, j] = np.sum(int_vals)
except Exception as e:
    st.error(f"Error processing spectra: {e}")

#st.write(libs_map)

fig2 = px.imshow(libs_map.T, color_continuous_scale="viridis")
st.plotly_chart(fig2)

