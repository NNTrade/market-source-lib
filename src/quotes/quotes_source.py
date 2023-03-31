from ..common.stock_quote_container import StockQuoteContainer
from ..client.abs_quote_source_client import AbsStockQuoteClient
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
                "Cann't find quotes for %s %s by step %s", stock, timeframe, step_timeframe)
            quote_stock_cnt:StockQuoteContainer = self.quote_source_client.get(stock, step_timeframe, from_date, untill_date)
            self.quote_cache.save_stock_quotes(stock, step_timeframe, quote_stock_cnt.to_df())
            if step_timeframe != timeframe:
                DfCondenser.LoopByCondesers(
                    stock, step_timeframe, [timeframe], self.quote_cache)
            
        return self.quote_cache.load_stock_quotes(stock, step_timeframe, from_date, untill_date, timeframe)
