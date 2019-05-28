"""This module consists of all the functions utilized."""
# This is a tool to automate cyclic voltametry analysis.
# Current Version = 1

import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import peakutils


def read_cycle(data):
    """This function reads a segment of datafile (corresponding a cycle)
    and generates a dataframe with columns 'Potential' and 'Current'

    Parameters
    __________
    data: segment of data file
    Returns
    _______
    A dataframe with potential and current columns
    """

    current = []
    potential = []
    for i in data[3:]:
        current.append(float(i.split("\t")[4]))
        potential.append(float(i.split("\t")[3]))
    zipped_list = list(zip(potential, current))
    dataframe = pd.DataFrame(zipped_list, columns=['Potential', 'Current'])
    return dataframe


def read_file_dash(lines):
    """This function is exactly similar to read_file, but it is for dash

    Parameters
    __________
    file: lines from dash input file

    Returns:
    ________
    dict_of_df: dictionary of dataframes with keys = cycle numbers and
    values = dataframes for each cycle
    n_cycle: number of cycles in the raw file
    """
    dict_of_df = {}
    h_val = 0
    l_val = 0
    n_cycle = 0
    number = 0
    # a = []
    # with open(file, 'rt') as f:
    #    print(file + ' Opened')
    for line in lines:
        record = 0
        if not (h_val and l_val):
            if line.startswith('SCANRATE'):
                scan_rate = float(line.split()[2])
                h_val = 1
            if line.startswith('STEPSIZE'):
                step_size = float(line.split()[2])
                l_val = 1
        if line.startswith('CURVE'):
            n_cycle += 1
            if n_cycle > 1:
                number = n_cycle - 1
                data = read_cycle(a_val)
                key_name = 'cycle_' + str(number)
                #key_name = number
                dict_of_df[key_name] = copy.deepcopy(data)
            a_val = []
        if n_cycle:
            a_val.append(line)
    return dict_of_df, number


def read_file(file):
    """This function reads the raw data file, gets the scanrate and stepsize
    and then reads the lines according to cycle number. Once it reads the data
    for one cycle, it calls read_cycle function to denerate a dataframe. It
    does the same thing for all the cycles and finally returns a dictionary,
    the keys of which are the cycle numbers and the values are the
    corresponding dataframes.

    Parameters
    __________
    file: raw data file

    Returns:
    ________
    dict_of_df: dictionary of dataframes with keys = cycle numbers and
    values = dataframes for each cycle
    n_cycle: number of cycles in the raw file
    """
    dict_of_df = {}
    h_val = 0
    l_val = 0
    n_cycle = 0
    #a = []
    with open(file, 'rt') as f_val:
        print(file + ' Opened')
        for line in f_val:
            record = 0
            if not (h_val and l_val):
                if line.startswith('SCANRATE'):
                    scan_rate = float(line.split()[2])
                    h_val = 1
                if line.startswith('STEPSIZE'):
                    step_size = float(line.split()[2])
                    l_val = 1
            if line.startswith('CURVE'):
                n_cycle += 1
                if n_cycle > 1:
                    number = n_cycle - 1
                    data = read_cycle(a_val)
                    key_name = 'cycle_' + str(number)
                    #key_name = number
                    dict_of_df[key_name] = copy.deepcopy(data)
                a_val = []
            if n_cycle:
                a_val.append(line)
    return dict_of_df, number
# df = pd.DataFrame(list(dict1['df_1'].items()))
# list1, list2 = list(dict1['df_1'].items())
# list1, list2 = list(dict1.get('df_'+str(1)))


def data_frame(dict_cycle, number):
    """Reads the dictionary of dataframes and returns dataframes for each cycle

    Parameters
    __________
    dict_cycle: Dictionary of dataframes
    n: cycle number

    Returns:
    _______
    Dataframe correcponding to the cycle number
    """
    list1, list2 = (list(dict_cycle.get('cycle_'+str(number)).items()))
    zipped_list = list(zip(list1[1], list2[1]))
    data = pd.DataFrame(zipped_list, columns=['Potential', 'Current'])
    return data


