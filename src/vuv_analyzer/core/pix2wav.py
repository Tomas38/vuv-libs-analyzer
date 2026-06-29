from pathlib import Path

import numpy as np


BASE_DIR = Path(__file__).resolve().parents[1]


def pix2wav(pixel_ids):
    """
    Convert pixel IDs to wavelengths using a calibration curve.

    Parameters:
    - pixel_ids: 1D array of pixel IDs
    - pixel_values: 1D array of pixel values corresponding to the pixel IDs
    - cal_xdata: 1D array of calibration x data (pixel IDs)
    - cal_ydata: 1D array of calibration y data (wavelengths)

    Returns:
    - wavelengths: 1D array of wavelengths corresponding to the input pixel IDs
    - pixel_values: 1D array of pixel values corresponding to the input pixel IDs
    """
    # LOAD CALIBRATION CURVE DATA
    # Load the CSV file, skipping the header row
    cal_data = np.loadtxt(BASE_DIR / "config" / "calibration_curve_data.csv", delimiter=",", skiprows=1)

    # Split into separate arrays
    # cal_xdata = cal_data[:, 0]
    # Expecting that the cal_data starts from pixel ID 0 and goes up to 4095, 
    # we can directly index into cal_data using pixel_ids
    cal_ydata = cal_data[:, 1]

    wavelengths = cal_ydata[pixel_ids]

    return wavelengths


if __name__ == "__main__":
    # Example usage
    pixel_ids = np.array([0, 1, 2, 3, 4])  # Replace with actual pixel IDs
    wavelengths = pix2wav(pixel_ids)
    print("Wavelengths:", wavelengths)

    pixel_ids = np.arange(1200, 1205)
    wavelengths = pix2wav(pixel_ids)
    print("Wavelengths:", wavelengths)
