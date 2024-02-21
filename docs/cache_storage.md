# Description
Service to stock cache

# Base class
```python
from NNTrade.source.market.cache import AbsCacheQuote
```

# Realizaition
1. [FileCache](#file-cache) 
2. [InMemoryCache](#in-memory)

## File cache
store cache in file system

### Dependency
- cache_folder - path to store cache

### Example
```python
from NNTrade.source.market.cache.filecache import FileCache
imc = FileCache("Path_to_cache_folder")
```

## In Memory
store cach in RAM

### Example
```python
from NNTrade.source.market.cache.in_memory import InMemoryCache
imc = InMemoryCache()
```