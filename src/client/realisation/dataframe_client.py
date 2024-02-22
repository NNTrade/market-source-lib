from ..abs_quote_source_client import TimeFrame,pd, Dict,List,date, AbsStockQuoteClient
from ...tools.filter_df import filter_df
from collections import defaultdict

class DataFrameClient(AbsStockQuoteClient):
    """Client to get base stock quotes from DataFrame 

    """
    def __init__(self):
        self._df_dic:Dict[TimeFrame, Dict[str, pd.DataFrame]] = {}
        super().__init__()

    def add_df(self, stock:str, timeframe:TimeFrame, data_df: pd.DataFrame):
        stocks_dic = self._df_dic.get(timeframe, {})
        stocks_dic[stock] = data_df

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
        df  = self._df_dic[timeframe][stock]
        return filter_df(df, from_date, untill_date)

    def stocks(self) -> Dict[TimeFrame, List[str]]:
        """Get list timeframe and stocks

        Returns:
            Dict[TimeFrame,List[str]]: list of timeframe and stocks
        """
        # Initialize a defaultdict to group symbols by TimeFrame
        output_dict: Dict[TimeFrame, List[str]] = defaultdict(list)

        # Iterate through the input dictionary
        for symbol, stock_dic in self._df_dic.items():
            for timeframe, value in stock_dic.items():
                # Append the symbol to the corresponding TimeFrame list
                output_dict[timeframe].append(symbol)

        # Convert the defaultdict to a regular dictionary
        return dict(output_dict)
