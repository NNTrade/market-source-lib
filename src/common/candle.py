from datetime import datetime
import pandas as pd
import NNTrade.common.candle_col_name as col

class Candle:
    def __init__(self, datetime:datetime, open:float, high:float, low:float,close:float,volume:float) -> None:
        self._datetime = datetime
        self._open = open
        self._high = high
        self._low = low
        self._close = close
        self._volume = volume
        pass

    @property
    def datetime(self)->datetime:
        return self._datetime
    @property
    def open(self)->float:
      return self._open
    @property
    def high(self)->float:
      return self._high
    @property
    def low(self)->float:
      return self._low
    @property
    def close(self)->float:
      return self._close
    @property
    def volume(self)->float:
      return self._volume
    
    def to_series(self)->pd.Series:
       return pd.Series({col.OPEN: self.open, col.HIGH: self.high, col.LOW: self.low, col.CLOSE:self.close, col.VOLUME:self.volume}, name=self.datetime)