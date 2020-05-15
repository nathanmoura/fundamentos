import requests
import pandas as pd
from .utils import convert_type, DataNotFound
from concurrent import futures
from datetime import date


def get_tickers(char=None):
    '''Downloads tickers' codes from ADVFN website

    :Parameters:

    char[chr] (ascii letter or digit):
        The char corresponding to ADVFN's webpage to download data from.
        If None, downloads all tickers enlisted on the website.
        Default is None

    :Raises:

    DataNotFound(IndexError) if it doesn't find any ticker
    ValueError if char is not None, or an ascii letter or digit
    '''
    pages = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    if char is None:

        papeis = []
        futures_list = []
        with futures.ThreadPoolExecutor(max_workers=15) as executor:
            for c in pages:
                future = executor.submit(get_tickers, c)
                futures_list.append(future)

        for future in futures_list:
            try:
                papeis += future.result()
            except DataNotFound:
                continue

        return papeis

    elif len(char) != 1 or not char.upper() in pages:
        raise ValueError(
            'Variable char should be an ascii letter, digit or None')

    char = char.upper()
    baseurl = 'https://br.advfn.com/bolsa-de-valores/bovespa/{}'
    html_src = requests.get(baseurl.format(char)).text
    dfs = pd.read_html(html_src)
    if len(dfs) != 9 or dfs[0].empty:
        raise DataNotFound('Couldn\'t find any ticker for that character')
    return list(dfs[0].iloc[:, 1])


def get_fundamentos(ticker, year=None, quarter=None,
                    dfs=False, reverse=False, threads=True):
    ''' Get fundamental data for one brazilian stock enlisted on ADVFN website.

    NOTE: Values are in thousands!

    :Arguments:

    ticker[str]:
        Ticker to download data from
    year[int] (2005 - today):
        Year to download data from. If None, downloads maximum range.
        Default is None
    quarter[int] (1 - 4):
        Quarter to download data from. If None, downloads annual data.
        Default is None.
    dfs[bool]:
        If true, the function returns a dict of DataFrames, in which each key is a separated topic of indicators:
            'valor_de_mercado': market_value,
            'resultado': result,
            'patrimonio': net worth,
            'caixa': cash,
            'divida': debt,
            'liquidez_e_solvencia': solvency and liquidy,
            'fluxo_de_caixa': cash flows,
            'investimentos': investments,
            'dividendo': dividends
        Default is False
    reverse[bool]:
        If downloading multiple years, whether they should be sorted reversely inside the DataFrame(s)
        Default is False
    threads[bool]:
        Whether it should download data using multiple threads.
        Default is true [highly recommended]

    :Raises:

    ValueError if the argument year is invalid
    DataNotFound(IndexError) if there's no data for that specific ticker or year

    :Returns:

    A pandas DataFrame, if dfs = False
    or
    A python dictionary, if dfs = True
    '''
    if year is None:
        years = [x for x in range(2005, date.today().year + 1)]
        annual_dfs = []

        # Recursive search
        if threads:

            futures_list = []
            with futures.ThreadPoolExecutor(max_workers=15) as executor:
                for year in years:
                    future = executor.submit(
                        get_fundamentos, ticker, year, quarter, dfs)
                    futures_list.append(future)
            for future in futures_list:
                try:
                    annual_dfs.append(future.result())
                except DataNotFound:
                    continue
        else:

            for year in years:
                try:
                    annual_dfs.append(get_fundamentos(
                        ticker, year, quarter, dfs))
                except DataNotFound:
                    continue

        if not dfs:
            df = pd.concat(annual_dfs, axis=1)
            df.dropna(how='all', inplace=True)
            return df.reindex(sorted(df.columns, reverse=reverse), axis=1)

        _dfs = {k: pd.concat([dfs[k] for dfs in annual_dfs], axis=1)
                for k in annual_dfs[0]}

        for k, df in _dfs.items():
            _dfs[k] = df.dropna(how='all').reindex(
                sorted(df.columns, reverse=reverse), axis=1)

        return _dfs

    if year > int(date.today().year):
        raise ValueError(f'Data inválida: {year}')

    str_tri = {
        1: 'primeiro-trimestre', 2: 'segundo-trimestre',
        3: 'terceiro-trimestre', 4: 'quarto-trimestre',
        None: None
    }

    baseurl = 'https://br.advfn.com/bolsa-de-valores/bovespa/{0}/fundamentos/individualizado/{1}/{2}'
    html_src = requests.get(baseurl.format(
        ticker, year, str_tri[quarter])).text

    _dfs = pd.read_html(html_src, index_col=0, decimal=',', thousands='.')

    if len(_dfs) < 9:
        raise DataNotFound(f'Couldn\'t find any data for {ticker} on {year}')

    _dfs = _dfs[:9]

    for i, df in enumerate(_dfs):
        _dfs[i] = df.iloc[:, [0]].applymap(convert_type)
        _dfs[i].index.name = ticker.upper()

    if dfs:
        return {
            'valor_de_mercado': _dfs[0],
            'resultado': _dfs[1],
            'patrimonio': _dfs[2],
            'caixa': _dfs[3],
            'divida': _dfs[4],
            'liquidez_e_solvencia': _dfs[5],
            'fluxo_de_caixa': _dfs[6],
            'investimentos': _dfs[7],
            'dividendo': _dfs[8]
        }

    return pd.concat(_dfs)
