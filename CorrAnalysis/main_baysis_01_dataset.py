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
from func_plot import plot_correlation
from func_utils import print_welcome, date_parser

if __name__ == '__main__':
    print_welcome()

    safe_plots = True
    show_plot = True

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
    if safe_plots:
        plt.savefig(plot_path + 'baysis_dataset_hist_month.png')
    if show_plot:
        plt.show()

    # Remove month column
    # baysis_selected.drop('Month', axis='columns', inplace=True)

    # Plot histogram of accidents over highway
    plt.figure(figsize=(13, 6))
    plt.hist(baysis_selected['Strasse'], color='blue', edgecolor='black')
    plt.title('Histogram of accidents per highways')
    plt.ylabel('Count')
    plt.xlabel('Highway')
    if safe_plots:
        plt.savefig(plot_path + 'baysis_dataset_hist_highway.png')
    if show_plot:
        plt.show()

    # Settings for box plots
    sns.set(font_scale=2)
    sns.set_context('paper')
    plt.figure(figsize=(11, 6))

    sns.boxplot(x='Strasse', y='Kat', data=baysis_selected, palette='Set1')
    if safe_plots:
        plt.savefig(plot_path + 'baysis_dataset_box_street2kat.png')
    if show_plot:
        plt.show()

    # defines column types
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

    # Print matrix for debugging
    print(baysis_selected.dtypes)
    print(baysis_selected)

    # Encode non numerical columns
    baysis_encoded = numerical_encoding(baysis_selected, nominal_columns, drop_single_label=False)

    # Print matrix for debugging
    print(baysis_encoded.dtypes)
    print(baysis_encoded)

    # defines coefficients
    con_nominal = 'kruskal-wallis'
    con_dichotomous = 'point_biserial'
    con_ordinal = 'kendall'

    # Calculate with Cramers 's V
    corr, sign, coef, columns, nominal_columns, dichotomous_columns, ordinal_columns, inf_nan, single_value_columns = \
        compute_correlations(
            baysis_encoded,
            continuous_nominal=con_nominal, continuous_dichotomous=con_dichotomous, continuous_ordinal=con_ordinal,
            nominal_columns=nominal_columns, dichotomous_columns=dichotomous_columns, ordinal_columns=ordinal_columns,
            bias_correction=False)

    plot_correlation(corr, columns, nominal_columns, dichotomous_columns, ordinal_columns, inf_nan,
                     single_value_columns, save=True, filepath=plot_path + 'baysis_dataset_corr_cramers.png',
                     show=True, figsize=(18, 15))

    with open(tex_path + 'baysis_dataset_sign_cramers.tex', 'w') as tf:
        tf.write(sign.to_latex(float_format="{:0.2f}".format))

    with open(tex_path + 'baysis_dataset_coef_cramers.tex', 'w') as tf:
        tf.write(coef.to_latex(float_format="{:0.2f}".format))

    # Calculate with Theil's U
    corr, sign, coef, columns, nominal_columns, dichotomous_columns, ordinal_columns, inf_nan, single_value_columns = \
        compute_correlations(
            baysis_encoded,
            categorical_categorical='theils_u',
            continuous_nominal=con_nominal, continuous_dichotomous=con_dichotomous, continuous_ordinal=con_ordinal,
            nominal_columns=nominal_columns, dichotomous_columns=dichotomous_columns, ordinal_columns=ordinal_columns,
            bias_correction=False)

    plot_correlation(corr, columns, nominal_columns, dichotomous_columns, ordinal_columns, inf_nan,
                     single_value_columns, save=True, filepath=plot_path + 'baysis_dataset_corr_theils.png',
                     show=True, figsize=(18, 15))

    with open(tex_path + 'baysis_dataset_sign_theils.tex', 'w') as tf:
        tf.write(sign.to_latex(float_format="{:0.2f}".format))

    with open(tex_path + 'baysis_dataset_coef_theils.tex', 'w') as tf:
        tf.write(coef.to_latex(float_format="{:0.2f}".format))

    print('Finished BAYSIS Dataset Analysis')
