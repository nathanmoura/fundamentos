import numpy as np


class DataNotFound(IndexError):
    pass


def convert_type(x):
    if str(x).endswith('%'):
        return float(x[:-1].replace('.', '').replace(',', '.')) / 100
    try:
        if float(x).is_integer():
            return int(x)
        return float(x)
    except ValueError:
        if x == 'N/D' or x == '-':
            return np.nan
        return x
