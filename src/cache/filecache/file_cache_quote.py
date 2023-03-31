from ..base_func import filter_df
from .basic_func import join_cache_path, save_df,load_df,get_file_path_csv,join_cache_path
from ..abs_cache_quote import AbsCacheQuote, TimeFrame, pd, date
from NNTrade.common import VOLUME
import os

class FileCacheQuote(AbsCacheQuote):
  def __init__(self, cache_folder:str) -> None:
    """_summary_
    File structure
    - Cache_folder
      - {stock} (__get_stock_folder)
        - {timeframe.full_name()} (__get_timeframe_folder)
          - quote.csv (__get_stock_quotes_file_path)
          - aggregated 
            - {timeframe.full_name()} (__get_aggregated_folder)
              - quote.csv (__get_aggregated_stock_quotes_file_path)

    Args:
        cache_folder (str): _description_

    Raises:
        Exception: _description_
    """
    super().__init__()
    self.__cache_folder = cache_folder
    if not (os.path.exists(self.__cache_folder)):
      raise Exception(f"Folder {self.__cache_folder} doesn't exist. Create cache folder")
    self.__logger = self._logger.getChild("FileCacheQuote")


  def __get_quotes_file(self,cache_folder:str)->str:
    return get_file_path_csv(cache_folder, "quote")
  
  def __get_stock_folder(self, stock)->str:
    return join_cache_path(self.__cache_folder, stock)

  def __get_timeframe_folder(self, stock, timeframe: TimeFrame)->str:
    return join_cache_path(self.__get_stock_folder(stock), timeframe.full_name())

  def __get_stock_quotes_file_path(self, stock:str, timeframe: TimeFrame)->str:
    cache_folder = self.__get_timeframe_folder(stock, timeframe)
    return self.__get_quotes_file(cache_folder)

  def _save_stock_quotes(self, stock:str, timeframe: TimeFrame, quotes_df:pd.DataFrame):
    file_path = self.__get_stock_quotes_file_path(stock, timeframe)
    save_df(file_path, quotes_df)

  def _load_stock_quotes(self, stock:str, timeframe: TimeFrame, from_date:date = None, till_date:date = None)->pd.DataFrame:
    file_path = self.__get_stock_quotes_file_path(stock, timeframe)
    df = load_df(file_path)
    df[VOLUME] = df[VOLUME].astype(float)
    return filter_df(df, from_date, till_date)    

  def _stock_quotes_is_exist(self, stock:str, timeframe: TimeFrame)->bool:
    file_path = self.__get_stock_quotes_file_path(stock, timeframe)
    return os.path.exists(file_path)

  def __get_aggregated_folder(self, stock, timeframe_base: TimeFrame, timeframe_target:TimeFrame)->str:
    agr_dir = join_cache_path(self.__get_timeframe_folder(stock, timeframe_base), "aggregated")
    return join_cache_path(agr_dir, timeframe_target.full_name())

  def __get_aggregated_stock_quotes_file_path(self, stock:str, timeframe_base: TimeFrame, timeframe_target:TimeFrame)->str:
    cache_folder = self.__get_aggregated_folder(stock, timeframe_base, timeframe_target)
    return self.__get_quotes_file(cache_folder)
    
  def save_aggregated_stock_quotes(self, stock:str, timeframe_base: TimeFrame, timeframe_target:TimeFrame, quotes_df:pd.DataFrame):
    file_path = self.__get_aggregated_stock_quotes_file_path(stock, timeframe_base, timeframe_target)
    save_df(file_path, quotes_df)
    
  def load_aggregated_stock_quotes(self, stock:str, timeframe_base: TimeFrame, timeframe_target:TimeFrame, from_date:date = None, till_date:date = None)->pd.DataFrame:
    file_path = self.__get_aggregated_stock_quotes_file_path(stock, timeframe_base, timeframe_target)
    df = load_df(file_path)
    df[VOLUME] = df[VOLUME].astype(float)
    return filter_df(df, from_date, till_date)    
  
  def aggregated_stock_quotes_is_exist(self, stock:str, timeframe_base: TimeFrame, timeframe_target:TimeFrame)->bool:
    file_path = self.__get_aggregated_stock_quotes_file_path(stock, timeframe_base, timeframe_target)
    return os.path.exists(file_path)