import unittest
import logging
from src.cache.in_memory.in_memory_quote import InMemoryQuoteCache
from src.client.realization.quote_source_client_csv import QuoteSourceClientFinamCSV
from src.quotes import QuoteSource, pd, TimeFrame, date
from NNTrade.common.candle_col_name import OPEN, CLOSE, HIGH, LOW, VOLUME, INDEX
from test.compare_df import compare_df
from datetime import datetime


class QuoteFactory_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_get_from_client_THEN_correct(self):
        # Array
        qsc = QuoteSourceClientFinamCSV("test/quotes")
        qsc.add_file("test.MINUTE1.csv", "EURUSD", TimeFrame.m1)

        imqc = InMemoryQuoteCache()
        qf = QuoteSource(imqc, qsc)

        expected_df = pd.DataFrame({
            OPEN:   [1.1729000,
                     1.1729100,
                     1.1728300,
                     1.1728100],
            HIGH:   [1.1730800,
                     1.1730700,
                     1.1730100,
                     1.1729000],
            LOW:    [1.1728000,
                     1.1727800,
                     1.1727800,
                     1.1726700],
            CLOSE:  [1.1730100,
                     1.1730100,
                     1.1728100,
                     1.1728500],
            VOLUME: [64,
                     67,
                     59,
                     125]}, index=[datetime(2021, 4, 2, 0, 2), datetime(2021, 4, 2, 0, 3), datetime(2021, 4, 3, 0, 4), datetime(2021, 4, 3, 0, 5)])
        expected_df.index.name = INDEX

        # Act
        asserted_df = qf.get("EURUSD", TimeFrame.m1,
                             date(2021, 4, 2), date(2021, 4, 4))

        # Assert
        self.logger.info("EXPECTED DF")
        self.logger.info(expected_df)
        self.logger.info("ASSERTED DF")
        self.logger.info(asserted_df)

        compare_df(self, expected_df, asserted_df)
        self.assertEqual(expected_df.index.name, asserted_df.index.name)

    def test_WHEN_get_from_memory_THEN_correct(self):
        # Array
        qsc = QuoteSourceClientFinamCSV("test/quotes")
        qsc.add_file("test.MINUTE1.csv", "EURUSD", TimeFrame.m1)

        imqc = InMemoryQuoteCache()
        qf = QuoteSource(imqc, qsc)

        expected_df = pd.DataFrame({
            OPEN:   [1.1729000,
                     1.1729100,
                     1.1728300,
                     1.1728100],
            HIGH:   [1.1730800,
                     1.1730700,
                     1.1730100,
                     1.1729000],
            LOW:    [1.1728000,
                     1.1727800,
                     1.1727800,
                     1.1726700],
            CLOSE:  [1.1730100,
                     1.1730100,
                     1.1728100,
                     1.1728500],
            VOLUME: [64,
                     67,
                     59,
                     125]}, index=[datetime(2021, 4, 2, 0, 2), datetime(2021, 4, 2, 0, 3), datetime(2021, 4, 3, 0, 4), datetime(2021, 4, 3, 0, 5)])
        expected_df.index.name = INDEX

        # Act
        qf.get("EURUSD", TimeFrame.m1, date(2021, 4, 2), date(2021, 4, 4))

        asserted_df = qf.get("EURUSD", TimeFrame.m1,
                             date(2021, 4, 2), date(2021, 4, 4))

        # Assert
        self.logger.info("ASSERTED DF")
        self.logger.info(asserted_df)
        compare_df(self, expected_df, asserted_df)

    def test_WHEN_get_with_aggregation_THEN_correct(self):
        # Array
        qsc = QuoteSourceClientFinamCSV("test/quotes")
        qsc.add_file("test.MINUTE1.csv", "EURUSD", TimeFrame.m1)

        imqc = InMemoryQuoteCache()

        qf = QuoteSource(imqc, qsc)

        expected_df = pd.DataFrame({
            f"aggregated_{INDEX}":  [datetime(2021, 4, 2, 0, 0), 
                            datetime(2021, 4, 2, 0, 0), 
                            datetime(2021, 4, 3, 0, 0), 
                            datetime(2021, 4, 3, 0, 0)],
            OPEN:   [1.1729000,
                     1.1729000,
                     1.1728300,
                     1.1728300],
            HIGH:   [1.1730800,
                     1.1730800,
                     1.1730100,
                     1.1730100],
            LOW:    [1.1728000,
                     1.1727800,
                     1.1727800,
                     1.1726700],
            CLOSE:  [1.1730100,
                     1.1730100,
                     1.1728100,
                     1.1728500],
            VOLUME: [64,
                     67+64,
                     59,
                     125+59],
            "isLast": [0, 1, 0, 1]}, index=[datetime(2021, 4, 2, 0, 2), datetime(2021, 4, 2, 0, 3), datetime(2021, 4, 3, 0, 4), datetime(2021, 4, 3, 0, 5)])
        expected_df.index.name = INDEX

        # Act
        asserted_df = qf.get("EURUSD", TimeFrame.D,
                             date(2021, 4, 2), date(2021, 4, 4), TimeFrame.m1)

        # Assert
        self.logger.info("ASSERTED DF")
        self.logger.info(asserted_df)
        compare_df(self, expected_df, asserted_df)
