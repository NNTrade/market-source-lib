from ..common.stock_quote_container import StockQuoteContainer
from ..client.abs_quote_source_client import AbsStockQuoteClient, Dict, List
from ..cache.abs_cache_quote import AbsCacheQuote, TimeFrame, date, pd
from .DfCondenser import DfCondenser
from logging import getLogger


class QuoteSource:
    def __init__(self, quote_cache: AbsCacheQuote, quote_source_client:AbsStockQuoteClient) -> None:
        self.quote_cache = quote_cache
        self.quote_source_client = quote_source_client
        self._logger = getLogger("QuoteFactory")
        pass
    
    def get(self,  stock: str, timeframe: TimeFrame, from_date: date = None, untill_date: date = None,  step_timeframe: TimeFrame = None) -> pd.DataFrame:
        """Get Pandas DataFrame with stock quote data

        Args:
            stock (str): stock name
            timeframe (TimeFrame): TimeFrame of quote candle
            from_date (date): from date (date included)
            untill_date (date): until date (date excluded)
            step_timeframe (TimeFrame, optional): Step of candle recalculation. Must be more or equal timeframe or None\n
                                                  If None or Equal timeframe then 1 row per candle.\n
                                                  If less than timeframe then several rows per candle, delta time between rows is step_timefrme.\n
                                                  Defaults to None.

        Returns:
            pd.DataFrame: _description_
        """
        if step_timeframe is None:
            step_timeframe = timeframe
        if step_timeframe.to_seconds() > timeframe.to_seconds():
            raise Exception("step_timeframe must be <= timeframe")
        
        if not self.quote_cache.stock_quotes_is_exist(stock, step_timeframe, timeframe):
            self._logger.info(
                "Cann't find quotes for %s %s by step %s", stock, timeframe, timeframe)
            
            if step_timeframe == timeframe:
                self._logger.info("get request quotes from client")
                quote_stock_df:pd.DataFrame = self.quote_source_client.get(stock, timeframe, from_date, untill_date)
                self._logger.info("save quotes in cache")
                self.quote_cache.save_stock_quotes(stock, timeframe, quote_stock_df)
                
            elif step_timeframe != timeframe:
                self._logger.info("get based df %s %s", stock, step_timeframe.full_name())
                base_df = self.get("EURUSD", step_timeframe, from_date, untill_date)
                
                self._logger.info("Condense data")
                condensed_df = DfCondenser.Condense(base_df, step_timeframe, timeframe)
                
                self._logger.info("save quotes in cache")
                self.quote_cache.save_stock_quotes(stock, step_timeframe, condensed_df, timeframe)

            
        return self.quote_cache.load_stock_quotes(stock, step_timeframe, from_date, untill_date, timeframe)

    def stocks(self) -> Dict[TimeFrame, List[str]]:
        """Get list timeframe and stocks

        Returns:
            Dict[TimeFrame,List[str]]: list of timeframe and stocks
        """
        return self.quote_source_client.stocks()
