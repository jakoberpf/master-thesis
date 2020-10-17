import math
import warnings
from collections import Counter

import numpy as np
import pandas as pd
import scipy.stats as ss

from func_utils import convert, remove_incomplete_samples, replace_nan_with_value, \
    cluster_correlations, identify_nominal_columns, identify_ordinal_columns, identify_dichotomous_columns, _inf_nan_str

__all__ = [
    'compute_correlations',
    # continuous-continuous
    'pearsons',
    # continuous-categorical(nominal)
    'kruskal_wallis',  # for significance
    'eta',
    # continuous-categorical(dichotomous)
    'wilcoxon',  # for significance
    'point_biserial',
    # continuous-categorical(ordinal)
    'kendall',
    # categorical-categorical
    'cramers_v',
    'theils_u'
]

_REPLACE = 'replace'
_DROP = 'drop'
_DROP_SAMPLES = 'drop_samples'
_DROP_FEATURES = 'drop_features'
_SKIP = 'skip'
_DEFAULT_REPLACE_VALUE = 0.0
_NOT_IMPLEMENTED = ' is not implemented'
_ALPHA = 0.05
_CORR_NAN = np.nan
_SIGN_NAN = np.nan


###############################
### Continuous - Continuous ###
###############################


def pearsons(measurements_x, measurements_y):
    """

    Pearson's r TODO add docstring

    Parameters:
    -----------
    switch : the coefficient to use for calculation
    x : list / NumPy ndarray / Pandas Series
        A sequence of continuous measurements
    y : list / NumPy ndarray / Pandas Series
        A sequence of continuous measurements

    Returns:
    --------
    float : in the range of [0,1]
    float : p-value (2 tailed)
    str   : correlation name/identifier
    """
    print(measurements_x.name + ' to ' + measurements_y.name + ' with Pearson')
    coefficient, p_value = ss.pearsonr(measurements_x, measurements_y)
    return coefficient, p_value, 'Pearson\'s r'


#########################################
### Continuous - Categorical(Nominal) ###
#########################################

def kruskal_wallis(x, y):
    """

    Kruskal-Wallis H TODO add docstring

    Parameters:
    -----------
    x : list / NumPy ndarray / Pandas Series
        A sequence of continuous measurements
    y : list / NumPy ndarray / Pandas Series
        A sequence of categorical measurements

    Returns:
    --------
    float : statistic of variations
    float : p-value
    str   : correlation name/identifier
    """
    f_statistic, p_value = ss.kruskal(x, y)
    # if p_value < _ALPHA:
    #     print(
    #         'ATTENTION: Kruskal-Wallis (' + p_value.__str__() + ') is smaller then alpha(' + _ALPHA.__str__() + '). ' +
    #         'This means that there is a different between the ranks and further testing is necessary')
    return f_statistic, p_value


