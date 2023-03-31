from abc import ABC
from datetime import date
from NNTrade.common import TimeFrame
import pandas as pd
from ..common import StockQuoteContainer

class AbsStockQuoteClient(ABC):
    """Abstacrt client to get data of stock quotes

    Args:
        ABC (_type_): _description_
    """
    def get(self, stock:str, timeframe:TimeFrame, from_date: date = None, untill_date: date = None)->StockQuoteContainer:
        """Get stock data by timeframe

        Args:
            stock (str): _description_
            timeframe (TimeFrame): _description_
            from_date (date, optional): _description_. Defaults to None.
            untill_date (date, optional): _description_. Defaults to None.

        Returns:
            StockQuoteContainer: _description_
        """
        ...