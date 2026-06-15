import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from vuv_analyzer.core.ham_reader import ham_read_file, ham_reader


def load_default():
    st.session_state.df = pd.read_csv("src/config/calibration_points_default0.csv")

def load_csv(uploaded_file):
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)

def clear_table():
    st.session_state.df = pd.DataFrame(columns=["pixel no.", "wavelength (nm)"])


if "df" not in st.session_state:
    st.session_state.df = pd.read_csv(
        "src/config/calibration_points_default0.csv"
    )

uploaded_file = st.file_uploader("Choose a file with calibration points")

load_button = st.button("Load from CSV", on_click=load_csv, args=(uploaded_file,))
load_default_button = st.button("Load Default", on_click=load_default)
clear_table_button = st.button("Clear Table", on_click=clear_table)

df0 = st.session_state.df.copy()
edited_df = st.data_editor(df0, num_rows="dynamic")

csv_data = edited_df.to_csv(index=False)

override_default_buttion = st.button("Overwrite Default", type="primary")
if override_default_buttion:
    edited_df.to_csv("src/config/calibration_points_default0.csv", index=False)

st.download_button(label="Export CSV", data=csv_data, file_name="calibration_points.csv", mime="text/csv")

xdata = np.arange(0, 4096, 1)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=edited_df["pixel no."],
        y=edited_df["wavelength (nm)"],
        mode="markers",
    )
)
fig.update_layout(title="Calibration Points",
                  xaxis_title="pixel no.",
                  yaxis_title="wavelength (nm)"
                  )

st.plotly_chart(fig, width=600, height=600, theme="streamlit")
