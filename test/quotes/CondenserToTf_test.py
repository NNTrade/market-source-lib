from src.quotes.CondenserToTf import get_condenser_to_timeframe, CondenserToTf
import unittest
import logging
from NNTrade.common import TimeFrame
from typing import Callable
from datetime import datetime
class To_TimeFrame_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


    def test_WHEN_request_func_THEN_get_func(self):
      # Array
      test_value =20220101111000
      
      # Act
      for tf in TimeFrame:
        with self.subTest(i=tf):
          asserted_condenser:CondenserToTf = get_condenser_to_timeframe(tf)
          asserted_value = asserted_condenser.condense_int(test_value)

      # Assert
          self.assertIsNotNone(asserted_value)

class To_m1_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    
    condenser:CondenserToTf = get_condenser_to_timeframe(TimeFrame.m1)

    def test_WHEN_give_int_values_THEN_get_correct_result(self):
      # Array
      test_values = [(20220101110000,20220101110000), (20220101110100,20220101110100), (20220101110959,20220101110900)]
      for test_value in test_values:
        with self.subTest(i=test_value):
          expect_dt = test_value[1]
      # Act
          assert_dt = self.condenser.condense_int(test_value[0])

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result(self):
      # Array
      test_values = [(datetime(2022,1,1,11,00,00),datetime(2022,1,1,11,00,00)), 
                     (datetime(2022,1,1,11,1,00),datetime(2022,1,1,11,1,00)), 
                     (datetime(2022,1,1,11,9,59),datetime(2022,1,1,11,9,00))]
      for test_value in test_values:
        with self.subTest(i=test_value):
          expect_dt = test_value[1]
      # Act
          assert_dt = self.condenser.condense_dt(test_value[0])

      # Assert
          self.assertEqual(expect_dt, assert_dt)

class To_m5_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    condenser:CondenserToTf = get_condenser_to_timeframe(TimeFrame.m5)

    def test_WHEN_give_int_values_THEN_get_correct_result(self):
      # Array
      test_values = [20220101110000, 20220101110300,20220101110450, 20220101110459]
      expect_dt = 20220101110000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_dt_values_THEN_get_correct_result(self):
      # Array
      test_values = [datetime(2022,1,1,11,0,0), datetime(2022,1,1,11,3,0),datetime(2022,1,1,11,4,50), datetime(2022,1,1,11,4,59)]
      expect_dt = datetime(2022,1,1,11,0,0)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    

    def test_WHEN_give_int_values_THEN_get_correct_result2(self):
      # Array
      test_values = [20220101110500,20220101110505,20220101110730, 20220101110859, 20220101110959]
      expect_dt = 20220101110500
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_dt_values_THEN_get_correct_result2(self):
      # Array
      test_values = [datetime(2022,1,1,11,5,00),
                     datetime(2022,1,1,11,5,5),
                     datetime(2022,1,1,11,7,30), 
                     datetime(2022,1,1,11,8,59), 
                     datetime(2022,1,1,11,9,59)]
      expect_dt = datetime(2022,1,1,11,5,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_int_values_THEN_get_correct_result3(self):
      # Array
      test_values = [20220101111000,20220101111133, 20220101111200, 20220101111345, 20220101111459]
      expect_dt = 20220101111000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_dt_values_THEN_get_correct_result3(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101111000,20220101111133, 20220101111200, 20220101111345, 20220101111459]]
      expect_dt = datetime(2022,1,1,11,10,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_int_values_THEN_get_correct_result4(self):
      # Array
      test_values = [20220101111500, 20220101111559, 20220101111600, 20220101111739, 20220101111959]
      expect_dt = 20220101111500
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_dt_values_THEN_get_correct_result4(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101111500, 20220101111559, 20220101111600, 20220101111739, 20220101111959]]
      expect_dt = datetime(2022,1,1,11,15,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

class To_m10_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    
    condenser:CondenserToTf = get_condenser_to_timeframe(TimeFrame.m10)

    def test_WHEN_give_int_values_THEN_get_correct_result(self):
      # Array
      test_values = [20220101110000, 20220101110100, 20220101110959]
      expect_dt = 20220101110000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101110000, 20220101110100, 20220101110959]]
      expect_dt = datetime(2022,1,1,11,0,0)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_int_values_THEN_get_correct_result_side(self):
      # Array
      expect_dt = 20220101111000
      test_value =20220101111000

      # Act
      assert_dt = self.condenser.condense_int(test_value)

      # Assert
      self.assertEqual(expect_dt, assert_dt)
      
    def test_WHEN_give_dt_values_THEN_get_correct_result_side(self):
      # Array
      expect_dt = datetime(2022,1,1,11,10,00)
      test_value =datetime(2022,1,1,11,10,00)

      # Act
      assert_dt = self.condenser.condense_dt(test_value)

      # Assert
      self.assertEqual(expect_dt, assert_dt)

