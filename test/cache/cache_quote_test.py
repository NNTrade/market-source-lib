import unittest
import logging
import pandas as pd
from NNTrade.common import CLOSE, OPEN, HIGH, CLOSE, VOLUME,LOW, TimeFrame, INDEX
from src.cache.filecache.file_cache_quote import FileCacheQuote
from src.client.quote_source_client_csv import QuoteSourceClientFinamCSV, StockQuoteContainer
import os
import shutil
from test.compare_df import compare_df

class CacheQuote_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
  stock = "EURUSD"
  file_path = "./test/cache/test_data/test_quote_EURUSD.csv"
  fc = FileCacheQuote("./test/cache/test_data/CacheQuote_TestCase")
  @classmethod
  def setUpClass(cls):
      shutil.rmtree("./test/cache/test_data/CacheQuote_TestCase")
      os.mkdir("./test/cache/test_data/CacheQuote_TestCase")

  def test_WHEN_save_and_load_THEN_get_same_quote(self):
    # Array
    qsc = QuoteSourceClientFinamCSV("test/cache/test_data")
    qsc.add_file("test.MINUTE1.csv", "EURUSD", TimeFrame.m1)
    expected_df = qsc.get("EURUSD", TimeFrame.m1).to_df()

    # Act
    self.fc.save_stock_quotes("EURUSD", TimeFrame.m1, expected_df)

    asserted_df =self.fc.load_stock_quotes("EURUSD", TimeFrame.m1)

    # Assert
    self.logger.info("Expected DF")
    self.logger.info(f"\n{expected_df}")
    self.logger.info("Asserted DF")
    self.logger.info(f"\n{asserted_df}")

    compare_df(self, expected_df, asserted_df)