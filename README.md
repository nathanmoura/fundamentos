
# fundamentos

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/NathanMoura/fundamentos/blob/master/LICENSE.txt)
[![PyPI version](https://badge.fury.io/py/fundamentos.svg)](https://badge.fury.io/py/fundamentos)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/fundamentos.svg)](https://pypi.python.org/pypi/fundamentos/)
[![Downloads](https://pepy.tech/badge/fundamentos)](https://pepy.tech/project/fundamentos)
[![GitHub stars](https://img.shields.io/github/stars/NathanMoura/fundamentos.svg?style=social&label=Star&maxAge=60)](https://github.com/NathanMoura/fundamentos/stargazers/)


`fundamentos` is a tiny, threaded, package that allows you to quickly download historical data from the Brazilian Stock Market, both annualy and quarterly.

The sources from where it downloads data are
- [ADVFN](https://br.advfn.com/bolsa-de-valores/bovespa "ADVFN") for [fundamentals](#the-get_fundamentos-function)
- [fundamentus](https://www.fundamentus.com.br/detalhes.php "fundamentus") for [balance sheets](#the-get_balanco-function) and [income statements](#the-get_dre-function).

## Instalation

Install `fundamentos` using pip:

```sh
$ pip install fundamentos
```


## Quick Start

### The get_fundamentos function

Get some fundamentals!

From default, the results are grouped by year, but if you want to, you can specify a quarter to download data from. Additionally, if you want to be even more specific, you can specify the year and the quarter from which you want to download.

```python
import fundamentos as ftos

# Downloading data from Itaú Unibanco SA

# Downloads all historical fundamentals, annually
df = ftos.get_fundamentos('ITUB4')

# Downloads all historical fundamentals on third quarters
df = ftos.get_fundamentos('ITUB4', quarter=3)

# Downloads fundamentals from first quarter of 2013
df = ftos.get_fundamentos('ITUB4', year=2013, quarter=1)
```

The output is a `pandas.DataFrame` and its columns are hierarchically ordered by topics, which makes it easier to filter the data. However, if you need a regular index of columns you can specify that by passing `separated=False` as a parameter.

Topics are


- Mercado - _Market_
- Resultados - _Income_
- Patrimônio - _Net Worth_
- Caixa - _Cash_
- Dívida - _Debt_
- Liquidez e Solvência - _Solvency and Liquidity_
- Fluxo de Caixa - _Cash Flow_
- Investimentos - _Investments_
- Dividendos - _Dividends_


So, for example, cash indicators could be accessed separately with

```python
df['Caixa']
```

**quick tip:** _if you can't understand the acronyms of the indicators you can use `ftos.get_schema()`, which is a function that returns a `pandas.DataFrame` with the full name versions of each indicator_

### The get_tickers function

This function returns a `pandas.DataFrame` with every company listed on the Brazilian Stock Market, their respective corporate names and codes

```python
import fundamentos as ftos

tickers = ftos.get_tickers()
```

### The get_balanco function

Get some balance sheets!

From default, the results are grouped by year, but if you want to, you can download them quarterly by using `quarterly=True`

```python
import fundamentos as ftos

# Downloads all historical balance sheets, annually
df = ftos.get_balanco('ITUB4')

# Downloads all historical balance sheets, quarterly
df = ftos.get_balanco('ITUB4', quarterly=True)
```
As with `get_fundamentos`, the output is also a `pandas.DataFrame` with columns hierarchically ordered by topics. You can also deactivate that by passing `separated=False` as an argument.

Topics are

- Ativo Total - _Total Assets_
- Ativo Circulante - _Current Assets_
- Ativo Não Circulante - _Non-current Assets_
- Passivo Total - _Total Liabilities_
- Passivo Circulante - _Current Liabilities_
- Passivo Não Circulante - _Non-current Liabilities_
- Patrimônio Líquido - _Net Worth_

### The get_dre function

Get some income statements!

The parameters are pretty similar to thoses in `get_balanco`

```python
import fundamentos as ftos

# Downloads all historical income statements, annually
df = ftos.get_dre('ITUB4')

# Downloads all historical income statements, quarterly
df = ftos.get_dre('ITUB4', quarterly=True)
```

### The python help function

I tried to be as descriptive as I could on the `docstrings`, so if you need more information about what each function does you can use

```python
help(function)
```


## License

`fundamentos` is distributed under the **MIT License**. See the [LICENSE.txt](https://github.com/NathanMoura/fundamentos/blob/master/LICENSE.txt) file in the release for details.
