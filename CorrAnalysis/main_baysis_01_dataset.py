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
import pandas as pd

from func_correlation import associations
from func_utils import print_welcome, date_parser

if __name__ == '__main__':
    print_welcome()

    safe_plots = True

    data_path = 'data/'
    work_path = data_path + 'BAYSIS/dataset/'
    plot_path = work_path + 'plots/'
    work_file = 'BAYSIS_2019.csv'

    baysis_import = pd.read_csv(work_path + work_file, sep=';', decimal=',', parse_dates=True, date_parser=date_parser)

    baysis_select_relevant = baysis_import[
        ["Kat", "Typ", "Betei",
         "UArt1", "UArt2",
         "AUrs1", "AUrs2",
         "AufHi",
         "Alkoh",
         "Char1", "Char2",
         "Char3",  # Not relevant because empty
         "Bes1", "Bes2",
         "Bes3",  # Not relevant because empty
         "Lich1", "Lich2",
         "Zust1", "Zust2",
         "Fstf",
         "StrklVu",
         "WoTagNr",  # Already represented by WoTag
         # "WoTag",
         "FeiTag"]].copy()

    # Manual data type conversion from str to datetime64
    baysis_import['Datum'] = pd.to_datetime(baysis_import['Datum'], format='%d.%m.%y')

    # Add month of roadwork
    baysis_select_relevant['Month'] = baysis_import['Datum'].dt.month_name()

    # Plot histogram of roadworks over time / months
    plt.figure(figsize=(13, 6))
    plt.hist(baysis_select_relevant['Month'], color='blue', edgecolor='black')
    plt.title('Histogram of accidents per month')
    plt.ylabel('Count')
    plt.xlabel('Month of 2019')
    if safe_plots:
        plt.savefig(plot_path + 'baysis_dataset_hist_month.png')
    plt.show()

    baysis_select_relevant.drop('Month', axis='columns', inplace=True)

    # Plot association matrix
    # Calculate without Theil's U -> Cramer's V
    associations(baysis_select_relevant, anova=True, theil_u=False, clustering=False,
                 figsize=(18, 15),
                 nominal_columns=["Kat", "Typ", "Betei", "UArt1", "UArt2", "AUrs1", "AUrs2", "AufHi", "Alkoh",
                                  "Char1", "Char2", "Bes1", "Bes2", "Lich1", "Lich2", "Zust1", "Zust2", "Fstf",
                                  "StrklVu", "WoTagNr", "FeiTag"],
                 plot=False, bias_correction=False)
    if safe_plots:
        plt.savefig(plot_path + 'baysis_dataset_corr_cramers.png')
    plt.show()

    # Calculate with Theil's U
    associations(baysis_select_relevant, anova=True, theil_u=True, clustering=False,
                 figsize=(18, 15),
                 nominal_columns=["Kat", "Typ", "Betei", "UArt1", "UArt2", "AUrs1", "AUrs2", "AufHi", "Alkoh",
                                  "Char1", "Char2", "Bes1", "Bes2", "Lich1", "Lich2", "Zust1", "Zust2", "Fstf",
                                  "StrklVu", "WoTagNr", "FeiTag"],
                 plot=False, bias_correction=False)
    if safe_plots:
        plt.savefig(plot_path + 'baysis_dataset_corr_theils.png')
    plt.show()

    print("Finished")
