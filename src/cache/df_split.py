import pandas as pd
from NNTrade.common import TimeFrame
from typing import Dict

def split_df(data_df:pd.DataFrame, timeframe:TimeFrame)->Dict[int, pd.DataFrame]:
  if timeframe in [TimeFrame.m1, TimeFrame.m5, TimeFrame.m10, TimeFrame.m15, TimeFrame.m30]:
    devider = 1000000
  elif timeframe in [TimeFrame.H, TimeFrame.H4, TimeFrame.D, TimeFrame.W, TimeFrame.M]:
    devider = 10000000000
  else:
    raise Exception("Unexpected timeframe")
  unique_idx = list(dict.fromkeys([idx // devider for idx in data_df.index]))
  return_dic = {idx*devider:data_df.loc[idx*devider:(idx+1)*devider-1] for idx in unique_idx}
  return return_dic
      