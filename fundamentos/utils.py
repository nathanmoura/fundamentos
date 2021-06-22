import random
import string


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


def get_headers():
    return {
        'User-Agent': ''.join(
            random.choices(string.ascii_letters, k=10)
        )
    }
