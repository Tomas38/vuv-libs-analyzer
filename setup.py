from setuptools import setup, find_packages

setup(
    name="vuv-libs-analyzer",
    version="0.1.0",
    description="VUV Spectrometer Analyzer - browser app for analyzing spectroscopy data",
    author="Your Name",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "h5py>=3.0.0",
        "streamlit>=1.30.0",
    ],
    entry_points={
        "console_scripts": [
            "vuv-analyzer=vuv_analyzer.launch:main",
        ],
    },
)
