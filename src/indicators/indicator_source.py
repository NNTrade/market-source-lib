from ..cache.abs_cache_indicator import AbsCacheIndicator
from ..quotes.quotes_source import QuoteSource, TimeFrame
import pandas as pd
from typing import List, Dict
from ..tools.progress_log import ProgressLogDate
from NNTrade.indicators import IndicatorSettings, AbsIndicator, IndicatorFactory
from datetime import date
from logging import getLogger
from ..quotes.DfCondenser import IS_LAST
from NNTrade.common.candle_col_name import INDEX

class IndicatorSource:
    def __init__(self, quote_factory: QuoteSource, cache: AbsCacheIndicator) -> None:
        self.__cache: AbsCacheIndicator = cache
        self.__quote_source: QuoteSource = quote_factory
        self._logger = getLogger("IndicatorFactory")
        self._indicator_factory: IndicatorFactory = IndicatorFactory()
        pass

    def get(self, stock: str, timeframe: TimeFrame, indicators_cfg: IndicatorSettings, step_timeframe: TimeFrame = None, from_date: date = None, till_date: date = None) -> Dict[IndicatorSettings, pd.DataFrame]:
        return self.get_many(stock, timeframe, [indicators_cfg], step_timeframe, from_date, till_date)[indicators_cfg]

    def get_many(self, stock: str,  timeframe: TimeFrame, indicators_cfg_list: List[IndicatorSettings], step_timeframe: TimeFrame = None, from_date: date = None, till_date: date = None) -> Dict[IndicatorSettings, pd.DataFrame]:
        """Get inficators data

        Args:
            stock (str): stock name
            timeframe_base (TimeFrame): base timeframe
            indicators_cfg_list (List[IndicatorSettings]): List of calculating indicators
            timeframe_target (TimeFrame, optional): Aggregation timeframe. Defaults to None.
            from_date (date, optional): Filtering from date. Defaults to None.
            till_date (date, optional): Filtering till date. Defaults to None.

        Returns:
            Dict[IndicatorSettings, pd.DataFrame]: Dict of indicators values
        """
        if step_timeframe is None:
            step_timeframe = timeframe

        unique_cfg_list = list(dict.fromkeys(indicators_cfg_list))
        new_ind_cfg_arr = self.__check_existed(
            stock, step_timeframe, unique_cfg_list, timeframe)

        if len(new_ind_cfg_arr) > 0:
            self._logger.info(
                "Cann't find indicators for %s %s by step %s:\n%s", stock, timeframe, step_timeframe, "\n".join([str(cfg.to_dict()) for cfg in new_ind_cfg_arr]))
            self.__calc_new_ind(stock, timeframe,
                                new_ind_cfg_arr, step_timeframe)
            self._logger.info(
                "Indicators calculation for %s %s by step %s. DONE", stock, timeframe, step_timeframe)

        return {ind_cfg: self.__cache.load_indicator(stock, step_timeframe, ind_cfg, from_date, till_date, timeframe) for ind_cfg in unique_cfg_list}

    def __check_existed(self, stock: str, timeframe_base: TimeFrame, unique_cfg_list: List[IndicatorSettings], timeframe_target: TimeFrame = None) -> List[IndicatorSettings]:
        new_ind_cfg_arr = []
        for ind_cfg in unique_cfg_list:
            if not self.__cache.indicator_is_exist(stock, timeframe_base, ind_cfg, timeframe_target):
                new_ind_cfg_arr.append(ind_cfg)
        return new_ind_cfg_arr

    def __calc_new_ind(self, stock: str,timeframe: TimeFrame, new_ind_cfg_list: List[IndicatorSettings],  step_timeframe: TimeFrame):
        work_df = self.__quote_source.get(
            stock, step_timeframe=step_timeframe, timeframe=timeframe)
        ind = self.__loop_by_periods(work_df, new_ind_cfg_list)
        ind_len = len(ind)
        for i in range(ind_len):
            ind_cfg = new_ind_cfg_list[i]
            ind_df = ind[i].result
            ind_df.index.name = INDEX
            self.__cache.save_indicator(
                stock, step_timeframe, ind_cfg, ind_df, timeframe)

    def __loop_by_periods(self, work_df: pd.DataFrame, indicators_cfg_list: List[IndicatorSettings]) -> List[AbsIndicator]:
        if IS_LAST not in work_df.columns:
            work_df[IS_LAST] = 1

        ind_list: List[AbsIndicator] = []
        for cfg in indicators_cfg_list:
            ind_list.append(self._indicator_factory.create(cfg))

        progressLog = ProgressLogDate(work_df.index[0],logger=self._logger)

        for index, row in work_df.iterrows():
            for ind_inst in ind_list:
                ind_inst.next(index, row, bool(
                    row[IS_LAST]))

            progressLog.check(index)

        for ind_inst in ind_list:
            ind_inst.finish()

        return ind_list
