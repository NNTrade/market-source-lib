from abc import ABC, abstractmethod
import pandas as pd
from NNTrade.common import TimeFrame
from datetime import date
from NNTrade.indicators import IndicatorSettings
from logging import getLogger


class AbsCacheIndicator(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._logger = getLogger("AbsCacheIndicator")

    def save_indicator(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings, indicator_df: pd.DataFrame, timeframe_target: TimeFrame = None):
        if timeframe_target is None or timeframe == timeframe_target:
            self._save_indicator(stock, timeframe, indicator, indicator_df)
        else:
            self.save_aggregated_indicator(
                stock, timeframe, timeframe_target, indicator, indicator_df)

    @abstractmethod
    def _save_indicator(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings, indicator_df: pd.DataFrame):
        ...

    def load_indicator(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings, from_date: date = None, till_date: date = None, timeframe_target: TimeFrame = None) -> pd.DataFrame:
        if timeframe_target is None or timeframe == timeframe_target:
            return self._load_indicator(stock, timeframe, indicator, from_date, till_date)
        else:
            return self.load_aggregated_indicator(stock, timeframe, timeframe_target, indicator, from_date, till_date)

    @abstractmethod
    def _load_indicator(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings, from_date: date = None, till_date: date = None) -> pd.DataFrame:
        ...

    def indicator_is_exist(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings, timeframe_target: TimeFrame = None) -> bool:
        if timeframe_target is None or timeframe == timeframe_target:
            return self._indicator_is_exist(stock, timeframe, indicator)
        else:
            return self.aggregated_indicator_is_exist(stock, timeframe, timeframe_target, indicator)

    @abstractmethod
    def _indicator_is_exist(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings) -> bool:
        ...

    @abstractmethod
    def save_aggregated_indicator(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, indicator: IndicatorSettings, indicator_df: pd.DataFrame):
        ...

    @abstractmethod
    def load_aggregated_indicator(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, indicator: IndicatorSettings, from_date: date = None, till_date: date = None) -> pd.DataFrame:
        ...

    @abstractmethod
    def aggregated_indicator_is_exist(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, indicator: IndicatorSettings) -> bool:
        ...
