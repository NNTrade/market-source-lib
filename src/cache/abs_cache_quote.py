from abc import ABC, abstractmethod
import pandas as pd
from NNTrade.common import TimeFrame
from datetime import date
from logging import getLogger

class AbsCacheQuote(ABC):
  def __init__(self) -> None:
    super().__init__()
    self._logger = getLogger("AbsCacheQuote")
    
  def save_stock_quotes(self, stock:str, timeframe: TimeFrame, quotes_df:pd.DataFrame, timeframe_target:TimeFrame = None):
    if timeframe_target is None or timeframe == timeframe_target:
      self._save_stock_quotes(stock, timeframe, quotes_df)
    else:
      self.save_aggregated_stock_quotes(stock, timeframe, timeframe_target, quotes_df)

  @abstractmethod
  def _save_stock_quotes(self, stock:str, timeframe: TimeFrame, quotes_df:pd.DataFrame):
    ...

  def load_stock_quotes(self, stock:str, timeframe: TimeFrame, from_date:date = None, till_date:date = None, timeframe_target:TimeFrame = None)->pd.DataFrame:
    if timeframe_target is None or timeframe == timeframe_target:
      return self._load_stock_quotes(stock, timeframe, from_date, till_date)
    else:
      return self.load_aggregated_stock_quotes(stock, timeframe, timeframe_target,from_date, till_date)

  @abstractmethod
  def _load_stock_quotes(self, stock:str, timeframe: TimeFrame, from_date:date = None, till_date:date = None)->pd.DataFrame:
     ...
  
  def stock_quotes_is_exist(self, stock:str, timeframe: TimeFrame,timeframe_target:TimeFrame = None)->bool:
    if timeframe_target is None or timeframe == timeframe_target:
      return self._stock_quotes_is_exist(stock, timeframe)
    else:
      return self.aggregated_stock_quotes_is_exist(stock,timeframe, timeframe_target)

  @abstractmethod
  def _stock_quotes_is_exist(self, stock:str, timeframe: TimeFrame)->bool:
    ...

  @abstractmethod
  def save_aggregated_stock_quotes(self, stock:str, timeframe_base: TimeFrame, timeframe_target:TimeFrame, quotes_df:pd.DataFrame):
     ...
    
  @abstractmethod
  def load_aggregated_stock_quotes(self, stock:str, timeframe_base: TimeFrame, timeframe_target:TimeFrame, from_date:date = None, till_date:date = None)->pd.DataFrame:
     ...

  @abstractmethod
  def aggregated_stock_quotes_is_exist(self, stock:str, timeframe_base: TimeFrame, timeframe_target:TimeFrame)->bool:
    ...
