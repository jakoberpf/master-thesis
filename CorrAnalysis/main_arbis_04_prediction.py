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
    work_path = data_path + 'ArbIS/04_predicted/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    csv_path = work_path + 'csv/'

    work_file = 'ArbIS_2019.csv'

    file_prefix = 'arbis_predicted'
    file_plot_type = '.pdf'

    arbis_read = pd.read_csv(data_path + 'ArbIS/02_matched/' + work_file, sep=';', decimal=',', parse_dates=True,
                             date_parser=date_parser)

    arbis_import = arbis_read[
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

    # Manual data type conversion from str to datetime64
    arbis_read['Von'] = pd.to_datetime(arbis_read['Von'], format='%Y-%m-%d %H:%M:%S')
    arbis_read['Bis'] = pd.to_datetime(arbis_read['Bis'], format='%Y-%m-%d %H:%M:%S')

    # Manual data type conversion from str to int64
    arbis_import["TLCar"] = pd.to_numeric(arbis_import["TLCar"])
    arbis_import["TLHGV"] = pd.to_numeric(arbis_import["TLHGV"])
    arbis_import["TLCar"] = arbis_import["TLCar"].astype('int64')
    arbis_import["TLHGV"] = arbis_import["TLHGV"].astype('int64')

    # Add month of roadwork
    arbis_import['Month'] = arbis_read['Von'].dt.strftime('%b')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    #################
    ### Selection ###
    #################

    arbis_selected = arbis_import

    ####################################
    ### Congestion (Before Cleaning) ###
    ####################################

    ################
    ### Cleaning ###
    ################

    arbis_selected = arbis_selected.drop(arbis_selected[arbis_selected['SpatMax'] > 50000].index)
    arbis_selected['TempDist'].loc[arbis_selected['TempDist'].isin([0])] = None
    arbis_selected['SpatDist'].loc[arbis_selected['SpatDist'].isin([0])] = None

    ####################################
    ### Congestion (After Cleaning) ###
    ####################################

    ##################
    ### Histograms ###
    ##################

    #####################
    ### Distributions ###
    #####################

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

    arbis_selected["TempMax"] = pd.qcut(arbis_selected["TempMax"], 4)
    arbis_selected["TempAvg"] = pd.qcut(arbis_selected["TempAvg"], 4)
    arbis_selected["SpatMax"] = pd.qcut(arbis_selected["SpatMax"], 4)
    arbis_selected["SpatAvg"] = pd.qcut(arbis_selected["SpatAvg"], 4)
    # arbis_selected["TempDist"] = pd.qcut(arbis_selected["TempDist"], 4)
    # arbis_selected["SpatDist"] = pd.qcut(arbis_selected["SpatDist"], 4)
    arbis_selected["Coverage"] = pd.qcut(arbis_selected["Coverage"], 4)
    arbis_selected["TLCar"] = pd.qcut(arbis_selected["TLCar"], 4)
    arbis_selected["TLHGV"] = pd.qcut(arbis_selected["TLHGV"], 4)

    arbis_selected["TempMax"] = arbis_selected["TempMax"].astype('string')
    arbis_selected["TempAvg"] = arbis_selected["TempAvg"].astype('string')
    arbis_selected["SpatMax"] = arbis_selected["SpatMax"].astype('string')
    arbis_selected["SpatAvg"] = arbis_selected["SpatAvg"].astype('string')
    arbis_selected["Coverage"] = arbis_selected["Coverage"].astype('string')
    arbis_selected["TLCar"] = arbis_selected["TLCar"].astype('string')
    arbis_selected["TLHGV"] = arbis_selected["TLHGV"].astype('string')

    ##############
    ### Report ###
    ##############

    if generate_report:
        report = ProfileReport(arbis_selected, title='ArbIS Prediction Dataset Report')
        report.to_file(work_path + file_prefix + '_report.html')

    ###################
    ### Correlation ###
    ###################

    # define column types
    nominal_columns = ['Str',
                       'Month']
    dichotomous_columns = ['Richtung']
    ordinal_columns = ['AnzGesperrtFs', 'Einzug',
                       "TempMax",
                       "TempAvg",
                       "SpatMax",
                       "SpatAvg",
                       "Coverage",
                       "TLCar",
                       "TLHGV"]

    # Encode non numerical columns
    arbis_encoded, arbis_encoded_dict = numerical_encoding(arbis_selected,
                                                           ["Strasse",
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
    arbis_encoded.to_csv(csv_path + 'encoded.csv', index=False, sep=';')

    with open(csv_path + 'encoded_dict.csv', 'w') as tf:
        for key in arbis_encoded_dict.keys():
            tf.write("%s, %s\n" % (key, arbis_encoded_dict[key]))

    arbis_encoded = arbis_encoded.rename(columns={"TempMax": "TMax",
                                                  "TempAvg": "TAvg",
                                                  "SpatMax": "SMax",
                                                  "SpatAvg": "SAvg",
                                                  "Coverage": "Cov",
                                                  "TempDist": "TDist",
                                                  "SpatDist": "SDist",
                                                  'Strasse': "Str",
                                                  'AnzGesperrtFs': 'AGF'})

    # arbis_encoded = arbis_encoded.drop(columns=["TempGL",
    #                                             "SpatGL",
    #                                             "TempIL",
    #                                             "SpatIL"])

    # Calculate with Cramers 's V
    results = None  # To make sure that no old data is reused
    results = compute_correlations(
        arbis_encoded,
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
        arbis_encoded,
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

    print('Finished ArbIS Dataset Analysis')
