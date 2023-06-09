from logging import getLogger, Logger
import math
from datetime import date,datetime

class ProgressLog:
    def __init__(self, index_len_log: int = 6, logger: Logger = None, init_index: int = 0):
        self._index_len_log = math.pow(10,index_len_log)
        self._cur_index = 0 if init_index == 0 else self._cut_index(init_index)
        self.__logger = getLogger("ProgressLog") if logger is None else logger

    def _cut_index(self, index: int) -> str:
        return int(index // self._index_len_log)

    def check(self, cur_index: int):
        cur_cutted_index = self._cut_index(cur_index)
        if cur_cutted_index != self._cur_index:
            self.__logger.info("Passed %s", cur_index)
            self._cur_index = cur_cutted_index

    def last(self):
        self.__logger.info("Passed %s", self._cur_index)

class ProgressLogDate:
    def __init__(self, init_index: date, logger: Logger = None):
        self._cur_index = self._cut_index(init_index)
        self.__logger = getLogger("ProgressLog") if logger is None else logger

    def _cut_index(self, index: date) -> date:
        return index.replace(day=1)

    def check(self, cur_index: datetime):
        cur_cutted_index = self._cut_index(cur_index.date())
        if cur_cutted_index != self._cur_index:
            self.__logger.info("Passed %s", cur_index)
            self._cur_index = cur_cutted_index

    def last(self):
        self.__logger.info("Passed %s", self._cur_index)