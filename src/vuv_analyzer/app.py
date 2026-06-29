"""Streamlit entry point for the VUV Spectrometer Analyzer."""

from pathlib import Path
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent

# Define the pages
st.logo(str(BASE_DIR / "CEITEC_Logo_Green.png"), size="large")
main_page = st.Page(str(BASE_DIR / "spectrum.py"), title="Spectrum module", icon="🌈")
page_2 = st.Page(str(BASE_DIR / "mapping.py"), title="Mapping module", icon="🗺️")
page_3 = st.Page(str(BASE_DIR / "wav_cal.py"), title="Wavelength Calibration", icon="📏")
page_4 = st.Page(str(BASE_DIR / "dark.py"), title="Dark Frame", icon="🌑")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3, page_4])

# Run the selected page
pg.run()
