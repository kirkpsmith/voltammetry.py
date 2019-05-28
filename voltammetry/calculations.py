"""This module consists of all the functions used
to calculate the pertinent values. """
import numpy as np
from . import core

def peak_values(dataframe_x, dataframe_y):
    """Outputs x (potentials) and y (currents) values from data indices
        given by peak_detection function.

       ----------
       Parameters
       ----------
       DataFrame_x : should be in the form of a pandas DataFrame column.
         For example, df['potentials'] could be input as the column of x
         data.

        DataFrame_y : should be in the form of a pandas DataFrame column.
          For example, df['currents'] could be input as the column of y
          data.

       Returns
       -------
       Result : numpy array of coordinates at peaks in the following order:
         potential of peak on top curve, current of peak on top curve,
         potential of peak on bottom curve, current of peak on bottom curve"""
    index = core.peak_detection_fxn(dataframe_y)
    potential1, potential2 = core.split(dataframe_x)
    current1, current2 = core.split(dataframe_y)
    peak_values = []
    peak_values.append(potential2[(index[0])])  # TOPX (bottom part of curve is
    # the first part of DataFrame)
    peak_values.append(current2[(index[0])])  # TOPY
    peak_values.append(potential1[(index[1])])  # BOTTOMX
    peak_values.append(current1[(index[1])])  # BOTTOMY
    peak_array = np.array(peak_values)
    return peak_array


def del_potential(dataframe_x, dataframe_y):
    """Outputs the difference in potentials between anoidc and
       cathodic peaks in cyclic voltammetry data.

       Parameters
       ----------
       DataFrame_x : should be in the form of a pandas DataFrame column.
         For example, df['potentials'] could be input as the column of x
         data.

        DataFrame_y : should be in the form of a pandas DataFrame column.
          For example, df['currents'] could be input as the column of y
          data.

        Returns
        -------
        Results: difference in peak potentials."""
    del_potentials = (peak_values(dataframe_x, dataframe_y)[0] -
                      peak_values(dataframe_x, dataframe_y)[2])
    return del_potentials


def half_wave_potential(dataframe_x, dataframe_y):
    """Outputs the half wave potential(redox potential) from cyclic
       voltammetry data.

       Parameters
       ----------
       DataFrame_x : should be in the form of a pandas DataFrame column.
         For example, df['potentials'] could be input as the column of x
         data.

        DataFrame_y : should be in the form of a pandas DataFrame column.
          For example, df['currents'] could be input as the column of y
          data.

       Returns
       -------
       Results : the half wave potential."""
    half_wave_pot = (del_potential(dataframe_x, dataframe_y))/2
    return half_wave_pot


def peak_heights(dataframe_x, dataframe_y):
    """Outputs heights of minimum peak and maximum
         peak from cyclic voltammetry data.

       Parameters
       ----------
       DataFrame_x : should be in the form of a pandas DataFrame column.
         For example, df['potentials'] could be input as the column of x
         data.

        DataFrame_y : should be in the form of a pandas DataFrame column.
          For example, df['currents'] could be input as the column of y
          data.

        Returns
        -------
        Results: height of maximum peak, height of minimum peak
          in that order in the form of a list."""
    current_max = peak_values(dataframe_x, dataframe_y)[1]
    current_min = peak_values(dataframe_x, dataframe_y)[3]
    col_x1, col_x2 = core.split(dataframe_x)
    col_y1, col_y2 = core.split(dataframe_y)
    line_at_min = core.linear_background(col_x1, col_y1)[core.peak_detection_fxn(dataframe_y)[1]]
    line_at_max = core.linear_background(col_x2, col_y2)[core.peak_detection_fxn(dataframe_y)[0]]
    height_of_max = current_max - line_at_max
    height_of_min = abs(current_min - line_at_min)
    return [height_of_max, height_of_min]


def peak_ratio(dataframe_x, dataframe_y):
    """Outputs the peak ratios from cyclic voltammetry data.

       Parameters
       ----------
       DataFrame_x : should be in the form of a pandas DataFrame column.
         For example, df['potentials'] could be input as the column of x
         data.

        DataFrame_y : should be in the form of a pandas DataFrame column.
          For example, df['currents'] could be input as the column of y
          data.

       Returns
       -------
       Result : returns a the peak ratio."""
    ratio = (peak_heights(dataframe_x, dataframe_y)[0] /
             peak_heights(dataframe_x, dataframe_y)[1])
    return ratio
