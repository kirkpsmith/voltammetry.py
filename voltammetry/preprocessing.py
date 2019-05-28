"""
Methods for preprocessing voltammetry data from instrument files
"""

import numpy as np


def readFile(filename, type=None, scan='last'):
    """ A wrapper for reading in many common types of impedance files

    Parameters
    ----------
    filename: string
        Filename to extract impedance data from
    type: string
        Type of instrument file
    scan: string
        Specify first scan, last scan, or average of last (n-1) scans

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
        scans = readGamry(filename, scan)
    elif type == 'autolab':
        scans = readAutolab(filename, scan)
    elif type == 'parstat':
        scans = readParstat(filename, scan)
    elif type is None:
        scans = readCSV(filename)

    if scan == 'first':
        return (col for col in scans[0])
    elif scan == 'last':
        return (col for col in scans[-1])

    return '...'




def readGamry(filename, scan):
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
        start_lines, end_lines = [], []
        for i, line in enumerate(lines):
            if line.startswith('CYCLES'):
                n_cycles = int(line.split()[2])
            if line.startswith('SCANRATE'):
                scan_rate = float(line.split()[2])
            if line.startswith('CURVE'):
                start_lines.append(i+3)
                end_lines.append(i)
        start_lines = start_lines[0:n_cycles]
        end_lines = end_lines[1:n_cycles+1]
        scan_data = []
        for i in range(0,n_cycles):
            raw_data = lines[start_lines[i]:end_lines[i]]
            t, i, v = [], [], []
            for line in raw_data:
                each = line.split()
                t.append(float(each[1]))
                i.append(float(each[3]))
                v.append(float(each[2]))
            scan_data.append([np.array(t),np.array(i),np.array(v)])
        return scan_data
#
# def readAutolab(filename):
#     """ function for reading the .csv file from Autolab
#
#     Parameters
#     ----------
#     filename: string
#         Filename of .csv file to extract impedance data from
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
#         each = line.split(',')
#         f.append(each[0])
#         Z.append(complex(float(each[1]), float(each[2])))
#
#     return np.array(t), np.array(i), np.array(v)


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