class To_m15_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    condenser:CondenserToTf = get_condenser_to_timeframe(TimeFrame.m15)

    def test_WHEN_give_int_values_THEN_get_correct_result(self):
      # Array
      test_values = [20220101110000, 20220101110100, 20220101110959, 20220101111000, 20220101111238, 20220101111459]
      expect_dt = 20220101110000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101110000, 20220101110100, 20220101110959, 20220101111000, 20220101111238, 20220101111459]]
      expect_dt = datetime(2022,1,1,11,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_int_values_THEN_get_correct_result2(self):
      # Array
      test_values = [20220101111500, 20220101111515, 20220101111700, 20220101111900, 20220101112534, 20220101112959]
      expect_dt = 20220101111500
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result2(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101111500, 20220101111515, 20220101111700, 20220101111900, 20220101112534, 20220101112959]]
      expect_dt = datetime(2022,1,1,11,15,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_int_values_THEN_get_correct_result3(self):
      # Array
      test_values = [20220101113000, 20220101113515, 20220101113732, 20220101114000, 20220101114334, 20220101114459]
      expect_dt = 20220101113000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result3(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101113000, 20220101113515, 20220101113732, 20220101114000, 20220101114334, 20220101114459]]
      expect_dt = datetime(2022,1,1,11,30,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_int_values_THEN_get_correct_result4(self):
      # Array
      test_values = [20220101114500, 20220101114515, 20220101114732, 20220101115400, 20220101115434, 20220101115959]
      expect_dt = 20220101114500
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result4(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101114500, 20220101114515, 20220101114732, 20220101115400, 20220101115434, 20220101115959]]
      expect_dt = datetime(2022,1,1,11,45,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_int_values_THEN_get_correct_result_side(self):
      # Array
      expect_dt = 20220101120000
      test_value =20220101120000

      # Act
      assert_dt = self.condenser.condense_int(test_value)

      # Assert
      self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_dt_values_THEN_get_correct_result_side(self):
      # Array
      expect_dt = datetime(2022,1,1,12,00,00)
      test_value = datetime(2022,1,1,12,00,00)

      # Act
      assert_dt = self.condenser.condense_dt(test_value)

      # Assert
      self.assertEqual(expect_dt, assert_dt)

class To_m30_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    condenser:CondenserToTf = get_condenser_to_timeframe(TimeFrame.m30)

    def test_WHEN_give_int_values_THEN_get_correct_result(self):
      # Array
      test_values = [20220101110000, 20220101111300,20220101111850, 20220101112000, 20220101112959]
      expect_dt = 20220101110000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101110000, 20220101111300,20220101111850, 20220101112000, 20220101112959]]
      expect_dt = datetime(2022,1,1,11,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_int_values_THEN_get_correct_result2(self):
      # Array
      test_values = [20220101113000, 20220101113300,20220101113850, 20220101114800, 20220101115959]
      expect_dt = 20220101113000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result2(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101113000, 20220101113300,20220101113850, 20220101114800, 20220101115959]]
      expect_dt = datetime(2022,1,1,11,30,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

class To_H_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    
    condenser:CondenserToTf = get_condenser_to_timeframe(TimeFrame.H)

    def test_WHEN_give_int_values_THEN_get_correct_result(self):
      # Array
      test_values = [20220101110000, 20220101111300, 20220101111600, 20220101113850, 20220101114800, 20220101115959]
      expect_dt = 20220101110000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    def test_WHEN_give_dt_values_THEN_get_correct_result(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101110000, 20220101111300, 20220101111600, 20220101113850, 20220101114800, 20220101115959]]
      expect_dt = datetime(2022,1,1,11,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

class To_H4_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    
    condenser:CondenserToTf = get_condenser_to_timeframe(TimeFrame.H4)

    def test_WHEN_give_int_values_THEN_get_correct_result(self):
      # Array
      test_values = [20220101000000, 20220101011700, 20220101020022,20220101030900, 20220101035959]
      expect_dt = 20220101000000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101000000, 20220101011700, 20220101020022,20220101030900, 20220101035959]]
      expect_dt = datetime(2022,1,1,00,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_int_values_THEN_get_correct_result2(self):
      # Array
      test_values = [20220101040000, 20220101051700, 20220101070022,20220101070900, 20220101075959]
      expect_dt = 20220101040000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result2(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101040000, 20220101051700, 20220101070022,20220101070900, 20220101075959]]
      expect_dt = datetime(2022,1,1,4,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_int_values_THEN_get_correct_result3(self):
      # Array
      test_values = [20220101080000, 20220101091700, 20220101100022,20220101110900, 20220101115959]
      expect_dt = 20220101080000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result3(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101080000, 20220101091700, 20220101100022,20220101110900, 20220101115959]]
      expect_dt = datetime(2022,1,1,8,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_int_values_THEN_get_correct_result4(self):
      # Array
      test_values = [20220101120000, 20220101131700, 20220101140022,20220101155959]
      expect_dt = 20220101120000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result4(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101120000, 20220101131700, 20220101140022,20220101155959]]
      expect_dt = datetime(2022,1,1,12,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_int_values_THEN_get_correct_result5(self):
      # Array
      test_values = [20220101160000, 20220101171700, 20220101180022,20220101195959]
      expect_dt = 20220101160000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result5(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101160000, 20220101171700, 20220101180022,20220101195959]]
      expect_dt = datetime(2022,1,1,16,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_int_values_THEN_get_correct_result5(self):
      # Array
      test_values = [20220101200000, 20220101211700, 20220101220022,20220101235959]
      expect_dt = 20220101200000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_dt_values_THEN_get_correct_result5(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101200000, 20220101211700, 20220101220022,20220101235959]]
      expect_dt = datetime(2022,1,1,20,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

class To_D_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    
    condenser:CondenserToTf = get_condenser_to_timeframe(TimeFrame.D)

    def test_WHEN_give_int_values_THEN_get_correct_result(self):
      # Array
      test_values = [20220101000000, 20220101023850, 20220101110000, 20220101165958,  20220101204800, 20220101235959]
      expect_dt = 20220101000000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101000000, 20220101023850, 20220101110000, 20220101165958,  20220101204800, 20220101235959]]
      expect_dt = datetime(2022,1,1,00,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

class To_W_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    
    condenser:CondenserToTf = get_condenser_to_timeframe(TimeFrame.W)

    def test_WHEN_give_int_values_THEN_get_correct_result(self):
      # Array
      test_values = [20221128000000,20221129123850, 20221130023850, 20221201110000, 20221202165958,  20221203204800, 20221204235959]
      expect_dt = 20221128000000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_dt_values_THEN_get_correct_result(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20221128000000,20221129123850, 20221130023850, 20221201110000, 20221202165958,  20221203204800, 20221204235959]]
      expect_dt = datetime(2022,11,28,00,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_int_values_THEN_get_correct_result2(self):
      # Array
      test_values = [20230102000000, 20230103123858, 20230104023850, 20230105110000, 20230106165958,  20230107204800, 20230108235959]
      expect_dt = 20230102000000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

    def test_WHEN_give_dt_values_THEN_get_correct_result2(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20230102000000, 20230103123858, 20230104023850, 20230105110000, 20230106165958,  20230107204800, 20230108235959]]
      expect_dt = datetime(2023,1,2,00,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)

class To_M_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    condenser:CondenserToTf = get_condenser_to_timeframe(TimeFrame.M)

    def test_WHEN_give_int_values_THEN_get_correct_result(self):
      # Array
      test_values = [20220101000000, 20220102023850, 20220103110000, 20220112165958,  20220125204800, 20220131235959]
      expect_dt = 20220101000000
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_int(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)
    
    def test_WHEN_give_dt_values_THEN_get_correct_result(self):
      # Array
      test_values = [ datetime.strptime(str(datetime_int),"%Y%m%d%H%M%S") for datetime_int in [20220101000000, 20220102023850, 20220103110000, 20220112165958,  20220125204800, 20220131235959]]
      expect_dt = datetime(2022,1,1,00,00,00)
      for test_value in test_values:
        with self.subTest(i=test_value):
      # Act
          assert_dt = self.condenser.condense_dt(test_value)

      # Assert
          self.assertEqual(expect_dt, assert_dt)