def eta(measurements,
        categories,
        nan_strategy=_REPLACE,
        nan_replace_value=_DEFAULT_REPLACE_VALUE):
    """
    Calculates the Correlation Ratio (sometimes marked by the greek letter Eta)
    for categorical-continuous association.

    Answers the question - given a continuous value of a measurement, is it
    possible to know which category is it associated with?

    Value is in the range [0,1], where 0 means a category cannot be determined
    by a continuous measurement, and 1 means a category can be determined with
    absolute certainty.

    Wikipedia: https://en.wikipedia.org/wiki/Correlation_ratio

    Parameters:
    -----------
    measurements : list / NumPy ndarray / Pandas Series
        A sequence of continuous measurements
    categories : list / NumPy ndarray / Pandas Series
        A sequence of categorical measurements
    nan_strategy : string, default = 'replace'
        How to handle missing values: can be either 'drop' to remove samples
        with missing values, or 'replace' to replace all missing values with
        the nan_replace_value. Missing values are None and np.nan.
    nan_replace_value : any, default = 0.0
        The value used to replace missing values with. Only applicable when
        nan_strategy is set to 'replace'.

    Returns:
    --------
    float : correlation coefficient in the range of [0,1]
    float : p-value, calculated with Kruskal-Wallis H
    str   : correlation name/identifier
    """
    print(categories.name + ' to ' + measurements.name + ' with Correlation Ration (Eta) and Kruskal-Wallis H')
    if nan_strategy == _REPLACE:
        categories, measurements = replace_nan_with_value(
            categories, measurements, nan_replace_value)
    elif nan_strategy == _DROP:
        categories, measurements = remove_incomplete_samples(
            categories, measurements)
    categories = convert(categories, 'array')
    measurements = convert(measurements, 'array')
    fcat, _ = pd.factorize(categories)
    cat_num = np.max(fcat) + 1
    y_avg_array = np.zeros(cat_num)
    n_array = np.zeros(cat_num)
    for i in range(0, cat_num):
        cat_measures = measurements[np.argwhere(fcat == i).flatten()]
        n_array[i] = len(cat_measures)
        y_avg_array[i] = np.average(cat_measures)
    y_total_avg = np.sum(np.multiply(y_avg_array, n_array)) / np.sum(n_array)
    numerator = np.sum(
        np.multiply(n_array, np.power(np.subtract(y_avg_array, y_total_avg), 2)))
    denominator = np.sum(np.power(np.subtract(measurements, y_total_avg), 2))
    if numerator == 0:
        correlation = 0.0
    else:
        correlation = np.sqrt(numerator / denominator)

    f_statistic, p_value = kruskal_wallis(measurements, categories)
    return correlation, p_value, 'Eta'


############################################
### Continuous - Categorical(Dichotoums) ###
############################################


def wilcoxon(measurements_x, measurements_y):
    """

    Wilcoxon (Mann-Withney) test TODO add docstring

    Parameters:
    -----------
    x : list / NumPy ndarray / Pandas Series
        A sequence of continuous measurements
    y : list / NumPy ndarray / Pandas Series
        A sequence of categorical(dichotoums) measurements

    Returns:
    --------
    float : statistic of variations
    float : p-value
    str   : correlation name/identifier
    """
    print(measurements_x.name + ' to ' + measurements_y.name + ' with Wilcoxon (Mann Whitney)')
    statistic, p_value = ss.wilcoxon(measurements_x, measurements_y)
    return statistic, p_value


def point_biserial(measurements, dichotomies):
    """

    Pearson's Point Biserial TODO add docstring

    Parameters:
    -----------
    x : list / NumPy ndarray / Pandas Series
        A sequence of continuous measurements
    y : list / NumPy ndarray / Pandas Series
        A sequence of categorical(dichotoums) measurements

    Returns:
    --------
    float : correlation coefficient in the range of [0,1]
    float : p-value
    str   : correlation name/identifier
    """
    print(measurements.name + ' to ' + dichotomies.name + ' with Point Biserial')
    correlation, p_value = ss.pointbiserialr(dichotomies, measurements)
    # statistic, p_value = wilcoxon(measurements, dichotomies)
    return correlation, p_value, 'Point Biserial and Wilcoxon (Mann Whitney)'


#########################################
### Continuous - Categorical(Nominal) ###
#########################################

def kendall(measurements_x, measurements_y):
    """

    Kruskal-Wallis H TODO add docstring

    Parameters:
    -----------
    x : list / NumPy ndarray / Pandas Series
        A sequence of continuous measurements
    y : list / NumPy ndarray / Pandas Series
        A sequence of categorical(dichotoums) measurements

    Returns:
    --------
    float : correlation coefficient in the range of [0,1]
    float : p-value
    str   : correlation name/identifier
    """
    print(measurements_x.name + ' to ' + measurements_y.name + ' with Kendall')
    correlation, p_value = ss.kendalltau(measurements_x, measurements_y)
    return correlation, p_value, 'Kendalls $tau$'


#################################
### Categorical - Categorical ###
#################################

