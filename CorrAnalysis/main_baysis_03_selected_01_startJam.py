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
from pandas_profiling import ProfileReport

from func_correlation import numerical_encoding, compute_correlations
from func_plot import plot_correlation, tex_fonts, \
    plot_congestion_dist, set_size
from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    generate_report = True

    data_path = 'data/'
    work_path = data_path + 'BAYSIS/03_selected_01_startJam/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    csv_path = work_path + 'csv/'

    work_file = 'BAYSIS_2019.csv'

    file_prefix = 'baysis_selected'
    file_plot_type = '.pdf'

    baysis_read = pd.read_csv(data_path + 'BAYSIS/02_matched/' + work_file, sep=';', decimal=',', parse_dates=True,
                              date_parser=date_parser)

    baysis_import = baysis_read[
        [
            # Congestion Data
            "TempMax",
            "TempAvg",
            "SpatMax",
            "SpatAvg",
            "TempDist",
            "SpatDist",
            "Coverage",
            # The temporal reference of if the incident to the congestion. The incident...
            # [-1] = Not Set
            # [1] = is before
            # [2] = is overlapping before
            # [3] = is during
            # [4] = is overlapping after
            # [5] = is after
            "TempGL",
            # The spatial reference of if the incident to the congestion. The incident...
            # [-1] = Not Set in case of congestion with no distance
            # [1] = is before
            # [2] = is during or overlapping
            # [3] = is after
            "SpatGL",
            # The temporal reference of if the incident is during the congestion. The incident is within...
            # [-1] = Not Set in case not during or overlapping
            # [1] = 10% to Beginning
            # [2] = 10% - 30% to Beginning
            # [3] = 30% - 70% (Middle)
            # [4] = 30% - 10% to Ending
            # [5] = 10% to Ending
            "TempIL",
            # The spatial reference of if the incident is during the congestion. The incident is within...
            # [-1] = Not Set in case not during or overlapping
            # [1] = 10% to Beginning
            # [2] = 10% - 30% to Beginning
            # [3] = 30% - 70% (Middle)
            # [4] = 30% - 10% to Ending
            # [5] = 10% to Ending
            "SpatIL",
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
    baysis_read['Date'] = pd.to_datetime(baysis_read['Date'], format='%Y-%m-%d')

    # Manual data type conversion from str to int64
    baysis_import["TLCar"] = pd.to_numeric(baysis_import["TLCar"])
    baysis_import["TLHGV"] = pd.to_numeric(baysis_import["TLHGV"])
    baysis_import["TLCar"] = baysis_import["TLCar"].astype('int64')
    baysis_import["TLHGV"] = baysis_import["TLHGV"].astype('int64')

    # Add month of roadwork
    baysis_import['Month'] = baysis_read['Date'].dt.strftime('%b')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Removing errors in WoTag
    days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    baysis_import['WoTag'].loc[np.invert(baysis_import['WoTag'].isin(days))] = ''

    # Removing whitespaces
    baysis_import['Strasse'] = baysis_import['Strasse'].str.replace(' ', '')

    #################
    ### Selection ###
    #################

    # select temporal before, overlapping during
    baysis_selected = baysis_import.loc[
        (baysis_import["TempGL"].isin([1, 2, 3]))
    ]

    # select temporal outside, 0 - 30
    baysis_selected = baysis_selected.loc[
        (baysis_selected["TempIL"].isin([-1, 1, 2]))
    ]

    # select spatial before or during
    baysis_selected = baysis_selected.loc[
        (baysis_selected["SpatGL"].isin([1, 2]))
    ]

    ####################################
    ### Congestion (Before Cleaning) ###
    ####################################

    plot_congestion_dist(
        ["TempMax",
         "TempAvg",
         "SpatMax",
         "SpatAvg",
         "TempDist",
         "SpatDist",
         "Coverage",
         "TLCar",
         "TLHGV"],
        baysis_selected, plot_path + 'cong_before_clean/', file_prefix, save_plot, show_plot)

    ################
    ### Cleaning ###
    ################

    baysis_selected = baysis_selected.drop(baysis_selected[baysis_selected['SpatMax'] > 50000].index)

    ####################################
    ### Congestion (After Cleaning) ###
    ####################################

    plot_congestion_dist(
        ["TempMax",
         "TempAvg",
         "SpatMax",
         "SpatAvg",
         "TempDist",
         "SpatDist",
         "Coverage",
         "TLCar",
         "TLHGV"],
        baysis_selected, plot_path + 'cong_after_clean/', file_prefix, save_plot, show_plot)

    ##################
    ### Histograms ###
    ##################

    # Plot histogram of accidents over time / months
    plt.figure(figsize=(13, 6))
    plt.title('Histogram of accidents per month, with at least one adjacent congestion')
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.ylabel('Count')
    ax = sns.countplot(x='Month', data=baysis_selected, palette='Spectral', order=months)
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_hist_month.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Remove month column
    # baysis_selected.drop('Month', axis='columns', inplace=True)

    # Plot histogram of accidents over highway
    plt.figure(figsize=(13, 6))
    plt.title('Histogram of accidents per highways, with at least one adjacent congestion')
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.ylabel('Count')
    ax = sns.countplot(x='Strasse', data=baysis_selected, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_hist_highway.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    ##############
    ### Counts ###
    ##############

    # Multi plots

    scale = 1.0
    (width, height) = set_size(418, scale)

    fig, axs = plt.subplots(4, 1, figsize=(width, 3.5 * height))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    sns.countplot(ax=axs[0], x='Kat', data=baysis_selected, palette='Spectral')
    sns.countplot(ax=axs[1], x='Typ', data=baysis_selected, palette='Spectral')
    sns.countplot(ax=axs[2], x='Betei', data=baysis_selected, palette='Spectral')
    atr = 'UArt'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    sns.countplot(ax=axs[3], x=atr, data=concat, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_multiple01.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    fig, axs = plt.subplots(4, 1, figsize=(width, 3.5  * height))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    atr = 'AUrs'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    sns.countplot(ax=axs[0], x=atr, data=concat, palette='Spectral')
    sns.countplot(ax=axs[1], x='AufHi', data=baysis_selected, palette='Spectral')
    atr = 'Char'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    sns.countplot(ax=axs[2], x=atr, data=concat, palette='Spectral')
    atr = 'Bes'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    sns.countplot(ax=axs[3], x=atr, data=concat, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_multiple02.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    fig, axs = plt.subplots(4, 1, figsize=(width, 3.5 * height))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    atr = 'Lich'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    sns.countplot(ax=axs[0], x=atr, data=concat, palette='Spectral')
    atr = 'Zust'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    sns.countplot(ax=axs[1], x=atr, data=concat, palette='Spectral')
    sns.countplot(ax=axs[2], x='Fstf', data=baysis_selected, palette='Spectral')
    sns.countplot(ax=axs[3], x='WoTag', data=baysis_selected, palette='Spectral',
                  order=['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'])
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_multiple03.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    baysis_matched.drop('Bes1', axis='columns', inplace=True)
    baysis_matched.drop('Bes2', axis='columns', inplace=True)

    ###############
    ### Scatter ###
    ###############

    ###########
    ### Box ###
    ###########

    ##############
    ### Report ###
    ##############

    if generate_report:
        report = ProfileReport(baysis_selected, title='BAYSIS Selected Dataset Report')
        report.to_file(work_path + file_prefix + '_report.html')

    ###################
    ### Encoding ###
    ###################

    # define column types
    nominal_columns = [
        "Str", "Kat", "Typ",
        "UArt1", "UArt2",
        "AUrs1", "AUrs2",
        "AufHi",
        "Char1", "Char2",
        "Bes1", "Bes2",
        "Lich1", "Lich2",
        "Zust1", "Zust2",
        "WoTag",
        'Month']
    dichotomous_columns = ["Alkoh"]
    ordinal_columns = ["Betei", "Fstf", "FeiTag"]

    # Encode non numerical columns
    baysis_encoded, baysis_encoded_dict = numerical_encoding(baysis_selected,
                                                             ["Strasse",
                                                              "Fstf",
                                                              'Month'],
                                                             drop_single_label=False,
                                                             drop_fact_dict=False)
    baysis_encoded.to_csv(csv_path + 'encoded.csv', index=False, sep=';')

    with open(csv_path + 'encoded_dict.csv', 'w') as tf:
        for key in baysis_encoded_dict.keys():
            tf.write("%s, %s\n" % (key, baysis_encoded_dict[key]))

    ###################
    ### Correlation ###
    ###################

    baysis_encoded = baysis_encoded.rename(columns={"TempMax": "TMax",
                                                    "TempAvg": "TAvg",
                                                    "SpatMax": "SMax",
                                                    "SpatAvg": "SAvg",
                                                    "Coverage": "Cov",
                                                    "TempDist": "TDist",
                                                    "SpatDist": "SDist",
                                                    'Strasse': "Str"})

    baysis_encoded = baysis_encoded.drop(columns=["TempGL",
                                                  "SpatGL",
                                                  "TempIL",
                                                  "SpatIL"])

    # Calculate with Cramers 's V
    results = None  # To make sure that no old data is reused
    results = compute_correlations(
        baysis_encoded,
        columns_nominal=nominal_columns, columns_dichotomous=dichotomous_columns, columns_ordinal=ordinal_columns,
        bias_correction=False)

    # Plot correlation matrix
    plot_correlation(results.get('correlation'), results.get('columns'),
                     nominal_columns, dichotomous_columns, ordinal_columns,
                     results.get('inf_nan_corr'),
                     results.get('columns_single_value'),
                     save=save_plot, filepath=plot_path + file_prefix + '_corr_cramers.pdf',
                     show=show_plot, figsize=(18, 15))

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + file_prefix + '_corr_cramers.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + file_prefix + '_sign_cramers.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex(float_format="{:0.3f}".format))

    with open(tex_path + file_prefix + '_coef_cramers.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex(escape=False))

    # Calculate with Theil's U
    results = None  # To make sure that no old data is reused
    results = compute_correlations(
        baysis_encoded,
        theils=True,
        columns_nominal=nominal_columns, columns_dichotomous=dichotomous_columns, columns_ordinal=ordinal_columns,
        bias_correction=False)

    # Plot correlation matrix
    plot_correlation(results.get('correlation'), results.get('columns'),
                     nominal_columns, dichotomous_columns, ordinal_columns,
                     results.get('inf_nan_corr'),
                     results.get('columns_single_value'),
                     save=save_plot, filepath=plot_path + file_prefix + '_corr_theils.pdf',
                     show=show_plot, figsize=(18, 15))

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + file_prefix + '_corr_theils.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + file_prefix + '_sign_theils.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex(float_format="{:0.3f}".format))

    with open(tex_path + file_prefix + '_coef_theils.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex(escape=False))

    ######################
    ### Scatter Matrix ###
    ######################

    # https://seaborn.pydata.org/examples/scatterplot_matrix.html
    # sns.set_theme(style='ticks')
    # sns.pairplot(baysis_selected, hue='Kat')
    # plt.show()

    print('Finished BAYSIS Selected Analysis')
