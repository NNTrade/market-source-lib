from abc import ABC
from datetime import date
from NNTrade.common import TimeFrame
import pandas as pd
from ..common import StockQuoteContainer
from typing import List, Tuple, Dict

class AbsStockQuoteClient(ABC):
    """Abstacrt client to get data of stock quotes

    Args:
        ABC (_type_): _description_
    """
    def get(self, stock:str, timeframe:TimeFrame, from_date: date = None, untill_date: date = None)->pd.DataFrame:
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

    def stocks(self) -> Dict[TimeFrame, List[str]]:
        """Get list timeframe and stocks

        Returns:
            Dict[TimeFrame,List[str]]: list of timeframe and stocks
        """
        ...
