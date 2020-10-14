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
from func_plot import plot_correlation, plot_boxplot, plot_statistic
from func_utils import print_welcome, date_parser

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    data_path = 'data/'
    work_path = data_path + 'BAYSIS/dataset/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
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
         "Char3",  # Not relevant because empty
         "Bes1", "Bes2",
         "Bes3",  # Not relevant because empty
         "Lich1", "Lich2",
         "Zust1", "Zust2",
         "Fstf",
         "StrklVu",
         "WoTagNr",  # Already represented by WoTag
         # "WoTag",
         "FeiTag"]].copy()

    # Manual data type conversion from str to datetime64
    baysis_imported['Datum'] = pd.to_datetime(baysis_imported['Datum'], format='%d.%m.%y')

    # Add month of roadwork
    baysis_selected['Month'] = baysis_imported['Datum'].dt.month_name()

    # Plot histogram of accidents over time / months
    plt.figure(figsize=(13, 6))
    plt.hist(baysis_selected['Month'], color='blue', edgecolor='black')
    plt.title('Histogram of accidents per month')
    plt.ylabel('Count')
    plt.xlabel('Month of 2019')
    if save_plot:
        plt.savefig(plot_path + 'baysis_dataset_hist_month.png')
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Remove month column
    # baysis_selected.drop('Month', axis='columns', inplace=True)

    # Plot histogram of accidents over highway
    plt.figure(figsize=(13, 6))
    plt.hist(baysis_selected['Strasse'], color='blue', edgecolor='black')
    plt.title('Histogram of accidents per highways')
    plt.ylabel('Count')
    plt.xlabel('Highway')
    if save_plot:
        plt.savefig(plot_path + 'baysis_dataset_hist_highway.png')
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Plot boxplots for visual relation testing
    plot_boxplot(baysis_selected, 'Strasse', 'Kat', save_plot, show_plot,
                 plot_path + 'baysis_dataset_box_street2kat.png')

    plot_boxplot(baysis_selected, 'Strasse', 'Typ', save_plot, show_plot,
                 plot_path + 'baysis_dataset_box_street2typ.png')

    # define column types
    nominal_columns = ["Strasse", "Kat", "Typ",
                       "UArt1", "UArt2",
                       "AUrs1", "AUrs2",
                       "AufHi",
                       "Char1", "Char2",
                       "Char3",  # Not relevant because empty
                       "Bes1", "Bes2",
                       "Bes3",  # Not relevant because empty
                       "Lich1", "Lich2",
                       "Zust1", "Zust2",
                       "StrklVu",
                       "WoTagNr",  # Already represented by WoTag
                       "FeiTag", 'Month']
    dichotomous_columns = ["Alkoh"]
    ordinal_columns = ["Betei", "Fstf"]

    # defines coefficients
    con_nominal = 'kruskal-wallis'
    con_dichotomous = 'point_biserial'
    con_ordinal = 'kendall'

    # Encode non numerical columns
    baysis_encoded = numerical_encoding(baysis_selected, nominal_columns, drop_single_label=False)

    # Calculate with Cramers 's V
    results = None  # To make sure that no old data is reused
    results = compute_correlations(
        baysis_encoded,
        continuous_nominal=con_nominal, continuous_dichotomous=con_dichotomous, continuous_ordinal=con_ordinal,
        columns_nominal=nominal_columns, columns_dichotomous=dichotomous_columns, columns_ordinal=ordinal_columns,
        bias_correction=False)

    # Plot correlation matrix
    plot_correlation(results.get('correlation'), results.get('columns'),
                     nominal_columns, dichotomous_columns, ordinal_columns,
                     results.get('inf_nan_corr'),
                     results.get('columns_single_value'),
                     save=save_plot, filepath=plot_path + 'baysis_dataset_corr_cramers.png',
                     show=show_plot, figsize=(18, 15))

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + 'baysis_dataset_sign_cramers.png',
                   show=show_plot, figsize=(18, 15))

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
        categorical_categorical='theils_u',
        continuous_nominal=con_nominal, continuous_dichotomous=con_dichotomous, continuous_ordinal=con_ordinal,
        columns_nominal=nominal_columns, columns_dichotomous=dichotomous_columns, columns_ordinal=ordinal_columns,
        bias_correction=False)

    # Plot correlation matrix
    plot_correlation(results.get('correlation'), results.get('columns'),
                     nominal_columns, dichotomous_columns, ordinal_columns,
                     results.get('inf_nan_corr'),
                     results.get('columns_single_value'),
                     save=save_plot, filepath=plot_path + 'baysis_dataset_corr_theils.png',
                     show=show_plot, figsize=(18, 15))

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + 'baysis_dataset_sign_theils.png',
                   show=show_plot, figsize=(18, 15))

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + 'baysis_dataset_corr_theils.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + 'baysis_dataset_sign_theils.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex())

    with open(tex_path + 'baysis_dataset_coef_theils.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex())

    print('Finished BAYSIS Dataset Analysis')
