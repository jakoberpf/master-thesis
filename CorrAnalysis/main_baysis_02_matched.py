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
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from func_correlation import associations
from func_utils import print_welcome

if __name__ == '__main__':
    print_welcome()

    safe_plots = True

    data_path = 'data/'
    work_path = data_path + 'BAYSIS/matched/'
    plot_path = work_path + 'plots/'
    work_file = 'BAYSIS_2019.csv'

    baysis_import = pd.read_csv(work_path + work_file, sep=";")

    baysis = baysis_import[
        [
            # Congestion Data
            "TempExMax",
            # "TempExMin",
            "SpatExMax",
            # "SpatExMin",
            "TempDist",
            "SpatDist",
            "Coverage",
            "temporalGlobalLoc",
            "spatialGlobalLoc",
            "temporalInternalLoc",
            "spatialInternalLoc",
            "TimeLossCar",
            "TimeLossHGV",
            # Accident Data
            "Kat", "Typ", "Betei",
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
            "Fstf",  # TODO deal with strings in numerical data column
            "StrklVu",  # TODO deal with strings in numerical data column
            "WoTagNr",  # Already represented by WoTag
            "WoTag",
            "FeiTag"]].copy()

    # column = 'TempExMax'
    # values = [1, 2, 3, 4, 5, 6]
    # conditions = [
    #     (baysis[column] <= 30),
    #     (baysis[column] > 30) & (baysis[column] <= 60),
    #     (baysis[column] > 60) & (baysis[column] <= 120),
    #     (baysis[column] > 120) & (baysis[column] <= 240),
    #     (baysis[column] > 240) & (baysis[column] <= 480),
    #     (baysis[column] > 480)
    # ]
    # baysis['TempExMaxKat'] = np.select(conditions, values)

    # column = 'SpatExMax'
    # values = [1, 2, 3, 4, 5, 6]
    # conditions = [
    #     (baysis[column] <= 1000),
    #     (baysis[column] > 1000) & (baysis[column] <= 2000),
    #     (baysis[column] > 2000) & (baysis[column] <= 4000),
    #     (baysis[column] > 4000) & (baysis[column] <= 8000),
    #     (baysis[column] > 8000) & (baysis[column] <= 16000),
    #     (baysis[column] > 16000)
    # ]
    # baysis['SpatExMaxKat'] = np.select(conditions, values)

    # Print matrix for debugging
    print(baysis)

    baysis.boxplot(column='TempExMax', grid=False)
    plt.show()
    baysis.boxplot(column='SpatExMax', grid=False)
    plt.show()

    # baysis.boxplot(column='TempExMaxKat', grid=False)
    # plt.show()
    # baysis.boxplot(column='SpatExMaxKat', grid=False)
    # plt.show()

    sns.boxplot(x='AUrs1', y='SpatExMax', data=baysis, palette='Set1')
    plt.show()

    # Plot features associations
    associations(baysis, point_biserial=True, chisquare=True, anova=False, theil_u=False, clustering=False,
                 figsize=(18, 15),
                 nominal_columns=["temporalGlobalLoc",
                                  "spatialGlobalLoc",
                                  "temporalInternalLoc",
                                  "spatialInternalLoc",
                                  "Kat", "Typ", "Betei", "UArt1", "UArt2", "AUrs1", "AUrs2", "AufHi", "Alkoh",
                                  "Char1", "Char2", "Bes1", "Bes2", "Lich1", "Lich2", "Zust1", "Zust2", "Fstf",
                                  "StrklVu", "WoTag", "FeiTag",
                                  # 'TempExMaxKat', 'SpatExMaxKat'
                                  ])

    associations(baysis, point_biserial=True, chisquare=True, anova=False, theil_u=True, clustering=False,
                 figsize=(18, 15),
                 nominal_columns=["temporalGlobalLoc",
                                  "spatialGlobalLoc",
                                  "temporalInternalLoc",
                                  "spatialInternalLoc",
                                  "Kat", "Typ", "Betei", "UArt1", "UArt2", "AUrs1", "AUrs2", "AufHi", "Alkoh",
                                  "Char1", "Char2", "Bes1", "Bes2", "Lich1", "Lich2", "Zust1", "Zust2", "Fstf",
                                  "StrklVu", "WoTag", "FeiTag",
                                  # 'TempExMaxKat', 'SpatExMaxKat'
                                  ])

    print("Finished")
