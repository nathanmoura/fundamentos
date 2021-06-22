import requests
import pandas as pd
from .utils import convert_type, DataNotFound, get_headers
from concurrent import futures
from datetime import date
from calendar import monthrange


schema = {
    'Quantidade de Ações ON': 'Quantidade de Ações ON',
    'Quantidade de Ações PN': 'Quantidade de Ações PN',
    'Última Cotação ON': 'Última Cotação ON',
    'Última Cotação PN': 'Última Cotação PN',
    'Valor de Mercado': 'Valor de Mercado',
    'Receita Líquida': 'Receita Líquida',
    'Price Sales Ratio (PSR)': 'PSR',
    'Resultado Bruto': 'Resultado Bruto',
    'Margem Bruta': 'Margem Bruta',
    'EBITDA': 'EBITDA',
    'Margem EBITDA': 'Margem EBITDA',
    'Preço / EBITDA': 'P/EBITDA',
    'EBIT': 'EBIT',
    'Margem EBIT': 'Margem EBIT',
    'Preço / EBIT': 'P/EBIT',
    'Lucro/Prejuízo Líquido': 'Lucro Líquido',
    'Preço / Lucro (P/L)': 'P/L',
    'Lucro por Ação (LPA)': 'LPA',
    'Ativo Total': 'Ativo Total',
    'Preço / Ativo (P/A)': 'P/Ativo',
    'Giro Ativos': 'Giro',
    'EBIT / Ativo': 'EBIT/Ativo',
    'Patrimônio Líquido': 'PL',
    'Retorno sobre PL (ROE)': 'ROE',
    'Valor Patrimonial por Ação (VPA)': 'VPA',
    'Preço / Valor Patrimonial por Ação (P/VPA)': 'P/VPA',
    '(Ativo - Patrimônio Líquido) / Patrimônio Líquido': '(A - PL)/PL',
    'Equity Multiplier (EM)': 'EM',
    'Disponibilidades': 'Disponibilidades',
    'Dinheiro em Caixa': 'Dinheiro em Caixa',
    'Aplicações Financeiras': 'Aplicações Financeiras',
    'Dívida Bruta': 'Dívida Bruta',
    'Dívida Bruta / Patrimônio Líquido': 'DB/PL',
    'Endividamento Financeiro': 'Endividamento Financeiro',
    'Dívida Líquida': 'Dívida Líquida',
    'Dívida Líquida / EBITDA': 'DL/EBITDA',
    'Enterprise Value (EV)': 'EV',
    'Enterprise Value / EBIT (EV/EBIT)': 'EV/EBIT',
    'Ativo Circulante': 'Ativo Circulante',
    'Ativo Não Circulante': 'Ativo Não Circulante',
    'Ativo Circulante Líquido': 'Ativo Circulante Líquido',
    'Preço / Ativo Circulante Líquido': 'P/ACL',
    'Passivo Circulante': 'Passivo Circulante',
    'Passivo Não Circulante': 'Passivo Não Circulante',
    'Liquidez Corrente': 'LC',
    'Liquidez Imediata': 'LI',
    'Capital de Giro': 'Capital de Giro',
    'Preço / Capital de Giro': 'P/Capital de Giro',
    'Dívida em Moeda Estrangeira': 'Dívida em Moeda Estrangeira',
    'Fluxo de Caixa Operacional (FCO)': 'FCO',
    'Fluxo de Caixa de Investimentos (FCI)': 'FCI',
    'Fluxo de Caixa de Financiamentos (FCF)': 'FCF',
    'Fluxo de Caixa Total (FCT)': 'FCT',
    'Fluxo de Caixa Livre (FCL)': 'FCL',
    'CAPEX': 'CAPEX',
    'Fluxo de Caixa Livre CAPEX': 'FCL CAPEX',
    'CAPEX / Fluxo de Caixa Operacional': 'CAPEX/FCO',
    'Fluxo de Caixa de Investimentos / Lucro Líquido': 'FCI/LL',
    'CAPEX / Lucro Líquido': 'CAPEX/LL',
    'Dividendos e Juros Sobre Capital Próprio Pagos': 'Dividendos e JCP',
    'Dividend Yield': 'DY',
    'Dividend Payout': 'Payout'
}


def get_schema():
    '''Get the schema used to abbreviate columns names on get_fundamentos DataFrame
    '''
    return (pd.DataFrame(schema.items(), columns=['Significado', 'Abreviação'])
            .set_index('Abreviação'))


