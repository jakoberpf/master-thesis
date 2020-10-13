from datetime import time

import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as sch

__all__ = [
    'cluster_correlations',
    'identify_nominal_columns',
    'identify_numeric_columns',
    'identify_columns_by_type'

]


def print_welcome():
    print(f'Welcome to the CONGSTST Correlation Analysis Script, please follow the instructions, if any are given.')


def date_parser(string_list):
    return [time.ctime(float(x)) for x in string_list]


def _inf_nan_str(x):
    if np.isnan(x):
        return 'NaN'
    elif abs(x) == np.inf:
        return 'inf'
    else:
        return ''


def identify_numeric_columns(dataset):
    """
    Given a dataset, identify numeric columns.

    Parameters:
    -----------
    dataset : NumPy ndarray / Pandas DataFrame

    Returns:
    --------
    A list of numerical columns names

    Example:
    --------
    >> df = pd.DataFrame({'col1': ['a', 'b', 'c', 'a'], 'col2': [3, 4, 2, 1], 'col3': [1., 2., 3., 4.]})
    >> identify_numeric_columns(df)
    ['col2', 'col3']

    """
    return identify_columns_by_type(dataset, include=['int64', 'float64'])


def identify_nominal_columns(dataset):
    """
    Given a dataset, identify categorical columns.

    Parameters:
    -----------
    dataset : NumPy ndarray / Pandas DataFrame

    Returns:
    --------
    A list of categorical columns names

    Example:
    --------
    >> df = pd.DataFrame({'col1': ['a', 'b', 'c', 'a'], 'col2': [3, 4, 2, 1]})
    >> identify_nominal_columns(df)
    ['col1']

    """
    return identify_columns_by_type(dataset, include=['object', 'category'])


def identify_dichotomous_columns(dataset, nominal_columns):
    """
    Given a dataset, identify categorical columns.

    Parameters:
    -----------
    dataset : NumPy ndarray / Pandas DataFrame

    Returns:
    --------
    A list of categorical columns names

    Example:
    --------
    >> df = pd.DataFrame({'col1': ['a', 'b', 'c', 'a'], 'col2': [3, 4, 2, 1]})
    >> identify_nominal_columns(df)
    ['col1']

    """
    pass


def identify_ordinal_columns(dataset, nominal_columns, dichotomous_columns):
    pass


def identify_columns_by_type(dataset, include):
    """
    Given a dataset, identify columns of the types requested.

    Parameters:
    -----------
    dataset : NumPy ndarray / Pandas DataFrame
    include : list of strings
        Desired column types

    Returns:
    --------
    A list of columns names

    Example:
    --------
    >> df = pd.DataFrame({'col1': ['a', 'b', 'c', 'a'], 'col2': [3, 4, 2, 1], 'col3': [1., 2., 3., 4.]})
    >> identify_columns_by_type(df, include=['int64', 'float64'])
    ['col2', 'col3']

    """
    dataset = convert(dataset, 'dataframe')
    columns = list(dataset.select_dtypes(include=include).columns)
    return columns


def convert(data, to):
    """
    Converts the given data format to a NumPy Array / List or Pandas Dataframe

    Parameters:
    -----------
    data : NumPy Array / List or Pandas Dataframe
    to : Desired type of return format

    Returns:
    --------
    The data as a NumPy Array / List or Pandas Dataframe
    """
    converted = None
    if to == 'array':
        if isinstance(data, np.ndarray):
            converted = data
        elif isinstance(data, pd.Series):
            converted = data.values
        elif isinstance(data, list):
            converted = np.array(data)
        elif isinstance(data, pd.DataFrame):
            converted = data.as_matrix()
    elif to == 'list':
        if isinstance(data, list):
            converted = data
        elif isinstance(data, pd.Series):
            converted = data.values.tolist()
        elif isinstance(data, np.ndarray):
            converted = data.tolist()
    elif to == 'dataframe':
        if isinstance(data, pd.DataFrame):
            converted = data
        elif isinstance(data, np.ndarray):
            converted = pd.DataFrame(data)
    else:
        raise ValueError("Unknown data conversion: {}".format(to))
    if converted is None:
        raise TypeError(
            'cannot handle data conversion of type: {} to {}'.format(
                type(data), to))
    else:
        return converted


def cluster_correlations(corr_mat, indices=None):
    """
    Apply agglomerative clustering in order to sort
    a correlation matrix.

    Based on https://github.com/TheLoneNut/CorrelationMatrixClustering/blob/master/CorrelationMatrixClustering.ipynb

    Parameters:
    -----------
    - corr_mat : a square correlation matrix (pandas DataFrame)
    - indices : cluster labels [None]; if not provided we'll do
        an agglomerative clustering to get cluster labels.

    Returns:
    --------
    - corr : a sorted correlation matrix
    - indices : cluster indexes based on the original dataset

    Example:
    --------
    >> assoc = associations(
        customers,
        plot=False
    )
    >> correlations = assoc['corr']
    >> correlations, _ = cluster_correlations(correlations)
    """
    if indices is None:
        X = corr_mat.values
        d = sch.distance.pdist(X)
        L = sch.linkage(d, method='complete')
        indices = sch.fcluster(L, 0.5 * d.max(), 'distance')
    columns = [corr_mat.columns.tolist()[i]
               for i in list((np.argsort(indices)))]
    corr_mat = corr_mat.reindex(columns=columns).reindex(index=columns)
    return corr_mat, indices


def remove_incomplete_samples(x, y):
    x = [v if v is not None else np.nan for v in x]
    y = [v if v is not None else np.nan for v in y]
    arr = np.array([x, y]).transpose()
    arr = arr[~np.isnan(arr).any(axis=1)].transpose()
    if isinstance(x, list):
        return arr[0].tolist(), arr[1].tolist()
    else:
        return arr[0], arr[1]


def replace_nan_with_value(x, y, value):
    x = np.array([v if v == v and v is not None else value for v in x])  # NaN != NaN
    y = np.array([v if v == v and v is not None else value for v in y])
    return x, y
