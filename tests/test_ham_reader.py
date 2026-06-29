import numpy as np
from vuv_analyzer.core.ham_reader import ham_reader


xdatas, ydatas = ham_reader("sample-data/10us_30meas_05_Al_alloy_30mJ_Ar_1020mbar.csv")

print(xdatas)
print(ydatas)
print()
print(ydatas.shape[0])

print(type(xdatas[0]))
print(len(xdatas))
