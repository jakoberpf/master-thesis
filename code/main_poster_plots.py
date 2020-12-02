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

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from func_plot import tex_fonts
from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = True

    file_plot_type = '.pdf'

    ##############
    ### Import ###
    ##############

    baysis_imported = pd.read_csv('data/BAYSIS/02_matched/' + 'BAYSIS_2019_cleaned.csv', sep=';', decimal=',', parse_dates=True,
                                  date_parser=date_parser)

    baysis_matched = baysis_imported[
        [
            # Congestion Data
            "TempMax",
            "TempAvg",
            "SpatMax",
            "SpatAvg",
            "TempDist",
            "SpatDist",
            "Coverage",
            "TLCar",
            "TLHGV",
            # Accident Data
            "Strasse",
            "Kat", "Typ", "Betei",
            "UArt1", "UArt2",
            "AUrs1", "AUrs2",
            "AufHi",
            "Alkoh",
            "Char1", "Char2",
            "Bes1", "Bes2",
            "Lich1", "Lich2",
            "Zust1", "Zust2",
            "Fstf",
            # "WoTagNr",  # Already represented by WoTag
            "WoTag",
            "FeiTag"]].copy()

    # Manual data type conversion from str to datetime64
    # baysis_imported['Date'] = pd.to_datetime(baysis_imported['Date'], format='%Y-%m-%d')
    baysis_imported['Date'] = pd.to_datetime(baysis_imported['Date'], format='%d.%m.%y')

    # Manual data type conversion from str to int64
    baysis_matched["TLCar"] = pd.to_numeric(baysis_matched["TLCar"])
    baysis_matched["TLHGV"] = pd.to_numeric(baysis_matched["TLHGV"])
    baysis_matched["TLCar"] = baysis_matched["TLCar"].astype('int64')
    baysis_matched["TLHGV"] = baysis_matched["TLHGV"].astype('int64')

    # Add month of roadwork
    baysis_matched['Month'] = baysis_imported['Date'].dt.strftime('%b')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Removing errors in WoTag
    days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    baysis_matched['WoTag'].loc[np.invert(baysis_matched['WoTag'].isin(days))] = -1

    # Removing whitespaces
    baysis_matched['Strasse'] = baysis_matched['Strasse'].str.replace(' ', '')

    ##################
    ### Histograms ###
    ##################

    # Plot histogram of accidents over time / months
    plt.figure(figsize=(13, 6))
    plt.title('Histogram of accidents per month, with at least one adjacent congestion')
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.ylabel('Count')
    plt.xlabel('Month of 2019')
    # https://seaborn.pydata.org/examples/scatterplot_matrix.html
    sns.set_theme(style='ticks')
    sns.pairplot(baysis_matched, hue='Kat')
    plt.show()
    if save_plot:
        plt.savefig('data/poster/' + 'pairplot.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()



