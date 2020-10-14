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

import matplotlib.pyplot as plt
import pandas as pd

from func_correlation import numerical_encoding, compute_correlations
from func_plot import plot_correlation, plot_statistic, plot_boxplot
from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

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
    if save_plot:
        plt.savefig(plot_path + 'arbis_dataset_hist_month.png')
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Plot histogram of accidents over highway
    plt.figure(figsize=(13, 6))
    plt.hist(arbis_selected['Strasse'], color='blue', edgecolor='black')
    plt.title('Histogram of roadworks per highways')
    plt.ylabel('Count')
    plt.xlabel('Highway')
    if save_plot:
        plt.savefig(plot_path + 'baysis_dataset_hist_highway.png')
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Add length of roadwork fragment in kilometers
    arbis_selected['Length'] = abs((arbis_imported['VonKilometer'] - arbis_imported['BisKilometer']))
    # Add duration of roadwork fragment in minutes
    arbis_selected['Duration'] = abs((arbis_imported['Von'] - arbis_imported['Bis'])).dt.total_seconds() / 60

    # Plot boxplots for visual relation testing
    plot_boxplot(arbis_selected, 'Strasse', 'Length', save_plot, show_plot,
                 plot_path + 'arbis_dataset_box_street2length.png')

    plot_boxplot(arbis_selected, 'Strasse', 'Duration', save_plot, show_plot,
                 plot_path + 'arbis_dataset_box_street2duration.png')

    plot_boxplot(arbis_selected, 'AnzGesperrtFs', 'Length', save_plot, show_plot,
                 plot_path + 'arbis_dataset_box_agfs2length.png')

    plot_boxplot(arbis_selected, 'AnzGesperrtFs', 'Duration', save_plot, show_plot,
                 plot_path + 'arbis_dataset_box_agfs2duration.png')

    plot_boxplot(arbis_selected, 'Einzug', 'Length', save_plot, show_plot,
                 plot_path + 'arbis_dataset_box_einzug2length.png')

    plot_boxplot(arbis_selected, 'Einzug', 'Duration', save_plot, show_plot,
                 plot_path + 'arbis_dataset_box_einzug2duration.png')

    plot_boxplot(arbis_selected, 'Richtung', 'Length', save_plot, show_plot,
                 plot_path + 'arbis_dataset_box_direction2length.png')

    plot_boxplot(arbis_selected, 'Richtung', 'Duration', save_plot, show_plot,
                 plot_path + 'arbis_dataset_box_direction2duration.png')

    # define column types
    nominal_columns = ['Strasse', 'StreckeID', 'Month']
    dichotomous_columns = ['Richtung']
    ordinal_columns = ['AnzGesperrtFs', 'Einzug']

    # define coefficients
    con_nominal = 'kruskal-wallis'
    con_dichotomous = 'point_biserial'
    con_ordinal = 'kendall'

    # Encode non numerical columns
    arbis_encoded = numerical_encoding(arbis_selected, nominal_columns, drop_single_label=False)

    # Calculate with Cramers 's V
    results = None  # To make sure that no old data is reused
    results = compute_correlations(
        arbis_encoded,
        continuous_nominal=con_nominal, continuous_dichotomous=con_dichotomous, continuous_ordinal=con_ordinal,
        columns_nominal=nominal_columns, columns_dichotomous=dichotomous_columns, columns_ordinal=ordinal_columns,
        bias_correction=False)

    # Plot correlation matrix
    plot_correlation(results.get('correlation'), results.get('columns'),
                     nominal_columns, dichotomous_columns, ordinal_columns,
                     results.get('inf_nan_corr'),
                     results.get('columns_single_value'),
                     save=save_plot, filepath=plot_path + 'arbis_dataset_corr_cramers.png',
                     show=show_plot, figsize=(18, 15))

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + 'arbis_dataset_sign_cramers.png',
                   show=show_plot, figsize=(18, 15))

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + 'arbis_dataset_corr_cramers.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + 'arbis_dataset_sign_cramers.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex())

    with open(tex_path + 'arbis_dataset_coef_cramers.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex())

    # Calculate with Theil's U
    results = None  # To make sure that no old data is reused
    results = compute_correlations(
        arbis_encoded,
        categorical_categorical='theils_u',
        continuous_nominal=con_nominal, continuous_dichotomous=con_dichotomous, continuous_ordinal=con_ordinal,
        columns_nominal=nominal_columns, columns_dichotomous=dichotomous_columns, columns_ordinal=ordinal_columns,
        bias_correction=False)

    # Plot correlation matrix
    plot_correlation(results.get('correlation'), results.get('columns'),
                     nominal_columns, dichotomous_columns, ordinal_columns,
                     results.get('inf_nan_corr'),
                     results.get('columns_single_value'),
                     save=save_plot, filepath=plot_path + 'arbis_dataset_corr_theils.png',
                     show=show_plot, figsize=(18, 15))

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + 'arbis_dataset_sign_theils.png',
                   show=show_plot, figsize=(18, 15))

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + 'arbis_dataset_corr_theils.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + 'arbis_dataset_sign_theils.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex())

    with open(tex_path + 'arbis_dataset_coef_theils.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex())

    print('Finished ArbIS Dataset Analysis')
