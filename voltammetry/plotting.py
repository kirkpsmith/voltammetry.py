import numpy as np
import pandas as pd
import altair as alt
alt.data_transformers.enable('default', max_rows=None)
def plot_voltammogram(t, i, v, convention = 'IUPAC', peaks = None, baselines = None):
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

    chart = alt.Chart(source).mark_line().encode(
    x='v:Q',
    y='i:Q'
    )
    if peaks is not None:
        source = pd.DataFrame(peaks,columns=['i','v'])
        peak_chart = alt.Chart(source).mark_point(filled=True, size=50).encode(
        x='v:Q',
        y='i:Q',
        color=alt.value('black')
        )
        chart = chart + peak_chart
    if baselines is not None:
        source = pd.DataFrame(baselines,columns=['b1','b2'])
        peak_chart = alt.Chart(source).mark_point(filled=True, size=50).encode(
        x='b1:Q',
        y='b2:Q',
        color=alt.value('black')
        )
        chart = chart + peak_chart
    return chart
