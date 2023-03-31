from .file_cache_indicator import FileCacheIndicator
from .file_cache_quote import FileCacheQuote
from .basic_func import join_cache_path
from ..abs_cache import AbsCache, AbsCacheQuote, AbsCacheIndicator
import os


class FileCache(AbsCache):
    def __init__(self, cache_folder: str) -> None:
        """_summary_
        File structure
        - Cache_folder
          - quote
          -indicator 
          - strategy

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
        self.__logger = self._logger.getChild("FileCache")
        self.__quote_cache = FileCacheQuote(
            join_cache_path(self.__cache_folder, "quote"))
        self.__indicator_cache = FileCacheIndicator(
            join_cache_path(self.__cache_folder, "indicator"))

    @property
    def quote(self) -> AbsCacheQuote:
        return self.__quote_cache

    @property
    def indicator(self) -> AbsCacheIndicator:
        return self.__indicator_cache
