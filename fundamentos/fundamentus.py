import requests
import pandas as pd
from datetime import date
from .utils import convert_type, DataNotFound


def get_tickers():
    '''Downloads tickers' codes from fundamentus website
    '''
    html_src = requests.get('http://fundamentus.com.br/detalhes.php').text
    return pd.read_html(html_src)[0].iloc[:, 0]


def get_fundamentos(ticker, dfs=False):
    ''' Get fundamental data for one brazilian stock enlisted on fundamentus website.

    NOTE: Values are in thousands!

    :Arguments:

    ticker[str]:
        Ticker to download data from
    dfs[bool]:
        If true, the function returns a dict of DataFrames, in which each key is a separated topic of indicators:
            'info': general information,
            'indicadores': some fundamental indicators,
            'balanço': balance sheet,
            'dre': results
        Default is False

    :Raises:

    DataNotFound(IndexError) if there's no data for that specific ticker

    :Returns:

    A pandas DataFrame, if dfs = False
    or
    A python dictionary, if dfs = True
    '''
    response = requests.get(
        f'https://www.fundamentus.com.br/detalhes.php', params={'papel': ticker})

    tabelas = pd.read_html(response.text, decimal=',', thousands='.')
    if len(tabelas) < 5:
        raise DataNotFound('Couldn\'t find any data for {ticker}')
    df = pd.DataFrame()
    for tabela in tabelas:
        novas_linhas = [[item for item in linha] for linha in tabela.values]
        for i in range(0, 6, 2):
            try:
                s = slice(i, i + 2)
                tmp_df = pd.DataFrame(novas_linhas).iloc[:, s].set_index(i)
                tmp_df.columns = [date.today().year]
                df = pd.concat(
                    [df, tmp_df])
            except KeyError:
                break

    df = df.applymap(convert_type)

    # Cleaning the DataFrame
    df = df.iloc[:-3]
    df.drop(df.loc['Dia':'?P/L'].iloc[:-1].index, inplace=True)
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    df.index = [idx.replace('?', '') for idx in df.index]
    for lbl, row in df.iterrows():
        if lbl == row.values:
            df.drop(lbl, inplace=True, errors='ignore')

    if dfs:
        return {
            'info': df.loc['Papel':'Nro. Ações'],
            'indicadores': df.loc['P/L':'Ativo'].iloc[:-1],
            'balanço': df.loc['Ativo':'Patrim. Líq'],
            'dre': df.loc['Patrim. Líq':].iloc[1:]
        }
    return df
