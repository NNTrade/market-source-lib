from ..cache.abs_cache_quote import AbsCacheQuote
from ..quotes import DfCondenser
from .abs_quote_source_client import AbsStockQuoteClient, TimeFrame, date
from ..common import StockQuoteContainer, Candle
import pandas as pd
from typing import Dict, Callable, List
import os
from logging import getLogger
import NNTrade.common.candle_col_name as col
import pandas as pd
from datetime import datetime


class QuoteSourceClientCSV(AbsStockQuoteClient):
    def __init__(self, base_path: str):
      """_summary_

      Args:
          path (str): path to folder with csv files
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
        self.logger.info("File %s to stock %s timeframe %s added to client", file_path, stock, timeframe.full_name())

    def get(self, stock: str, timeframe: TimeFrame, from_date: date = None, untill_date: date = None) -> StockQuoteContainer:
       if stock not in self.file_list.keys():
          raise Exception("Stock not register in client")
       else:
         stock_tf_dict = self.file_list[stock]
       
       if timeframe not in stock_tf_dict.keys():
          raise Exception("Stock timeframe not register in client")
       
       file_path = os.path.join(self.base_path, stock_tf_dict[timeframe])
       self.logger.info("Load file %s", file_path)

       candle_arr:List[Candle] = self.read_csv(file_path,from_date,untill_date)
       return StockQuoteContainer([candle for candle in candle_arr if (from_date is None or candle.datetime.date() >= from_date) and (untill_date is None or candle.datetime.date() < untill_date)])

    def read_csv(self,file_path:str, from_date: date=None, untill_date: date=None)->List[Candle]:
       ...
            
class QuoteSourceClientFinamCSV(QuoteSourceClientCSV):
    def __init__(self, base_path: str):
       super().__init__(base_path)
    def read_csv(self,file_path:str, from_date: date=None, untill_date: date=None)->List[Candle]:
        df = pd.read_csv(file_path, sep=";", decimal=".", header=0,dtype={"<DATE>":str,"<TIME>":str})
        c_arr =[]
        for index, sr in df.iterrows():
          dt = datetime.strptime(sr["<DATE>"]+sr["<TIME>"], "%Y%m%d%H%M%S")
          if (from_date is None or dt.date() >= from_date) and (untill_date is None or dt.date() < untill_date):
            c_arr.append(Candle(dt, sr["<OPEN>"], sr["<HIGH>"], sr["<LOW>"], sr["<CLOSE>"], sr["<VOL>"]))
        return c_arr

       
    