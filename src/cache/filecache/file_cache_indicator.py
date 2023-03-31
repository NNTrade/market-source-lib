from ...tools.filter_df import filter_df
from .basic_func import join_cache_path, save_df, load_df, get_file_path_csv, join_cache_path, config_to_name
from ..abs_cache_indicator import AbsCacheIndicator, IndicatorSettings, TimeFrame, pd, date
import os


class FileCacheIndicator(AbsCacheIndicator):
    def __init__(self, cache_folder: str) -> None:
        """_summary_
        File structure
        - Cache_folder
          - {stock} (__get_stock_folder)
            - {timeframe.full_name()} (__get_timeframe_folder) 
              - {indicator} (__get_indicator_folder)
                 {config_value}.csv (__get_indicator_file_path)
              - aggregated 
                - {timeframe.full_name()} (__get_aggregated_folder)
                  - {indicator} (__get_aggregated_indicator_folder)
                    - {config_value}.csv (__get_aggregated_indicator_file_path)        

        Args:
            cache_folder (str): _description_

        Raises:
            Exception: _description_
        """
        super().__init__()
        self.__cache_folder = cache_folder
        if not (os.path.exists(self.__cache_folder)):
            raise Exception(
                f"Folder {self.__cache_folder} doesn't exist. Create cache folder")
        self.__logger = self._logger.getChild("FileCacheIndicator")

    def __get_stock_folder(self, stock) -> str:
        return join_cache_path(self.__cache_folder, stock)

    def __get_timeframe_folder(self, stock, timeframe: TimeFrame) -> str:
        return join_cache_path(self.__get_stock_folder(stock), timeframe.full_name())

    def __get_indicator_folder(self, stock, timeframe: TimeFrame, indicator: str) -> str:
        return join_cache_path(self.__get_timeframe_folder(stock, timeframe), indicator)

    def __get_indicator_file_path(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings) -> str:
        cache_folder = self.__get_indicator_folder(
            stock, timeframe, indicator.indicator_type)
        fileName = config_to_name(indicator.parameters)
        return get_file_path_csv(cache_folder, fileName)

    def _save_indicator(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings, indicator_df: pd.DataFrame):
        file_path = self.__get_indicator_file_path(stock, timeframe, indicator)
        save_df(file_path, indicator_df)

    def _load_indicator(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings, from_date: date = None, till_date: date = None) -> pd.DataFrame:
        file_path = self.__get_indicator_file_path(stock, timeframe, indicator)
        df = load_df(file_path)
        return filter_df(df, from_date, till_date)

    def _indicator_is_exist(self, stock: str, timeframe: TimeFrame, indicator: IndicatorSettings) -> bool:
        file_path = self.__get_indicator_file_path(stock, timeframe, indicator)
        return os.path.exists(file_path)

    def __get_aggregated_folder(self, stock, timeframe_base: TimeFrame, timeframe_target: TimeFrame) -> str:
        agr_dir = join_cache_path(self.__get_timeframe_folder(
            stock, timeframe_base), "aggregated")
        return join_cache_path(agr_dir, timeframe_target.full_name())

    def __get_aggregated_indicator_folder(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, indicator: str) -> str:
        return join_cache_path(self.__get_aggregated_folder(stock, timeframe_base, timeframe_target), indicator)

    def __get_aggregated_indicator_file_path(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, indicator: IndicatorSettings) -> str:
        cache_folder = self.__get_aggregated_indicator_folder(
            stock, timeframe_base, timeframe_target, indicator.indicator_type)
        fileName = config_to_name(indicator.parameters)
        return get_file_path_csv(cache_folder, fileName)

    def save_aggregated_indicator(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, indicator: IndicatorSettings, indicator_df: pd.DataFrame):
        file_path = self.__get_aggregated_indicator_file_path(
            stock, timeframe_base, timeframe_target, indicator)
        save_df(file_path, indicator_df)

    def load_aggregated_indicator(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, indicator: IndicatorSettings, from_date: date = None, till_date: date = None) -> pd.DataFrame:
        file_path = self.__get_aggregated_indicator_file_path(
            stock, timeframe_base, timeframe_target, indicator)
        df = load_df(file_path)
        return filter_df(df, from_date, till_date)

    def aggregated_indicator_is_exist(self, stock: str, timeframe_base: TimeFrame, timeframe_target: TimeFrame, indicator: IndicatorSettings) -> bool:
        file_path = self.__get_aggregated_indicator_file_path(
            stock, timeframe_base, timeframe_target, indicator)
        return os.path.exists(file_path)
