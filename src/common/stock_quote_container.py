from datetime import datetime
from typing import List,Dict
import pandas as pd
import NNTrade.common.candle_col_name as col
import collections
from .candle import Candle

class StockQuoteContainer:
    def __init__(self, candle_arr:List[Candle]):
       self._data_dic:Dict[datetime, Candle] = collections.OrderedDict(sorted({candle.datetime:candle for candle in candle_arr}.items()))

    def candles(self)->List[Candle]:
       return [candle for candle in self._data_dic.values()]
    
    def to_df(self)->pd.DataFrame:
       ret_df = pd.DataFrame([candle.to_series() for candle in self._data_dic.values()])
       ret_df.index.name = col.INDEX
       return ret_df