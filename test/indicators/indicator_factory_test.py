import unittest
import logging
from src.client.quote_source_client_csv import QuoteSourceClientFinamCSV
from src.indicators.indicator_source import IndicatorSource, QuoteSource, pd
from src.cache.in_memory import InMemoryIndicatorCache, InMemoryQuoteCache, TimeFrame, date
from NNTrade.common.candle_col_name import OPEN, HIGH, LOW, CLOSE, VOLUME, INDEX
from NNTrade.indicators.realizations.ma.settings_builder import MASettingsBuilder
from datetime import datetime
from test.compare_df import compare_df

class IndicatorFactory_TestCase(unittest.TestCase):

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

    def test_WHEN_get_ind_THEN_get_correct(self):
        # Array
        #base_df = pd.DataFrame({OPEN: [10, 20, 30, 40, 50], HIGH: [10, 20, 30, 40, 50], LOW: [1, 2, 3, 4, 5], CLOSE: [1, 2, 3, 4, 5], VOLUME: [
        #    10, 20, 30, 40, 50]},
        #    index=[20200101000000, 20200101010000, 20200101030000, 20200101050000, 20220101060000])
        qsc = QuoteSourceClientFinamCSV("test/indicators")
        qsc.add_file("test.HOUR.csv", "EURUSD", TimeFrame.H)

        imqc = InMemoryQuoteCache()
        #imqc.save_stock_quotes("test", TimeFrame.H, base_df)
        imic = InMemoryIndicatorCache()
        qf = QuoteSource(imqc, qsc)
        ind_f = IndicatorSource(qf, imic)

        expected_df = pd.DataFrame({"MA": [1, 1.5, 2.5, 3.5, 4.5]}, index=[
                                   datetime(2020,1,1), datetime(2020,1,1,1), datetime(2020,1,1,3), datetime(2020,1,1,5), datetime(2022,1,1,6)])
        expected_df.index.name = INDEX
        # Act
        asserted_df = ind_f.get("EURUSD", TimeFrame.H,
                                MASettingsBuilder.create_sma_setting(2))

        # Assert
        self.logger.info("ASSERTED DF")
        self.logger.info(asserted_df)
        compare_df(self,expected_df, asserted_df)

    def test_WHEN_get_ind_with_filet_THEN_get_correct(self):
        # Array
        imqc = InMemoryQuoteCache()
        qsc = QuoteSourceClientFinamCSV("test/indicators")
        qsc.add_file("test.DAY.csv", "EURUSD", TimeFrame.D)
        
        imic = InMemoryIndicatorCache()
        qf = QuoteSource(imqc, qsc)
        ind_f = IndicatorSource(qf, imic)

        expected_df = pd.DataFrame({"MA": [1.5, 2.5, 3.5]}, index=[
                                   datetime(2020,1,3), datetime(2020,1,4), datetime(2020,1,5)])
        expected_df.index.name = INDEX
        # Act
        asserted_df = ind_f.get("EURUSD", TimeFrame.D,
                                MASettingsBuilder.create_sma_setting(2), from_date=date(2020, 1, 3), till_date=date(2020, 1, 6))

        # Assert
        self.logger.info("ASSERTED DF")
        self.logger.info(asserted_df)
        compare_df(self,expected_df, asserted_df)

    def test_WHEN_get_argeated_ind_THEN_get_correct(self):
        # Array
        #base_df = pd.DataFrame({OPEN: [10, 20, 30, 40, 50], HIGH: [10, 20, 30, 40, 50], LOW: [1, 2, 3, 4, 5], CLOSE: [1, 2, 3, 4, 5], VOLUME: [
        #    10, 20, 30, 40, 50]},
        #    index=[20200101000000, 20200101010000, 20200102000000, 20200102010000, 20220103000000])
        qsc = QuoteSourceClientFinamCSV("test/indicators")
        qsc.add_file("test2.HOUR.csv", "EURUSD", TimeFrame.H)

        imqc = InMemoryQuoteCache()
        imic = InMemoryIndicatorCache()
        qf = QuoteSource(imqc, qsc)
        ind_f = IndicatorSource(qf, imic)

        expected_df = pd.DataFrame({"MA": [1, 2.0, 2.5, 3.0, 4.5]}, index=[
                                   datetime(2020,1,1), datetime(2020,1,1,1), datetime(2020,1,2), datetime(2020,1,2,1), datetime(2022,1,3)])
        expected_df.index.name = INDEX

        # Act
        asserted_df = ind_f.get("EURUSD", TimeFrame.D,
                                MASettingsBuilder.create_sma_setting(2), TimeFrame.H)

        # Assert
        self.logger.info("EXPECTED DF")
        self.logger.info(expected_df)
        self.logger.info("ASSERTED DF")
        self.logger.info(asserted_df)
        compare_df(self,expected_df, asserted_df)
        
