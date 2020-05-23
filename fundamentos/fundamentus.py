import requests
import pandas as pd


def get_tickers():
    '''Downloads tickers' codes from fundamentus website

    :Returns:

    A pandas DataFrame with three columns:

    Papel (Ticker),
    Nome Comercial (Trade Name),
    Razão Social (Corporate Name)
    '''
    html_src = requests.get(
        'http://fundamentus.com.br/detalhes.php').text
    return pd.read_html(html_src)[0]
