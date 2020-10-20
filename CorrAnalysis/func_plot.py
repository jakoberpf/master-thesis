#  Copyright (c) Jakob Erpf 2020
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#  Written by Jakob Erpf <contact@jakoberpf.de>, 2020.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_correlation(corr, columns,
                     nominal_columns=None,
                     dichotomous_columns=None,
                     ordinal_columns=None,
                     inf_nan=None,
                     single_value_columns=None,
                     save=False,
                     filepath='plot.png',
                     show=True,
                     ax=None,
                     figsize=None,
                     annot=True,
                     fmt='.2f',
                     cmap=None,
                     sv_color='silver',
                     cbar=True,
                     scale=1.0
                     ):
    """

    Parameters:
    -----------


    nominal_columns : string / list / NumPy ndarray
        Names of columns of the data-set which hold categorical values.
    mark_columns : Boolean, default = False
        if True, output's columns' names will have a suffix of '(nom)' or
        '(con)' based on there type (eda_tools or continuous), as provided
        by nominal_columns

    ax : matplotlib ax, default = None
        Matplotlib Axis on which the heat-map will be plotted
    figsize : (int,int) or None, default = None
        A Matplotlib figure-size tuple. If `None`, falls back to Matplotlib's
        default. Only used if `ax=None`.
    annot : Boolean, default = True
        Plot number annotations on the heat-map
    fmt : string, default = '.2f'
        String formatting of annotations
    cmap : Matplotlib colormap or None, default = None
        A colormap to be used for the heat-map. If None, falls back to Seaborn's
        heat-map default
    sv_color : string, default = 'silver'
        A Matplotlib color. The color to be used when displaying single-value
        features over the heat-map
    cbar: Boolean, default = True
        Display heat-map's color-bar

    Returns:
    --------
    A dictionary with the following keys:
    - `corr`: A DataFrame of the correlation/strength-of-association between
    all features
    - `ax`: A Matplotlib `Axe`

    """

    if ax is None:
        # If no figure/mathplotlib is given, set new figure size
        plt.figure(figsize=figsize)

    if figsize is None:
        x, y = set_size(418, scale)
        plt.figure(figsize=(x, x))

    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)

    if inf_nan.any(axis=None):
        inf_nan_mask = np.vectorize(lambda x: not bool(x))(inf_nan.values)
        ax = sns.heatmap(inf_nan_mask,
                         cmap=['white'],
                         annot=inf_nan if annot else None,
                         fmt='',
                         center=0,
                         square=True,
                         ax=ax,
                         mask=inf_nan_mask,
                         cbar=False)
    else:
        inf_nan_mask = np.ones_like(corr)

    if len(single_value_columns) > 0:
        # If dataframe contains single value columns
        sv = pd.DataFrame(data=np.zeros_like(corr),
                          columns=columns,
                          index=columns)
        for c in single_value_columns:
            sv.loc[:, c] = ' '
            sv.loc[c, :] = ' '
            sv.loc[c, c] = 'SV'
        sv_mask = np.vectorize(lambda x: not bool(x))(sv.values)
        ax = sns.heatmap(sv_mask,
                         cmap=[sv_color],
                         annot=sv if annot else None,
                         fmt='',
                         center=0,
                         square=True,
                         ax=ax,
                         mask=sv_mask,
                         cbar=False)
    else:
        sv_mask = np.ones_like(corr)

    # combine inf_nan_mask and sv_mask into one mask for all not available values
    mask = np.vectorize(lambda x: not bool(x))(inf_nan_mask) + np.vectorize(lambda x: not bool(x))(sv_mask)

    ax = sns.heatmap(corr,
                     cmap=cmap,
                     annot=annot,
                     fmt=fmt,
                     center=0,
                     vmax=1.0,
                     # if there are only
                     vmin=-1.0 if len(columns) - len(nominal_columns) >= 2 else 0.0,
                     square=True,
                     mask=mask,
                     ax=ax,
                     cbar=cbar)

    if save:
        plt.savefig(filepath)
    if show:
        plt.show()
    else:
        plt.close()

    return ax


