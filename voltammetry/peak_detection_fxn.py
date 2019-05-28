"""This module contains a function to determine the peaks in the specified dataset,
based on the y values (or current values). The function takes in the specified
y column of the dataframe and outputs a list consisting of the index values of
the peaks. This module calls the peakutils and numpy packages along with the
'main.py' file in the master branch."""

import peakutils
import numpy as np
import core


def peak_detection_fxn(data_y):
    """The function takes an input of the column containing the y variables in the dataframe,
    associated with the current. The function calls the split function, which splits the
    column into two arrays, one of the positive and one of the negative values.
    This is because cyclic voltammetry delivers negative peaks, but the peakutils function works
    better with positive peaks. The function also runs on the middle 80% of data to eliminate
    unnecessary noise and messy values associated with pseudo-peaks.The vectors are then imported
    into the peakutils.indexes function to determine the significant peak for each array.
    The values are stored in a list, with the first index corresponding to the top peak and the
    second corresponding to the bottom peak.
    Parameters
    ______________
    y column: must be a column from a pandas dataframe
    Returns
    _____________
    A list with the index of the peaks from the top curve and bottom curve.
    """

    # initialize storage list
    index_list = []

    # split data into above and below the baseline
    col_y1, col_y2 = core.split(data_y)

    # detemine length of data and what 10% of the data is
    len_y = len(col_y1)
    ten_percent = int(np.around(0.1*len_y))

    # adjust both input columns to be the middle 80% of data
    # (take of the first and last 10% of data)
    # this avoid detecting peaks from electrolysis
    # (from water splitting and not the molecule itself,
    # which can form random "peaks")
    mod_col_y2 = col_y2[ten_percent:len_y-ten_percent]
    mod_col_y1 = col_y1[ten_percent:len_y-ten_percent]

    # run peakutils package to detect the peaks for both top and bottom
    peak_top = peakutils.indexes(mod_col_y2, thres=0.99, min_dist=20)
    peak_bottom = peakutils.indexes(abs(mod_col_y1), thres=0.99, min_dist=20)

    # detemine length of both halves of data
    len_top = len(peak_top)
    len_bot = len(peak_bottom)

    # append the values to the storage list
    # manipulate values by adding the ten_percent value back
    # (as the indecies have moved)
    # to detect the actual peaks and not the modified values
    index_list.append(peak_top[int(len_top/2)]+ten_percent)
    index_list.append(peak_bottom[int(len_bot/2)]+ten_percent)

    # return storage list
    # first value is the top, second value is the bottom
    return index_list
