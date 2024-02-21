from ..cache.abs_cache_quote import AbsCacheQuote
from ..quotes import DfCondenser
from .abs_quote_source_client import AbsStockQuoteClient, TimeFrame, date, List, Tuple
from ..common import StockQuoteContainer, Candle
import pandas as pd
from typing import Dict, Callable, List
import os
from logging import getLogger
import NNTrade.common.candle_col_name as col
import pandas as pd
from datetime import datetime
from ..tools.progress_log import ProgressLog
import NNTrade.common.candle_col_name as col_name
from ..tools.filter_df import filter_df
from collections import defaultdict

class QuoteSourceClientCSV(AbsStockQuoteClient):
   def __init__(self, base_path: str):
      """_summary_

      Args:
            base_path (str): path to folder with csv files
      """
      self.file_list: Dict[str, Dict[TimeFrame, str]] = {}
      self.base_path = base_path
      self.logger = getLogger("QuoteSourceClientCSV")

   def add_file(self, file_name: str, stock: str, timeframe: TimeFrame):

      file_path = os.path.join(self.base_path, file_name)
      if not os.path.exists(file_path):
         raise Exception(f"File with path {file_path} not exist")

      if stock not in self.file_list.keys():
         self.file_list[stock] = {}

      self.file_list[stock][timeframe] = file_name
      self.logger.info("File %s to stock %s timeframe %s added to client",
                       file_path, stock, timeframe.full_name())

   def get(self, stock: str, timeframe: TimeFrame, from_date: date = None, untill_date: date = None) -> pd.DataFrame:
      if stock not in self.file_list.keys():
         raise Exception("Stock not register in client")
      else:
         stock_tf_dict = self.file_list[stock]

      if timeframe not in stock_tf_dict.keys():
         raise Exception("Stock timeframe not register in client")

      file_path = os.path.join(self.base_path, stock_tf_dict[timeframe])
      self.logger.info("Load file %s", file_path)

      csv_df = self.read_csv(file_path)
      return filter_df(csv_df, from_date, untill_date)

   def read_csv(self, file_path: str) -> pd.DataFrame:
      ...

   def stocks(self) -> Dict[TimeFrame, List[str]]:
      # Initialize a defaultdict to group symbols by TimeFrame
      output_dict: Dict[TimeFrame, List[str]] = defaultdict(list)

      # Iterate through the input dictionary
      for symbol, timeframes in self.file_list.items():
         for timeframe, value in timeframes.items():
            # Append the symbol to the corresponding TimeFrame list
            output_dict[timeframe].append(symbol)

      # Convert the defaultdict to a regular dictionary
      return dict(output_dict)
            
class QuoteSourceClientFinamCSV(QuoteSourceClientCSV):
    def __init__(self, base_path: str):
       super().__init__(base_path)

    def read_csv(self,file_path:str)->pd.DataFrame:
        self.logger.info("start reading csv")
        df = pd.read_csv(file_path, sep=";", decimal=".", header=0,dtype={"<DATE>":str,"<TIME>":str})
        
        self.logger.info("start parsing csv DataFrame")
        df["dt_str"] = df["<DATE>"].astype(str) +df["<TIME>"].astype(str)
        df[col_name.INDEX] = pd.to_datetime(df["dt_str"], format="%Y%m%d%H%M%S")
        df =    df.rename(columns=
                       {"<OPEN>":col_name.OPEN,
                        "<HIGH>":col_name.HIGH,
                        "<LOW>":col_name.LOW,
                        "<CLOSE>":col_name.CLOSE,
                        "<VOL>":col_name.VOLUME })\
                  .set_index(col_name.INDEX)
        self.logger.info("finish parsing csv DataFrame")
        return df[[col_name.OPEN,col_name.HIGH,col_name.LOW,col_name.CLOSE,col_name.VOLUME]]

class QuoteSourceClientDefaultCSV(QuoteSourceClientCSV):
   def __init__(self, base_path: str, sep = ",", decimal = "."):
      super().__init__(base_path)
      self.sep = sep
      self.decimal = decimal

   def read_csv(self,file_path:str)->pd.DataFrame:
      self.logger.info("start reading csv")
      df = pd.read_csv(file_path, decimal=self.decimal, sep=self.sep, header=0, index_col=0)
      df.index = pd.DatetimeIndex(df.index)
      self.logger.info("finish parsing csv DataFrame")
      return df

       
    