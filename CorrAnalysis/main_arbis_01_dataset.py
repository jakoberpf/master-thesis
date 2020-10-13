#  Copyright (c) 2020. Jakob Erpf
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of
#  the Software.
#
#  THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from func_correlation import numerical_encoding, compute_correlations, plot_correlations
from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    safe_plots = True

    data_path = 'data/'
    work_path = data_path + 'ArbIS/dataset/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    work_file = 'ArbIS_2019.csv'

    arbis_imported = pd.read_csv(work_path + work_file, sep=';', decimal=',', parse_dates=True, date_parser=date_parser)

    arbis_selected = arbis_imported[
        [
            # Roadwork Data
            # 'Von', 'Bis',  # Not correlate able
            'Strasse',
            'AnzGesperrtFs',
            'Einzug',
            # 'VonKilometer', # Not correlate able
            # 'BisKilometer', # Not correlate able
            'Richtung',
            # 'VonKilometerBlock', # Not correlate able
            # 'BisKilometerBlock', # Not correlate able
            # 'VonStation', 'BisStation', # Not correlate able
            # 'VonAbschnitt', 'BisAbschnitt', # Not correlate able
            # 'SperrungID', 'StreckeID' # Not correlate able
            # 'StreckeID'
        ]].copy()

    # Manual data type conversion from str to datetime64
    arbis_imported['Von'] = pd.to_datetime(arbis_imported['Von'], format='%Y-%m-%d %H:%M:%S')
    arbis_imported['Bis'] = pd.to_datetime(arbis_imported['Bis'], format='%Y-%m-%d %H:%M:%S')

    # Manual data type conversion str to float64
    # arbis_import['VonKilometer'] = arbis_import['VonKilometer'].replace(',', '.', regex=True).astype(float)
    # arbis_import['BisKilometer'] = arbis_import['BisKilometer'].replace(',', '.', regex=True).astype(float)

    # Manual data type conversion str to float64
    # arbis_import['VonKilometer'] = arbis_import['VonKilometer'].replace(',', '.', regex=True).astype(float)

    # Add month of roadwork
    arbis_selected['Month'] = arbis_imported['Von'].dt.month_name()

    # Plot histogram of roadworks over time / months
    plt.figure(figsize=(13, 6))
    plt.hist(arbis_selected['Month'], color='blue', edgecolor='black')
    plt.title('Histogram of roadworks per month')
    plt.ylabel('Count')
    plt.xlabel('Month of 2019')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_hist_month.png')
    plt.show()

    # Add length of roadwork fragment in kilometers
    arbis_selected['Length'] = abs((arbis_imported['VonKilometer'] - arbis_imported['BisKilometer']))
    # Add duration of roadwork fragment in minutes
    arbis_selected['Duration'] = abs((arbis_imported['Von'] - arbis_imported['Bis'])).dt.total_seconds() / 60

    sns.set(font_scale=2)
    sns.set_context('paper')
    plt.figure(figsize=(11, 6))

    sns.boxplot(x='Strasse', y='Length', data=arbis_selected, palette='Set1')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_box_street2length.png')

    sns.boxplot(x='Strasse', y='Duration', data=arbis_selected, palette='Set1')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_box_stree2duration.png')

    sns.boxplot(x='AnzGesperrtFs', y='Length', data=arbis_selected, palette='Set1')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_box_agfs2length.png')

    sns.boxplot(x='AnzGesperrtFs', y='Duration', data=arbis_selected, palette='Set1')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_box_agfs2duration.png')

    sns.boxplot(x='Einzug', y='Length', data=arbis_selected, palette='Set1')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_box_einzug2length.png')

    sns.boxplot(x='Einzug', y='Duration', data=arbis_selected, palette='Set1')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_box_einzug2duration.png')

    sns.boxplot(x='Richtung', y='Length', data=arbis_selected, palette='Set1')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_box_direction2length.png')

    sns.boxplot(x='Richtung', y='Duration', data=arbis_selected, palette='Set1')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_box_direction2duration.png')

    # Print matrix for debugging
    print(arbis_selected.dtypes)
    print(arbis_selected)

    # defines column types
    nominal_columns = ['Strasse', 'StreckeID', 'Month']
    dichotomous_columns = ['Richtung']
    ordinal_columns = ['AnzGesperrtFs', 'Einzug']

    # Encode non numerical columns
    arbis_encoded = numerical_encoding(arbis_selected, nominal_columns, drop_single_label=False)

    # Calculate with Cramer's V is chosen

    corr, sign, coef, columns, nominal_columns, dichotomous_columns, ordinal_columns, inf_nan, single_value_columns = compute_correlations(
        arbis_encoded,
        nominal_columns=nominal_columns, dichotomous_columns=dichotomous_columns, ordinal_columns=ordinal_columns,
        bias_correction=False)

    plot_correlations(corr, columns, nominal_columns, dichotomous_columns, ordinal_columns, inf_nan,
                      single_value_columns, save=True, filepath=plot_path + 'arbis_dataset_corr_cramers.png',
                      show=True, figsize=(18, 15))

    test = sign.to_latex(float_format="{:0.2f}".format)

    with open(tex_path + 'arbis_dataset_sign_cramers.tex', 'w') as tf:
        tf.write(sign.to_latex(float_format="{:0.2f}".format))

    with open(tex_path + 'arbis_dataset_coef_cramers.tex', 'w') as tf:
        tf.write(coef.to_latex(float_format="{:0.2f}".format))

    # Calculate with Theil's U
    # associations(arbis_encoded, figsize=(18, 15),
    #              nominal_columns=['Strasse', 'Richtung', 'StreckeID', 'Month'],
    #              plot=False, bias_correction=False)
    # if safe_plots:
    #     plt.savefig(plot_path + 'arbis_dataset_corr_theils.png')
    # plt.show()



    print('Finished ArbIS Dataset Analysis')
