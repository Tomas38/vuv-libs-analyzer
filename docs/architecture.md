# Architecture

The application is organized as a Streamlit front end with a small Python core.

## Goals

- Keep the UI simple and fast to build.
- Keep the data-processing code independent from Streamlit.
- Make Hamamatsu CSV import the first supported data path.

## Layout

- `src/app.py` is the Streamlit entry point.
- `src/vuv_analyzer/core/` holds loading, Hamamatsu parsing, processing, config, and export code.
- `src/vuv_analyzer/ui/` holds plotting helpers and presentation utilities.
- `config/default_config.json` keeps runtime defaults.
- `sample-data/` holds example input files.

## Runtime Flow

1. The user uploads a file or selects a sample.
2. The loader detects whether the file is Hamamatsu-style or plain CSV.
3. The processing layer builds the trace, statistics, and wavelength axis.
4. The UI renders the plot and offers exports.

## What stays out of the UI

- File parsing
- Conversion logic
- Statistics
- Export logic
- Calibration logic when it is added later