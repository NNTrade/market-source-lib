# Description 
Clients to get basic stock quotes

# Base class
```python
from NNTrade.source.market.client import AbsStockQuoteClient
```

# Realizaition
1. [QuoteSourceClientCSV](#csv-client-group) - realizations which get stock quotes from csv
    1. [QuoteSourceClientFinamCSV](#finam-csv-client) - realization to get stock quotes from finam csv files
2. [DataFrame client](#dataframe-client)

## CSV client group
realizations which get stock quotes from csv

### Finam CSV client
realization to get stock quotes from finam csv files

#### Dependency
- base_path - path to folder with csv files

#### Example
```python
from NNTrade.source.market.client.realization import QuoteSourceClientFinamCSV
qsc = QuoteSourceClientFinamCSV("Path_to_folder_with_csv")
```

## DataFrame client
Realization of client from data frame

### Example
```python
from NNTrade.source.market.client.realization import DataFrameClient
dfc = DataFrameClient()
```