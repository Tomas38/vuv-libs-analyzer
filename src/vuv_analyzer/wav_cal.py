from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from scipy.optimize import curve_fit


BASE_DIR = Path(__file__).resolve().parent


def load_default():
    st.session_state.df = pd.read_csv(BASE_DIR / "config" / "calibration_points_default0.csv")

def load_csv(uploaded_file):
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)

def clear_table():
    st.session_state.df = pd.DataFrame(columns=["pixel no.", "wavelength (nm)"])

def linear_func(x, a, b):
    x0 = np.mean(x)  # fix x0 before fitting
    return a * (x - x0) + b

def quadratic_func(x, a, b, c):
    x0 = np.mean(x)  # fix x0 before fitting
    return a * (x - x0)**2 + b * (x - x0) + c


st.title("VUV LIBS Wavelength Calibration")

if "df" not in st.session_state:
    st.session_state.df = pd.read_csv(
        BASE_DIR / "config" / "calibration_points_default0.csv"
    )
if "xdata" not in st.session_state:
    st.session_state.xdata = np.array([])
    st.session_state.ydata = np.array([])
    st.session_state.dy = np.array([])

uploaded_file = st.file_uploader("Choose a file with calibration points")

load_button = st.button("Load from CSV", on_click=load_csv, args=(uploaded_file,))
load_default_button = st.button("Load Default", on_click=load_default)
clear_table_button = st.button("Clear Table", on_click=clear_table)

df0 = st.session_state.df.copy()
edited_df = st.data_editor(df0, num_rows="dynamic")

csv_data = edited_df.to_csv(index=False)

override_default_buttion = st.button("Overwrite Default Points", type="primary")
if override_default_buttion:
    edited_df.to_csv(BASE_DIR / "config" / "calibration_points_default0.csv", index=False)

st.download_button(label="Export Points as CSV", data=csv_data, file_name="calibration_points.csv", mime="text/csv")

placeholder = st.empty()


method = st.selectbox("Calibration method",
                  options=["Linear Regression",
                           "Linear Interpolation (TBD)",
                           "Quadratic Regression",
                           "Cubic Regression",
                           "Cubic Splines Interpolation (TBD)",
                           ],
                  index=0)

# st.write("$\\lambda(x) = A x^2 + B x + C$")
# st.write("$\\lambda(x) = A x + B$")

X = edited_df["pixel no."].to_numpy()
Y = edited_df["wavelength (nm)"].to_numpy()


if method == "Linear Regression":
    popt, pcov = curve_fit(linear_func, X, Y)
    perr = np.sqrt(np.diag(pcov))
    A_fit, B_fit = popt
    st.write(f"Fitted parameters: A = {A_fit:.4f} ± {perr[0]:.4f}, B = {B_fit:.4f} ± {perr[1]:.4f}")

    yfit = linear_func(X, *popt)

    ss_res = np.sum((Y - yfit)**2)
    ss_tot = np.sum((Y - np.mean(Y))**2)

    r_squared = 1 - ss_res / ss_tot

    st.write(f"R² = {r_squared:.4f}")

    st.session_state.xdata = np.arange(0, 4096, 1)
    st.session_state.ydata = linear_func(st.session_state.xdata, A_fit, B_fit)

    # # --- Uncertainty band ---
    # x0 = np.mean(X)
    # xi = X - x0  # shifted coordinate

    # # Jacobian: shape (len(x), 3) — one row per x point
    # J = np.column_stack([xi**2, xi, np.ones_like(xi)])

    # # Variance at each x: diag(J @ pcov @ J.T)
    # dy2 = np.einsum('ij,jk,ik->i', J, pcov, J)
    # dy = np.sqrt(dy2)

    # n=1
    # # Degree-n polynomial: f = sum_k p_k * (x-x0)^k
    # J = np.column_stack([(x - x0)**k for k in range(n+1)])
    # dy = np.sqrt(np.einsum('ij,jk,ik->i', J, pcov, J))
    # st.session_state.dy = dy

elif method == "Quadratic Regression":
    popt, pcov = curve_fit(quadratic_func, X, Y)
    perr = np.sqrt(np.diag(pcov))
    A_fit, B_fit, C_fit = popt
    st.write(f"Fitted parameters: A = {A_fit:.4f} ± {perr[0]:.4f}, B = {B_fit:.4f} ± {perr[1]:.4f}, C = {C_fit:.4f} ± {perr[2]:.4f}")

    yfit = quadratic_func(X, *popt)

    ss_res = np.sum((Y - yfit)**2)
    ss_tot = np.sum((Y - np.mean(Y))**2)

    r_squared = 1 - ss_res / ss_tot

    st.write(f"R² = {r_squared:.4f}")

    st.session_state.xdata = np.arange(0, 4096, 1)
    st.session_state.ydata = quadratic_func(st.session_state.xdata, A_fit, B_fit, C_fit)
else:
    st.session_state.xdata = np.array([])
    st.session_state.ydata = np.array([])


fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=edited_df["pixel no."],
        y=edited_df["wavelength (nm)"],
        mode="markers",
        name="Calibration Points",
    )
)

fig.add_trace(
    go.Scatter(
        x=st.session_state.xdata,
        y=st.session_state.ydata,
        mode="lines",
        name="Calibration Curve",
    )
)

# fig.add_trace(
#     go.Scatter(
#         x=st.session_state.xdata,
#         y=st.session_state.ydata - st.session_state.dy,
#         mode="lines",
#         name="Calibration Curve Error Band",
#     )
# )

fig.update_layout(title="Calibration Points",
                xaxis_title="pixel no.",
                yaxis_title="wavelength (nm)"
                )

placeholder.plotly_chart(fig, width=800, height=600, theme="streamlit")


override_default_curve_buttion = st.button("Overwrite Default Curve", type="primary")

if override_default_curve_buttion:
    # Combine the arrays column-wise
    data = np.column_stack((st.session_state.xdata, st.session_state.ydata))

    # Save to CSV
    np.savetxt(
        BASE_DIR / "config" / "calibration_curve_data.csv",
        data,
        delimiter=",",
        header="x,y",
        comments="",
        fmt="%.10g"   # Adjust formatting as needed
    )


st.download_button(label="Export Curve as CSV", data=csv_data, file_name="calibration_curve.csv", mime="text/csv")