def cramers_v(x,
              y,
              bias_correction=True,
              nan_strategy=_REPLACE,
              nan_replace_value=_DEFAULT_REPLACE_VALUE):
    """
    Calculates Cramer's V statistic for categorical-categorical association.
    This is a symmetric coefficient: V(x,y) = V(y,x)
    Uses correction from Bergsma and Wicher, Journal of the Korean Statistical Society 42 (2013): 323-328

    Original function taken from: https://stackoverflow.com/a/46498792/5863503
    Wikipedia: https://en.wikipedia.org/wiki/Cram%C3%A9r%27s_V

    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    temp = phi2 - ((k - 1) * (r - 1)) / (n - 1)
    phi2corr = max(0, temp)
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))

    Parameters:
    -----------
    x : list / NumPy ndarray / Pandas Series
        A sequence of categorical measurements
    y : list / NumPy ndarray / Pandas Series
        A sequence of categorical measurements
    bias_correction : Boolean, default = True
        Use bias correction from Bergsma and Wicher,
        Journal of the Korean Statistical Society 42 (2013): 323-328.
    nan_strategy : string, default = 'replace'
        How to handle missing values: can be either 'drop' to remove samples
        with missing values, or 'replace' to replace all missing values with
        the nan_replace_value. Missing values are None and np.nan.
    nan_replace_value : any, default = 0.0
        The value used to replace missing values with. Only applicable when
        nan_strategy is set to 'replace'.

    Returns:
    --------
    float : in the range of [0,1]
    float : _SIGN_NAN as default p-value
    str   : correlation name/identifier
    """

    print(x.name + ' to ' + y.name + ' with Cramers V')

    if nan_strategy == _REPLACE:
        x, y = replace_nan_with_value(x, y, nan_replace_value)
    elif nan_strategy == _DROP:
        x, y = remove_incomplete_samples(x, y)
    confusion_matrix = pd.crosstab(x, y)
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    if bias_correction:
        phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
        rcorr = r - ((r - 1) ** 2) / (n - 1)
        kcorr = k - ((k - 1) ** 2) / (n - 1)
        if min((kcorr - 1), (rcorr - 1)) == 0:
            warnings.warn(
                "Unable to calculate Cramer's V using bias correction. Consider using bias_correction=False",
                RuntimeWarning)
            return np.nan
        else:
            return np.sqrt(phi2corr / min((kcorr - 1), (rcorr - 1)))
    else:
        return np.sqrt(phi2 / min(k - 1, r - 1)), _SIGN_NAN, 'Cramer\'s V'


def theils_u(x,
             y,
             nan_strategy=_REPLACE,
             nan_replace_value=_DEFAULT_REPLACE_VALUE):
    """
    Calculates Theil's U statistic (Uncertainty coefficient) for categorical-
    categorical association. This is the uncertainty of x given y: value is
    on the range of [0,1] - where 0 means y provides no information about
    x, and 1 means y provides full information about x.

    This is an asymmetric coefficient: U(x,y) != U(y,x)

    Wikipedia: https://en.wikipedia.org/wiki/Uncertainty_coefficient

    s_xy = conditional_entropy(x, y)
    x_counter = Counter(x)
    total_occurrences = sum(x_counter.values())
    p_x = list(map(lambda n: n / total_occurrences, x_counter.values()))
    s_x = ss.entropy(p_x)
    if s_x == 0:
        return 1
    else:
        return (s_x - s_xy) / s_x

    Parameters:
    -----------
    x : list / NumPy ndarray / Pandas Series
        A sequence of categorical measurements
    y : list / NumPy ndarray / Pandas Series
        A sequence of categorical measurements
    nan_strategy : string, default = 'replace'
        How to handle missing values: can be either 'drop' to remove samples
        with missing values, or 'replace' to replace all missing values with
        the nan_replace_value. Missing values are None and np.nan.
    nan_replace_value : any, default = 0.0
        The value used to replace missing values with. Only applicable when
        nan_strategy is set to 'replace'.

    Returns:
    --------
    float : in the range of [0,1]
    float : _SIGN_NAN as default p-value
    str   : correlation name/identifier
    """

    print(x.name + ' to ' + y.name + ' with Theils U')

    if nan_strategy == _REPLACE:
        x, y = replace_nan_with_value(x, y, nan_replace_value)
    elif nan_strategy == _DROP:
        x, y = remove_incomplete_samples(x, y)
    s_xy = conditional_entropy(x, y)
    x_counter = Counter(x)
    total_occurrences = sum(x_counter.values())
    p_x = list(map(lambda n: n / total_occurrences, x_counter.values()))
    s_x = ss.entropy(p_x)
    if s_x == 0:
        return 1, -1
    else:
        return (s_x - s_xy) / s_x, _SIGN_NAN, 'Theils\'s U'


