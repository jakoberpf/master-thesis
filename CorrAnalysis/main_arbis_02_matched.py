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
import seaborn as sns
from pandas_profiling import ProfileReport

from func_correlation import numerical_encoding, compute_correlations
from func_plot import plot_correlation, set_size, tex_fonts, \
    plot_congestion_dist, plot_arbis_dist
from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    generate_report = False

    data_path = 'data/'
    work_path = data_path + 'ArbIS/02_matched/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    csv_path = work_path + 'csv/'

    work_file = 'ArbIS_2019.csv'

    file_prefix = 'arbis_matched'
    file_plot_type = '.pdf'

    arbis_read = pd.read_csv(work_path + work_file, sep=';', decimal=',', parse_dates=True, date_parser=date_parser)

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
        arbis_import, plot_path + 'cong_before_clean/', file_prefix, save_plot, show_plot)

    ################
    ### Cleaning ###
    ################

    arbis_import = arbis_import.drop(arbis_import[arbis_import['SpatMax'] > 50000].index)
    arbis_import['TempDist'].loc[arbis_import['TempDist'].isin([0])] = None
    arbis_import['SpatDist'].loc[arbis_import['SpatDist'].isin([0])] = None

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
        arbis_import, plot_path + 'cong_after_clean/', file_prefix, save_plot, show_plot)

    ##################
    ### Histograms ###
    ##################

    # Plot histogram of roadworks over time / months
    plt.figure(figsize=set_size(418, 1.8))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Histogram of roadwork per month, with at least one adjacent congestion')
    plt.ylabel('Count')
    plt.xlabel('Month of 2019')
    sns.countplot(x='Month', data=arbis_import, palette='Spectral', order=months)
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_hist_month.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Remove month column
    # arbis_selected.drop('Month', axis='columns', inplace=True)

    # Plot histogram of accidents over highway
    plt.figure(figsize=set_size(418, 1.8))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Histogram of roadwork per highway, with at least one adjacent congestion')
    plt.ylabel('Count')
    plt.xlabel('Highway')
    sns.countplot(x='Strasse', data=arbis_import, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_hist_highway.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    #####################
    ### Distributions ###
    #####################

    plot_arbis_dist([
        'Length',
        'Duration'],
        arbis_import, plot_path, file_prefix, save_plot, show_plot)

    ##############
    ### Counts ###
    ##############

    scale = 1.0
    (width, height) = set_size(418, scale)
    fig, axs = plt.subplots(3, 1, figsize=(width, 3 * height))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    sns.countplot(ax=axs[0], x='AnzGesperrtFs', data=arbis_import, palette='Spectral')
    sns.countplot(ax=axs[1], x='Einzug', data=arbis_import, palette='Spectral')
    sns.countplot(ax=axs[2], x='Richtung', data=arbis_import, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_multiple01.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

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
        report = ProfileReport(arbis_import, title='ArbIS Matched Dataset Report')
        report.to_file(work_path + file_prefix + '_report.html')

    ###################
    ### Correlation ###
    ###################

    # define column types
    nominal_columns = ['Str',
                       'Month']
    dichotomous_columns = ['Richtung']
    ordinal_columns = ['AnzGesperrtFs', 'Einzug']

    # Encode non numerical columns
    arbis_encoded, arbis_encoded_dict = numerical_encoding(arbis_import,
                                                           ["Strasse",
                                                            'Month'],
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
