import requests
import xlrd
import pandas as pd
import io
import os
from zipfile import ZipFile
from .utils import convert_type, DataNotFound, get_headers


def get_tickers():
    '''Downloads tickers' codes from fundamentus website

    :Returns:

    A pandas DataFrame with three columns:

    Papel (Ticker),
    Nome Comercial (Trade Name),
    Razão Social (Corporate Name)
    '''
    html_src = requests.get(
        'http://fundamentus.com.br/detalhes.php', headers=get_headers()).text
    return pd.read_html(html_src)[0]


def _get_sheets(ticker, quarterly, ascending):
    '''Downloads sheets from fundamentus website.

    available sheets:
        \'Bal. Patrim.\' for balance sheet
        \'Dem. Result.\' for income statement
    '''

    ticker = ticker.upper()

    # Apparently fundamentus is blocking requests library's standard user-agent
    # To solve this problem, I'm generating random user-agents

    r = requests.get('https://www.fundamentus.com.br/balancos.php',
                     params={'papel': ticker},
                     headers=get_headers())

    SID = r.cookies.values()[0]

    response_sheet = requests.get(
        'https://www.fundamentus.com.br/planilhas.php',
        params={'SID': SID}, headers=get_headers())

    if response_sheet.text.startswith('Ativo nao encontrado'):
        raise DataNotFound(
            f'Couldn\'t find any data for {ticker}')

    with io.BytesIO(response_sheet.content) as zip_bytes:
        with ZipFile(zip_bytes) as z:
            xls_bytes = z.read('balanco.xls')

    # Supress warnings
    wb = xlrd.open_workbook(file_contents=xls_bytes,
                            logfile=open(os.devnull, 'w'))

    dfs = {
        'Bal. Patrim.': pd.read_excel(wb, engine='xlrd',
                                      index_col=0,
                                      sheet_name='Bal. Patrim.'),
        'Dem. Result.': pd.read_excel(wb, engine='xlrd',
                                      index_col=0,
                                      sheet_name='Dem. Result.')
    }

    for sheet, df in dfs.items():

        # Cleaning the DataFrame
        df.columns = df.iloc[0, :]
        df = df.iloc[1:].T.applymap(convert_type)
        df.index.name = 'Data'
        df.columns.name = ticker
        df = df.loc[df.index.notnull()]
        df.index = pd.to_datetime(
            df.index, format='%d/%m/%Y')

        # Excluding empty columns (usually subtitles)
        df.dropna(axis=1, how='all', inplace=True)
        # Filling empty cells with 0
        df.fillna(0, inplace=True)

        if not quarterly:
            rows_to_drop = [x for x in df.index.year
                            if list(df.index.year).count(x) != 4]
            df = df.groupby(df.index.year).sum()
            df.drop(rows_to_drop, inplace=True)
            df.index = [str(x) for x in df.index]

        dfs[sheet] = df.sort_index(ascending=ascending).astype(int)

    return dfs


def get_balanco(ticker, quarterly=False, ascending=True, separated=True):
    '''Get the balance sheet for one brazilian stock listed on fundamentus website.

    NOTE: Values are in thousands!

    :Arguments:

    ticker[str]:
        Ticker to download data from
    quarterly[bool]:
        Whether to download quarterly or annualy data.
        Default is False.
    ascending[bool]:
        Whether the date index should be sorted ascendingly on the DataFrame
        Default is True
    separated[bool]:
        If True, the DataFrame will be hierarchically divided by super columns:
            \'Ativo Total\' (Total Assets),
            \'Ativo Circulante\' (Current Assets),
            \'Ativo Não Circulante\' (Non-current Assets),
            \'Passivo Total\' (Total Liabilities),
            \'Passivo Circulante\' (Current Liabilities),
            \'Passivo Não Circulante\' (Non-current Liabilities),
            \'Patrimônio Líquido\' (Net Worth)
        Default is True (highly recommended, as some infra columns are
        duplicated which could lead to confusion).

    :Raises:

    DataNotFound(IndexError) if there's no data available for that ticker

    :Returns:

    A pandas DataFrame
    '''

    df = _get_sheets(ticker, quarterly=quarterly,
                     ascending=ascending)['Bal. Patrim.']

    if separated:
        super_cols = [
            'Ativo Total',
            'Ativo Circulante',
            'Ativo Não Circulante',
            'Ativo Realizável a Longo Prazo',
            'Passivo Total',
            'Passivo Circulante',
            'Passivo Não Circulante',
            'Passivo Exigível a Longo Prazo',
            'Patrimônio Líquido'
        ]

        cols = list(df.columns)

        # Handling different balance sheets for banks and other companies
        if 'Ativo Não Circulante' in cols:
            super_cols.remove('Ativo Realizável a Longo Prazo')
        else:
            super_cols.remove('Ativo Não Circulante')

        if 'Passivo Não Circulante' in cols:
            super_cols.remove('Passivo Exigível a Longo Prazo')
        else:
            super_cols.remove('Passivo Não Circulante')

        idxs = [cols.index(x) for x in cols if x in super_cols]

        slices = [slice(idxs[i], idxs[i + 1])
                  if i < (len(idxs) - 1)
                  else slice(idxs[i], None)
                  for i, _ in enumerate(idxs)]

        tuples = []

        for s in slices:
            sup = super_cols.pop(0)

            # Renaming columns to standardize different companies' DataFrames
            if sup == 'Ativo Realizável a Longo Prazo':
                sup = 'Ativo Não Circulante'
            if sup == 'Passivo Exigível a Longo Prazo':
                sup = 'Passivo Não Circulante'

            for col in cols[s]:
                tuples.append((sup, col))

        df.columns = pd.MultiIndex.from_tuples(tuples)

    return df


def get_dre(ticker, quarterly=False, ascending=True):
    '''Get the income statement for one brazilian stock listed on fundamentus website.

    NOTE: Values are in thousands!

    :Arguments:

    ticker[str]:
        Ticker to download data from
    quarterly[bool]:
        Whether to download quarterly or annualy data.
        Default is False.
    ascending[bool]:
        Whether the date index should be sorted ascendingly on the DataFrame
        Default is True

    :Raises:

    DataNotFound(IndexError) if there's no data available for that ticker

    :Returns:

    A pandas DataFrame
    '''

    df = _get_sheets(ticker, quarterly=quarterly,
                     ascending=ascending)['Dem. Result.']

    return df
