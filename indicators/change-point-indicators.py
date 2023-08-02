# props:
#  - https://github.com/sztistvan/change_detection
#  - https://www.r-bloggers.com/2023/04/building-and-backtesting-a-volatility-based-trading-strategy-with-chatgpt/
#
# chatgpt is cool and all but its hallucinations are troublesome, e.g. the bcp python module.

import os
import scipy
import random
import pickle
import numpy as np
import pandas as pd
import yfinance as yf
import ruptures as rpt
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def get_data(ticker, data_path="data.pkl", num_of_days=500):
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


def detect_changes(time_series):
  signal = time_series.values
  algo = rpt.Pelt(model="rbf", min_size=1, jump=10).fit(signal)
  result = algo.predict(pen=2)
  change_points = [i for i in result if i < len(signal)]
  return change_points


# Get ticker price data and calculate means and std dev
df = get_data(ticker="GOOG")
signal = df['Adj Close']
changes = detect_changes(signal)
lookback_window = 10
# center=True would introduce a look-ahead bias
rolling_mean = signal.rolling(window=lookback_window, center=False).mean()
rolling_std = signal.rolling(window=lookback_window, center=False).std()
upper = rolling_mean + (2*rolling_std)
lower = rolling_mean - (2*rolling_std)


# Plot price, mean, and std dev
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(signal, label='close price', color='blue')
ax.plot(rolling_mean, color='orange', label='mean')
ax.plot(upper, color='green', label='2 std dev')
ax.plot(lower, color='green')
plt.fill_between(signal.index, upper, lower, alpha=0.25, color='green')
ax.set_xlabel('Time')
ax.set_ylabel('Price')
ax.set_title('BUY/SELL Indicators Based on Mean-Reversion and Change Point Detection')


# we use the slope of the rolling mean to indicate a BUY or SELL
#  this makes some assumptions but we're using it for simplicity
ignore_weak_trends = False
for i in changes:
  lookback = rolling_mean[i-lookback_window:i]
  res = scipy.stats.linregress(range(len(lookback)), lookback)
  if ignore_weak_trends and abs(res.slope) < 0.15:
    continue
  if res.slope > 0:
   action = "BUY"
  else:
    action = "SELL"
  ax.axvline(signal.index[i], color='red', linestyle='--')
  ax.text(signal.index[i], signal.min(), action+str(round(res.slope, 2)), color='red', rotation=45)


# If the price goes outside of 2 stddev from the rolling mean,
#  we assume it will revert to the mean "soon"
for idx in range(len(signal)):
  if signal[idx] > upper[idx]:
    plt.scatter(signal.index[idx], signal[idx], color="purple")
    ax.text(signal.index[idx], signal[idx], "SELL", rotation=45)
  if signal[idx] < lower[idx]:
    plt.scatter(signal.index[idx], signal[idx], color="purple")
    ax.text(signal.index[idx], signal[idx], "BUY", rotation=45)


ax.legend()
plt.show()
