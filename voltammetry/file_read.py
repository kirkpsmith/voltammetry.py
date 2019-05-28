"""This module test the file reading functions."""

import copy
import pandas as pd
import matplotlib.pyplot as plt


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


#df = pd.DataFrame(list(dict1['df_1'].items()))
#list1, list2 = list(dict1['df_1'].items())
#list1, list2 = list(dict1.get('df_'+str(1)))

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
