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

from func_correlation import numerical_encoding, compute_correlations
from func_plot import plot_correlation, plot_boxplot_logscale, plot_statistic, plot_boxplot, tex_fonts, set_size
from func_utils import print_welcome, date_parser

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    data_path = 'data/'
    work_path = data_path + 'BAYSIS/01_dataset/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    csv_path = work_path + 'csv/'
    work_file = 'BAYSIS_2019.csv'

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

    baysis_imported.drop(baysis_imported[(baysis_imported['WoTag'] != 'Mo')
                                         & (baysis_imported['WoTag'] != 'Di')
                                         & (baysis_imported['WoTag'] != 'Mi')
                                         & (baysis_imported['WoTag'] != 'Do')
                                         & (baysis_imported['WoTag'] != 'Fr')
                                         & (baysis_imported['WoTag'] != 'Sa')
                                         & (baysis_imported['WoTag'] != 'So')
                                         ].index)

    # Manual data type conversion from str to datetime64
    baysis_imported['Date'] = pd.to_datetime(baysis_imported['Datum'], format='%d.%m.%y')

    # Add month of roadwork
    baysis_selected['Month'] = baysis_imported['Date'].dt.month_name()
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    # TODO https://stackoverflow.com/questions/33179122/seaborn-countplot-with-frequencies

    # Plot histogram of accidents over time / months
    plt.figure(figsize=set_size(418, 1.8))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Histogram of accidents per month')
    plt.ylabel('Count')
    plt.xlabel('Month of 2019')
    # https://seaborn.pydata.org/generated/seaborn.countplot.html
    ax = sns.countplot(x='Month', data=baysis_selected, palette='Spectral', order=months)
    if save_plot:
        plt.savefig(plot_path + 'baysis_dataset_hist_month.pdf')
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
    plt.title(r'Histogram of accidents per highways')
    plt.ylabel(r'Count')
    plt.xlabel(r'Highway')
    # https://seaborn.pydata.org/generated/seaborn.countplot.html
    ax = sns.countplot(x='Strasse', data=baysis_selected, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + 'baysis_dataset_hist_highway.pdf')
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Plot distribution of Kat
    plt.figure(figsize=set_size(418, 1.0))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title(r'Distribution of Kat')
    plt.ylabel(r'Count')
    plt.xlabel(r'Kat')
    # https://seaborn.pydata.org/generated/seaborn.countplot.html
    ax = sns.countplot(x='Kat', data=baysis_selected, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + 'baysis_dataset_dist_Kat.pdf')
    if show_plot:
        plt.show()
    else:
        plt.close()

       # "Typ", "Betei",
       #  "UArt1", "UArt2",
       #  "AUrs1", "AUrs2",
       #  "AufHi",
       #  "Alkoh",
       #  "Char1", "Char2",
       #  # "Char3",  # Not relevant because empty
       #  "Bes1", "Bes2",
       #  # "Bes3",  # Not relevant because empty
       #  "Lich1", "Lich2",
       #  "Zust1", "Zust2",
       #  "Fstf",
       #  "StrklVu",
       #  # "WoTagNr",  # Already represented by WoTag
       #  "WoTag",
       #  "FeiTag"

    # TODO add more plot variations

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
                     save=save_plot, filepath=plot_path + 'baysis_dataset_corr_cramers.pdf',
                     show=show_plot, scale=4.0)

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + 'baysis_dataset_sign_cramers.pdf',
                   show=show_plot, scale=4.0)

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + 'baysis_dataset_corr_cramers.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + 'baysis_dataset_sign_cramers.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex())

    with open(tex_path + 'baysis_dataset_coef_cramers.tex', 'w') as tf:
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
                     save=save_plot, filepath=plot_path + 'baysis_dataset_corr_theils.pdf',
                     show=show_plot, scale=4.0)

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + 'baysis_dataset_sign_theils.pdf',
                   show=show_plot, scale=4.0)

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + 'baysis_dataset_corr_theils.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + 'baysis_dataset_sign_theils.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex())

    with open(tex_path + 'baysis_dataset_coef_theils.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex())

    # https://seaborn.pydata.org/examples/scatterplot_matrix.html
    # sns.set_theme(style='ticks')
    # sns.pairplot(baysis_selected, hue='Kat')
    # plt.show()

    print('Finished BAYSIS Dataset Analysis')
