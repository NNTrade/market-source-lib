# Library to get stock quotes and indicators
## Glossary
- candle - container with data which describes, stock quotes changes in timinterval
  - datetime|start_date_time - time when candle opened
  - open - price when candle open
  - high - max price in candle time interval
  - low - min price in candle time interval 
  - close - price when candle close
  - volume - amount of trades in candle
- step_timeframe|step_tf|stf - interval of time when candle will recalculate
- timeframe|tf - interval of time which contain in one candle

## How to use
### Import to pip
NNTrade.source.market @ git+https://git@github.com/NNTrade/market-source-lib.git#egg=NNTrade.source.market

### QyoteSource
[Package]("./src/quotes/__init__.py")
1. Создаем вспомогательные объекты
1.1. [AbsCacheQuote](#cachestorage) - хранилище кэша
1.2. [AbsStockQuoteClient](#клиент-получения-исходных-данных) - источник базовых котировок

2. Инициализация
```python
from NNTrade.source.market.quotes import QuoteSource
cq = AbsCacheQuote()
sqc = AbsStockQuoteClient()
qs = QuoteSource(imqc,sqc)
```

3. Получение данных
```python
qs.get("EURUSD", TimeFrame.m1, date(2021, 4, 2), date(2021, 4, 4))
```

### IndicatorSource
[Package]("./src/indicators/__init__.py")
1. Создаем вспомогательные объекты
1.1. [QuoteSource](#qyotesource) - источник котировок
1.2. [AbsCacheIndicator](#cachestorage) - хранилище кэша

2. Инициализация
```python
from NNTrade.source.market.indicators import IndicatorSource
qs = QuoteSource(...)
ci = AbsCacheIndicator()
inds = IndicatorSource(qs,ci)
```

3. Описываем параметры индикатора
NNTrade.indicators @ git+https://git@github.com/NNTrade/IndicatorFactory.git#egg=NNTrade.indicators

4. Запрашиваем индикатор 
```python
inds.get("EURUSD", TimeFrame.H, MASettingsBuilder.create_sma_setting(2))
```

### CacheStorage
#### Базовые классы
[Package]('./src/cache/__init__.py')
- [AbsCache]("./src/cache/abs_cache.py") - контейнер с кэшем котировок и индикаторов
- [AbsCacheQuote]("./src/cache/abs_cache_quote.py") - кеш котировок
- [AbsCacheIndicator]("src/cache/abs_cache_indicator.py") - кэш индикаторов

#### In Memory 
[Package]('./src/cache/in_memory/__init__.py')
Хранение рассчитанных данных в памяти. Подоходит только для тестов, небольших объемов данных или когда кеш не нужно сохранять между инстанциями источника

```python
from NNTrade.source.market.cache.in_memory import InMemoryCache
imc = InMemoryCache()
```

#### File cahce
[Package]('./src/cache/filecache/__init__.py')
Хранение рассчитанных данных в файловой системе.

```python
from NNTrade.source.market.cache.filecache import FileCache
imc = FileCache("Path_to_cache_folder")
```

### Клиент получения исходных данных
[Package]('./src/client/__init__.py')

#### абстракция CSV клиент
[Py file]("./src/client/quote_source_client_csv.py")
- QuoteSourceClientCSV - реализует клиент через CSV файл

##### Finam CSV client
[Py file]("./src/client/quote_source_client_csv.py")
- QuoteSourceClientFinamCSV - реализация клиента для csv файлов Finam

```python
from NNTrade.source.market.client import QuoteSourceClientFinamCSV
qsc = QuoteSourceClientFinamCSV("Path_to_folder_with_csv")
```