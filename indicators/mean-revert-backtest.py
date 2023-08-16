
import os
import pickle
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict


def get_data(ticker, data_path="data.pkl", num_of_days=365*3):
  # check to see if there's a cache on disk and read from it
  if os.path.isfile(data_path):
    file = open(data_path, 'rb')
    df = pickle.load(file)
    file.close()
  # if there's no cache, Grab it from the API and write it to disk
  else:
    end_day = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    start_day = (datetime.today() - timedelta(days=num_of_days)).strftime('%Y-%m-%d')
    data = yf.download(ticker, start=start_day, end=end_day)
    df = pd.DataFrame(data)
    file = open(data_path, 'wb')
    pickle.dump(df, file)
    file.close()
  return df



# Get ticker price data and calculate means and std dev
df = get_data(ticker="GOOG")
signal = df['Adj Close']
lookback_window = 10
rolling_mean = signal.rolling(window=lookback_window, center=False).mean()
rolling_std = signal.rolling(window=lookback_window, center=False).std()
upper = rolling_mean + (2*rolling_std)
lower = rolling_mean - (2*rolling_std)


# number of days to wait before flattening our position
flatten = [1,2,3,4,5]
fig, ax = plt.subplots(len(flatten))
Ys = defaultdict(list)
Xs = defaultdict(list)

for idx in range(len(signal)):

  # if the price is above the 2stddev window, sell it
  if signal[idx] > upper[idx]:
    action = "SELL_"
    for days in flatten:
      try:
        Ys[days].append(signal[idx] - signal[idx+days])
      except:
        Ys[days].append(0) # we cannot look ahead that many days
      Xs[days].append(signal.index[idx])

  # if the price is below the 2stddev window, buy it
  if signal[idx] < lower[idx]:
    action = "BUY_"
    for days in flatten:
      Ys[days].append(signal[idx] - signal[idx+days])
      Xs[days].append(signal.index[idx])

# plot cumulative P/L
for idx in range(len(flatten)):
  ax[idx].plot(Xs[flatten[idx]], np.cumsum(Ys[flatten[idx]]).tolist(), color='black')
  ax[idx].set_title("Hold for " + str(flatten[idx]) + "days. P/L: " + str(sum(Ys[flatten[idx]])))

plt.show()
