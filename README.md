# fundamentos

Download Bovespa Stock Market fundamentals.

`fundamentos` is a tiny, threaded, package that allows you to quickly download historical fundamentals of the Brazilian Stock Market, both annualy and quarterly.

The default source for searching for historical data is [ADVFN](https://br.advfn.com/bolsa-de-valores/bovespa "ADVFN") but it also features [fundamentus](https://www.fundamentus.com.br/detalhes.php "fundamentus") for current fundamentals.

## Usage

### The get_fundamentos function

The `get_fundamentos` is the main function of the package. From default, it downloads data from advfn

```python
import fundamentos as fos

# Downloads all historical fundamentals
# to AmBev SA, annualy
df = fos.get_fundamentos('ABEV3')

# Downloads all historical fundamentals
# to Itaú Unibanco SA on third quarters
df = fos.get_fundamentos('ITUB4', quarter=3)

# Downloads data from first quarter of
# 2013 to Banco Bradesco
df = fos.get_fundamentos('BBDC4', year=2013, quarter=1)
```
Besides returning a single `pandas.DataFrame` with all the data, it also features returning a python `dictionary` of `DataFrames` in which each key represents a different category of economic indicators, so that they can be accessed separately. Its format should be something like this:

```python
import fundamentos as ftos

dfs = ftos.get_fundamentos('LREN3', dfs=True)
print(dfs)

# Expected Output:
# {
#     'valor_de_mercado': market_value_df,
#     'resultado': result_df,
#     'patrimonio': net_worth_df,
#     'caixa': cash_df,
#     'divida': debt_df,
#     'liquidez_e_solvencia': solvency_and_liquidy_df,
#     'fluxo_de_caixa': cash_flows_df,
#     'investimentos': investments_df,
#     'dividendo': dividends_df
# }
```
So, for example, cash indicators could be printed separately with
```python
print(dfs['caixa'])
```

### The get_tickers function

The `get_tickers` function simply returns a list with all the tickers currently listed on [ADVFN website](https://br.advfn.com/bolsa-de-valores/bovespa/A "advfn tickers").

```python
import fundamentos as ftos

tickers = ftos.get_tickers()
```

### The fundamentus module

The `fundamentus` module has the same functions of the main module, but it doesn't feature historical data. The reason why I added this module to the package is because, sometimes, [fundamentus](https://www.fundamentus.com.br/detalhes.php "fundamentus") happens to be more complete than advfn.

In order to use it, you have to import it from the main module

```python
from fundamentos import fundamentus as ftus

# Downloads fundamentals of Lojas Renner SA
df = ftus.get_fundamentos('LREN3')

# Downloads tickers currently listed
# on fundamentus website
tickers = ftus.get_tickers()
```

### The python help function

For more information about what each function does, use
```python
help(function)
```
