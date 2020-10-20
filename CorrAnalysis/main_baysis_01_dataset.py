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
from pandas_profiling import ProfileReport
import seaborn as sns

from func_correlation import numerical_encoding, compute_correlations
from func_plot import plot_correlation, plot_statistic, tex_fonts, set_size
from func_utils import print_welcome, date_parser

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    generate_report = False

    data_path = 'data/'
    work_path = data_path + 'BAYSIS/01_dataset/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    csv_path = work_path + 'csv/'

    work_file = 'BAYSIS_2019.csv'

    file_prefix = 'baysis_dataset'
    file_plot_type = '.pdf'

    baysis_imported = pd.read_csv(work_path + work_file, sep=';', decimal=',', parse_dates=True,
                                  date_parser=date_parser)

    baysis_selected = baysis_imported[
        ["Strasse",
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
    baysis_imported['Date'] = pd.to_datetime(baysis_imported['Datum'], format='%d.%m.%y')

    # Add month of roadwork
    baysis_selected['Month'] = baysis_imported['Date'].dt.strftime('%b')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Removing errors in WoTag
    days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
    baysis_selected['WoTag'].loc[np.invert(baysis_selected['WoTag'].isin(days))] = np.nan

    ##################
    ### Report ###
    ##################

    if generate_report:
        report = ProfileReport(baysis_selected, title='BAYSIS Original Dataset Report')
        report.to_file(work_path + file_prefix + '_report.html')

    ##################
    ### Histograms ###
    ##################

    # Plot histogram of accidents over time / months
    plt.figure(figsize=set_size(418, 1.8))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Histogram of accidents per month')
    plt.ylabel('Count')
    plt.xlabel('Month of 2019')
    ax = sns.countplot(x='Month', data=baysis_selected, palette='Spectral', order=months)
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_hist_month.pdf')
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Remove month column
    # baysis_selected.drop('Month', axis='columns', inplace=True)

    # Plot histogram of accidents over highway
    plt.figure(figsize=set_size(418, 1.8))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Histogram of accidents per highways')
    plt.ylabel('Count')
    plt.xlabel('Highway')
    ax = sns.countplot(x='Strasse', data=baysis_selected, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_hist_highway.pdf')
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
    ax = sns.countplot(x=atr, data=baysis_selected, palette='Spectral',
                       order=['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'])
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
    if show_plot:
        plt.show()
    else:
        plt.close()

    ###################
    ### Correlation ###
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
                       "FeiTag", 'Month']
    dichotomous_columns = ["Alkoh"]
    ordinal_columns = ["Betei", "Fstf"]

    # Encode non numerical columns
    baysis_encoded, baysis_encoded_dict = numerical_encoding(baysis_selected,
                                                             ["Strasse", "Kat", "Typ",
                                                              "UArt1", "UArt2",
                                                              "AUrs1", "AUrs2",
                                                              "AufHi",
                                                              "Char1", "Char2",
                                                              "Bes1", "Bes2",
                                                              "Lich1", "Lich2",
                                                              "Zust1", "Zust2",
                                                              "StrklVu",
                                                              "Fstf"
                                                              "WoTag",
                                                              "FeiTag", 'Month'], drop_single_label=False,
                                                             drop_fact_dict=False)
    baysis_encoded.to_csv(csv_path + 'encoded.csv', index=False, sep=';')

    with open(csv_path + 'encoded_dict.csv', 'w') as tf:
        for key in baysis_encoded_dict.keys():
            tf.write("%s, %s\n" % (key, baysis_encoded_dict[key]))

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
                     show=show_plot, scale=4.0)

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + file_prefix + '_sign_cramers.pdf',
                   show=show_plot, scale=4.0)

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
                     show=show_plot, scale=4.0)

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + file_prefix + '_sign_theils.pdf',
                   show=show_plot, scale=4.0)

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + file_prefix + '_corr_theils.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + file_prefix + '_sign_theils.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex())

    with open(tex_path + file_prefix + '_coef_theils.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex())

    print('Finished BAYSIS Dataset Analysis')
