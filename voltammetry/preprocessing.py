"""
Methods for preprocessing voltammetry data from instrument files
"""

import numpy as np


def readFile(filename, type=None, scan = 'last'):
    """ A wrapper for reading in many common types of impedance files

    Parameters
    ----------
    filename: string
        Filename to extract impedance data from
    type: string
        Type of instrument file
    scan: string
        First scan, last scan, or average of last (n-1) scans

    Returns
    -------
    time : np.ndarray
        Array of frequencies
    current : np.ndarray
        Array of currents
    voltage : np.ndarray
        Array of voltages

    """

    supported_types = ['gamry', 'autolab', 'parstat']

    if type is not None:
        assert type in supported_types,\
            '{} is not a supported type ({})'.format(type, supported_types)

    if type == 'gamry':
        t, i, v = readGamry(filename)
    elif type == 'autolab':
        t, i, v = readAutolab(filename)
    elif type == 'parstat':
        t, i, v = readParstat(filename)
    elif type is None:
        t, i, v = readCSV(filename)

    return t, i , v


def readGamry(filename):
    """ function for reading the .DTA file from Gamry

    Parameters
    ----------
    filename: string
        Filename of .DTA file to extract impedance data from

    Returns
    -------
    time : np.ndarray
        Array of frequencies
    current : np.ndarray
        Array of currents
    voltage : np.ndarray
        Array of voltages

    """

    with open(filename, 'r', encoding='ISO-8859-1') as input:
        lines = input.readlines()

    for i, line in enumerate(lines):
        if 'ZCURVE' in line:
            start_line = i

    raw_data = lines[start_line + 3:]
    f, Z = [], []
    for line in raw_data:
        each = line.split()
        f.append(float(each[2]))
        Z.append(complex(float(each[3]), float(each[4])))

    return np.array(f), np.array(Z)


def readAutolab(filename):
    """ function for reading the .csv file from Autolab

    Parameters
    ----------
    filename: string
        Filename of .csv file to extract impedance data from

    Returns
    -------
    time : np.ndarray
        Array of frequencies
    current : np.ndarray
        Array of currents
    voltage : np.ndarray
        Array of voltages

    """

    with open(filename, 'r') as input:
        lines = input.readlines()

    raw_data = lines[1:]
    f, Z = [], []
    for line in raw_data:
        each = line.split(',')
        f.append(each[0])
        Z.append(complex(float(each[1]), float(each[2])))

    return np.array(t), np.array(i), np.array(v)


# def readParstat(filename):
#     """ function for reading the .txt file from Parstat
#
#     Parameters
#     ----------
#     filename: string
#         Filename of .txt file to extract impedance data from
#
#     Returns
#     -------
#     time : np.ndarray
#         Array of frequencies
#     current : np.ndarray
#         Array of currents
#     voltage : np.ndarray
#         Array of voltages
#
#     """
#
#     with open(filename, 'r') as input:
#         lines = input.readlines()
#
#     raw_data = lines[1:]
#     f, Z = [], []
#     for line in raw_data:
#         each = line.split()
#         f.append(each[4])
#         Z.append(complex(float(each[6]), float(each[7])))
#
#     return np.array(f), np.array(Z)


# def readCSV(filename):
#     data = np.genfromtxt(filename, delimiter=',')
#
#     f = data[:, 0]
#     Z = data[:, 1] + 1j*data[:, 2]
#
#     return f, Z
