# VUV-LIBS-Analyzer

## Description

This program should be used for controling VUV spectrometer developed at FME BUT.

First version will use the Hamamatsu SW for obtaining data from CMOS sensor in .csv. In the future, full integration in this program should be done using SDK.

## Basic functions

### Wavelength conversion

Values 0–4095 should be recalculated to wavelength in nm (~120–220 nm).

### Data export

Export the data withing compatible data format suitable for further data analysis (h5, csv, json).

---

## Program modules ideas

### Spectrum display

- Should be possible to display the raw data in plot (with x axis 0-4095 or inversed).
- Zooming, and movind should be possible (e.g. matplotlib GUI)
- selecting spectrum to be displayed
- show averaged spectrum (manual range selection should be possible)

### Wavelength calibration

- select interval with peak (mouse cling-and-drag in graph)
- the software will detect peak position
- asign tabeled wavelength to the detected peak
- add this datapoint to calibration config (multiple configs should be possible)
- calibration/recalculation then as curve fit of quadratic function
- config as file
- calibration might involve using peaks from multiple spectra

### LIBS map viewer

- select interval with peak (mouse cling-and-drag in graph)
- plot signal from detected interval in graph
- aditional entry needed (data from SpectraController):
  - spacing size
  - no. shots per spot
  - grid size M x N
  - (mapping sequence, e.g. where is which corner, if zig-zag or always left-to-right)
- set min and max value (from 16-bit), linearity (possibly gamma curve setting)
- show histogram

### Data export

- TBD