def get_fundamentos(ticker, year=None, quarter=None,
                    separated=True, ascending=True, threads=True):
    '''Get fundamental data for one brazilian stock listed on ADVFN website.

    NOTE: Values are in thousands!

    Also, none of the data is in percentage scale.

    :Arguments:

    ticker[str]:
        Ticker to download data from
    year[int] (2007 - today):
        Year to download data from. If None, downloads maximum range.
        Default is None
    quarter[int] (1 - 4):
        Quarter to download data from. If None, downloads annual data.
        Default is None.
    separated[bool]:
        If True, the DataFrame will be hierarchically divided by super columns.
        Each super column is a different topic of economic indicators
            \'Mercado\' (Market),
            \'Resultados\' (Income),
            \'Patrimônio\'(Net Worth),
            \'Caixa\' (Cash),
            \'Dívida\' (Debt),
            \'Liquidez e Solvência\' (Solvency and Liquidity),
            \'Fluxo de Caixa\' (Cash Flow),
            \'Investimentos\' (Investments),
            \'Dividendos\' (Dividends)
        Default is True
    ascending[bool]:
        If downloading multiple years, whether they should be sorted ascendingly
         on the DataFrame
        Default is True
    threads[bool]:
        If downloading multiple years, whether to download data using multiple
         threads.
        Default is True (highly recommended)

    :Raises:

    ValueError if the argument year is invalid
    DataNotFound(IndexError) if there's no data available for that specific
     ticker or year

    :Returns:

    A pandas DataFrame, if dfs = False
    '''
    ticker = ticker.upper()

    if year is None:
        years = [x for x in range(2007, date.today().year + 1)]
        annual_dfs = []

        # Recursive search
        if threads:

            futures_list = []
            with futures.ThreadPoolExecutor(max_workers=15) as executor:
                for year in years:
                    future = executor.submit(
                        get_fundamentos, ticker, year, quarter, separated)
                    futures_list.append(future)
            for future in futures_list:
                try:
                    annual_dfs.append(future.result())
                except (DataNotFound, ValueError):
                    continue
        else:
            for year in years:
                try:
                    annual_dfs.append(get_fundamentos(
                        ticker, year, quarter, separated))
                except (DataNotFound, ValueError):
                    continue

        if not annual_dfs:
            raise DataNotFound(f'Couldn\'t find any data for \'{ticker}\'')

        df = pd.concat(annual_dfs)

        return df.sort_index(ascending=ascending)

    if year > int(date.today().year):
        raise ValueError(
            f'Year variable ca\'nt be higher than current year: {year}')

    str_tri = {
        1: 'primeiro-trimestre', 2: 'segundo-trimestre',
        3: 'terceiro-trimestre', 4: 'quarto-trimestre',
        None: None
    }

    baseurl = 'https://br.advfn.com/bolsa-de-valores/bovespa/{0}/fundamentos/individualizado/{1}/{2}'
    html_src = requests.get(baseurl.format(
        ticker, year, str_tri[quarter]), headers=get_headers()).text

    _dfs = pd.read_html(html_src, index_col=0, decimal=',', thousands='.')

    if len(_dfs) < 9:
        raise DataNotFound(
            f'Couldn\'t find any data for \'{ticker}\' on {year}')

    _dfs = _dfs[:9]

    for i, df in enumerate(_dfs):
        # Formating types and dropping entire NaN columns
        _dfs[i] = df.iloc[:, [0]].T.applymap(convert_type)
        _dfs[i].dropna(how='all', axis=1, inplace=True)

        if quarter:
            # Formating index column to be datetime
            _dfs[i].index = [f'{monthrange(year, quarter*3)[1]}/{quarter*3}/{x[3:]}'
                             for x in _dfs[i].index]
            _dfs[i].index = pd.to_datetime(_dfs[i].index,
                                           format='%d/%m/%Y')
        else:
            # Removing '*' from some years
            _dfs[i].index = [year if '*' not in year else year[:-2]
                             for year in _dfs[i].index]

        _dfs[i].columns = [schema[x] for x in _dfs[i].columns]
        _dfs[i].columns.name = ticker
        _dfs[i].index.name = 'Data'

    if separated:
        super_cols = [
            'Mercado', 'Resultados', 'Patrimônio', 'Caixa', 'Dívida',
            'Liquidez e Solvência', 'Fluxo de Caixa', 'Investimentos',
            'Dividendos',
        ]
        return pd.concat(_dfs, axis=1, keys=super_cols)

    return pd.concat(_dfs, axis=1)
