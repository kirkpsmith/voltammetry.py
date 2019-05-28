import numpy as np
import pandas as pd
import altair as alt
alt.data_transformers.enable('default', max_rows=None)
def plot_voltammogram(t, i, v, convention = 'IUPAC'):
    """ Convenience function for plotting voltammograms


        Parameters
        ----------
        ax: matplotlib.axes.Axes
            axes on which to plot the nyquist plot
        freq: np.array of floats
            frequencies
        Z: np.array of complex numbers
            impedance data
        scale: float
            the scale for the axes
        units: string
            units for :math:`Z(\\omega)`
        fmt: string
            format string passed to matplotlib (e.g. '.-' or 'o')

        Returns
        -------
        ax: matplotlib.axes.Axes
    """
    source = pd.DataFrame({
        't': t,
        'i': i,
        'v': v,
    })

    chart = alt.Chart(source).mark_point().encode(
    x='v:Q',
    y='i:Q'
    )
    return chart
