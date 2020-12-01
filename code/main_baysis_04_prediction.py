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

import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

from func_correlation import numerical_encoding, compute_correlations
from func_plot import plot_correlation
from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    generate_report = True

    data_path = 'data/'
    work_path = data_path + 'BAYSIS/04_predicted/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    csv_path = work_path + 'csv/'

    work_file = 'BAYSIS_2019.csv'

    file_prefix = 'baysis_predicted'
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

    baysis_selected = baysis_import

    ####################################
    ### Congestion (Before Cleaning) ###
    ####################################

    ################
    ### Cleaning ###
    ################

    baysis_selected = baysis_selected.drop(baysis_selected[baysis_selected['SpatMax'] > 50000].index)

    ####################################
    ### Congestion (After Cleaning) ###
    ####################################

    ##################
    ### Histograms ###
    ##################

    ##############
    ### Counts ###
    ##############

    ###############
    ### Scatter ###
    ###############

    ###########
    ### Box ###
    ###########

    #################
    ### Quantiles ###
    #################

    baysis_selected["TempMax"] = pd.qcut(baysis_selected["TempMax"], 4)
    baysis_selected["TempAvg"] = pd.qcut(baysis_selected["TempAvg"], 4)
    baysis_selected["SpatMax"] = pd.qcut(baysis_selected["SpatMax"], 4)
    baysis_selected["SpatAvg"] = pd.qcut(baysis_selected["SpatAvg"], 4)
    # baysis_selected["TempDist"] = pd.qcut(baysis_selected["TempDist"], 4)
    # baysis_selected["SpatDist"] = pd.qcut(baysis_selected["SpatDist"], 4)
    baysis_selected["Coverage"] = pd.qcut(baysis_selected["Coverage"], 4)
    baysis_selected["TLCar"] = pd.qcut(baysis_selected["TLCar"], 4)
    baysis_selected["TLHGV"] = pd.qcut(baysis_selected["TLHGV"], 4)

    baysis_selected["TempMax"] = baysis_selected["TempMax"].astype('string')
    baysis_selected["TempAvg"] = baysis_selected["TempAvg"].astype('string')
    baysis_selected["SpatMax"] = baysis_selected["SpatMax"].astype('string')
    baysis_selected["SpatAvg"] = baysis_selected["SpatAvg"].astype('string')
    baysis_selected["Coverage"] = baysis_selected["Coverage"].astype('string')
    baysis_selected["TLCar"] = baysis_selected["TLCar"].astype('string')
    baysis_selected["TLHGV"] = baysis_selected["TLHGV"].astype('string')

    ##############
    ### Report ###
    ##############

    if generate_report:
        report = ProfileReport(baysis_selected, title='BAYSIS Prediction Dataset Report')
        report.to_file(work_path + file_prefix + '_report.html')

    ################
    ### Encoding ###
    ################

    # define column types
    nominal_columns = [
        "TMax",
        "TAvg",
        "SMax",
        "SAvg",
        "TDist",
        "SDist",
        "Cov",
        "TLCar",
        "TLHGV",
        # Accident Data
        "Str",
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
        "WoTag",
        "FeiTag",
        'Month'
    ]
    dichotomous_columns = []
    ordinal_columns = []

    # Encode non numerical columns
    baysis_encoded, baysis_encoded_dict = numerical_encoding(baysis_selected,
                                                             ["Strasse",
                                                              "Fstf",
                                                              'Month',
                                                              "TempMax",
                                                              "TempAvg",
                                                              "SpatMax",
                                                              "SpatAvg",
                                                              "Coverage",
                                                              "TLCar",
                                                              "TLHGV"
                                                              ],
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

    # baysis_encoded = baysis_encoded.drop(columns=["TempGL",
    #                                               "SpatGL",
    #                                               "TempIL",
    #                                               "SpatIL"])

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