def conditional_entropy(x,
                        y,
                        nan_strategy=_REPLACE,
                        nan_replace_value=_DEFAULT_REPLACE_VALUE,
                        log_base: float = math.e):
    """
    Calculates the conditional entropy of x given y: S(x|y)
    Used by the Theil's U implementation

    Wikipedia: https://en.wikipedia.org/wiki/Conditional_entropy

    Parameters:
    -----------
    x : list / NumPy ndarray / Pandas Series
        A sequence of measurements
    y : list / NumPy ndarray / Pandas Series
        A sequence of measurements
    nan_strategy : string, default = 'replace'
        How to handle missing values: can be either 'drop' to remove samples
        with missing values, or 'replace' to replace all missing values with
        the nan_replace_value. Missing values are None and np.nan.
    nan_replace_value : any, default = 0.0
        The value used to replace missing values with. Only applicable when
        nan_strategy is set to 'replace'.
    log_base: float, default = e
        specifying base for calculating entropy. Default is base e.

    Returns:
    --------
    float
    """
    if nan_strategy == _REPLACE:
        x, y = replace_nan_with_value(x, y, nan_replace_value)
    elif nan_strategy == _DROP:
        x, y = remove_incomplete_samples(x, y)
    y_counter = Counter(y)
    xy_counter = Counter(list(zip(x, y)))
    total_occurrences = sum(y_counter.values())
    entropy = 0.0
    for xy in xy_counter.keys():
        p_xy = xy_counter[xy] / total_occurrences
        p_y = y_counter[xy[1]] / total_occurrences
        entropy += p_xy * math.log(p_y / p_xy, log_base)
    return entropy


