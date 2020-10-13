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
    work_file = 'ArbIS_2019.csv'

    arbis_import = pd.read_csv(work_path + work_file, sep=';', decimal=',', parse_dates=True, date_parser=date_parser)

    arbis_select_relevant = arbis_import[
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
    arbis_import['Von'] = pd.to_datetime(arbis_import['Von'], format='%Y-%m-%d %H:%M:%S')
    arbis_import['Bis'] = pd.to_datetime(arbis_import['Bis'], format='%Y-%m-%d %H:%M:%S')

    # Manual data type conversion str to float64
    # arbis_import['VonKilometer'] = arbis_import['VonKilometer'].replace(',', '.', regex=True).astype(float)
    # arbis_import['BisKilometer'] = arbis_import['BisKilometer'].replace(',', '.', regex=True).astype(float)

    # Manual data type conversion str to float64
    # arbis_import['VonKilometer'] = arbis_import['VonKilometer'].replace(',', '.', regex=True).astype(float)

    # Add month of roadwork
    arbis_select_relevant['Month'] = arbis_import['Von'].dt.month_name()

    # Plot histogram of roadworks over time / months
    plt.figure(figsize=(13, 6))
    plt.hist(arbis_select_relevant['Month'], color='blue', edgecolor='black')
    plt.title('Histogram of roadworks per month')
    plt.ylabel('Count')
    plt.xlabel('Month of 2019')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_hist_month.png')
    plt.show()

    # Add length of roadwork fragment in kilometers
    arbis_select_relevant['Length'] = abs((arbis_import['VonKilometer'] - arbis_import['BisKilometer']))
    # Add duration of roadwork fragment in minutes
    arbis_select_relevant['Duration'] = abs((arbis_import['Von'] - arbis_import['Bis'])).dt.total_seconds() / 60

    # Print matrix for debugging
    print(arbis_select_relevant.dtypes)
    print(arbis_select_relevant)

    nominal_columns = ['Strasse', 'StreckeID', 'Month']
    dichotomous_columns = ['Richtung']
    ordinal_columns = ['AnzGesperrtFs']

    # Plot association matrix
    # Calculate without Theil's U -> Cramer's V is chosen
    arbis_encoded = numerical_encoding(arbis_select_relevant, nominal_columns, drop_single_label=False)

    corr, sign, columns, nominal_columns, dichotomous_columns, ordinal_columns, inf_nan, single_value_columns = compute_correlations(
        arbis_encoded,
        nominal_columns=nominal_columns, dichotomous_columns=dichotomous_columns, ordinal_columns=ordinal_columns,
        bias_correction=False)

    plot_correlations(corr, columns, nominal_columns, dichotomous_columns, ordinal_columns, inf_nan,
                      single_value_columns, save=True, filepath=plot_path + 'arbis_dataset_corr_cramers.png',
                      show=True, figsize=(18, 15))

    print(sign.to_latex())

    with open(plot_path + 'arbis_dataset_sign_cramers.tex', 'w') as tf:
        tf.write(sign.to_latex(float_format="{:0.2f}".format))

    # Calculate with Theil's U
    # associations(arbis_encoded, figsize=(18, 15),
    #              nominal_columns=['Strasse', 'Richtung', 'StreckeID', 'Month'],
    #              plot=False, bias_correction=False)
    # if safe_plots:
    #     plt.savefig(plot_path + 'arbis_dataset_corr_theils.png')
    # plt.show()

    plt.figure(figsize=(11, 6))
    sns.set_context('paper', font_scale=1.0)
    sns.boxplot(x='Strasse', y='Length', data=arbis_select_relevant, palette='Set1')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_box_street2length.png')
    plt.show()

    plt.figure(figsize=(11, 6))
    sns.set_context('paper', font_scale=1.0)
    sns.boxplot(x='Strasse', y='Duration', data=arbis_select_relevant, palette='Set1')
    if safe_plots:
        plt.savefig(plot_path + 'arbis_dataset_box_stree2duration.png')
    plt.show()

    print('Finished ArbIS Dataset Analysis')
