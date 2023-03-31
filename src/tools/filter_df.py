import pandas as pd
from datetime import date, datetime, timedelta

def filter_df(df:pd.DataFrame, from_date:date, till_date:date)->pd.DataFrame:
  if from_date is None and till_date is None:
    return df
  
  if from_date is not None:
    from_index = datetime(from_date.year, from_date.month, from_date.day)
  if till_date is not None:
    till_index = datetime(till_date.year, till_date.month, till_date.day) - timedelta(0,0,1)

  if from_date is None or till_date is None:
    if from_date is not None:
      return df.loc[from_index:]
    elif till_date is not None:
      df.loc[: till_index]
  return df.loc[from_index: till_index]