def compute_correlations(dataset,
                         encode=False,
                         columns_nominal='auto',
                         columns_dichotomous='auto',
                         columns_ordinal=None,
                         mark_columns=False,
                         continuous_continuous='pearson',
                         continuous_nominal='kruskal-wallis',
                         continuous_dichotomous='point-biserial',
                         continuous_ordinal='spearman',
                         categorical_categorical='cramers_v',
                         clustering=False,
                         bias_correction=True,
                         nan_strategy=_REPLACE,
                         nan_replace_value=_DEFAULT_REPLACE_VALUE):
    """
    Calculate the correlation/strength-of-association of features in data-set
    with both categorical and continuous features using:
     * Pearson's R for continuous-continuous cases
     * Correlation Ratio or Point Biserial for categorical-continuous cases
     * Cramer's V or Theil's U for categorical-categorical cases

    Parameters:
    -----------
    dataset : NumPy ndarray / Pandas DataFrame
        The data-set for which the features' correlation is computed
    nominal_columns : string / list / NumPy ndarray
        Names of columns of the data-set which hold categorical values. Can
        also be the string 'all' to state that all columns are categorical,
        'auto' (default) to try to identify nominal columns, or None to state
        none are categorical
    mark_columns : Boolean, default = False
        if True, output's columns' names will have a suffix of '(nom)' or
        '(con)' based on there type (eda_tools or continuous), as provided
        by nominal_columns
    continuous_continuous : default is 'pearson', but other correlation
        coefficients can be chosen.
    continuous_nominal : default is 'correlation_ratio', but other correlation
        coefficients can be chosen.
    continuous_dichotomous : default is  'point_biserial', but other correlation
        coefficients can be chosen.
    continuous_ordinal : default is 'spearman', but other correlation
        coefficients can be chosen.
    categorical_categorical : default is 'cramer', but other correlation
        coefficients can be chosen.
    clustering : Boolean, default = False
        If True, hierarchical clustering is applied in order to sort
        features into meaningful groups
    bias_correction : Boolean, default = True
        Use bias correction for Cramer's V from Bergsma and Wicher,
        Journal of the Korean Statistical Society 42 (2013): 323-328.
    nan_strategy : string, default = 'replace'
        How to handle missing values: can be either 'drop_samples' to remove
        samples with missing values, 'drop_features' to remove features
        (columns) with missing values, or 'replace' to replace all missing
        values with the nan_replace_value. Missing values are None and np.nan.
    nan_replace_value : any, default = 0.0
        The value used to replace missing values with. Only applicable when
        nan_strategy is set to 'replace'

    Returns:
    --------
    A DataFrame of the correlation/strength-of-association between all features
    """
    dataset = convert(dataset, 'dataframe')  # TODO implement encoding

    if nan_strategy == _REPLACE:
        dataset.fillna(nan_replace_value, inplace=True)
    elif nan_strategy == _DROP_SAMPLES:
        dataset.dropna(axis=0, inplace=True)
    elif nan_strategy == _DROP_FEATURES:
        dataset.dropna(axis=1, inplace=True)

    columns = dataset.columns

    if columns_nominal is None:
        columns_nominal = list()
    elif columns_nominal == 'all':
        columns_nominal = columns
    elif columns_nominal == 'auto':
        columns_nominal = identify_nominal_columns(dataset)

    if columns_dichotomous is None:
        columns_dichotomous = list()
    elif columns_dichotomous == 'all':
        columns_dichotomous = columns
    elif columns_dichotomous == 'auto':
        columns_dichotomous = identify_dichotomous_columns(dataset, columns_nominal)

    if columns_ordinal is None:
        columns_ordinal = list()
    elif columns_ordinal == 'all':
        columns_ordinal = columns
    elif columns_ordinal == 'auto':
        columns_ordinal = identify_ordinal_columns(dataset, columns_nominal, columns_dichotomous)

    corr = pd.DataFrame(index=columns, columns=columns)
    sign = pd.DataFrame(index=columns, columns=columns)
    coef = pd.DataFrame(index=columns, columns=columns)

    columns_single_value = []

    inf_nan_corr = pd.DataFrame(data=np.zeros_like(corr),
                                columns=columns,
                                index=columns)

    inf_nan_sign = pd.DataFrame(data=np.zeros_like(corr),
                                columns=columns,
                                index=columns)

    for c in columns:
        # Test if column only contains single value
        if dataset[c].unique().size == 1:
            # Column only contains a single value, prepare for no calculation to be done
            columns_single_value.append(c)

    for i in range(0, len(columns)):

        if columns[i] in columns_single_value:
            # If column only contains a single value, not correlation calculation necessary
            corr.loc[:, columns[i]] = 0.0
            corr.loc[columns[i], :] = 0.0
            continue

        for j in range(i, len(columns)):

            if columns[j] in columns_single_value:
                continue

            elif i == j:
                # Correlation to itself is always 1.0
                corr.loc[columns[i], columns[j]] = 1.0
                sign.loc[columns[i], columns[j]] = _SIGN_NAN
                inf_nan_sign.loc[columns[i], columns[j]] = _inf_nan_str(_SIGN_NAN)

            else:
                # print('Processing ' + columns[i] + ' and ' + columns[j])
                if columns[i] in columns_nominal or columns[i] in columns_dichotomous or columns[i] in columns_ordinal:
                    # i is categorical
                    if columns[j] in columns_nominal or columns[j] in columns_dichotomous or columns[
                        j] in columns_ordinal:
                        # i and j are categorical
                        if categorical_categorical == 'theils_u':
                            # Because Theil's U is asymmetrical, calculate both directions separately
                            ij, p, c = theils_u(dataset[columns[i]], dataset[columns[j]])  # TODO handle two p values
                            ji, p, c = theils_u(dataset[columns[j]], dataset[columns[i]])  # TODO handle two p values
                        else:
                            cell, p, c = cramers_v(dataset[columns[i]], dataset[columns[j]],
                                                   bias_correction=bias_correction)
                            ij = cell
                            ji = cell
                    else:
                        # i is categorical, j is continuous
                        if columns[i] in columns_ordinal:
                            # i is ordinal, j is continuous
                            if continuous_ordinal == 'kendall':
                                cell, p, c = kendall(dataset[columns[j]], dataset[columns[i]])
                            else:
                                cell, p, c = spearman(dataset[columns[j]], dataset[columns[i]])
                        elif columns[i] in columns_dichotomous:
                            # i is dichotomous, j is continuous
                            if continuous_dichotomous == 'mann-whitney':
                                cell, p, c = mann_whitney(dataset[columns[j]], dataset[columns[i]])
                            else:
                                cell, p, c = point_biserial(dataset[columns[j]], dataset[columns[i]])
                        else:
                            # i is nominal, j is continuous
                            if continuous_nominal == 'anova':
                                cell, p, c = anova(dataset[columns[j]], dataset[columns[i]])
                            elif continuous_nominal == 'kruskal-wallis':
                                cell, p, c = kruskal_wallis(dataset[columns[j]], dataset[columns[i]])
                            else:
                                cell, p, c = eta(dataset[columns[j]], dataset[columns[i]])

                        ij = cell
                        ji = cell

                elif columns[j] in columns_nominal or columns[j] in columns_dichotomous or columns[
                    j] in columns_ordinal:
                    # j is categorical, i is continuous
                    if columns[j] in columns_ordinal:
                        # j is ordinal, i is continuous
                        if continuous_ordinal == 'kendall':
                            cell, p, c = kendall(dataset[columns[i]], dataset[columns[j]])
                        else:
                            cell, p, c = spearman(dataset[columns[i]], dataset[columns[j]])
                    elif columns[j] in columns_dichotomous:
                        # j is dichotomous, i is continuous
                        if continuous_dichotomous == 'mann-whitney':
                            cell, p, c = mann_whitney(dataset[columns[i]], dataset[columns[j]])
                        elif continuous_dichotomous == 'wilcoxon':
                            cell, p, c = wilcoxon(dataset[columns[i]], dataset[columns[j]])
                        else:
                            cell, p, c = point_biserial(dataset[columns[i]], dataset[columns[j]])
                    else:
                        # j is nominal, i is continuous
                        if continuous_nominal == 'anova':
                            cell, p, c = anova(dataset[columns[i]], dataset[columns[j]])
                        elif continuous_nominal == 'kruskal-wallis':
                            cell, p, c = kruskal_wallis(dataset[columns[i]], dataset[columns[j]])
                        else:
                            cell, p, c = eta(dataset[columns[i]], dataset[columns[j]])

                    ij = cell
                    ji = cell

                else:
                    # i and j are continuous
                    assert columns[i] not in columns_nominal or columns[i] not in columns_dichotomous or columns[
                        i] not in columns_ordinal, columns[i] + ' should not be here'
                    assert columns[j] not in columns_nominal or columns[j] not in columns_dichotomous or columns[
                        j] not in columns_ordinal, columns[j] + ' should not be here'
                    cell, p, c = pearsons(dataset[columns[i]], dataset[columns[j]])

                    ij = cell
                    ji = cell

                corr.loc[columns[i], columns[j]] = round(ij, 2) if not np.isnan(ij) and abs(ij) < np.inf else 0.0
                corr.loc[columns[j], columns[i]] = round(ji, 2) if not np.isnan(ji) and abs(ji) < np.inf else 0.0
                sign.loc[columns[i], columns[j]] = round(p, 4) if not np.isnan(p) and abs(p) < np.inf else _SIGN_NAN
                sign.loc[columns[j], columns[i]] = round(p, 4) if not np.isnan(p) and abs(p) < np.inf else _SIGN_NAN
                coef.loc[columns[i], columns[j]] = c
                coef.loc[columns[j], columns[i]] = c
                inf_nan_corr.loc[columns[i], columns[j]] = _inf_nan_str(ij)
                inf_nan_corr.loc[columns[j], columns[i]] = _inf_nan_str(ji)
                inf_nan_sign.loc[columns[i], columns[j]] = _inf_nan_str(p)
                inf_nan_sign.loc[columns[j], columns[i]] = _inf_nan_str(p)

    corr.fillna(value=np.nan, inplace=True)
    sign.fillna(value=np.nan, inplace=True)

    if mark_columns:
        marked_columns = [
            '{} (nom)'.format(col)
            if col in columns_nominal else '{} (con)'.format(col)
            for col in columns
        ]
        corr.columns = marked_columns
        corr.index = marked_columns
        inf_nan_corr.columns = marked_columns
        inf_nan_corr.index = marked_columns

    if clustering:
        corr, p = cluster_correlations(corr)
        columns = corr.columns

    return {
        'correlation': corr,
        'significance': sign,
        'coefficient': coef,
        'columns': columns,
        'columns_nominal': columns_nominal,
        'columns_dichotomous': columns_dichotomous,
        'columns_ordinal': columns_ordinal,
        'inf_nan_corr': inf_nan_corr,
        'inf_nan_sign': inf_nan_sign,
        'columns_single_value': columns_single_value}


