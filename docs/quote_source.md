# Descripction
Main tool to get quotes

# Dependency
1. [AbsCacheQuote](#cachestorage) - chache storage
2. [AbsStockQuoteClient](#absstockquoteclient) - source to get basic stock quotes

# Example
```python
from NNTrade.source.market.quotes import QuoteSource
cq = AbsCacheQuote()
sqc = AbsStockQuoteClient()
qs = QuoteSource(cq,sqc)
qs.get("EURUSD", TimeFrame.m1, date(2021, 4, 2), date(2021, 4, 4))
```