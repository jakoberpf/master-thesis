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
import seaborn as sns
from pandas_profiling import ProfileReport

from func_correlation import numerical_encoding, compute_correlations
from func_plot import plot_correlation, plot_statistic, set_size, tex_fonts, \
    plot_arbis_dist
from func_utils import date_parser, print_welcome

if __name__ == '__main__':
    print_welcome()

    save_plot = True
    show_plot = False

    generate_report = False

    data_path = 'data/'
    work_path = data_path + 'ArbIS/01_dataset/'
    plot_path = work_path + 'plots/'
    tex_path = work_path + 'latex/'
    csv_path = work_path + 'csv/'

    work_file = 'ArbIS_2019.csv'

    file_prefix = 'arbis_dataset'
    file_plot_type = '.pdf'

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

    # Add length of roadwork fragment in kilometers
    arbis_selected['Length'] = abs((arbis_imported['VonKilometer'] - arbis_imported['BisKilometer']))
    # Add duration of roadwork fragment in minutes
    arbis_selected['Duration'] = abs((arbis_imported['Von'] - arbis_imported['Bis'])).dt.total_seconds() / 60

    # Add month of roadwork
    arbis_selected['Month'] = arbis_imported['Von'].dt.strftime('%b')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    ##################
    ### Report ###
    ##################

    if generate_report:
        report = ProfileReport(arbis_selected, title='ArbIS Original Dataset Report')
        report.to_file(work_path + file_prefix + '_report.html')

    ##################
    ### Histograms ###
    ##################

    # Plot histogram of roadworks over time / months
    plt.figure(figsize=set_size(418, 1.8))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title(r'Histogram of total roadworks per month')
    plt.ylabel('Count')
    plt.xlabel('Month of 2019')
    sns.countplot(x='Month', data=arbis_selected, palette='Spectral', order=months)
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_hist_month.pdf')
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
    plt.title('Histogram of total roadworks per highways')
    plt.ylabel('Count')
    plt.xlabel('Highway')
    sns.countplot(x='Strasse', data=arbis_selected, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_hist_highway.pdf')
    if show_plot:
        plt.show()
    else:
        plt.close()

    #####################
    ### Distributions ###
    #####################

    plot_arbis_dist([
        'Length',
        # 'Duration'
    ],
        arbis_selected, plot_path, file_prefix, save_plot, show_plot)

    ##############
    ### Counts ###
    ##############

    # Plot distribution of AnzGesperrtFs
    plt.figure(figsize=set_size(418))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Distribution of AnzGesperrtFs')
    plt.ylabel('Count')
    plt.xlabel('AnzGesperrtFs')
    sns.countplot(x='AnzGesperrtFs', data=arbis_selected, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_dist_AnzGesperrtFs.pdf')
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Plot distribution of Einzug
    plt.figure(figsize=set_size(418))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Distribution of Einzug')
    plt.ylabel('Count')
    plt.xlabel('Einzug')
    sns.countplot(x='Einzug', data=arbis_selected, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_dist_Einzug.pdf')
    if show_plot:
        plt.show()
    else:
        plt.close()

    # Plot distribution of Richtung
    plt.figure(figsize=set_size(418, 0.8))
    plt.style.use('seaborn')
    plt.rcParams.update(tex_fonts)
    plt.title('Distribution of Richtung')
    plt.ylabel('Count')
    plt.xlabel('Richtung')
    sns.countplot(x='Richtung', data=arbis_selected, palette='Spectral')
    if save_plot:
        plt.savefig(plot_path + file_prefix + '_dist_Richtung.pdf')
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

    # Plot boxplots for visual relation testing
    # plot_boxplot_logscale(arbis_selected, 'Strasse', 'Length', save_plot, show_plot,
    #                       plot_path + file_prefix + '_box_street2length.pdf', scale=1.8)
    #
    # plot_boxplot_logscale(arbis_selected, 'Strasse', 'Duration', save_plot, show_plot,
    #                       plot_path + file_prefix + '_box_street2duration.pdf', scale=1.8)
    #
    # plot_boxplot_logscale(arbis_selected, 'AnzGesperrtFs', 'Length', save_plot, show_plot,
    #                       plot_path + file_prefix + '_box_agfs2length.pdf')
    #
    # plot_boxplot_logscale(arbis_selected, 'AnzGesperrtFs', 'Duration', save_plot, show_plot,
    #                       plot_path + file_prefix + '_box_agfs2duration.pdf')
    #
    # plot_boxplot_logscale(arbis_selected, 'Einzug', 'Length', save_plot, show_plot,
    #                       plot_path + file_prefix + '_box_einzug2length.pdf')
    #
    # plot_boxplot_logscale(arbis_selected, 'Einzug', 'Duration', save_plot, show_plot,
    #                       plot_path + file_prefix + '_box_einzug2duration.pdf')
    #
    # plot_boxplot_logscale(arbis_selected, 'Richtung', 'Length', save_plot, show_plot,
    #                       plot_path + file_prefix + '_box_direction2length.pdf')
    #
    # plot_boxplot_logscale(arbis_selected, 'Richtung', 'Duration', save_plot, show_plot,
    #                       plot_path + file_prefix + '_box_direction2duration.pdf')

    ###################
    ### Correlation ###
    ###################

    # define column types
    nominal_columns = ['Strasse', 'StreckeID', 'Month']
    dichotomous_columns = ['Richtung']
    ordinal_columns = ['AnzGesperrtFs', 'Einzug']

    # Encode non numerical columns
    arbis_encoded, arbis_encoded_dict = numerical_encoding(arbis_selected,
                                                           ['Strasse',
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
                     show=show_plot, scale=2.0)

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + file_prefix + '_sign_cramers.pdf',
                   show=show_plot, scale=2.0)

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
                     show=show_plot, scale=2.0)

    # Plot statistics/significant matrix
    plot_statistic(results.get('significance'), results.get('columns'),
                   nominal_columns, dichotomous_columns, ordinal_columns,
                   results.get('inf_nan_corr'),
                   results.get('columns_single_value'),
                   save=save_plot, filepath=plot_path + file_prefix + '_sign_theils.pdf',
                   show=show_plot, scale=2.0)

    # Export correlation/statistics/coefficients into latex tables
    with open(tex_path + file_prefix + '_corr_theils.tex', 'w') as tf:
        tf.write(results.get('correlation').to_latex(float_format="{:0.2f}".format))

    with open(tex_path + file_prefix + '_sign_theils.tex', 'w') as tf:
        tf.write(results.get('significance').to_latex())

    with open(tex_path + file_prefix + '_coef_theils.tex', 'w') as tf:
        tf.write(results.get('coefficient').to_latex())

    print('Finished ArbIS Dataset Analysis')
