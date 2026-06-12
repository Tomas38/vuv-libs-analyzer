"""Plot helpers for the Streamlit app."""

from __future__ import annotations

from matplotlib.figure import Figure


def create_figure() -> Figure:
    return Figure(figsize=(8, 5), dpi=100)


def plot_spectrum(figure: Figure, wavelengths, intensities, title: str = "Spectrum") -> Figure:
    figure.clear()
    axis = figure.add_subplot(111)
    axis.plot(wavelengths, intensities, color="#1f77b4", linewidth=1.4)
    axis.set_xlabel("Wavelength (nm)" if len(wavelengths) else "Index")
    axis.set_ylabel("Intensity")
    axis.set_title(title)
    axis.grid(True, alpha=0.25)
    figure.tight_layout()
    return figure