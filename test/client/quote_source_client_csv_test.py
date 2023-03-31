import unittest
import logging
from src.client.quote_source_client_csv import QuoteSourceClientFinamCSV, TimeFrame,date, pd
from NNTrade.common.candle_col_name import OPEN, HIGH, LOW, CLOSE, VOLUME, INDEX
from datetime import datetime
from test.compare_df import compare_df

class QuoteSourceClientCSV_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_get_data_THEN_correct_data(self):
    # Array
    qsc = QuoteSourceClientFinamCSV("test/client")
    qsc.add_file("test.MINUTE1.csv", "EURUSD", TimeFrame.m1)
    expected_df = pd.DataFrame({
      OPEN:   [ 1.1729000, 
                1.1729100,
                1.1728300,
                1.1728100 ],
      HIGH:   [ 1.1730800,
                1.1730700,
                1.1730100,
                1.1729000 ],
      LOW:    [ 1.1728000,
                1.1727800,
                1.1727800,
                1.1726700 ],
      CLOSE:  [ 1.1730100,
                1.1730100,
                1.1728100,
                1.1728500 ],
      VOLUME: [ 64,
                67,
                59,
                125 ] }, index=[datetime(2021,4,2,0,2),datetime(2021,4,2,0,3),datetime(2021,4,3,0,4),datetime(2021,4,3,0,5)])
    expected_df.index.name = INDEX
    # Act
    asserted_sqcnt = qsc.get("EURUSD", TimeFrame.m1, date(2021,4,2), date(2021,4,4))
    asserted_df = asserted_sqcnt.to_df()
    # Assert
    self.logger.info(asserted_df)
    self.logger.info(expected_df)
    compare_df(self, expected_df, asserted_df)
    self.assertEqual(expected_df.index.name, asserted_df.index.name)