def plot_statistic(corr, columns,
                   nominal_columns=None,
                   dichotomous_columns=None,
                   ordinal_columns=None,
                   inf_nan=None,
                   single_value_columns=None,
                   save=False,
                   filepath='plot.png',
                   show=True,
                   ax=None,
                   figsize=None,
                   annot=True,
                   fmt='.4f',
                   cmap=None,
                   sv_color='silver',
                   cbar=True,
                   scale=1.0
                   ):
    if ax is None:
        # If no figure/mathplotlib is given, set new figure size
        plt.figure(figsize=figsize)

    if figsize is None:
        x, y = set_size(418, scale)
        plt.figure(figsize=(x, x))

    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)

    if inf_nan.any(axis=None):
        inf_nan_mask = np.vectorize(lambda x: not bool(x))(inf_nan.values)

        ax = sns.heatmap(inf_nan_mask,
                         cmap=['white'],
                         annot=inf_nan if annot else None,
                         fmt='',
                         center=0,
                         square=True,
                         ax=ax,
                         mask=inf_nan_mask,
                         cbar=False)
    else:
        inf_nan_mask = np.ones_like(corr)

    if len(single_value_columns) > 0:
        # If dataframe contains single value columns
        sv = pd.DataFrame(data=np.zeros_like(corr),
                          columns=columns,
                          index=columns)
        for c in single_value_columns:
            sv.loc[:, c] = ' '
            sv.loc[c, :] = ' '
            sv.loc[c, c] = 'SV'
        sv_mask = np.vectorize(lambda x: not bool(x))(sv.values)
        ax = sns.heatmap(sv_mask,
                         cmap=[sv_color],
                         annot=sv if annot else None,
                         fmt='',
                         center=0,
                         square=True,
                         ax=ax,
                         mask=sv_mask,
                         cbar=False)
    else:
        sv_mask = np.ones_like(corr)

    mask = np.vectorize(lambda x: not bool(x))(inf_nan_mask) + np.vectorize(lambda x: not bool(x))(sv_mask)
    ax = sns.heatmap(corr,
                     cmap=cmap,
                     annot=annot,
                     fmt=fmt,
                     center=0,
                     vmax=1.0,
                     # if there are only
                     vmin=-1.0 if len(columns) - len(nominal_columns) >= 2 else 0.0,
                     square=True,
                     mask=mask,
                     ax=ax,
                     cbar=cbar)

    if save:
        plt.savefig(filepath)
    if show:
        plt.show()
    else:
        plt.close()

    return ax


def plot_congestion_dist(columns, dataframe, path, prefix, save, show):
    for atr in columns:
        plt.figure(figsize=set_size(418))
        plt.style.use('seaborn')
        plt.rcParams.update(tex_fonts)
        plt.title('Distribution of ' + atr)
        plt.ylabel('Count')
        sns.displot(x=atr, data=dataframe, palette='Spectral')
        if atr is 'TempExMax':
            plt.xlabel('Maximum temporal extend [min]')
        elif atr is 'SpatExMax':
            plt.xlabel('Maximum spatial extend [m]')
        elif atr is 'TempDist':
            plt.xlabel('Minimum temporal distance to incident [min]')
        elif atr is 'SpatDist':
            plt.xlabel('Minimum spatial distance to incident [m]')
        elif atr is 'temporalGlobalLoc':
            plt.xlabel('Relative temporal location')
        elif atr is 'spatialGlobalLoc':
            plt.xlabel('Relative spatial location')
        elif atr is 'temporalInternalLoc':
            plt.xlabel('Internal relative temporal location')
        elif atr is 'spatialInternalLoc':
            plt.xlabel('Internal relative spatial location')
        elif atr is 'Coverage':
            plt.xlabel('')
        elif atr is 'TimeLossCar':
            plt.xlabel('TimeLossCar')
        elif atr is 'TimeLossHGV':
            plt.xlabel('TimeLossHGV')
        else:
            plt.xlabel(atr)
        if save:
            plt.savefig(path + prefix + '_congestion_dist_' + atr + '.pdf')
        if show:
            plt.show()
        else:
            plt.close()


