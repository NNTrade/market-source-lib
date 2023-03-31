from abc import ABC
from .abs_cache_indicator import AbsCacheIndicator
from .abs_cache_quote import AbsCacheQuote
from logging import getLogger

class AbsCache(ABC):
  def __init__(self) -> None:
    super().__init__()
    self._logger = getLogger("AbsCache")
    
  @property
  def quote(self)->AbsCacheQuote:
    ...

  @property
  def indicator(self)->AbsCacheIndicator:
    ...