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
from func_plot import plot_correlation, plot_statistic, set_size, tex_fonts, \
    plot_congestion_dist, plot_arbis_dist, plot_congestion_scatter
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

    arbis_imported = pd.read_csv(work_path + work_file, sep=';', decimal=',', parse_dates=True, date_parser=date_parser)

    arbis_matched = arbis_imported[
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
    arbis_imported['Von'] = pd.to_datetime(arbis_imported['Von'], format='%Y-%m-%d %H:%M:%S')
    arbis_imported['Bis'] = pd.to_datetime(arbis_imported['Bis'], format='%Y-%m-%d %H:%M:%S')

    # Manual data type conversion from str to int64
    arbis_matched["TLCar"] = pd.to_numeric(arbis_matched["TLCar"])
    arbis_matched["TLHGV"] = pd.to_numeric(arbis_matched["TLHGV"])
    arbis_matched["TLCar"] = arbis_matched["TLCar"].astype('int64')
    arbis_matched["TLHGV"] = arbis_matched["TLHGV"].astype('int64')

    # Add month of roadwork
    arbis_matched['Month'] = arbis_imported['Von'].dt.strftime('%b')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    ##############
    ### Report ###
    ##############

    if generate_report:
        report = ProfileReport(arbis_matched, title='ArbIS Matched Dataset Report')
        report.to_file(work_path + file_prefix + '_report.html')

    ##################
    ### Congestion ###
    ##################

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
        arbis_matched, plot_path, file_prefix, save_plot, show_plot)

    plot_congestion_scatter(
        ["TempMax"],
        ["SpatMax"],
        arbis_matched, plot_path, file_prefix, save_plot, show_plot)

    plot_congestion_scatter(
        ["TempAvg"],
        ["SpatAvg"],
        arbis_matched, plot_path, file_prefix, save_plot, show_plot)

    plot_congestion_scatter(
        ["TempDist"],
        ["SpatDist"],
        arbis_matched, plot_path, file_prefix, save_plot, show_plot)

    plot_congestion_scatter(
        ["TLCar"],
        ["TLHGV"],
        arbis_matched, plot_path, file_prefix, save_plot, show_plot)

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
    sns.countplot(x='Month', data=arbis_matched, palette='Spectral', order=months)
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
    sns.countplot(x='Strasse', data=arbis_matched, palette='Spectral')
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
        arbis_matched, plot_path, file_prefix, save_plot, show_plot)

    ##############
    ### Counts ###
    ##############

    scale = 1.0
    (width, height) = set_size(418, scale)
    fig, axs = plt.subplots(3, 1, figsize=(width, 3 * height))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    sns.countplot(ax=axs[0], x='AnzGesperrtFs', data=arbis_matched, palette='Spectral')
    sns.countplot(ax=axs[1], x='Einzug', data=arbis_matched, palette='Spectral')
    sns.countplot(ax=axs[2], x='Richtung', data=arbis_matched, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_multiple01.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    # # Plot distribution of AnzGesperrtFs
    # plt.figure(figsize=set_size(418))
    # plt.style.use('seaborn')
    # plt.rcParams.update(tex_fonts)
    # plt.title('Distribution of AnzGesperrtFs')
    # plt.ylabel('Count')
    # plt.xlabel('AnzGesperrtFs')
    # sns.countplot(x='AnzGesperrtFs', data=arbis_matched, palette='Spectral')
    # if save_plot:
    #     plt.savefig(plot_path + file_prefix + '_dist_AnzGesperrtFs.pdf')
    #     if not show_plot:
    #         plt.close()
    # if show_plot:
    #     plt.show()
    # else:
    #     plt.close()
    #
    # # Plot distribution of Einzug
    # plt.figure(figsize=set_size(418))
    # plt.style.use('seaborn')
    # plt.rcParams.update(tex_fonts)
    # plt.title('Distribution of Einzug')
    # plt.ylabel('Count')
    # plt.xlabel('Einzug')
    # sns.countplot(x='Einzug', data=arbis_matched, palette='Spectral')
    # if save_plot:
    #     plt.savefig(plot_path + file_prefix + '_dist_Einzug.pdf')
    #     if not show_plot:
    #         plt.close()
    # if show_plot:
    #     plt.show()
    # else:
    #     plt.close()
    #
    # # Plot distribution of Richtung
    # plt.figure(figsize=set_size(418, 0.8))
    # plt.style.use('seaborn')
    # plt.rcParams.update(tex_fonts)
    # plt.title('Distribution of Richtung')
    # plt.ylabel('Count')
    # plt.xlabel('Richtung')
    # sns.countplot(x='Richtung', data=arbis_matched, palette='Spectral')
    # if save_plot:
    #     plt.savefig(plot_path + file_prefix + '_dist_Richtung.pdf')
    #     if not show_plot:
    #         plt.close()
    # if show_plot:
    #     plt.show()
    # else:
    #     plt.close()

    ###############
    ### Scatter ###
    ###############

    # Congestion -> Roadwork
    for atr in ['AnzGesperrtFs', 'Einzug', 'Length', 'Duration']:
        plt.figure(figsize=set_size(418, 0.8))
        plt.style.use('seaborn')
        plt.rcParams.update(tex_fonts)
        plt.title('Scatterplot of ' + atr)
        arbis_matched.plot.scatter(x='TempMax', y='SpatMax', c=atr, colormap='viridis')
        if save_plot:
            plt.savefig(plot_path + file_prefix + '_scatter_E_' + atr + '.pdf')
            if not show_plot:
                plt.close()
        if show_plot:
            plt.show()
        else:
            plt.close()

    # Congestion -> Roadwork
    for atr in ['AnzGesperrtFs', 'Einzug', 'Length', 'Duration']:
        plt.figure(figsize=set_size(418, 0.8))
        plt.style.use('seaborn')
        plt.rcParams.update(tex_fonts)
        plt.title('Scatterplot of ' + atr)
        arbis_matched.plot.scatter(x='TempAvg', y='SpatAvg', c=atr, colormap='viridis')
        if save_plot:
            plt.savefig(plot_path + file_prefix + '_scatter_E_' + atr + '.pdf')
            if not show_plot:
                plt.close()
        if show_plot:
            plt.show()
        else:
            plt.close()

    # Congestion -> Roadwork
    for atr in ['AnzGesperrtFs', 'Einzug', 'Length', 'Duration']:
        plt.figure(figsize=set_size(418, 0.8))
        plt.style.use('seaborn')
        plt.rcParams.update(tex_fonts)
        plt.title('Scatterplot of ' + atr)
        arbis_matched.plot.scatter(x='TempDist', y='SpatDist', c=atr, colormap='viridis')
        if save_plot:
            plt.savefig(plot_path + file_prefix + '_scatter_D_' + atr + '.pdf')
            if not show_plot:
                plt.close()
        if show_plot:
            plt.show()
        else:
            plt.close()

    # Roadwork -> Congestion
    for atr in ['TempMax', 'SpatMax', 'TempAvg', 'SpatAvg', 'TLCar', 'TLHGV']:
        plt.figure(figsize=set_size(418, 0.8))
        plt.style.use('seaborn')
        plt.rcParams.update(tex_fonts)
        plt.title('Scatterplot of ' + atr)
        arbis_matched.plot.scatter(x='Length', y='Duration', c=atr, colormap='viridis')
        if save_plot:
            plt.savefig(plot_path + file_prefix + '_scatter_' + atr + '.pdf')
            if not show_plot:
                plt.close()
        if show_plot:
            plt.show()
        else:
            plt.close()

    ###########
    ### Box ###
    ###########

    ###################
    ### Correlation ###
    ###################

    # define column types
    nominal_columns = ['Strasse',
                       'StreckeID',
                       'Month']
    dichotomous_columns = ['Richtung']
    ordinal_columns = ['AnzGesperrtFs', 'Einzug']

    # Encode non numerical columns
    arbis_encoded, arbis_encoded_dict = numerical_encoding(arbis_matched,
                                                           ["Strasse",
                                                            'StreckeID',
                                                            'Month'],
                                                           drop_single_label=False,
                                                           drop_fact_dict=False)
    arbis_encoded.to_csv(csv_path + 'encoded.csv', index=False, sep=';')

    with open(csv_path + 'encoded_dict.csv', 'w') as tf:
        for key in arbis_encoded_dict.keys():
            tf.write("%s, %s\n" % (key, arbis_encoded_dict[key]))

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

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + file_prefix + '_sign_cramers.pdf',
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

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + file_prefix + '_sign_theils.pdf',
                   show=show_plot, figsize=(18, 15))

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + file_prefix + '_corr_theils.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + file_prefix + '_sign_theils.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex(float_format="{:0.3f}".format))

    with open(tex_path + file_prefix + '_coef_theils.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex(escape=False))

    print('Finished ArbIS Dataset Analysis')
