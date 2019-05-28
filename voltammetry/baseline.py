# This module is to fit baseline to calculate peak current
# values from cyclic voltammetry data.
# If you wish to choose best fitted baseline,
# checkout branch baseline_old method2.
# If have any questions contact sabiha3@uw.edu

import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook


# split forward and backward sweping data, to make it easier for processing.
def split(vector):
    """
    This function takes an array and splits it into equal two half.
    ----------
    Parameters
    ----------
    vector : Can be in any form of that can be turned into numpy array.
    Normally, for the use of this function, it expects pandas DataFrame column.
    For example, df['potentials'] could be input as the column of x data.
    -------
    Returns
    -------
    This function returns two equally splited vector.
    The output then can be used to ease the implementation
    of peak detection and baseline finding.
    """
    (assert type(vector) == pd.core.series.Series,
        "Input of the function should be pandas series")
    split = int(len(vector)/2)
    end = int(len(vector))
    vector1 = np.array(vector)[0:split]
    vector2 = np.array(vector)[split:end]
    return vector1, vector2


def critical_idx(x, y):  # Finds index where data set is no longer linear
    """
    This function takes x and y values callculate the derrivative
    of x and y, and calculate moving average of 5 and 15 points.
    Finds intercepts of different moving average curves and
    return the indexs of the first intercepts.
    ----------
    Parameters
    ----------
    x : Numpy array.
    y : Numpy array.
    Normally, for the use of this function, it expects
    numpy array that came out from split function.
    For example, output of split.df['potentials']
    could be input for this function as x.
    -------
    Returns
    -------
    This function returns 5th index of the intercepts
    of different moving average curves.
    User can change this function according to
    baseline branch method 2 to get various indexes..
    """
    (assert type(x) == np.ndarray,
     "Input of the function should be numpy array")
    (assert type(y) == np.ndarray,
     "Input of the function should be numpy array")
    if x.shape[0] != y.shape[0]:
        raise ValueError("x and y must have same first dimension, but "
                         "have shapes {} and {}".format(x.shape, y.shape))
    k = np.diff(y)/(np.diff(x))  # calculated slops of x and y
    # Calculate moving average for 10 and 15 points.
    # This two arbitrary number can be tuned to get better fitting.
    ave10 = []
    ave15 = []
    for i in range(len(k)-10):
        # The reason to minus 10 is to prevent j from running out of index.
        a = 0
        for j in range(0, 5):
            a = a + k[i+j]
        ave10.append(round(a/10, 5))
    # keeping 5 desimal points for more accuracy
    # This numbers affect how sensitive to noise.
    for i in range(len(k)-15):
        b = 0
        for j in range(0, 15):
            b = b + k[i+j]
        ave15.append(round(b/15, 5))
    ave10i = np.asarray(ave10)
    ave15i = np.asarray(ave15)
    # Find intercepts of different moving average curves
    # reshape into one row.
    idx = {np.argwhere(np.diff(np.sign(ave15i -
                               ave10i[:len(ave15i)]) != 0)).reshape(-1) + 0}
    return idx[5]
# This is based on the method 1 where user can't choose the baseline.
# If wanted to add that, choose method2.


def sum_mean(vector):
    """
    This function returns the mean and sum of the given vector.
    ----------
    Parameters
    ----------
    vector : Can be in any form of that can be turned into numpy array.
    Normally, for the use of this function, it expects pandas DataFrame column.
    For example, df['potentials'] could be input as the column of x data.
    """
    (assert type(vector) == np.ndarray,
     "Input of the function should be numpy array")
    a = 0
    for i in vector:
        a = a + i
    return [a, a/len(vector)]


def multiplica(vector_x, vector_y):
    """
    This function returns the sum of the multilica of two given vector.
    ----------
    Parameters
    ----------
    vector_x, vector_y : Output of the split vector function.
    Two inputs can be the same vector or different vector with same length.
    -------
    Returns
    -------
    This function returns a number that is the sum
    of multiplicity of given two vector.
    """
    (assert type(vector_x) == np.ndarray,
     "Input of the function should be numpy array")
    (assert type(vector_y) == np.ndarray,
     "Input of the function should be numpy array")
    a = 0
    for x, y in zip(vector_x, vector_y):
        a = a + (x * y)
    return a


def linear_coeff(x, y):
    """
    This function returns the inclination coeffecient and
    y axis interception coeffecient m and b.
    ----------
    Parameters
    ----------
    x : Output of the split vector function.
    y : Output of the split vector function.
    -------
    Returns
    -------
    float number of m and b.
    """
    m = {(multiplica(x, y) - sum_mean(x)[0] * sum_mean(y)[1]) /
         (multiplica(x, x) - sum_mean(x)[0] * sum_mean(x)[1])}
    b = sum_mean(y)[1] - m * sum_mean(x)[1]
    return m, b


def y_fitted_line(m, b, x):
    """
    This function returns the fitted baseline constructed
    by coeffecient m and b and x values.
    ----------
    Parameters
    ----------
    x : Output of the split vector function. x value of the input.
    m : inclination of the baseline.
    b : y intercept of the baseline.
    -------
    Returns
    -------
    List of constructed y_labels.
    """
    y_base = []
    for i in x:
        y = m * i + b
        y_base.append(y)
    return y_base


def linear_background(x, y):
    """
    This function is wrapping function for calculating linear fitted line.
    It takes x and y values of the cv data, returns the fitted baseline.
    ----------
    Parameters
    ----------
    x : Output of the split vector function. x value
    of the cyclic voltammetry data.
    y : Output of the split vector function. y value
    of the cyclic voltammetry data.
    -------
    Returns
    -------
    List of constructed y_labels.
    """
    assert type(x) == np.ndarray, "Input of the function should be numpy array"
    assert type(y) == np.ndarray, "Input of the function should be numpy array"
    idx = critical_idx(x, y) + 5
    # this is also arbitrary number we can play with.
    m, b = {linear_coeff(x[(idx - int(0.5 * idx)): (idx + int(0.5 * idx))],
                         y[(idx - int(0.5 * idx)): (idx + int(0.5 * idx))])}
    y_base = y_fitted_line(m, b, x)
    return y_base
