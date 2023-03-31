from NNTrade.common import TimeFrame
from typing import Callable
from abc import ABC, abstractmethod
import datetime as dt
from datetime import datetime, timedelta


class CondenserToTf(ABC):
  @abstractmethod
  def condense_dt(self, datetime:datetime)->datetime:
    ...
  @abstractmethod
  def condense_int(self, int_datetime:int)->int:
    ...

class CondenserTo_m1(CondenserToTf):
  def condense_dt(self, datetime:datetime)->datetime:
    return datetime.replace(second=0)
  def condense_int(self, int_datetime:int)->int:
    return int_datetime // 100 * 100

class CondenserTo_m5(CondenserToTf):
  def condense_dt(self, datetime:datetime)->datetime:
    quoter = datetime.minute // 5
    new_minute = 5 * quoter
    ret_dt = datetime.replace(minute=new_minute, second=0)
    return ret_dt
  def condense_int(self, int_datetime:int)->int:
    base_dt = int_datetime // 100
    quoter = base_dt % 10 // 5
    base_dt = base_dt // 10 * 10  + 5 * quoter
    return base_dt * 100
  
class CondenserTo_m10(CondenserToTf):
  def condense_dt(self, datetime:datetime)->datetime:
    quoter = datetime.minute // 10
    new_minute = 10 * quoter
    ret_dt = datetime.replace(minute=new_minute, second=0)
    return ret_dt
  def condense_int(self, int_datetime:int)->int:
    return int_datetime // 1000 * 1000
  
class CondenserTo_m15(CondenserToTf):
  def condense_dt(self, datetime:datetime)->datetime:
    quoter = datetime.minute // 15
    new_minute = 15 * quoter
    ret_dt = datetime.replace(minute=new_minute, second=0)
    return ret_dt
  def condense_int(self, int_datetime:int)->int:
    base_dt = int_datetime // 100
    quoter = base_dt % 100 // 15
    base_dt = base_dt // 100 * 100  + 15 * quoter
    return base_dt * 100
  
class CondenserTo_m30(CondenserToTf):
  def condense_dt(self, datetime:datetime)->datetime:
    quoter = datetime.minute // 30
    new_minute = 30 * quoter
    ret_dt = datetime.replace(minute=new_minute, second=0)
    return ret_dt
  def condense_int(self, int_datetime:int)->int:
    base_dt = int_datetime // 1000
    quoter = base_dt % 10 // 3
    base_dt = base_dt // 10 * 10  + 3 * quoter
    return base_dt * 1000
  
class CondenserTo_H(CondenserToTf):
  def condense_dt(self, datetime:datetime)->datetime:
    ret_dt = datetime.replace(minute=0, second=0)
    return ret_dt
  def condense_int(self, int_datetime:int)->int:
    return int_datetime // 10000 * 10000
  
class CondenserTo_H4(CondenserToTf):
  def condense_dt(self, datetime:datetime)->datetime:
    quoter = datetime.hour // 4
    new_hour = 4 * quoter
    ret_dt = datetime.replace(hour=new_hour,minute=0, second=0)
    return ret_dt
  def condense_int(self, int_datetime:int)->int:
    base_dt = int_datetime // 10000
    quoter = base_dt % 100 // 4
    base_dt = base_dt // 100 * 100 + 4 * quoter
    return base_dt * 10000
  
class CondenserTo_D(CondenserToTf):
  def condense_dt(self, datetime:datetime)->datetime:
    ret_dt = datetime.replace(hour=0, minute=0, second=0)
    return ret_dt
  def condense_int(self, int_datetime:int)->int:
    return int_datetime // 1000000 * 1000000
  
class CondenserTo_W(CondenserToTf):
  def condense_dt(self, datetime:datetime)->datetime:
    base_dt = datetime - dt.timedelta(datetime.weekday())
    ret_dt = base_dt.replace(hour=0, minute=0, second=0)
    return ret_dt
  def condense_int(self, int_datetime:int)->int:
    datetime_str = str(int_datetime)
    dt_val = datetime.strptime(datetime_str,"%Y%m%d%H%M%S")
    base_dt = dt_val - timedelta(dt_val.weekday())
    return int(base_dt.strftime("%Y%m%d")) *  1000000
  
class CondenserTo_M(CondenserToTf):
  def condense_dt(self, datetime:datetime)->datetime:
    ret_dt = datetime.replace(day=1,hour=0, minute=0, second=0)
    return ret_dt
  def condense_int(self, int_datetime:int)->int:
    return ( int_datetime // 100000000 * 100 + 1 ) * 1000000
  
def get_condenser_to_timeframe(timeframe: TimeFrame)->CondenserToTf:
  if timeframe == TimeFrame.m1:
    return CondenserTo_m1()
  elif timeframe == TimeFrame.m5:
    return CondenserTo_m5()
  elif timeframe == TimeFrame.m10:
    return CondenserTo_m10()
  elif timeframe == TimeFrame.m15:
    return CondenserTo_m15()
  elif timeframe == TimeFrame.m30:
    return CondenserTo_m30()
  elif timeframe == TimeFrame.H:
    return CondenserTo_H()
  elif timeframe == TimeFrame.H4:
    return CondenserTo_H4()
  elif timeframe == TimeFrame.D:
    return CondenserTo_D()
  elif timeframe == TimeFrame.W:
    return CondenserTo_W()
  elif timeframe == TimeFrame.M:
    return CondenserTo_M()