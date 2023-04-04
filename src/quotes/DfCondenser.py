from __future__ import annotations
from NNTrade.common import TimeFrame, INDEX, CLOSE, OPEN, HIGH, LOW, VOLUME
from .CondenserToTf import CondenserToTf, get_condenser_to_timeframe
import pandas as pd
from typing import List
from ..cache.abs_cache_quote import AbsCacheQuote
from ..tools.progress_log import ProgressLogDate
from logging import getLogger
from datetime import datetime

IS_LAST = "isLast"
AGGR_INDEX = f"aggregated_{INDEX}"

class DfCondenser():
  def __init__(self, target_tf: TimeFrame) -> None:
    self._condenser_tf: CondenserToTf = get_condenser_to_timeframe(target_tf)
    self._target_tf = target_tf
    self.clear()
    pass

  @staticmethod
  def LoopByCondesers(stock: str, timeframe_base: TimeFrame, timeframe_list: List[TimeFrame], cache: AbsCacheQuote):
    logger = getLogger("DfCondenser.LoopByCondesers")
    base_df = cache._load_stock_quotes(stock, timeframe_base)
    condensers = [DfCondenser(tf) for tf in timeframe_list]
    for condenser in condensers:
      if cache.aggregated_stock_quotes_is_exist(stock, timeframe_base, condenser.target_tf):
        raise Exception(
            f"Aggregation to time frame {condenser.target_tf.full_name()} already exist")

      logger.info("Condense %s %s from %s", stock,
                  condenser.target_tf.full_name(), timeframe_base.full_name())
      pl = ProgressLogDate(base_df.index[0], logger=logger)
      for index, row in base_df.iterrows():
        open = row[OPEN]
        close = row[CLOSE]
        high = row[HIGH]
        low = row[LOW]
        volume = row[VOLUME]
        condenser.next(index, open, close, high, low, volume)

        pl.check(index)

      condenser.finish()

      cache.save_aggregated_stock_quotes(
          stock, timeframe_base, condenser.target_tf, condenser.result)

      condenser.clear()
      logger.info("Condensing %s %s from %s. DONE", stock,
                  condenser.target_tf.full_name(), timeframe_base.full_name())

  def _clear_tmp(self):
    self._index_arr = []
    self._condense_index_arr = []
    self._condense_open_arr = []
    self._condense_close_arr = []
    self._condense_high_arr = []
    self._condense_low_arr = []
    self._condense_volume_arr = []
    self._condense_is_last_arr = []

    self._prev_condense_index = None
    self._cur_condense_open = None
    self._cur_condense_high = None
    self._cur_condense_low = None
    self._cur_condense_volume = 0

  def clear(self):
    self._result_df = None
    self._clear_tmp()

  @property
  def target_tf(self) -> TimeFrame:
    return self._target_tf

  def next(self, index: datetime, open: float, close: float, high: float, low: float, volume: int):
    condence_candle_index = self._condenser_tf.condense_dt(index)

    if self._prev_condense_index is None or self._prev_condense_index != condence_candle_index:
      self._cur_condense_high = high
      self._cur_condense_low = low
      self._cur_condense_open = open
      self._cur_condense_volume = volume
      if self._prev_condense_index is not None:
        # add 1 that prev line was the last in condense group
        self._condense_is_last_arr.append(1)
      self._prev_condense_index = condence_candle_index
    else:
      self._cur_condense_high = max(self._cur_condense_high, high)
      self._cur_condense_low = min(self._cur_condense_low, low)
      self._cur_condense_volume = self._cur_condense_volume + volume
      # add 0 that prev line was not the last in condense group
      self._condense_is_last_arr.append(0)

    self._index_arr.append(index)
    self._condense_index_arr.append(condence_candle_index)
    self._condense_open_arr.append(self._cur_condense_open)
    self._condense_low_arr.append(self._cur_condense_low)
    self._condense_high_arr.append(self._cur_condense_high)
    self._condense_close_arr.append(close)
    self._condense_volume_arr.append(self._cur_condense_volume)

  def next_row(self, index: int, row: pd.Series):
    self.next(index, row[OPEN], row[CLOSE], row[HIGH], row[LOW], row[VOLUME])

  def finish(self):
    # add 0 because on next we add to prev line
    self._condense_is_last_arr.append(1)

    self._result_df = pd.DataFrame({
        AGGR_INDEX: self._condense_index_arr,
        OPEN: self._condense_open_arr,
        LOW: self._condense_low_arr,
        HIGH: self._condense_high_arr,
        CLOSE: self._condense_close_arr,
        VOLUME: self._condense_volume_arr,
        IS_LAST: self._condense_is_last_arr},
        index=self._index_arr)
    self._result_df.index.name = INDEX
    self._clear_tmp()

  @property
  def result(self) -> pd.DataFrame:
    return self._result_df
