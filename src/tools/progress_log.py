from logging import getLogger, Logger


class ProgressLog:
    def __init__(self, index_len_log: int = 6, logger: Logger = None, init_index: int = 0):
        self._index_len_log = index_len_log
        self._cur_index = 0 if init_index == 0 else self._cut_index(init_index)
        self.__logger = getLogger("ProgressLog") if logger is None else logger

    def _cut_index(self, index: int) -> str:
        return str(index)[:self._index_len_log]

    def check(self, cur_index: int):
        cur_cutted_index = self._cut_index(cur_index)
        if cur_cutted_index != self._cur_index:
            self.__logger.info("Passed %s", self._cur_index)
            self._cur_index = cur_cutted_index

    def last(self):
        self.__logger.info("Passed %s", self._cur_index)
