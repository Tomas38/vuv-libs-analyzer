import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def linear_func(x, a, b):
    return a * x + b


xdata = np.array([1, 2, 3, 4, 5])
ydata = np.array([2.0, 2.1, 2.2, 2.1, 2.15]) + 100.0

x0 = np.mean(xdata)  # decorrelation point
popt, pcov = curve_fit(linear_func, xdata, ydata)
perr = np.sqrt(np.diag(pcov))
A_fit, B_fit = popt

sigma_A, sigma_B = perr[0], perr[1]

print(sigma_A, sigma_B)


x_line = np.linspace(-1, 8, 100)
yfit = linear_func(x_line, A_fit, B_fit)

# Correct uncertainty band (assuming A, B decorrelated because x0 = mean(x))
dy = np.sqrt(sigma_B**2 + sigma_A**2 * (x_line - x0)**2)

plt.plot(xdata, ydata, 'x', label='Data')
plt.plot(x_line, yfit, '--', color='black', label='Best fit')
plt.fill_between(x_line, yfit - 3*dy, yfit + 3*dy, alpha=0.3, label='±3σ band')
plt.axvline(x0, color='gray', linestyle='--', label='x0 (pivot)')
plt.legend()
plt.show()
