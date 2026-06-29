"""Streamlit entry point for the VUV Spectrometer Analyzer."""

import streamlit as st


# Define the pages
st.logo("CEITEC_Logo_Green.png", size="large")
main_page = st.Page("D:/software/vuv-libs-analyzer/src/spectrum.py", title="Spectrum module", icon="🌈")
page_2 = st.Page("D:/software/vuv-libs-analyzer/src/mapping.py", title="Mapping module", icon="🗺️")
page_3 = st.Page("D:/software/vuv-libs-analyzer/src/wav_cal.py", title="Wavelength Calibration", icon="📏")
page_4 = st.Page("D:/software/vuv-libs-analyzer/src/dark.py", title="Dark Frame", icon="🌑")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3, page_4])

# Run the selected page
pg.run()
