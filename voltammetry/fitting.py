# This is a tool to automate cyclic voltametry analysis.
# Current Version = 1

import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import peakutils
import scipy
from scipy.signal import savgol_filter

def peak_find(potential, current):
    # Smooth the current curve, the window and order are emperical
    sm_cur = savgol_filter(current, 21, 5, mode='nearest')
    der_1 = np.diff(sm_cur)
    max_der = max(der_1)
    min_der = min(der_1)
    max_der_pt =  np.argmin(abs(der_1 - max_der))
    min_der_pt =  np.argmin(abs(der_1 - min_der))

    # Find 0 in the first derivative
    if max(sm_cur)+min(sm_cur)>0:
        peak_pt = np.argmin(abs(der_1[max_der_pt:min_der_pt] - 0))
        peak_pot = potential[peak_pt+max_der_pt]
        peak_cur = current[peak_pt+max_der_pt]
    else:
        peak_pt = np.argmin(abs(der_1[min_der_pt:max_der_pt] - 0))
        peak_pot = potential[peak_pt+min_der_pt]
        peak_cur = current[peak_pt+min_der_pt]


    return peak_pt, peak_pot, peak_cur

#def baseline(current)
    # Deep
