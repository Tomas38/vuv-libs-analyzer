# VUV Spectrometer Analyzer

A browser-based Python application for analyzing VUV spectroscopy data from CSV files, with configurable data conversion, live graph visualization, and export capabilities.

## Features

- Load CSV data files
- Configure data conversion parameters
- Display graphs in the application
- Export results to H5 and PNG formats

## Setup

### Linux/Mac
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/app.py
```

You can also run the launcher after installing the package:

```bash
vuv-analyzer
```

## Project Structure

- `src/app.py` - Streamlit entry point
- `src/vuv_analyzer/` - Core package and UI helpers
- `config/` - Configuration files
- `tests/` - Unit tests

## Architecture

- `core/` contains file loading, Hamamatsu parsing, conversion, statistics, config, and export logic.
- `ui/` contains plotting helpers and presentation utilities.
- `app.py` is the only Streamlit front door and should stay thin.
- `ham_reader.py` is kept as the import primitive for Hamamatsu-style files.

## Dependencies

See `requirements.txt` for full list of dependencies.
