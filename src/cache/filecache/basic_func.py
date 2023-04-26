from typing import List, Dict
import os
import json
import pandas as pd
from ...quotes.DfCondenser import AGGR_INDEX

def join_cache_path_arr(start_path, paths:List[str])->str:
    _return = start_path
    for path in paths:
      _return = join_cache_path(_return, path)
    return _return

def join_cache_path(start_path, end_path)->str:
  cache_path = os.path.join(start_path, end_path)
  if not os.path.exists(cache_path):
    os.mkdir(cache_path)
  return cache_path

def get_file_path_csv(cache_folder:str, cache_name:str)->str:
  return os.path.join(cache_folder, f"{cache_name}.csv")

def get_file_path_json(cache_folder:str, cache_name:str)->str:
  return os.path.join(cache_folder, f"{cache_name}.json")

def save_dic(file_path:str, dic: Dict[str,any])->str:
  if os.path.exists(file_path):
    raise Exception(f"Cache file {file_path} already exist")
  json_str = json.dumps(dic)
  if os.path.exists(file_path):
    os.remove(file_path)
  with open(file_path, 'w') as convert_file:
    convert_file.write(json_str)

def save_df(file_path:str, df:pd.DataFrame, overwrite:bool = False):
  if os.path.exists(file_path) and not overwrite:
    raise Exception(f"Cache file {file_path} already exist")
  df.to_csv(file_path, sep=";",decimal=",")

def load_df(file_path:str, header_cols:List[int] = [0])->pd.DataFrame:
  if not os.path.exists(file_path):
    raise Exception(f"Cache file {file_path} doesn't exist")
  df = pd.read_csv(file_path, sep=";", decimal=",", index_col=0, header=header_cols)
  df.index = pd.to_datetime(df.index)
  if AGGR_INDEX in df.columns:
    df[AGGR_INDEX] = pd.to_datetime(df[AGGR_INDEX])
  return df.sort_index()

def config_to_name(indicator_args:Dict[str, float])->str:
    args_key = list(indicator_args.keys())
    args_key.sort()
    return str.join("__", [f"{key}-{str(indicator_args[key])}" for key in args_key])