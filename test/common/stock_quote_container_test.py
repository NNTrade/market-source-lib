import unittest
import logging
from src.common import Candle, StockQuoteContainer,datetime,pd,col
from test.compare_df import compare_df

class StockQuoteContainer_TestCase(unittest.TestCase):

  logger = logging.getLogger(__name__)
  logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                      datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

  def test_WHEN_get_df_THEN_get_correct_df(self):
    # Array
    c_arr = [Candle(datetime(2020,1,2,1,1,1),15,25,10,20,150), Candle(datetime(2020,1,1,1,1,1),10,20,5,15,100)]
    sqc = StockQuoteContainer(c_arr)

    expected_df = pd.DataFrame.from_dict({datetime(2020,1,1,1,1,1):[10,20,5,15,100],datetime(2020,1,2,1,1,1):[15,25,10,20,150]}, orient='index', columns=[col.OPEN,col.HIGH,col.LOW,col.CLOSE,col.VOLUME])
    expected_df.index.name = col.INDEX

    # Act
    asserted_df = sqc.to_df()

    # Assert
    self.assertEqual(asserted_df.index.name, col.INDEX)
    self.assertEqual(asserted_df.index[0], datetime(2020,1,1,1,1,1))
    self.assertEqual(asserted_df.index[1], datetime(2020,1,2,1,1,1))
    self.logger.info("ASSERTED_DF:")
    self.logger.info(asserted_df)
    compare_df(self, expected_df, asserted_df)
