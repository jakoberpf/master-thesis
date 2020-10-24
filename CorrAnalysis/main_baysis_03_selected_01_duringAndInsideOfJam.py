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
    plot_congestion_dist, plot_congestion_scatter
from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    generate_report = True

    data_path = 'data/'
    work_path = data_path + 'BAYSIS/03_selected_01_duringAndInsideOfJam/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    csv_path = work_path + 'csv/'

    work_file = 'BAYSIS_2019.csv'

    file_prefix = 'baysis_matched'
    file_plot_type = '.pdf'

    baysis_imported = pd.read_csv(data_path + 'BAYSIS/02_matched/' + work_file, sep=';', decimal=',', parse_dates=True,
                                  date_parser=date_parser)

    baysis_matched = baysis_imported[
        [
            # Congestion Data
            "TempExMax",
            # "TempExMin", # Not implemented
            "SpatExMax",
            # "SpatExMin", # Not implemented
            "TempDist",
            "SpatDist",
            "Coverage",
            #  * The temporal reference of if the incident to the congestion. The incident...
            #  * [-1] = Not Set
            #  * [1] = is before
            #  * [2] = is after
            #  * [3] = is during
            #  * [4] = is overlapping before
            #  * [5] = is overlapping after
            "temporalGlobalLoc",
            #  * The spatial reference of if the incident to the congestion. The incident...
            #  * [0] = is before or after
            #  * [1] = is during
            "spatialGlobalLoc",
            #  * The temporal reference of if the incident is during the congestion. The incident is within...
            #  * [-1] = Not Set in case not during or overlapping
            #  * [1] = 10% to Beginning
            #  * [2] = 10% - 30% to Beginning
            #  * [3] = 30% - 70% (Middle)
            #  * [4] = 30% - 10% to Ending
            #  * [5] = 10% to Ending
            "temporalInternalLoc",
            #  * The spatial reference of if the incident is during the congestion. The incident is within...
            #  * [-1] = Not Set in case not during or overlapping
            #  * [1] = 10% to Beginning
            #  * [2] = 10% - 30% to Beginning
            #  * [3] = 30% - 70% (Middle)
            #  * [4] = 30% - 10% to Ending
            #  * [5] = 10% to Ending
            "spatialInternalLoc",
            "TimeLossCar",
            "TimeLossHGV",
            # Accident Data
            "Strasse",
            "Kat", "Typ", "Betei",
            "UArt1", "UArt2",
            "AUrs1", "AUrs2",
            "AufHi",
            "Alkoh",
            "Char1", "Char2",
            # "Char3",  # Not relevant because empty
            "Bes1", "Bes2",
            # "Bes3",  # Not relevant because empty
            "Lich1", "Lich2",
            "Zust1", "Zust2",
            "Fstf",
            "StrklVu",
            # "WoTagNr",  # Already represented by WoTag
            "WoTag",
            "FeiTag"]].copy()

    # Manual data type conversion from str to datetime64
    baysis_imported['Date'] = pd.to_datetime(baysis_imported['Date'], format='%Y-%m-%d')

    # Manual data type conversion from str to int64
    baysis_matched["TimeLossCar"] = pd.to_numeric(baysis_matched["TimeLossCar"])
    baysis_matched["TimeLossHGV"] = pd.to_numeric(baysis_matched["TimeLossHGV"])
    baysis_matched["TimeLossCar"] = baysis_matched["TimeLossCar"].astype('int64')
    baysis_matched["TimeLossHGV"] = baysis_matched["TimeLossHGV"].astype('int64')

    # Add month of roadwork
    baysis_matched['Month'] = baysis_imported['Date'].dt.strftime('%b')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Correcting the column WoTag
    days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']

    #################
    ### Selection ###
    #################

    baysis_selected = baysis_matched.loc[
        (baysis_matched["spatialGlobalLoc"] == 0) & (baysis_matched["temporalGlobalLoc"] == 3)]

    ##################
    ### Congestion ###
    ##################

    plot_congestion_dist([
        "TempExMax",
        "SpatExMax",
        "TempDist",
        "SpatDist",
        "Coverage",
        "TimeLossCar",
        "TimeLossHGV"],
        baysis_selected, plot_path, file_prefix, save_plot, show_plot)

    plot_congestion_scatter(
        ["TempExMax"],
        ["SpatExMax"],
        baysis_selected, plot_path, file_prefix, save_plot, show_plot)

    plot_congestion_scatter(
        ["TempDist"],
        ["SpatDist"],
        baysis_selected, plot_path, file_prefix, save_plot, show_plot)

    plot_congestion_scatter(
        ["TimeLossCar"],
        ["TimeLossHGV"],
        baysis_selected, plot_path, file_prefix, save_plot, show_plot)

    locators = ["temporalGlobalLoc",
                "spatialGlobalLoc",
                "temporalInternalLoc",
                "spatialInternalLoc"]

    for atr in locators:
        plt.figure(figsize=set_size(418, 0.8))
        plt.style.use('seaborn')
        plt.rcParams.update(tex_fonts)
        plt.title('Distribution of ' + atr)
        plt.ylabel('Count')
        baysis_selected.plot.scatter(x='TempExMax', y='SpatExMax', c=atr, colormap='viridis')
        plt.xlabel(atr)
        if save_plot:
            plt.savefig(plot_path + file_prefix + '_scatter_E_' + atr + '.pdf')
            if not show_plot:
                plt.close()
        if show_plot:
            plt.show()
        else:
            plt.close()

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

    for atr in ['Typ', 'Kat', 'Betei', 'AufHi', 'Alkoh', 'Fstf', 'StrklVu', 'FeiTag']:
        plt.figure(figsize=set_size(418, 1.0))
        plt.style.use('seaborn')
        plt.rcParams.update(tex_fonts)
        plt.title('Counts of ' + atr)
        plt.ylabel('Count')
        plt.xlabel(atr)
        sns.countplot(x=atr, data=baysis_selected, palette='Spectral')
        if save_plot:
            plt.savefig(plot_path + file_prefix + '_count_' + atr + '.pdf')
            if not show_plot:
                plt.close()
        if show_plot:
            plt.show()
        else:
            plt.close()

    # Plot Counts of WoTag
    atr = 'WoTag'
    plt.figure(figsize=set_size(418, 1.0))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Counts of ' + atr)
    plt.ylabel('Count')
    plt.xlabel(atr)
    ax = sns.countplot(x=atr, data=baysis_selected, palette='Spectral')
    plt.xticks(range(0, 7), ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'])
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_' + atr + '.pdf')
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Plot Counts of UArt
    atr = 'UArt'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    plt.figure(figsize=set_size(418, 1.0))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Counts of UArt')
    plt.ylabel('Count')
    ax = sns.countplot(x=atr, data=concat, palette='Spectral')
    plt.xlabel(atr)
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_' + atr + '.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Plot Counts of AUrs
    atr = 'AUrs'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    plt.figure(figsize=set_size(418, 1.0))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Counts of UArt')
    plt.ylabel('Count')
    ax = sns.countplot(x=atr, data=concat, palette='Spectral')
    plt.xlabel(atr)
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_' + atr + '.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Plot Counts of Char
    atr = 'Char'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    plt.figure(figsize=set_size(418, 1.0))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Counts of UArt')
    plt.ylabel('Count')
    ax = sns.countplot(x=atr, data=concat, palette='Spectral')
    plt.xlabel(atr)
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_' + atr + '.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Plot Counts of Bes
    atr = 'Bes'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    plt.figure(figsize=set_size(418, 1.0))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Counts of UArt')
    plt.ylabel('Count')
    ax = sns.countplot(x=atr, data=concat, palette='Spectral')
    plt.xlabel(atr)
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_' + atr + '.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Plot Counts of Lich
    atr = 'Lich'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    plt.figure(figsize=set_size(418, 1.0))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Counts of UArt')
    plt.ylabel('Count')
    ax = sns.countplot(x=atr, data=concat, palette='Spectral')
    plt.xlabel(atr)
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_' + atr + '.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Plot Counts of Zust
    atr = 'Zust'
    concat = pd.concat([baysis_selected[atr + '1'], baysis_selected[atr + '2']], keys=[atr])
    plt.figure(figsize=set_size(418, 1.0))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Counts of UArt')
    plt.ylabel('Count')
    ax = sns.countplot(x=atr, data=concat, palette='Spectral')
    plt.xlabel(atr)
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_count_' + atr + '.pdf')
        if not show_plot:
            plt.close()
    if show_plot:
        plt.show()
    else:
        plt.close()

    ###############
    ### Scatter ###
    ###############

    attributes = [
        # "Strasse", # TODO fix handling of non number sequences in scatter plots
        "Kat", "Typ", "Betei",
        "UArt1", "UArt2",
        "AUrs1", "AUrs2",
        "AufHi",
        "Alkoh",
        "Char1", "Char2",
        # "Char3",  # Not relevant because empty
        "Bes1", "Bes2",
        # "Bes3",  # Not relevant because empty
        "Lich1", "Lich2",
        "Zust1", "Zust2",
        # "Fstf", # TODO fix handling of non number sequences in scatter plots
        # "StrklVu",  # TODO fix handling of non number sequences in scatter plots
        # "WoTagNr",  # Already represented by WoTag
        "WoTag",
        "FeiTag"]

    # Congestion -> Accident
    for atr in attributes:
        plt.figure(figsize=set_size(418, 0.8))
        plt.style.use('seaborn')
        plt.rcParams.update(tex_fonts)
        plt.title('Distribution of ' + atr)
        plt.ylabel('Count')
        baysis_selected.plot.scatter(x='TempExMax', y='SpatExMax', c=atr, colormap='viridis')
        plt.xlabel(atr)
        if save_plot:
            plt.savefig(plot_path + file_prefix + '_scatter_' + atr + '.pdf')
            if not show_plot:
                plt.close()
        if show_plot:
            plt.show()
        else:
            plt.close()

    # Congestion -> Accident
    for atr in attributes:
        plt.figure(figsize=set_size(418, 0.8))
        plt.style.use('seaborn')
        plt.rcParams.update(tex_fonts)
        plt.title('Distribution of ' + atr)
        plt.ylabel('Count')
        baysis_selected.plot.scatter(x='TempDist', y='SpatDist', c=atr, colormap='viridis')
        plt.xlabel(atr)
        if save_plot:
            plt.savefig(plot_path + file_prefix + '_scatter_D_' + atr + '.pdf')
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
    ### Encoding ###
    ###################

    # define column types
    nominal_columns = ["Strasse", "Kat", "Typ",
                       "UArt1", "UArt2",
                       "AUrs1", "AUrs2",
                       "AufHi",
                       "Char1", "Char2",
                       "Bes1", "Bes2",
                       "Lich1", "Lich2",
                       "Zust1", "Zust2",
                       "StrklVu",
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

    ##############
    ### Report ###
    ##############

    if generate_report:
        report = ProfileReport(baysis_encoded, title='BAYSIS Selected Dataset Report')
        report.to_file(work_path + file_prefix + '_report.html')

    ###################
    ### Correlation ###
    ###################

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
        tf.write(results.get('significance').to_latex())

    with open(tex_path + file_prefix + '_coef_cramers.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex())

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
        tf.write(results.get('significance').to_latex())

    with open(tex_path + file_prefix + '_coef_theils.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex())

    ######################
    ### Scatter Matrix ###
    ######################

    # https://seaborn.pydata.org/examples/scatterplot_matrix.html
    # sns.set_theme(style='ticks')
    # sns.pairplot(baysis_selected, hue='Kat')
    # plt.show()

    print('Finished BAYSIS Matched Analysis')