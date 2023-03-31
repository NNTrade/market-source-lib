from .. import AbsCacheQuote, TimeFrame, pd, date
from ..base_func import filter_df
from typing import Dict


class InMemoryQuoteCache(AbsCacheQuote):
  def __init__(self) -> None:
    self.__stock_tf_df_dict: Dict[str, Dict[TimeFrame, pd.DataFrame]] = {}
    self.__stock_tf_tf_df_dict: Dict[str,
                                     Dict[TimeFrame, Dict[TimeFrame, pd.DataFrame]]] = {}
    super().__init__()

  def _save_stock_quotes(self, stock: str, timeframe: TimeFrame, quotes_df: pd.DataFrame):
    tf_df_dict = self.__stock_tf_df_dict.pop(stock, {})
    tf_df_dict[timeframe] = quotes_df
    self.__stock_tf_df_dict[stock] = tf_df_dict

  def _load_stock_quotes(self, stock: str, timeframe: TimeFrame, from_date: date = None, till_date: date = None) -> pd.DataFrame:
     return filter_df(self.__stock_tf_df_dict[stock][timeframe], from_date, till_date)

  def _stock_quotes_is_exist(self, stock: str, timeframe: TimeFrame) -> bool:
    if stock not in self.__stock_tf_df_dict.keys():
      return False
    if timeframe not in self.__stock_tf_df_dict[stock].keys():
      return False
    return True

  def save_aggregated_stock_quotes(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, quotes_df: pd.DataFrame):
      tf_tf_df_dict = self.__stock_tf_tf_df_dict.pop(stock, {})
      tf_df_dict = tf_tf_df_dict.pop(timeframe_base, {})

      tf_df_dict[timeframe_target] = quotes_df

      tf_tf_df_dict[timeframe_base] = tf_df_dict
      self.__stock_tf_tf_df_dict[stock] = tf_tf_df_dict

  def load_aggregated_stock_quotes(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, from_date: date = None, till_date: date = None) -> pd.DataFrame:
      return filter_df(self.__stock_tf_tf_df_dict[stock][timeframe_base][timeframe_target], from_date, till_date)

  def aggregated_stock_quotes_is_exist(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame) -> bool:
    if stock not in self.__stock_tf_tf_df_dict.keys():
      return False
    if timeframe_base not in self.__stock_tf_tf_df_dict[stock].keys():
      return False
    if timeframe_target not in self.__stock_tf_tf_df_dict[stock][timeframe_base].keys():
      return False
    return True
