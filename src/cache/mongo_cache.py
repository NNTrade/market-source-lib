from .abs_cache import AbsCache
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Dict, Tuple
import pandas as pd
from NNTrade.common import TimeFrame
from io import StringIO
from .df_split import split_df
from datetime import date

class MongoCache(AbsCache):
  def __init__(self, connection_str:str) -> None:
    """_summary_

    Args:
        connection_str (str): `mongodb://${DB_USERNAME}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}?authSource={auth-db}`
    """
    self.connection_str = connection_str
    self.__database = "finam"
    pass

  def __get_connection(self, database:str, collection:str)->Tuple[MongoClient, Collection]:
    client:MongoClient = MongoClient(self.connection_str)
    mng_db = client[database]
    mng_collection:Collection = mng_db[collection]
    return client, mng_collection

  def __save_cache(self, database:str, collection:str, config:Dict[str,str], data:Dict[str,pd.DataFrame]):
    try:
      mng_clnt, mng_collection = self.__get_connection(database, collection)
      data = { **config, **{ f"__payload_{k}":v.to_csv(sep=";",decimal=",") for k,v in data.items()} }
      replaced = mng_collection.find_one_and_replace(config, data)
      if replaced is not None:
        return replaced["_id"]
      return mng_collection.insert_one(data)
    finally:
      mng_clnt.close()

  def __extract_payload(self, doc)->Dict[str,pd.DataFrame]:
    return {key[10:]:pd.read_csv(StringIO(doc[key]), sep=";", decimal=",", index_col=0)  for key in [k for k in doc.keys() if "__payload_" == k[:10]]}
    
  def __load_splitted_data(self, from_date:date, till_date:date, collection:str, config:str, payload_name:str)->pd.DataFrame:
    from_index = int(from_date.strftime("%Y%m%d")) * 1000000
    till_index = int(till_date.strftime("%Y%m%d")) * 1000000
    try:
      df_arr = []
      mng_clnt, mng_collection = self.__get_connection(self.__database, collection)
      for doc in mng_collection.find(config):
        if doc["index"] >= from_index and doc["index"] < till_index:
          extracted_payload = self.__extract_payload(doc)
          df_arr.append(extracted_payload[payload_name])
      return pd.concat(df_arr).sort_index()
    finally:
      mng_clnt.close()

  def __save_df(self,collection:str, config:str, df:pd.DataFrame, timeframe:TimeFrame, payload_name:str):
    splitted_data = split_df(df, timeframe)
    for key, df in splitted_data.items():
      config["index"] = key
      self.__save_cache(self.__database, collection, config, {payload_name:df})

  def _save_stock_quotes(self, stock:str, timeframe: TimeFrame, quotes_df:pd.DataFrame):
    collection = "quotes"
    config = {"stock":stock, "timeframe":timeframe.short_name()}

    self.__save_df(collection, config, quotes_df, timeframe, "quote")

  def _load_stock_quotes(self, stock:str, timeframe: TimeFrame, from_date:date, till_date:date)->pd.DataFrame:
    collection = "quotes"
    config = {"stock":stock, "timeframe":timeframe.short_name()}
    return self.__load_splitted_data(from_date, till_date, collection, config, "quote")

  def save_aggregated_stock_quotes(self, stock:str, timeframe_base: TimeFrame, timeframe_target:TimeFrame, quotes_df:pd.DataFrame):
    collection = "aggregated_quotes"
    config = {"stock":stock, "timeframe_base":timeframe_base.short_name(), "timeframe_target": timeframe_target.short_name()}
    self.__save_df(collection, config, quotes_df, timeframe_base, "quote")
  
  def load_aggregated_stock_quotes(self, stock:str, timeframe_base: TimeFrame, timeframe_target:TimeFrame, from_date:date, till_date:date)->pd.DataFrame:
    collection = "aggregated_quotes"
    config = {"stock":stock, "timeframe_base":timeframe_base.short_name(), "timeframe_target": timeframe_target.short_name()}
    return self.__load_splitted_data(from_date, till_date, collection, config, "quote")

  def _save_indicator(self, stock:str, timeframe: TimeFrame,indicator:str, indicator_args:Dict[str, float], indicator_df:pd.DataFrame):
    collection = "indicators"
    config = {"stock":stock, "timeframe":timeframe.short_name(), "indicator": indicator, **indicator_args}
    self.__save_df(collection, config, indicator_df, timeframe, "indicator")

  def _load_indicator(self, stock:str, timeframe: TimeFrame,indicator:str, indicator_args:Dict[str, float], from_date:date, till_date:date)->pd.DataFrame:
    collection = "indicators"
    config = {"stock":stock, "timeframe":timeframe.short_name(), "indicator": indicator, **indicator_args}
    return self.__load_splitted_data(from_date, till_date, collection, config, "indicator")

  def save_aggregated_indicator(self, stock:str, timeframe_base: TimeFrame,timeframe_target:TimeFrame, indicator:str, indicator_args:Dict[str, float], indicator_df:pd.DataFrame):
    collection = "indicators"
    config = {"stock":stock, "timeframe_base":timeframe_base.short_name(), "timeframe_target": timeframe_target.short_name(), "indicator": indicator, **indicator_args}
    self.__save_df(collection, config, indicator_df, timeframe_base, "indicator")

  def load_aggregated_indicator(self, stock:str, timeframe_base: TimeFrame,timeframe_target:TimeFrame,indicator:str, indicator_args:Dict[str, float], from_date:date, till_date:date)->pd.DataFrame:
    collection = "aggregated_indicators"
    config = {"stock":stock, "timeframe_base":timeframe_base.short_name(), "timeframe_target": timeframe_target.short_name(), "indicator": indicator, **indicator_args}
    return self.__load_splitted_data(from_date, till_date, collection, config, "indicator")
