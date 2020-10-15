#  Copyright (c) 2020. Jakob Erpf
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

import pandas as pd
import matplotlib.pyplot as plt

from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    data_path = 'data/'
    work_path = data_path + 'ArbIS/matched/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    work_file = 'ArbIS_2019.csv'

    arbis_imported = pd.read_csv(work_path + work_file, sep=';', decimal=',', parse_dates=True, date_parser=date_parser)

    arbis_selected = arbis_imported[
        [
            # Congestion Data
            "TempExMax",
            # "TempExMin [min]", # Not implemented
            "SpatExMax",
            # "SpatExMin [m]", # Not implemented
            "TempDist",
            "SpatDist",
            "Coverage",
            "TimeLossCar",
            "TimeLossHGV",
            # Accident Data
            # "Von", "Bis", # Not correlate able
            "Strasse",
            "AnzGesperrtFs",
            "Einzug",
            # "VonKilometer", # Not correlate able
            # "BisKilometer", # Not correlate able
            "Richtung",
            # "VonKilometerBlock", # Not correlate able
            # "BisKilometerBlock", # Not correlate able
            # "VonStation", "BisStation", # Not correlate able
            # "VonAbschnitt", "BisAbschnitt", # Not correlate able
            # "SperrungID", "StreckeID", # Not correlate able
            "Length",
            "Duration"]].copy()

    arbis_selected["TimeLossCar"] = pd.to_numeric(arbis_selected["TimeLossCar"])
    arbis_selected["TimeLossHGV"] = pd.to_numeric(arbis_selected["TimeLossHGV"])

    # Print matrix for debugging
    print(arbis_selected.dtypes)

    # Plot association matrix
    associations(arbis_selected, point_biserial=True, kruskal=False, theil_u=False, clustering=False,
                 figsize=(18, 15),
                 nominal_columns=["temporalGlobalLoc",
                                  "spatialGlobalLoc",
                                  "temporalInternalLoc",
                                  "spatialInternalLoc",
                                  "AnzGesperrtFs",
                                  "Richtung",
                                  "Strasse"
                                  ],
                 plot=False, bias_correction=False)
    if safe_plots:
        plt.savefig(plot_path + 'arbis_matched_corr_cramers.png')
    plt.show()

    # Plot association matrix
    associations(arbis_selected, point_biserial=True, kruskal=False, theil_u=True, clustering=False,
                 figsize=(18, 15),
                 nominal_columns=["temporalGlobalLoc",
                                  "spatialGlobalLoc",
                                  "temporalInternalLoc",
                                  "spatialInternalLoc",
                                  "AnzGesperrtFs",
                                  "Richtung",
                                  "Strasse"
                                  ],
                 plot=False, bias_correction=False)
    if safe_plots:
        plt.savefig(plot_path + 'arbis_matched_corr_theils.png')
    plt.show()

    # Plot scatter diagrams
    # Congestion -> Roadwork
    arbis_selected.plot.scatter(x='TempExMax', y='SpatExMax', c='AnzGesperrtFs', colormap='viridis')
    plt.show()
    arbis_selected.plot.scatter(x='TempExMax', y='SpatExMax', c='Einzug', colormap='viridis')
    plt.show()
    arbis_selected.plot.scatter(x='TempExMax', y='SpatExMax', c='Length', colormap='viridis')
    plt.show()
    arbis_selected.plot.scatter(x='TempExMax', y='SpatExMax', c='Duration', colormap='viridis')
    plt.show()
    # Roadwork -> Congestion
    arbis_selected.plot.scatter(x='Length', y='Duration', c='TempExMax', colormap='viridis')
    plt.show()
    arbis_selected.plot.scatter(x='Length', y='Duration', c='SpatExMax', colormap='viridis')
    plt.show()
    # arbis.plot.scatter(x='Length', y='Duration', c='TimeLossCar', colormap='viridis')
    # plt.show()
    # arbis.plot.scatter(x='Length', y='Duration', c='TimeLossHGV', colormap='viridis')
    # plt.show()
