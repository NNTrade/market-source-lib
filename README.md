# Glossary
- candle - container with data which describes, stock quotes changes in timinterval
  - datetime|start_date_time - time when candle opened
  - open - price when candle open
  - high - max price in candle time interval
  - low - min price in candle time interval 
  - close - price when candle close
  - volume - amount of trades in candle
- step_timeframe|step_tf|stf - interval of time when candle will recalculate
- timeframe|tf - interval of time which contain in one candle

# Import to pip
NNTrade.source.market @ git+https://git@github.com/NNTrade/market-source-lib.git#egg=NNTrade.source.market

# Components
1. [QuoteSource](./docs/quote_source.md) - main tool to get quotes
2. [Stock quote client](./docs/stock_quote_client.md) - client to get stock quotes
3. [Cache storage](./docs/cache_storage.md) - service to stock cache data

# Quick start
1. Choose which [Stock quote client](./docs/stock_quote_client.md) will you use
2. Choose which [Cache storage](./docs/cache_storage.md) will you use
3. Init them
```python
from NNTrade.source.market.client import AbsStockQuoteClient
from NNTrade.source.market.cache import AbsCacheQuote
cq = AbsCacheQuote()
sqc = AbsStockQuoteClient()
```
4. Init [QuoteSource](./docs/quote_source.md)
```python
qs = QuoteSource(cq,sqc)
```
5. Call required stock
```python
qs.get("EURUSD", TimeFrame.m1, date(2021, 4, 2), date(2021, 4, 4))
```


