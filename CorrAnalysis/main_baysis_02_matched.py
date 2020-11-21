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
    plot_congestion_dist
from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    generate_report = True

    data_path = 'data/'
    work_path = data_path + 'BAYSIS/02_matched/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    csv_path = work_path + 'csv/'

    work_file = 'BAYSIS_2019_cleaned.csv'

    file_prefix = 'baysis_matched'
    file_plot_type = '.pdf'

    ##############
    ### Import ###
    ##############

    baysis_imported = pd.read_csv(work_path + work_file, sep=';', decimal=',', parse_dates=True,
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
        baysis_matched, plot_path + 'cong_before_clean/', file_prefix, save_plot, show_plot)

    ################
    ### Cleaning ###
    ################

    baysis_matched = baysis_matched.drop(baysis_matched[baysis_matched['SpatMax'] > 50000].index)

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
        baysis_matched, plot_path + 'cong_after_clean/', file_prefix, save_plot, show_plot)

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
    ax = sns.countplot(x='Month', data=baysis_matched, palette='Spectral', order=months)
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
    plt.xlabel('Highway')
    ax = sns.countplot(x='Strasse', data=baysis_matched, palette='Spectral')
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

    ###############
    ### Scatter ###
    ###############

    ###########
    ### Box ###
    ###########

    ##################
    ### Report ###
    ##################

    if generate_report:
        report = ProfileReport(baysis_matched, title='BAYSIS Matched Dataset Report')
        report.to_file(work_path + file_prefix + '_report.html')

    ###################
    ### Correlation ###
    ###################

    # define column types
    nominal_columns = ['Str', 'Kat', 'Typ',
                       'UArt1', 'UArt2',
                       'AUrs1', 'AUrs2',
                       'AufHi',
                       'Char1', 'Char2',
                       'Lich1', 'Lich2',
                       'Zust1', 'Zust2',
                       'WoTag',
                       'Month']
    dichotomous_columns = ['Alkoh']
    ordinal_columns = ['Betei', 'Fstf', 'FeiTag']

    # Encode non numerical columns
    baysis_encoded, baysis_encoded_dict = numerical_encoding(baysis_matched,
                                                             ['Strasse',
                                                              'Fstf',
                                                              'WoTag',
                                                              'Month'],
                                                             drop_single_label=False,
                                                             drop_fact_dict=False)
    baysis_encoded.to_csv(csv_path + 'encoded.csv', index=False, sep=';')

    with open(csv_path + 'encoded_dict.csv', 'w') as tf:
        for key in baysis_encoded_dict.keys():
            tf.write("%s, %s\n" % (key, baysis_encoded_dict[key]))

    baysis_encoded = baysis_encoded.rename(columns={"TempMax": "TMax",
                                                    "TempAvg": "TAvg",
                                                    "SpatMax": "SMax",
                                                    "SpatAvg": "SAvg",
                                                    "Coverage": "Cov",
                                                    "TempDist": "TDist",
                                                    "SpatDist": "SDist",
                                                    'Strasse': "Str"})

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

    print('Finished BAYSIS Matched Analysis')
