from .. import AbsCacheIndicator, TimeFrame, IndicatorSettings, pd, date
from ...tools.filter_df import filter_df
from typing import Dict


class InMemoryIndicatorCache(AbsCacheIndicator):
    def __init__(self) -> None:
      self.__stock_tf_cfg_df: Dict[str, Dict[TimeFrame,
                                             Dict[IndicatorSettings, pd.DataFrame]]] = {}
      self.__stock_tf_tf_cfg_df: Dict[str, Dict[TimeFrame, Dict[TimeFrame,
                                                                Dict[IndicatorSettings, pd.DataFrame]]]] = {}
      super().__init__()

    def _save_indicator(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings, indicator_df: pd.DataFrame):
        tf_cfg_df = self.__stock_tf_cfg_df.pop(stock, {})
        cfg_df = tf_cfg_df.pop(timeframe, {})

        cfg_df[indicator] = indicator_df

        tf_cfg_df[timeframe] = cfg_df
        self.__stock_tf_cfg_df[stock] = tf_cfg_df

    def _load_indicator(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings, from_date: date = None, till_date: date = None) -> pd.DataFrame:
      return filter_df(self.__stock_tf_cfg_df[stock][timeframe][indicator], from_date, till_date)

    def _indicator_is_exist(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings) -> bool:
        if stock not in self.__stock_tf_cfg_df.keys():
          return False
        if timeframe not in self.__stock_tf_cfg_df[stock].keys():
          return False
        if indicator not in self.__stock_tf_cfg_df[stock][timeframe].keys():
          return False
        return True

    def save_aggregated_indicator(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, indicator: IndicatorSettings, indicator_df: pd.DataFrame):
        tf_tf_cfg_df = self.__stock_tf_tf_cfg_df.pop(stock, {})
        tf_cfg_df = tf_tf_cfg_df.pop(timeframe_base, {})
        cfg_df = tf_cfg_df.pop(timeframe_target, {})

        cfg_df[indicator] = indicator_df

        tf_cfg_df[timeframe_target] = cfg_df
        tf_tf_cfg_df[timeframe_base] = tf_cfg_df
        self.__stock_tf_tf_cfg_df[stock] = tf_tf_cfg_df

    def load_aggregated_indicator(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, indicator: IndicatorSettings, from_date: date = None, till_date: date = None) -> pd.DataFrame:
        return filter_df(self.__stock_tf_tf_cfg_df[stock][timeframe_base][timeframe_target][indicator], from_date, till_date)

    def aggregated_indicator_is_exist(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, indicator: IndicatorSettings) -> bool:
        if stock not in self.__stock_tf_tf_cfg_df.keys():
          return False
        if timeframe_base not in self.__stock_tf_tf_cfg_df[stock].keys():
          return False
        if timeframe_target not in self.__stock_tf_tf_cfg_df[stock][timeframe_base].keys():
          return False
        if indicator not in self.__stock_tf_tf_cfg_df[stock][timeframe_base][timeframe_target].keys():
          return False
        return True
