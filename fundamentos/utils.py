
class DataNotFound(IndexError):
    pass


def convert_type(x):
    if str(x).endswith('%'):
        return float(x[:-1].replace('.', '').replace(',', '.')) / 100
    try:
        if float(x).is_integer():
            return int(float(x))
        return float(x)
    except ValueError:
        return None