def numerical_encoding(dataset,
                       nominal_columns='auto',
                       drop_single_label=False,
                       drop_fact_dict=True,
                       nan_strategy=_REPLACE,
                       nan_replace_value=_DEFAULT_REPLACE_VALUE):
    """
    Encoding a data-set with mixed data (numerical and categorical) to a
    numerical-only data-set using the following logic:
    * categorical with only a single value will be marked as zero (or dropped,
        if requested)
    * categorical will be replaced with the result of Pandas
        `factorize`
    * numerical columns will not be modified

    Parameters:
    -----------
    dataset : NumPy ndarray / Pandas DataFrame
        The data-set to encode
    nominal_columns : sequence / string. default = 'all'
        A sequence of the nominal (categorical) columns in the dataset. If
        string, must be 'all' to state that all columns are nominal. If None,
        nothing happens. If 'auto', categorical columns will be identified
        based on dtype.
    drop_single_label : Boolean, default = False
        If True, nominal columns with a only a single value will be dropped.
    drop_fact_dict : Boolean, default = True
        If True, the return value will be the encoded DataFrame alone. If
        False, it will be a tuple of the DataFrame and the dictionary of the
        binary factorization (originating from pd.factorize)
    nan_strategy : string, default = 'replace'
        How to handle missing values: can be either 'drop_samples' to remove
        samples with missing values, 'drop_features' to remove features
        (columns) with missing values, or 'replace' to replace all missing
        values with the nan_replace_value. Missing values are None and np.nan.
    nan_replace_value : any, default = 0.0
        The value used to replace missing values with. Only applicable when nan
        _strategy is set to 'replace'

    Returns:
    --------
    DataFrame or (DataFrame, dict). If `drop_fact_dict` is True,
    returns the encoded DataFrame.
    else, returns a tuple of the encoded DataFrame and dictionary, where each
    key is a two-value column, and the value is the original labels, as
    supplied by Pandas `factorize`. Will be empty if no two-value columns are
    present in the data-set
    """
    dataset = convert(dataset, 'dataframe')
    if nan_strategy == _REPLACE:
        dataset.fillna(nan_replace_value, inplace=True)
    elif nan_strategy == _DROP_SAMPLES:
        dataset.dropna(axis=0, inplace=True)
    elif nan_strategy == _DROP_FEATURES:
        dataset.dropna(axis=1, inplace=True)
    if nominal_columns is None:
        return dataset
    elif nominal_columns == 'all':
        nominal_columns = dataset.columns
    elif nominal_columns == 'auto':
        nominal_columns = identify_nominal_columns(dataset)
    converted_dataset = pd.DataFrame()
    binary_columns_dict = dict()
    for col in dataset.columns:
        if col not in nominal_columns:
            # Not a nominal column -> Copy original
            converted_dataset.loc[:, col] = dataset[col]
        else:
            # A nominal column -> Convert
            unique_values = pd.unique(dataset[col])
            if len(unique_values) == 1 and not drop_single_label:
                # Only one value present -> Drop
                converted_dataset.loc[:, col] = 0
            else:
                converted_dataset.loc[:, col], binary_columns_dict[col] = pd.factorize(dataset[col])
    if drop_fact_dict:
        return converted_dataset
    else:
        return converted_dataset, binary_columns_dict