def plot_baysis_dist(columns, dataframe, path, prefix, save, show):
    for atr in columns:
        plt.figure(figsize=set_size(418, 1.0))
        plt.style.use('seaborn')
        plt.rcParams.update(tex_fonts)
        plt.title('Distribution of ' + atr)
        plt.ylabel('Count')
        plt.xlabel(atr)
        ax = sns.displot(x=atr, data=dataframe, palette='Spectral')
        if save:
            plt.savefig(path + prefix + '_dist_' + atr + '.pdf')
        if show:
            plt.show()
        else:
            plt.close()


def plot_arbis_dist(columns, dataframe, path, prefix, save, show):
    for atr in columns:
        plt.figure(figsize=set_size(418, 1.0))
        plt.style.use('seaborn')
        plt.rcParams.update(tex_fonts)
        plt.title('Distribution of ' + atr)
        plt.ylabel('Count')
        plt.xlabel(atr)
        ax = sns.displot(x=atr, data=dataframe, palette='Spectral')
        if save:
            plt.savefig(path + prefix + '_dist_' + atr + '.pdf')
        if show:
            plt.show()
        else:
            plt.close()


def plot_baysis_scatter(measurement, categories, dataframe, path, prefix, save, show):
    for atr_m in measurement:
        for atr_c in categories:
            plt.figure(figsize=set_size(418, 1.0))
            plt.style.use('seaborn')
            plt.rcParams.update(tex_fonts)
            plt.title('Scatterplot of ' + atr_m + ' and ' + atr_c)
            plt.ylabel(atr_m)
            plt.xlabel(atr_c)
            ax = sns.stripplot(x=atr_c, y=atr_m, data=dataframe, palette='Spectral')
            if save:
                plt.savefig(path + prefix + '_scatter_' + atr_m + '_' + atr_c + '.pdf')
            if show:
                plt.show()
            else:
                plt.close()


def plot_arbis_scatter(measurement, categories, dataframe, path, prefix, save, show):
    for atr_m in measurement:
        for atr_c in categories:
            plt.figure(figsize=set_size(418, 1.0))
            plt.style.use('seaborn')
            plt.rcParams.update(tex_fonts)
            plt.title('Scatterplot of ' + atr_m + ' and ' + atr_c)
            plt.ylabel(atr_m)
            plt.xlabel(atr_c)
            ax = sns.scatterplot(x=atr_c, y=atr_m, data=dataframe, palette='Spectral')
            if save:
                plt.savefig(path + prefix + '_scatter_' + atr_m + '_' + atr_c + '.pdf')
            if show:
                plt.show()
            else:
                plt.close()


def plot_boxplot(data, x, y, save, show, file, figsize=None, scale=1):
    # Settings for box plots
    if figsize == None:
        plt.figure(figsize=set_size(418, scale))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    sns.boxplot(x=x, y=y, data=data, palette='Spectral')
    if save:
        plt.savefig(file)
    if show:
        plt.show()
    else:
        plt.close()


def plot_boxplot_logscale(data, x, y, save, show, file, figsize=None, scale=1):
    # Settings for box plots
    if figsize == None:
        plt.figure(figsize=set_size(418, scale))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.yscale('log')
    sns.boxplot(x=x, y=y, data=data, palette='Spectral')
    if save:
        plt.savefig(file)
    if show:
        plt.show()
    else:
        plt.close()


def set_size(width, fraction=1):
    """Set figure dimensions to avoid scaling in LaTeX.

    Parameters
    ----------
    width: float
            Document textwidth or columnwidth in pts
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # Width of figure (in pts)
    fig_width_pt = width * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5 ** .5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio

    fig_dim = (fig_width_in, fig_height_in)

    return fig_dim


tex_fonts = {
    # Use LaTeX to write all text
    "text.usetex": True,
    "font.family": "serif",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 10,
    "font.size": 10,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 8,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8
}
