from ..abs_cache import AbsCache, AbsCacheQuote, AbsCacheIndicator
from .in_memory_indicator import InMemoryIndicatorCache
from .in_memory_quote import InMemoryQuoteCache


class InMemoryCache(AbsCache):
  def __init__(self) -> None:
    super().__init__()
    self._quote = InMemoryQuoteCache()
    self._ind = InMemoryIndicatorCache()

  @property
  def quote(self) -> AbsCacheQuote:
    return self._quote

  @property
  def indicator(self) -> AbsCacheIndicator:
    return self._ind
