x# This is a tool to automate cyclic voltametry analysis.
# Current Version = 1

import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import peakutils
import scipy
from scipy.signal import savgol_filter

def peak_find(potential_1, current_1, potential_2, current_2):
    # Having only one peak, situation 1
    if max(abs(current_1))/max(abs(current_2)) > 100:
        sm_cur_1 = savgol_filter(current_1, 21, 5, mode='nearest')
        der_1 = np.diff(sm_cur_1)
        max_der_1 = max(der_1)
        min_der_1 = min(der_1)
        max_der_pt_1 =  np.argmin(abs(der_1 - max_der_1))
        min_der_pt_1 =  np.argmin(abs(der_1 - min_der_1))

        if max(sm_cur_1)+min(sm_cur_1)>0:
            peak_pt_1 = np.argmin(abs(der_1[max_der_pt_1:min_der_pt_1] - 0))
            peak_pot_1 = potential_1[peak_pt_1+max_der_pt_1]
            peak_cur_1 = current_1[peak_pt_1+max_der_pt_1]

        else:
            peak_pt_1 = np.argmin(abs(der_1[min_der_pt_1:max_der_pt_1] - 0))
            peak_pot_1 = potential_1[peak_pt_1+min_der_pt_1]
            peak_cur_1 = current_1[peak_pt_1+min_der_pt_1]


        peak_pt = [peak_pt_1]
        peak_pot = [peak_pot_1]
        peak_cur = [peak_cur_1]
    # Having only one peak, situation 2
    elif max(abs(current_1))/max(abs(current_2)) < 0.01:
        sm_cur_2 = savgol_filter(current_2, 21, 5, mode='nearest')
        der_2 = np.diff(sm_cur_2)
        max_der_2 = max(der_2)
        min_der_2 = min(der_2)
        max_der_pt_2 =  np.argmin(abs(der_2 - max_der_2))
        min_der_pt_2 =  np.argmin(abs(der_2 - min_der_2))
        if max(sm_cur_2)+min(sm_cur_2)<0:
            peak_pt_2 = np.argmin(abs(der_2[min_der_pt_2:max_der_pt_2] - 0))
            peak_pot_2 = potential_2[peak_pt_2+min_der_pt_2]
            peak_cur_2 = current_2[peak_pt_2+min_der_pt_2]
        else:
            peak_pt_2 = np.argmin(abs(der_2[max_der_pt_2:min_der_pt_2] - 0))
            peak_pot_2 = potential_2[peak_pt_2+max_der_pt_2]
            peak_cur_2 = current_2[peak_pt_2+max_der_pt_2]

        peak_pt = [peak_pt_2]
        peak_pot = [peak_pot_2]
        peak_cur = [peak_cur_2]

    #Having both cathodic and anodic peaks
    else:
        # process the first 1/2 of the CV
        sm_cur_1 = savgol_filter(current_1, 21, 5, mode='nearest')
        der_1 = np.diff(sm_cur_1)
        max_der_1 = max(der_1)
        min_der_1 = min(der_1)
        max_der_pt_1 =  np.argmin(abs(der_1 - max_der_1))
        min_der_pt_1 =  np.argmin(abs(der_1 - min_der_1))
        # process the 2nd 1/2 of the CV
        sm_cur_2 = savgol_filter(current_2, 21, 5, mode='nearest')
        der_2 = np.diff(sm_cur_2)
        max_der_2 = max(der_2)
        min_der_2 = min(der_2)
        max_der_pt_2 =  np.argmin(abs(der_2 - max_der_2))
        min_der_pt_2 =  np.argmin(abs(der_2 - min_der_2))
        # Find 0 in the first derivative
        if max(sm_cur_1)+min(sm_cur_1)>0 and min_der_pt_1>max_der_pt_1 and min_der_pt_2<max_der_pt_2:
            peak_pt_1 = np.argmin(abs(der_1[max_der_pt_1:min_der_pt_1] - 0))
            peak_pot_1 = potential_1[peak_pt_1+max_der_pt_1]
            peak_cur_1 = current_1[peak_pt_1+max_der_pt_1]
            peak_pt_2 = np.argmin(abs(der_2[min_der_pt_2:max_der_pt_2] - 0))
            peak_pot_2 = potential_2[peak_pt_2+min_der_pt_2]
            peak_cur_2 = current_2[peak_pt_2+min_der_pt_2]
            peak_pt = [peak_pt_1,peak_pt_2]
            peak_pot = [peak_pot_1,peak_pot_2]
            peak_cur = [peak_cur_1,peak_cur_2]
        elif max(sm_cur_1)+min(sm_cur_1)<=0 and min_der_pt_1<max_der_pt_1 and min_der_pt_2>max_der_pt_2:
            peak_pt_1 = np.argmin(abs(der_1[min_der_pt_1:max_der_pt_1] - 0))
            peak_pot_1 = potential_1[peak_pt_1+min_der_pt_1]
            peak_cur_1 = current_1[peak_pt_1+min_der_pt_1]
            peak_pt_2 = np.argmin(abs(der_2[max_der_pt_2:min_der_pt_2] - 0))
            peak_pot_2 = potential_2[peak_pt_2+max_der_pt_2]
            peak_cur_2 = current_2[peak_pt_2+max_der_pt_2]
            peak_pt = [peak_pt_1,peak_pt_2]
            peak_pot = [peak_pot_1,peak_pot_2]
            peak_cur = [peak_cur_1,peak_cur_2]
        else:
            peak_pt = []
            peak_pot = []
            peak_cur = []




    return peak_pt, peak_pot, peak_cur

def baseline(potential_1, current_1, potential_2, current_2):
    # Deep smoothing of first derivative
    sm_cur_1 = savgol_filter(current_1, 301, 5, mode='nearest')
    first_dev_1 = np.diff(sm_cur_1)/np.diff(potential_1)
    sm_first_dev_1 = savgol_filter(first_dev_1, 301, 5, mode='nearest')
    second_dev_1 = np.diff(sm_first_dev_1)
    sm_second_dev_1 = savgol_filter(second_dev_1, 201, 5, mode='nearest')
    third_dev_1 = np.diff(sm_second_dev_1)
    sm_third_dev_1 = savgol_filter(third_dev_1, 301, 5, mode='nearest')

    baseline_pt_1 = np.argmin(abs(sm_third_dev_1[10:500] - 0))
    baseline_slope_1 = sm_first_dev_1[baseline_pt_1]
    baseline_intercept_1 = current_1[baseline_pt_1]-baseline_slope_1*potential_1[baseline_pt_1]

    baseline_1 = baseline_slope_1 * potential_1 + baseline_intercept_1


    sm_cur_2 = savgol_filter(current_2, 301, 5, mode='nearest')
    first_dev_2 = np.diff(sm_cur_2)/np.diff(potential_2)
    sm_first_dev_2 = savgol_filter(first_dev_2, 301, 5, mode='nearest')
    second_dev_2 = np.diff(sm_first_dev_2)
    sm_second_dev_2 = savgol_filter(second_dev_2, 201, 5, mode='nearest')
    third_dev_2 = np.diff(sm_second_dev_2)
    sm_third_dev_2 = savgol_filter(third_dev_2, 301, 5, mode='nearest')

    baseline_pt_2 = np.argmin(abs(sm_third_dev_2[10:500] - 0))
    baseline_slope_2 = sm_first_dev_2[baseline_pt_2]
    baseline_intercept_2 = current_2[baseline_pt_2]-baseline_slope_2*potential_2[baseline_pt_2]

    baseline_2 = baseline_slope_2 * potential_2 + baseline_intercept_2

    return baseline_1,baseline_2
