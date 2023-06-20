import pickle
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from tickers import all_tickers

tickers = all_tickers

def get_data(data_path="data.pkl", num_of_days=10, ival="15m"):
  # disk
  if os.path.isfile(data_path):
    file = open(data_path, 'rb')
    df = pickle.load(file)
    file.close()
    start_day = df['Close'][tickers[0]].keys()[0].date()
    end_day = df['Close'][tickers[0]].keys()[len(df['Close'][tickers[0]].keys())-1].date()
  # api
  else:
    start_day = (datetime.today() - timedelta(days=num_of_days)).strftime('%Y-%m-%d')
    end_day = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    data = yf.download(" ".join(tickers), start=start_day, end=end_day, interval=ival)
    df = pd.DataFrame(data)
    file = open(data_path, 'wb')
    pickle.dump(df, file)
    file.close()
  return df, start_day, end_day

if __name__ == '__main__':
  get_data()