def plot_fig(dict_cycle, number):
    """For basic plotting of the cycle data

    Parameters
    __________
    dict: dictionary of dataframes for all the cycles
    n: number of cycles

    Saves the plot in a file called cycle.png
    """

    for i in range(number):
        print(i+1)
        data = data_frame(dict_cycle, i+1)
        plt.plot(data.Potential, data.Current, label="Cycle{}".format(i+1))

    print(data.head())
    plt.xlabel('Voltage')
    plt.ylabel('Current')
    plt.legend()
    plt.savefig('cycle.png')
    print('executed')


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
    The output then can be used to ease the implementation of peak detection and baseline finding.
    """
    assert isinstance(vector, pd.core.series.Series), "Input should be pandas series"
    split_top = int(len(vector)/2)
    end = int(len(vector))
    vector1 = np.array(vector)[0:split]
    vector2 = np.array(vector)[split_top:end]
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
    baseline branch method 2 to get various indexes.
    """
    assert isinstance(x, np.ndarray), "Input should be numpy array"                                                                                                                               
    assert isinstance(y == np.ndarray), "Input should be numpy array"
    if x.shape[0] != y.shape[0]:
        raise ValueError("x and y must have same first dimension, but "
                         "have shapes {} and {}".format(x.shape, y.shape))
    k_val = np.diff(y)/(np.diff(x))  # calculated slops of x and y
    # Calculate moving average for 10 and 15 points.
    # This two arbitrary number can be tuned to get better fitting.
    ave10 = []
    ave15 = []
    for i in range(len(k_val)-10):
        # The reason to minus 10 is to prevent j from running out of index.
        a_val = 0
        for j in range(0, 5):
            a_val = a_val + k_val[i+j]
        ave10.append(round(a/10, 5))
    # keeping 5 desimal points for more accuracy
    # This numbers affect how sensitive to noise.
    for i in range(len(k_val)-15):
        b = 0
        for j in range(0, 15):
            b = b + k_val[i+j]
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
    assert isinstance(vector == np.ndarray), "Input should be numpy array"
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


def y_fitted_line(m_val, b_val, vec_x):
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
    for i in vec_x:
        y_val = m_val * i + b_val
        y_base.append(y_val)
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
    assert isinstance(x, np.ndarray), "Input of the function should be numpy array"
    assert isinstance(y, np.ndarray), "Input of the function should be numpy array"
    idx = critical_idx(x, y) + 5
    # this is also arbitrary number we can play with.
    m_val, b_val = (linear_coeff(x[(idx - int(0.5 * idx)) : (idx + int(0.5 * idx))],
                                 y[(idx - int(0.5 * idx)) : (idx + int(0.5 * idx))]))
    y_base = y_fitted_line(m_val, b_val, x)
    return y_base


def peak_detection_fxn(data_y):
    """The function takes an input of the column containing the y variables in
    the dataframe, associated with the current. The function calls the split
    function, which splits the column into two arrays, one of the positive and
    one of the negative values. This is because cyclic voltammetry delivers
    negative peaks,but the peakutils function works better with positive peaks.
    The function also runs on the middle 80% of data to eliminate unnecessary
    noise and messy values associated with pseudo-peaks.The vectors are then
    imported into the peakutils. Indexes function to determine the significant
    peak for each array. The values are stored in a list, with the first index
    corresponding to the top peak and the second corresponding to the bottom
    peak.
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
    col_y1, col_y2 = split(data_y)  # removed main. head.

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
    index = peak_detection_fxn(dataframe_y)
    potential1, potential2 = split(dataframe_x)
    current1, current2 = split(dataframe_y)
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
    col_x1, col_x2 = split(dataframe_x)
    col_y1, col_y2 = split(dataframe_y)
    line_at_min = linear_background(col_x1, col_y1)[peak_detection_fxn(dataframe_y)[1]]
    line_at_max = linear_background(col_x2, col_y2)[peak_detection_fxn(dataframe_y)[0]]
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


def data_analysis(data):
    """This function returns a dictionary consisting of
    the relevant values. This can be seen in the user
    interface (Dash) as well."""
    results_dict = {}

    # df = main.data_frame(dict_1,1)
    x_val = data['Potential']
    y_val = data['Current']
    # Peaks are here [list]
    peak_index = peak_detection_fxn(y_val)
    # Split x,y to get baselines
    col_x1, col_x2 = split(x_val)
    col_y1, col_y2 = split(y_val)
    y_base1 = linear_background(col_x1, col_y1)
    y_base2 = linear_background(col_x2, col_y2)
    # Calculations based on baseline and peak
    values = peak_values(x_val, y_val)
    esub_t = values[0]
    esub_b = values[2]
    dof_e = del_potential(x_val, y_val)
    half_e = min(esub_t, esub_b) + half_wave_potential(x_val, y_val)
    ipa = peak_heights(x_val, y_val)[0]
    ipc = peak_heights(x_val, y_val)[1]
    ratio_i = peak_ratio(x_val, y_val)
    results_dict['Peak Current Ratio'] = ratio_i
    results_dict['Ipc (A)'] = ipc
    results_dict['Ipa (A)'] = ipa
    results_dict['Epc (V)'] = esub_b
    results_dict['Epa (V)'] = esub_t
    results_dict['∆E (V)'] = dof_e
    results_dict['Redox Potential (V)'] = half_e
    if dof_e > 0.3:
        results_dict['Reversible'] = 'No'
    else:
        results_dict['Reversible'] = 'Yes'
    if half_e > 0 and  'Yes' in results_dict.values():
        results_dict['Type'] = 'Catholyte'
    elif 'Yes' in results_dict.values():
        results_dict['Type'] = 'Anolyte'
    return results_dict, col_x1, col_x2, col_y1, col_y2, y_base1, y_base2, peak_index
    #return results_dict
