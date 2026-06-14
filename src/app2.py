"""Streamlit entry point for the VUV Spectrometer Analyzer."""

import streamlit as st


# Define the pages
main_page = st.Page("D:/software/vuv-libs-analyzer/src/spectrum.py", title="Spectrum module", icon="🌈")
page_2 = st.Page("D:/software/vuv-libs-analyzer/src/mapping.py", title="Mapping module", icon="🗺️")
page_3 = st.Page("D:/software/vuv-libs-analyzer/src/wav_cal.py", title="Wavelength Calibration")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

# Run the selected page
pg.run()


st.sidebar.header("Select file")

slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

st.sidebar.header("Config file")